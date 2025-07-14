# AI AGENT FRAMEWORKS: PRACTICAL IMPLEMENTATION GUIDE

## GENERAL SETUP (DO THIS FIRST)

### Create a dedicated virtual environment
```powershell
# Navigate to your TEC code directory
cd C:\Users\Ghedd\TEC_CODE

# Create a new directory for agent experiments
mkdir agent_experiments
cd agent_experiments

# Create a virtual environment
python -m venv agent_venv

# Activate the virtual environment
.\agent_venv\Scripts\Activate.ps1

# Create subdirectories for each framework
mkdir openai_agents
mkdir smol_agents
mkdir llamaindex_agents
```

## OPENAI AGENTS SDK IMPLEMENTATION

### Setup & Installation
```powershell
# Navigate to the OpenAI agents directory
cd C:\Users\Ghedd\TEC_CODE\agent_experiments\openai_agents

# Install the OpenAI Agents SDK
pip install openai-agents

# Create a config file for your API key
echo "OPENAI_API_KEY=your_api_key_here" > .env
```

### Basic Agent Implementation
```python
# Simple agent implementation with OpenAI Agents SDK
from openai import OpenAI
from openai.agents import Agent, Tool

# Initialize the client
client = OpenAI()

# Define a simple tool
def get_current_time():
    """Gets the current time."""
    import datetime
    return datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")

time_tool = Tool(
    name="get_current_time",
    description="Gets the current time",
    function=get_current_time
)

# Create an agent with the tool
tec_agent = Agent.create(
    name="TEC Assistant",
    instructions="You are a helpful assistant for The Elidoras Codex.",
    tools=[time_tool],
    model="gpt-4-turbo"
)

# Run the agent with a user query
result = tec_agent.run("What time is it, and can you tell me about the Astradigital Ocean?")
print(result.message.content)
```

## HUGGING FACE SMOLAGENS IMPLEMENTATION

### Setup & Installation
```powershell
# Navigate to the SmolAgents directory
cd C:\Users\Ghedd\TEC_CODE\agent_experiments\smol_agents

# Clone the SmolAgents repository
git clone https://github.com/huggingface/smolagens.git

# Install the requirements
pip install -e .
```

### Basic Agent Implementation
```python
# Simple agent implementation with SmolAgents
from smolagens import Agent

# Define a simple agent
tec_agent = Agent(
    instructions="You are a helpful assistant for The Elidoras Codex.",
    model="mistralai/Mixtral-8x7B-Instruct-v0.1",
    tools=[] # No tools for this simple example
)

# Run the agent with a user query
response = tec_agent.run("Tell me about the Astradigital Ocean and its factions.")
print(response)
```

## LLAMAINDEX IMPLEMENTATION

### Setup & Installation
```powershell
# Navigate to the LlamaIndex directory
cd C:\Users\Ghedd\TEC_CODE\agent_experiments\llamaindex_agents

# Install LlamaIndex
pip install llama-index llama-hub
```

### Basic Implementation
```python
# Simple implementation with LlamaIndex
from llama_index import VectorStoreIndex
from llama_index.readers.file import DirectoryReader
from llama_index.agent import ReActAgent
from llama_index.llms import OpenAI

# Load documents from TEC lore directory
documents = DirectoryReader(
    input_dir="C:\\Users\\Ghedd\\TEC_CODE\\astradigital-engine\\data\\lore",
    recursive=True
).load_data()

# Create an index from the documents
index = VectorStoreIndex.from_documents(documents)

# Create a query engine
query_engine = index.as_query_engine()

# Create an agent that can use the query engine
llm = OpenAI(model="gpt-3.5-turbo")
agent = ReActAgent.from_tools(
    [query_engine], 
    llm=llm,
    verbose=True
)

# Run the agent with a user query
response = agent.chat("What can you tell me about MAGMASOX?")
print(response)
```

## INTEGRATION WITH TEC ASTRADIGITAL ENGINE

### Creating an Agent Interface Module

Create a new file at `C:\Users\Ghedd\TEC_CODE\astradigital-engine\src\agents\agent_interface.py`:

