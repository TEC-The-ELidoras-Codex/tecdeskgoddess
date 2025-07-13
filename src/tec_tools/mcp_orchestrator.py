"""
MCP Orchestrator - Central command for all MCP servers
Part of TEC: BITLYFE IS THE NEW SHIT - The Creator's Rebellion

This orchestrator manages all MCP servers and provides a unified interface
for Daisy Purecode: Silicate Mother to access all TEC capabilities.
"""

import json
import os
import logging
from typing import Dict, Any, List, Optional
from flask import Flask, request, jsonify
from datetime import datetime
import threading
import time
from .mcp_base import MCPClient
from .mcp_journal import JournalMCPServer
from .mcp_finance import FinanceMCPServer
from .mcp_questlog import QuestLogMCPServer

logger = logging.getLogger(__name__)

class MCPOrchestrator:
    """
    Central orchestrator for all MCP servers in the TEC ecosystem
    """
    
    def __init__(self):
        self.app = Flask(__name__)
        self.servers = {}
        self.clients = {}
        self.server_threads = {}
        
        # Server configurations
        self.server_configs = {
            "journal": {
                "class": JournalMCPServer,
                "port": 5001,
                "url": "http://localhost:5001"
            },
            "finance": {
                "class": FinanceMCPServer,
                "port": 5002,
                "url": "http://localhost:5002"
            },
            "questlog": {
                "class": QuestLogMCPServer,
                "port": 5003,
                "url": "http://localhost:5003"
            }
        }
        
        self._setup_routes()
    
    def _setup_routes(self):
        """Setup orchestrator routes"""
        
        @self.app.route('/health', methods=['GET'])
        def health_check():
            """Health check for orchestrator"""
            return jsonify({
                "status": "healthy",
                "orchestrator": "mcp-orchestrator",
                "servers": {name: "running" for name in self.servers.keys()},
                "timestamp": datetime.now().isoformat()
            })
        
        @self.app.route('/mcp/servers', methods=['GET'])
        def list_servers():
            """List all available MCP servers"""
            server_info = {}
            for name, config in self.server_configs.items():
                server_info[name] = {
                    "name": name,
                    "port": config["port"],
                    "url": config["url"],
                    "status": "running" if name in self.servers else "stopped"
                }
            
            return jsonify({
                "servers": server_info,
                "total": len(server_info)
            })
        
        @self.app.route('/mcp/unified/resources', methods=['POST'])
        def unified_resources():
            """Get resources from all servers"""
            all_resources = {}
            
            for name, client in self.clients.items():
                try:
                    resources = client.list_resources()
                    all_resources[name] = resources
                except Exception as e:
                    logger.error(f"Error getting resources from {name}: {e}")
                    all_resources[name] = {"error": str(e)}
            
            return jsonify({"resources": all_resources})
        
        @self.app.route('/mcp/unified/tools', methods=['POST'])
        def unified_tools():
            """Get tools from all servers"""
            all_tools = {}
            
            for name, client in self.clients.items():
                try:
                    tools = client.list_tools()
                    all_tools[name] = tools
                except Exception as e:
                    logger.error(f"Error getting tools from {name}: {e}")
                    all_tools[name] = {"error": str(e)}
            
            return jsonify({"tools": all_tools})
        
        @self.app.route('/mcp/unified/query', methods=['POST'])
        def unified_query():
            """Unified query interface for all MCP servers"""
            data = request.get_json()
            query_type = data.get('type')  # 'resource', 'tool', 'prompt'
            server_name = data.get('server')
            query_data = data.get('data', {})
            
            if not all([query_type, server_name]):
                return jsonify({"error": "type and server are required"}), 400
            
            if server_name not in self.clients:
                return jsonify({"error": f"Server {server_name} not available"}), 404
            
            client = self.clients[server_name]
            
            try:
                if query_type == 'resource':
                    uri = query_data.get('uri')
                    if not uri:
                        return jsonify({"error": "URI required for resource query"}), 400
                    result = client.read_resource(uri)
                elif query_type == 'tool':
                    tool_name = query_data.get('name')
                    arguments = query_data.get('arguments', {})
                    if not tool_name:
                        return jsonify({"error": "Tool name required"}), 400
                    result = client.call_tool(tool_name, arguments)
                else:
                    return jsonify({"error": f"Unknown query type: {query_type}"}), 400
                
                return jsonify({"result": result})
                
            except Exception as e:
                logger.error(f"Error executing unified query: {e}")
                return jsonify({"error": str(e)}), 500
        
        @self.app.route('/mcp/daisy/context', methods=['POST'])
        def daisy_context():
            """
            Special endpoint for Daisy Purecode to get comprehensive context
            from all MCP servers for AI processing
            """
            data = request.get_json()
            user_id = data.get('userId')
            context_type = data.get('contextType', 'full')  # 'full', 'summary', 'recent'
            
            if not user_id:
                return jsonify({"error": "userId required"}), 400
            
            try:
                context = self._gather_daisy_context(user_id, context_type)
                return jsonify({
                    "context": context,
                    "timestamp": datetime.now().isoformat(),
                    "user_id": user_id,
                    "context_type": context_type
                })
            except Exception as e:
                logger.error(f"Error gathering Daisy context: {e}")
                return jsonify({"error": str(e)}), 500
    
    def start_all_servers(self):
        """Start all MCP servers"""
        logger.info("Starting all MCP servers...")
        
        for name, config in self.server_configs.items():
            try:
                # Create server instance
                server = config["class"]()
                self.servers[name] = server
                
                # Start server in separate thread
                def run_server(srv, port):
                    srv.run(host='0.0.0.0', port=port, debug=False)
                
                thread = threading.Thread(
                    target=run_server,
                    args=(server, config["port"]),
                    daemon=True
                )
                thread.start()
                self.server_threads[name] = thread
                
                logger.info(f"Started MCP server: {name} on port {config['port']}")
                
                # Wait a moment for server to start
                time.sleep(1)
                
                # Create client connection
                client = MCPClient(config["url"])
                self.clients[name] = client
                
                # Initialize client connection
                client.initialize({
                    "name": "TEC-MCP-Orchestrator",
                    "version": "1.0.0"
                })
                
                logger.info(f"Connected to MCP server: {name}")
                
            except Exception as e:
                logger.error(f"Error starting server {name}: {e}")
        
        logger.info("All MCP servers started successfully")
    
    def stop_all_servers(self):
        """Stop all MCP servers"""
        logger.info("Stopping all MCP servers...")
        
        # Close client connections
        for name, client in self.clients.items():
            try:
                # Client cleanup if needed
                pass
            except Exception as e:
                logger.error(f"Error stopping client {name}: {e}")
        
        self.clients.clear()
        self.servers.clear()
        self.server_threads.clear()
        
        logger.info("All MCP servers stopped")
    
    def _gather_daisy_context(self, user_id: str, context_type: str) -> Dict[str, Any]:
        """
        Gather comprehensive context from all MCP servers for Daisy Purecode
        """
        context = {
            "user_id": user_id,
            "context_type": context_type,
            "timestamp": datetime.now().isoformat(),
            "servers": {}
        }
        
        # Gather context from each server
        for name, client in self.clients.items():
            try:
                server_context = {}
                
                if name == "journal":
                    # Get journal context
                    recent_entries = client.read_resource("journal://entries/recent")
                    themes = client.read_resource("journal://themes/all")
                    server_context = {
                        "recent_entries": recent_entries,
                        "themes": themes,
                        "focus": "Personal insights, reflection patterns, creative ideas"
                    }
                
                elif name == "finance":
                    # Get finance context
                    crypto_prices = client.read_resource("finance://crypto/prices")
                    portfolio = client.read_resource("finance://portfolio/overview")
                    market_analysis = client.read_resource("finance://analysis/market")
                    server_context = {
                        "crypto_prices": crypto_prices,
                        "portfolio": portfolio,
                        "market_analysis": market_analysis,
                        "focus": "Financial status, investment performance, market opportunities"
                    }
                
                elif name == "questlog":
                    # Get quest log context
                    active_quests = client.read_resource("quest://quests/active")
                    user_profile = client.read_resource("quest://profile/user")
                    productivity_stats = client.read_resource("quest://stats/productivity")
                    server_context = {
                        "active_quests": active_quests,
                        "user_profile": user_profile,
                        "productivity_stats": productivity_stats,
                        "focus": "Current goals, productivity patterns, gamification progress"
                    }
                
                context["servers"][name] = server_context
                
            except Exception as e:
                logger.error(f"Error gathering context from {name}: {e}")
                context["servers"][name] = {"error": str(e)}
        
        return context
    
    def run(self, host: str = '0.0.0.0', port: int = 5000, debug: bool = False):
        """Run the MCP orchestrator"""
        logger.info(f"Starting MCP Orchestrator on {host}:{port}")
        
        # Start all MCP servers first
        self.start_all_servers()
        
        # Start orchestrator
        try:
            self.app.run(host=host, port=port, debug=debug)
        finally:
            self.stop_all_servers()


def main():
    """Main entry point for MCP Orchestrator"""
    logging.basicConfig(level=logging.INFO)
    orchestrator = MCPOrchestrator()
    orchestrator.run(debug=True)


if __name__ == "__main__":
    main()
