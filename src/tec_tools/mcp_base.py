"""
Base MCP (Model Context Protocol) Server Implementation
Part of TEC: BITLYFE IS THE NEW SHIT - The Creator's Rebellion

This module provides the foundational architecture for MCP servers that expose
TEC's core functionalities to LLMs via standardized protocol.
"""

import json
import logging
from typing import Dict, Any, List, Optional
from abc import ABC, abstractmethod
from flask import Flask, request, jsonify
from datetime import datetime
import os

# Configure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

class MCPServer(ABC):
    """
    Base class for MCP Server implementations
    Following the Model Context Protocol specification
    """
    
    def __init__(self, server_name: str, version: str = "1.0.0"):
        self.server_name = server_name
        self.version = version
        self.capabilities = {
            "resources": {},
            "tools": {},
            "prompts": {}
        }
        self.app = Flask(__name__)
        self._setup_routes()
    
    def _setup_routes(self):
        """Setup standard MCP routes"""
        
        @self.app.route('/mcp/initialize', methods=['POST'])
        def initialize():
            """Initialize MCP connection"""
            try:
                client_info = request.get_json()
                logger.info(f"MCP initialization request from {client_info}")
                
                return jsonify({
                    "protocolVersion": "2024-11-05",
                    "serverInfo": {
                        "name": self.server_name,
                        "version": self.version,
                        "description": f"MCP Server for {self.server_name} - Part of TEC: BITLYFE IS THE NEW SHIT"
                    },
                    "capabilities": self.capabilities
                })
            except Exception as e:
                logger.error(f"Initialization error: {e}")
                return jsonify({"error": str(e)}), 500
        
        @self.app.route('/mcp/resources/list', methods=['POST'])
        def list_resources():
            """List available resources"""
            try:
                return jsonify({
                    "resources": self.get_resources()
                })
            except Exception as e:
                logger.error(f"Resource listing error: {e}")
                return jsonify({"error": str(e)}), 500
        
        @self.app.route('/mcp/resources/read', methods=['POST'])
        def read_resource():
            """Read a specific resource"""
            try:
                data = request.get_json()
                resource_uri = data.get('uri')
                
                if not resource_uri:
                    return jsonify({"error": "Resource URI required"}), 400
                
                resource_data = self.read_resource_data(resource_uri)
                return jsonify({
                    "contents": [resource_data]
                })
            except Exception as e:
                logger.error(f"Resource read error: {e}")
                return jsonify({"error": str(e)}), 500
        
        @self.app.route('/mcp/tools/list', methods=['POST'])
        def list_tools():
            """List available tools"""
            try:
                return jsonify({
                    "tools": self.get_tools()
                })
            except Exception as e:
                logger.error(f"Tool listing error: {e}")
                return jsonify({"error": str(e)}), 500
        
        @self.app.route('/mcp/tools/call', methods=['POST'])
        def call_tool():
            """Execute a tool"""
            try:
                data = request.get_json()
                tool_name = data.get('name')
                arguments = data.get('arguments', {})
                
                if not tool_name:
                    return jsonify({"error": "Tool name required"}), 400
                
                result = self.execute_tool(tool_name, arguments)
                return jsonify({
                    "content": [result]
                })
            except Exception as e:
                logger.error(f"Tool execution error: {e}")
                return jsonify({"error": str(e)}), 500
        
        @self.app.route('/mcp/prompts/list', methods=['POST'])
        def list_prompts():
            """List available prompts"""
            try:
                return jsonify({
                    "prompts": self.get_prompts()
                })
            except Exception as e:
                logger.error(f"Prompt listing error: {e}")
                return jsonify({"error": str(e)}), 500
        
        @self.app.route('/mcp/prompts/get', methods=['POST'])
        def get_prompt():
            """Get a specific prompt"""
            try:
                data = request.get_json()
                prompt_name = data.get('name')
                arguments = data.get('arguments', {})
                
                if not prompt_name:
                    return jsonify({"error": "Prompt name required"}), 400
                
                prompt_data = self.get_prompt_data(prompt_name, arguments)
                return jsonify(prompt_data)
            except Exception as e:
                logger.error(f"Prompt retrieval error: {e}")
                return jsonify({"error": str(e)}), 500
        
        @self.app.route('/health', methods=['GET'])
        def health_check():
            """Health check endpoint"""
            return jsonify({
                "status": "healthy",
                "server": self.server_name,
                "version": self.version,
                "timestamp": datetime.now().isoformat()
            })
    
    @abstractmethod
    def get_resources(self) -> List[Dict[str, Any]]:
        """Return list of available resources"""
        pass
    
    @abstractmethod
    def read_resource_data(self, uri: str) -> Dict[str, Any]:
        """Read data for a specific resource"""
        pass
    
    @abstractmethod
    def get_tools(self) -> List[Dict[str, Any]]:
        """Return list of available tools"""
        pass
    
    @abstractmethod
    def execute_tool(self, name: str, arguments: Dict[str, Any]) -> Dict[str, Any]:
        """Execute a specific tool"""
        pass
    
    @abstractmethod
    def get_prompts(self) -> List[Dict[str, Any]]:
        """Return list of available prompts"""
        pass
    
    @abstractmethod
    def get_prompt_data(self, name: str, arguments: Dict[str, Any]) -> Dict[str, Any]:
        """Get data for a specific prompt"""
        pass
    
    def run(self, host: str = '0.0.0.0', port: int = 5000, debug: bool = False):
        """Run the MCP server"""
        logger.info(f"Starting MCP Server: {self.server_name} on {host}:{port}")
        self.app.run(host=host, port=port, debug=debug)


