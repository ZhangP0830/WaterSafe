<script setup>
import { ref, onMounted, onUnmounted } from "vue";
import MaterialInput from "@/components/MaterialInput.vue";
import MaterialButton from "@/components/MaterialButton.vue";
import NavbarDefault from "../components/navigation/NavbarDefault.vue";
import DefaultFooter from "../components/layout/FooterDefault.vue";
import Header from "../components/layout/Header.vue";

// Background image
import heroBg from "@/assets/img/trusted-background.png";

// Page lifecycle
const body = document.getElementsByTagName("body")[0];
onMounted(() => {
  body.classList.add("water-quality-prediction-page");
  body.classList.add("bg-gray-100");
  
  // Load available suburbs for autocomplete
  loadAvailableSuburbs();
});
onUnmounted(() => {
  body.classList.remove("water-quality-prediction-page");
  body.classList.remove("bg-gray-100");
});

// Reactive data
const siteId = ref("");
const suburbName = ref("");
const isLoading = ref(false);
const predictionResult = ref(null);
const errorMessage = ref("");
const suburbSearchResults = ref([]);
const showSuburbSearch = ref(false);

// Autocomplete functionality
const availableSuburbs = ref([]);
const filteredSuburbs = ref([]);
const showSuggestions = ref(false);
const selectedSuggestionIndex = ref(-1);

// API base URL - Auto-detect environment
const API_BASE_URL = import.meta.env.VITE_BACKEND_API_URL || 
  (import.meta.env.DEV ? 'http://localhost:8000' : '/api');

// Load available suburbs for autocomplete
const loadAvailableSuburbs = async () => {
  try {
    const response = await fetch(`${API_BASE_URL}/prediction/suburbs`);
    if (response.ok) {
      const data = await response.json();
      availableSuburbs.value = data.suburbs.map(suburb => suburb.nearest_suburb);
      console.log("Loaded suburbs:", availableSuburbs.value.length);
    }
  } catch (error) {
    console.error("Failed to load suburbs:", error);
  }
};

// Filter suburbs based on input
const filterSuburbs = () => {
  const input = suburbName.value;
  
  if (!input || input.length < 2) {
    filteredSuburbs.value = [];
    showSuggestions.value = false;
    return;
  }
  
  filteredSuburbs.value = availableSuburbs.value.filter(suburb =>
    suburb.toLowerCase().includes(input.toLowerCase())
  ).slice(0, 8); // Limit to 8 suggestions
  
  showSuggestions.value = filteredSuburbs.value.length > 0;
  selectedSuggestionIndex.value = -1;
};

// Select suggestion
const selectSuggestion = (suburb) => {
  suburbName.value = suburb;
  showSuggestions.value = false;
  filteredSuburbs.value = [];
  selectedSuggestionIndex.value = -1;
};

// Handle keyboard navigation
const handleKeydown = (event) => {
  if (!showSuggestions.value || filteredSuburbs.value.length === 0) return;
  
  switch (event.key) {
    case 'ArrowDown':
      event.preventDefault();
      selectedSuggestionIndex.value = Math.min(
        selectedSuggestionIndex.value + 1,
        filteredSuburbs.value.length - 1
      );
      break;
    case 'ArrowUp':
      event.preventDefault();
      selectedSuggestionIndex.value = Math.max(selectedSuggestionIndex.value - 1, -1);
      break;
    case 'Enter':
      event.preventDefault();
      if (selectedSuggestionIndex.value >= 0) {
        selectSuggestion(filteredSuburbs.value[selectedSuggestionIndex.value]);
      }
      break;
    case 'Escape':
      showSuggestions.value = false;
      selectedSuggestionIndex.value = -1;
      break;
  }
};

// Get status color based on risk level
const getStatusColor = (riskLevel) => {
  const colors = {
    "Safe": "success",
    "Moderate": "warning", 
    "Unsafe": "danger"
  };
  return colors[riskLevel] || "secondary";
};

