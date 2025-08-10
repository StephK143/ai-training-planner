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

3. Wait for all services to start (this may take a few minutes on first run as it downloads the Llama2 model)

4. Access the application:
   - **Frontend**: [http://localhost:3000](http://localhost:3000)
   - **Backend API**: [http://localhost:5002](http://localhost:5002)
   - **Ollama API**: [http://localhost:11434](http://localhost:11434)

#### Docker Services

The Docker setup includes:
- **Frontend**: React app served by Nginx with optimized timeout settings for LLM requests
- **Backend**: Python Flask API server with AI integration
- **Ollama**: Local LLM service with Llama2 model automatically downloaded
- **Ollama Init**: One-time service that ensures the Llama2 model is available

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

4. Pull the Llama2 model:
```bash
ollama pull llama2
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

This project uses Llama 2 through Ollama for several key reasons:

1. **Local Processing**: All AI computations happen locally, ensuring data privacy and reducing latency.
2. **No API Costs**: Unlike cloud-based solutions, there are no ongoing API costs.
3. **Performance**: Llama 2 offers an excellent balance of performance and resource requirements.
4. **Open Source**: Being open source, it allows for greater customization and transparency.
5. **Active Community**: Strong community support and regular updates ensure long-term viability.

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
- **LLM**: Ollama with Llama2 model for local AI processing
- **Containerization**: Docker & Docker Compose for easy deployment
- **Web Server**: Nginx for production-ready frontend serving
- **State Management**: Local state management with custom hooks

## 🔧 Troubleshooting

### Docker Issues

**Services not starting properly:**
```bash
docker compose down
docker compose up --build
```

**Ollama model download issues:**
- The first startup may take 5-10 minutes to download the Llama2 model
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
- Check if model is loaded: `ollama show llama2`
