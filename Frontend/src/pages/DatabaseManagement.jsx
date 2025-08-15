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
  Button,
  Dialog,
  DialogTitle,
  DialogContent,
  DialogActions,
  TextField,
  IconButton,
  Chip,
  Select,
  MenuItem,
  FormControl,
  InputLabel,
  Alert,
  Snackbar,
  Fab,
  Avatar,
  Divider,
  Tooltip,
  Badge,
  InputAdornment,
} from '@mui/material';
import {
  Add as AddIcon,
  Edit as EditIcon,
  Delete as DeleteIcon,
  Search as SearchIcon,
  FilterList as FilterListIcon,
  Storage as StorageIcon,
  Person as PersonIcon,
  Phone as PhoneIcon,
  LocalHospital as LocalHospitalIcon,
  CalendarToday as CalendarIcon,
  Visibility as ViewIcon,
  GetApp as ExportIcon,
  CloudUpload as ImportIcon,
  MoreVert as MoreIcon,
  CloudDone as CloudDoneIcon,
  CloudOff as CloudOffIcon,
} from '@mui/icons-material';
import './DatabaseManagement.css';
import { patientService } from '../services/patientService';
import { ColorThemeService } from '../services/colorThemeService';

const DatabaseManagement = () => {
  const { t, i18n } = useTranslation();
  const [patients, setPatients] = useState([]);
  const [filteredPatients, setFilteredPatients] = useState([]);
  const [openDialog, setOpenDialog] = useState(false);
  const [openDeleteDialog, setOpenDeleteDialog] = useState(false);
  const [editingPatient, setEditingPatient] = useState(null);
  const [deletingPatient, setDeletingPatient] = useState(null);
  const [searchQuery, setSearchQuery] = useState('');
  const [statusFilter, setStatusFilter] = useState('all');
  const [snackbar, setSnackbar] = useState({ open: false, message: '', severity: 'success' });
  const [loading, setLoading] = useState(false);
  const [dataSource, setDataSource] = useState({ isAPI: false, source: 'Mock Data' });
  const [formData, setFormData] = useState({
    id: null,
    name: '',
    age: '',
    gender: '',
    condition: '',
    status: 'Active',
    phone: '',
    address: '',
    dateAdmitted: '',
    treatmentPlan: '',
    emergencyContact: '',
    bloodType: '',
    allergies: '',
    medications: '',
  });

  // Load patients data (real or mock)
  useEffect(() => {
    const loadPatients = async () => {
      setLoading(true);
      try {
        const patientsData = await patientService.getPatients();
        setPatients(patientsData);
        setFilteredPatients(patientsData);
        
        // Update data source info
        const sourceInfo = patientService.getDataSourceInfo();
        setDataSource(sourceInfo);
        
        console.log(`Loaded ${patientsData.length} patients from ${sourceInfo.source}`);
      } catch (error) {
        console.error('Error loading patients:', error);
        setSnackbar({
          open: true,
          message: t('database.messages.loadError') || 'Failed to load patient data',
          severity: 'error'
        });
      } finally {
        setLoading(false);
      }
    };

    loadPatients();
  }, [t]);

  // Filter patients based on search and status
  useEffect(() => {
    let filtered = patients.filter(patient => {
      const patientName = getPatientName(patient);
      return patientName.toLowerCase().includes(searchQuery.toLowerCase()) ||
             patient.condition.toLowerCase().includes(searchQuery.toLowerCase()) ||
             patient.phone.includes(searchQuery) ||
             patient.name?.toLowerCase().includes(searchQuery.toLowerCase()); // Also search original name
    });

    if (statusFilter !== 'all') {
      filtered = filtered.filter(patient => patient.status === statusFilter);
    }

    setFilteredPatients(filtered);
  }, [patients, searchQuery, statusFilter, i18n.language]); // Include language dependency

  // Initialize color theme on component mount
  useEffect(() => {
    ColorThemeService.initializeTheme();
  }, []);

  const handleOpenDialog = (patient = null) => {
    if (patient) {
      setEditingPatient(patient);
      setFormData({ ...patient });
    } else {
      setEditingPatient(null);
      setFormData({
        id: null,
        name: '',
        age: '',
        gender: '',
        condition: '',
        status: 'Active',
        phone: '',
        address: '',
        dateAdmitted: new Date().toISOString().split('T')[0],
        treatmentPlan: '',
        emergencyContact: '',
        bloodType: '',
        allergies: '',
        medications: '',
      });
    }
    setOpenDialog(true);
  };

  const handleCloseDialog = () => {
    setOpenDialog(false);
    setEditingPatient(null);
    setFormData({
      id: null,
      name: '',
      age: '',
      gender: '',
      condition: '',
      status: 'Active',
      phone: '',
      address: '',
      dateAdmitted: '',
      treatmentPlan: '',
      emergencyContact: '',
      bloodType: '',
      allergies: '',
      medications: '',
    });
  };

  const handleInputChange = (e) => {
    const { name, value } = e.target;
    setFormData(prev => ({
      ...prev,
      [name]: value
    }));
  };

  const handleSubmit = async () => {
    // Validation
    if (!formData.name || !formData.age || !formData.condition) {
      setSnackbar({
        open: true,
        message: t('database.messages.validationError'),
        severity: 'error'
      });
      return;
    }

    setLoading(true);
    try {
      if (editingPatient) {
        // Update existing patient
        const updatedPatient = await patientService.updatePatient(editingPatient.id, formData);
        setPatients(prev =>
          prev.map(patient =>
            patient.id === editingPatient.id ? updatedPatient : patient
          )
        );
        setSnackbar({
          open: true,
          message: t('database.messages.updateSuccess'),
          severity: 'success'
        });
      } else {
        // Add new patient
        const newPatient = await patientService.createPatient(formData);
        setPatients(prev => [...prev, newPatient]);
        setSnackbar({
          open: true,
          message: t('database.messages.addSuccess'),
          severity: 'success'
        });
      }
      handleCloseDialog();
    } catch (error) {
      console.error('Error saving patient:', error);
      setSnackbar({
        open: true,
        message: editingPatient ? t('database.messages.updateError') : t('database.messages.addError'),
        severity: 'error'
      });
    } finally {
      setLoading(false);
    }
  };

  const handleDeleteConfirm = (patient) => {
    setDeletingPatient(patient);
    setOpenDeleteDialog(true);
  };

  const handleDelete = async () => {
    if (deletingPatient) {
      setLoading(true);
      try {
        await patientService.deletePatient(deletingPatient.id);
        setPatients(prev => prev.filter(patient => patient.id !== deletingPatient.id));
        setSnackbar({
          open: true,
          message: t('database.messages.deleteSuccess'),
          severity: 'success'
        });
      } catch (error) {
        console.error('Error deleting patient:', error);
        setSnackbar({
          open: true,
          message: t('database.messages.deleteError'),
          severity: 'error'
        });
      } finally {
        setLoading(false);
        setOpenDeleteDialog(false);
        setDeletingPatient(null);
      }
    }
  };

  const getStatusColor = (status) => {
    switch (status) {
      case 'Active':
        return 'success';
      case 'Critical':
        return 'error';
      case 'Inactive':
        return 'default';
      case 'Recovered':
        return 'primary';
      default:
        return 'default';
    }
  };

  const getPatientInitials = (name) => {
    return name.split(' ').map(n => n[0]).join('').toUpperCase();
  };

  // Get multilingual patient name
  const getPatientName = (patient) => {
    // If patient has a nameKey, use translation; otherwise use the name field
    if (patient.nameKey && t(`database.patientNames.${patient.nameKey}`, { defaultValue: null })) {
      return t(`database.patientNames.${patient.nameKey}`);
    }
    return patient.name || t('database.patientNames.default');
  };

  return (
    <div className="database-container">
      <Container maxWidth="xl">
        {/* Header Section */}
        <Paper className="database-header-card">
          <div className="database-header-content">
            <div className="database-header-info">
              <StorageIcon className="database-header-icon" />
              <div>
                <Typography variant="h4" component="h1" className="database-title">
                  {t('database.title')}
                </Typography>
                <Typography variant="body1" className="database-subtitle">
                  {t('database.subtitle')}
                </Typography>
                <div style={{ display: 'flex', alignItems: 'center', gap: '8px', marginTop: '4px' }}>
                  {dataSource.isAPI ? (
                    <CloudDoneIcon fontSize="small" style={{ color: '#4caf50' }} />
                  ) : (
                    <CloudOffIcon fontSize="small" style={{ color: '#ff9800' }} />
                  )}
                  <Typography variant="caption" style={{ color: dataSource.isAPI ? '#4caf50' : '#ff9800' }}>
                    {dataSource.source} • {patients.length} {patients.length === 1 ? 'patient' : 'patients'}
                  </Typography>
                </div>
              </div>
            </div>
            <div className="database-header-actions">
              <Button
                variant="outlined"
                startIcon={<ExportIcon />}
                className="database-action-button"
              >
                {t('database.actions.export')}
              </Button>
              <Button
                variant="outlined"
                startIcon={<ImportIcon />}
                className="database-action-button"
              >
                {t('database.actions.import')}
              </Button>
            </div>
          </div>
        </Paper>

        {/* Search and Filter Section */}
        <Paper className="database-controls-card">
          <div className="database-controls-content">
            <TextField
              placeholder={t('database.search.placeholder')}
              variant="outlined"
              size="medium"
              value={searchQuery}
              onChange={(e) => setSearchQuery(e.target.value)}
              className="database-search-field"
              InputProps={{
                startAdornment: (
                  <InputAdornment position="start">
                    <SearchIcon className="database-search-icon" />
                  </InputAdornment>
                ),
              }}
            />
            
            <FormControl className="database-filter-control" size="medium">
              <InputLabel>{t('database.filters.statusLabel')}</InputLabel>
              <Select
                value={statusFilter}
                label={t('database.filters.statusLabel')}
                onChange={(e) => setStatusFilter(e.target.value)}
                startAdornment={<FilterListIcon className="database-filter-icon" />}
              >
                <MenuItem value="all">{t('database.filters.allStatus')}</MenuItem>
                <MenuItem value="Active">{t('database.filters.active')}</MenuItem>
                <MenuItem value="Inactive">{t('database.filters.inactive')}</MenuItem>
                <MenuItem value="Critical">{t('database.filters.critical')}</MenuItem>
                <MenuItem value="Recovered">{t('database.filters.recovered')}</MenuItem>
              </Select>
            </FormControl>

            <Typography variant="body2" className="database-results-count">
              {t('database.search.results', { count: filteredPatients.length, total: patients.length })}
            </Typography>
          </div>
        </Paper>

        {/* Patient List */}
        <div className="database-patients-section">
          {filteredPatients.length === 0 ? (
            <Paper className="database-empty-state">
              <div className="database-empty-content">
                <StorageIcon className="database-empty-icon" />
                <Typography variant="h6" className="database-empty-title">
                  {patients.length === 0 ? t('database.table.empty') : t('database.search.noResults')}
                </Typography>
                <Typography variant="body2" className="database-empty-description">
                  {patients.length === 0 ? t('database.table.emptyDescription') : ''}
                </Typography>
                {patients.length === 0 && (
                  <Button
                    variant="contained"
                    startIcon={<AddIcon />}
                    onClick={() => handleOpenDialog()}
                    className="database-empty-action"
                  >
                    {t('database.actions.add')}
                  </Button>
                )}
              </div>
            </Paper>
          ) : (
            <Paper className="database-list-container">
              {filteredPatients.map((patient) => {
                const patientName = getPatientName(patient);
                return (
                  <div key={patient.id} className="database-list-item">
                    <div className="database-patient-info-list">
                      <Avatar className="database-patient-avatar-list">
                        {getPatientInitials(patientName)}
                      </Avatar>
                      <div className="database-patient-details-list">
                        <Typography variant="subtitle1" className="database-patient-name-list">
                          {patientName}
                        </Typography>
                        <div className="database-patient-meta-list">
                          <Typography variant="body2">
                            {patient.age} years • {patient.gender}
                          </Typography>
                          <Typography variant="body2">
                            {patient.condition}
                          </Typography>
                          <Typography variant="body2">
                            {patient.phone}
                          </Typography>
                          <Chip
                            label={patient.status === 'Active' ? t('database.filters.active') : 
                                  patient.status === 'Inactive' ? t('database.filters.inactive') :
                                  patient.status === 'Critical' ? t('database.filters.critical') :
                                  t('database.filters.recovered')}
                            size="small"
                            color={getStatusColor(patient.status)}
                            variant="outlined"
                          />
                        </div>
                      </div>
                    </div>
                    <div className="database-patient-actions-list">
                      <Tooltip title={t('database.actions.edit')} arrow>
                        <IconButton
                          size="small"
                          onClick={() => handleOpenDialog(patient)}
                          className="database-action-btn-list edit"
                        >
                          <EditIcon fontSize="small" />
                        </IconButton>
                      </Tooltip>
                      <Tooltip title={t('database.actions.delete')} arrow>
                        <IconButton
                          size="small"
                          onClick={() => handleDeleteConfirm(patient)}
                          className="database-action-btn-list delete"
                        >
                          <DeleteIcon fontSize="small" />
                        </IconButton>
                      </Tooltip>
                    </div>
                  </div>
                );
              })}
            </Paper>
          )}
        </div>

        {/* Floating Add Button */}
        <Fab
          color="primary"
          aria-label={t('database.actions.add')}
          className="database-fab"
          onClick={() => handleOpenDialog()}
        >
          <AddIcon />
        </Fab>

        {/* Add/Edit Dialog */}
        <Dialog 
          open={openDialog} 
          onClose={handleCloseDialog} 
          maxWidth="md" 
          fullWidth 
          className="database-dialog"
        >
          <DialogTitle className="database-dialog-title">
            {editingPatient ? t('database.dialog.editTitle') : t('database.dialog.addTitle')}
          </DialogTitle>
          <DialogContent className="database-dialog-content">
            <Grid container spacing={3} className="database-form-grid">
              <Grid item xs={12} md={6}>
                <TextField
                  name="name"
                  label={t('database.dialog.fields.nameRequired')}
                  value={formData.name}
                  onChange={handleInputChange}
                  fullWidth
                  required
                  className="database-form-field"
                />
              </Grid>
              <Grid item xs={12} md={6}>
                <TextField
                  name="age"
                  label={t('database.dialog.fields.ageRequired')}
                  type="number"
                  value={formData.age}
                  onChange={handleInputChange}
                  fullWidth
                  required
                  className="database-form-field"
                />
              </Grid>
              <Grid item xs={12} md={6}>
                <FormControl fullWidth className="database-form-field">
                  <InputLabel>{t('database.dialog.fields.gender')}</InputLabel>
                  <Select
                    name="gender"
                    value={formData.gender}
                    label={t('database.dialog.fields.gender')}
                    onChange={handleInputChange}
                  >
                    <MenuItem value="Male">{t('database.dialog.fields.male')}</MenuItem>
                    <MenuItem value="Female">{t('database.dialog.fields.female')}</MenuItem>
                    <MenuItem value="Other">{t('database.dialog.fields.other')}</MenuItem>
                  </Select>
                </FormControl>
              </Grid>
              <Grid item xs={12} md={6}>
                <FormControl fullWidth className="database-form-field">
                  <InputLabel>{t('database.dialog.fields.status')}</InputLabel>
                  <Select
                    name="status"
                    value={formData.status}
                    label={t('database.dialog.fields.status')}
                    onChange={handleInputChange}
                  >
                    <MenuItem value="Active">{t('database.filters.active')}</MenuItem>
                    <MenuItem value="Inactive">{t('database.filters.inactive')}</MenuItem>
                    <MenuItem value="Critical">{t('database.filters.critical')}</MenuItem>
                    <MenuItem value="Recovered">{t('database.filters.recovered')}</MenuItem>
                  </Select>
                </FormControl>
              </Grid>
              <Grid item xs={12}>
                <TextField
                  name="condition"
                  label={t('database.dialog.fields.conditionRequired')}
                  value={formData.condition}
                  onChange={handleInputChange}
                  fullWidth
                  required
                  className="database-form-field"
                />
              </Grid>
              <Grid item xs={12} md={6}>
                <TextField
                  name="phone"
                  label={t('database.dialog.fields.phone')}
                  value={formData.phone}
                  onChange={handleInputChange}
                  fullWidth
                  className="database-form-field"
                />
              </Grid>
              <Grid item xs={12} md={6}>
                <TextField
                  name="emergencyContact"
                  label={t('database.dialog.fields.emergencyContact')}
                  value={formData.emergencyContact}
                  onChange={handleInputChange}
                  fullWidth
                  className="database-form-field"
                />
              </Grid>
              <Grid item xs={12} md={6}>
                <TextField
                  name="dateAdmitted"
                  label={t('database.dialog.fields.dateAdmitted')}
                  type="date"
                  value={formData.dateAdmitted}
                  onChange={handleInputChange}
                  fullWidth
                  className="database-form-field"
                  InputLabelProps={{
                    shrink: true,
                  }}
                />
              </Grid>
              <Grid item xs={12} md={6}>
                <TextField
                  name="bloodType"
                  label={t('database.dialog.fields.bloodType')}
                  value={formData.bloodType}
                  onChange={handleInputChange}
                  fullWidth
                  className="database-form-field"
                />
              </Grid>
              <Grid item xs={12}>
                <TextField
                  name="address"
                  label={t('database.dialog.fields.address')}
                  value={formData.address}
                  onChange={handleInputChange}
                  fullWidth
                  multiline
                  rows={2}
                  className="database-form-field"
                />
              </Grid>
              <Grid item xs={12}>
                <TextField
                  name="allergies"
                  label={t('database.dialog.fields.allergies')}
                  value={formData.allergies}
                  onChange={handleInputChange}
                  fullWidth
                  multiline
                  rows={2}
                  className="database-form-field"
                />
              </Grid>
              <Grid item xs={12}>
                <TextField
                  name="medications"
                  label={t('database.dialog.fields.medications')}
                  value={formData.medications}
                  onChange={handleInputChange}
                  fullWidth
                  multiline
                  rows={2}
                  className="database-form-field"
                />
              </Grid>
              <Grid item xs={12}>
                <TextField
                  name="treatmentPlan"
                  label={t('database.dialog.fields.treatmentPlan')}
                  value={formData.treatmentPlan}
                  onChange={handleInputChange}
                  fullWidth
                  multiline
                  rows={3}
                  className="database-form-field"
                />
              </Grid>
            </Grid>
          </DialogContent>
          <DialogActions className="database-dialog-actions">
            <Button onClick={handleCloseDialog} className="database-cancel-button" disabled={loading}>
              {t('database.dialog.buttons.cancel')}
            </Button>
            <Button 
              onClick={handleSubmit} 
              variant="contained" 
              className="database-submit-button"
              disabled={loading}
            >
              {loading ? '...' : (editingPatient ? t('database.dialog.buttons.update') : t('database.dialog.buttons.add'))}
            </Button>
          </DialogActions>
        </Dialog>

        {/* Delete Confirmation Dialog */}
        <Dialog
          open={openDeleteDialog}
          onClose={() => setOpenDeleteDialog(false)}
          className="database-delete-dialog"
        >
          <DialogTitle className="database-delete-title">
            {t('database.dialog.deleteTitle')}
          </DialogTitle>
          <DialogContent>
            <Typography variant="body1">
              {t('database.dialog.deleteMessage')}
            </Typography>
            {deletingPatient && (
              <Typography variant="body2" className="database-delete-patient-name">
                <strong>{getPatientName(deletingPatient)}</strong>
              </Typography>
            )}
          </DialogContent>
          <DialogActions>
            <Button onClick={() => setOpenDeleteDialog(false)} disabled={loading}>
              {t('database.dialog.buttons.cancel')}
            </Button>
            <Button onClick={handleDelete} color="error" variant="contained" disabled={loading}>
              {loading ? '...' : t('database.dialog.buttons.delete')}
            </Button>
          </DialogActions>
        </Dialog>

        {/* Snackbar for notifications */}
        <Snackbar
          open={snackbar.open}
          autoHideDuration={6000}
          onClose={() => setSnackbar({ ...snackbar, open: false })}
          anchorOrigin={{ vertical: 'bottom', horizontal: 'right' }}
        >
          <Alert
            onClose={() => setSnackbar({ ...snackbar, open: false })}
            severity={snackbar.severity}
            className="database-snackbar-alert"
            variant="filled"
          >
            {snackbar.message}
          </Alert>
        </Snackbar>
      </Container>
    </div>
  );
};

export default DatabaseManagement;
