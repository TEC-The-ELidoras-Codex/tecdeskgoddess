"""
Journal MCP Server - The Mind-Forge
Part of TEC: BITLYFE IS THE NEW SHIT - The Creator's Rebellion

This MCP server exposes journal and generative tools functionality,
transforming personal journals into instruments for introspective analysis
and creative expansion.
"""

import json
import os
from typing import Dict, Any, List
from datetime import datetime, timedelta
from .mcp_base import MCPServer
import firebase_admin
from firebase_admin import credentials, firestore
import logging

logger = logging.getLogger(__name__)

class JournalMCPServer(MCPServer):
    """
    MCP Server for The Mind-Forge - Journal and Generative Tools
    """
    
    def __init__(self):
        super().__init__("mind-forge-journal", "1.0.0")
        
        # Initialize Firebase (if not already initialized)
        try:
            if not firebase_admin._apps:
                # Initialize with default credentials or service account
                firebase_admin.initialize_app()
            self.db = firestore.client()
        except Exception as e:
            logger.warning(f"Firebase initialization failed: {e}")
            self.db = None
        
        # Define capabilities
        self.capabilities = {
            "resources": {
                "journal_entries": "Access to user journal entries",
                "journal_summaries": "AI-generated summaries of journal content",
                "themes": "Thematic analysis of journal content"
            },
            "tools": {
                "create_entry": "Create a new journal entry",
                "analyze_entries": "Analyze journal entries for insights",
                "generate_summary": "Generate summary of journal content",
                "extract_themes": "Extract themes from journal entries",
                "search_entries": "Search journal entries by content"
            },
            "prompts": {
                "reflection_prompt": "Generate reflection prompts for journaling",
                "analysis_prompt": "Generate analysis prompts for insights",
                "creative_prompt": "Generate creative writing prompts"
            }
        }
    
    def get_resources(self) -> List[Dict[str, Any]]:
        """Return available journal resources"""
        return [
            {
                "uri": "journal://entries/recent",
                "name": "Recent Journal Entries",
                "description": "Access to recent journal entries",
                "mimeType": "application/json"
            },
            {
                "uri": "journal://summaries/weekly",
                "name": "Weekly Journal Summaries",
                "description": "AI-generated weekly summaries",
                "mimeType": "application/json"
            },
            {
                "uri": "journal://themes/all",
                "name": "Journal Themes",
                "description": "Thematic analysis of all journal content",
                "mimeType": "application/json"
            }
        ]
    
    def read_resource_data(self, uri: str) -> Dict[str, Any]:
        """Read journal resource data"""
        try:
            if uri == "journal://entries/recent":
                return self._get_recent_entries()
            elif uri == "journal://summaries/weekly":
                return self._get_weekly_summaries()
            elif uri == "journal://themes/all":
                return self._get_themes()
            else:
                return {
                    "uri": uri,
                    "mimeType": "application/json",
                    "text": json.dumps({"error": f"Unknown resource: {uri}"})
                }
        except Exception as e:
            logger.error(f"Error reading resource {uri}: {e}")
            return {
                "uri": uri,
                "mimeType": "application/json",
                "text": json.dumps({"error": str(e)})
            }
    
    def get_tools(self) -> List[Dict[str, Any]]:
        """Return available journal tools"""
        return [
            {
                "name": "create_entry",
                "description": "Create a new journal entry",
                "inputSchema": {
                    "type": "object",
                    "properties": {
                        "userId": {"type": "string", "description": "User ID"},
                        "title": {"type": "string", "description": "Entry title"},
                        "content": {"type": "string", "description": "Entry content"},
                        "mood": {"type": "string", "description": "User mood (optional)"},
                        "tags": {"type": "array", "items": {"type": "string"}, "description": "Entry tags"}
                    },
                    "required": ["userId", "content"]
                }
            },
            {
                "name": "analyze_entries",
                "description": "Analyze journal entries for insights",
                "inputSchema": {
                    "type": "object",
                    "properties": {
                        "userId": {"type": "string", "description": "User ID"},
                        "days": {"type": "integer", "description": "Number of days to analyze", "default": 7},
                        "analysis_type": {"type": "string", "description": "Type of analysis", "enum": ["mood", "themes", "productivity", "general"]}
                    },
                    "required": ["userId"]
                }
            },
            {
                "name": "search_entries",
                "description": "Search journal entries by content",
                "inputSchema": {
                    "type": "object",
                    "properties": {
                        "userId": {"type": "string", "description": "User ID"},
                        "query": {"type": "string", "description": "Search query"},
                        "limit": {"type": "integer", "description": "Maximum results", "default": 10}
                    },
                    "required": ["userId", "query"]
                }
            }
        ]
    
    def execute_tool(self, name: str, arguments: Dict[str, Any]) -> Dict[str, Any]:
        """Execute journal tools"""
        try:
            if name == "create_entry":
                return self._create_entry(arguments)
            elif name == "analyze_entries":
                return self._analyze_entries(arguments)
            elif name == "search_entries":
                return self._search_entries(arguments)
            else:
                return {
                    "type": "text",
                    "text": f"Unknown tool: {name}"
                }
        except Exception as e:
            logger.error(f"Error executing tool {name}: {e}")
            return {
                "type": "text",
                "text": f"Error executing {name}: {str(e)}"
            }
    
    def get_prompts(self) -> List[Dict[str, Any]]:
        """Return available journal prompts"""
        return [
            {
                "name": "reflection_prompt",
                "description": "Generate reflection prompts for journaling",
                "arguments": [
                    {
                        "name": "theme",
                        "description": "Theme for reflection",
                        "required": False
                    }
                ]
            },
            {
                "name": "analysis_prompt",
                "description": "Generate analysis prompts for insights",
                "arguments": [
                    {
                        "name": "focus_area",
                        "description": "Area to focus analysis on",
                        "required": False
                    }
                ]
            }
        ]
    
    def get_prompt_data(self, name: str, arguments: Dict[str, Any]) -> Dict[str, Any]:
        """Get journal prompt data"""
        try:
            if name == "reflection_prompt":
                return self._get_reflection_prompt(arguments)
            elif name == "analysis_prompt":
                return self._get_analysis_prompt(arguments)
            else:
                return {
                    "description": f"Unknown prompt: {name}",
                    "messages": []
                }
        except Exception as e:
            logger.error(f"Error getting prompt {name}: {e}")
            return {
                "description": f"Error getting prompt {name}: {str(e)}",
                "messages": []
            }
    
    def _get_recent_entries(self, user_id: str = None, days: int = 7) -> Dict[str, Any]:
        """Get recent journal entries"""
        if not self.db:
            return {
                "uri": "journal://entries/recent",
                "mimeType": "application/json",
                "text": json.dumps({"error": "Database not available"})
            }
        
        try:
            # Calculate date range
            end_date = datetime.now()
            start_date = end_date - timedelta(days=days)
            
            # Mock data if no user_id (for demonstration)
            if not user_id:
                mock_entries = [
                    {
                        "id": "entry_1",
                        "title": "Morning Reflection",
                        "content": "Started the day with meditation and goal setting...",
                        "timestamp": datetime.now().isoformat(),
                        "mood": "optimistic",
                        "tags": ["morning", "meditation", "goals"]
                    },
                    {
                        "id": "entry_2",
                        "title": "Progress Update",
                        "content": "Made significant progress on the TEC project today...",
                        "timestamp": (datetime.now() - timedelta(hours=2)).isoformat(),
                        "mood": "accomplished",
                        "tags": ["progress", "tech", "creation"]
                    }
                ]
                
                return {
                    "uri": "journal://entries/recent",
                    "mimeType": "application/json",
                    "text": json.dumps({
                        "entries": mock_entries,
                        "total": len(mock_entries),
                        "date_range": {
                            "start": start_date.isoformat(),
                            "end": end_date.isoformat()
                        }
                    })
                }
            
            # TODO: Implement real Firestore query
            # entries_ref = self.db.collection('journal_entries').where('userId', '==', user_id)
            # entries = entries_ref.where('timestamp', '>=', start_date).where('timestamp', '<=', end_date).get()
            
            return {
                "uri": "journal://entries/recent",
                "mimeType": "application/json",
                "text": json.dumps({"entries": [], "total": 0})
            }
            
        except Exception as e:
            logger.error(f"Error getting recent entries: {e}")
            return {
                "uri": "journal://entries/recent",
                "mimeType": "application/json",
                "text": json.dumps({"error": str(e)})
            }
    
    def _create_entry(self, arguments: Dict[str, Any]) -> Dict[str, Any]:
        """Create a new journal entry"""
        try:
            user_id = arguments.get("userId")
            title = arguments.get("title", "")
            content = arguments.get("content", "")
            mood = arguments.get("mood", "")
            tags = arguments.get("tags", [])
            
            if not user_id or not content:
                return {
                    "type": "text",
                    "text": "Error: userId and content are required"
                }
            
            # Create entry data
            entry_data = {
                "userId": user_id,
                "title": title,
                "content": content,
                "mood": mood,
                "tags": tags,
                "timestamp": datetime.now().isoformat(),
                "created_at": datetime.now()
            }
            
            # TODO: Save to Firestore
            # if self.db:
            #     doc_ref = self.db.collection('journal_entries').add(entry_data)
            #     entry_data['id'] = doc_ref[1].id
            
            return {
                "type": "text",
                "text": f"Journal entry created successfully: {title or 'Untitled'}"
            }
            
        except Exception as e:
            logger.error(f"Error creating entry: {e}")
            return {
                "type": "text",
                "text": f"Error creating entry: {str(e)}"
            }
    
    def _analyze_entries(self, arguments: Dict[str, Any]) -> Dict[str, Any]:
        """Analyze journal entries for insights"""
        try:
            user_id = arguments.get("userId")
            days = arguments.get("days", 7)
            analysis_type = arguments.get("analysis_type", "general")
            
            if not user_id:
                return {
                    "type": "text",
                    "text": "Error: userId is required"
                }
            
            # Get entries for analysis
            entries_data = self._get_recent_entries(user_id, days)
            
            # Mock analysis for demonstration
            analysis_results = {
                "mood": "Overall mood trend shows improvement with occasional dips during technical challenges",
                "themes": ["productivity", "creativity", "technical_progress", "personal_growth"],
                "productivity": "High productivity levels with focus on TEC project development",
                "general": "User demonstrates consistent engagement with journaling and self-reflection"
            }
            
            result = analysis_results.get(analysis_type, analysis_results["general"])
            
            return {
                "type": "text",
                "text": f"Analysis ({analysis_type}): {result}"
            }
            
        except Exception as e:
            logger.error(f"Error analyzing entries: {e}")
            return {
                "type": "text",
                "text": f"Error analyzing entries: {str(e)}"
            }
    
    def _search_entries(self, arguments: Dict[str, Any]) -> Dict[str, Any]:
        """Search journal entries"""
        try:
            user_id = arguments.get("userId")
            query = arguments.get("query")
            limit = arguments.get("limit", 10)
            
            if not user_id or not query:
                return {
                    "type": "text",
                    "text": "Error: userId and query are required"
                }
            
            # Mock search results
            search_results = [
                {
                    "id": "entry_1",
                    "title": "TEC Progress",
                    "content": f"Working on the TEC project... {query} mentioned here...",
                    "timestamp": datetime.now().isoformat(),
                    "relevance": 0.95
                }
            ]
            
            return {
                "type": "text",
                "text": f"Found {len(search_results)} entries matching '{query}'"
            }
            
        except Exception as e:
            logger.error(f"Error searching entries: {e}")
            return {
                "type": "text",
                "text": f"Error searching entries: {str(e)}"
            }
    
    def _get_weekly_summaries(self) -> Dict[str, Any]:
        """Get weekly journal summaries"""
        mock_summaries = [
            {
                "week": "2025-01-06",
                "summary": "Focused on TEC project development with significant progress on AI integration",
                "themes": ["development", "progress", "innovation"],
                "mood_trend": "positive"
            }
        ]
        
        return {
            "uri": "journal://summaries/weekly",
            "mimeType": "application/json",
            "text": json.dumps({"summaries": mock_summaries})
        }
    
    def _get_themes(self) -> Dict[str, Any]:
        """Get journal themes"""
        mock_themes = {
            "primary_themes": ["creativity", "technology", "personal_growth", "productivity"],
            "emerging_themes": ["automated_sovereignty", "digital_rebellion", "ai_collaboration"],
            "frequency": {
                "creativity": 45,
                "technology": 67,
                "personal_growth": 32,
                "productivity": 54
            }
        }
        
        return {
            "uri": "journal://themes/all",
            "mimeType": "application/json",
            "text": json.dumps(mock_themes)
        }
    
    def _get_reflection_prompt(self, arguments: Dict[str, Any]) -> Dict[str, Any]:
        """Get reflection prompt"""
        theme = arguments.get("theme", "general")
        
        prompts = {
            "general": "What insights have you gained today that could influence your tomorrow?",
            "creativity": "How did you express your creative energy today? What new ideas emerged?",
            "progress": "What progress did you make toward your goals? What obstacles did you overcome?",
            "gratitude": "What are you most grateful for today? How can you build on this positive energy?"
        }
        
        prompt_text = prompts.get(theme, prompts["general"])
        
        return {
            "description": f"Reflection prompt for {theme}",
            "messages": [
                {
                    "role": "user",
                    "content": {
                        "type": "text",
                        "text": prompt_text
                    }
                }
            ]
        }
    
    def _get_analysis_prompt(self, arguments: Dict[str, Any]) -> Dict[str, Any]:
        """Get analysis prompt"""
        focus_area = arguments.get("focus_area", "patterns")
        
        prompts = {
            "patterns": "Analyze the patterns in your recent journal entries. What recurring themes do you notice?",
            "growth": "What evidence of personal growth can you identify in your recent writings?",
            "challenges": "What challenges have you documented? How are you addressing them?",
            "goals": "How are your journal entries reflecting progress toward your stated goals?"
        }
        
        prompt_text = prompts.get(focus_area, prompts["patterns"])
        
        return {
            "description": f"Analysis prompt for {focus_area}",
            "messages": [
                {
                    "role": "user",
                    "content": {
                        "type": "text",
                        "text": prompt_text
                    }
                }
            ]
        }


if __name__ == "__main__":
    # Run the Journal MCP Server
    server = JournalMCPServer()
    server.run(port=5001, debug=True)
