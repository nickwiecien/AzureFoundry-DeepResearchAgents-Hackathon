# Deep Research API

A FastAPI-based research orchestration service that conducts multi-layered research using Azure AI Foundry agents. This API implements a sophisticated research methodology that combines breadth-first exploration with depth-first investigation to produce comprehensive research reports.

## 🎯 Overview

The Deep Research API transforms simple research queries into comprehensive, multi-source investigations by:

1. **Query Generation**: Breaking down research topics into specific, targeted questions
2. **Parallel Research**: Executing multiple research threads simultaneously using Azure AI agents
3. **Progressive Deepening**: Following up on initial findings with more specific investigations
4. **Intelligent Synthesis**: Using advanced reasoning models to compile findings into comprehensive reports

## 🔧 How It Works

### Research Methodology

```
Initial Query → Query Generation → Parallel Agent Calls → Distillation → Follow-up Questions
       ↓                ↓                    ↓               ↓              ↓
   "AI in Manufacturing" → ["What are current AI applications?", "ROI of AI implementation?"] 
                           → [Agent Research] → [Key Learnings] → ["What about safety concerns?"]
```

### Architecture

```
┌─────────────────┐    ┌─────────────────┐    ┌─────────────────┐
│   FastAPI       │    │   Research      │    │  Azure AI       │
│   Endpoints     │◄──►│   Orchestrator  │◄──►│  Foundry Agent  │
└─────────────────┘    └─────────────────┘    └─────────────────┘
         │                       │                       │
         ▼                       ▼                       ▼
┌─────────────────┐    ┌─────────────────┐    ┌─────────────────┐
│   Streaming     │    │   Reasoning     │    │   Data Sources  │
│   Response      │    │   Engine (o1)   │    │   (Bing, etc.)  │
└─────────────────┘    └─────────────────┘    └─────────────────┘
```

## 🚀 Getting Started

### Prerequisites

1. **Azure AI Foundry Project** with an active research agent
2. **Environment Variables** configured (see `.env.sample` in project root)
3. **Python 3.11+** with required dependencies

### Required Environment Variables

```bash
# Azure AI Foundry
PROJECT_ENDPOINT=your_azure_ai_foundry_endpoint
AGENT_ID=your_research_agent_id

# Azure OpenAI (for reasoning and synthesis)
AOAI_ENDPOINT=your_azure_openai_endpoint
AOAI_KEY=your_azure_openai_key
AOAI_GPT_MODEL=gpt-4o
AOAI_REASONING_MODEL=o1-mini
```

### Installation

1. **Install dependencies**:
   ```bash
   pip install fastapi uvicorn azure-ai-projects azure-identity python-dotenv openai
   ```

2. **Set up environment**:
   ```bash
   # Copy environment template from project root
   cp ../../.env.sample ../../.env
   # Edit .env with your Azure credentials
   ```

### Running the API

**Start the server with uvicorn**:
```bash
uvicorn deep_research_api:app --host 0.0.0.0 --port 8000 --reload
```

**Alternative startup options**:
```bash
# Development mode with auto-reload
uvicorn deep_research_api:app --reload

# Production mode
uvicorn deep_research_api:app --host 0.0.0.0 --port 8000 --workers 4

# Custom host and port
uvicorn deep_research_api:app --host 127.0.0.1 --port 3000
```

## 📡 API Endpoints

### POST `/run_deep_research_stream`

Executes deep research with real-time streaming responses.

**Request Body**:
```json
{
  "query": "Impact of artificial intelligence on manufacturing efficiency",
  "breadth": 3,
  "depth": 4,
  "report_prompt": "Generate a comprehensive business report...",
  "agent_id": "your_agent_id_here"
}
```

**Parameters**:
- `query` (string, required): The research topic or question
- `breadth` (integer, default: 3): Number of initial research questions to generate
- `depth` (integer, default: 4): How many levels deep to investigate follow-up questions
- `report_prompt` (string, required): Instructions for final report generation
- `agent_id` (string, optional): Specific agent ID to use (defaults to `AGENT_ID` env var)

**Response**: Streaming text/plain with real-time research progress and final report

## 🔄 Research Process

### 1. Query Generation
The API breaks down your research topic into specific, targeted questions:
```
Topic: "Sustainable manufacturing processes"
Generated Queries:
- "What are the latest innovations in sustainable manufacturing?"
- "How do companies measure sustainability in manufacturing?"
- "What are the cost implications of sustainable practices?"
```

### 2. Parallel Research
Each generated query is sent to Azure AI Foundry agents simultaneously, leveraging:
- **BingGroundingService** for current web information
- **Multiple data sources** for comprehensive coverage
- **Concurrent processing** for faster results

