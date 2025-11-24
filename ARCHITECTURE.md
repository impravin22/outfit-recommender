# Project Aura - Architecture Overview

## System Architecture

Project Aura is a sophisticated multi-agent AI fashion stylist system built with modern web technologies and advanced AI orchestration.

### High-Level Architecture

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

## Component Architecture

### Frontend Architecture

**Technology Stack:**
- **Framework:** Next.js 16 with App Router
- **UI Library:** React 19
- **Styling:** Tailwind CSS 4
- **Language:** TypeScript 5
- **State Management:** React useState/useEffect

**Key Components:**
- **Upload Interface:** Drag-and-drop file upload with preview
- **Processing Overlay:** Animated agent workflow visualization
- **Results Dashboard:** Side-by-side comparison with AI analysis
- **Server Actions:** Next.js 16 server actions for API communication

**File Structure:**
```
frontend/
├── src/
│   ├── app/
│   │   ├── layout.tsx      # Root layout with navigation
│   │   ├── page.tsx        # Main application page
│   │   └── actions.ts      # Server actions for API calls
│   └── components/         # (Currently empty - cleaned up)
├── prisma/
│   └── schema.prisma       # Database schema for logging
├── package.json
├── next.config.js          # Next.js configuration
├── tsconfig.json           # TypeScript configuration
└── tailwind.config.ts      # Tailwind CSS configuration
```

### Backend Architecture

**Technology Stack:**
- **Framework:** Flask with Flask-CORS
- **Language:** Python 3.12
- **Package Manager:** UV
- **AI Orchestration:** LangGraph
- **LLM Framework:** DSPy
- **AI Models:** Google Gemini 2.5 Pro/Flash
- **Server:** Gunicorn for production

**Core Components:**

#### 1. Agent System (`app/agents/`)
- **supervisor.py:** LangGraph state machine orchestration
- **state.py:** TypedDict definitions for agent state
- **config.py:** LM configuration per analysis mode
- **multi_model.py:** Vision analysis and image generation
- **analysis.py:** Styling advice synthesis using DSPy
- **trending.py:** Trend generation using DSPy
- **dspy_signatures.py:** DSPy signature definitions

#### 2. API Layer (`app/routers/`)
- **analyze.py:** Main analysis endpoint with file upload handling
- **healthcheck.py:** Health check endpoint

#### 3. Utilities (`app/utils/`)
- **logs.py:** Agent execution logging utilities

#### 4. Main Application (`app/main.py`)
- Flask application setup with CORS
- Blueprint registration
- Development server configuration

**File Structure:**
```
backend/
├── app/
│   ├── agents/             # Multi-agent system
│   │   ├── config.py       # LM configuration per mode
│   │   ├── state.py        # AgentState TypedDict
│   │   ├── supervisor.py   # LangGraph orchestration
│   │   ├── multi_model.py  # Vision + Generation
│   │   ├── analysis.py     # Styling advice synthesis
│   │   ├── trending.py     # Trend generation
│   │   └── dspy_signatures.py # DSPy signatures
│   ├── routers/
│   │   ├── analyze.py      # POST /analyze endpoint
│   │   └── healthcheck.py  # GET /health endpoint
│   ├── utils/
│   │   └── logs.py         # Agent logging utilities
│   └── main.py             # Flask app entry point
├── pyproject.toml          # UV dependencies & Ruff config
├── uv.lock                 # Dependency lock file
├── run.py                  # Development runner script
└── Containerfile           # Podman/Docker container config
```

## Agent Workflow Architecture

### Sequential Multi-Agent Pipeline

The system implements a sophisticated 4-agent workflow orchestrated by LangGraph:

