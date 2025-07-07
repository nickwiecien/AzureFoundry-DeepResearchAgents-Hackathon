# Deep Research API with Azure AI Foundry Agents

A comprehensive demonstration of building intelligent research systems using Azure AI Foundry agents that can access and analyze multiple data sources. This repository showcases how to create sophisticated research APIs that can tap into public internet data, Wikipedia, and can be extended to enterprise datasets.

## 🎯 Overview

This project demonstrates the construction of a **Deep Research API** powered by Azure AI Foundry agents, designed for Microsoft Manufacturing customers. The system showcases how AI agents can be orchestrated to conduct comprehensive research across different data sources, providing detailed analysis with proper citations and structured reporting.

### Key Capabilities

- **Multi-Source Research**: Agents can search across web data, Wikipedia, and custom enterprise datasets
- **Intelligent Analysis**: AI-powered synthesis and analysis of research findings
- **Citation Management**: Automatic citation tracking with clickable URL references
- **Streaming Responses**: Real-time research progress updates
- **Configurable Depth**: Adjustable research breadth and depth parameters
- **Professional Reporting**: Structured markdown reports suitable for business use

### Architecture

```
┌─────────────────┐    ┌─────────────────┐    ┌─────────────────┐
│   Streamlit     │    │   FastAPI       │    │  Azure AI       │
│   Frontend      │◄──►│   Research API  │◄──►│  Foundry        │
│                 │    │                 │    │  Agents         │
└─────────────────┘    └─────────────────┘    └─────────────────┘
                                │
                                ▼
                       ┌─────────────────┐
                       │   Data Sources  │
                       │                 │
                       │ • Bing Search   │
                       │ • Wikipedia     │
                       │ • Custom APIs   │
                       └─────────────────┘
```

## 📁 Repository Structure

```
Microsoft-Manufacturing-Research-Demo/
├── instructor-led/          # Step-by-step guided tutorials
│   ├── 01_wikipedia_api_sample/     # Wikipedia API implementation
│   ├── 02_wikipedia_api_testing/    # API testing notebooks
│   ├── 03_agent_creation/           # Agent creation workflows
│   ├── 04_agent_testing/            # Agent validation tests
│   ├── 05_deep_research_api/        # Advanced research API
│   └── 06_streamlit_app/            # Web application interface
├── self-guided/             # Independent learning path
│   ├── 01_agent_creation/           # Web research agent setup
│   ├── 02_agent_testing/            # Agent functionality tests
│   ├── 03_deep_research_api/        # Research API development
│   └── 04_application/              # Full application build
├── reference/               # Reference implementations
└── .env.sample             # Environment configuration template
```

## 🚀 Quick Start

### Prerequisites

1. **Azure AI Foundry Project** with appropriate permissions
2. **Python 3.11** installed
3. **Bing Grounding Service resource** (Azure) for web search capabilities
4. **Azure Container App environment** for deployment
5. **Azure CLI** configured and authenticated

### Environment Setup

1. **Clone the repository**
   ```bash
   git clone <repository-url>
   cd Microsoft-Manufacturing-Research-Demo
   ```

2. **Configure environment variables**
   ```bash
   cp .env.sample .env
   # Edit .env with your Azure AI Foundry credentials
   ```

3. **Install dependencies**
   ```bash
   pip install azure-ai-projects azure-identity python-dotenv streamlit fastapi uvicorn
   ```

### Choose Your Learning Path

#### 🎓 Instructor-Led Path
Perfect for workshops and guided learning sessions:
```bash
cd instructor-led/
# Follow numbered directories 01-06 in sequence
```

#### 🔍 Self-Guided Path  
Ideal for independent exploration:
```bash
cd self-guided/
# Follow the README.md for step-by-step instructions
```

## 📚 Learning Paths

### Instructor-Led Journey

