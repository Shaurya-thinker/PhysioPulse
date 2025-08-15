import React, { useState, useEffect } from 'react';
import { Link, useLocation } from 'react-router-dom';
import { useTranslation } from 'react-i18next';
import {
  Dashboard as DashboardIcon,
  People as PeopleIcon,
  Assessment as AssessmentIcon,
  Storage as StorageIcon,
  Settings as SettingsIcon,
  Language as LanguageIcon,
  LightMode as LightModeIcon,
  DarkMode as DarkModeIcon
} from '@mui/icons-material';
import './Sidebar.css';
import { ColorThemeService } from '../services/colorThemeService';

export default function Sidebar() {
  const { t, i18n } = useTranslation();
  const location = useLocation();
  const [activeItem, setActiveItem] = useState(location.pathname);
  const [isCollapsed, setIsCollapsed] = useState(false);
  const [isDarkMode, setIsDarkMode] = useState(false);

  useEffect(() => {
    setActiveItem(location.pathname);
  }, [location.pathname]);

  useEffect(() => {
    // Check if dark mode is already enabled
    const darkMode = document.body.classList.contains('dark-theme');
    setIsDarkMode(darkMode);
  }, []);

  // Initialize color theme on component mount
  useEffect(() => {
    ColorThemeService.initializeTheme();
  }, []);

  const changeLang = (lang) => {
    i18n.changeLanguage(lang);
  };

  const toggleTheme = () => {
    const newDarkMode = !isDarkMode;
    setIsDarkMode(newDarkMode);
    
    if (newDarkMode) {
      document.body.classList.add('dark-theme');
      localStorage.setItem('theme', 'dark');
    } else {
      document.body.classList.remove('dark-theme');
      localStorage.setItem('theme', 'light');
    }
  };

  const menuItems = [
    { path: '/', icon: <DashboardIcon />, label: t('dashboard_title') || 'Dashboard' },
    { path: '/patients', icon: <PeopleIcon />, label: t('patients') || 'Patients' },
    { path: '/reports', icon: <AssessmentIcon />, label: t('reports') || 'Reports' },
    { path: '/database', icon: <StorageIcon />, label: t('database') || 'Database' },
    { path: '/settings', icon: <SettingsIcon />, label: t('settings') || 'Settings' },
  ];

  const languages = [
    { code: 'en', label: 'EN', name: 'English' },
    { code: 'pa', label: 'ਪੰ', name: 'ਪੰਜਾਬੀ' },
    { code: 'hi', label: 'हि', name: 'हिंदी' }
  ];

  return (
    <aside className={`sidebar ${isCollapsed ? 'sidebar-collapsed' : ''}`}>
      <div className="sidebar-header">
        <div className="sidebar-logo">
          <div className="sidebar-logo-icon">
            <DashboardIcon />
          </div>
          {!isCollapsed && (
            <h2 className="sidebar-title">NGO Dashboard</h2>
          )}
        </div>
      </div>

      <nav className="sidebar-nav">
        {menuItems.map((item) => (
          <Link
            key={item.path}
            to={item.path}
            className={`sidebar-nav-item ${activeItem === item.path ? 'active' : ''}`}
            onClick={() => setActiveItem(item.path)}
          >
            <div className="sidebar-nav-icon">
              {item.icon}
            </div>
            {!isCollapsed && (
              <span className="sidebar-nav-label">{item.label}</span>
            )}
            {activeItem === item.path && <div className="sidebar-nav-indicator" />}
          </Link>
        ))}
      </nav>

      <div className="sidebar-footer">
    
        {/* Language Selector */}
        <div className="sidebar-section">
          {!isCollapsed && (
            <h3 className="sidebar-section-title">
              <LanguageIcon className="sidebar-section-icon" />
              Language
            </h3>
          )}
          <div className={`sidebar-lang-grid ${isCollapsed ? 'collapsed' : ''}`}>
            {languages.map((lang) => (
              <button
                key={lang.code}
                onClick={() => changeLang(lang.code)}
                className={`sidebar-lang-btn ${i18n.language === lang.code ? 'active' : ''}`}
                title={isCollapsed ? lang.name : ''}
              >
                {lang.label}
              </button>
            ))}
          </div>
        </div>
      </div>
    </aside>
  );
}