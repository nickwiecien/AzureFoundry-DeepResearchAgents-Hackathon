from __future__ import annotations
import asyncio
import os
from dataclasses import dataclass, field
from datetime import datetime, timezone
from typing import List, Sequence

import openai
from fastapi import FastAPI, HTTPException
from pydantic import BaseModel, Field
from azure.core.credentials import AzureKeyCredential
from azure.search.documents import SearchClient
from openai import AzureOpenAI
import json
from dotenv import load_dotenv
import wikipediaapi
import requests

import os
from azure.ai.projects import AIProjectClient
from azure.identity import DefaultAzureCredential
from azure.ai.agents.models import CodeInterpreterTool, MessageRole, FilePurpose, MessageAttachment, CodeInterpreterToolDefinition

# --------------------------------------------------------------------- #
# 0️⃣  Configuration
# --------------------------------------------------------------------- #
load_dotenv(override=True)  # Load environment variables from a .env file
GPT_MODEL = os.getenv("AOAI_GPT_MODEL", "gpt-4.1")
REASONING_MODEL = os.getenv("AOAI_REASONING_MODEL", "o4-mini")

DEFAULT_TOP_K = 2
CONCURRENCY = 2

# --------------------------------------------------------------------- #
# 1️⃣  Small helpers
# --------------------------------------------------------------------- #

def chat(messages, **kw) -> str:
    """Return content of first OpenAI completion choice."""
    client = AzureOpenAI(
        azure_endpoint = os.environ['AOAI_ENDPOINT'], 
        #   azure_ad_token_provider=token_provider,
        api_version="2025-04-01-preview", # You must use this version or greater to access reasoning summary
        api_key = os.environ['AOAI_KEY']
        )
    resp = client.chat.completions.create(model='gpt-4.1', messages=messages, **kw)
    return resp.choices[0].message.content

def reason(messages, **kw) -> str:
    """Return content of first OpenAI completion choice."""
    client = AzureOpenAI(
        azure_endpoint = os.environ['AOAI_ENDPOINT'],  
        #   azure_ad_token_provider=token_provider,
        api_version="2025-04-01-preview", # You must use this version or greater to access reasoning summary
        api_key = os.environ['AOAI_KEY']
        )
    resp = client.chat.completions.create(model='o4-mini', messages=messages, max_completion_tokens=15000, **kw)
    return resp.choices[0].message.content

async def invoke_agent(question, original_topic, agent_id):

    project_endpoint = os.environ["PROJECT_ENDPOINT"]  # Ensure the PROJECT_ENDPOINT environment variable is set
    if not agent_id:
        agent_id = os.environ['AGENT_ID']
    # Create an AIProjectClient instance
    project_client = AIProjectClient(
        endpoint=project_endpoint,
        credential=DefaultAzureCredential(),  # Use Azure Default Credential for authentication
    )
    # Call agent
    thread = project_client.agents.threads.create()
    message = project_client.agents.messages.create(
        thread_id=thread.id,
        role=MessageRole.USER,
        content=f'Topic: {original_topic}\nQuestion: {question}',
    )

    run = project_client.agents.runs.create_and_process(thread_id=thread.id, agent_id=agent_id)

    if run.status == "completed":
        m = project_client.agents.messages.get_last_message_by_role(thread_id=thread.id, role=MessageRole.AGENT)
        citations = m.url_citation_annotations
        if len(citations) > 0:
            citations = [x.as_dict() for x in citations]

        updated_text = ''
        if len(m.content) > 0:
            for entity in m.content:
                if entity.type=='text':
                    updated_text += entity.text.value
        for citation in citations:
            formatted_citation = f"[{citation['url_citation']['title']}]({citation['url_citation']['url']}) "
            updated_text = updated_text.replace(citation['text'], formatted_citation)

        # out_messages = [msg for msg in out_messages]


        # Summarize the key learnings
        messages = [{'role': 'system', 'content': f'You review output from a researcher on a given topic and distill succinct learnings. These learnings should be no more than 5 **very detailed** bullet points containing the most relevant information obtained. These bullets should contain sufficient detail and EACH BULLET SHOULD CONTAIN A SOURCE CITATION. **IMPORTANT:** Your source citations should retain the citation format from the initial research, often a website title with URL. **DO NOT** include a list of sources separate from the bulleted learnings. Your learnings should be relevant to the following question: {question}'},
                    {'role': 'user', 'content': json.dumps(updated_text)}]
        
        response = chat(messages, temperature=0.0, max_tokens=2000)
    
        return response