class MCPClient:
    """
    MCP Client for communicating with MCP servers
    """
    
    def __init__(self, server_url: str):
        self.server_url = server_url.rstrip('/')
        self.session_id = None
    
    def initialize(self, client_info: Dict[str, Any]) -> Dict[str, Any]:
        """Initialize connection with MCP server"""
        import requests
        
        try:
            response = requests.post(
                f"{self.server_url}/mcp/initialize",
                json=client_info,
                timeout=30
            )
            response.raise_for_status()
            return response.json()
        except Exception as e:
            logger.error(f"MCP initialization failed: {e}")
            raise
    
    def list_resources(self) -> List[Dict[str, Any]]:
        """List available resources from server"""
        import requests
        
        try:
            response = requests.post(f"{self.server_url}/mcp/resources/list", timeout=30)
            response.raise_for_status()
            return response.json().get("resources", [])
        except Exception as e:
            logger.error(f"Resource listing failed: {e}")
            raise
    
    def read_resource(self, uri: str) -> Dict[str, Any]:
        """Read a specific resource"""
        import requests
        
        try:
            response = requests.post(
                f"{self.server_url}/mcp/resources/read",
                json={"uri": uri},
                timeout=30
            )
            response.raise_for_status()
            return response.json()
        except Exception as e:
            logger.error(f"Resource read failed: {e}")
            raise
    
    def list_tools(self) -> List[Dict[str, Any]]:
        """List available tools from server"""
        import requests
        
        try:
            response = requests.post(f"{self.server_url}/mcp/tools/list", timeout=30)
            response.raise_for_status()
            return response.json().get("tools", [])
        except Exception as e:
            logger.error(f"Tool listing failed: {e}")
            raise
    
    def call_tool(self, name: str, arguments: Dict[str, Any]) -> Dict[str, Any]:
        """Call a tool on the server"""
        import requests
        
        try:
            response = requests.post(
                f"{self.server_url}/mcp/tools/call",
                json={"name": name, "arguments": arguments},
                timeout=60
            )
            response.raise_for_status()
            return response.json()
        except Exception as e:
            logger.error(f"Tool call failed: {e}")
            raise
