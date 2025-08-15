import React, { useState, useEffect } from 'react';
import { useTranslation } from 'react-i18next';
import {
  Box,
  Container,
  Typography,
} from '@mui/material';
import PeopleAltIcon from '@mui/icons-material/PeopleAlt';
import LocalHospitalIcon from '@mui/icons-material/LocalHospital';
import TrendingUpIcon from '@mui/icons-material/TrendingUp';
import AccessibilityNewIcon from '@mui/icons-material/AccessibilityNew';
import MonitorHeartIcon from '@mui/icons-material/MonitorHeart';
import CalendarTodayIcon from '@mui/icons-material/CalendarToday';
import PersonAddIcon from '@mui/icons-material/PersonAdd';
import HealingIcon from '@mui/icons-material/Healing';
import AssessmentIcon from '@mui/icons-material/Assessment';
import './Reports.css';
import { ColorThemeService } from '../services/colorThemeService';

const Reports = () => {
  const { t, i18n } = useTranslation();
  const [reportsData, setReportsData] = useState({
    totalPatients: 0,
    activeCases: 0,
    recoveryRate: 0,
    criticalCases: 0,
    appointmentsToday: 0,
    therapistsAvailable: 0,
    treatmentsCompleted: 0,
    patientSatisfaction: 0,
    recentActivities: []
  });

  // Get translated progress data
  const getProgressData = () => [
    { label: t('reportsPage.departmentOverview.patientRegistration'), value: 0, color: 'progress-patients' },
    { label: t('reportsPage.departmentOverview.recoveryProgress'), value: 0, color: 'progress-recovery' },
    { label: t('reportsPage.departmentOverview.treatmentCompletion'), value: 0, color: 'progress-treatment' },
    { label: t('reportsPage.departmentOverview.criticalCases'), value: 0, color: 'progress-critical' },
  ];

  useEffect(() => {
    // Try to fetch data from backend if available
    const fetchReportsData = async () => {
      try {
        // Replace with your actual backend API endpoint
        // const response = await fetch('/api/reports');
        // const data = await response.json();
        // setReportsData(data);
        
        // For now, keep showing zeros as no backend is connected
        console.log('No backend connected - showing zero values');
      } catch (error) {
        console.log('Backend not available - showing zero values');
      }
    };

    fetchReportsData();
  }, []);

  // Initialize color theme on component mount
  useEffect(() => {
    ColorThemeService.initializeTheme();
  }, []);

  const stats = [
    {
      title: t('reportsPage.stats.totalPatients'),
      value: reportsData.totalPatients.toString(),
      change: '0%',
      isPositive: true,
      icon: <PeopleAltIcon />,
    },
    {
      title: t('reportsPage.stats.activeCases'),
      value: reportsData.activeCases.toString(),
      change: '0%',
      isPositive: true,
      icon: <LocalHospitalIcon />,
    },
    {
      title: t('reportsPage.stats.recoveryRate'),
      value: `${reportsData.recoveryRate}%`,
      change: '0%',
      isPositive: true,
      icon: <TrendingUpIcon />,
    },
    {
      title: t('reportsPage.stats.criticalCases'),
      value: reportsData.criticalCases.toString(),
      change: '0%',
      isPositive: false,
      icon: <MonitorHeartIcon />,
    },
  ];

  return (
    <div className="reports-container">
      <Container maxWidth="xl">
        {/* Header Section */}
        <div className="reports-header">
          <div className="reports-header-content">
            <div className="reports-header-info">
              <AssessmentIcon className="reports-header-icon" />
              <div>
                <Typography variant="h4" component="h1" className="reports-title">
                  {t('reportsPage.title')}
                </Typography>
                <Typography variant="body1" className="reports-subtitle">
                  {t('reportsPage.subtitle')}
                </Typography>
              </div>
            </div>
          </div>
        </div>

        {/* Statistics Cards */}
        <div className="reports-stats-grid">
          {stats.map((stat, index) => (
            <div key={index} className="reports-stat-card">
              <div className="reports-stat-header">
                <div className="reports-stat-icon">
                  {stat.icon}
                </div>
                <div className={`reports-stat-change ${stat.isPositive ? 'positive' : 'negative'}`}>
                  {stat.change}
                  <span>{stat.isPositive ? '↗' : '↘'}</span>
                </div>
              </div>
              <Typography variant="h4" className="reports-stat-value">
                {stat.value}
              </Typography>
              <Typography variant="body2" className="reports-stat-title">
                {stat.title}
              </Typography>
            </div>
          ))}
        </div>

        {/* Charts and Activity Section */}
        <div className="reports-charts-grid">
          {/* Progress Overview */}
          <div className="reports-progress-card">
            <div className="reports-card-header">
              <TrendingUpIcon className="reports-card-icon" />
              <Typography variant="h6" className="reports-card-title">
                {t('reportsPage.departmentOverview.title')}
              </Typography>
            </div>
            {getProgressData().map((item, index) => (
              <div key={index} className="reports-progress-item">
                <div className="reports-progress-info">
                  <Typography variant="body2" className="reports-progress-label">
                    {item.label}
                  </Typography>
                  <Typography variant="body2" className="reports-progress-value">
                    {item.value}%
                  </Typography>
                </div>
                <div className="reports-progress-bar">
                  <div 
                    className={`reports-progress-fill ${item.color}`}
                    style={{ width: `${item.value}%` }}
                  />
                </div>
              </div>
            ))}
          </div>

          {/* Recent Activity */}
          <div className="reports-activity-card">
            <div className="reports-card-header">
              <CalendarTodayIcon className="reports-card-icon" />
              <Typography variant="h6" className="reports-card-title">
                {t('reportsPage.recentActivity.title')}
              </Typography>
            </div>
            <div className="reports-activity-list">
              {reportsData.recentActivities.length === 0 ? (
                <Typography variant="body2" className="reports-activity-empty">
                  {t('reportsPage.recentActivity.noActivities')}
                </Typography>
              ) : (
                reportsData.recentActivities.map((activity, index) => (
                  <div key={index} className="reports-activity-item">
                    <div className={`reports-activity-icon ${activity.type}`}>
                      {activity.icon}
                    </div>
                    <div className="reports-activity-content">
                      <Typography variant="body2" className="reports-activity-title">
                        {activity.title}
                      </Typography>
                      <Typography variant="body2" className="reports-activity-description">
                        {activity.description}
                      </Typography>
                      <Typography variant="caption" className="reports-activity-time">
                        {activity.time}
                      </Typography>
                    </div>
                  </div>
                ))
              )}
            </div>
          </div>
        </div>

        {/* Quick Overview Cards */}
        <div className="reports-overview-grid">
          <div className="reports-overview-card">
            <Typography variant="h4" className="reports-overview-value">
              {reportsData.appointmentsToday}
            </Typography>
            <Typography variant="body2" className="reports-overview-label">
              {t('reportsPage.overview.appointmentsToday')}
            </Typography>
          </div>
          <div className="reports-overview-card">
            <Typography variant="h4" className="reports-overview-value">
              {reportsData.therapistsAvailable}
            </Typography>
            <Typography variant="body2" className="reports-overview-label">
              {t('reportsPage.overview.therapistsAvailable')}
            </Typography>
          </div>
          <div className="reports-overview-card">
            <Typography variant="h4" className="reports-overview-value">
              {reportsData.treatmentsCompleted}
            </Typography>
            <Typography variant="body2" className="reports-overview-label">
              {t('reportsPage.overview.treatmentsCompleted')}
            </Typography>
          </div>
          <div className="reports-overview-card">
            <Typography variant="h4" className="reports-overview-value">
              {reportsData.patientSatisfaction}%
            </Typography>
            <Typography variant="body2" className="reports-overview-label">
              {t('reportsPage.overview.patientSatisfaction')}
            </Typography>
          </div>
        </div>
      </Container>
    </div>
  );
};

export default Reports;