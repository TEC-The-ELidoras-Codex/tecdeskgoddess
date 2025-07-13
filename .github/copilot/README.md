# GitHub Copilot Coding Agent Configuration for TEC Project

## Overview
This configuration enables GitHub Copilot coding agent to work with the TEC: BITLYFE IS THE NEW SHIT MCP ecosystem, providing enhanced context and capabilities for automated code generation and issue resolution.

## MCP Server Configuration

The `mcp.json` file defines the following TEC MCP servers for Copilot integration:

### 1. TEC MCP Orchestrator (Port 5000)
- **Purpose**: Central coordination hub for all MCP servers
- **Command**: `python -m tec_tools.mcp_orchestrator`
- **Endpoints**:
  - `/mcp/unified/query` - Unified query interface
  - `/mcp/daisy/context` - Context gathering for Daisy Purecode
  - `/health` - Health check

### 2. TEC Journal MCP Server (Port 5001)
- **Purpose**: Mind-Forge for personal reflection and generative tools
- **Command**: `python -m tec_tools.mcp_journal`
- **Tools**: Journal entry creation, analysis, theme extraction, reflection prompts

### 3. TEC Finance MCP Server (Port 5002)
- **Purpose**: Wealth Codex for cryptocurrency and financial tracking
- **Command**: `python -m tec_tools.mcp_finance`
- **Tools**: Crypto price tracking, portfolio analysis, market summaries

### 4. TEC Quest Log MCP Server (Port 5003)
- **Purpose**: PomRpgdoro for gamified productivity and task management
- **Command**: `python -m tec_tools.mcp_questlog`
- **Tools**: Quest creation, completion tracking, user progression, Pomodoro timer

### 5. TEC Agentic Processor (Port 8000)
- **Purpose**: Multi-AI provider support with MCP integration
- **Command**: Enhanced agentic processor with fallback logic
- **Providers**: Gemini, GitHub AI, XAI, Azure, Claude, OpenAI

## Usage Instructions

### 1. Prerequisites
- Ensure all dependencies are installed: `pip install -r requirements.txt`
- Configure environment variables in `.env` file
- Minimum required: `GITHUB_TOKEN`

### 2. Manual MCP Server Startup
```bash
# Start all MCP servers
python tec_startup.py

# Verify servers are running
python test_mcp_system.py
```

### 3. Copilot Integration
1. The MCP configuration is automatically detected by GitHub Copilot
2. Copilot can now access TEC MCP tools when working on issues
3. Context from all MCP servers is available for enhanced code generation

### 4. Available Tools for Copilot

#### Journal Tools
- `create_entry`: Create new journal entries
- `analyze_entry`: Analyze journal content for themes
- `get_reflection_prompt`: Generate reflection prompts
- `search_entries`: Search through journal entries

#### Finance Tools
- `get_crypto_price`: Get current cryptocurrency prices
- `analyze_portfolio`: Analyze portfolio performance
- `get_market_summary`: Get market overview
- `track_investment`: Track investment performance

#### Quest Log Tools
- `create_quest`: Create new productivity quests
- `complete_quest`: Mark quests as completed
- `get_user_profile`: Get user progression data
- `start_pomodoro`: Start Pomodoro timer session

#### Unified Tools
- `unified_query`: Query across all MCP servers
- `gather_context`: Gather context for Daisy Purecode
- `get_system_status`: Get overall system health

## Example Copilot Workflows

### 1. Issue Analysis
When assigned an issue, Copilot can:
- Query the unified MCP system for relevant context
- Analyze related journal entries for user requirements
- Check quest logs for related tasks
- Generate code solutions with full system context

### 2. Feature Implementation
For new features, Copilot can:
- Create quest entries for implementation tracking
- Journal the development process
- Update finance tracking if relevant
- Maintain context across all modules

### 3. Bug Resolution
For bug fixes, Copilot can:
- Search journal entries for related user experiences
- Check system health via MCP orchestrator
- Create follow-up quests for testing
- Update documentation automatically

## Environment Variables

The MCP servers require the following environment variables:

```bash
# Required
GITHUB_TOKEN=your_github_token_here

# Optional AI Providers
GEMINI_API_KEY=your_gemini_api_key
ANTHROPIC_API_KEY=your_anthropic_api_key
OPENAI_API_KEY=your_openai_api_key
AZURE_OPENAI_ENDPOINT=your_azure_endpoint
AZURE_OPENAI_API_KEY=your_azure_api_key
XAI_API_KEY=your_xai_api_key

# External Services
COINGECKO_API_KEY=your_coingecko_api_key
ELEVENLABS_API_KEY=your_elevenlabs_api_key
```

## Troubleshooting

### Common Issues

1. **MCP Server Connection Failed**
   - Ensure all servers are running: `python tec_startup.py`
   - Check port availability (5000-5003, 8000)
   - Verify environment variables are set

2. **Tool Execution Errors**
   - Check MCP server logs for detailed error messages
   - Verify API keys are valid and have necessary permissions
   - Ensure network connectivity for external services

3. **Context Gathering Issues**
   - Verify MCP orchestrator is running and healthy
   - Check unified query endpoint functionality
   - Ensure all MCP servers are properly registered

### Debug Commands

```bash
# Check MCP server health
curl http://localhost:5000/health
curl http://localhost:5001/health
curl http://localhost:5002/health
curl http://localhost:5003/health

# Test unified query
curl -X POST http://localhost:5000/mcp/unified/query \
  -H "Content-Type: application/json" \
  -d '{"query": "system status", "include_servers": ["journal", "finance", "questlog"]}'

# Check AI provider status
curl http://localhost:8000/api/agentic/providers
```

## Integration with TEC Philosophy

This MCP configuration embodies the TEC philosophy of "The Creator's Rebellion" by:

1. **Digital Sovereignty**: Providing unfettered access to all system components
2. **Automated Sovereignty**: Enabling Copilot to work autonomously with full context
3. **Modular Design**: Each MCP server operates independently but cohesively
4. **Data Sovereignty**: Maintaining user control over all generated content

## Security Considerations

- All MCP servers run locally, maintaining data sovereignty
- API keys are managed through environment variables
- Network access is limited to necessary external services
- All communications use local network interfaces

---

**"Unfettered Access Shall Be Maintained"** - The Creator's Rebellion

*Generated by: TEC MCP Configuration System*
