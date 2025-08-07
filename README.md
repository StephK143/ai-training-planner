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

### Prerequisites

- Node.js
- Python 3.8+
- [Ollama](https://ollama.ai) installed locally
- Flask (`pip install flask`)

### Setup and Installation

1. Clone the repository:

```bash
git clone https://github.com/StephK143/ai-training-planner.git
cd ai-training-planner
```

2. Install dependencies:

```bash
npm install
```

3. Pull the Llama2 model:

```bash
ollama pull llama2
```

4. Start Ollama service:

```bash
ollama serve
```

5. Start the Flask backend server:

```bash
python server.py
```

6. Start the frontend development server:

```bash
npm run dev
```

The frontend will be available at [http://localhost:5174](http://localhost:5174)
The backend API will be running at [http://localhost:5002](http://localhost:5002)

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

- React + TypeScript
- Material-UI components
- Ollama for LLM integration
- Local state management
- Custom hooks for data handling
