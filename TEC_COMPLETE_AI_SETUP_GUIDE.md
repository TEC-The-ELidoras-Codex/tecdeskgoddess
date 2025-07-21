# 🚀 TEC: BITLYFE - Complete AI Setup Guide
## Clean Architecture Protocol TEC_ARCH_071925_V1 + Local AI + RAG + Docker + MCP

---

## 🏗️ **Current Status: COMPLETE**
✅ **TEC Clean Architecture Protocol TEC_ARCH_071925_V1** - 100% Operational
- Core Layer: Player, NPC, GameWorld, Item classes
- Service Layer: MCPService, PlayerService, NPCService  
- Facade Layer: GameFacade unified interface
- UI Layer: Flask integration with legacy compatibility

✅ **Ollama** - Installed and detected in Hugging Face settings

---

## 🎯 **Phase 1: Local AI with Ollama (Start Here)**

### Step 1: Verify Ollama Installation
```bash
# Check version
ollama --version

# List available models
ollama list
```

### Step 2: Install Recommended Models
```bash
# For Text Generation (Choose one based on your 12GB RAM):

# Option A: Best balance - 2GB model
ollama pull llama3.2:3b

# Option B: Fastest - 1.3GB model  
ollama pull llama3.2:1b

# Option C: Alternative - 1.6GB model
ollama pull gemma2:2b
```

### Step 3: Test Your Model
```bash
# Test basic functionality
ollama run llama3.2:3b "You are a wise sage in an RPG. Introduce yourself briefly."

# Test for TEC integration
ollama run llama3.2:3b "You are an NPC blacksmith named Thorin. A player just entered your shop. Greet them."
```

### Step 4: Start TEC System
```bash
cd C:\Users\Ghedd\TEC_CODE\tecdeskgoddess
python tec_enhanced_api.py
```

### Step 5: Verify Integration
- Visit: http://localhost:5000/health
- Should show: "Clean Architecture Status: ✅ Fully Operational"

---

## 🖼️ **Phase 2: Image Generation Setup**

### Option A: Local with Draw Things (Recommended for you)
Since you have **Draw Things** checked in Hugging Face:

```bash
# Install Stable Diffusion via Ollama (if supported)
ollama pull stable-diffusion

# Or use Draw Things directly from Hugging Face interface
```

### Option B: Docker Image Generation
```bash
# Pull Stable Diffusion Docker container
docker pull stabilityai/stable-diffusion:latest

# Run image generation container
docker run -p 7860:7860 stabilityai/stable-diffusion:latest
```

---

## 🧠 **Phase 3: RAG (Retrieval Augmented Generation) Setup**

### What is RAG?
RAG lets your AI access and reason over your specific documents/knowledge base instead of just using training data.

### Step 1: Install RAG Dependencies
```bash
pip install chromadb sentence-transformers langchain
```

### Step 2: Create TEC RAG System
```python
# File: tec_tools/rag_service.py
import chromadb
from sentence_transformers import SentenceTransformer
import os

class TECRAGService:
    def __init__(self):
        self.client = chromadb.Client()
        self.collection = self.client.create_collection("tec_knowledge")
        self.encoder = SentenceTransformer('all-MiniLM-L6-v2')
    
    def add_documents(self, docs, ids):
        """Add documents to knowledge base"""
        embeddings = self.encoder.encode(docs)
        self.collection.add(
            embeddings=embeddings.tolist(),
            documents=docs,
            ids=ids
        )
    
    def query(self, question, n_results=3):
        """Query knowledge base"""
        query_embedding = self.encoder.encode([question])
        results = self.collection.query(
            query_embeddings=query_embedding.tolist(),
            n_results=n_results
        )
        return results['documents'][0]
```

### Step 3: Add Your Game Knowledge
```python
# Add your RPG lore, rules, character backgrounds
rag_service = TECRAGService()

game_docs = [
    "TEC: BITLYFE is a fantasy RPG with modular architecture...",
    "NPCs use AI-powered dialogue generation...",
    "The Clean Architecture has 4 layers: Core, Service, Facade, UI...",
    # Add your specific game content
]

rag_service.add_documents(game_docs, [f"doc_{i}" for i in range(len(game_docs))])
```

---

## 🐳 **Phase 4: Docker Advanced Setup**

### Why Docker?
- Run larger models that don't fit in Ollama
- Isolate different AI services
- Easy scaling and deployment

### Step 1: Install Docker Desktop
If not already installed: https://www.docker.com/products/docker-desktop/

### Step 2: TEC Docker Setup
```dockerfile
# File: Dockerfile.tec-ai
FROM python:3.11-slim

WORKDIR /app

# Install system dependencies
RUN apt-get update && apt-get install -y \
    gcc \
    g++ \
    && rm -rf /var/lib/apt/lists/*

# Copy requirements
COPY requirements.txt .
RUN pip install -r requirements.txt

# Copy TEC code
COPY . .

# Expose ports
EXPOSE 5000 8000

# Start command
CMD ["python", "tec_enhanced_api.py"]
```

### Step 3: Docker Compose for Full Stack
```yaml
# File: docker-compose.yml
version: '3.8'
services:
  tec-api:
    build:
      context: .
      dockerfile: Dockerfile.tec-ai
    ports:
      - "5000:5000"
    environment:
      - OLLAMA_URL=http://ollama:11434
    depends_on:
      - ollama
      - chromadb
  
  ollama:
    image: ollama/ollama:latest
    ports:
      - "11434:11434"
    volumes:
      - ollama_data:/root/.ollama
  
  chromadb:
    image: chromadb/chroma:latest
    ports:
      - "8000:8000"
    volumes:
      - chromadb_data:/chroma/chroma

volumes:
  ollama_data:
  chromadb_data:
```

