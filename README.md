A production-ready, multi-agent AI system that analyzes outfit images and provides personalized fashion recommendations using Google Gemini models and LangGraph orchestration.

## 🚀 Quick Start (Local Development)

### Prerequisites

- **Python 3.12+** with UV package manager
- **Node.js 20+** with npm
- **Google Gemini API Key** ([Get one here](https://makersuite.google.com/app/apikey))

### 1. Clone and Setup

```bash
git clone <repository-url>
cd outfit-recommender

# Copy environment template
cp .env.example .env

# Add your API key
echo "GOOGLE_API_KEY=your_gemini_api_key_here" >> .env
```

### 2. Backend Setup

```bash
cd backend

# Install UV (if not installed)
curl -LsSf https://astral.sh/uv/install.sh | sh

# Install dependencies
uv sync --dev

# Run linting and formatting (optional)
uv run ruff check . --fix
uv run ruff format .

# Start backend server
uv run flask --app app.main run --debug --host 0.0.0.0 --port 5000
```

**Backend will run on**: http://localhost:5000

### 3. Frontend Setup (New Terminal)

```bash
cd frontend

# Install dependencies
npm install

# Generate Prisma client
npx prisma generate

# Start development server
npm run dev
```

**Frontend will run on**: http://localhost:3000

### 4. Test the Application

1. Open http://localhost:3000 in your browser
2. Upload an outfit image (try `outfit_shorts.jpg` from project root)
3. Enter a query like "What should I wear for a wedding?"
4. Choose **Quick Analyze** or **Deep Analyze**
5. View AI-powered recommendations!

### 🐳 Alternative: Run with Containers

If you prefer containers (requires Podman/Docker):

```bash
# Make script executable
chmod +x run-podman.sh

# Start all services
./run-podman.sh start

# Access at http://localhost:3000
```

---

## 📋 Table of Contents

- [System Overview](#-system-overview)
- [Architecture](#-architecture)
- [Agent Workflow](#-agent-workflow)
- [Local Development](#-local-development)
- [Container Deployment](#-container-deployment)
- [API Documentation](#-api-documentation)
- [Project Structure](#-project-structure)
- [Technology Stack](#-technology-stack)
- [Testing](#-testing)

---

## 🎯 System Overview

**Project Aura** is a sophisticated fashion recommendation system that combines:
- **Multi-agent AI orchestration** using LangGraph
- **Advanced vision analysis** with Gemini 2.5 Pro/Flash
- **Context-aware trend generation** using DSPy
- **Luxury user interface** with Next.js 16 and React 19

### Key Features

✅ **Dual Analysis Modes**
- **Quick Analyze**: Fast insights using Gemini 2.5 Flash
- **Deep Analyze**: Comprehensive analysis using Gemini 2.5 Pro

✅ **Multi-Agent Workflow**
- Vision Agent → Trend Agent → Advisor Agent → Generator Agent

✅ **Real-time Processing**
- Animated agent workflow visualization
- Live status updates during analysis

✅ **Production Ready**
- Containerized with Podman/Docker
- Health checks and monitoring
- Comprehensive error handling

---

## 🏗️ Architecture


### System Architecture Diagram

<img width="1093" height="1355" alt="image" src="https://github.com/user-attachments/assets/3b251991-8a03-45c9-af7e-61708441221c" />



```
┌─────────────────────────────────────────────────────────────────┐
│                         USER INTERFACE                          │
│                     (Next.js 16 + React 19)                     │
│  ┌────────────┐  ┌──────────────┐  ┌────────────────────────┐  │
│  │   Upload   │  │  Processing  │  │   Results Dashboard    │  │
│  │    View    │→ │   Overlay    │→ │  (Side-by-side view)   │  │
│  └────────────┘  └──────────────┘  └────────────────────────┘  │
└─────────────────────────────┬───────────────────────────────────┘
                              │
                              │ HTTP POST /api/analyze
                              │ (multipart/form-data)
                              ↓
┌─────────────────────────────────────────────────────────────────┐
│                      FLASK BACKEND API                          │
│                       (Python 3.12)                             │
│  ┌───────────────────────────────────────────────────────────┐  │
│  │              LangGraph State Machine                      │  │
│  │                                                           │  │
│  │  ┌──────────┐   ┌──────────┐   ┌──────────┐   ┌───────┐ │  │
│  │  │  Vision  │ → │  Trends  │ → │ Advisor  │ → │ Image │ │  │
│  │  │  Agent   │   │  Agent   │   │  Agent   │   │ Agent │ │  │
│  │  └──────────┘   └──────────┘   └──────────┘   └───────┘ │  │
│  │       ↓              ↓              ↓             ↓       │  │
│  │   Gemini 2.5     DSPy CoT      DSPy CoT      Gemini 2.5  │  │
│  │   Pro/Flash       Prompt       Prompt          Flash     │  │
│  └───────────────────────────────────────────────────────────┘  │
└─────────────────────────────┬───────────────────────────────────┘
                              │
                              │ API Calls
                              ↓
┌─────────────────────────────────────────────────────────────────┐
│                    GOOGLE GEMINI API                            │
│  ┌────────────────┐  ┌────────────────┐  ┌──────────────────┐  │
│  │ Gemini 2.5 Pro │  │Gemini 2.5 Flash│  │Gemini Flash Image│  │
│  │  (Deep mode)   │  │  (Quick mode)  │  │  (Generation)    │  │
│  └────────────────┘  └────────────────┘  └──────────────────┘  │
└─────────────────────────────────────────────────────────────────┘
```

### Component Breakdown

| Component | Technology | Purpose |
|-----------|-----------|---------|
| **Frontend** | Next.js 16, React 19, TypeScript, Tailwind CSS 4 | Luxury UI with three-view architecture |
| **Backend** | Flask, Python 3.12, LangGraph | Multi-agent orchestration and API |
| **Agent Framework** | LangGraph + DSPy | Sequential workflow with structured prompts |
| **AI Models** | Gemini 2.5 Pro/Flash | Vision analysis and text generation |
| **Deployment** | Podman/Docker Compose | Containerized production deployment |

---

## 🤖 Agent Workflow

### Sequential Multi-Agent Pipeline

```
┌─────────────────────────────────────────────────────────────────────┐
│                        AGENT WORKFLOW                               │
└─────────────────────────────────────────────────────────────────────┘

   Upload Image + Query
          ↓
┌──────────────────────┐
│   1. VISION AGENT    │  ← Gemini 2.5 Pro (Deep) / 2.5 Flash (Quick)
│  analyze_image()     │
└──────────────────────┘
          ↓
    Visual Features:
    - Gender Style
    - Cut & Silhouette
    - Color Palette
    - Textile & Texture
    - Occasion
          ↓
┌──────────────────────┐
│   2. TRENDS AGENT    │  ← DSPy Chain-of-Thought
│  fetch_trends()      │
└──────────────────────┘
          ↓
    Trend Summary:
    - Relaxed Tailoring
    - Textural Play
    - Muted Color Palettes
    - Elevated Separates
          ↓
┌──────────────────────┐
│   3. ADVISOR AGENT   │  ← DSPy Chain-of-Thought
│  synthesize_advice() │
└──────────────────────┘
          ↓
    Styling Advice:
    - Personalized recommendations
    - Occasion-specific tips
    - Color theory application
    - Accessory suggestions
          ↓
┌──────────────────────┐
│   4. GENERATOR AGENT │  ← Gemini 2.5 Flash Image
│  generate_outfit()   │
└──────────────────────┘
          ↓
    Generated Image URL
          ↓
    Return JSON Response
```

### Agent Details

#### 1️⃣ **Vision Agent** (`multi_model.py`)
- **Model**: `gemini-2.5-flash` (Quick) or `gemini-2.5-pro` (Deep)
- **Input**: Raw image bytes + analysis mode
- **Process**: Multimodal vision analysis using DSPy signature
- **Output**: Structured JSON with visual features

#### 2️⃣ **Trends Agent** (`trending.py`)
- **Framework**: DSPy Chain-of-Thought
- **Input**: User query context (gender, occasion, style preferences)
- **Process**: Generate context-aware fashion trends
- **Output**: Markdown-formatted trend summary

#### 3️⃣ **Advisor Agent** (`analysis.py`)
- **Framework**: DSPy Chain-of-Thought
- **Input**: Visual analysis + trend summary + user query
- **Process**: Synthesize personalized styling advice
- **Output**: Comprehensive recommendation paragraph

#### 4️⃣ **Generator Agent** (`multi_model.py`)
- **Model**: `gemini-2.5-flash-image`
- **Input**: Styling advice + visual features + original image
- **Process**: Generate outfit visualization
- **Output**: Image URL (currently may return placeholder)
- **Note**: Limited by API capabilities; may require Vertex AI Imagen

## 💻 Local Development

### Backend Development

```bash
cd backend

# Install dependencies
uv sync --dev

# Code quality (automatically applied)
uv run ruff check . --fix    # Lint and auto-fix
uv run ruff format .         # Format code

# Run development server
uv run flask --app app.main run --debug --host 0.0.0.0 --port 5000

# Alternative: Run with Python directly
uv run python run.py
```

### Frontend Development

```bash
cd frontend

# Install dependencies
npm install

# Development commands
npm run dev          # Start dev server
npm run build        # Build for production
npm run lint         # Run ESLint
npx tsc --noEmit    # Type check

# Database (SQLite for development)
npx prisma generate
npx prisma studio    # Open database GUI
```

### Development Workflow

```bash
# 1. Start backend (terminal 1)
cd backend && uv run flask --app app.main run --debug

# 2. Start frontend (terminal 2)
cd frontend && npm run dev

# 3. Code changes auto-reload
# 4. Test at http://localhost:3000
```

### Code Quality

The backend uses **Ruff** for linting and formatting:

```bash
cd backend
uv run ruff check . --fix    # Fix linting issues
uv run ruff format .         # Format code
```

**Standards enforced:**
- PEP 8 style guide
- Import sorting (isort)
- Common bug detection (flake8-bugbear)
- Code complexity checks

---

## 🐳 Container Deployment

### Using Podman (Recommended)

```bash
# Quick start
./run-podman.sh start

# View logs
./run-podman.sh logs

# Stop services
./run-podman.sh stop
```

### Manual Container Commands

```bash
# Build containers
podman build -t outfit-backend -f backend/Containerfile backend/
podman build -t outfit-frontend -f frontend/Containerfile frontend/

# Create network
podman network create outfit-network

# Run backend
podman run -d --name outfit-backend --network outfit-network \
  -p 5000:5000 -e GOOGLE_API_KEY=your_key outfit-backend

# Run frontend
podman run -d --name outfit-frontend --network outfit-network \
  -p 3000:3000 -e NEXT_PUBLIC_API_URL=http://localhost:5000/api \
  -e BACKEND_INTERNAL_URL=http://outfit-backend:5000/api outfit-frontend
```

### Health Checks

```bash
# Backend health
curl http://localhost:5000/api/health

# Container status
podman ps
```

---

## 📡 API Documentation

### Base URL

```
http://localhost:5000/api
```

### Endpoints

#### `GET /health`

Health check endpoint.

**Response:**
```json
{
  "status": "healthy"
}
```

**cURL Test:**
```bash
curl http://localhost:5000/api/health
```

---

#### `POST /analyze`

Analyze outfit image and receive AI recommendations.

**Request:**
- **Content-Type**: `multipart/form-data`
- **Max File Size**: 10MB
- **Supported Formats**: PNG, JPG, JPEG, GIF, WEBP

**Form Fields:**

| Field | Type | Required | Description |
|-------|------|----------|-------------|
| `image` | File | Yes | Outfit image to analyze |
| `query` | String | No | User context/question (default: "What should I wear for a wedding?") |
| `mode` | String | No | Analysis mode: `quick` or `deep` (default: `deep`) |

**Response:**
```json
{
  "visual_analysis": {
    "gender_style": "masculine",
    "cut": "Regular-fit crew-neck sweater over slim-fit trousers",
    "color": "Black sweater with white t-shirt, charcoal trousers",
    "fabric": "Cotton knit sweater, cotton jersey t-shirt, cotton twill trousers",
    "occasion": "Smart casual, urban wear, creative work environments"
  },
  "trend_summary": "**Relaxed Tailoring:** Modern suits with softer construction...",
  "final_report": "Your smart casual ensemble balances comfort with sophistication...",
  "generated_image_url": "https://storage.googleapis.com/...",
  "analysis_mode": "deep",
  "generation_prompt": "Fashion illustration of...",
  "image_generation_error": null
}
```

**cURL Test:**
```bash
# Quick analyze mode
curl -X POST http://localhost:5000/api/analyze \
  -F "image=@/path/to/outfit.jpg" \
  -F "query=What should I wear for a wedding?" \
  -F "mode=quick"

# Deep analyze mode with full workflow
curl -X POST http://localhost:5000/api/analyze \
  -F "image=@/path/to/outfit.jpg" \
  -F "query=What colors would complement this outfit?" \
  -F "mode=deep"
```

**Error Responses:**

```json
// 400 Bad Request - No image provided
{
  "error": "No image file provided"
}

// 400 Bad Request - Invalid file type
{
  "error": "Invalid file type. Allowed: png, jpg, jpeg, gif, webp"
}

// 500 Internal Server Error
{
  "error": "Analysis failed",
  "details": "Error message details"
}
```

---

## 💻 Local Development

### Backend Setup

```bash
cd backend

# Install UV package manager (if not installed)
curl -LsSf https://astral.sh/uv/install.sh | sh

# Install dependencies
uv sync --dev

# Run development server
uv run flask --app app.main run --debug

# Run with auto-reload
uv run python app/main.py
```

**Backend runs on**: http://localhost:5000

### Frontend Setup

```bash
cd frontend

# Install dependencies
npm install

# Install lucide-react icons (if not already)
npm install lucide-react@^0.469.0 react-markdown@9.0.3

# Generate Prisma client
npx prisma generate

# Run migrations (optional, uses SQLite)
DATABASE_URL="file:./dev.db" npx prisma migrate dev --name init

# Start development server
npm run dev
```

**Frontend runs on**: http://localhost:3000

### Development Commands

```bash
# Backend linting and formatting
cd backend
uv run ruff check .           # Check for issues
uv run ruff check . --fix     # Auto-fix issues
uv run ruff format .          # Format code

# Frontend linting and type checking
cd frontend
npm run lint                  # ESLint check
npx tsc --noEmit             # Type check
npm run build                # Build for production

# Database management (Prisma)
npx prisma studio            # Open database GUI
npx prisma migrate reset     # Reset database
```

---

## 📂 Project Structure

```
outfit-recommender/
├── backend/
│   ├── app/
│   │   ├── agents/                 # Multi-agent system
│   │   │   ├── config.py           # LM configuration per mode
│   │   │   ├── state.py            # AgentState TypedDict
│   │   │   ├── supervisor.py       # LangGraph orchestration
│   │   │   ├── multi_model.py      # Vision + Generation
│   │   │   ├── analysis.py         # Styling advice synthesis
│   │   │   └── trending.py         # Trend generation
│   │   ├── routers/
│   │   │   ├── analyze.py          # POST /analyze endpoint
│   │   │   └── healthcheck.py      # GET /health endpoint
│   │   ├── utils/
│   │   │   └── logs.py             # Agent logging utilities
│   │   └── main.py                 # Flask app entry point
│   ├── pyproject.toml              # UV dependencies
│   ├── uv.lock                     # Lock file
│   ├── requirements.txt            # Pip fallback
│   └── Containerfile               # Backend container
│
├── frontend/
│   ├── src/
│   │   ├── app/
│   │   │   ├── page.tsx            # Main UI component
│   │   │   ├── layout.tsx          # Root layout
│   │   │   ├── actions.ts          # Server actions
│   │   │   └── globals.css         # Tailwind styles
│   │   └── components/             # React components (legacy)
│   ├── prisma/
│   │   └── schema.prisma           # Database schema
│   ├── public/                     # Static assets
│   ├── package.json
│   ├── next.config.ts              # Next.js config
│   ├── tsconfig.json               # TypeScript config
│   └── Containerfile               # Frontend container
│
├── compose.yaml                    # Podman/Docker compose
├── .env.example                    # Environment template
├── .gitignore
└── README.md                       # This file
```

---

## 🛠️ Technology Stack

### Backend

| Technology | Version | Purpose |
|------------|---------|---------|
| Python | 3.12 | Runtime |
| Flask | 3.0+ | Web framework |
| LangGraph | 0.0.1+ | Agent orchestration |
| DSPy | 2.0+ | Structured prompting |
| Google Generative AI | 0.3+ | Gemini models |
| LiteLLM | Latest | Model abstraction |
| UV | Latest | Package manager |
| Ruff | 0.9.1 | Linter & formatter |
| Gunicorn | 21.0+ | Production server |

### Frontend

| Technology | Version | Purpose |
|------------|---------|---------|
| Next.js | 16 | React framework |
| React | 19 | UI library |
| TypeScript | 5+ | Type safety |
| Tailwind CSS | 4 | Styling |
| Prisma | Latest | Database ORM |
| lucide-react | 0.469.0 | Icons |
| react-markdown | 9.0.3 | Markdown rendering |

### Infrastructure

| Technology | Purpose |
|------------|---------|
| Podman/Docker | Containerization |
| Podman Compose | Multi-container orchestration |
| SQLite | Development database |

---

## 🎭 Mocked Components

### ⚠️ Image Generation

**Status**: Partially mocked

**Reason**: Gemini API's `gemini-2.5-flash-image` model may not support direct image generation via `generate_content()`. Real image generation requires Google Cloud Vertex AI Imagen.

**Current Behavior**:
- System generates detailed prompt
- Attempts API call to `gemini-2.5-flash-image`
- May return empty response or placeholder
- Falls back gracefully with error message

**How to Integrate Real Generation**:

1. **Option 1: Vertex AI Imagen** (Recommended)
   ```python
   from google.cloud import aiplatform
   
   aiplatform.init(project="your-project", location="us-central1")
   model = aiplatform.ImageGenerationModel.from_pretrained("imagegeneration@006")
   response = model.generate_images(prompt=generation_prompt)
   ```

2. **Option 2: OpenAI DALL-E 3**
   ```python
   import openai
   response = openai.images.generate(
       model="dall-e-3",
       prompt=generation_prompt,
       size="1024x1792"
   )
   ```

3. **Option 3: Stable Diffusion (Replicate)**
   ```python
   import replicate
   output = replicate.run(
       "stability-ai/sdxl:...",
       input={"prompt": generation_prompt}
   )
   ```

### ✅ Working Components

All other components are fully functional:
- ✅ Vision analysis (Gemini 2.5 Pro/Flash)
- ✅ Trend generation (DSPy Chain-of-Thought)
- ✅ Styling advice synthesis (DSPy)
- ✅ Multi-agent orchestration (LangGraph)
- ✅ Mode selection (Quick/Deep)
- ✅ Frontend UI with three views
- ✅ File upload and validation
- ✅ API error handling

---

## 🧪 Testing

### Test API Endpoints

```bash
# Health check
curl http://localhost:5000/api/health

# Quick analyze with sample image
curl -X POST http://localhost:5000/api/analyze \
  -F "image=@../outfit_shorts.jpg" \
  -F "query=What should I wear?" \
  -F "mode=quick"

# Deep analyze
curl -X POST http://localhost:5000/api/analyze \
  -F "image=@../attractive_men_outfits_jeans.jpg" \
  -F "query=How can I style this for work?" \
  -F "mode=deep"
```

### Test via Frontend

1. Open http://localhost:3000
2. Upload an image from the project root
3. Try different queries and modes
4. Check browser console for errors

### Run Backend Tests

```bash
cd backend
uv run pytest  # If tests are added later
```

---

## 🔒 Security & Best Practices

### Environment Variables

- Never commit `.env` file
- Use `.env.example` as template
- Rotate API keys regularly
- Use secrets management in production

### File Upload Security

- Max file size: 10MB
- Allowed formats: PNG, JPG, JPEG, GIF, WEBP
- Validation on both client and server
- No direct file system access

### Production Considerations

- Enable HTTPS/TLS
- Set up CORS properly
- Implement rate limiting
- Add authentication/authorization
- Monitor API usage and costs
- Set up error tracking (Sentry)

---

## 📝 Development Workflow

### Making Changes

```bash
# 1. Create feature branch
git checkout -b feature/your-feature

# 2. Make changes and test locally
cd backend && uv run flask run --debug
cd frontend && npm run dev

# 3. Run linters
cd backend && uv run ruff check . --fix && uv run ruff format .
cd frontend && npm run lint

# 4. Test in containers
podman-compose up --build

# 5. Commit and push
git add .
git commit -m "feat: your feature description"
git push origin feature/your-feature
```

### Debugging Tips

**Backend Issues:**
```bash
# View detailed logs
podman logs outfit-backend -f

# Check environment
podman exec -it outfit-backend env | grep GOOGLE

# Access container shell
podman exec -it outfit-backend bash
```

**Frontend Issues:**
```bash
# View Next.js logs
podman logs outfit-frontend -f

# Check build output
podman exec -it outfit-frontend ls -la .next/

# Access container shell
podman exec -it outfit-frontend sh
```

---

## 📄 License

[Your License Here]

## 👥 Contributors

[Your Team Here]

## 🙏 Acknowledgments

- Google Gemini for powerful multimodal AI
- LangGraph for agent orchestration
- DSPy for structured prompting
- Vercel for Next.js framework
- Astral.sh for UV and Ruff tools

---

## 🔧 Troubleshooting

### Podman Machine Not Running

```bash
# Check status
podman machine list

# Start machine
podman machine start

# Restart machine
podman machine stop && podman machine start
```

### Build Failures

```bash
# Clean rebuild
./run-podman.sh clean
./run-podman.sh start

# Check logs
podman logs outfit-backend
podman logs outfit-frontend
```

### Port Already in Use

```bash
# Stop conflicting services
lsof -ti:5000 | xargs kill -9  # Backend port
lsof -ti:3000 | xargs kill -9  # Frontend port

# Or change ports in compose.yaml
```

### API Not Responding

```bash
# Check container status
podman ps

# Check backend logs
podman logs outfit-backend -f

# Test health endpoint
curl http://localhost:5000/api/health
```

### Frontend Can't Reach Backend

Make sure both containers are on the same network:
```bash
podman network inspect outfit-network
```

### Image Generation Not Working

This is expected - see [Mocked Components](#-mocked-components) section. To enable real generation, integrate Vertex AI Imagen or DALL-E 3.

---
