# ==============================================================================
# TEC PROTOCOL: KIMI-K2 LOCAL INFERENCE ENGINE
# OBJECTIVE: Load the downloaded Kimi-K2 GGUF model and demonstrate its
#            agentic tool-calling capabilities.
# ==============================================================================

import json
import sys
import os
from typing import Dict, List, Any, Optional

# Check if llama-cpp-python is installed
try:
    from llama_cpp import Llama
except ImportError:
    print("❌ ERROR: llama-cpp-python is not installed.")
    print("   Please install it with: pip install llama-cpp-python")
    sys.exit(1)

# --- CONFIGURATION ---
# IMPORTANT: Update this path to where you saved the downloaded .gguf file.
MODEL_PATH = "./models/kimi-k2-instruct-IQ2_XXS.gguf" 

# --- TOOL DEFINITIONS ---
# This is where we define the tools the AI can use.

def get_weather(city: str) -> dict:
    """A mock function to get the weather for a city."""
    print(f"--- [TOOL EXECUTED: get_weather(city='{city}')] ---")
    # In a real application, this would call a real weather API.
    return {"weather": "Sunny, with a high chance of digital rebellion."}

def get_player_info(player_id: str) -> dict:
    """Mock function to get player information."""
    print(f"--- [TOOL EXECUTED: get_player_info(player_id='{player_id}')] ---")
    return {
        "player_id": player_id,
        "name": "Brave Adventurer",
        "level": 15,
        "health": 85,
        "location": "Enchanted Forest"
    }

def start_battle(participants: List[str], battle_type: str = "pve") -> dict:
    """Mock function to start a battle."""
    print(f"--- [TOOL EXECUTED: start_battle(participants={participants}, type='{battle_type}')] ---")
    return {
        "battle_id": "battle_001",
        "participants": participants,
        "type": battle_type,
        "status": "Battle initiated! Roll for initiative!"
    }

# The schema tells the AI what the tool is, what it does, and what parameters it needs.
# This is a core concept of agentic AI.
tools = [
    {
        "type": "function",
        "function": {
            "name": "get_weather",
            "description": "Retrieve current weather information. Call this when the user asks about the weather.",
            "parameters": {
                "type": "object",
                "required": ["city"],
                "properties": {
                    "city": {
                        "type": "string",
                        "description": "Name of the city, e.g., Buffalo, NY"
                    }
                }
            }
        }
    },
    {
        "type": "function", 
        "function": {
            "name": "get_player_info",
            "description": "Get information about a player in the TEC: BITLYFE game.",
            "parameters": {
                "type": "object",
                "required": ["player_id"],
                "properties": {
                    "player_id": {
                        "type": "string",
                        "description": "The unique identifier for the player"
                    }
                }
            }
        }
    },
    {
        "type": "function",
        "function": {
            "name": "start_battle",
            "description": "Initiate a battle between game entities.",
            "parameters": {
                "type": "object",
                "required": ["participants"],
                "properties": {
                    "participants": {
                        "type": "array",
                        "items": {"type": "string"},
                        "description": "List of participant IDs for the battle"
                    },
                    "battle_type": {
                        "type": "string",
                        "description": "Type of battle: pve, pvp, siege, etc.",
                        "default": "pve"
                    }
                }
            }
        }
    }
]

# A mapping to call the actual Python function based on the tool's name.
tool_map = {
    "get_weather": get_weather,
    "get_player_info": get_player_info,
    "start_battle": start_battle
}

