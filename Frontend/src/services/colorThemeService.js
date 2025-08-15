// Color Theme Service
// This service manages the global color theme across the application

export const COLOR_THEMES = {
  BLUE: 'blue',
  ORANGE: 'orange'
};

export const THEME_COLORS = {
  [COLOR_THEMES.BLUE]: {
    primary: '#667eea',
    primaryDark: '#5a67d8',
    primaryLight: '#7c3aed',
    accent: '#8b5cf6',
    rgb: '102, 126, 234'
  },
  [COLOR_THEMES.ORANGE]: {
    primary: '#ff6b35',
    primaryDark: '#e55a2b',
    primaryLight: '#ff8659',
    accent: '#ff8f65',
    rgb: '255, 107, 53'
  }
};

export class ColorThemeService {
  static applyColorTheme(theme = COLOR_THEMES.BLUE) {
    const root = document.documentElement;
    const colors = THEME_COLORS[theme] || THEME_COLORS[COLOR_THEMES.BLUE];
    
    root.style.setProperty('--primary-color', colors.primary);
    root.style.setProperty('--primary-dark', colors.primaryDark);
    root.style.setProperty('--primary-light', colors.primaryLight);
    root.style.setProperty('--accent-color', colors.accent);
    root.style.setProperty('--primary-color-rgb', colors.rgb);
  }

  static getCurrentTheme() {
    return localStorage.getItem('colorTheme') || COLOR_THEMES.BLUE;
  }

  static setCurrentTheme(theme) {
    if (Object.values(COLOR_THEMES).includes(theme)) {
      localStorage.setItem('colorTheme', theme);
      this.applyColorTheme(theme);
      return true;
    }
    return false;
  }

  static initializeTheme() {
    const savedTheme = this.getCurrentTheme();
    this.applyColorTheme(savedTheme);
    return savedTheme;
  }

  static resetToDefault() {
    localStorage.removeItem('colorTheme');
    this.applyColorTheme(COLOR_THEMES.BLUE);
  }
}

// Export for direct use
export const applyColorTheme = ColorThemeService.applyColorTheme;
export const getCurrentColorTheme = ColorThemeService.getCurrentTheme;
export const setColorTheme = ColorThemeService.setCurrentTheme;
export const initializeColorTheme = ColorThemeService.initializeTheme;
