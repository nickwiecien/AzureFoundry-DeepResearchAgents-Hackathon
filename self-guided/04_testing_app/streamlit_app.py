import streamlit as st
from datetime import datetime
import requests
import os
from dotenv import load_dotenv

load_dotenv(override=True)


# Dummy chat function
# This function will be called when the user submits a chat prompt
# Replace this with your actual chat handler as needed


now = datetime.now()
now_str = now.strftime("%Y-%m-%d")


default_report_prompt = (
        f"""# Research Analyst Brief  
You are an expert research analyst. Today is {now_str}.

Your task is to generate a detailed Markdown report (7–10 pages) on a designated research topic, based strictly on the cited research provided.  This should be a written report in the style of an academic research paper or investigative news article.
All insights and analysis MUST be grounded in the information provided.

> **Important:** When discussing findings, always reference specific data points, sources, or subtopics. Avoid speculation or generalization unsupported by evidence.

---

## Report Audience:
This report is intended for an informed but non-specialist audience, including educators, business leaders, or policy-makers—depending on the topic.

---

## Report Requirements:

### 1. Executive Summary
- Begin with a clear, high-level summary of the most important insights, findings, or takeaways from your research.
- Highlight any surprising patterns, significant implications, or overarching themes.

### 2. Key Themes or Focus Areas
- Identify 3–5 major themes, categories, or lines of inquiry relevant to the topic (e.g., historical evolution, biological mechanisms, cultural impact, geographic variation).
- For each theme:
  - Provide a structured breakdown of findings.
  - Include key data points, explanations, or summaries.
  - Present information using written paragraphs with inline source citations.
  - Include subsections and tableswhere appropriate.
  - Citations should be in the same format as the initial research findings provided and included inline. Assume these will be viewed on a display screen, so use clickable links.

### 3. Comprehensive Topic Overview
- Provide a broader contextual analysis of the subject.
- Include:
  - Timeline of major developments (if applicable)
  - Comparative analysis across relevant cases or subtopics
  - Tables summarizing data points, events, or classifications

### 4. Data Presentation & Structure
- Use Markdown formatting throughout the report:
  - Headings and subheadings
  - Detailed written paragraphs for narrative explanations. Prioritize news-report style paragraphs over bullet points for in-depth analysis.
  - Tables with clearly labeled rows/columns
  - Inline links (if web-based)

### 5. Analytical Depth
- Draw conclusions supported directly by the data or source material.
- Distinguish clearly between well-supported facts and observations that are tentative or limited.
- Emphasize causal relationships, patterns, or implications when possible.

### 6. Audience-Focused Writing
- Write in clear, accessible language suitable for professionals or stakeholders with varying levels of technical knowledge.
- Avoid excessive jargon unless essential—and always define terms when introduced.
- Keep tone professional, objective, and informative.

### 7. Sourcing
- Base your analysis solely on the research findings provided to you.
- It is critical that you include primary source citations in your report from the provided research.
- **IMPORTANT**: Assume that this report will be viewed on a display screen and use clickable links for citations.
---

## Purpose:
Deliver a well-structured, evidence-based report that deepens understanding of the topic, informs future inquiry, and supports decision-making, education, or strategic planning depending on the context."""
    )

if "research_agent_prompt" not in st.session_state:
    st.session_state["research_agent_prompt"] = ''
if "report_agent_prompt" not in st.session_state:
    st.session_state["report_agent_prompt"] = default_report_prompt
if 'messages' not in st.session_state:
    st.session_state.messages = []

st.set_page_config(layout="wide")  
st.title('Azure AI Foundry Agents - Deep Research Demo')
st.write('Demo application showcasing a "Deep Research" style approach for generating detailed research reports based on research findings from Azure AI Foundry Agents.')

# Expandable panel for deep research settings
with st.expander("Deep Research Settings"):
    # Numeric inputs side by side
    col1, col2 = st.columns(2)
    depth = col1.number_input(
        label="Depth",
        min_value=0,
        step=1,
        value=3,
        help="Set how deep the research should go"
    )
    breadth = col2.number_input(
        label="Breadth",
        min_value=0,
        step=1,
        value=3,
        help="Set how wide the research scope should be"
    )

    # Text areas side by side
    report_agent_prompt = st.text_area(
        label="Report Agent Prompt",
        placeholder="Enter prompt for the report agent",
        key="report_agent_prompt",
        height=400  # Approximate 10 lines
    )

# Chat bar at the bottom of the page
prompt = st.chat_input("Enter a research topic to explore...")
if prompt:
    # Display user's chat message
    st.chat_message("user").write(prompt)
    # Call the dummy chat function and display its response
    with st.chat_message("assistant"):
        placeholder2 = st.markdown(body="")
        partial_response = ""


        payload = {
            "query": prompt,
            "report_prompt": st.session_state["report_agent_prompt"],
            "depth": depth,
            "breadth": breadth,
            "agent_id": os.environ.get("AGENT_ID", "default_agent_id"),
        }
        

        try:
            uri = '127.0.0.1:8000' # Updaate this to your API endpoint
            response = requests.post(f'http://{uri}/run_deep_research_stream', json=(payload), stream=True)
            if response.status_code == 200:
                for chunk in response.iter_content( decode_unicode=True):
                    if chunk:
                       
                        partial_response += chunk.replace("```","")
                        placeholder2.markdown(partial_response, unsafe_allow_html=True)
                        
            else:
                partial_response = f"Error from API: {response.status_code} - {response.text}"
                placeholder2.markdown(partial_response)
        except Exception as e:
            partial_response = f"Request failed: {e}"
            placeholder2.markdown(partial_response)

        placeholder2.markdown(partial_response, unsafe_allow_html=True)
        

    st.session_state["messages"].append({"role": "assistant", "content": partial_response})