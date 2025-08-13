# AI Training Planner - MCP Implementation

This document describes the Model Context Protocol (MCP) implementation in the AI Training Planner.

## Architecture Overview

The AI Training Planner now includes a complete MCP-based architecture:

```
┌─────────────────┐     ┌─────────────────┐     ┌─────────────────┐
│   React         │────▶│   Flask         │────▶│   MCP Server    │
│   Frontend      │     │   Backend       │     │   (aiohttp)     │
│   (Port 3000)   │     │   (Port 5002)   │     │   (Port 8080)   │
└─────────────────┘     └─────────────────┘     └─────────────────┘
                                                          │
                                                          ▼
                                                ┌─────────────────┐
                                                │   Ollama        │
                                                │   (Port 11434)  │
                                                └─────────────────┘
```

## MCP Server Implementation

### Location

- Server: `src/mcp_server/server.py`
- Client: `src/llm/mcp_client.py`
- Config: `src/config/mcp_config.py`
- Service: `src/llm/career_advisor.py`

### Features

1. **HTTP API Server**: Built with aiohttp for async performance
2. **Career Path Analysis**: Intelligent career path recommendations
3. **Path Refinement**: Personalized adjustments based on user feedback
4. **Ollama Integration**: Uses Llama 3.3:70b-instruct-q2_K model for dynamic content generation
5. **Fallback System**: Structured responses when LLM is unavailable
6. **Docker Integration**: Fully containerized with health checks

### API Endpoints

#### Health Check

```bash
GET /health
```

#### Career Analysis

```bash
POST /api/career/analyze
{
  "user_data": {
    "job_title": "Software Developer",
    "description": "...",
    "completed_badges": [],
    "completed_courses": [],
    "in_progress_courses": []
  },
  "career_preferences": "I want to learn machine learning and AI"
}
```

#### Career Path Refinement

```bash
POST /api/career/refine
{
  "user_data": {...},
  "selected_path": "AI/ML Engineering Path",
  "user_feedback": "I want to focus more on practical projects"
}
```

## Configuration

### Environment Variables

- `MCP_SERVER_URL`: URL of the MCP server (default: http://localhost:8080)
- `MCP_HOST`: Host for MCP server (default: 0.0.0.0)
- `MCP_PORT`: Port for MCP server (default: 8080)
- `OLLAMA_URL`: URL of Ollama service (default: http://ollama:11434)
- `MODEL_NAME`: Ollama model name (default: llama3.3:70b-instruct-q2_K)

### Docker Configuration

The MCP server is configured in `docker-compose.yml`:

```yaml
mcp-server:
  build:
    context: .
    dockerfile: Dockerfile.mcp
  ports:
    - "8080:8080"
  environment:
    - PYTHONUNBUFFERED=1
    - MCP_HOST=0.0.0.0
    - MCP_PORT=8080
```

## Usage

### Starting the Complete System

```bash
# Use the provided startup script
./start-mcp.sh

# Or manually with Docker Compose
docker-compose build
docker-compose up -d
```

### Integration with Flask Backend

The Flask backend automatically uses the MCP server for career guidance:

1. **CareerAdvisor Service**: Handles async communication with MCP server
2. **Async Route Handlers**: Flask routes use async decorators for MCP calls
3. **Fallback System**: Returns structured data if MCP server is unavailable
4. **Error Handling**: Graceful degradation with meaningful error messages

### Frontend Integration

No changes required to the React frontend - it continues to use the same API endpoints:

- `POST /api/career/paths`
- `POST /api/career/refine`

## Development

### Local Development

1. Start services: `./start-mcp.sh`
2. Frontend: http://localhost:3000
3. Backend API: http://localhost:5002
4. MCP Server: http://localhost:8080
5. Ollama: http://localhost:11434

### Adding New MCP Features

1. Add endpoint to `src/mcp_server/server.py`
2. Add client method to `src/llm/mcp_client.py`
3. Update `CareerAdvisor` in `src/llm/career_advisor.py`
4. Add Flask route in `src/api/server.py`

### Testing MCP Server Directly

```bash
# Health check
curl http://localhost:8080/health

# Career analysis
curl -X POST http://localhost:8080/api/career/analyze \
  -H "Content-Type: application/json" \
  -d '{"user_data": {...}, "career_preferences": "..."}'
```

## Benefits of MCP Implementation

1. **Scalability**: Separate MCP server can scale independently
2. **Modularity**: Clear separation between AI logic and web application
3. **Performance**: Async architecture for better concurrent handling
4. **Flexibility**: Easy to switch between different AI providers
5. **Reliability**: Robust fallback system ensures service availability
6. **Maintainability**: Well-structured codebase with clear responsibilities

## Troubleshooting

### MCP Server Not Starting

1. Check Docker logs: `docker-compose logs mcp-server`
2. Verify port availability: `lsof -i :8080`
3. Check requirements: `pip install -r src/mcp_server/requirements.txt`

### Backend Connection Issues

1. Verify MCP_SERVER_URL environment variable
2. Check network connectivity between containers
3. Review Flask backend logs: `docker-compose logs backend`

### Ollama Integration Issues

1. Ensure Ollama is running: `curl http://localhost:11434/api/tags`
2. Verify Llama 3.3:70b model is pulled: `docker-compose logs ollama-init`
3. Check MCP server Ollama URL configuration

## Future Enhancements

1. **Multiple Model Support**: Support for different AI models
2. **Caching**: Redis cache for frequently requested career paths
3. **Analytics**: Usage tracking and recommendation improvement
4. **Authentication**: User-specific career path history
5. **Real-time Updates**: WebSocket support for live refinements