// Get data freshness status
const getDataFreshnessColor = (freshness) => {
  const colors = {
    "fresh": "success",
    "stale": "warning",
    "outdated": "danger",
    "unknown": "secondary"
  };
  return colors[freshness] || "secondary";
};

// Get data freshness icon
const getDataFreshnessIcon = (freshness) => {
  const icons = {
    "fresh": "check_circle",
    "stale": "schedule",
    "outdated": "warning",
    "unknown": "help_outline"
  };
  return icons[freshness] || "help_outline";
};

// Get status icon based on risk level
const getStatusIcon = (riskLevel) => {
  const icons = {
    "Safe": "check_circle",
    "Moderate": "warning",
    "Unsafe": "error"
  };
  return icons[riskLevel] || "help_outline";
};



// Get parameter unit
const getParameterUnit = (paramName) => {
  const units = {
    'Chloride as Cl': 'mg/L',
    'Calcium (Total)': 'mg/L',
    'Total Magnesium': 'mg/L',
    'Sodium as Na': 'mg/L',
    'Potassium as K': 'mg/L',
    'Salinity as EC@25 (lab)': 'µS/cm',
    'pH': 'pH units'
  };
  return units[paramName] || '';
};

// Get parameter description
const getParameterDescription = (paramName) => {
  const descriptions = {
    'pH': 'Measures water acidity/alkalinity. Optimal: 6.5-8.5. Low pH can cause corrosion and metal leaching. High pH may cause scaling and bitter taste.',
    'Chloride as Cl': 'Essential mineral for health. Safe levels <250mg/L. High levels (>250mg/L) can cause salty taste, corrosion, and may be harmful to people with heart conditions.',
    'Calcium (Total)': 'Beneficial mineral for bone health. Generally safe, but high levels (>200mg/L) can cause scaling, kidney stones, and affect soap efficiency.',
    'Total Magnesium': 'Essential mineral for health. Safe levels <150mg/L. Very high levels may cause diarrhea and digestive issues, especially in infants.',
    'Sodium as Na': 'Important electrolyte. Safe levels <200mg/L. High levels (>200mg/L) can be harmful to people with high blood pressure, heart disease, or kidney problems.',
    'Potassium as K': 'Essential mineral for heart and muscle function. Generally safe in drinking water. Very high levels (>12mg/L) may be harmful to people with kidney problems.',
    'Salinity as EC@25 (lab)': 'Measures total dissolved salts. Safe levels <500µS/cm. High levels (>1000µS/cm) can cause salty taste, dehydration, and health issues for sensitive populations.'
  };
  return descriptions[paramName] || 'Water quality parameter';
};

// Search for water quality prediction by suburb
const searchWaterQuality = async () => {
  if (!suburbName.value.trim()) {
    errorMessage.value = "Please enter a suburb name";
    return;
  }
  
  // Clear previous results
  predictionResult.value = null;
  errorMessage.value = "";
  showSuburbSearch.value = false;
  
  // Direct prediction flow: search suburb and get prediction for first site
  await searchSuburbAndPredict();
};

// Search suburb and get prediction for the first available site
const searchSuburbAndPredict = async () => {
  isLoading.value = true;
  errorMessage.value = "";
  
  try {
    // First, search for sites in the suburb
    const response = await fetch(`${API_BASE_URL}/prediction/search-by-suburb`, {
      method: 'POST',
      headers: {
        'Content-Type': 'application/json',
      },
      body: JSON.stringify({
        suburb_name: suburbName.value
      })
    });

    if (!response.ok) {
      const errorData = await response.json();
      throw new Error(errorData.detail || 'Failed to search suburbs');
    }

    const data = await response.json();
    
    if (!data.sites || data.sites.length === 0) {
      errorMessage.value = `No monitoring sites found for "${suburbName.value}"`;
      return;
    }

    // Get the first site ID and make prediction
    const firstSite = data.sites[0];
    siteId.value = firstSite.site_id;
    
    // Hide suburb search results and get prediction
    showSuburbSearch.value = false;
    
    // Get prediction for the first site
    await searchBySiteId();
    
  } catch (error) {
    errorMessage.value = `Failed to search and predict: ${error.message}`;
    console.error("Error in searchSuburbAndPredict:", error);
  } finally {
    isLoading.value = false;
  }
};

