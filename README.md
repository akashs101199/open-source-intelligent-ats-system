# Intelligent Multi-Agent ATS System for Agentic AI Roles

A sophisticated, Applicant Tracking System that uses multiple AI agents to deeply understand candidate qualifications beyond keywords, specifically designed for evaluating Agentic AI engineering roles.

<img width="1615" height="952" alt="Screenshot 2025-11-22 at 09 32 26" src="https://github.com/user-attachments/assets/74d7f5bd-5bc0-4ccb-9013-b1c72fda91d9" />
<img width="1613" height="934" alt="Screenshot 2025-11-22 at 09 32 45" src="https://github.com/user-attachments/assets/68f3eb8a-bbab-4d32-927c-48184dc4ad0a" />
<img width="1629" height="952" alt="Screenshot 2025-11-22 at 09 33 05" src="https://github.com/user-attachments/assets/7b3be49d-760c-4844-a0d8-be51d5674554" />


## 🌟 Features

### Multi-Agent Architecture
- **Parser Agent**: Extracts structured information from resumes (PDF/DOCX/TXT)
- **Semantic Analyzer Agent**: Deep semantic understanding via embeddings + LLM reasoning
- **Technical Evaluator Agent**: Assesses technical depth in 6 key areas for Agentic AI
- **Experience Synthesizer Agent**: Evaluates work quality and impact over duration
- **Orchestrator Agent**: Coordinates all agents and produces comprehensive scoring

### Key Capabilities
- **Context-Aware Evaluation**: Understands actual work accomplished, not just buzzwords
- **Semantic Matching**: Embeddings-based similarity search using sentence-transformers
- **Production-Grade**: FastAPI backend, proper error handling, health checks, logging
- **Scalable**: Vector database (Qdrant) for fast candidate retrieval
- **Specialized**: Tailored for Agentic AI roles (LangChain, multi-agent, tool use, etc.)
- **Detailed Insights**: Provides strengths, gaps, and reasoning for each candidate

### Scoring Methodology
Weighted composite score prioritizing:
1. **Agentic Capabilities (35%)**: Evidence of building autonomous agent systems
2. **Technical Depth (30%)**: Expertise in LLMs, frameworks, vector DBs, etc.
3. **Semantic Match (20%)**: Relevance of experience to job requirements
4. **Experience Quality (15%)**: Impact and complexity of work done

## 📋 Prerequisites

- Docker & Docker Compose
- 16GB+ RAM (for running LLM locally)
- 20GB+ disk space
- GPU recommended but not required (CPU mode works with llama3.1:8b)

## 🚀 Quick Start

### 1. Clone and Setup
```bash
# Create project directory
mkdir intelligent-ats && cd intelligent-ats

# Copy all the modularized code into the structure shown above
# Or clone from your repository

# Make setup script executable
chmod +x setup.sh
```

### 2. Run Setup Script
```bash
./setup.sh
```

This will:
- Check Docker installation
- Create necessary directories
- Start all services (Qdrant, Ollama, Backend)
- Pull the Llama 3.1 8B model
- Verify services are healthy

### 3. Verify Installation
```bash
# Check service health
curl http://localhost:8000/health

# View API documentation
open http://localhost:8000/docs
```

## 📚 Usage

### Using the API

**1. Create a Job Description**
```bash
curl -X POST "http://localhost:8000/api/jobs" \
  -H "Content-Type: application/json" \
  -d '{
    "title": "Senior Agentic AI Engineer",
    "description": "Build autonomous AI agent systems...",
    "responsibilities": [
      "Design and implement multi-agent architectures",
      "Develop tool-use capabilities for agents",
      "Build planning and reasoning systems"
    ],
    "required_skills": [
      "LangChain", "LLMs", "Python", "Multi-agent systems"
    ],
    "preferred_skills": [
      "CrewAI", "AutoGPT", "Vector databases"
    ],
    "experience_level": "senior"
  }'
```

**2. Upload Resumes**
```bash
curl -X POST "http://localhost:8000/api/candidates/upload" \
  -F "file=@resume.pdf" \
  -F "candidate_name=John Doe"
```

**3. Match Candidates**
```bash
curl -X POST "http://localhost:8000/api/match" \
  -H "Content-Type: application/json" \
  -d '{
    "job_id": "job_1_1234567890",
    "top_k": 10,
    "min_score": 0.3
  }'
```

**4. Get Detailed Scores**
```bash
curl "http://localhost:8000/api/match/job_1/candidate_1"
```

### Understanding the Results

Each candidate receives:
- **Overall Score**: 0-1, weighted composite
- **Breakdown Scores**: Agentic, Technical, Semantic, Experience
- **Strengths**: Key positive findings
- **Gaps**: Areas of concern or missing experience
- **Reasoning**: AI-generated explanation of the score

Example output:
```json
{
  "candidate_id": "candidate_1",
  "overall_score": 0.756,
  "agentic_capabilities": 0.82,
  "technical_depth": 0.75,
  "semantic_match": 0.68,
  "experience_quality": 0.71,
  "strengths": [
    "Strong agentic AI experience: Built production chatbot using LangChain with tool use",
    "Strong technical expertise: Agent Frameworks, Tool Use, Planning Reasoning"
  ],
  "gaps": [
    "Limited experience in: Vector Dbs, Orchestration"
  ],
  "reasoning": "This candidate demonstrates strong agentic AI capabilities with concrete evidence of building autonomous systems. Technical depth is solid across most key areas, particularly in agent frameworks and tool integration. The semantic match shows highly relevant experience for this role. Recommend for interview based on strong agent-building background and production experience."
}
```

