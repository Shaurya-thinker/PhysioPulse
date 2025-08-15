import { useTranslation } from 'react-i18next';

export default function LanguageSwitcher() {
  const { i18n } = useTranslation();

  return (
    <div className="mb-4">
      <button onClick={() => i18n.changeLanguage('en')} className="mr-2">EN</button>
      <button onClick={() => i18n.changeLanguage('hi')}>हिंदी</button>
      <button onClick={() => i18n.changeLanguage('pa')} className="ml-2">ਪੰਜਾਬੀ</button>
    </div>
  );
}