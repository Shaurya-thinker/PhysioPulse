# 🏥 PhysioPulse - AI-Powered Telerehabilitation Platform

<div align="center">
  
  [![Python](https://img.shields.io/badge/Python-3.9+-blue.svg)](https://python.org)
  [![React](https://img.shields.io/badge/React-19.1+-61DAFB.svg)](https://reactjs.org)
  [![FastAPI](https://img.shields.io/badge/FastAPI-0.104+-green.svg)](https://fastapi.tiangolo.com)
  [![Material-UI](https://img.shields.io/badge/Material--UI-7.3+-0081CB.svg)](https://mui.com)
  [![License](https://img.shields.io/badge/License-MIT-yellow.svg)](LICENSE)

  **PhysioPulse** is a comprehensive AI-powered telerehabilitation platform that combines cutting-edge pose detection technology with an intuitive patient management system. It enables healthcare providers to deliver remote physiotherapy services with real-time exercise tracking, automated scoring, and detailed progress monitoring.

  [🚀 Live Demo](#-live-demo) • [📖 Documentation](#-documentation) • [🛠️ Installation](#️-installation) • [💻 Usage](#-usage)

</div>

---

## ✨ Key Features

### 🎯 Core Capabilities
- **Real-time Pose Detection** - MediaPipe-powered body landmark tracking
- **Intelligent Exercise Scoring** - AI-driven form assessment and feedback
- **Multi-language Support** - English, Hindi, and Punjabi interfaces
- **Patient Management** - Comprehensive patient data and progress tracking
- **Dark/Light Themes** - Customizable user interface
- **Responsive Design** - Seamless experience across all devices

### 🏃‍♂️ Supported Exercises
- **Arm Extension** - Elbow angle analysis and form correction
- **Squats** - Knee angle tracking and depth assessment
- **Shoulder Press** - Range of motion and movement quality evaluation

### 📊 Dashboard Features
- Real-time patient statistics
- Exercise completion tracking
- Progress visualization charts
- Report generation and export
- Database management tools

---

## 🏗️ Project Architecture

```
PhysioPulse/
├── 🎨 Frontend/                     # React Dashboard & UI
│   ├── 📦 src/
│   │   ├── 🧩 components/          # Reusable UI components
│   │   ├── 📄 pages/               # Main application pages
│   │   ├── 🌐 i18n/                # Internationalization
│   │   └── 🔧 services/            # API & utility services
│   ├── 📋 package.json             # Dependencies & scripts
│   └── ⚙️ vite.config.js           # Build configuration
│
└── 🚀 telerehab-ai-backend/        # Python AI Backend
    ├── 📦 src/
    │   ├── 🔌 api.py               # FastAPI application
    │   ├── 🎯 pose_detector.py     # MediaPipe pose detection
    │   ├── 📊 pose_scorer.py       # Exercise scoring engine
    │   ├── 🎬 video_analyzer.py    # Video processing pipeline
    │   └── 📋 models.py            # Data models
    ├── 📋 requirements.txt         # Python dependencies
    └── 🐳 Dockerfile              # Container configuration
```

---

## 🛠️ Installation

### Prerequisites
- **Node.js** 18+ and npm/yarn
- **Python** 3.9+
- **Git**

### 🚀 Quick Start

1. **Clone the repository**
   ```bash
   git clone https://github.com/DevRanbir/PhysioPulse.git
   cd PhysioPulse
   ```

2. **Setup Backend (AI Engine)**
   ```bash
   cd telerehab-ai-backend
   
   # Create virtual environment
   python -m venv venv
   venv\Scripts\activate  # Windows
   # source venv/bin/activate  # macOS/Linux
   
   # Install dependencies
   pip install -r requirements.txt
   
   # Start the API server
   python run.py
   ```
   
   The backend will be available at: `http://localhost:8000`
   API Documentation: `http://localhost:8000/docs`

3. **Setup Frontend (Dashboard)**
   ```bash
   cd Frontend
   
   # Install dependencies
   npm install
   
   # Start development server
   npm start
   ```
   
   The frontend will be available at: `http://localhost:3000`

### 🐳 Docker Deployment

```bash
# Backend
cd telerehab-ai-backend
docker-compose up -d

# Frontend (build for production)
cd Frontend
npm run build
npm run deploy  # Deploy to GitHub Pages
```

---

## 💻 Usage

### 🏥 For Healthcare Providers

1. **Patient Management**
   - Add new patients with detailed profiles
   - Track exercise assignments and progress
   - Generate comprehensive reports

2. **Exercise Monitoring**
   - Upload patient exercise videos
   - Review AI-generated scores and feedback
   - Monitor real-time exercise sessions

3. **Progress Analysis**
   - View detailed analytics and trends
   - Export patient reports
   - Customize treatment plans

### 🎯 For Developers

#### Backend API Usage
```python
import requests

# Analyze exercise video
response = requests.post(
    "http://localhost:8000/analyze-video",
    files={"video": open("exercise.mp4", "rb")},
    data={"exercise_type": "squat"}
)

result = response.json()
print(f"Score: {result['score']}")
print(f"Feedback: {result['feedback']}")
```

#### Frontend Integration
```javascript
import { PatientService } from './services/patientService';

// Fetch patient data
const patients = await PatientService.getAllPatients();

// Add new patient
const newPatient = await PatientService.addPatient({
  name: "John Doe",
  age: 45,
  condition: "Knee rehabilitation"
});
```

---

## 🌐 API Documentation

### Core Endpoints

| Method | Endpoint | Description |
|--------|----------|-------------|
| `POST` | `/analyze-video` | Analyze exercise video and return score |
| `GET` | `/exercises` | Get list of supported exercises |
| `POST` | `/patients` | Create new patient record |
| `GET` | `/patients/{id}/progress` | Get patient progress data |
| `GET` | `/health` | Health check endpoint |

### Example API Calls

```bash
# Health check
curl http://localhost:8000/health

# Analyze exercise video
curl -X POST "http://localhost:8000/analyze-video" \
  -F "video=@exercise.mp4" \
  -F "exercise_type=squat"

# Get exercise list
curl http://localhost:8000/exercises
```

---

## 🧪 Testing

### Backend Tests
```bash
cd telerehab-ai-backend
pytest tests/ -v --cov=src
```

### Frontend Tests
```bash
cd Frontend
npm test
```

---

## 🌍 Internationalization

PhysioPulse supports multiple languages:

- **English** (en) - Default
- **Hindi** (hi) - हिन्दी
- **Punjabi** (pa) - ਪੰਜਾਬੀ

Add new languages by creating translation files in `Frontend/src/i18n/locales/`.

---

## 📁 Key Files & Configuration

### Frontend Configuration
- `Frontend/src/App.jsx` - Main application component
- `Frontend/src/i18n/i18n.js` - Internationalization setup
- `Frontend/src/services/` - API integration services
- `Frontend/package.json` - Dependencies and build scripts

### Backend Configuration
- `telerehab-ai-backend/src/config.py` - Server configuration
- `telerehab-ai-backend/requirements.txt` - Python dependencies
- `telerehab-ai-backend/run.py` - Server startup script
- `telerehab-ai-backend/Dockerfile` - Container configuration

---

## 🤝 Contributing

We welcome contributions! Please follow these steps:

1. Fork the repository
2. Create a feature branch (`git checkout -b feature/amazing-feature`)
3. Commit your changes (`git commit -m 'Add amazing feature'`)
4. Push to the branch (`git push origin feature/amazing-feature`)
5. Open a Pull Request

### Development Guidelines
- Follow Python PEP 8 style guide for backend code
- Use ESLint rules for frontend JavaScript/React code
- Write tests for new features
- Update documentation as needed

---

## 📄 License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.

---

## 🆘 Support & Documentation

- **GitHub Issues**: [Report bugs or request features](https://github.com/DevRanbir/PhysioPulse/issues)
- **API Docs**: Available at `http://localhost:8000/docs` when running locally
- **Wiki**: [Detailed documentation and guides](https://github.com/DevRanbir/PhysioPulse/wiki)

---

<div align="center">

**Built with ❤️ by the PhysioPulse Team**

[⬆ Back to Top](#-physiopulse---ai-powered-telerehabilitation-platform)

</div>
