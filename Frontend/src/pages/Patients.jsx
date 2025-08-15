import React, { useState, useEffect } from 'react';
import { useTranslation } from 'react-i18next';
import {
  Box,
  Container,
  Typography,
  Paper,
  Table,
  TableBody,
  TableCell,
  TableContainer,
  TableHead,
  TableRow,
  Chip,
  TextField,
  InputAdornment,
  IconButton,
} from '@mui/material';
import SearchIcon from '@mui/icons-material/Search';
import FilterListIcon from '@mui/icons-material/FilterList';
import './Patients.css';
import { ColorThemeService } from '../services/colorThemeService';

export default function Patients() {
  const { t } = useTranslation();
  const [searchQuery, setSearchQuery] = useState('');

  // Initialize color theme on component mount
  useEffect(() => {
    ColorThemeService.initializeTheme();
  }, []);

  const patients = [
    {
      id: 1,
      name: 'Amit Sharma',
      age: 42,
      condition: 'Paralysis',
      status: 'Active',
      lastVisit: '2025-08-01',
    },
    {
      id: 2,
      name: 'Sita Devi',
      age: 65,
      condition: 'Stroke',
      status: 'Inactive',
      lastVisit: '2025-07-20',
    },
  ];

  const filteredPatients = patients.filter(patient =>
    patient.name.toLowerCase().includes(searchQuery.toLowerCase()) ||
    patient.condition.toLowerCase().includes(searchQuery.toLowerCase())
  );

  return (
    <div className="patients-container">
      <Container maxWidth="xl">
        <div className="patients-header">
          <Typography variant="h4" component="h1" className="patients-title">
            {t('patients_title')}
          </Typography>
          
          <TextField
            placeholder={t('search_patients')}
            variant="outlined"
            size="small"
            value={searchQuery}
            onChange={(e) => setSearchQuery(e.target.value)}
            className="patients-search-field"
            InputProps={{
              startAdornment: (
                <InputAdornment position="start">
                  <SearchIcon className="patients-search-icon" />
                </InputAdornment>
              ),
              endAdornment: (
                <InputAdornment position="end">
                  <IconButton size="small" className="patients-filter-button">
                    <FilterListIcon />
                  </IconButton>
                </InputAdornment>
              ),
            }}
          />
        </div>

        <TableContainer component={Paper} className="patients-table-container">
          <Table>
            <TableHead>
              <TableRow className="patients-table-header">
                <TableCell className="patients-table-header-cell">{t('name')}</TableCell>
                <TableCell className="patients-table-header-cell">{t('age')}</TableCell>
                <TableCell className="patients-table-header-cell">{t('condition')}</TableCell>
                <TableCell className="patients-table-header-cell">{t('status')}</TableCell>
                <TableCell className="patients-table-header-cell">{t('last_visit')}</TableCell>
              </TableRow>
            </TableHead>
            <TableBody>
              {filteredPatients.map((patient) => (
                <TableRow
                  key={patient.id}
                  className="patients-table-row"
                >
                  <TableCell className="patients-table-cell">{patient.name}</TableCell>
                  <TableCell className="patients-table-cell">{patient.age}</TableCell>
                  <TableCell className="patients-table-cell">
                    <Chip
                      label={t(patient.condition.toLowerCase())}
                      size="small"
                      className="patients-condition-chip"
                    />
                  </TableCell>
                  <TableCell className="patients-table-cell">
                    <Chip
                      label={t(patient.status.toLowerCase())}
                      size="small"
                      className={`patients-status-chip ${patient.status.toLowerCase()}`}
                    />
                  </TableCell>
                  <TableCell className="patients-table-cell">{patient.lastVisit}</TableCell>
                </TableRow>
              ))}
            </TableBody>
          </Table>
        </TableContainer>
      </Container>
    </div>
  );
}