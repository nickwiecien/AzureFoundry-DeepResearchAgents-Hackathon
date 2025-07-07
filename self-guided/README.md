# Self-Guided Azure AI Foundry Agent Development

This section contains a complete self-guided walkthrough for building and testing Azure AI Foundry agents with web research capabilities. Follow the numbered directories in sequence to build a complete deep research system.

## Overview

This tutorial demonstrates how to create a sophisticated research system using Azure AI Foundry agents that can:
- Perform comprehensive web research using Bing Search
- Generate detailed analytical reports
- Provide interactive web interfaces for research queries

## Prerequisites

Before starting, ensure you have:

1. **Azure AI Foundry Project** set up with appropriate permissions
2. **Environment Variables** configured in the root `.env` file:
   ```bash
   # Azure AI Foundry Configuration
   AZURE_AI_FOUNDRY_ENDPOINT=your_azure_ai_foundry_endpoint
   MODEL_DEPLOYMENT_NAME=your_model_deployment_name
   
   # Optional: Bing Connection (if using specific Bing connection)
   BING_CONNECTION_ID=your_bing_connection_id
   
   # Agent IDs (will be populated as you create agents)
   WEB_RESEARCH_AGENT_ID=your_web_research_agent_id
   ```

3. **Python Dependencies** installed:
   ```bash
   pip install azure-ai-projects azure-identity python-dotenv streamlit requests ipython
   ```

4. **Azure Authentication** configured (Azure CLI login or service principal)

## Directory Structure

```
self-guided/
├── 01_agent_creation/          # Create the web research agent
├── 02_agent_testing/           # Test the agent functionality  
├── 03_deep_research_api/       # Build API for advanced research
├── 04_application/             # Streamlit web application
└── README.md                   # This file
```

## Step-by-Step Guide

### 01. Agent Creation (`01_agent_creation/`)

**File:** `web_research_agent.ipynb`

**Purpose:** Creates an Azure AI Foundry agent equipped with BingGroundingService for web research capabilities.

**What it does:**
- Sets up Azure AI Project client connection
- Configures BingGroundingService tool for web searches
- Creates an agent with specific instructions for research tasks
- Provides the agent with capabilities to search the internet and cite sources

**How to run:**
1. Open the notebook in VS Code or Jupyter
2. Ensure your `.env` file is properly configured
3. Run all cells in sequence
4. **Important:** Copy the generated agent ID and add it to your `.env` file as `WEB_RESEARCH_AGENT_ID`

**Output:** A functional web research agent registered in Azure AI Foundry

---

### 02. Agent Testing (`02_agent_testing/`)

**File:** `test_web_research_agent.ipynb`

**Purpose:** Tests the web research agent with a default query and displays formatted results.

**What it does:**
- Loads the previously created agent using its ID
- Creates a conversation thread
- Asks the default question: "What is the latest in Microsoft Manufacturing news?"
- Displays the research results in formatted markdown

**How to run:**
1. Ensure step 01 is completed and agent ID is saved in `.env`
2. Open and run the testing notebook
3. Wait for the research to complete (may take 30-60 seconds)
4. Review the formatted research results

**Output:** A comprehensive research report about Microsoft Manufacturing news with citations

---

### 03. Deep Research API (`03_deep_research_api/`)

**File:** `deep_research_api.py`

**Purpose:** Provides a FastAPI server that enables advanced research workflows with streaming responses.

**What it does:**
- Creates REST API endpoints for research requests
- Implements streaming responses for real-time research updates
- Supports configurable research depth and breadth parameters
- Handles multi-step research processes with progress updates

**How to run:**
1. Ensure the web research agent is created and ID is in `.env`
2. Navigate to the `03_deep_research_api` directory:
   ```bash
   cd self-guided/03_deep_research_api
   ```
3. Install additional dependencies if needed:
   ```bash
   pip install fastapi uvicorn
   ```
4. Run the API server:
   ```bash
   python deep_research_api.py
   ```
5. The API will be available at `http://127.0.0.1:8000`
6. View API documentation at `http://127.0.0.1:8000/docs`

**API Endpoints:**
- `POST /run_deep_research_stream` - Execute research with streaming responses
- `GET /health` - Health check endpoint

**Output:** Running API server ready to handle research requests

---

### 04. Application (`04_application/`)

**File:** `streamlit_app.py`

**Purpose:** Provides a user-friendly web interface for conducting research using the created agents and API.

**What it does:**
- Creates an interactive Streamlit web application
- Allows users to input research topics
- Configures research parameters (depth, breadth)
- Displays real-time streaming research results
- Provides customizable report generation prompts

**How to run:**
1. Ensure steps 01-03 are completed and the API server is running
2. Navigate to the `04_application` directory:
   ```bash
   cd self-guided/04_application
   ```
3. Update the API endpoint in `streamlit_app.py` if needed (line 144):
   ```python
   uri = '127.0.0.1:8000'  # Update this to your API endpoint
   ```
4. Run the Streamlit application:
   ```bash
   streamlit run streamlit_app.py
   ```
5. Open your browser to the provided URL (typically `http://localhost:8501`)

**Features:**
- **Research Input:** Text input for research topics
- **Configuration Panel:** Adjustable depth/breadth parameters
- **Custom Prompts:** Editable report generation instructions
- **Real-time Results:** Streaming research updates
- **Formatted Output:** Professional research reports with citations

**Output:** Interactive web application for conducting research

## Usage Examples

### Basic Research Query
```
Research Topic: "Sustainable aviation fuel developments in 2024"
Depth: 3
Breadth: 3
```

### Advanced Research Query
```
Research Topic: "Impact of AI on manufacturing efficiency"
Depth: 5
Breadth: 4
Custom Report Prompt: Focus on cost savings and implementation challenges
```

## Troubleshooting

### Common Issues

1. **Agent ID Not Found**
   - Ensure you've completed step 01 and saved the agent ID to `.env`
   - Check that the environment variable name matches: `WEB_RESEARCH_AGENT_ID`

2. **API Connection Errors**
   - Verify the API server is running (step 03)
   - Check the URI in `streamlit_app.py` matches your API endpoint
   - Ensure no firewall is blocking local connections

3. **Azure Authentication Issues**
   - Run `az login` to authenticate with Azure CLI
   - Verify your Azure AI Foundry endpoint and permissions
   - Check that your model deployment name is correct

4. **Environment Variables Missing**
   - Verify your `.env` file exists in the project root
   - Ensure all required variables are set with correct values
   - Check for typos in variable names

### Performance Notes

- **Research Time:** Initial research queries may take 1-3 minutes depending on complexity
- **Streaming:** The application provides real-time updates during research
- **Rate Limits:** Be aware of Azure AI and Bing search rate limits
- **Costs:** Monitor your Azure usage as research operations consume tokens

## Next Steps

After completing this self-guided tutorial, you can:

1. **Customize Agent Instructions:** Modify the research agent's behavior for specific domains
2. **Add More Tools:** Integrate additional Azure AI services or external APIs
3. **Scale the API:** Deploy the research API to Azure Container Apps or other cloud platforms
4. **Enhance the UI:** Add more sophisticated features to the Streamlit application
5. **Create Specialized Agents:** Build domain-specific research agents for different industries

## Support

For issues specific to this tutorial:
1. Check the troubleshooting section above
2. Verify all prerequisites are met
3. Review the Azure AI Foundry documentation
4. Check Azure service status and quotas

## Contributing

This is a demonstration project for Microsoft Manufacturing customers. Feel free to modify and extend the code for your specific use cases.
