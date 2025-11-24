#!/bin/bash

# Test Script for Project Aura API
# This script tests all API endpoints

set -e

GREEN='\033[0;32m'
BLUE='\033[0;34m'
YELLOW='\033[1;33m'
RED='\033[0;31m'
NC='\033[0m'

API_URL="http://localhost:5000/api"

echo -e "${BLUE}========================================${NC}"
echo -e "${BLUE}Project Aura - API Test Script${NC}"
echo -e "${BLUE}========================================${NC}"
echo ""

# Test 1: Health Check
echo -e "${YELLOW}Test 1: Health Check${NC}"
echo "GET $API_URL/health"
echo ""
HEALTH_RESPONSE=$(curl -s "$API_URL/health")
echo "$HEALTH_RESPONSE" | jq .
if echo "$HEALTH_RESPONSE" | grep -q "healthy"; then
    echo -e "${GREEN}✓ Health check passed${NC}"
else
    echo -e "${RED}✗ Health check failed${NC}"
    exit 1
fi
echo ""
echo "---"
echo ""

# Test 2: Quick Analyze (requires image file)
if [ -f "outfit_shorts.jpg" ]; then
    echo -e "${YELLOW}Test 2: Quick Analyze${NC}"
    echo "POST $API_URL/analyze"
    echo "  - image: outfit_shorts.jpg"
    echo "  - query: What should I wear for a summer wedding?"
    echo "  - mode: quick"
    echo ""
    
    QUICK_RESPONSE=$(curl -s -X POST "$API_URL/analyze" \
        -F "image=@outfit_shorts.jpg" \
        -F "query=What should I wear for a summer wedding?" \
        -F "mode=quick")
    
    echo "$QUICK_RESPONSE" | jq .
    
    if echo "$QUICK_RESPONSE" | grep -q "visual_analysis"; then
        echo -e "${GREEN}✓ Quick analyze completed${NC}"
    else
        echo -e "${RED}✗ Quick analyze failed${NC}"
    fi
    echo ""
    echo "---"
    echo ""
fi

# Test 3: Deep Analyze (requires image file)
if [ -f "attractive_men_outfits_jeans.jpg" ]; then
    echo -e "${YELLOW}Test 3: Deep Analyze${NC}"
    echo "POST $API_URL/analyze"
    echo "  - image: attractive_men_outfits_jeans.jpg"
    echo "  - query: How can I style this outfit for different occasions?"
    echo "  - mode: deep"
    echo ""
    
    DEEP_RESPONSE=$(curl -s -X POST "$API_URL/analyze" \
        -F "image=@attractive_men_outfits_jeans.jpg" \
        -F "query=How can I style this outfit for different occasions?" \
        -F "mode=deep")
    
    echo "$DEEP_RESPONSE" | jq .
    
    if echo "$DEEP_RESPONSE" | grep -q "final_report"; then
        echo -e "${GREEN}✓ Deep analyze completed${NC}"
    else
        echo -e "${RED}✗ Deep analyze failed${NC}"
    fi
    echo ""
    echo "---"
    echo ""
fi

# Test 4: Error Handling - No Image
echo -e "${YELLOW}Test 4: Error Handling - No Image${NC}"
echo "POST $API_URL/analyze (without image)"
echo ""
ERROR_RESPONSE=$(curl -s -X POST "$API_URL/analyze" -F "query=Test")
echo "$ERROR_RESPONSE" | jq .
if echo "$ERROR_RESPONSE" | grep -q "error"; then
    echo -e "${GREEN}✓ Error handling works${NC}"
else
    echo -e "${RED}✗ Error handling failed${NC}"
fi
echo ""
echo "---"
echo ""

echo -e "${BLUE}========================================${NC}"
echo -e "${GREEN}API Tests Complete!${NC}"
echo -e "${BLUE}========================================${NC}"
echo ""
echo "Example curl commands:"
echo ""
echo -e "${YELLOW}# Health check${NC}"
echo "curl http://localhost:5000/api/health"
echo ""
echo -e "${YELLOW}# Quick analyze${NC}"
echo "curl -X POST http://localhost:5000/api/analyze \\"
echo "  -F \"image=@./outfit.jpg\" \\"
echo "  -F \"query=What should I wear?\" \\"
echo "  -F \"mode=quick\" | jq ."
echo ""
echo -e "${YELLOW}# Deep analyze${NC}"
echo "curl -X POST http://localhost:5000/api/analyze \\"
echo "  -F \"image=@./outfit.jpg\" \\"
echo "  -F \"query=Style tips for formal events?\" \\"
echo "  -F \"mode=deep\" | jq ."