// Search by site ID
const searchBySiteId = async () => {
  isLoading.value = true;
  errorMessage.value = "";
  
  try {
    // Call the real prediction API
    const response = await fetch(`${API_BASE_URL}/prediction/predict`, {
      method: 'POST',
      headers: {
        'Content-Type': 'application/json',
      },
      body: JSON.stringify({
        site_id: siteId.value
      })
    });

    if (!response.ok) {
      const errorData = await response.json();
      throw new Error(errorData.detail || 'Failed to fetch prediction');
    }

    const data = await response.json();
    predictionResult.value = data;
    
  } catch (error) {
    errorMessage.value = `Failed to fetch water quality prediction: ${error.message}`;
    console.error("Error fetching water quality:", error);
  } finally {
    isLoading.value = false;
  }
};

// Search by suburb name
const searchBySuburbName = async () => {
  isLoading.value = true;
  errorMessage.value = "";
  
  try {
    // Call the suburb search API
    const response = await fetch(`${API_BASE_URL}/api/prediction/search-by-suburb`, {
      method: 'POST',
      headers: {
        'Content-Type': 'application/json',
      },
      body: JSON.stringify({
        suburb_name: suburbName.value
      })
    });

    if (!response.ok) {
      const errorData = await response.json();
      throw new Error(errorData.detail || 'Failed to search suburbs');
    }

    const data = await response.json();
    suburbSearchResults.value = data.sites;
    showSuburbSearch.value = true;
    
  } catch (error) {
    errorMessage.value = `Failed to search suburbs: ${error.message}`;
    console.error("Error searching suburbs:", error);
  } finally {
    isLoading.value = false;
  }
};

// Select site from suburb search results
const selectSiteFromSuburb = async (selectedSiteId) => {
  siteId.value = selectedSiteId;
  showSuburbSearch.value = false;
  await searchBySiteId();
};

// Clear results
const clearResults = () => {
  predictionResult.value = null;
  errorMessage.value = "";
  siteId.value = "";
  suburbName.value = "";
  suburbSearchResults.value = [];
  showSuburbSearch.value = false;
};

// Generate PDF report
const generatePDFReport = () => {
  if (!predictionResult.value) return;
  
  const reportContent = `
WATER QUALITY PREDICTION REPORT
Generated: ${new Date().toLocaleDateString()}
Suburb: ${suburbName.value}
Site ID: ${predictionResult.value.site_id}
Prediction Date: ${predictionResult.value.prediction_date}

OVERALL ASSESSMENT:
Risk Level: ${predictionResult.value.risk_level}
WQI Score: ${predictionResult.value.wqi_score}/100
Data Freshness: ${predictionResult.value.data_freshness}

WATER QUALITY PARAMETERS:
${Object.entries(predictionResult.value.parameters).map(([param, value]) => 
  `${param}: ${value.toFixed(2)} ${getParameterUnit(param)}`
).join('\n')}

SPECIFIC GUIDANCE:

Pregnancy:
${(predictionResult.value.specific_guidance?.pregnancy || []).join('\n')}

Infants:
${(predictionResult.value.specific_guidance?.infants || []).join('\n')}

Elderly:
${(predictionResult.value.specific_guidance?.elderly || []).join('\n')}

OFFLINE SAFETY CHECKLIST:
${(predictionResult.value.offline_checklist || []).join('\n')}
`;

  // Create and download the report
  const blob = new Blob([reportContent], { type: 'text/plain' });
  const url = window.URL.createObjectURL(blob);
  const link = document.createElement('a');
  link.href = url;
  link.download = `water_quality_report_${predictionResult.value.site_id}_${new Date().toISOString().split('T')[0]}.txt`;
  document.body.appendChild(link);
  link.click();
  document.body.removeChild(link);
  window.URL.revokeObjectURL(url);
};
</script>

