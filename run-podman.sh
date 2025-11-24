#!/bin/bash

# Project Aura - Podman Deployment Script
# This script helps build and run the application using Podman

set -e

# Colors for output
GREEN='\033[0;32m'
BLUE='\033[0;34m'
YELLOW='\033[1;33m'
RED='\033[0;31m'
NC='\033[0m' # No Color

# Check if .env file exists
if [ ! -f .env ]; then
    echo -e "${RED}Error: .env file not found!${NC}"
    echo "Please create .env file with your GOOGLE_API_KEY"
    echo "Example: cp .env.example .env"
    exit 1
fi

# Load environment variables
export $(cat .env | grep -v '^#' | xargs)

# Function to check Podman machine status
check_podman_machine() {
    echo -e "${BLUE}Checking Podman machine status...${NC}"
    if ! podman machine list | grep -q "Currently running"; then
        echo -e "${YELLOW}Starting Podman machine...${NC}"
        podman machine start
    else
        echo -e "${GREEN}✓ Podman machine is running${NC}"
    fi
}

# Function to build containers
build_containers() {
    echo -e "${BLUE}Building containers...${NC}"
    
    echo -e "${YELLOW}Building backend...${NC}"
    podman build -t outfit-backend -f backend/Containerfile backend/
    echo -e "${GREEN}✓ Backend built successfully${NC}"
    
    echo -e "${YELLOW}Building frontend...${NC}"
    podman build -t outfit-frontend -f frontend/Containerfile frontend/
    echo -e "${GREEN}✓ Frontend built successfully${NC}"
}

# Function to stop and remove existing containers
cleanup_containers() {
    echo -e "${BLUE}Cleaning up existing containers...${NC}"
    podman stop outfit-backend outfit-frontend 2>/dev/null || true
    podman rm outfit-backend outfit-frontend 2>/dev/null || true
}

# Function to create network
create_network() {
    echo -e "${BLUE}Creating network...${NC}"
    podman network exists outfit-network 2>/dev/null || podman network create outfit-network
    echo -e "${GREEN}✓ Network ready${NC}"
}

# Function to run backend
run_backend() {
    echo -e "${BLUE}Starting backend...${NC}"
    podman run -d \
        --name outfit-backend \
        --network outfit-network \
        -p 5000:5000 \
        -e GOOGLE_API_KEY="${GOOGLE_API_KEY}" \
        -e FLASK_ENV=production \
        outfit-backend
    
    echo -e "${GREEN}✓ Backend started on http://localhost:5000${NC}"
}

# Function to run frontend
run_frontend() {
    echo -e "${BLUE}Starting frontend...${NC}"
    podman run -d \
        --name outfit-frontend \
        --network outfit-network \
        -p 3000:3000 \
        -e NEXT_PUBLIC_API_URL=http://localhost:5000/api \
        -e BACKEND_INTERNAL_URL=http://outfit-backend:5000/api \
        -e DATABASE_URL=file:./dev.db \
        outfit-frontend
    
    echo -e "${GREEN}✓ Frontend started on http://localhost:3000${NC}"
}

# Function to show logs
show_logs() {
    echo -e "${BLUE}Showing container logs (Ctrl+C to exit)...${NC}"
    podman logs -f outfit-backend &
    BACKEND_PID=$!
    podman logs -f outfit-frontend &
    FRONTEND_PID=$!
    
    trap "kill $BACKEND_PID $FRONTEND_PID 2>/dev/null; exit" INT
    wait
}

# Function to test health
test_health() {
    echo -e "${BLUE}Testing backend health...${NC}"
    sleep 5
    HEALTH_RESPONSE=$(curl -s http://localhost:5000/api/health || true)
    if echo "$HEALTH_RESPONSE" | grep -q '"status":"ok"'; then
        echo -e "${GREEN}✓ Backend is healthy${NC}"
    else
        echo -e "${RED}✗ Backend health check failed${NC}"
        echo -e "${YELLOW}Response was:${NC} $HEALTH_RESPONSE"
    fi
}

# Main script
case "${1:-}" in
    start)
        check_podman_machine
        build_containers
        cleanup_containers
        create_network
        run_backend
        sleep 3
        run_frontend
        test_health
        echo ""
        echo -e "${GREEN}========================================${NC}"
        echo -e "${GREEN}🚀 Project Aura is running!${NC}"
        echo -e "${GREEN}========================================${NC}"
        echo -e "Frontend: ${BLUE}http://localhost:3000${NC}"
        echo -e "Backend:  ${BLUE}http://localhost:5000/api${NC}"
        echo -e "Health:   ${BLUE}http://localhost:5000/api/health${NC}"
        echo ""
        echo -e "View logs: ${YELLOW}./run-podman.sh logs${NC}"
        echo -e "Stop:      ${YELLOW}./run-podman.sh stop${NC}"
        ;;
    
    stop)
        echo -e "${BLUE}Stopping containers...${NC}"
        podman stop outfit-backend outfit-frontend 2>/dev/null || true
        podman rm outfit-backend outfit-frontend 2>/dev/null || true
        echo -e "${GREEN}✓ Containers stopped${NC}"
        ;;
    
    logs)
        show_logs
        ;;
    
    restart)
        $0 stop
        sleep 2
        $0 start
        ;;
    
    build)
        check_podman_machine
        build_containers
        echo -e "${GREEN}✓ Build complete${NC}"
        ;;
    
    clean)
        echo -e "${BLUE}Cleaning up everything...${NC}"
        cleanup_containers
        podman rmi outfit-backend outfit-frontend 2>/dev/null || true
        podman network rm outfit-network 2>/dev/null || true
        echo -e "${GREEN}✓ Cleanup complete${NC}"
        ;;
    
    test)
        echo -e "${BLUE}Testing API endpoint...${NC}"
        echo ""
        echo -e "${YELLOW}1. Health check:${NC}"
        curl -s http://localhost:5000/api/health | jq .
        echo ""
        echo -e "${YELLOW}2. Test analyze endpoint (use your own image):${NC}"
        echo "curl -X POST http://localhost:5000/api/analyze \\"
        echo "  -F \"image=@./outfit_shorts.jpg\" \\"
        echo "  -F \"query=What should I wear?\" \\"
        echo "  -F \"mode=quick\" | jq ."
        ;;
    
    *)
        echo "Project Aura - Podman Deployment Script"
        echo ""
        echo "Usage: ./run-podman.sh [command]"
        echo ""
        echo "Commands:"
        echo "  start    - Build and start all containers"
        echo "  stop     - Stop and remove containers"
        echo "  restart  - Restart all containers"
        echo "  logs     - Show container logs (follow mode)"
        echo "  build    - Build containers only"
        echo "  clean    - Remove all containers and images"
        echo "  test     - Test API endpoints"
        echo ""
        echo "Examples:"
        echo "  ./run-podman.sh start   # Start the application"
        echo "  ./run-podman.sh logs    # View logs"
        echo "  ./run-podman.sh stop    # Stop the application"
        ;;
esac
