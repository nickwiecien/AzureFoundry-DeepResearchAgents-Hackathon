# src/api/wikipedia_api.py
from fastapi import FastAPI, Query
from fastapi.middleware.cors import CORSMiddleware
from typing import List, Optional
import wikipediaapi
import requests

app = FastAPI(
    title="3M-Hackathon-Testing-API",
    description="API for 3M Hackathon testing endpoints, including Wikipedia search.",
    version="1.0.0",
    docs_url="/docs",
    openapi_url="/openapi.json"
)

# Allow CORS for all origins (customize as needed)
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

@app.get("/search/wikipedia", tags=["Wikipedia"], summary="Search Wikipedia articles", response_model=List[dict])
async def search_wikipedia_articles(
    keywords: str = Query(..., description="Keywords to search for in Wikipedia articles."),
    max_results: int = Query(5, ge=1, le=20, description="Maximum number of articles to return (1-20).")
):
    """
    Search Wikipedia for articles matching the given keywords. Returns a list of article titles and URLs (with a snippet of the article text).
    """
    wiki_wiki = wikipediaapi.Wikipedia(user_agent='your-user-agent', language='en')
    search_url = "https://en.wikipedia.org/w/api.php"
    params = {
        'action': 'query',
        'list': 'search',
        'srsearch': keywords,
        'format': 'json'
    }
    response = requests.get(search_url, params=params)
    search_results = response.json().get('query', {}).get('search', [])
    articles = []
    for result in search_results[:max_results]:
        title = result['title']
        page = wiki_wiki.page(title)
        if page.exists():
            url = f'https://en.wikipedia.org/wiki/{page.title.replace(" ", "_")}'
            snippet = page.text
            articles.append({"title": title, "url": url, "content": snippet})
        else:
            articles.append({"title": title, "url": None, "snippet": "Page not found"})
    return articles
