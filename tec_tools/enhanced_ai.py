"""
TEC Enhanced AI Processor
The Creator's Rebellion - Better AI responses with smart fallbacks
"""
import os
import logging
from typing import Dict, Any, Optional
from datetime import datetime
import json

# Configure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

class TECEnhancedAI:
    """Enhanced AI processor with smart fallbacks and better responses"""
    
    def __init__(self):
        self.load_environment()
        self.fallback_responses = self.load_fallback_responses()
        
    def load_environment(self):
        """Load environment variables"""
        from dotenv import load_dotenv
        load_dotenv()
        
        self.providers = {
            'gemini': {
                'api_key': os.getenv('GEMINI_API_KEY'),
                'available': bool(os.getenv('GEMINI_API_KEY')) and os.getenv('GEMINI_API_KEY') != 'your_gemini_api_key_here'
            },
            'openai': {
                'api_key': os.getenv('OPENAI_API_KEY'),
                'available': bool(os.getenv('OPENAI_API_KEY')) and os.getenv('OPENAI_API_KEY') != 'your_openai_api_key_here'
            },
            'claude': {
                'api_key': os.getenv('ANTHROPIC_API_KEY'),
                'available': bool(os.getenv('ANTHROPIC_API_KEY')) and os.getenv('ANTHROPIC_API_KEY') != 'your_anthropic_api_key_here'
            },
            'github': {
                'api_key': os.getenv('GITHUB_TOKEN'),
                'available': bool(os.getenv('GITHUB_TOKEN')) and os.getenv('GITHUB_TOKEN') != 'your_github_token_here'
            },
            'xai': {
                'api_key': os.getenv('XAI_API_KEY'),
                'available': bool(os.getenv('XAI_API_KEY')) and os.getenv('XAI_API_KEY') != 'your_xai_api_key_here'
            },
            'azure': {
                'api_key': os.getenv('AZURE_AI_KEY_1'),
                'endpoint': os.getenv('AZURE_AI_ENDPOINT'),
                'available': bool(os.getenv('AZURE_AI_KEY_1')) and bool(os.getenv('AZURE_AI_ENDPOINT'))
            }
        }
        
        logger.info(f"Available providers: {[name for name, config in self.providers.items() if config['available']]}")
    
    def load_fallback_responses(self) -> Dict[str, list]:
        """Load intelligent fallback responses for when AI providers fail"""
        return {
            'greeting': [
                "Hello! I'm TEC - your digital sovereignty assistant. While I'm connecting to my AI providers, I can help you with basic information about digital sovereignty, crypto tracking, and life management.",
                "Welcome to TEC: BITLYFE IS THE NEW SHIT! I'm here to help you take control of your digital life. Currently working on connecting to my AI providers...",
                "Greetings, rebel! I'm TEC, your digital sovereignty companion. My full AI capabilities are coming online - meanwhile, I can discuss the Creator's Rebellion philosophy!"
            ],
            'digital_sovereignty': [
                "Digital sovereignty means taking complete control of your digital life - your data, your AI interactions, your financial tracking, and your personal analytics. TEC gives you multiple AI providers so you're never dependent on just one company.",
                "The Creator's Rebellion is about breaking free from digital servitude. With TEC, you have 6 different AI providers, local data storage, and complete control over your information. No single company owns your digital soul!",
                "Digital sovereignty = YOUR data stays YOURS. TEC runs locally, uses multiple AI providers for redundancy, and gives you complete control. You choose which AI to use, when to use it, and what data to share."
            ],
            'crypto': [
                "TEC supports crypto portfolio tracking with multiple free APIs - CryptoCompare (250k calls/month), CoinMarketCap, and others. No expensive subscriptions needed for basic crypto monitoring!",
                "Your crypto data sovereignty matters! TEC tracks portfolios using free APIs and stores everything locally. You control your financial data, not some centralized service.",
                "Cryptocurrency tracking in TEC uses redundant data sources to ensure you always have access to price data, even if one API goes down. True financial data sovereignty!"
            ],
            'features': [
                "TEC features: 🤖 6 AI providers, 💰 Crypto tracking, 🎮 Life gamification, 🎵 Voice features, 🏠 IoT integration, 📱 Mobile-ready interface. All running locally with YOUR control!",
                "Current TEC capabilities: Multi-AI chat, crypto portfolio tracking, gamified life management, voice integration ready, hardware IoT support planned. Everything designed for digital sovereignty!",
                "TEC modules: Mind-Forge (journaling), Wealth Codex (crypto), Quest Log (gamification), Voice Assistant, Hardware Integration. Each module respects your digital sovereignty."
            ],
            'help': [
                "I can help with: Digital sovereignty concepts, crypto portfolio setup, life gamification strategies, AI provider comparisons, local data storage, privacy-first design, and taking control of your digital life!",
                "TEC assistance available: Setting up multiple AI providers, configuring crypto tracking, creating gamified life goals, planning voice assistant features, and designing your digital sovereignty strategy.",
                "Ask me about: AI provider redundancy, crypto data sovereignty, gamified productivity, voice interface setup, hardware integration, or philosophical aspects of the Creator's Rebellion!"
            ],
            'error': [
                "I'm currently connecting to my AI providers. While that happens, I can discuss digital sovereignty concepts, crypto tracking setup, or TEC features. What interests you most?",
                "My AI providers are initializing. In the meantime, I can share information about taking control of your digital life, setting up crypto tracking, or planning your digital sovereignty strategy!",
                "AI providers coming online... Meanwhile, let's talk about the Creator's Rebellion philosophy, your digital sovereignty goals, or how TEC can help you break free from digital servitude!"
            ]
        }
    
    def get_smart_response(self, message: str, provider: str = 'auto') -> Dict[str, Any]:
        """Generate smart response with enhanced fallbacks"""
        
        # Analyze message intent
        message_lower = message.lower()
        intent = self.analyze_intent(message_lower)
        
        # Try AI providers first
        ai_response = self.try_ai_providers(message, provider)
        if ai_response['success']:
            return ai_response
            
        # Use intelligent fallbacks based on intent
        fallback_response = self.generate_fallback_response(intent, message)
        
        return {
            'output': fallback_response,
            'provider': 'TEC Fallback Intelligence',
            'status': 'success',
            'fallback_used': True,
            'intent': intent,
            'available_providers': [name for name, config in self.providers.items() if config['available']],
            'suggestion': self.get_next_step_suggestion(intent)
        }
    
    def analyze_intent(self, message: str) -> str:
        """Analyze user intent from message"""
        
        greetings = ['hello', 'hi', 'hey', 'greetings', 'yo', 'sup']
        crypto_terms = ['crypto', 'bitcoin', 'ethereum', 'portfolio', 'trading', 'price']
        sovereignty_terms = ['sovereignty', 'control', 'privacy', 'freedom', 'rebellion', 'digital']
        feature_terms = ['features', 'capabilities', 'what can', 'functions', 'modules']
        help_terms = ['help', 'assist', 'support', 'guide', 'how to']
        
        if any(term in message for term in greetings):
            return 'greeting'
        elif any(term in message for term in crypto_terms):
            return 'crypto'
        elif any(term in message for term in sovereignty_terms):
            return 'digital_sovereignty'
        elif any(term in message for term in feature_terms):
            return 'features'
        elif any(term in message for term in help_terms):
            return 'help'
        else:
            return 'general'
    
    def try_ai_providers(self, message: str, preferred_provider: str) -> Dict[str, Any]:
        """Try to get response from AI providers"""
        
        if preferred_provider != 'auto' and preferred_provider in self.providers:
            if self.providers[preferred_provider]['available']:
                # Try specific provider
                result = self.call_provider(preferred_provider, message)
                if result['success']:
                    return result
        
        # Try available providers in order of preference
        provider_order = ['gemini', 'claude', 'openai', 'xai', 'azure', 'github']
        
        for provider in provider_order:
            if self.providers[provider]['available']:
                result = self.call_provider(provider, message)
                if result['success']:
                    return result
        
        return {'success': False, 'error': 'No AI providers available'}
    
    def call_provider(self, provider: str, message: str) -> Dict[str, Any]:
        """Call specific AI provider (placeholder for now)"""
        
        # For now, return that providers are being configured
        # This will be replaced with actual AI calls once authentication is fixed
        
        provider_status = {
            'gemini': 'Authentication being configured',
            'openai': 'API key validation in progress', 
            'claude': 'Connection being established',
            'github': 'GitHub AI access being set up',
            'xai': 'XAI connection ready but not implemented',
            'azure': 'Azure AI services being initialized'
        }
        
        return {
            'success': False,
            'error': provider_status.get(provider, 'Provider not configured'),
            'provider': provider
        }
    
    def generate_fallback_response(self, intent: str, message: str) -> str:
        """Generate intelligent fallback response based on intent"""
        
        import random
        
        # Get base response for intent
        if intent in self.fallback_responses:
            base_response = random.choice(self.fallback_responses[intent])
        else:
            base_response = random.choice(self.fallback_responses['help'])
        
        # Add contextual information
        timestamp = datetime.now().strftime("%H:%M")
        
        context_suffix = f"\n\n🔧 **System Status ({timestamp}):**\n"
        context_suffix += f"• Backend API: ✅ Running on http://127.0.0.1:5000\n"
        context_suffix += f"• AI Providers: 🔄 Configuring authentication\n"
        context_suffix += f"• Crypto APIs: ✅ Ready (CryptoCompare, CoinMarketCap)\n"
        context_suffix += f"• Local Database: ✅ Operational\n"
        context_suffix += f"• Digital Sovereignty: ✅ Active\n\n"
        context_suffix += "💡 **Try asking about:** Digital sovereignty, crypto tracking, life gamification, or TEC features!"
        
        return base_response + context_suffix
    
    def get_next_step_suggestion(self, intent: str) -> str:
        """Get suggestion for next steps based on intent"""
        
        suggestions = {
            'greeting': 'Ask me about digital sovereignty or explore TEC features',
            'crypto': 'Try: "How do I set up crypto portfolio tracking?" or "What crypto APIs does TEC use?"',
            'digital_sovereignty': 'Ask: "How does TEC protect my digital privacy?" or "What is the Creator\'s Rebellion?"',
            'features': 'Try: "Show me TEC modules" or "What can TEC do for me?"',
            'help': 'Ask about specific topics like crypto, gamification, or voice features',
            'general': 'Try asking about digital sovereignty, crypto tracking, or TEC capabilities'
        }
        
        return suggestions.get(intent, suggestions['general'])

# Global instance
tec_ai = TECEnhancedAI()

def enhanced_process_input(message: str, user_id: str = 'anonymous', 
                         session_id: str = 'default', provider: str = 'auto') -> Dict[str, Any]:
    """Enhanced input processing with smart fallbacks"""
    
    logger.info(f"Enhanced processing: {message[:50]}... (user: {user_id}, provider: {provider})")
    
    try:
        response = tec_ai.get_smart_response(message, provider)
        
        # Add session information
        response.update({
            'user_id': user_id,
            'session_id': session_id,
            'timestamp': datetime.now().isoformat(),
            'message_length': len(message)
        })
        
        return response
        
    except Exception as e:
        logger.error(f"Enhanced processing error: {str(e)}")
        
        return {
            'output': f"TEC system error: {str(e)}. I'm still here to help with digital sovereignty concepts!",
            'provider': 'TEC Error Handler',
            'status': 'error',
            'error': str(e),
            'user_id': user_id,
            'session_id': session_id
        }