1. **Wikipedia API Sample** - Build a basic Wikipedia search API
2. **API Testing** - Validate API functionality with Jupyter notebooks
3. **Agent Creation** - Create Azure AI Foundry agents with different capabilities
4. **Agent Testing** - Comprehensive testing of agent functionality
5. **Deep Research API** - Advanced API with streaming and multi-step research
6. **Streamlit Application** - Full-featured web interface

### Self-Guided Journey

1. **Agent Creation** - Set up web research agent with Bing integration
2. **Agent Testing** - Test agent with real research scenarios
3. **Deep Research API** - Build scalable research API
4. **Application Development** - Create interactive web application

## 🔧 Core Components

### Research Agents

**Web Research Agent**
- Uses BingGroundingService for internet searches
- Provides current information with citations
- Ideal for market research and trend analysis

**Wikipedia Research Agent**  
- Searches Wikipedia for authoritative information
- Perfect for historical and scientific research
- Provides foundational knowledge with references

### APIs and Interfaces

**FastAPI Research Service**
- RESTful endpoints for research operations
- Streaming responses for real-time updates
- Configurable research parameters

**Streamlit Web Application**
- User-friendly research interface
- Customizable report generation
- Real-time progress tracking

## 🌟 Use Cases

### Demonstrated Applications

- **Market Research**: Analyze industry trends and competitive landscapes
- **Technology Assessment**: Research emerging technologies and their applications
- **Historical Analysis**: Gather background information and context
- **Scientific Research**: Access authoritative sources and technical information

### Enterprise Extensions

The patterns demonstrated here can be extended to:

- **Internal Knowledge Bases**: Connect to SharePoint, Confluence, or custom databases
- **Document Repositories**: Search through technical specifications, reports, and documentation
- **Customer Data**: Analyze support tickets, feedback, and usage patterns
- **Regulatory Information**: Access compliance databases and legal requirements

## 🔮 Advanced Features

### Research Orchestration
- **Multi-Agent Coordination**: Different agents specialized for different data sources
- **Progressive Research**: Iterative deepening based on initial findings
- **Source Validation**: Cross-referencing information across multiple sources

### Customization Options
- **Custom Data Connectors**: Integrate with enterprise APIs and databases
- **Specialized Agents**: Domain-specific research agents (legal, medical, technical)
- **Report Templates**: Configurable output formats for different audiences

## 🛠️ Development Guidelines

### Adding New Data Sources

1. **Create OpenAPI Specification**: Define the API contract for your data source
2. **Implement Agent Tool**: Configure Azure AI agent with the new tool
3. **Test Integration**: Validate agent functionality with the new source
4. **Update Documentation**: Add usage examples and guidelines

### Extending Agent Capabilities

1. **Define Agent Instructions**: Specify research protocols and quality standards
2. **Configure Tools**: Set up appropriate tools and connections
3. **Test Scenarios**: Validate with realistic research questions
4. **Monitor Performance**: Track token usage and response quality

## 📊 Performance Considerations

- **Rate Limiting**: Be aware of API rate limits for external services
- **Token Usage**: Monitor Azure AI token consumption
- **Caching**: Implement caching for frequently accessed information
- **Async Processing**: Use streaming for long-running research operations

## 🔒 Security & Compliance

- **API Key Management**: Store credentials securely using Azure Key Vault
- **Data Privacy**: Implement appropriate data handling for sensitive information
- **Access Controls**: Configure role-based access for different user types
- **Audit Logging**: Track research activities for compliance requirements

## 🤝 Contributing

This project serves as a foundation for building enterprise research systems. Contributions are welcome for:

- New data source integrations
- Enhanced agent capabilities
- Improved user interfaces
- Performance optimizations

## 📄 License

This project is licensed under the terms specified in the LICENSE file.

## 🆘 Support

For technical issues:
1. Check the troubleshooting sections in individual README files
2. Verify Azure AI Foundry configuration and permissions
3. Review the Azure AI service status and quotas
4. Consult the Azure AI Foundry documentation

---

**Built for Microsoft Manufacturing customers** - Demonstrating the power of AI-driven research systems for enterprise applications.