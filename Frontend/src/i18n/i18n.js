import i18n from 'i18next';
import { initReactI18next } from 'react-i18next';
import LanguageDetector from 'i18next-browser-languagedetector';

import en from './en.json';
import pa from './pa.json';
import hi from './hi.json';

// Get saved language preference or default to 'en'
const savedLanguage = localStorage.getItem('language') || 'en';

i18n
  .use(LanguageDetector)
  .use(initReactI18next) 
  .init({
    resources: {
      en: { translation: en },
      hi: { translation: hi },
      pa: { translation: pa }
    },
    lng: savedLanguage, // Use saved language preference
    fallbackLng: 'en',
    detection: {
      // Override browser detection with saved preference
      order: ['localStorage', 'navigator', 'htmlTag'],
      lookupLocalStorage: 'language',
      caches: ['localStorage']
    },
    interpolation: { escapeValue: false }
  });

export default i18n;