### Step 4: Run with Docker
```bash
# Start everything
docker-compose up -d

# Check status
docker-compose ps

# View logs
docker-compose logs -f tec-api
```

---

## 🔗 **Phase 5: MCP Server Integration with Hugging Face**

### Step 1: Get Your Hugging Face Token
1. Go to: https://huggingface.co/settings/tokens
2. Create new token with READ permissions
3. Copy the token

### Step 2: Configure VS Code MCP
Create file: `.vscode/mcp.json`
```json
{
  "servers": {
    "hf-mcp-server": {
      "url": "https://huggingface.co/mcp",
      "headers": {
        "Authorization": "Bearer hf_your_token_here"
      }
    }
  }
}
```

### Step 3: Enhanced TEC MCP Service
```python
# File: tec_tools/enhanced_mcp_service.py
import requests
import json

class EnhancedMCPService:
    def __init__(self):
        self.hf_token = os.getenv("HF_TOKEN")
        self.hf_headers = {"Authorization": f"Bearer {self.hf_token}"}
    
    def search_models(self, task="text-generation", limit=5):
        """Search Hugging Face models"""
        url = "https://huggingface.co/api/models"
        params = {"filter": task, "limit": limit}
        response = requests.get(url, params=params, headers=self.hf_headers)
        return response.json()
    
    def search_spaces(self, query):
        """Search Hugging Face Spaces"""
        url = "https://huggingface.co/api/spaces"
        params = {"search": query}
        response = requests.get(url, params=params, headers=self.hf_headers)
        return response.json()
    
    def run_space(self, space_id, inputs):
        """Run a Hugging Face Space"""
        url = f"https://huggingface.co/spaces/{space_id}/api/predict"
        response = requests.post(url, json={"data": inputs}, headers=self.hf_headers)
        return response.json()
```

---

## 🎮 **Phase 6: Complete TEC Integration**

### Step 1: Enhanced AI NPC Service
```python
# File: services/enhanced_npc_service.py
from tec_tools.rag_service import TECRAGService
from tec_tools.enhanced_mcp_service import EnhancedMCPService

class EnhancedNPCService:
    def __init__(self):
        self.rag = TECRAGService()
        self.mcp = EnhancedMCPService()
        self.ollama_url = "http://localhost:11434"
    
    def generate_contextual_dialogue(self, npc, player_input, use_rag=True):
        """Generate NPC dialogue with RAG context"""
        
        # Get relevant context from RAG
        if use_rag:
            context_docs = self.rag.query(f"NPC {npc.name} {player_input}")
            context = "\n".join(context_docs)
        else:
            context = ""
        
        # Build prompt with context
        prompt = f"""
        Context: {context}
        
        You are {npc.name}, a {npc.character_class} in the TEC: BITLYFE RPG.
        Personality: {npc.personality}
        Location: {npc.location}
        
        Player says: "{player_input}"
        
        Respond in character (2-3 sentences):
        """
        
        # Generate with Ollama
        response = self._call_ollama(prompt)
        return response
    
    def _call_ollama(self, prompt, model="llama3.2:3b"):
        """Call local Ollama model"""
        import requests
        
        response = requests.post(f"{self.ollama_url}/api/generate", 
            json={
                "model": model,
                "prompt": prompt,
                "stream": False
            })
        
        if response.status_code == 200:
            return response.json()["response"]
        else:
            return "I seem to be at a loss for words..."
```

---

## 📋 **Quick Start Commands (After Restart)**

```bash
# 1. Check everything is working
ollama --version
docker --version

# 2. Start Ollama model
ollama pull llama3.2:3b
ollama run llama3.2:3b "Hello!"

# 3. Start TEC system
cd C:\Users\Ghedd\TEC_CODE\tecdeskgoddess
python tec_enhanced_api.py

# 4. Test endpoints
curl http://localhost:5000/health
curl http://localhost:5000/api/game/npc/create -X POST -H "Content-Type: application/json" -d '{"name":"Thorin","character_class":"Blacksmith"}'

# 5. (Optional) Start Docker stack
docker-compose up -d
```

---

## 🎯 **Benefits of This Complete Setup**

### **Local AI (Ollama)**
- ✅ Fast, private, no API costs
- ✅ Works offline
- ✅ Perfect for NPCs and dialogue

### **RAG System**
- ✅ AI knows your specific game world
- ✅ Consistent character backgrounds
- ✅ Up-to-date game rules and lore

### **Docker Integration**
- ✅ Run larger models
- ✅ Easy deployment
- ✅ Scalable architecture

### **MCP + Hugging Face**
- ✅ Access to 500k+ models
- ✅ 25 minutes daily ZeroGPU compute
- ✅ Latest AI capabilities

### **Image Generation**
- ✅ Generate character portraits
- ✅ Create item illustrations  
- ✅ Generate world artwork

---

## 🔄 **Recommended Implementation Order**

1. **Start with Ollama** (Phase 1) - Get basic AI working
2. **Add RAG** (Phase 3) - Make AI know your game world  
3. **Test integration** with TEC Clean Architecture
4. **Add Docker** (Phase 4) - Scale up capabilities
5. **Configure MCP** (Phase 5) - Access Hugging Face ecosystem
6. **Add images** (Phase 2) - Visual enhancements

This gives you a complete AI-powered RPG system with both local privacy and cloud capabilities!