<template>
  <!-- Navigation bar -->
  <div class="container position-sticky z-index-sticky top-0">
    <div class="row">
      <div class="col-12">
        <NavbarDefault :sticky="true" />
      </div>
    </div>
  </div>
    
  <!-- Page header -->
  <Header>
    <div
    class="page-header min-vh-100"
    :style="`background-image: url(${heroBg})`"
    loading="lazy"
  >
      <div class="container">
        <div class="row">
          <div class="col-lg-8 mx-auto text-center">
            <h1
            class="text-white pt-3 mt-n5 me-2 display-5 fw-bold"
            :style="{ display: 'inline-block' }"
          >
            Water Quality Prediction
          </h1>
            <p class="lead text-white px-5 mt-4 mb-5" :style="{ fontWeight: '500', fontSize: '1.25rem' }">
              Advanced AI-powered water quality forecasting system providing real-time predictions, safety ratings, and personalized guidance for different population groups
            </p>
          </div>
        </div>
      </div>
    </div>
  </Header>

  <!-- Main content -->
  <div class="card card-body blur shadow-blur mx-3 mx-md-4 mt-n6">
    <div class="container">
        <!-- Page Introduction -->
        <div class="row mb-4">
          <div class="col-12">
            <div class="card shadow-sm border-0">
              <div class="card-body">
                <div class="row align-items-center">
                  <div class="col-12">
                    <h4 class="mb-3">
                      <i class="material-icons me-2 text-info">analytics</i>
                      Water Quality Prediction
                    </h4>
                    <p class="text-muted mb-3">
                      Our prediction system uses machine learning models trained on historical water quality data to forecast water safety conditions for monitoring sites. Simply enter a suburb name below to get instant water quality predictions including safety ratings, parameter forecasts, and personalized guidance for different population groups.
                    </p>
                  </div>
                </div>
              </div>
            </div>
          </div>
        </div>

        <!-- Search control panel -->
        <div class="row mb-4">
          <div class="col-12">
            <div class="card shadow-sm">
              <div class="card-body">
                <div class="row align-items-end">
                  <!-- Suburb Name input -->
                  <div class="col-md-8">
                    <div class="position-relative">
                      <label class="form-label">
                        <i class="material-icons me-2 text-primary">location_city</i>
                        Suburb Name
                      </label>
                      <MaterialInput
                        v-model="suburbName"
                        class="mb-3"
                        type="text"
                        placeholder="e.g., Modella, Lyndhurst, Koo Wee Rup"
                        :disabled="isLoading"
                        @input="filterSuburbs"
                        @keydown="handleKeydown"
                        @blur="setTimeout(() => showSuggestions = false, 200)"
                      />
                      
                      
                      <!-- Autocomplete suggestions -->
                      <div v-if="showSuggestions && filteredSuburbs.length > 0" 
                           class="position-absolute w-100 bg-white border rounded shadow-lg"
                           style="top: 100%; z-index: 1000; max-height: 200px; overflow-y: auto;">
                        <div v-for="(suburb, index) in filteredSuburbs" 
                             :key="suburb"
                             class="p-2 border-bottom cursor-pointer"
                             :class="{ 'bg-primary text-white': index === selectedSuggestionIndex }"
                             @click="selectSuggestion(suburb)"
                             @mouseenter="selectedSuggestionIndex = index">
                          <i class="material-icons me-2 text-muted">location_city</i>
                          {{ suburb }}
                        </div>
                      </div>
                    </div>
                  </div>
                  
                  <!-- Search button -->
                  <div class="col-md-4">
                    <MaterialButton
                      @click="searchWaterQuality"
                      variant="gradient"
                      color="success"
                      size="lg"
                      class="w-100"
                      :disabled="isLoading"
                    >
                      <i v-if="isLoading" class="material-icons me-2">hourglass_empty</i>
                      <i v-else class="material-icons me-2">search</i>
                      {{ isLoading ? "Getting Prediction..." : "Get Water Quality Prediction" }}
                    </MaterialButton>
                  </div>
                </div>
              </div>
            </div>
          </div>
        </div>

      <!-- Error Message -->
      <div v-if="errorMessage" class="row mb-4">
        <div class="col-12">
          <div class="alert alert-danger" role="alert">
            <i class="material-icons me-2">error</i>
            {{ errorMessage }}
          </div>
        </div>
      </div>

      <!-- Suburb Search Results -->
      <div v-if="showSuburbSearch && suburbSearchResults.length > 0" class="row mb-4">
        <div class="col-12">
          <div class="card shadow-sm">
            <div class="card-header bg-light">
              <h5 class="mb-0">
                <i class="material-icons me-2 text-info">location_city</i>
                Sites Found in "{{ suburbName }}"
              </h5>
            </div>
            <div class="card-body">
              <div class="row">
                <div v-for="site in suburbSearchResults" :key="site.site_id" class="col-md-6 col-lg-4 mb-3">
                  <div class="card border-primary h-100">
                    <div class="card-body text-center">
                      <h6 class="card-title">
                        <i class="material-icons me-2 text-primary">location_on</i>
                        Site ID: {{ site.site_id }}
                      </h6>
                      <p class="card-text text-muted">
                        <i class="material-icons me-2">location_city</i>
                        {{ site.nearest_suburb }}
                      </p>
                      <MaterialButton
                        @click="selectSiteFromSuburb(site.site_id)"
                        variant="gradient"
                        color="primary"
                        size="sm"
                        class="w-100"
                      >
                        <i class="material-icons me-2">analytics</i>
                        Get Prediction
                      </MaterialButton>
                    </div>
                  </div>
                </div>
              </div>
              <div v-if="suburbSearchResults.length === 0" class="text-center py-4">
                <i class="material-icons text-muted" style="font-size: 3rem;">search_off</i>
                <p class="text-muted mt-2">No sites found for "{{ suburbName }}"</p>
              </div>
            </div>
          </div>
        </div>
      </div>

      <!-- Prediction Results -->
      <div v-if="predictionResult">
        <!-- Overall Quality Card with Traffic Light Status -->
        <div class="row mb-4">
          <div class="col-12">
            <div class="card shadow-lg border-0">
              <div class="card-body p-4">
                <div class="row align-items-center">
                  <div class="col-md-6">
                    <h3 class="mb-2">
                      <i class="material-icons me-2 text-success">water_drop</i>
                      Water Quality Prediction for {{ suburbName }}
                    </h3>
                    <p class="text-muted mb-0">
                      Prediction Date: {{ predictionResult.prediction_date }}
                    </p>
                  </div>
                  <div class="col-md-6 text-end">
                    <div class="d-flex flex-column align-items-end">
                      <!-- Risk Level with Traffic Light -->
                      <div class="d-flex align-items-center mb-2">
                        <div class="traffic-light me-3">
                          <div class="light" :class="{
                            'red': predictionResult.risk_level === 'Unsafe',
                            'yellow': predictionResult.risk_level === 'Moderate', 
                            'green': predictionResult.risk_level === 'Safe'
                          }"></div>
                        </div>
                        <div class="text-end">
                          <h2 class="mb-0">{{ predictionResult.risk_level }}</h2>
                          <small class="text-muted">Risk Level</small>
                        </div>
                      </div>
                      <!-- Status Badge -->
                      <span class="badge badge-lg bg-gradient-{{ getStatusColor(predictionResult.risk_level) }}">
                        {{ predictionResult.risk_level }}
                      </span>
                    </div>
                  </div>
                </div>
                
              </div>
            </div>
          </div>
        </div>

        <!-- Water Parameters -->
        <div class="row mb-4">
          <div class="col-12">
            <div class="card shadow-lg border-0">
              <div class="card-header pb-0">
                <h5 class="mb-0">
                  <i class="material-icons me-2">science</i>
                  Water Quality Parameters
                </h5>
              </div>
              <div class="card-body">
                  <div class="row">
                    <div v-for="(value, paramName) in predictionResult.parameters" :key="paramName" class="col-md-6 mb-3">
                      <div class="d-flex align-items-start p-3 border rounded">
                        <div class="me-3">
                          <i class="material-icons text-info">
                            science
                          </i>
                        </div>
                        <div class="flex-grow-1">
                          <h6 class="mb-1">{{ paramName }}</h6>
                          <p class="mb-1">
                            <strong>{{ value.toFixed(2) }}</strong>
                            <span class="text-muted ms-2">{{ getParameterUnit(paramName) }}</span>
                          </p>
                          <p class="mb-2 text-muted small">
                            {{ getParameterDescription(paramName) }}
                          </p>
                          <span class="badge bg-info badge-sm">
                            Predicted
                          </span>
                        </div>
                      </div>
                    </div>
                  </div>
              </div>
            </div>
          </div>
        </div>

        <!-- Specific Guidance for Different Groups -->
        <div class="row mb-4">
          <div class="col-12">
            <div class="card shadow-lg border-0">
              <div class="card-header pb-0">
                <h5 class="mb-0">
                  <i class="material-icons me-2">pregnant_woman</i>
                  Pregnancy Safety Guidelines
                </h5>
              </div>
              <div class="card-body">
                <!-- Safe Level Guidelines -->
                <div v-if="predictionResult.risk_level === 'Safe'" class="row">
                  <div class="col-12">
                    <div class="card border-success">
                      <div class="card-header bg-success text-white">
                        <h6 class="mb-0">
                          <i class="material-icons me-2">check_circle</i>
                          Safe Water - Pregnancy Guidelines
                        </h6>
                      </div>
                      <div class="card-body">
                        <ul class="list-group list-group-flush">
                          <li class="list-group-item border-0 px-0 py-2">
                            <i class="material-icons me-2 text-success">check</i>
                            <strong>Safe to drink</strong> - Water quality is within safe limits for pregnant women
                          </li>
                          <li class="list-group-item border-0 px-0 py-2">
                            <i class="material-icons me-2 text-success">check</i>
                            <strong>No special precautions needed</strong> - Continue normal water consumption
                          </li>
                          <li class="list-group-item border-0 px-0 py-2">
                            <i class="material-icons me-2 text-success">check</i>
                            <strong>Monitor regularly</strong> - Continue regular water quality monitoring
                          </li>
                          <li class="list-group-item border-0 px-0 py-2">
                            <i class="material-icons me-2 text-success">check</i>
                            <strong>Stay hydrated</strong> - Maintain adequate fluid intake for healthy pregnancy
                          </li>
                        </ul>
                      </div>
                    </div>
                  </div>
                </div>

                <!-- Moderate Level Guidelines -->
                <div v-else-if="predictionResult.risk_level === 'Moderate'" class="row">
                  <div class="col-12">
                    <div class="card border-warning">
                      <div class="card-header bg-warning text-white">
                        <h6 class="mb-0">
                          <i class="material-icons me-2">warning</i>
                          Moderate Risk - Pregnancy Guidelines
                        </h6>
                      </div>
                      <div class="card-body">
                        <ul class="list-group list-group-flush">
                          <li class="list-group-item border-0 px-0 py-2">
                            <i class="material-icons me-2 text-warning">warning</i>
                            <strong>Use water filter</strong> - Install a certified water filtration system
                          </li>
                          <li class="list-group-item border-0 px-0 py-2">
                            <i class="material-icons me-2 text-warning">warning</i>
                            <strong>Boil water</strong> - Boil water for at least 1 minute before drinking
                          </li>
                          <li class="list-group-item border-0 px-0 py-2">
                            <i class="material-icons me-2 text-warning">warning</i>
                            <strong>Consult healthcare provider</strong> - Discuss water consumption with your doctor
                          </li>
                          <li class="list-group-item border-0 px-0 py-2">
                            <i class="material-icons me-2 text-warning">warning</i>
                            <strong>Monitor closely</strong> - Watch for any adverse health effects
                          </li>
                          <li class="list-group-item border-0 px-0 py-2">
                            <i class="material-icons me-2 text-warning">warning</i>
                            <strong>Consider alternatives</strong> - Use bottled water for drinking if available
                          </li>
                        </ul>
                      </div>
                    </div>
                  </div>
                </div>

                <!-- Unsafe Level Guidelines -->
                <div v-else-if="predictionResult.risk_level === 'Unsafe'" class="row">
                  <div class="col-12">
                    <div class="card border-danger">
                      <div class="card-header bg-danger text-white">
                        <h6 class="mb-0">
                          <i class="material-icons me-2">dangerous</i>
                          Unsafe Water - Pregnancy Guidelines
                        </h6>
                      </div>
                      <div class="card-body">
                        <ul class="list-group list-group-flush">
                          <li class="list-group-item border-0 px-0 py-2">
                            <i class="material-icons me-2 text-danger">block</i>
                            <strong>DO NOT DRINK</strong> - Avoid consuming this water immediately
                          </li>
                          <li class="list-group-item border-0 px-0 py-2">
                            <i class="material-icons me-2 text-danger">block</i>
                            <strong>Use bottled water only</strong> - Switch to certified bottled water
                          </li>
                          <li class="list-group-item border-0 px-0 py-2">
                            <i class="material-icons me-2 text-danger">block</i>
                            <strong>Contact healthcare provider immediately</strong> - Seek medical advice
                          </li>
                          <li class="list-group-item border-0 px-0 py-2">
                            <i class="material-icons me-2 text-danger">block</i>
                            <strong>Report to authorities</strong> - Notify local health department
                          </li>
                          <li class="list-group-item border-0 px-0 py-2">
                            <i class="material-icons me-2 text-danger">block</i>
                            <strong>Find alternative water source</strong> - Locate safe water supply
                          </li>
                          <li class="list-group-item border-0 px-0 py-2">
                            <i class="material-icons me-2 text-danger">block</i>
                            <strong>Monitor pregnancy closely</strong> - Increased medical monitoring recommended
                          </li>
                        </ul>
                      </div>
                    </div>
                  </div>
                </div>
              </div>
            </div>
          </div>
        </div>


        <!-- Action Buttons -->
        <div class="row mb-4">
          <div class="col-12 text-center">
            <MaterialButton
              @click="generatePDFReport"
              variant="gradient"
              color="info"
            >
              <i class="material-icons me-2">download</i>
              Download Result
            </MaterialButton>
          </div>
        </div>
      </div>
    </div>
  </div>

  <!-- Footer -->
  <DefaultFooter />
</template>

<style scoped>
.page-header {
  background-size: cover;
  background-position: center;
  background-attachment: fixed;
}

.cursor-pointer {
  cursor: pointer;
}

.hover-bg-light:hover {
  background-color: #f8f9fa !important;
}

.position-relative {
  position: relative;
}

/* Traffic Light Styles */
.traffic-light {
  width: 20px;
  height: 20px;
  border-radius: 50%;
  border: 2px solid #333;
  position: relative;
}

.traffic-light .light {
  width: 100%;
  height: 100%;
  border-radius: 50%;
  opacity: 0.3;
}

.traffic-light .light.red {
  background-color: #dc3545;
  opacity: 1;
}

.traffic-light .light.yellow {
  background-color: #ffc107;
  opacity: 1;
}

.traffic-light .light.green {
  background-color: #28a745;
  opacity: 1;
}

.badge-lg {
  font-size: 1rem;
  padding: 0.5rem 1rem;
}

.list-group-item {
  background: transparent;
}

.material-icons {
  vertical-align: middle;
}
</style>