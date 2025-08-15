import React, { useState, useEffect } from 'react';
import { useTranslation } from 'react-i18next';
import {
  Box,
  Container,
  Typography,
  Paper,
  Grid,
  Card,
  CardContent,
  FormControl,
  InputLabel,
  Select,
  MenuItem,
  Switch,
  FormControlLabel,
  Divider,
  Alert,
  Snackbar,
  Button,
} from '@mui/material';
import {
  Language as LanguageIcon,
  Palette as PaletteIcon,
  Save as SaveIcon,
  Restore as RestoreIcon,
  Settings as SettingsIcon,
} from '@mui/icons-material';
import './Settings.css';
import { ColorThemeService, COLOR_THEMES } from '../services/colorThemeService';

export default function Settings() {
  const { t, i18n } = useTranslation();
  const [language, setLanguage] = useState(i18n.language || 'en');
  const [theme, setTheme] = useState(() => {
    return localStorage.getItem('theme') || 'light';
  });
  const [colorTheme, setColorTheme] = useState(() => {
    return ColorThemeService.getCurrentTheme();
  });
  const [showSaveAlert, setShowSaveAlert] = useState(false);

  useEffect(() => {
    // Apply color theme using service
    ColorThemeService.applyColorTheme(colorTheme);
  }, [colorTheme]);

  useEffect(() => {
    // No need to apply theme here - it's handled globally by App component
    // Theme application is now centralized in App.jsx
  }, [theme]);

  useEffect(() => {
    // Initialize color theme on component mount
    const savedColorTheme = ColorThemeService.initializeTheme();
    setColorTheme(savedColorTheme);
  }, []);

  const handleLanguageChange = (event) => {
    const newLanguage = event.target.value;
    setLanguage(newLanguage);
    i18n.changeLanguage(newLanguage);
    localStorage.setItem('language', newLanguage);
  };

  const handleThemeChange = (event) => {
    const newTheme = event.target.checked ? 'dark' : 'light';
    setTheme(newTheme);
    localStorage.setItem('theme', newTheme);
  };

  const handleColorThemeChange = (event) => {
    const newColorTheme = event.target.value;
    setColorTheme(newColorTheme);
    ColorThemeService.setCurrentTheme(newColorTheme);
  };

  const handleSaveSettings = () => {
    setShowSaveAlert(true);
  };

  const handleResetSettings = () => {
    setLanguage('en');
    setTheme('light');
    setColorTheme('blue');
    i18n.changeLanguage('en');
    localStorage.removeItem('language');
    localStorage.removeItem('theme');
    ColorThemeService.setCurrentTheme('blue');
    setShowSaveAlert(true);
  };

  const languages = [
    { code: 'en', name: 'English', flag: '🇺🇸' },
    { code: 'hi', name: 'हिन्दी', flag: '🇮🇳' },
    { code: 'pa', name: 'ਪੰਜਾਬੀ', flag: '🇮🇳' },
  ];

  return (
    <div className="settings-container">
      <Container maxWidth="xl">
        {/* Header Section */}
        <Paper className="settings-header-card">
          <div className="settings-header-content">
            <div className="settings-header-info">
              <SettingsIcon className="settings-header-icon" />
              <div>
                <Typography variant="h4" component="h1" className="settings-title">
                  {t('settings.title') || 'Settings'}
                </Typography>
                <Typography variant="body1" className="settings-subtitle">
                  {t('settings.subtitle') || 'Customize your dashboard experience with language and theme preferences'}
                </Typography>
              </div>
            </div>
          </div>
        </Paper>

        {/* Settings Content */}
        <div className="settings-content-section">
          <Grid container spacing={3}>
            {/* Language Settings */}
            <Grid item xs={12} md={4}>
              <Paper className="settings-section-card">
                <div className="settings-section-header">
                  <LanguageIcon className="settings-section-icon" />
                  <Typography variant="h6" className="settings-section-title">
                    {t('settings.language.title') || 'Language Settings'}
                  </Typography>
                </div>
                
                <Typography variant="body2" className="settings-section-description">
                  {t('settings.language.description') || 'Choose your preferred language for the dashboard interface'}
                </Typography>

                <FormControl fullWidth className="settings-form-control">
                  <InputLabel className="settings-input-label">
                    {t('settings.language.selectLabel') || 'Select Language'}
                  </InputLabel>
                  <Select
                    value={language}
                    onChange={handleLanguageChange}
                    label={t('settings.language.selectLabel') || 'Select Language'}
                    className="settings-select"
                    size="medium"
                  >
                    {languages.map((lang) => (
                      <MenuItem 
                        key={lang.code} 
                        value={lang.code}
                        className="settings-menu-item"
                      >
                        <Box sx={{ display: 'flex', alignItems: 'center', gap: 1.5 }}>
                          <span className="settings-flag">{lang.flag}</span>
                          <span className="settings-lang-name">{lang.name}</span>
                        </Box>
                      </MenuItem>
                    ))}
                  </Select>
                </FormControl>

                <Alert severity="info" className="settings-info-alert">
                  {t('settings.language.info') || 'Language changes will be applied immediately across the entire dashboard'}
                </Alert>
              </Paper>
            </Grid>

            {/* Theme Settings */}
            <Grid item xs={12} md={4}>
              <Paper className="settings-section-card">
                <div className="settings-section-header">
                  <PaletteIcon className="settings-section-icon" />
                  <Typography variant="h6" className="settings-section-title">
                    {t('settings.theme.title') || 'Theme Settings'}
                  </Typography>
                </div>

                <Typography variant="body2" className="settings-section-description">
                  {t('settings.theme.description') || 'Switch between light and dark themes for better visual comfort'}
                </Typography>

                <div className="settings-theme-control">
                  <FormControlLabel
                    control={
                      <Switch
                        checked={theme === 'dark'}
                        onChange={handleThemeChange}
                        color="primary"
                        className="settings-theme-switch"
                      />
                    }
                    label={
                      <Typography className="settings-theme-label">
                        {theme === 'dark' 
                          ? (t('settings.theme.dark') || '🌙 Dark Theme')
                          : (t('settings.theme.light') || '☀️ Light Theme')
                        }
                      </Typography>
                    }
                    className="settings-switch-label"
                  />
                </div>

                <div className="settings-theme-preview">
                  <Typography variant="body2" className="settings-preview-label">
                    {t('settings.theme.preview') || 'Current Theme:'}
                  </Typography>
                  <div className="settings-preview-indicator">
                    <div className={`settings-preview-dot ${theme}`}></div>
                    <Typography variant="caption" className="settings-preview-text">
                      {theme === 'dark' 
                        ? (t('settings.theme.darkMode') || 'Dark Mode Active')
                        : (t('settings.theme.lightMode') || 'Light Mode Active')
                      }
                    </Typography>
                  </div>
                </div>

                <Alert severity="success" className="settings-success-alert">
                  {t('settings.theme.info') || 'Theme preference will be saved automatically and persist across sessions'}
                </Alert>
              </Paper>
            </Grid>

            {/* Color Theme Settings */}
            <Grid item xs={12} md={4}>
              <Paper className="settings-section-card">
                <div className="settings-section-header">
                  <PaletteIcon className="settings-section-icon" />
                  <Typography variant="h6" className="settings-section-title">
                    {t('settings.colorTheme.title') || 'Color Theme'}
                  </Typography>
                </div>

                <Typography variant="body2" className="settings-section-description">
                  {t('settings.colorTheme.description') || 'Choose your preferred color scheme for the application'}
                </Typography>

                <FormControl fullWidth className="settings-form-control">
                  <InputLabel className="settings-input-label">
                    {t('settings.colorTheme.selectLabel') || 'Select Color Theme'}
                  </InputLabel>
                  <Select
                    value={colorTheme}
                    onChange={handleColorThemeChange}
                    label={t('settings.colorTheme.selectLabel') || 'Select Color Theme'}
                    className="settings-select"
                    size="medium"
                  >
                    <MenuItem value="blue" className="settings-menu-item">
                      <Box sx={{ display: 'flex', alignItems: 'center', gap: 1.5 }}>
                        <div className="settings-color-dot blue-theme"></div>
                        <span className="settings-theme-name">
                          {t('settings.colorTheme.blue') || '🔵 Blue Theme (Default)'}
                        </span>
                      </Box>
                    </MenuItem>
                    <MenuItem value="orange" className="settings-menu-item">
                      <Box sx={{ display: 'flex', alignItems: 'center', gap: 1.5 }}>
                        <div className="settings-color-dot orange-theme"></div>
                        <span className="settings-theme-name">
                          {t('settings.colorTheme.orange') || '🟠 Orange Theme'}
                        </span>
                      </Box>
                    </MenuItem>
                  </Select>
                </FormControl>

                <div className="settings-color-preview">
                  <Typography variant="body2" className="settings-preview-label">
                    {t('settings.colorTheme.preview') || 'Current Colors:'}
                  </Typography>
                  <div className="settings-color-palette">
                    <div className={`settings-color-sample primary ${colorTheme}`}></div>
                    <div className={`settings-color-sample accent ${colorTheme}`}></div>
                    <div className={`settings-color-sample light ${colorTheme}`}></div>
                  </div>
                </div>

                <Alert severity="info" className="settings-info-alert">
                  {t('settings.colorTheme.info') || 'Color theme changes will be applied immediately across the entire application'}
                </Alert>
              </Paper>
            </Grid>
          </Grid>
        </div>

        {/* Actions Section */}
        <Paper className="settings-actions-card">
          <div className="settings-actions-header">
            <Typography variant="h6" className="settings-actions-title">
              {t('settings.actions.title') || 'Actions'}
            </Typography>
          </div>
          <div className="settings-actions-buttons">
            <Button
              variant="contained"
              startIcon={<SaveIcon />}
              onClick={handleSaveSettings}
              className="settings-save-button"
              size="medium"
            >
              {t('settings.actions.save') || 'Save Settings'}
            </Button>
            <Button
              variant="outlined"
              startIcon={<RestoreIcon />}
              onClick={handleResetSettings}
              className="settings-reset-button"
              size="medium"
            >
              {t('settings.actions.reset') || 'Reset to Default'}
            </Button>
          </div>
        </Paper>

        {/* Success Snackbar */}
        <Snackbar
          open={showSaveAlert}
          autoHideDuration={4000}
          onClose={() => setShowSaveAlert(false)}
          anchorOrigin={{ vertical: 'bottom', horizontal: 'right' }}
        >
          <Alert 
            onClose={() => setShowSaveAlert(false)} 
            severity="success"
            className="settings-snackbar-alert"
            variant="filled"
          >
            {t('settings.messages.saveSuccess') || 'Settings saved successfully!'}
          </Alert>
        </Snackbar>
      </Container>
    </div>
  );
}