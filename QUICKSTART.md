# Project Aura - Quickstart Guide

## 🚀 Quick Start

Get Project Aura up and running in minutes with containerized deployment.

## Prerequisites

Before you begin, ensure you have the following installed:

### Required Software
- **Podman** (or Docker) - Container runtime
- **Git** - Version control
- **curl** - For API testing (optional)

### System Requirements
- **OS:** macOS, Linux, or Windows with WSL2
- **RAM:** 4GB minimum, 8GB recommended
- **Storage:** 2GB free space
- **Network:** Internet connection for AI API calls

### API Keys
- **Google Gemini API Key** - Required for AI functionality

## ⚡ Quick Setup (5 minutes)

### 1. Clone the Repository
```bash
git clone <repository-url>
cd outfit-recommender
```

### 2. Set Up Environment Variables
```bash
# Create environment file
cp .env.example .env

# Edit .env and add your Google Gemini API key
# GOOGLE_API_KEY=your_api_key_here
```

### 3. Start the Application
```bash
# Make the script executable (first time only)
chmod +x run-podman.sh

# Start all services
./run-podman.sh start
```

### 4. Access the Application
- **Frontend:** http://localhost:3000
- **Backend API:** http://localhost:5000/api
- **Health Check:** http://localhost:5000/api/health

## 🧪 Testing the Application

### Health Check
```bash
curl http://localhost:5000/api/health
```

Expected response:
```json
{
  "status": "healthy",
  "timestamp": "2024-01-01T12:00:00Z"
}
```

### API Testing
```bash
# Run the test script
./test-api.sh
```

Or test manually:
```bash
# Quick analysis (replace with your image)
curl -X POST http://localhost:5000/api/analyze \
  -F "image=@./your-outfit.jpg" \
  -F "query=What should I wear?" \
  -F "mode=quick" | jq .
```

## 🛠️ Development Setup

### Backend Development

#### Prerequisites
- **Python 3.11+**
- **UV** package manager

#### Setup
```bash
cd backend

# Install dependencies
uv sync

# Activate virtual environment
source .venv/bin/activate  # On Windows: .venv\Scripts\activate

# Run development server
python run.py
```

#### Code Quality
```bash
# Format code
uv run ruff format .

# Lint code
uv run ruff check .

# Type checking
uv run pyright
```

### Frontend Development

#### Prerequisites
- **Node.js 20+**
- **npm** or **yarn**

#### Setup
```bash
cd frontend

# Install dependencies
npm install

# Run development server
npm run dev
```

#### Code Quality
```bash
# Lint code
npm run lint

# Build for production
npm run build
```

## 📁 Project Structure

```
outfit-recommender/
├── backend/                 # Python Flask API
│   ├── app/
│   │   ├── agents/         # Multi-agent system
│   │   ├── routers/        # API endpoints
│   │   ├── utils/          # Utilities
│   │   └── main.py         # Flask app
│   ├── pyproject.toml      # Dependencies & config
│   ├── run.py             # Development runner
│   └── Containerfile      # Podman/Docker config
├── frontend/               # Next.js React app
│   ├── src/
│   │   ├── app/           # Next.js app router
│   │   └── components/    # React components
│   ├── package.json       # Dependencies
│   ├── next.config.js     # Next.js config
│   └── Containerfile      # Podman/Docker config
├── compose.yaml           # Docker Compose config
├── run-podman.sh         # Deployment script
└── test-api.sh           # API testing script
```

## 🔧 Configuration

### Environment Variables

#### Required
- `GOOGLE_API_KEY` - Your Google Gemini API key

#### Optional
- `FLASK_ENV` - Flask environment (development/production)
- `DATABASE_URL` - Database connection string (development only)

### Analysis Modes

#### Quick Mode
- Fast analysis using Gemini 2.5 Flash
- Basic visual analysis and styling advice
- Suitable for quick feedback

#### Deep Mode
- Comprehensive analysis using Gemini 2.5 Pro
- Detailed trend analysis and styling recommendations
- Multi-agent workflow with trend synthesis

## 🚦 Managing the Application

### Podman Commands

```bash
# Start application
./run-podman.sh start

# Stop application
./run-podman.sh stop

# View logs
./run-podman.sh logs

# Restart application
./run-podman.sh restart

# Rebuild containers
./run-podman.sh build

# Clean up everything
./run-podman.sh clean
```

### Docker Alternative

If you prefer Docker over Podman:

```bash
# Build and start
docker-compose up --build

# Run in background
docker-compose up -d --build

# Stop
docker-compose down

# View logs
docker-compose logs -f
```

## 🐛 Troubleshooting

### Common Issues

#### Frontend Container Won't Start
**Problem:** TypeScript runtime dependency in production
**Solution:** Ensure `next.config.js` exists (not `.ts`)

#### Backend Health Check Fails
**Problem:** GOOGLE_API_KEY not set or invalid
**Solution:**
```bash
# Check environment variables
cat .env

# Restart containers
./run-podman.sh restart
```

#### Port Already in Use
**Problem:** Ports 3000 or 5000 are occupied
**Solution:**
```bash
# Find process using port
lsof -i :3000
lsof -i :5000

# Kill process or change ports in compose.yaml
```

#### Podman Machine Issues (macOS)
**Problem:** Podman machine not running
**Solution:**
```bash
podman machine start
./run-podman.sh start
```

### Logs and Debugging

```bash
# View all container logs
./run-podman.sh logs

# View specific container logs
podman logs outfit-backend
podman logs outfit-frontend

# Check container status
podman ps

# Access container shell
podman exec -it outfit-backend /bin/bash
```

### API Debugging

```bash
# Test health endpoint
curl -v http://localhost:5000/api/health

# Test with sample data
curl -X POST http://localhost:5000/api/analyze \
  -F "image=@./sample.jpg" \
  -F "query=Test query" \
  -F "mode=quick"
```

## 📚 Next Steps

1. **Upload an outfit image** through the web interface
2. **Ask questions** like:
   - "What should I wear for a summer wedding?"
   - "How can I style this for different occasions?"
   - "What colors would complement this outfit?"

3. **Experiment with analysis modes:**
   - Quick mode for fast feedback
   - Deep mode for comprehensive analysis

4. **Explore the architecture** in `ARCHITECTURE.md` for technical details

## 🤝 Contributing

1. Fork the repository
2. Create a feature branch
3. Make your changes
4. Test thoroughly
5. Submit a pull request

## 📄 License

This project is licensed under the MIT License - see the LICENSE file for details.</content>
<parameter name="filePath">/Users/kumarpr/Desktop/Projects/outfit-recommender/QUICKSTART.md