```
┌─────────────────────────────────────────────────────────────────────┐
│                        AGENT WORKFLOW                               │
└─────────────────────────────────────────────────────────────────────┘

   User Uploads Image + Query
          ↓
┌──────────────────────┐
│   1. VISION AGENT    │  ← Gemini 2.5 Pro (Deep) / 2.5 Flash (Quick)
│  analyze_image()     │
└──────────────────────┘
          ↓
    Structured Visual Analysis:
    - Gender Style Classification
    - Cut & Silhouette Analysis
    - Color Palette Extraction
    - Textile & Texture Assessment
    - Occasion Suitability
          ↓
┌──────────────────────┐
│   2. TRENDS AGENT    │  ← DSPy Chain-of-Thought
│  fetch_trends()      │
└──────────────────────┘
          ↓
    Contextual Trend Summary:
    - Current Fashion Movements
    - Seasonal Color Palettes
    - Textile Innovations
    - Silhouette Trends
          ↓
┌──────────────────────┐
│   3. ADVISOR AGENT   │  ← DSPy Chain-of-Thought
│  synthesize_advice() │
└──────────────────────┘
          ↓
    Personalized Recommendations:
    - Style Improvement Suggestions
    - Occasion-Specific Advice
    - Color Theory Applications
    - Accessory Recommendations
          ↓
┌──────────────────────┐
│   4. GENERATOR AGENT │  ← Gemini 2.5 Flash Image
│  generate_outfit()   │
└──────────────────────┘
          ↓
    AI-Generated Outfit Visualization
          ↓
    JSON Response Compilation
```

### Agent Communication Flow

**State Management:**
- **LangGraph StateGraph:** Manages agent transitions and state
- **TypedDict State:** Strongly typed agent state with visual analysis, trends, advice, and generation results
- **Error Handling:** Graceful degradation when agents fail

**Data Flow:**
1. **Input Processing:** Image upload → Base64 encoding → Gemini Vision API
2. **State Updates:** Each agent updates the shared state with its results
3. **Conditional Logic:** Different paths for Quick vs Deep analysis modes
4. **Output Synthesis:** Final JSON compilation with all agent outputs

## Data Architecture

### API Schema

**Request Format:**
```typescript
POST /api/analyze
Content-Type: multipart/form-data

{
  image: File,        // Outfit image (PNG/JPG/JPEG/GIF/WEBP)
  query: string,      // User question/context
  mode: "quick" | "deep"  // Analysis depth
}
```

**Response Format:**
```typescript
{
  visual_analysis: {
    gender_style: string,
    cut: string,
    color: string,
    fabric: string,
    occasion: string
  },
  trend_summary: string,     // Markdown formatted
  final_report: string,      // Comprehensive advice
  generated_image_url: string,
  analysis_mode: "quick" | "deep",
  generation_prompt: string,
  image_generation_error: string | null
}
```

### Database Schema (Development)

**Prisma Schema:**
```prisma
model RequestLog {
  id        Int      @id @default(autoincrement())
  query     String
  createdAt DateTime @default(now())
}
```

## Deployment Architecture

### Container Architecture

**Multi-Container Setup:**
- **Backend Container:** Python 3.12 + Flask + Gunicorn
- **Frontend Container:** Node.js 20 + Next.js production build
- **Network:** Podman/Docker network for inter-container communication

**Container Configuration:**
- **Backend:** Health checks, environment variables, volume mounts
- **Frontend:** Static optimization, API proxy configuration
- **Shared Network:** Service discovery via container names

### Environment Architecture

**Development:**
- Local Flask server with hot reload
- Next.js development server
- SQLite database for logging
- Direct API communication

**Production:**
- Gunicorn WSGI server
- Next.js production build
- Podman/Docker containerization
- Environment-based configuration

## Security Architecture

### Input Validation
- File type validation (images only)
- File size limits (10MB)
- Base64 encoding for API transmission

### API Security
- CORS configuration
- Input sanitization
- Error message sanitization
- No sensitive data exposure

### Container Security
- Non-root user execution
- Minimal base images
- No development dependencies in production
- Environment variable management

## Performance Architecture

### Frontend Optimization
- Next.js 16 App Router for performance
- React 19 concurrent features
- Tailwind CSS for optimized styling
- Image optimization (when implemented)

### Backend Optimization
- LangGraph for efficient agent orchestration
- DSPy for structured prompting
- Gunicorn for production serving
- Health checks for monitoring

### AI Model Optimization
- Model selection based on analysis depth
- Streaming responses (when supported)
- Error handling and fallbacks
- Cost optimization through appropriate model selection

## Monitoring & Observability

### Logging Architecture
- Agent execution logging
- API request/response logging
- Error tracking and reporting
- Development vs production log levels

### Health Checks
- Backend health endpoint
- Container health checks
- API responsiveness monitoring
- Dependency availability checks

This architecture provides a scalable, maintainable, and performant foundation for the AI fashion stylist application.</content>
<parameter name="filePath">/Users/kumarpr/Desktop/Projects/outfit-recommender/ARCHITECTURE.md