## ⚙️ Configuration

### Adjusting Scoring Weights

Edit `backend/.env`:
```env
# Default weights (must sum to 1.0)
WEIGHT_AGENTIC=0.35
WEIGHT_TECHNICAL=0.30
WEIGHT_SEMANTIC=0.20
WEIGHT_EXPERIENCE=0.15
```

### Using Different LLM Models
```bash
# For better quality (requires more RAM):
docker exec intelligent-ats-ollama ollama pull llama3.1:70b

# Update .env:
OLLAMA_MODEL=llama3.1:70b
```

### Customizing Technical Areas

Edit `backend/app/agents/technical_evaluator_agent.py`:
```python
self.key_areas = {
    "llm_expertise": ["llm", "gpt", ...],
    "agent_frameworks": ["langchain", ...],
    # Add your custom areas
}
```

## 🏗️ Architecture
```
┌─────────────┐
│   Frontend  │  (React/CLI)
└──────┬──────┘
       │ HTTP
┌──────▼──────────────────────────┐
│      FastAPI Backend            │
├─────────────────────────────────┤
│  ┌─────────────────────────┐   │
│  │  Orchestrator Agent     │   │
│  └────────┬────────────────┘   │
│           │                     │
│  ┌────────▼────────┐           │
│  │  Parser Agent   │           │
│  │  ┌───────────┐  │           │
│  │  │  LLM      │  │           │
│  │  └───────────┘  │           │
│  └─────────────────┘           │
│           │                     │
│  ┌────────▼─────────────────┐  │
│  │  Parallel Execution      │  │
│  ├──────────────────────────┤  │
│  │ • Semantic Analyzer      │  │
│  │ • Technical Evaluator    │  │
│  │ • Experience Synthesizer │  │
│  └──────────────────────────┘  │
│           │                     │
│  ┌────────▼────────────────┐   │
│  │  Scoring & Reasoning    │   │
│  └─────────────────────────┘   │
└────────┬────────┬───────────────┘
         │        │
    ┌────▼───┐  ┌▼──────┐
    │ Qdrant │  │Ollama │
    │Vector  │  │  LLM  │
    │   DB   │  │       │
    └────────┘  └───────┘
```

## 🧪 Testing

### Test Individual Agents
```python
# Test parser
from app.agents.parser_agent import ParserAgent

parser = ParserAgent()
with open("resume.pdf", "rb") as f:
    result = await parser.process(f.read(), "resume.pdf")
print(result)
```

### Run Health Checks
```bash
# Check all services
curl http://localhost:8000/health | jq

# Check Qdrant
curl http://localhost:6333/health

# Check Ollama
curl http://localhost:11434/api/tags
```

## 📊 Performance

**Typical Processing Times** (llama3.1:8b on CPU):
- Resume parsing: 5-10s
- Semantic analysis: 3-5s
- Technical evaluation: 5-8s
- Experience synthesis: 5-8s
- **Total per candidate**: ~20-30s

**With GPU** (llama3.1:70b):
- **Total per candidate**: ~10-15s with better quality

## 🔧 Troubleshooting

### Services Won't Start
```bash
# Check logs
docker-compose logs -f

# Restart services
docker-compose down
docker-compose up -d
```

### Ollama Model Not Found
```bash
# Pull model manually
docker exec intelligent-ats-ollama ollama pull llama3.1:8b

# List available models
docker exec intelligent-ats-ollama ollama list
```

### Slow Processing
```bash
# Use smaller model
OLLAMA_MODEL=llama3.1:8b

# Reduce candidates per match
MAX_CANDIDATES_PER_MATCH=10
```

### Out of Memory
```bash
# Increase Docker memory limit
# Docker Desktop -> Settings -> Resources -> Memory

# Or use smaller model
ollama pull phi-3:mini
```

## 🚀 Production Deployment

### Replace In-Memory Database
```python
# Replace backend/app/models/database.py with PostgreSQL/MongoDB
# Example with PostgreSQL:

from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker

DATABASE_URL = "postgresql://user:pass@localhost/atsdb"
engine = create_engine(DATABASE_URL)
SessionLocal = sessionmaker(bind=engine)
```

### Add Authentication
```python
# Add to backend/app/main.py

from fastapi.security import HTTPBearer
security = HTTPBearer()

@app.middleware("http")
async def authenticate(request: Request, call_next):
    # Add your auth logic
    pass
```

### Scale with Kubernetes
```yaml
# kubernetes/deployment.yaml
apiVersion: apps/v1
kind: Deployment
metadata:
  name: ats-backend
spec:
  replicas: 3
  selector:
    matchLabels:
      app: ats-backend
  template:
    # ... pod spec
```

## 📈 Future Enhancements

- [ ] Add resume anonymization for bias reduction
- [ ] Implement candidate interview scheduling
- [ ] Add email notifications for matches
- [ ] Build collaborative filtering for better recommendations
- [ ] Add support for video resume analysis
- [ ] Implement A/B testing for scoring algorithms
- [ ] Add explainable AI visualizations
- [ ] Multi-language support

## 📝 License

MIT License - Feel free to use and modify

## 🤝 Contributing

Contributions welcome! Please:
1. Fork the repository
2. Create a feature branch
3. Submit a pull request

## 📧 Support

For issues or questions, please create a GitHub issue or contact the maintainers.

---

**Built with ❤️ for better AI hiring**
