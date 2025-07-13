#!/usr/bin/env python3
"""
Simple TEC API Server
Provides basic API endpoints for the web interface
"""
import os
import json
import logging
from datetime import datetime
from flask import Flask, request, jsonify, send_from_directory
from flask_cors import CORS

app = Flask(__name__)
CORS(app)

# Set up logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

@app.route('/health')
def health():
    """Health check endpoint"""
    return jsonify({
        'status': 'ok',
        'timestamp': datetime.now().isoformat(),
        'service': 'TEC API',
        'version': '1.0.0'
    })

@app.route('/chat', methods=['POST'])
def chat():
    """Basic chat endpoint"""
    try:
        data = request.get_json()
        message = data.get('message', '')
        
        # Simple response logic
        if not message:
            return jsonify({'error': 'No message provided'}), 400
        
        # Generate a basic response
        response = generate_response(message)
        
        return jsonify({
            'response': response,
            'timestamp': datetime.now().isoformat()
        })
        
    except Exception as e:
        logger.error(f"Chat error: {e}")
        return jsonify({'error': 'Internal server error'}), 500

def generate_response(message):
    """Generate a basic response to user messages"""
    message_lower = message.lower()
    
    if 'status' in message_lower:
        return "TEC System Status: Web interface is running. MCP servers are in development mode. Basic functionality available."
    
    elif 'journal' in message_lower:
        return "Journal feature: Ready to help you with personal reflection and note-taking. Future updates will include AI-powered analysis."
    
    elif 'finance' in message_lower or 'crypto' in message_lower:
        return "Finance tracking: Currently in development. Will support cryptocurrency monitoring and financial insights."
    
    elif 'quest' in message_lower:
        return "Quest system: RPG-style goal tracking and gamification features coming soon. Your adventure awaits!"
    
    elif 'hello' in message_lower or 'hi' in message_lower:
        return "Greetings! I am Daisy Purecode, your digital sovereignty companion. How can I assist you in The Creator's Rebellion today?"
    
    else:
        return f"I understand you said: '{message}'. The TEC system is currently in development mode. Full AI capabilities will be available once all MCP servers are properly configured."

@app.route('/')
def serve_chat():
    """Serve the chat interface"""
    return send_from_directory('.', 'tec_chat.html')

if __name__ == '__main__':
    logger.info("Starting TEC Simple API Server...")
    logger.info("Web interface available at: http://localhost:8000")
    logger.info("Health check at: http://localhost:8000/health")
    
    app.run(
        host='localhost',
        port=8000,
        debug=False,
        threaded=True
    )
