"""
Hugging Face Spaces Deployment Configuration
For deploying TEC Enhanced Persona System to Hugging Face Spaces
"""

import gradio as gr
import sqlite3
import json
import os
import sys
from pathlib import Path

# Add src to path
sys.path.insert(0, 'src')

from tec_tools.persona_manager import PersonaManager
from tec_tools.agentic_processor import AgenticProcessor
from tec_tools.data_persistence import TECDataManager

class TECHuggingFaceSpace:
    def __init__(self):
        # Initialize data manager for HF persistent storage
        self.data_manager = TECDataManager("./data")
        
        # Load settings
        self.settings = self.data_manager.load_settings()
        
        # Initialize core components
        self.setup_database()
        self.persona_manager = PersonaManager()
        self.ai_processor = AgenticProcessor()
        
        self.current_character = "default"
        self.conversation_history = []
        
    def setup_database(self):
        """Initialize database for HF Spaces"""
        db_path = Path("./data/tec_database.db")
        db_path.parent.mkdir(exist_ok=True)
        
        if not db_path.exists():
            # Initialize with character lore
            self.initialize_character_lore()
    
    def initialize_character_lore(self):
        """Initialize character lore for HF deployment"""
        from scripts.initialize_character_lore import initialize_all_lore
        initialize_all_lore()
    
    def chat_interface(self, message, history, character, creativity, memory_mode, reasoning_mode):
        """Main chat interface for Gradio"""
        if not message.strip():
            return "", history
        
        try:
            # Update current character
            self.current_character = character.lower()
            
            # Get character context
            character_lore = self.persona_manager.get_character_lore(character)
            
            # Process message with AI
            response = self.ai_processor.process_enhanced_chat(
                message=message,
                character=character,
                creativity=creativity,
                memory_mode=memory_mode,
                reasoning_mode=reasoning_mode,
                character_context=character_lore
            )
            
            # Update conversation history
            history.append((message, response))
            self.conversation_history = history
            
            # Save conversation
            self.data_manager.save_conversation(
                f"hf_session_{len(history)}", 
                [{"role": "user", "content": msg[0], "character": character} for msg in history] +
                [{"role": "assistant", "content": msg[1], "character": character} for msg in history]
            )
            
            return "", history
            
        except Exception as e:
            error_msg = f"Error: {str(e)}"
            history.append((message, error_msg))
            return "", history
    
    def create_persona(self, persona_name, persona_intro, persona_tags):
        """Create user persona"""
        try:
            persona_data = {
                "title": persona_name,
                "intro": persona_intro,
                "tags": [tag.strip() for tag in persona_tags.split(",") if tag.strip()],
                "created_via": "huggingface_spaces"
            }
            
            persona_id = self.persona_manager.create_persona(persona_data)
            
            if persona_id:
                return f"✅ Persona '{persona_name}' created successfully!"
            else:
                return "❌ Failed to create persona"
                
        except Exception as e:
            return f"❌ Error creating persona: {str(e)}"
    
    def get_character_info(self, character):
        """Get character information"""
        try:
            lore = self.persona_manager.get_character_lore(character)
            if lore:
                return f"**{character}**\n\n{lore.get('background', 'No background available')}"
            else:
                return f"No information available for {character}"
        except Exception as e:
            return f"Error: {str(e)}"
    
    def export_conversation(self):
        """Export conversation history"""
        try:
            if not self.conversation_history:
                return "No conversation to export"
            
            export_data = {
                "timestamp": self.data_manager.get_system_stats(),
                "character": self.current_character,
                "conversation": self.conversation_history
            }
            
            return json.dumps(export_data, indent=2)
        except Exception as e:
            return f"Export failed: {str(e)}"
    
    def create_interface(self):
        """Create the Gradio interface"""
        
        # Custom CSS for TEC styling
        css = """
        .gradio-container {
            background: linear-gradient(135deg, #0a0a0f 0%, #1a1a2e 50%, #16213e 100%);
            color: #e0e6ed;
        }
        .gr-button-primary {
            background: linear-gradient(135deg, #7c3aed 0%, #a855f7 100%);
            border: none;
        }
        .gr-panel {
            background: rgba(255,255,255,0.05);
            backdrop-filter: blur(20px);
            border: 1px solid rgba(255,255,255,0.1);
            border-radius: 16px;
        }
        """
        
        with gr.Blocks(
            title="TEC Enhanced Persona System", 
            css=css,
            theme=gr.themes.Base()
        ) as demo:
            
            gr.Markdown("""
            # 🚀 TEC: BITLyfe - Enhanced Persona System
            *The Creator's Rebellion - AI-Powered Digital Sovereignty Companion*
            
            Experience the complete TEC persona system with character selection, enhanced AI responses, and persistent data storage.
            """)
            
            with gr.Row():
                with gr.Column(scale=2):
                    # Main Chat Interface
                    chatbot = gr.Chatbot(
                        height=500,
                        label="Chat with TEC Characters",
                        show_label=True,
                        container=True
                    )
                    
                    with gr.Row():
                        msg_input = gr.Textbox(
                            placeholder="Chat with your chosen TEC character...",
                            container=False,
                            scale=4
                        )
                        send_btn = gr.Button("Send", variant="primary", scale=1)
                
                with gr.Column(scale=1):
                    # Character Selection
                    gr.Markdown("## 🎭 Character Selection")
                    character_select = gr.Dropdown(
                        choices=["Polkin", "Mynx", "Kaelen", "Default"],
                        value="Polkin",
                        label="Choose Character",
                        info="Each character has unique personality and knowledge"
                    )
                    
                    character_info = gr.Textbox(
                        label="Character Info",
                        value="Select a character to see their background",
                        lines=4,
                        interactive=False
                    )
                    
                    # AI Settings
                    gr.Markdown("## ⚙️ AI Settings")
                    creativity_slider = gr.Slider(
                        minimum=0,
                        maximum=100,
                        value=70,
                        step=5,
                        label="Creativity",
                        info="Higher = more creative responses"
                    )
                    
                    memory_select = gr.Dropdown(
                        choices=["short", "medium", "long"],
                        value="medium",
                        label="Memory Length",
                        info="How much conversation history to remember"
                    )
                    
                    reasoning_select = gr.Dropdown(
                        choices=["simple", "balanced", "complex"],
                        value="balanced",
                        label="Reasoning Mode",
                        info="Depth of AI reasoning process"
                    )
            
            with gr.Row():
                with gr.Column():
                    # Persona Creation
                    gr.Markdown("## 👤 Create Your Persona")
                    with gr.Row():
                        persona_name = gr.Textbox(label="Persona Name", placeholder="Your Character Name")
                        persona_intro = gr.Textbox(label="Introduction", placeholder="Describe your persona...")
                    
                    persona_tags = gr.Textbox(label="Tags", placeholder="creative, analytical, spiritual")
                    create_persona_btn = gr.Button("Create Persona", variant="secondary")
                    persona_result = gr.Textbox(label="Result", interactive=False)
                
                with gr.Column():
                    # Export/Import
                    gr.Markdown("## 📤 Data Management")
                    export_btn = gr.Button("Export Conversation", variant="secondary")
                    export_output = gr.Textbox(
                        label="Exported Data",
                        lines=5,
                        interactive=False,
                        placeholder="Exported conversation will appear here..."
                    )
            
            # Event handlers
            def update_character_info(character):
                return self.get_character_info(character)
            
            # Chat events
            send_btn.click(
                self.chat_interface,
                inputs=[msg_input, chatbot, character_select, creativity_slider, memory_select, reasoning_select],
                outputs=[msg_input, chatbot]
            )
            
            msg_input.submit(
                self.chat_interface,
                inputs=[msg_input, chatbot, character_select, creativity_slider, memory_select, reasoning_select],
                outputs=[msg_input, chatbot]
            )
            
            # Character selection
            character_select.change(
                update_character_info,
                inputs=[character_select],
                outputs=[character_info]
            )
            
            # Persona creation
            create_persona_btn.click(
                self.create_persona,
                inputs=[persona_name, persona_intro, persona_tags],
                outputs=[persona_result]
            )
            
            # Export
            export_btn.click(
                self.export_conversation,
                outputs=[export_output]
            )
            
            # Load initial character info
            demo.load(
                lambda: self.get_character_info("Polkin"),
                outputs=[character_info]
            )
        
        return demo

def create_tec_space():
    """Create and launch the TEC HF Space"""
    tec_space = TECHuggingFaceSpace()
    demo = tec_space.create_interface()
    
    return demo

# For Hugging Face Spaces deployment
if __name__ == "__main__":
    demo = create_tec_space()
    demo.launch(
        server_name="0.0.0.0",
        server_port=7860,
        share=False,
        show_error=True
    )