# --------------------------------------------------------------------- #
# 2️⃣  Pydantic + dataclasses
# --------------------------------------------------------------------- #
class Query(BaseModel):
    query: str

class QueryList(BaseModel):
    queries: List[Query]

class Processed(BaseModel):
    learnings: List[str] = Field(default_factory=list)
    follow_up_questions: List[str] = Field(default_factory=list)

@dataclass
class State:
    learnings: List[str] = field(default_factory=list)
    sources: List[str] = field(default_factory=list)

# --------------------------------------------------------------------- #
# 3️⃣  LLM steps
# --------------------------------------------------------------------- #
async def make_queries(prompt: str, k: int, prior: Sequence[str] | None, system_prompt=''):
    block = ("\nHere are previous learnings:\n" + "\n".join(prior)) if prior else ""
    raw = chat(
        [
            {"role": "system", "content": "You generate research inquiries based on a research topic or question. You should generate unique questions that are relevant to the topic and can be asked of a subject matter expert."},
            {"role": "user",
             "content": f"Generate ≤{k} UNIQUE questions about the research topic or question presented here. These questions should be framed as though they were being asked of a subject matter expert in the area.\n## TOPIC/QUESTION: {prompt}</prompt>{block}."}
        ],
        temperature=0.0,
        max_tokens=800,
        response_format = {
            "type": "json_schema",
            "json_schema": {
                "name": "queries",
                "schema": {
                    "type": "object",
                    "properties": {
                        "queries": {
                            "type": "array",
                            "items": {
                                "type": "object",
                                "properties": {
                                    "query": {"type": "string"},
                                },
                                "required": ["query"],
                                "additionalProperties": False
                            }
                        }
                    },
                    "required": ["queries"],
                    "additionalProperties": False
                },
                "strict": True
            }
        }

    )
    parsed = QueryList.model_validate_json(raw)
    for q in parsed.queries:
        print('Query: ' + q.query)
        print()
        # pass
    return QueryList.model_validate_json(raw).queries[:k]

async def distil(query: str, docs, n_learn=3, n_q=3):
    # print(docs)
    content = docs
    raw = chat(
        [
            {"role": "system", "content": 'You generate follow up questions for a research topic or question based on learnings from previous research.'},
            {"role": "user",
             "content": f"Generate {n_q} follow‑up questions for this question ## QUESTION: {query}\n\n These follow ups should be based on the following learnings.:\n{content}"},
             
        ],
        temperature=0.0,
        max_tokens=2000,
        response_format = {
            "type": "json_schema",
            "json_schema": {
                "name": "processing",
                "schema": {
                    "type": "object",
                    "properties": {
                        "follow_up_questions": {
                            "type": "array",
                            "items": {"type": "string"}
                        }
                    },
                    "required": ["follow_up_questions"],
                    "additionalProperties": False
                },
                "strict": True
            }
        }

    )

    return Processed.model_validate_json(raw)


async def final_report(prompt: str, learnings: Sequence[str], sources: Sequence[str], system_prompt=''):
    # print(len(learnings))
    # print(learnings)
    block = "\n".join(f"<l>{l}</l>" for l in learnings)
    raw = reason(
        [
            {"role": "system", "content": system_prompt},
            {"role": "user",
             "content": f"## Original Research Question/Topic: {prompt}\n\n##Research learnings: {block}"},
        ],
        # response_format={"type": "json_object"},
        reasoning_effort="medium"
    )
    body = raw
    return body
    # return body + "\n\n## Sources\n" + "\n".join(f"- `{s}`" for s in sources)

