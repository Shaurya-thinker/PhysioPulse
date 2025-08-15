import React, { useState, useEffect } from 'react';
import { BrowserRouter as Router, Routes, Route } from 'react-router-dom';
import { ThemeProvider, createTheme } from '@mui/material/styles';
import { CssBaseline, Box } from '@mui/material';

import Sidebar from './components/Sidebar.jsx';
import Dashboard from './pages/Dashboard.jsx';
import Patients from './pages/Patients.jsx';
import Reports from './pages/Reports.jsx';
import Settings from './pages/Settings.jsx';
import DatabaseManagement from './pages/DatabaseManagement.jsx';
import { ColorThemeService } from './services/colorThemeService';

export default function App() {
  const [darkMode, setDarkMode] = useState(() => {
    const savedTheme = localStorage.getItem('theme') === 'dark';
    // Apply theme immediately to prevent flash
    document.body.className = savedTheme ? 'dark-theme' : 'light-theme';
    return savedTheme;
  });

  useEffect(() => {
    // Apply theme to body class immediately on mount
    document.body.className = darkMode ? 'dark-theme' : 'light-theme';
    
    // Initialize color theme
    ColorThemeService.initializeTheme();
    
    // Apply theme colors to root CSS variables
    const root = document.documentElement;
    if (darkMode) {
      root.style.setProperty('--bg-primary', '#121212');
      root.style.setProperty('--bg-secondary', '#1e1e1e');
      root.style.setProperty('--text-primary', '#ffffff');
      root.style.setProperty('--text-secondary', '#b3b3b3');
    } else {
      root.style.setProperty('--bg-primary', '#ffffff');
      root.style.setProperty('--bg-secondary', '#f5f5f5');
      root.style.setProperty('--text-primary', '#000000');
      root.style.setProperty('--text-secondary', '#666666');
    }

    const handleStorageChange = () => {
      const newTheme = localStorage.getItem('theme') === 'dark';
      setDarkMode(newTheme);
    };

    // Listen for storage changes from other tabs/windows
    window.addEventListener('storage', handleStorageChange);
    
    // Also listen for theme changes within the same tab
    const interval = setInterval(() => {
      const currentTheme = localStorage.getItem('theme') === 'dark';
      if (currentTheme !== darkMode) {
        setDarkMode(currentTheme);
      }
    }, 100);

    return () => {
      window.removeEventListener('storage', handleStorageChange);
      clearInterval(interval);
    };
  }, [darkMode]);

  // Update theme whenever darkMode changes
  useEffect(() => {
    document.body.className = darkMode ? 'dark-theme' : 'light-theme';
    
    const root = document.documentElement;
    if (darkMode) {
      root.style.setProperty('--bg-primary', '#121212');
      root.style.setProperty('--bg-secondary', '#1e1e1e');
      root.style.setProperty('--text-primary', '#ffffff');
      root.style.setProperty('--text-secondary', '#b3b3b3');
    } else {
      root.style.setProperty('--bg-primary', '#ffffff');
      root.style.setProperty('--bg-secondary', '#f5f5f5');
      root.style.setProperty('--text-primary', '#000000');
      root.style.setProperty('--text-secondary', '#666666');
    }
  }, [darkMode]);

  const theme = createTheme({
    palette: {
      mode: darkMode ? 'dark' : 'light',
      primary: {
        main: '#1976d2',
      },
      background: {
        default: darkMode ? '#121212' : '#f5f5f5',
        paper: darkMode ? '#1e1e1e' : '#ffffff',
      },
      text: {
        primary: darkMode ? '#ffffff' : '#000000',
        secondary: darkMode ? '#b3b3b3' : '#666666',
      },
    },
    typography: {
      fontFamily: 'Roboto, Arial, sans-serif',
    },
    components: {
      MuiButton: {
        styleOverrides: {
          root: {
            textTransform: 'none',
          },
        },
      },
      MuiDrawer: {
        styleOverrides: {
          paper: {
            backgroundColor: darkMode ? '#1e1e1e' : '#ffffff',
            borderRight: `1px solid ${darkMode ? '#333' : 'rgba(0, 0, 0, 0.12)'}`,
          },
        },
      },
    },
  });

  return (
    <ThemeProvider theme={theme}>
      <CssBaseline />
      <Router>
        <Box sx={{ display: 'flex', minHeight: '100vh' }}>
          <Sidebar />
          <Box
            component="main"
            className="main-content"
            sx={{
              flexGrow: 1,
              marginLeft: '280px', // Match sidebar width
              bgcolor: 'background.default',
              transition: 'margin-left 0.4s cubic-bezier(0.23, 1, 0.320, 1)',
              minHeight: '100vh',
            }}
          >
            <Routes>
              <Route path="/" element={<Dashboard />} />
              <Route path="/patients" element={<Patients />} />
              <Route path="/database" element={<DatabaseManagement />} />
              <Route path="/reports" element={<Reports />} />
              <Route path="/settings" element={<Settings />} />
            </Routes>
          </Box>
        </Box>
      </Router>
    </ThemeProvider>
  );
}
