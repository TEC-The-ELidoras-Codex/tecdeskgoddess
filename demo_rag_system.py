#!/usr/bin/env python3
"""
TEC RAG (Retrieval Augmented Generation) Example
Part of TEC Clean Architecture Protocol TEC_ARCH_071925_V1

This demonstrates how to give your AI access to your specific game knowledge.
"""

import os
import json
from pathlib import Path

# Simple in-memory vector store (for demo - use ChromaDB for production)
class SimpleRAG:
    def __init__(self):
        self.documents = []
        self.knowledge_base = {}
    
    def add_document(self, doc_id, content, metadata=None):
        """Add a document to the knowledge base"""
        self.documents.append({
            "id": doc_id,
            "content": content,
            "metadata": metadata or {}
        })
        print(f"📄 Added document: {doc_id}")
    
    def search(self, query, max_results=3):
        """Simple keyword search (in production, use embeddings)"""
        query_lower = query.lower()
        results = []
        
        for doc in self.documents:
            content_lower = doc["content"].lower()
            # Simple relevance scoring based on keyword matches
            score = sum(1 for word in query_lower.split() if word in content_lower)
            if score > 0:
                results.append((score, doc))
        
        # Sort by relevance and return top results
        results.sort(key=lambda x: x[0], reverse=True)
        return [doc for score, doc in results[:max_results]]
    
    def get_context(self, query):
        """Get relevant context for a query"""
        relevant_docs = self.search(query)
        context = "\n\n".join([doc["content"] for doc in relevant_docs])
        return context

def create_tec_knowledge_base():
    """Create a knowledge base with TEC: BITLYFE information"""
    rag = SimpleRAG()
    
    # Add game world knowledge
    rag.add_document("world_overview", """
    TEC: BITLYFE is a fantasy RPG set in the world of Eldoras. 
    The game features a modular clean architecture with AI-powered NPCs.
    Players can explore different biomes, each with unique characteristics and inhabitants.
    """, {"category": "world"})
    
    rag.add_document("npc_thorin", """
    Thorin Ironforge is the master blacksmith of Ironhold Village.
    He's a gruff but kind-hearted dwarf who takes pride in his craft.
    Thorin can repair weapons, craft new equipment, and shares stories of ancient forging techniques.
    He has a deep respect for quality craftsmanship and dislikes rushed work.
    """, {"category": "character", "name": "Thorin"})
    
    rag.add_document("location_ironhold", """
    Ironhold Village is a mining settlement nestled in the Ironback Mountains.
    The village is known for its skilled blacksmiths and rich iron deposits.
    Key locations include Thorin's Forge, the Iron Mine, and the Mountain Inn.
    The village is protected by stone walls and has a guard tower overlooking the main path.
    """, {"category": "location", "name": "Ironhold Village"})
    
    rag.add_document("game_mechanics", """
    The TEC Clean Architecture consists of four layers:
    1. Core Layer: Contains game entities like Player, NPC, GameWorld, Item
    2. Service Layer: Handles business logic like PlayerService, NPCService, MCPService
    3. Facade Layer: Provides unified interface via GameFacade
    4. UI Layer: Flask API endpoints for game interactions
    
    NPCs use AI-powered dialogue generation with personality-driven responses.
    """, {"category": "system"})
    
    rag.add_document("crafting_system", """
    The crafting system allows players to create items using materials and recipes.
    Thorin the Blacksmith specializes in metal weapons and armor.
    Required materials include iron ore, coal for fuel, and various gems for enchantments.
    Higher skill levels unlock more complex recipes and better quality items.
    """, {"category": "gameplay", "system": "crafting"})
    
    return rag

def demo_rag_queries():
    """Demonstrate RAG functionality with example queries"""
    print("🧠 Creating TEC: BITLYFE Knowledge Base...")
    rag = create_tec_knowledge_base()
    
    print(f"📚 Knowledge base created with {len(rag.documents)} documents\n")
    
    # Test queries
    test_queries = [
        "Tell me about Thorin the blacksmith",
        "What can I do in Ironhold Village?", 
        "How does the crafting system work?",
        "What is the TEC Clean Architecture?",
        "Where can I get my weapons repaired?"
    ]
    
    for query in test_queries:
        print("=" * 60)
        print(f"🔍 Query: {query}")
        print("-" * 40)
        
        # Get relevant context
        context = rag.get_context(query)
        
        if context:
            print("📖 Relevant Context:")
            print(context)
            
            # This is where you'd call your AI model (Ollama) with the context
            print("\n🤖 [AI Response would use this context to give accurate, specific answers]")
        else:
            print("❌ No relevant information found")
        
        print()

def create_rag_enhanced_prompt(query, rag_context):
    """Create a prompt that includes RAG context for better AI responses"""
    return f"""
You are an AI assistant for TEC: BITLYFE, a fantasy RPG game.

CONTEXT FROM KNOWLEDGE BASE:
{rag_context}

PLAYER QUERY: {query}

Please provide a helpful response based on the context above. If the context doesn't contain relevant information, say so clearly.

Response:"""

def demo_ai_integration():
    """Show how RAG integrates with AI models"""
    print("\n🔌 RAG + AI Integration Demo")
    print("=" * 40)
    
    rag = create_tec_knowledge_base()
    
    query = "I want to craft a sword. Who should I talk to?"
    context = rag.get_context(query)
    
    prompt = create_rag_enhanced_prompt(query, context)
    
    print("📝 Generated Prompt for AI:")
    print("-" * 30)
    print(prompt)
    print("-" * 30)
    print("\n💡 This prompt would be sent to Ollama for a contextually accurate response!")

def save_knowledge_base():
    """Save knowledge base to file for persistence"""
    rag = create_tec_knowledge_base()
    
    # Convert to JSON for saving
    kb_data = {
        "documents": rag.documents,
        "created_at": "2025-07-20",
        "game": "TEC: BITLYFE"
    }
    
    kb_file = Path("data/tec_knowledge_base.json")
    kb_file.parent.mkdir(exist_ok=True)
    
    with open(kb_file, 'w') as f:
        json.dump(kb_data, f, indent=2)
    
    print(f"💾 Knowledge base saved to: {kb_file}")
    return kb_file

def main():
    """Main demo function"""
    print("🧠 TEC: BITLYFE - RAG (Retrieval Augmented Generation) Demo")
    print("=" * 60)
    print()
    
    # Demo basic RAG functionality
    demo_rag_queries()
    
    # Demo AI integration
    demo_ai_integration()
    
    # Save knowledge base
    kb_file = save_knowledge_base()
    
    print("\n🎯 Next Steps:")
    print("1. Install chromadb: pip install chromadb sentence-transformers")
    print("2. Replace SimpleRAG with ChromaDB for better search")
    print("3. Integrate with Ollama for AI responses")
    print("4. Add more game knowledge to the knowledge base")
    print(f"5. Load knowledge base from: {kb_file}")
    
    print("\n🔗 Integration with TEC Clean Architecture:")
    print("- Add RAGService to the Service Layer")
    print("- Use in NPCService for contextual dialogue")
    print("- Expose via GameFacade for easy access")
    print("- Add REST endpoints for knowledge management")

if __name__ == "__main__":
    main()
