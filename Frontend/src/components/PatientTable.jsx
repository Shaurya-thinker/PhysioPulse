import React from 'react';
import { useTranslation } from 'react-i18next';

const PatientTable = () => {
  const { t } = useTranslation();
  const patients = [
    { id: 1, name: 'Amit Sharma', age: 35, gender: 'Male', diagnosis: 'Stroke' },
    { id: 2, name: 'Suman Kaur', age: 29, gender: 'Female', diagnosis: 'Spinal Injury' },
    { id: 3, name: 'Raj Patel', age: 45, gender: 'Male', diagnosis: 'Fracture' }
  ];

  return (
    <div className="overflow-x-auto shadow rounded-lg mt-6">
      <table className="min-w-full bg-white border border-gray-200">
        <thead className="bg-gray-100 text-gray-700 text-left">
          <tr>
            <th className="px-4 py-2">{t('table.name')}</th>
            <th className="px-4 py-2">{t('table.age')}</th>
            <th className="px-4 py-2">{t('table.gender')}</th>
            <th className="px-4 py-2">{t('table.diagnosis')}</th>
            <th className="px-4 py-2">{t('table.actions')}</th>
          </tr>
        </thead>
        <tbody>
          {patients.map((patient) => (
            <tr key={patient.id} className="border-t border-gray-200 hover:bg-gray-50">
              <td className="px-4 py-2">{patient.name}</td>
              <td className="px-4 py-2">{patient.age}</td>
              <td className="px-4 py-2">{patient.gender}</td>
              <td className="px-4 py-2">{patient.diagnosis}</td>
              <td className="px-4 py-2">
                <button className="text-blue-600 hover:underline">
                  {t('table.actions')}
                </button>
              </td>
            </tr>
          ))}
        </tbody>
      </table>
    </div>
  );
};

export default PatientTable;