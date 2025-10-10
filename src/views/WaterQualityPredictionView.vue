<script setup>
import { ref, onMounted, onUnmounted } from "vue";
import MaterialInput from "@/components/MaterialInput.vue";
import MaterialButton from "@/components/MaterialButton.vue";
import NavbarDefault from "../components/navigation/NavbarDefault.vue";
import DefaultFooter from "../components/layout/FooterDefault.vue";


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
const API_BASE_URL = import.meta.env.DEV ? 'http://localhost:8000/api' : '/api';

// Load available suburbs for autocomplete
const loadAvailableSuburbs = async () => {
  try {
    // Use this for deployment
    const response = await fetch(`${API_BASE_URL}/prediction/suburbs`);

    // Use this for Local
    // const response = await fetch(`http://localhost:8000/api/prediction/suburbs`);

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
  
  // Always show suggestions if user has typed 2+ characters, even if no matches
  showSuggestions.value = input.length >= 2;
  selectedSuggestionIndex.value = -1;
};

// Select suggestion
const selectSuggestion = (suburb) => {
  suburbName.value = suburb;
  showSuggestions.value = false;
  filteredSuburbs.value = [];
  selectedSuggestionIndex.value = -1;
  // Automatically trigger search after selecting
  setTimeout(() => searchWaterQuality(), 100);
};

// Handle keyboard navigation
const handleKeydown = (event) => {
  if (!showSuggestions.value) return;
  
  switch (event.key) {
    case 'ArrowDown':
      event.preventDefault();
      if (filteredSuburbs.value.length > 0) {
        selectedSuggestionIndex.value = Math.min(
          selectedSuggestionIndex.value + 1,
          filteredSuburbs.value.length - 1
        );
      }
      break;
    case 'ArrowUp':
      event.preventDefault();
      if (filteredSuburbs.value.length > 0) {
        selectedSuggestionIndex.value = Math.max(selectedSuggestionIndex.value - 1, -1);
      }
      break;
    case 'Enter':
      event.preventDefault();
      if (filteredSuburbs.value.length > 0 && selectedSuggestionIndex.value >= 0) {
        selectSuggestion(filteredSuburbs.value[selectedSuggestionIndex.value]);
        // Automatically search after selecting
        setTimeout(() => searchWaterQuality(), 100);
      } else {
        // If no suggestions available, try to search anyway
        searchWaterQuality();
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

// Parameter safety thresholds
const getParameterThresholds = (paramName) => {
  const thresholds = {
    'pH': { safe: [6.5, 8.5], warning: [6.0, 9.0], danger: [0, 14] },
    'Chloride as Cl': { safe: [0, 250], warning: [250, 500], danger: [500, Infinity] },
    'Calcium (Total)': { safe: [0, 200], warning: [200, 400], danger: [400, Infinity] },
    'Total Magnesium': { safe: [0, 150], warning: [150, 300], danger: [300, Infinity] },
    'Sodium as Na': { safe: [0, 200], warning: [200, 400], danger: [400, Infinity] },
    'Potassium as K': { safe: [0, 12], warning: [12, 24], danger: [24, Infinity] },
    'Salinity as EC@25 (lab)': { safe: [0, 500], warning: [500, 1000], danger: [1000, Infinity] }
  };
  return thresholds[paramName] || { safe: [0, 100], warning: [100, 200], danger: [200, Infinity] };
};

// Get parameter color based on value
const getParameterColor = (paramName, value) => {
  const thresholds = getParameterThresholds(paramName);
  
  if (value >= thresholds.danger[0] && value < thresholds.danger[1]) {
    return 'danger'; // Red
  } else if (value >= thresholds.warning[0] && value < thresholds.warning[1]) {
    return 'warning'; // Yellow
  } else {
    return 'success'; // Green
  }
};

// Get parameter status text
const getParameterStatus = (paramName, value) => {
  const color = getParameterColor(paramName, value);
  const statusMap = {
    'success': 'Safe',
    'warning': 'Caution',
    'danger': 'Unsafe'
  };
  return statusMap[color] || 'Unknown';
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
  
  // Check if the input matches any available suburb exactly
  const exactMatch = availableSuburbs.value.find(suburb => 
    suburb.toLowerCase() === suburbName.value.toLowerCase()
  );
  
  if (!exactMatch) {
    // If no exact match, check if there are suggestions available
    const hasSuggestions = filteredSuburbs.value.length > 0;
    if (hasSuggestions) {
      errorMessage.value = `No exact match found for "${suburbName.value}". Please select a suburb from the suggestions below.`;
      return;
    } else {
      errorMessage.value = `No suburbs found for "${suburbName.value}". Please try a different suburb name.`;
      return;
    }
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
    // Use this for deployment
    const response = await fetch(`${API_BASE_URL}/prediction/search-by-suburb`, {
      method: 'POST',
      headers: {
        'Content-Type': 'application/json',
      },
      body: JSON.stringify({
        suburb_name: suburbName.value
      })
    });

    // Use this for Local
    // const response = await fetch(`http://localhost:8000/api/prediction/search-by-suburb`, {
    //   method: 'POST',
    //   headers: {
    //     'Content-Type': 'application/json',
    //   },
    //   body: JSON.stringify({
    //     suburb_name: suburbName.value
    //   })
    // });

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

</script>

<template>
  <!-- Navigation bar -->
  <div class="container position-sticky z-index-sticky top-0 navbar-container">
    <div class="row">
      <div class="col-12">
        <NavbarDefault :sticky="true" />
      </div>
    </div>
  </div>
    

  <!-- Main content -->
  <div class="container-fluid px-4 mt-6 pt-5 main-content">
    <!-- Page Introduction -->
    <div class="row mb-4">
      <div class="col-12">
        <div class="card shadow-sm border-0">
          <div class="card-body">
            <h4 class="mb-3 text-center">
              <i class="material-icons me-2 text-info">analytics</i>
              Water Quality Prediction
            </h4>
            <p class="text-muted mb-3 text-center">
              This tool predicts water quality safety for your area. Simply enter your suburb name in the search box below and click "Search". The system will automatically find the nearest monitoring site and provide instant water quality predictions, safety ratings, and personalized guidance for pregnant women, infants, and elderly populations.
            </p>
          </div>
        </div>
      </div>
    </div>

    <!-- Left-Right Layout -->
    <div class="row">
      <!-- Left Panel: Search Input -->
      <div class="col-lg-4 mb-4">
        <div class="card shadow-lg border-0 h-100">
          <div class="card-header bg-primary text-white">
            <h5 class="mb-0">
              <i class="material-icons me-2">search</i>
              Search Area
            </h5>
          </div>
          <div class="card-body">
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
              
              <!-- Input validation feedback -->
              <div v-if="suburbName && suburbName.length > 0 && suburbName.length < 2" 
                   class="text-warning small mt-1">
                <i class="material-icons me-1" style="font-size: 16px;">info</i>
                Please enter at least 2 characters to see suggestions
              </div>
              
              <!-- Autocomplete suggestions -->
              <div v-if="showSuggestions" 
                   class="position-absolute w-100 bg-white border rounded shadow-lg"
                   style="top: 100%; z-index: 1000; max-height: 200px; overflow-y: auto;">
                <!-- Show suggestions if available -->
                <div v-if="filteredSuburbs.length > 0">
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
                <!-- Show no matches message -->
                <div v-else class="p-3 text-center text-muted">
                  <i class="material-icons me-2">search_off</i>
                  No matching suburbs found for "{{ suburbName }}"
                  <br>
                  <small class="text-muted">Please try a different suburb name</small>
                </div>
              </div>
            </div>
            
            <!-- Search button -->
            <MaterialButton
              @click="searchWaterQuality"
              variant="gradient"
              color="success"
              size="lg"
              class="w-100 mt-3"
              :disabled="isLoading || !suburbName.trim()"
            >
              <i v-if="isLoading" class="material-icons me-2">hourglass_empty</i>
              <i v-else class="material-icons me-2">search</i>
              {{ isLoading ? "Getting Prediction..." : "Get Water Quality Prediction" }}
            </MaterialButton>
          </div>
        </div>
      </div>

      <!-- Right Panel: Results Display -->
      <div class="col-lg-8 mb-4">
        <div class="card shadow-lg border-0 h-100">
          <div class="card-header bg-info text-white">
            <h5 class="mb-0">
              <i class="material-icons me-2">analytics</i>
              Prediction Results
            </h5>
          </div>
          <div class="card-body">
            <!-- Loading State -->
            <div v-if="isLoading" class="text-center py-5">
              <div class="spinner-border text-primary" role="status">
                <span class="visually-hidden">Loading...</span>
              </div>
              <p class="mt-3 text-muted">Getting water quality prediction...</p>
            </div>

            <!-- Error State -->
            <div v-else-if="errorMessage" class="text-center py-5">
              <div class="alert alert-danger" role="alert">
                <i class="material-icons me-2">error</i>
                {{ errorMessage }}
              </div>
            </div>

            <!-- No Results State -->
            <div v-else-if="!predictionResult" class="text-center py-5">
              <i class="material-icons text-muted mb-3" style="font-size: 4rem;">water_drop</i>
              <h5 class="text-muted">No Prediction Results</h5>
              <p class="text-muted">Enter a suburb name and click search to get water quality predictions</p>
            </div>

            <!-- Results Display -->
            <div v-else>
              <!-- Overall Quality Card with Traffic Light Status -->
              <div class="row mb-4">
                <div class="col-12">
                  <div class="card border-0 bg-light">
                    <div class="card-body p-4">
                      <div class="row align-items-center">
                        <div class="col-md-8">
                          <h3 class="mb-2">
                            <i class="material-icons me-2 text-success">water_drop</i>
                            Water Quality Prediction for {{ suburbName }}
                          </h3>
                          <p class="text-muted mb-0">
                            Prediction Date: {{ predictionResult.prediction_date }}
                          </p>
                        </div>
                        <div class="col-md-4 text-end">
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
              <div class="row">
                <div class="col-12">
                  <h5 class="mb-3">
                    <i class="material-icons me-2">science</i>
                    Water Quality Parameters
                  </h5>
                  <div class="row">
                    <div v-for="(value, paramName) in predictionResult.parameters" :key="paramName" class="col-md-6 mb-3">
                      <div class="d-flex align-items-start p-3 border rounded parameter-card" 
                           :class="`border-${getParameterColor(paramName, value)} bg-light-${getParameterColor(paramName, value)}`">
                        <div class="me-3">
                          <div class="parameter-indicator" :class="`bg-${getParameterColor(paramName, value)}`">
                            <i class="material-icons text-white">
                              {{ getParameterColor(paramName, value) === 'success' ? 'check_circle' : 
                                 getParameterColor(paramName, value) === 'warning' ? 'warning' : 'error' }}
                            </i>
                          </div>
                        </div>
                        <div class="flex-grow-1">
                          <div class="d-flex justify-content-between align-items-center mb-1">
                            <h6 class="mb-0">{{ paramName }}</h6>
                            <span class="badge" :class="`bg-${getParameterColor(paramName, value)}`">
                              {{ getParameterStatus(paramName, value) }}
                            </span>
                          </div>
                          <p class="mb-1">
                            <strong class="parameter-value" :class="`text-${getParameterColor(paramName, value)}`">
                              {{ value.toFixed(2) }}
                            </strong>
                            <span class="text-muted ms-2">{{ getParameterUnit(paramName) }}</span>
                          </p>
                          <p class="mb-2 text-muted small">
                            {{ getParameterDescription(paramName) }}
                          </p>
                        </div>
                      </div>
                    </div>
                  </div>
                </div>
              </div>
            </div>
          </div>
        </div>
      </div>
    </div>

    <!-- Guidelines Section at Bottom -->
    <div v-if="predictionResult" class="row">
      <div class="col-12">

        <!-- Pregnancy Safety Guidelines -->
        <div class="mt-4">
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

  <!-- Footer -->
  <DefaultFooter />
</template>

<style scoped>
/* Ensure proper spacing between navigation and content */
.navbar-container {
  margin-bottom: 3rem;
}

.main-content {
  margin-top: 4rem;
  padding-top: 2rem;
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

/* Parameter color styling */
.parameter-card {
  transition: all 0.3s ease;
}

.parameter-card:hover {
  transform: translateY(-2px);
  box-shadow: 0 4px 12px rgba(0,0,0,0.1);
}

.parameter-indicator {
  width: 40px;
  height: 40px;
  border-radius: 50%;
  display: flex;
  align-items: center;
  justify-content: center;
  box-shadow: 0 2px 8px rgba(0,0,0,0.15);
}

.parameter-value {
  font-size: 1.1rem;
  font-weight: 600;
}

/* Background colors for parameter cards */
.bg-light-success {
  background-color: rgba(40, 167, 69, 0.1) !important;
}

.bg-light-warning {
  background-color: rgba(255, 193, 7, 0.1) !important;
}

.bg-light-danger {
  background-color: rgba(220, 53, 69, 0.1) !important;
}

/* Border colors */
.border-success {
  border-color: rgba(40, 167, 69, 0.3) !important;
}

.border-warning {
  border-color: rgba(255, 193, 7, 0.3) !important;
}

.border-danger {
  border-color: rgba(220, 53, 69, 0.3) !important;
}

/* Text colors */
.text-success {
  color: #28a745 !important;
}

.text-warning {
  color: #ffc107 !important;
}

.text-danger {
  color: #dc3545 !important;
}

/* Badge colors */
.bg-success {
  background-color: #28a745 !important;
}

.bg-warning {
  background-color: #ffc107 !important;
  color: #212529 !important;
}

.bg-danger {
  background-color: #dc3545 !important;
}
</style>