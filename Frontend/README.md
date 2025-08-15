# 🎨 PhysioPulse Frontend - Patient Dashboard & Management Interface

<div align="center">

[![React](https://img.shields.io/badge/React-19.1+-61DAFB.svg)](https://reactjs.org)
[![Material-UI](https://img.shields.io/badge/Material--UI-7.3+-0081CB.svg)](https://mui.com)
[![Vite](https://img.shields.io/badge/Vite-5.0+-646CFF.svg)](https://vitejs.dev)
[![i18next](https://img.shields.io/badge/i18next-23.15+-26A69A.svg)](https://www.i18next.com)
[![GitHub Pages](https://img.shields.io/badge/Deployed-GitHub%20Pages-blue.svg)](https://devranbir.github.io/ngo-frontend)

**Modern, responsive dashboard for PhysioPulse telerehabilitation platform**

Built with React 19, Material-UI, and multi-language support for healthcare providers

[🚀 Live Demo](https://devranbir.github.io/ngo-frontend) • [📱 Features](#-features) • [🛠️ Setup](#️-quick-setup) • [🌐 API Integration](#-api-integration)

</div>

---

## ✨ Features

### 🏥 Healthcare Dashboard
- **Patient Management** - Complete patient profiles and data tracking
- **Exercise Monitoring** - Real-time exercise session oversight
- **Progress Analytics** - Visual charts and progress tracking
- **Report Generation** - Comprehensive patient reports and exports
- **Database Management** - Patient data administration tools

### 🎨 User Experience
- **Dark/Light Themes** - Toggle between themes with smooth transitions
- **Responsive Design** - Seamless experience on desktop, tablet, and mobile
- **Multi-language Support** - English, Hindi (हिन्दी), and Punjabi (ਪੰਜਾਬੀ)
- **Material Design** - Modern, accessible UI components
- **Real-time Updates** - Live data synchronization

### 🔧 Technical Features
- **React 19** - Latest React with concurrent features
- **Material-UI v7** - Modern component library
- **React Router** - Client-side routing and navigation
- **i18next** - Internationalization framework
- **ESLint** - Code quality and consistency
- **Vite** - Fast development and optimized builds

---

## 🏗️ Project Structure

```
Frontend/
├── 📁 public/                       # Static assets
│   ├── index.html                  # Main HTML template
│   └── vite.svg                    # Vite logo
│
├── 📁 src/                         # Source code
│   ├── 📄 App.jsx                  # Main application component
│   ├── 📄 index.js                 # Application entry point
│   ├── 🎨 App.css                  # Global styles
│   ├── 🎨 index.css                # Base styles
│   ├── 🎨 theme.css                # Theme variables
│   │
│   ├── 📁 components/              # Reusable UI components
│   │   ├── Layout.jsx              # Main layout wrapper
│   │   ├── Sidebar.jsx             # Navigation sidebar
│   │   ├── PatientTable.jsx        # Patient data table
│   │   └── LanguageSwitcher.jsx    # Language selection
│   │
│   ├── 📁 pages/                   # Main application pages
│   │   ├── Dashboard.jsx           # Main dashboard
│   │   ├── Patients.jsx            # Patient management
│   │   ├── Reports.jsx             # Reports and analytics
│   │   ├── Settings.jsx            # Application settings
│   │   └── DatabaseManagement.jsx  # Data management
│   │
│   ├── 📁 services/                # API and utility services
│   │   ├── patientService.js       # Patient data operations
│   │   └── colorThemeService.js    # Theme management
│   │
│   ├── 📁 i18n/                    # Internationalization
│   │   ├── i18n.js                 # i18next configuration
│   │   ├── en.json                 # English translations
│   │   ├── hi.json                 # Hindi translations
│   │   ├── pa.json                 # Punjabi translations
│   │   └── 📁 locales/             # Organized translation files
│   │
│   └── 📁 assets/                  # Images and icons
│       └── react.svg               # React logo
│
├── 📋 package.json                 # Dependencies and scripts
├── ⚙️ vite.config.js               # Vite configuration
├── 🔧 eslint.config.js             # ESLint configuration
└── 📖 README.md                    # This file
```

---

## 🛠️ Quick Setup

### Prerequisites
- **Node.js** 18.0+ and npm/yarn
- **Git** for version control

### 🚀 Installation

1. **Clone & Navigate**
   ```bash
   git clone https://github.com/DevRanbir/PhysioPulse.git
   cd PhysioPulse/Frontend
   ```

2. **Install Dependencies**
   ```bash
   npm install
   # or
   yarn install
   ```

3. **Start Development Server**
   ```bash
   npm start
   # or
   yarn start
   ```
   
   Opens at: `http://localhost:3000`

4. **Build for Production**
   ```bash
   npm run build
   # or
   yarn build
   ```

### 🚀 Available Scripts

| Command | Description |
|---------|-------------|
| `npm start` | Start development server with hot reload |
| `npm run build` | Build optimized production bundle |
| `npm test` | Run test suite |
| `npm run lint` | Run ESLint for code quality |
| `npm run deploy` | Deploy to GitHub Pages |
| `npm run predeploy` | Pre-deployment build |

---

## 🌐 API Integration

### Backend Connection
The frontend connects to the PhysioPulse AI backend for real-time data:

```javascript
// Example: Patient service integration
import { PatientService } from './services/patientService';

// Fetch all patients
const patients = await PatientService.getAllPatients();

// Add new patient
const newPatient = await PatientService.addPatient({
  name: "Jane Doe",
  age: 32,
  condition: "Shoulder rehabilitation",
  assignedExercises: ["arm_extension", "shoulder_press"]
});

// Update patient progress
await PatientService.updateProgress(patientId, {
  exerciseId: "arm_extension",
  score: 85,
  completedDate: new Date()
});
```

### Real-time Updates
```javascript
// WebSocket connection for live exercise monitoring
const socket = new WebSocket('ws://localhost:8000/ws/exercises');

socket.onmessage = (event) => {
  const exerciseData = JSON.parse(event.data);
  updateDashboard(exerciseData);
};
```

---

## 🌍 Multi-language Support

### Supported Languages
- **English** (en) - Default language
- **Hindi** (hi) - हिन्दी भाषा समर्थन
- **Punjabi** (pa) - ਪੰਜਾਬੀ ਭਾਸ਼ਾ ਸਹਿਯੋਗ

### Usage Example
```javascript
import { useTranslation } from 'react-i18next';

function PatientCard() {
  const { t } = useTranslation();
  
  return (
    <Card>
      <CardContent>
        <Typography variant="h6">
          {t('patient.name')}
        </Typography>
        <Typography variant="body2">
          {t('patient.lastSession')}
        </Typography>
      </CardContent>
    </Card>
  );
}
```

### Adding New Languages
1. Create translation file: `src/i18n/locales/[language]/translation.json`
2. Add language to `src/i18n/i18n.js`
3. Update language switcher component

---

## 🎨 Theming & Customization

### Theme Switching
```javascript
import { ColorThemeService } from './services/colorThemeService';

// Toggle theme
const toggleTheme = () => {
  const newTheme = darkMode ? 'light' : 'dark';
  ColorThemeService.setTheme(newTheme);
  setDarkMode(!darkMode);
};
```

### Custom CSS Variables
```css
/* Light theme */
:root {
  --bg-primary: #ffffff;
  --bg-secondary: #f5f5f5;
  --text-primary: #000000;
  --text-secondary: #666666;
}

/* Dark theme */
.dark-theme {
  --bg-primary: #121212;
  --bg-secondary: #1e1e1e;
  --text-primary: #ffffff;
  --text-secondary: #b3b3b3;
}
```

---

## 📱 Responsive Design

### Breakpoints
- **Mobile**: < 768px
- **Tablet**: 768px - 1024px  
- **Desktop**: > 1024px

### Key Features
- Mobile-first design approach
- Collapsible sidebar navigation
- Responsive data tables
- Touch-friendly interface elements
- Optimized typography scaling

---

## 🧪 Testing

### Running Tests
```bash
# Run all tests
npm test

# Run tests in watch mode
npm test -- --watch

# Run tests with coverage
npm test -- --coverage
```

### Test Structure
```javascript
// Example component test
import { render, screen } from '@testing-library/react';
import PatientTable from '../components/PatientTable';

test('renders patient data correctly', () => {
  const mockPatients = [
    { id: 1, name: 'John Doe', age: 45 }
  ];
  
  render(<PatientTable patients={mockPatients} />);
  expect(screen.getByText('John Doe')).toBeInTheDocument();
});
```

---

## 🚀 Deployment

### GitHub Pages (Current)
```bash
npm run deploy
```
Automatically builds and deploys to: `https://devranbir.github.io/ngo-frontend`

### Manual Deployment
```bash
# Build production bundle
npm run build

# Deploy build folder to your hosting platform
# Build output is in: ./build/
```

### Environment Configuration
```bash
# .env file (for API endpoints)
REACT_APP_API_URL=http://localhost:8000
REACT_APP_WS_URL=ws://localhost:8000/ws
```

---

## 🛠️ Development

### Code Style
- **ESLint** configuration for consistent code quality
- **Prettier** integration for code formatting
- **React Hooks** best practices
- **Material-UI** design system guidelines

### Best Practices
- Component-based architecture
- Custom hooks for shared logic
- Proper error boundaries
- Accessibility (a11y) compliance
- Performance optimization with React.memo

### Adding New Features
1. Create component in appropriate directory
2. Add routing if needed (pages)
3. Update translations for all languages
4. Add tests for new functionality
5. Update this README if needed

---

## 🤝 Contributing

### Development Workflow
1. Fork the repository
2. Create feature branch: `git checkout -b feature/new-feature`
3. Make changes following code style
4. Add tests for new functionality
5. Update translations if UI text changes
6. Submit pull request

### Code Quality
- All components should be functional with hooks
- Use TypeScript for type safety (when migrating)
- Follow Material-UI design patterns
- Ensure responsive design
- Add proper error handling

---

## 📄 Dependencies

### Core Dependencies
```json
{
  "react": "^19.1.0",
  "react-dom": "^19.1.0",
  "react-router-dom": "^7.7.1",
  "@mui/material": "^7.3.1",
  "@mui/icons-material": "^7.3.1",
  "i18next": "^23.15.1",
  "react-i18next": "^15.6.1"
}
```

### Development Dependencies
```json
{
  "eslint": "^9.30.1",
  "react-scripts": "^5.0.1",
  "gh-pages": "^6.3.0",
  "typescript": "4.9.5"
}
```

---

## 🆘 Support

### Common Issues
- **Build fails**: Check Node.js version (18.0+ required)
- **Translations missing**: Verify all language files are updated
- **API connection**: Ensure backend is running on correct port
- **Deployment**: Check GitHub Pages settings and build output

### Getting Help
- **GitHub Issues**: [Report bugs or request features](https://github.com/DevRanbir/PhysioPulse/issues)
- **Documentation**: Check the main project README
- **Development**: Follow React and Material-UI documentation

---

<div align="center">

**PhysioPulse Frontend - Empowering Healthcare Through Technology** 

[⬆ Back to Top](#-physiopulse-frontend---patient-dashboard--management-interface)

</div>
