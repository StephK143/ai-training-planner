# AI Training Planner

A sophisticated career development tool that helps users visualize and plan their learning path using an interactive skill tree and AI-powered career advisor.

## 🌟 Features

- Interactive skill tree visualization
- Dark mode UI with modern design
- User-specific progress tracking
- AI-powered career path recommendations
- Badge and course completion tracking
- Real-time skill path visualization

## 🚀 Getting Started

### Option 1: Docker Setup (Recommended)

The easiest way to run the application is using Docker Compose, which handles all dependencies and services automatically.

#### Prerequisites

- [Docker](https://docs.docker.com/get-docker/) installed
- [Docker Compose](https://docs.docker.com/compose/install/) installed

#### Quick Start

1. Clone the repository:

```bash
git clone https://github.com/StephK143/ai-training-planner.git
cd ai-training-planner
```

2. Start all services:

```bash
docker compose up --build
```

3. Wait for all services to start (this may take a few minutes on first run as it downloads the Llama 3.3:70b model)

4. Access the application:
   - **Frontend**: [http://localhost:3000](http://localhost:3000)
   - **Backend API**: [http://localhost:5002](http://localhost:5002)
   - **Ollama API**: [http://localhost:11434](http://localhost:11434)

#### Docker Services

The Docker setup includes:

- **Frontend**: React app served by Nginx with optimized timeout settings for LLM requests
- **Backend**: Python Flask API server with AI integration
- **MCP Server**: Custom HTTP API for enhanced AI career guidance
- **Ollama**: Local LLM service with Llama 3.3:70b model automatically downloaded
- **Ollama Init**: One-time service that ensures the Llama 3.3:70b model is available

#### Stopping the Application

```bash
docker compose down
```

### Option 2: Manual Setup

If you prefer to run the services manually:

#### Prerequisites

- Node.js 18+
- Python 3.9+
- [Ollama](https://ollama.ai) installed locally

#### Setup Steps

1. Clone the repository:

```bash
git clone https://github.com/StephK143/ai-training-planner.git
cd ai-training-planner
```

2. Install frontend dependencies:

```bash
npm install
```

3. Install backend dependencies:

```bash
pip install -r requirements.txt
```

4. Pull the Llama 3.3:70b model:

```bash
ollama pull llama3.3:70b-instruct-q2_K
```

5. Start Ollama service:

```bash
ollama serve
```

6. Start the Flask backend server:

```bash
python src/api/server.py
```

7. Start the frontend development server:

```bash
npm run dev
```

**Access URLs:**

- Frontend: [http://localhost:5174](http://localhost:5174)
- Backend API: [http://localhost:5002](http://localhost:5002)

## 🤖 About the LLM Choice

This project uses **Llama 3.3:70b-instruct-q2_K** through Ollama for several key reasons:

1. **Advanced Reasoning**: Llama 3.3 offers significantly improved reasoning capabilities for complex career guidance
2. **Large Context Window**: 25k+ token context enables comprehensive career planning discussions
3. **Local Processing**: All AI computations happen locally, ensuring data privacy and reducing latency
4. **No API Costs**: Unlike cloud-based solutions, there are no ongoing API costs
5. **Optimized Performance**: Q2_K quantization provides excellent performance with manageable resource usage
6. **Open Source**: Being open source, it allows for greater customization and transparency
7. **Active Community**: Strong community support and regular updates ensure long-term viability

## 🎯 Core Functionality

- **Skill Tree Visualization**: Interactive view of available learning paths
- **Progress Tracking**: Monitor completion status of courses and badges
- **AI Career Advisor**: Get personalized career path recommendations

## 🎨 UI/UX Features

- Elegant dark mode interface
- Responsive design
- Interactive card animations
- Intuitive navigation
- Progress indicators
- Status badges for courses

## 🛠 Technical Stack

- **Frontend**: React + TypeScript, Material-UI components
- **Backend**: Python Flask API with AI integration
- **MCP Server**: Custom HTTP API server for enhanced AI capabilities
- **LLM**: Ollama with Llama 3.3:70b-instruct-q2_K model for advanced AI processing
- **Containerization**: Docker & Docker Compose for easy deployment
- **Web Server**: Nginx for production-ready frontend serving
- **State Management**: Local state management with custom hooks

## 🔧 Troubleshooting

### Docker Issues

**Docker daemon not running:**
If you get an error like `Cannot connect to the Docker daemon` or `Is the docker daemon running?`, you need to start Docker Desktop:

- **macOS/Windows**: Open Docker Desktop application from your Applications folder or system menu
- **Linux**: Start Docker service: `sudo systemctl start docker`
- Wait for Docker to fully start (you'll see the Docker icon in your system tray/menu bar)
- Then retry: `docker compose up --build`

**Services not starting properly:**

```bash
docker compose down
docker compose up --build
```

**Ollama model download issues:**

- The first startup may take 10-20 minutes to download the Llama 3.3:70b model (it's a larger model)
- Check logs: `docker compose logs ollama-init`

**504 Gateway Timeout errors:**

- This is normal for the first few LLM requests as the model loads
- Subsequent requests should be faster

**Port conflicts:**

```bash
# Check what's using the ports
lsof -i :3000
lsof -i :5002
lsof -i :11434
```

### Manual Setup Issues

**Ollama connection errors:**

- Ensure Ollama is running: `ollama serve`
- Verify model is available: `ollama list`
- Check if model is loaded: `ollama show llama3.3:70b-instruct-q2_K`
