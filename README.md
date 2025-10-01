# AI Mind Explorer 

**Visualizing AI Reasoning Processes Through Interactive Knowledge Graphs**

Hi there! I wanted to develop a full-stack application that externalizes and visualizes how Large Language Models (LLMs) think, making AI reasoning transparent, explorable, and editable. I didn't really like that I couldn't see how LLMs make connections between  reasoning chains (e.g. only listing out the steps of how they're thinking without really showing how their thinking can be more interconnected).

![Tech Stack](https://img.shields.io/badge/Python-FastAPI-009688?style=flat-square)
![Tech Stack](https://img.shields.io/badge/React-TypeScript-61DAFB?style=flat-square)
![Tech Stack](https://img.shields.io/badge/Neo4j-Graph%20DB-008CC1?style=flat-square)
![Tech Stack](https://img.shields.io/badge/D3.js-Visualization-F9A03C?style=flat-square)

---

## Project Significance

As AI systems become increasingly integrated into critical decision-making processes, understanding *how* they reach conclusions is essential. This was inspired by my intern project with the DoD this summer, and realizing how important it is to have LLM outputs that we can trust and expose. Traditional LLM interfaces generally show only the final output, hiding the reasoning chain that produced it. Even if there are reasoning chains (like Perplexity), they're not clear about how each idea/piece of information is connected to other pieces of information. I believe that as humans, our best ideas come from being able to make connections across many different ideas instead of just disparately using  random information.

**AI Mind Explorer** addresses this transparency gap by:

- **Externalizing AI thought processes** into structured, visual reasoning chains
- **Making black-box decisions interpretable** through graph-based visualization
- **Enabling reasoning exploration** so users can understand AI logic step-by-step
- **Building toward AI accountability** by preserving and analyzing reasoning patterns

This project demonstrates proficiency in:
- Full-stack development with modern frameworks
- Graph database design and implementation
- LLM integration and prompt engineering
- Interactive data visualization
- RESTful API design
- Dockerized microservices architecture

---

##  Current Features

### Core Functionality
- **LLM Reasoning Extraction**: Gemini model externalizes its thought process and internal mapping/problem solving approach to your question as structured JSON
- **Graph Visualization**: Interactive D3.js force-directed graph showing reasoning flow
- **Neo4j Persistence**: Stores reasoning chains as nodes (thoughts) and edges (logical connections)
- **Real-time Processing**: FastAPI backend processes prompts and returns structured reasoning chains
- **Interactive Exploration**:
  - Click nodes to view detailed reasoning content
  - Drag nodes to rearrange the graph
  - Zoom and pan to explore complex reasoning chains
- **Thought Classification**: Categorizes reasoning steps into question, retrieval, reasoning, and conclusion types
- **Confidence Metrics**: Displays AI confidence levels for each reasoning step

### Technical Features
- Multi-provider LLM support (OpenAI, Google Gemini)
- Type-safe TypeScript frontend
- Pydantic data validation
- CORS-enabled API
- Environment-based configuration
- Dockerized Neo4j database

---

## Planned Enhancements

### Phase 1: Core Improvements
- [ ] Session retrieval and history browsing
- [ ] Enhanced graph layouts (hierarchical, radial, custom)
- [ ] Export reasoning chains (JSON, PDF, PNG)
- [ ] Advanced filtering and search

### Phase 2: Interactive Editing
- [ ] **Edit reasoning nodes** and observe how changes propagate
- [ ] Branch alternate reasoning paths
- [ ] Compare different AI models' reasoning for the same question
- [ ] Manual reasoning chain construction

### Phase 3: Analytics & Insights
- [ ] Reasoning pattern detection across sessions
- [ ] Confidence correlation analysis
- [ ] Reasoning chain complexity metrics
- [ ] Common reasoning path identification

### Phase 4: Collaboration & Deployment
- [ ] Multi-user support with authentication
- [ ] Shared reasoning sessions
- [ ] Public reasoning chain gallery
- [ ] Production deployment with CI/CD

---

## Tech Stack

### Backend
- **FastAPI** - Modern Python web framework for APIs
- **Neo4j** - Graph database for storing reasoning chains
- **Python 3.9+** - Core language
- **Pydantic** - Data validation and settings management
- **Google Generative AI** - LLM integration (Gemini)
- **Uvicorn** - ASGI server

### Frontend
- **React 18** - UI framework
- **TypeScript** - Type-safe development
- **D3.js** - Interactive graph visualization
- **React Router** - Navigation
- **CSS3** - Styling

### Infrastructure
- **Docker** - Containerization
- **Neo4j 5.15** - Graph database container
- **Git** - Version control

---

## Project Structure

```
ai-mind-explorer/
├── backend/                    # FastAPI backend
│   ├── app/
│   │   ├── api/               # API endpoints
│   │   │   └── reasoning.py   # Reasoning chain processing
│   │   ├── core/              # Core configuration
│   │   │   ├── config.py      # Settings management
│   │   │   └── database.py    # Neo4j connection
│   │   ├── models/            # Pydantic models
│   │   │   └── thought_models.py
│   │   └── services/          
│   │       ├── llm_service.py      # LLM integration
│   │       └── graph_service.py    # Neo4j operations
│   ├── main.py                # FastAPI app entry point
│   ├── requirements.txt       # Python dependencies
│   └── .env                   # Environment variables
│
├── frontend/                  # React frontend
│   ├── src/
│   │   ├── components/
│   │   │   ├── ThoughtGraph/       # D3.js graph visualization
│   │   │   ├── PromptInput/        # User input interface
│   │   │   └── NodeDetails/        # Node detail viewer
│   │   ├── types/
│   │   │   └── reasoning.ts        # TypeScript interfaces
│   │   ├── App.tsx            # Main app component
│   │   └── index.tsx          # Entry point
│   └── package.json           # Node dependencies
│
└── docker/                    # Docker configurations
    └── docker-compose-test.yml
```

---

##  Getting Started

### Prerequisites
- **Python 3.9+**
- **Node.js 16+**
- **Docker Desktop**
- **Gemini API Key** ([Get one here](https://ai.google.dev/))

### Installation

#### 1. Clone the Repository
```bash
git clone https://github.com/yourusername/ai-mind-explorer.git
cd ai-mind-explorer
```

#### 2. Set Up Backend

```bash
cd backend

# Create virtual environment
python -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate

# Install dependencies
pip install -r requirements.txt

# Configure environment variables
cp .env.example .env
# Edit .env and add your API keys:
#   GEMINI_API_KEY=your-key-here
#   NEO4J_URI=bolt://localhost:7687
#   NEO4J_USER=neo4j
#   NEO4J_PASSWORD=testpassword
```

#### 3. Start Neo4j Database

```bash
# Start Docker Desktop, then:
docker run -d \
  --name neo4j-ai-mind-explorer \
  -p 7474:7474 \
  -p 7687:7687 \
  -e NEO4J_AUTH=neo4j/testpassword \
  neo4j:5.15
```

#### 4. Start Backend Server

```bash
# From backend directory with venv activated
python -m uvicorn main:app --reload

# API will be available at http://localhost:8000
# API docs at http://localhost:8000/docs
```

#### 5. Set Up Frontend

```bash
cd ../frontend

# Install dependencies
npm install

# Start development server
npm start

# App will open at http://localhost:3000
```

### Quick Test

1. Open http://localhost:3000
2. Enter a question like: "Why is the sky blue?"
3. Click "Process Prompt"
4. Explore the generated reasoning graph!
5. View Neo4j database at http://localhost:7474 (login: neo4j/testpassword)

---

##  Usage

### Processing a Prompt

1. **Enter your question** in the input field
2. **Click "Process Prompt"** - the LLM will generate a reasoning chain
3. **Explore the graph**:
   - **Blue nodes** = Understanding the question
   - **Green nodes** = Information retrieval
   - **Orange nodes** = Logical reasoning
   - **Red nodes** = Conclusions
4. **Click any node** to see detailed reasoning content
5. **Drag nodes** to rearrange the visualization
6. **Zoom/pan** to navigate complex graphs

### API Endpoints

- `GET /health` - Health check
- `POST /api/reasoning/process` - Process a prompt and generate reasoning chain
- `GET /api/reasoning/session/{session_id}` - Retrieve saved session (planned)

---

##  Development (TBD)

### Running Tests
```bash
# Backend tests (coming soon)
cd backend
pytest

# Frontend tests (coming soon)
cd frontend
npm test
```

### Database Management

```bash
# Access Neo4j browser
open http://localhost:7474

# Example Cypher queries:
# View all reasoning sessions
MATCH (s:Session) RETURN s

# View thoughts for a session
MATCH (s:Session)-[:HAS_THOUGHT]->(t:ThoughtNode)
WHERE s.session_id = 'your-session-id'
RETURN t

# View reasoning flow
MATCH (t1:ThoughtNode)-[r:LEADS_TO]->(t2:ThoughtNode)
RETURN t1, r, t2
```

---

##  Contributing

This is a personal portfolio project, but feedback and suggestions are welcome! Feel free to:
- Open issues for bugs or feature requests
- Fork the project and experiment
- Share your thoughts on reasoning visualization approaches

---

##  License

MIT License 

---

## 👤 Author

**Erika Lee**

---

## 🙏 Acknowledgments

- Inspired by research in explainable AI and knowledge graphs! I'll definitely be adding more depth to this project as I get more into research on AI explainability, alignment, and interpretability.

**⭐ If you find this project interesting, please consider starring it!**