```python
"""
Agent Interface for The Elidoras Codex.
Provides a unified interface for different agent frameworks.
"""
import os
import logging
from typing import Dict, Any, List, Optional, Union
from enum import Enum

class AgentFramework(Enum):
    """Supported agent frameworks."""
    OPENAI = "openai"
    SMOL = "smol"
    LLAMAINDEX = "llamaindex"
    
class AgentInterface:
    """
    Unified interface for different agent frameworks.
    Allows for easy switching between implementations.
    """
    
    def __init__(self, framework: AgentFramework = AgentFramework.OPENAI, config_path: Optional[str] = None):
        """
        Initialize the agent interface.
        
        Args:
            framework: The agent framework to use
            config_path: Path to configuration directory or file
        """
        self.framework = framework
        self.config_path = config_path or os.path.join(os.path.dirname(
            os.path.dirname(os.path.dirname(os.path.abspath(__file__)))), 'config')
        
        self.logger = logging.getLogger(f"TEC.AgentInterface.{framework.value}")
        self.agent = self._initialize_agent()
        
    def _initialize_agent(self):
        """Initialize the appropriate agent based on the selected framework."""
        if self.framework == AgentFramework.OPENAI:
            try:
                from openai.agents import Agent, Tool
                # Initialize OpenAI agent
                return Agent.create(
                    name="TEC Assistant",
                    instructions="You are a helpful assistant for The Elidoras Codex.",
                    tools=[],
                    model="gpt-4-turbo"
                )
            except ImportError:
                self.logger.error("OpenAI Agents SDK not installed. Please install with: pip install openai-agents")
                return None
                
        elif self.framework == AgentFramework.SMOL:
            try:
                from smolagens import Agent
                # Initialize SmolAgents agent
                return Agent(
                    instructions="You are a helpful assistant for The Elidoras Codex.",
                    model="mistralai/Mixtral-8x7B-Instruct-v0.1"
                )
            except ImportError:
                self.logger.error("SmolAgents not installed. Please install from GitHub.")
                return None
                
        elif self.framework == AgentFramework.LLAMAINDEX:
            try:
                from llama_index.llms import OpenAI
                from llama_index.agent import ReActAgent
                # Initialize LlamaIndex agent
                llm = OpenAI(model="gpt-3.5-turbo")
                return ReActAgent.from_tools(
                    [], 
                    llm=llm,
                    verbose=True
                )
            except ImportError:
                self.logger.error("LlamaIndex not installed. Please install with: pip install llama-index")
                return None
                
        else:
            self.logger.error(f"Unsupported framework: {self.framework}")
            return None
            
    def run(self, query: str) -> str:
        """
        Run the agent with the given query.
        
        Args:
            query: The user query to process
            
        Returns:
            The agent's response as a string
        """
        if not self.agent:
            return "Agent not initialized properly. Please check logs for details."
            
        try:
            if self.framework == AgentFramework.OPENAI:
                result = self.agent.run(query)
                return result.message.content
                
            elif self.framework == AgentFramework.SMOL:
                return self.agent.run(query)
                
            elif self.framework == AgentFramework.LLAMAINDEX:
                response = self.agent.chat(query)
                return str(response)
                
            else:
                return "Unsupported framework selected."
                
        except Exception as e:
            self.logger.error(f"Error running agent: {e}")
            return f"Error: {str(e)}"

# Example usage
if __name__ == "__main__":
    # Configure logging
    logging.basicConfig(
        level=logging.INFO,
        format='%(asctime)s - %(name)s - %(levelname)s - %(message)s'
    )
    
    # Test with OpenAI framework
    agent = AgentInterface(framework=AgentFramework.OPENAI)
    response = agent.run("Tell me about the Kaznak Voyagers.")
    print(f"OpenAI Agent Response: {response}")
    
    # Test with SmolAgents framework
    agent = AgentInterface(framework=AgentFramework.SMOL)
    response = agent.run("Tell me about MAGMASOX.")
    print(f"SmolAgents Response: {response}")
```

### Testing the Agent Interface

Create a test script at `C:\Users\Ghedd\TEC_CODE\astradigital-engine\scripts\test_agent_interface.py`:

```python
#!/usr/bin/env python3
"""
Test script for the Agent Interface module.
Tests each supported framework with a simple query.
"""
import os
import sys
import logging

# Add the parent directory to the Python path
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

# Configure logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s')
logger = logging.getLogger("TestAgentInterface")

# Import the Agent Interface
try:
    from src.agents.agent_interface import AgentInterface, AgentFramework
except ImportError as e:
    logger.critical(f"Failed to import required modules: {e}")
    print(f"Error: Failed to import required modules. Make sure all dependencies are installed.")
    print(f"Details: {e}")
    sys.exit(1)

def test_agent_interface():
    """Test the Agent Interface with different frameworks."""
    frameworks = [
        (AgentFramework.OPENAI, "Tell me about the Astradigital Ocean."),
        (AgentFramework.SMOL, "Who are the Kaznak Voyagers?"),
        (AgentFramework.LLAMAINDEX, "What can you tell me about MAGMASOX?")
    ]
    
    results = {}
    
    for framework, query in frameworks:
        logger.info(f"Testing {framework.value} framework with query: {query}")
        
        try:
            agent = AgentInterface(framework=framework)
            response = agent.run(query)
            
            logger.info(f"Response from {framework.value}: {response[:100]}...")
            results[framework.value] = True
        except Exception as e:
            logger.error(f"Error with {framework.value}: {e}")
            results[framework.value] = False
    
    # Print summary
    logger.info("Test results summary:")
    for framework, success in results.items():
        logger.info(f"  {framework}: {'Success' if success else 'Failed'}")
    
    return all(results.values())

if __name__ == "__main__":
    logger.info("Starting Agent Interface test...")
    
    if test_agent_interface():
        logger.info("All tests passed successfully!")
        sys.exit(0)
    else:
        logger.error("Some tests failed.")
        sys.exit(1)
```
