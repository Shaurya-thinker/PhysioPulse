import React, { useState, useEffect } from 'react';
import { useTranslation } from 'react-i18next';
import {
  Container,
  Typography,
  Card,
  CardContent,
  Grid,
  Paper,
  ToggleButton,
  ToggleButtonGroup,
  ButtonGroup,
  Button,
} from '@mui/material';
import PeopleAltIcon from '@mui/icons-material/PeopleAlt';
import LocalHospitalIcon from '@mui/icons-material/LocalHospital';
import TrendingUpIcon from '@mui/icons-material/TrendingUp';
import MonitorHeartIcon from '@mui/icons-material/MonitorHeart';
import WavingHandIcon from '@mui/icons-material/WavingHand';
import ShowChartIcon from '@mui/icons-material/ShowChart';
import CalendarTodayIcon from '@mui/icons-material/CalendarToday';
import DateRangeIcon from '@mui/icons-material/DateRange';
import './Dashboard.css';
import { ColorThemeService } from '../services/colorThemeService';

const Dashboard = () => {
  const { t, i18n } = useTranslation();
  const [dashboardData, setDashboardData] = useState({
    totalPatients: 0,
    activeCases: 0,
    recoveryRate: 0,
    criticalCases: 0,
  });

  // Chart state
  const [chartType, setChartType] = useState('admissions'); // 'admissions' or 'recoveries'
  const [timeFilter, setTimeFilter] = useState('today'); // 'today' or 'month'
  const [realChartData, setRealChartData] = useState(null); // Store real patient data
  const [hasRealData, setHasRealData] = useState(false);

  useEffect(() => {
    // Fetch real data from backend/database
    const fetchDashboardData = async () => {
      try {
        /* 
        REAL DATA INTEGRATION EXAMPLE:
        
        // 1. Fetch dashboard stats from your patient database
        const response = await fetch('/api/dashboard/stats');
        const data = await response.json();
        setDashboardData({
          totalPatients: data.totalPatients,
          activeCases: data.activeCases,
          recoveryRate: data.recoveryRate,
          criticalCases: data.criticalCases
        });
        
        // 2. Fetch chart data based on current filters
        const chartResponse = await fetch(`/api/patients/analytics?type=${chartType}&period=${timeFilter}`);
        const chartData = await chartResponse.json();
        
        // Expected API response format:
        // {
        //   labels: ['2025-08-01', '2025-08-02', ...], // dates or hours
        //   data: [10, 15, 8, 12, ...], // actual patient counts
        //   type: 'admissions' | 'recoveries'
        // }
        
        if (chartData && chartData.data && chartData.data.length > 0) {
          setRealChartData(chartData);
          setHasRealData(true);
        } else {
          setHasRealData(false);
          setRealChartData(null);
        }
        */
        
        // For now, no backend is connected - show no data state
        console.log('No backend connected - no real data available');
        console.log('To show real data: Connect to your patient database and implement the API endpoints above');
        setHasRealData(false);
        setRealChartData(null);
      } catch (error) {
        console.log('Backend not available - no real data');
        setHasRealData(false);
        setRealChartData(null);
      }
    };

    fetchDashboardData();
  }, [chartType, timeFilter]); // Refetch when chart type or time filter changes

  // Initialize color theme on component mount
  useEffect(() => {
    ColorThemeService.initializeTheme();
  }, []);

  // Real data chart processing (only use actual patient data)
  const getRealChartData = () => {
    if (!hasRealData || !realChartData) {
      // Return empty data structure with 0 values instead of null
      const today = new Date();
      let labels = [];
      let data = [];

      if (timeFilter === 'today') {
        // Generate hourly labels for today with 0 values
        for (let i = 0; i < 24; i++) {
          labels.push(`${i.toString().padStart(2, '0')}:00`);
          data.push(0); // All zeros - no real data
        }
      } else {
        // Generate daily labels for this month with 0 values
        const daysInMonth = new Date(today.getFullYear(), today.getMonth() + 1, 0).getDate();
        for (let i = 1; i <= daysInMonth; i++) {
          labels.push(`${i}`);
          data.push(0); // All zeros - no real data
        }
      }

      return { labels, data };
    }

    // Process real data based on time filter and chart type
    // This would process your actual patient database records
    const processedData = {
      labels: realChartData.labels || [],
      data: realChartData.data || []
    };

    return processedData;
  };

  const chartData = getRealChartData();

  // No Data Component
  const NoDataMessage = () => (
    <div className="no-data-container">
      <div className="no-data-icon">
        <ShowChartIcon className="no-data-chart-icon" />
      </div>
      <h3 className="no-data-title">{t('dashboard.chart.noData.title')}</h3>
      <p className="no-data-description">
        {chartType === 'admissions' 
          ? t('dashboard.chart.noData.admissionDescription')
          : t('dashboard.chart.noData.recoveryDescription')
        }
      </p>
      <div className="no-data-instructions">
        <p><strong>{t('dashboard.chart.noData.instructions')}</strong></p>
        <ul>
          {t('dashboard.chart.noData.steps', { returnObjects: true }).map((step, index) => (
            <li key={index}>{step}</li>
          ))}
        </ul>
      </div>
    </div>
  );

  // Simple SVG Line Chart Component
  const SimpleLineChart = ({ data, labels, type }) => {
    const width = 800;
    const height = 300;
    const padding = 50;
    const chartWidth = width - 2 * padding;
    const chartHeight = height - 2 * padding;

    const maxValue = Math.max(...data);
    const minValue = Math.min(...data);
    const range = maxValue - minValue || 1;
    
    // If all values are 0, set a reasonable scale
    const displayMaxValue = maxValue === 0 ? 10 : maxValue;
    const displayRange = displayMaxValue - minValue || 10;

    // Generate path for the line
    const pathData = data.map((value, index) => {
      const x = padding + (index / (data.length - 1)) * chartWidth;
      const y = padding + ((displayMaxValue - value) / displayRange) * chartHeight;
      return `${index === 0 ? 'M' : 'L'} ${x} ${y}`;
    }).join(' ');

    // Generate area path
    const areaData = `${pathData} L ${padding + chartWidth} ${padding + chartHeight} L ${padding} ${padding + chartHeight} Z`;

    const color = type === 'admissions' ? '#1976d2' : '#2e7d32';
    const lightColor = type === 'admissions' ? 'rgba(25, 118, 210, 0.1)' : 'rgba(46, 125, 50, 0.1)';

    // Check if we have real data or just zeros
    const hasActualData = data.some(value => value > 0);

    return (
      <div className="simple-chart-container">
        <svg width="100%" height="300" viewBox={`0 0 ${width} ${height}`} className="simple-chart-svg">
          {/* Grid lines */}
          <defs>
            <pattern id="grid" width="40" height="30" patternUnits="userSpaceOnUse">
              <path d="M 40 0 L 0 0 0 30" fill="none" stroke="rgba(0,0,0,0.1)" strokeWidth="1" strokeDasharray="2,2"/>
            </pattern>
          </defs>
          <rect width="100%" height="100%" fill="url(#grid)" />
          
          {/* Area under curve - only show if there's actual data */}
          {hasActualData && <path d={areaData} fill={lightColor} />}
          
          {/* Main line */}
          <path 
            d={pathData} 
            fill="none" 
            stroke={hasActualData ? color : 'rgba(107, 114, 128, 0.4)'} 
            strokeWidth="3" 
            strokeLinecap="round"
            strokeLinejoin="round"
            strokeDasharray={hasActualData ? "none" : "5,5"}
          />
          
          {/* Data points - only show if there's actual data */}
          {hasActualData && data.map((value, index) => {
            const x = padding + (index / (data.length - 1)) * chartWidth;
            const y = padding + ((displayMaxValue - value) / displayRange) * chartHeight;
            return (
              <circle
                key={index}
                cx={x}
                cy={y}
                r="4"
                fill={color}
                stroke="#ffffff"
                strokeWidth="2"
                className="chart-point"
              />
            );
          })}
          
          {/* Y-axis labels */}
          <text x="20" y={padding} textAnchor="middle" className="chart-label">{displayMaxValue}</text>
          <text x="20" y={padding + chartHeight} textAnchor="middle" className="chart-label">0</text>
          
          {/* X-axis labels */}
          <text x={padding} y={height - 10} textAnchor="middle" className="chart-label">{labels[0]}</text>
          <text x={padding + chartWidth} y={height - 10} textAnchor="middle" className="chart-label">{labels[labels.length - 1]}</text>
          
          {/* No data overlay text */}
          {!hasActualData && (
            <text 
              x={width / 2} 
              y={height / 2} 
              textAnchor="middle" 
              className="no-data-overlay-text"
              fill="rgba(107, 114, 128, 0.6)"
              fontSize="16"
              fontWeight="600"
            >
              {t('dashboard.chart.overlay.' + (type === 'admissions' ? 'noAdmissions' : 'noRecoveries'))} {timeFilter === 'today' ? t('dashboard.chart.today').toLowerCase() : t('dashboard.chart.thisMonth').toLowerCase()}
            </text>
          )}
        </svg>
        
        <div className="chart-stats">
          <div className="chart-stat">
            <span className="chart-stat-label">{t('dashboard.chart.stats.max')}:</span>
            <span className="chart-stat-value" style={{ color: hasActualData ? color : '#6b7280' }}>{maxValue}</span>
          </div>
          <div className="chart-stat">
            <span className="chart-stat-label">{t('dashboard.chart.stats.min')}:</span>
            <span className="chart-stat-value" style={{ color: hasActualData ? color : '#6b7280' }}>{minValue}</span>
          </div>
          <div className="chart-stat">
            <span className="chart-stat-label">{t('dashboard.chart.stats.total')}:</span>
            <span className="chart-stat-value" style={{ color: hasActualData ? color : '#6b7280' }}>{data.reduce((a, b) => a + b, 0)}</span>
          </div>
        </div>
      </div>
    );
  };

  const getCurrentTime = () => {
    const now = new Date();
    const hours = now.getHours();
    if (hours < 12) return t('dashboard.greeting.morning');
    if (hours < 17) return t('dashboard.greeting.afternoon');
    return t('dashboard.greeting.evening');
  };

  const stats = [
    {
      title: t('dashboard.metrics.totalPatients'),
      value: dashboardData.totalPatients,
      icon: <PeopleAltIcon />,
      color: '#1976d2',
      bgColor: '#e3f2fd',
    },
    {
      title: t('dashboard.metrics.activeCases'),
      value: dashboardData.activeCases,
      icon: <LocalHospitalIcon />,
      color: '#2e7d32',
      bgColor: '#e8f5e8',
    },
    {
      title: t('dashboard.metrics.recoveryRate'),
      value: `${dashboardData.recoveryRate}%`,
      icon: <TrendingUpIcon />,
      color: '#f57c00',
      bgColor: '#fff3e0',
    },
    {
      title: t('dashboard.metrics.criticalCases'),
      value: dashboardData.criticalCases,
      icon: <MonitorHeartIcon />,
      color: '#d32f2f',
      bgColor: '#ffebee',
    },
  ];

  return (
    <div className="dashboard-container">
      <Container maxWidth="xl">
        {/* Welcome Section */}
        <Paper className="dashboard-welcome-card" elevation={0}>
          <div className="dashboard-welcome-content">
            <div className="dashboard-greeting">
              <WavingHandIcon className="dashboard-greeting-icon" />
              <Typography className="dashboard-greeting-text" variant="h4">
                {getCurrentTime()}!
              </Typography>
            </div>
            <Typography className="dashboard-welcome-title" variant="h5">
              {t('dashboard.welcome.title')}
            </Typography>
            <Typography className="dashboard-welcome-description" variant="body1">
              {t('dashboard.welcome.description')}
            </Typography>
          </div>
          
          {/* Decorative elements */}
          <div className="dashboard-decoration-1" />
          <div className="dashboard-decoration-2" />
        </Paper>

        {/* Main Statistics */}
        <Typography className="dashboard-section-title" variant="h5">
          {t('dashboard.metrics.title')}
        </Typography>

        <Grid container spacing={3} className="dashboard-stats-grid">
          {stats.map((stat, index) => (
            <Grid item xs={12} sm={6} md={3} key={index}>
              <Card className="dashboard-stat-card">
                <CardContent className="dashboard-stat-content">
                  <div className="dashboard-stat-header">
                    <div className={`dashboard-stat-icon dashboard-stat-icon-${index + 1}`}>
                      {stat.icon}
                    </div>
                    <Typography className="dashboard-stat-title" variant="h6">
                      {stat.title}
                    </Typography>
                  </div>
                  
                  <Typography className={`dashboard-stat-value dashboard-stat-value-${index + 1}`} variant="h3">
                    {stat.value}
                  </Typography>
                </CardContent>
              </Card>
            </Grid>
          ))}
        </Grid>

        {/* Patient Trends Chart */}
        <Paper className="dashboard-chart-card">
          <div className="dashboard-chart-header">
            <div className="dashboard-chart-title-section">
              <ShowChartIcon className="dashboard-chart-icon" />
              <Typography className="dashboard-chart-title" variant="h6">
                {t('dashboard.chart.title')}
              </Typography>
            </div>
            
            <div className="dashboard-chart-controls">
              <ToggleButtonGroup
                value={chartType}
                exclusive
                onChange={(e, newType) => newType && setChartType(newType)}
                className="dashboard-toggle-group"
                size="small"
              >
                <ToggleButton value="admissions" className="dashboard-toggle-btn">
                  <PeopleAltIcon className="dashboard-toggle-icon" />
                  {t('dashboard.chart.admissions')}
                </ToggleButton>
                <ToggleButton value="recoveries" className="dashboard-toggle-btn">
                  <TrendingUpIcon className="dashboard-toggle-icon" />
                  {t('dashboard.chart.recoveries')}
                </ToggleButton>
              </ToggleButtonGroup>

              <ButtonGroup className="dashboard-time-filter" size="small">
                <Button
                  variant={timeFilter === 'today' ? 'contained' : 'outlined'}
                  onClick={() => setTimeFilter('today')}
                  startIcon={<CalendarTodayIcon />}
                  className="dashboard-filter-btn"
                >
                  {t('dashboard.chart.today')}
                </Button>
                <Button
                  variant={timeFilter === 'month' ? 'contained' : 'outlined'}
                  onClick={() => setTimeFilter('month')}
                  startIcon={<DateRangeIcon />}
                  className="dashboard-filter-btn"
                >
                  {t('dashboard.chart.thisMonth')}
                </Button>
              </ButtonGroup>
            </div>
          </div>

          <div className="dashboard-chart-container">
            {chartData ? (
              <SimpleLineChart 
                data={chartData.data} 
                labels={chartData.labels} 
                type={chartType}
              />
            ) : (
              <NoDataMessage />
            )}
          </div>
        </Paper>
        

        {/* Quick Actions */}
        <Paper className="dashboard-actions-card">
          <Typography className="dashboard-actions-title" variant="h6">
            {t('dashboard.quickActions.title')}
          </Typography>
          
          <Grid container spacing={2}>
            <Grid item xs={12} sm={6} md={3}>
              <div className="dashboard-action-item">
                <PeopleAltIcon className="dashboard-action-icon dashboard-action-icon-patients" />
                <Typography className="dashboard-action-text" variant="body2">
                  {t('dashboard.quickActions.viewPatients')}
                </Typography>
              </div>
            </Grid>
            
            <Grid item xs={12} sm={6} md={3}>
              <div className="dashboard-action-item">
                <LocalHospitalIcon className="dashboard-action-icon dashboard-action-icon-add" />
                <Typography className="dashboard-action-text" variant="body2">
                  {t('dashboard.quickActions.addPatient')}
                </Typography>
              </div>
            </Grid>
            
            <Grid item xs={12} sm={6} md={3}>
              <div className="dashboard-action-item">
                <TrendingUpIcon className="dashboard-action-icon dashboard-action-icon-reports" />
                <Typography className="dashboard-action-text" variant="body2">
                  {t('dashboard.quickActions.viewReports')}
                </Typography>
              </div>
            </Grid>
            
            <Grid item xs={12} sm={6} md={3}>
              <div className="dashboard-action-item">
                <MonitorHeartIcon className="dashboard-action-icon dashboard-action-icon-database" />
                <Typography className="dashboard-action-text" variant="body2">
                  {t('dashboard.quickActions.manageDatabase')}
                </Typography>
              </div>
            </Grid>
          </Grid>
        </Paper>
      </Container>
    </div>
  );
};

export default Dashboard;