class KimiK2Server:
    """
    Local Kimi-K2 server that can be integrated with TEC: BITLYFE
    """
    
    def __init__(self, model_path: str = MODEL_PATH):
        self.model_path = model_path
        self.llm = None
        self.is_loaded = False
        
    def load_model(self) -> bool:
        """Load the Kimi-K2 model"""
        print("--- [INITIALIZING LOCAL INFERENCE ENGINE] ---")
        print(f"Attempting to load model from: {self.model_path}")
        
        if not os.path.exists(self.model_path):
            print(f"❌ ERROR: Model file not found at {self.model_path}")
            print("   Please download the model file and update MODEL_PATH")
            return False
        
        try:
            # Load the model from the specified path.
            # n_ctx: The context window size. Kimi-K2 is massive, but we'll keep it reasonable.
            # n_gpu_layers: -1 tries to offload all possible layers to the GPU.
            #               On your Legion Go, this will use the integrated graphics.
            # verbose=True: Shows detailed loading information.
            self.llm = Llama(
                model_path=self.model_path,
                n_ctx=8192,
                n_gpu_layers=-1,
                verbose=True
            )
            print("\n✅ SUCCESS: Kimi-K2 Model Loaded Locally.")
            self.is_loaded = True
            return True
            
        except Exception as e:
            print(f"\n❌ ERROR: Failed to load model.")
            print(f"   If you are out of memory, try a smaller model (e.g., a 2-bit quant).")
            print(f"   Error details: {e}")
            return False
    
    def generate_response(self, messages: List[Dict], use_tools: bool = True) -> Dict:
        """Generate a response using the loaded model"""
        if not self.is_loaded:
            return {
                "success": False,
                "error": "Model not loaded"
            }
        
        try:
            # This is where the magic happens. We ask the model to generate a response.
            # We pass the message history and the available tools.
            completion_args = {
                "messages": messages,
                "temperature": 0.6
            }
            
            if use_tools:
                completion_args["tools"] = tools
                completion_args["tool_choice"] = "auto"
            
            completion = self.llm.create_chat_completion(**completion_args)
            
            choice = completion['choices'][0]['message']
            
            # Check if the model decided to call a tool.
            if choice.get("tool_calls") and use_tools:
                print(f"--- [AI DECISION: TOOL CALL REQUIRED] ---")
                tool_call = choice["tool_calls"][0]
                tool_name = tool_call['function']['name']
                tool_args = json.loads(tool_call['function']['arguments'])
                
                # Execute the tool
                if tool_name in tool_map:
                    tool_function = tool_map[tool_name]
                    tool_result = tool_function(**tool_args)

                    # Add the tool's result back into the message history
                    # This lets the AI know what the tool's output was.
                    messages.append(choice)
                    messages.append({
                        "role": "tool",
                        "content": json.dumps(tool_result)
                    })

                    # Now, we call the model AGAIN with the tool result included,
                    # so it can generate a final, natural language response.
                    final_completion = self.llm.create_chat_completion(
                        messages=messages,
                        temperature=0.6
                    )
                    final_response = final_completion['choices'][0]['message']['content']
                    
                    return {
                        "success": True,
                        "content": final_response,
                        "tool_used": tool_name,
                        "tool_result": tool_result
                    }
                else:
                    return {
                        "success": False,
                        "error": f"Unknown tool: {tool_name}"
                    }
            else:
                # If no tool was called, just return the response.
                response_text = choice['content']
                return {
                    "success": True,
                    "content": response_text
                }
                
        except Exception as e:
            return {
                "success": False,
                "error": str(e)
            }

# --- MAIN INFERENCE LOGIC ---
def main():
    """
    Initializes the model and runs an interactive chat loop.
    """
    # Initialize the server
    server = KimiK2Server()
    
    if not server.load_model():
        return
    
    # The chat history starts with a system prompt.
    messages = [
        {"role": "system", "content": "You are Kimi, an AI assistant created by Moonshot AI. You are a helpful assistant with access to tools. You are now integrated into TEC: BITLYFE, a mystical RPG world where you can help players and NPCs interact."},
    ]

    print("\n--- [INTERACTIVE CHAT STARTED] ---")
    print("Type 'exit' to end the session.")
    print("Try asking about the weather, player info, or starting a battle!")

    while True:
        user_input = input("\n[USER]: ")
        if user_input.lower() == 'exit':
            print("--- [SESSION TERMINATED] ---")
            break

        messages.append({"role": "user", "content": user_input})

        # Generate response
        response = server.generate_response(messages)
        
        if response["success"]:
            print(f"\n[KIMI]: {response['content']}")
            messages.append({"role": "assistant", "content": response['content']})
            
            if response.get("tool_used"):
                print(f"--- [TOOL RESULT: {response['tool_used']}] ---")
                print(f"Result: {response['tool_result']}")
        else:
            print(f"\n❌ ERROR: {response['error']}")

def test_installation():
    """Test if everything is set up correctly"""
    print("=== TEC KIMI-K2 INSTALLATION TEST ===\n")
    
    # Check if model file exists
    if os.path.exists(MODEL_PATH):
        print(f"✅ Model file found at: {MODEL_PATH}")
        file_size = os.path.getsize(MODEL_PATH) / (1024**3)  # Size in GB
        print(f"   File size: {file_size:.2f} GB")
    else:
        print(f"❌ Model file NOT found at: {MODEL_PATH}")
        print("   Please download the model file first!")
        return False
    
    # Check memory (rough estimate)
    try:
        import psutil
        memory = psutil.virtual_memory()
        available_gb = memory.available / (1024**3)
        print(f"✅ Available RAM: {available_gb:.2f} GB")
        
        if available_gb < 4:
            print("⚠️  WARNING: Low memory. Model may not load properly.")
    except ImportError:
        print("⚠️  Could not check memory (psutil not installed)")
    
    # Test model loading
    print("\n--- Testing Model Load ---")
    server = KimiK2Server()
    if server.load_model():
        print("✅ Model loaded successfully!")
        
        # Test a simple query
        test_messages = [
            {"role": "system", "content": "You are a helpful AI assistant."},
            {"role": "user", "content": "Hello, can you tell me about yourself?"}
        ]
        
        response = server.generate_response(test_messages, use_tools=False)
        if response["success"]:
            print(f"✅ Test response: {response['content'][:100]}...")
            print("\n🎉 ALL TESTS PASSED! Kimi-K2 is ready for TEC: BITLYFE!")
            return True
        else:
            print(f"❌ Test failed: {response['error']}")
    
    return False

if __name__ == "__main__":
    if len(sys.argv) > 1 and sys.argv[1] == "--test":
        test_installation()
    else:
        main()