### 3. Learning Distillation
Research results are processed to extract:
- **Key learnings** with source citations
- **Follow-up questions** for deeper investigation
- **Relevant insights** related to the original query

### 4. Progressive Deepening
The system automatically generates and researches follow-up questions:
```
Initial: "What are AI applications in manufacturing?"
Follow-up: "What are the safety implications of AI in manufacturing?"
Deeper: "How do companies ensure AI safety compliance?"
```

### 5. Final Report Generation
Uses advanced reasoning models (o1-mini) to synthesize all findings into a comprehensive report.

## 🎛️ Configuration

### Research Parameters

**Breadth (1-10)**:
- Controls initial question generation
- Higher values = broader initial exploration
- Recommended: 3-5 for balanced research

**Depth (1-6)**:
- Controls follow-up investigation levels
- Higher values = deeper, more detailed research
- Recommended: 3-4 for comprehensive coverage

### Performance Tuning

**Concurrency Settings**:
```python
CONCURRENCY = 5  # Maximum parallel agent calls
```

**Model Configuration**:
```python
GPT_MODEL = "gpt-4o"        # For query generation and distillation
REASONING_MODEL = "o1-mini"  # For final report synthesis
```

## 📊 Example Usage

### Basic Research Request
```bash
curl -X POST "http://localhost:8000/run_deep_research_stream" \
     -H "Content-Type: application/json" \
     -d '{
       "query": "Latest developments in renewable energy storage",
       "breadth": 3,
       "depth": 3,
       "report_prompt": "Generate a technical analysis report for engineers"
     }'
```

### Advanced Research Request
```bash
curl -X POST "http://localhost:8000/run_deep_research_stream" \
     -H "Content-Type: application/json" \
     -d '{
       "query": "Market opportunities for sustainable packaging",
       "breadth": 5,
       "depth": 4,
       "report_prompt": "Create a business intelligence report focusing on market size, growth trends, key players, and investment opportunities",
       "agent_id": "your_specific_agent_id"
     }'
```

## 🔍 Monitoring and Debugging

### API Documentation
- Visit `http://localhost:8000/docs` for interactive API documentation
- View OpenAPI schema at `http://localhost:8000/openapi.json`

### Logging
The API provides real-time feedback during research:
- Research topic announcements
- Progress updates
- Learning discoveries
- Report generation status

### Error Handling
Common issues and solutions:
- **Agent not found**: Verify `AGENT_ID` in environment variables
- **Authentication errors**: Check Azure credentials and permissions
- **Rate limiting**: Adjust `CONCURRENCY` setting for your Azure quotas

## 🚀 Deployment

### Docker Deployment
```dockerfile
FROM python:3.11-slim
COPY requirements.txt .
RUN pip install -r requirements.txt
COPY deep_research_api.py .
EXPOSE 8000
CMD ["uvicorn", "deep_research_api:app", "--host", "0.0.0.0", "--port", "8000"]
```

### Azure Container Apps
```bash
# Build and deploy to Azure Container Apps
az containerapp create \
  --name deep-research-api \
  --resource-group your-resource-group \
  --image your-container-registry/deep-research-api:latest \
  --target-port 8000 \
  --ingress external
```

## 🔧 Integration

### With Streamlit Apps
```python
import requests
import streamlit as st

response = requests.post(
    "http://localhost:8000/run_deep_research_stream",
    json={
        "query": user_query,
        "breadth": breadth_setting,
        "depth": depth_setting,
        "report_prompt": report_instructions
    },
    stream=True
)

for chunk in response.iter_content(decode_unicode=True):
    st.write(chunk)
```

### With Other Applications
The API returns streaming text responses, making it easy to integrate with:
- Web applications (JavaScript fetch with streaming)
- Python applications (requests with stream=True)
- Command-line tools (curl with streaming)

## 📈 Performance Considerations

- **Concurrency**: Adjust based on Azure AI quotas and rate limits
- **Depth vs Speed**: Higher depth values increase research quality but take longer
- **Breadth vs Focus**: Higher breadth values provide broader coverage but may dilute focus
- **Token Usage**: Monitor Azure OpenAI token consumption for cost management

## 🆘 Troubleshooting

**Common Issues**:

1. **"Agent not found"**
   - Verify `AGENT_ID` environment variable
   - Ensure agent exists in your Azure AI Foundry project

2. **"Authentication failed"**
   - Check Azure credentials (`az login`)
   - Verify Azure AI Foundry permissions

3. **"Rate limit exceeded"**
   - Reduce `CONCURRENCY` setting
   - Check Azure service quotas

4. **Slow responses**
   - Reduce `depth` parameter
   - Check network connectivity to Azure services

**For additional support**, refer to the main project README and Azure AI Foundry documentation.