# --------------------------------------------------------------------- #
# 4️⃣  Recursive research engine
# --------------------------------------------------------------------- #
async def deep_research(prompt: str, *, breadth: int, depth: int,
                        state: State | None = None,
                        sem: asyncio.Semaphore | None = None) -> State:
    state = state or State()
    sem = sem or asyncio.Semaphore(CONCURRENCY)

    queries = await make_queries(prompt, k=breadth, prior=state.learnings)

    async def handle(sq: Query):
        async with sem:
            docs = await invoke_agent(sq.query)
        ids, _ = zip(*docs) if docs else ((), ())
        proc = await distil(sq.query, docs)

        state.learnings.extend(proc.learnings)
        state.sources.extend(ids)

        if depth - 1 > 0 and proc.follow_up_questions:
            nxt = f"Goal: {sq.research_goal}\n" + "\n".join(proc.follow_up_questions)
            await deep_research(nxt, breadth=max(1, breadth // 2),
                                depth=depth - 1, state=state, sem=sem)

    await asyncio.gather(*(handle(q) for q in queries))

    # dedupe
    state.learnings = list(dict.fromkeys(state.learnings))
    state.sources = list(dict.fromkeys(state.sources))
    return state


##### --------------------------------------------------------------------- #
# 5️⃣  FastAPI app
app = FastAPI()  # Create a FastAPI application instance

load_dotenv(override=True)  # Load environment variables from a .env file  
from fastapi.responses import StreamingResponse

from pydantic import BaseModel

class ResearchParams(BaseModel):
    query:    str
    breadth:  int = 3
    depth:    int = 4
    report_prompt: str
    agent_id: str = Field(default=os.getenv("AGENT_ID", ""))


CONCURRENCY = 5  # max parallel worker threads  
import threading  # Import threading for creating and managing threads  
import queue  # Import queue for creating a queue to handle data between threads  
import tempfile  # Import tempfile for creating temporary files and directories  
@app.post("/run_deep_research_stream")  
async def run_deep_research_stream(params: ResearchParams):  
    """  
    Streams deep research in the same style as your `run_agent` example:  
    - spawn a single “driver” thread  
    - communicate via queue.Queue  
    - return a generator that yields queue items until a sentinel  
    """  
    def generate_response():  
        q: queue.Queue[str] = queue.Queue()  
        state = State()  
        threads: list[threading.Thread] = []  
        sem = threading.Semaphore(CONCURRENCY)  
        researched_topics = set()
  
        def worker(sq: Query, depth: int):  
            with sem:  
                # 1️⃣ announce the goal  
                if sq.query not in researched_topics:
                    researched_topics.add(sq.query)  
                    #q.put(f"🔍 Researching: {sq.query}<br/>")
                    # q.put(f"<span style='color:dodgerblue;'><b>Research Topic: </b></span>{sq.query}<br/>")  
  
                # 2️⃣ do the search  
                docs = asyncio.run(invoke_agent(sq.query, params.query, params.agent_id)) 
                # print(docs, flush=True) 
                # q.put(f"  • Retrieved {len(docs)} Reviews\n")  
  
                # 3️⃣ distill learnings  
                proc = asyncio.run(distil(sq.query, docs))  
                q.put(f"<span style='color:dodgerblue;'><b>Research Topic: </b></span>{sq.query}<br/>") 
                q.put("<span style='color:limegreen;'><b>Learnings:</b></span><br/>")  
                # for learning in proc.learnings:  
                q.put(f"&emsp; • {docs}<br/>")
                q.put("<br/>")  
  
                # 4️⃣ record in state  
                state.learnings.append(docs)  
                # state.sources.extend(doc_id for doc_id, _ in docs)  
  
                # 5️⃣ spawn follow-ups  
                if depth > 1 and proc.follow_up_questions:  
                    for fu in proc.follow_up_questions:  
                        child = Query(query=fu)  
                        t = threading.Thread(target=worker, args=(child, depth - 1))  
                        t.start()  
                        threads.append(t)  
  
        def run_research():  
            # Kick off  
            
            q.put("⚗️ Generating initial research inquiries…<br/><br/>")  
            queries = asyncio.run(make_queries(params.query, k=params.breadth, prior=None))  
  
            # Fan-out initial workers  
            for query_item in queries:  
                t = threading.Thread(target=worker, args=(query_item, params.depth))  
                t.start()  
                threads.append(t)  
  
            # Wait for all workers  
            for t in threads:  
                t.join()  
  
            # Final report  
            q.put("<h2>✅ Research complete. Generating a final report with o4-mini…</h2><br/><br/>")  
     
            report = asyncio.run(final_report(params.query, state.learnings, state.sources, params.report_prompt))  
            q.put(report + "\n")  
  
            # Sentinel  
            q.put("<<DONE>>")  
  
        # Start the driver thread  
        driver = threading.Thread(target=run_research, daemon=True)  
        driver.start()  
  
        # Synchronous generator that yields until we see "<<DONE>>"  
        while True:  
            chunk = q.get()  
            if chunk == "<<DONE>>":  
                break  
            if chunk is None:  
                continue  
            yield chunk  
  
        # Clean up  
        driver.join()  
  
    return StreamingResponse(generate_response(), media_type="text/plain") 