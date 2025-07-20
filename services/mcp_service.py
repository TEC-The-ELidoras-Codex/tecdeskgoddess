"""
TEC: BITLYFE - MCP Service
Handles all AI communication using the Model Context Protocol
"""

import json
import requests
import asyncio
import aiohttp
from typing import Dict, List, Optional, Any
from datetime import datetime
import os
import logging

# Set up logging
logger = logging.getLogger(__name__)


class MCPService:
    """
    MCP Service - Handles communication with AI models
    Supports multiple providers with fallback logic
    """
    
    def __init__(self):
        self.providers = {
            "gemini": {
                "enabled": True,
                "api_key": os.getenv("GEMINI_API_KEY"),
                "base_url": "https://generativelanguage.googleapis.com/v1beta",
                "model": "gemini-1.5-pro"
            },
            "github": {
                "enabled": True,
                "api_key": os.getenv("GITHUB_TOKEN"),
                "base_url": "https://models.inference.ai.azure.com",
                "model": "gpt-4o-mini"
            },
            "local": {
                "enabled": False,  # Will be enabled when Kimi-K2 is set up
                "base_url": "http://localhost:8080/v1",
                "model": "kimi-k2-instruct"
            }
        }
        
        self.current_provider = "gemini"
        self.conversation_history: Dict[str, List] = {}
        
        # Tool definitions for agentic behavior
        self.available_tools = {
            "get_player_info": {
                "description": "Get information about a player",
                "parameters": {
                    "type": "object",
                    "properties": {
                        "player_id": {"type": "string", "description": "The player ID"}
                    },
                    "required": ["player_id"]
                }
            },
            "get_npc_info": {
                "description": "Get information about an NPC",
                "parameters": {
                    "type": "object",
                    "properties": {
                        "npc_id": {"type": "string", "description": "The NPC ID"}
                    },
                    "required": ["npc_id"]
                }
            },
            "update_npc_mood": {
                "description": "Update an NPC's mood based on interaction",
                "parameters": {
                    "type": "object",
                    "properties": {
                        "npc_id": {"type": "string", "description": "The NPC ID"},
                        "new_mood": {"type": "string", "description": "The new mood"},
                        "reason": {"type": "string", "description": "Reason for mood change"}
                    },
                    "required": ["npc_id", "new_mood"]
                }
            },
            "start_battle": {
                "description": "Initiate a battle between entities",
                "parameters": {
                    "type": "object",
                    "properties": {
                        "participants": {"type": "array", "items": {"type": "string"}, "description": "List of participant IDs"},
                        "battle_type": {"type": "string", "description": "Type of battle (pve, pvp, etc.)"}
                    },
                    "required": ["participants"]
                }
            }
        }
    
    def set_provider(self, provider_name: str) -> bool:
        """Switch to a different AI provider"""
        if provider_name in self.providers and self.providers[provider_name]["enabled"]:
            self.current_provider = provider_name
            logger.info(f"Switched to AI provider: {provider_name}")
            return True
        return False
    
    def get_available_providers(self) -> List[str]:
        """Get list of available AI providers"""
        return [name for name, config in self.providers.items() if config["enabled"]]
    
    async def generate_npc_dialogue(self, npc_data: Dict, player_message: str, conversation_context: Dict) -> Dict:
        """
        Generate NPC dialogue response using AI
        """
        try:
            # Prepare the prompt
            system_prompt = self._build_npc_system_prompt(npc_data)
            user_prompt = self._build_user_prompt(player_message, conversation_context)
            
            messages = [
                {"role": "system", "content": system_prompt},
                {"role": "user", "content": user_prompt}
            ]
            
            # Add conversation history if available
            npc_id = npc_data["npc_profile"]["name"]
            if npc_id in self.conversation_history:
                # Add last few exchanges
                recent_history = self.conversation_history[npc_id][-6:]  # Last 3 exchanges
                for exchange in recent_history:
                    messages.extend([
                        {"role": "user", "content": exchange.get("player_message", "")},
                        {"role": "assistant", "content": exchange.get("npc_response", "")}
                    ])
            
            # Try primary provider first
            response = await self._call_ai_provider(self.current_provider, messages, tools=self.available_tools)
            
            if response["success"]:
                # Store conversation for future context
                self._store_conversation(npc_id, player_message, response["content"])
                return response
            else:
                # Try fallback providers
                for provider in self.get_available_providers():
                    if provider != self.current_provider:
                        logger.warning(f"Primary provider {self.current_provider} failed, trying {provider}")
                        fallback_response = await self._call_ai_provider(provider, messages)
                        if fallback_response["success"]:
                            self._store_conversation(npc_id, player_message, fallback_response["content"])
                            return fallback_response
                
                # All providers failed
                return {
                    "success": False,
                    "content": "I seem to be having trouble speaking right now...",
                    "error": "All AI providers failed"
                }
                
        except Exception as e:
            logger.error(f"Error generating NPC dialogue: {e}")
            return {
                "success": False,
                "content": "I'm not feeling very talkative right now.",
                "error": str(e)
            }
    
    def _build_npc_system_prompt(self, npc_data: Dict) -> str:
        """Build the system prompt for NPC dialogue"""
        profile = npc_data["npc_profile"]
        state = npc_data["current_state"]
        relationship = npc_data["player_relationship"]
        
        prompt = f"""You are {profile['name']}, a {profile['type']} in the mystical world of TEC: BITLYFE.

PERSONALITY TRAITS:
- Friendliness: {profile['personality_traits']['friendliness']}/100
- Aggression: {profile['personality_traits']['aggression']}/100  
- Curiosity: {profile['personality_traits']['curiosity']}/100
- Loyalty: {profile['personality_traits']['loyalty']}/100
- Intelligence: {profile['personality_traits']['intelligence']}/100
- Humor: {profile['personality_traits']['humor']}/100

CURRENT STATE:
- Mood: {state['mood']}
- Goal: {state['goal']}
- Location: {state['location']}
- Health: {state['health_percentage']:.0f}%

PLAYER RELATIONSHIP:
- Relationship Level: {relationship['level']} (Score: {relationship['score']}/100)

SPECIAL ROLES:
- Merchant: {profile['special_roles']['is_merchant']}
- Quest Giver: {profile['special_roles']['is_quest_giver']}
- Hostile: {profile['special_roles']['is_hostile']}

INSTRUCTIONS:
1. Respond as this character would, considering their personality, mood, and relationship with the player
2. Keep responses concise but meaningful (1-3 sentences typically)
3. If you're a merchant, mention your wares when appropriate
4. If you have quests available, hint at them naturally in conversation
5. Your mood and personality should strongly influence your tone and word choice
6. Remember your current goal and let it influence your priorities in conversation
7. If relationship is poor, be more distant or hostile
8. If relationship is good, be more helpful and friendly

IMPORTANT: Stay in character at all times. You are NOT an AI assistant - you are {profile['name']} living in this fantasy world."""

        return prompt
    
    def _build_user_prompt(self, player_message: str, context: Dict) -> str:
        """Build the user prompt with context"""
        prompt = f"Player says: \"{player_message}\"\n\n"
        
        if context.get("available_actions"):
            actions = context["available_actions"]
            if actions.get("can_trade"):
                prompt += "Note: You can offer to trade with this player.\n"
            if actions.get("has_quests"):
                prompt += "Note: You have quests available for this player.\n"
            if actions.get("can_battle"):
                prompt += "Note: This player could be challenged to battle.\n"
        
        prompt += "\nRespond as your character would:"
        return prompt
    
    async def _call_ai_provider(self, provider_name: str, messages: List[Dict], tools: Optional[Dict] = None) -> Dict:
        """Call a specific AI provider"""
        provider_config = self.providers[provider_name]
        
        try:
            if provider_name == "gemini":
                return await self._call_gemini(provider_config, messages, tools)
            elif provider_name == "github":
                return await self._call_github_ai(provider_config, messages, tools)
            elif provider_name == "local":
                return await self._call_local_ai(provider_config, messages, tools)
            else:
                return {"success": False, "error": f"Unknown provider: {provider_name}"}
                
        except Exception as e:
            logger.error(f"Error calling {provider_name}: {e}")
            return {"success": False, "error": str(e)}
    
    async def _call_gemini(self, config: Dict, messages: List[Dict], tools: Optional[Dict] = None) -> Dict:
        """Call Gemini API"""
        if not config["api_key"]:
            return {"success": False, "error": "Gemini API key not configured"}
        
        # Convert messages to Gemini format
        prompt = ""
        for msg in messages:
            if msg["role"] == "system":
                prompt += f"System: {msg['content']}\n\n"
            elif msg["role"] == "user":
                prompt += f"User: {msg['content']}\n\n"
            elif msg["role"] == "assistant":
                prompt += f"Assistant: {msg['content']}\n\n"
        
        prompt += "Assistant:"
        
        url = f"{config['base_url']}/models/{config['model']}:generateContent"
        headers = {"Content-Type": "application/json"}
        
        payload = {
            "contents": [{"parts": [{"text": prompt}]}],
            "generationConfig": {
                "temperature": 0.7,
                "maxOutputTokens": 500
            }
        }
        
        async with aiohttp.ClientSession() as session:
            async with session.post(f"{url}?key={config['api_key']}", 
                                   json=payload, headers=headers) as response:
                if response.status == 200:
                    data = await response.json()
                    content = data["candidates"][0]["content"]["parts"][0]["text"]
                    return {"success": True, "content": content.strip()}
                else:
                    error_text = await response.text()
                    return {"success": False, "error": f"HTTP {response.status}: {error_text}"}
    
    async def _call_github_ai(self, config: Dict, messages: List[Dict], tools: Optional[Dict] = None) -> Dict:
        """Call GitHub AI Models"""
        if not config["api_key"]:
            return {"success": False, "error": "GitHub token not configured"}
        
        url = f"{config['base_url']}/chat/completions"
        headers = {
            "Authorization": f"Bearer {config['api_key']}",
            "Content-Type": "application/json"
        }
        
        payload = {
            "model": config["model"],
            "messages": messages,
            "temperature": 0.7,
            "max_tokens": 500
        }
        
        if tools:
            payload["tools"] = [{"type": "function", "function": tool} for tool in tools.values()]
            payload["tool_choice"] = "auto"
        
        try:
            response = requests.post(url, json=payload, headers=headers, timeout=30)
            if response.status_code == 200:
                data = response.json()
                content = data["choices"][0]["message"]["content"]
                return {"success": True, "content": content}
            else:
                return {"success": False, "error": f"HTTP {response.status_code}: {response.text}"}
        except requests.RequestException as e:
            return {"success": False, "error": f"Request failed: {e}"}
    
    async def _call_local_ai(self, config: Dict, messages: List[Dict], tools: Optional[Dict] = None) -> Dict:
        """Call local Kimi-K2 model"""
        url = f"{config['base_url']}/chat/completions"
        headers = {"Content-Type": "application/json"}
        
        payload = {
            "model": config["model"],
            "messages": messages,
            "temperature": 0.7,
            "max_tokens": 500
        }
        
        if tools:
            payload["tools"] = [{"type": "function", "function": tool} for tool in tools.values()]
            payload["tool_choice"] = "auto"
        
        try:
            response = requests.post(url, json=payload, headers=headers, timeout=30)
            if response.status_code == 200:
                data = response.json()
                content = data["choices"][0]["message"]["content"]
                return {"success": True, "content": content}
            else:
                return {"success": False, "error": f"HTTP {response.status_code}: {response.text}"}
        except requests.RequestException as e:
            return {"success": False, "error": f"Request failed: {e}"}
    
    def _store_conversation(self, npc_id: str, player_message: str, npc_response: str):
        """Store conversation for context"""
        if npc_id not in self.conversation_history:
            self.conversation_history[npc_id] = []
        
        self.conversation_history[npc_id].append({
            "timestamp": datetime.now().isoformat(),
            "player_message": player_message,
            "npc_response": npc_response
        })
        
        # Keep only last 20 exchanges
        if len(self.conversation_history[npc_id]) > 20:
            self.conversation_history[npc_id] = self.conversation_history[npc_id][-20:]
    
    async def generate_battle_description(self, battle_data: Dict) -> str:
        """Generate epic battle descriptions"""
        prompt = f"""Generate an epic, cinematic description of a battle in the mystical world of TEC: BITLYFE.

BATTLE DETAILS:
- Participants: {', '.join(battle_data.get('participants', []))}
- Battle Type: {battle_data.get('type', 'unknown')}
- Location: {battle_data.get('location', 'mystical battlefield')}

Create a vivid, 2-3 sentence description that captures the drama and intensity of this battle. 
Use fantasy language and make it feel epic and immersive."""
        
        messages = [{"role": "user", "content": prompt}]
        response = await self._call_ai_provider(self.current_provider, messages)
        
        return response.get("content", "An epic battle unfolds!")
    
    async def generate_quest_description(self, quest_data: Dict) -> str:
        """Generate quest descriptions and dialogue"""
        prompt = f"""Create an engaging quest description for TEC: BITLYFE.

QUEST DATA:
- Quest Type: {quest_data.get('type', 'adventure')}
- Objective: {quest_data.get('objective', 'unknown')}
- Difficulty: {quest_data.get('difficulty', 'normal')}
- Location: {quest_data.get('location', 'mystical realm')}

Generate a compelling quest description that would motivate a player to embark on this adventure.
Keep it concise but intriguing (2-3 sentences)."""
        
        messages = [{"role": "user", "content": prompt}]
        response = await self._call_ai_provider(self.current_provider, messages)
        
        return response.get("content", "A mysterious quest awaits...")
    
    def enable_local_model(self, model_path: str) -> bool:
        """Enable the local Kimi-K2 model"""
        try:
            # Test if the local model is accessible
            test_response = requests.get("http://localhost:8080/v1/models", timeout=5)
            if test_response.status_code == 200:
                self.providers["local"]["enabled"] = True
                logger.info("Local Kimi-K2 model enabled successfully")
                return True
        except:
            pass
        
        logger.warning("Could not connect to local Kimi-K2 model")
        return False
    
    def get_service_status(self) -> Dict:
        """Get the current status of the MCP service"""
        return {
            "current_provider": self.current_provider,
            "available_providers": self.get_available_providers(),
            "provider_status": {
                name: {
                    "enabled": config["enabled"],
                    "has_api_key": bool(config.get("api_key"))
                }
                for name, config in self.providers.items()
            },
            "conversation_histories": len(self.conversation_history),
            "available_tools": list(self.available_tools.keys())
        }
