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
              Trusted Alternatives Finder
            </h1>
              <p class="lead text-white px-5 mt-4 mb-5" :style="{ fontWeight: '500', fontSize: '1.25rem' }">
                Find safe drinking water sources near you during water advisories
              </p>
            </div>
          </div>
        </div>
      </div>
    </Header>

    <!-- Main content -->
    <div class="card card-body blur shadow-blur mx-3 mx-md-4 mt-n6">
      <div class="container">
        <!-- Search control panel -->
        <div class="row mb-4">
          <div class="col-12">
            <div class="card shadow-sm">
              <div class="card-body">
                <div class="row align-items-end">
                  <!-- Search radius selection -->
                  <div class="col-md-6">
                    <label class="form-label">Search Radius</label>
                    <select v-model="searchRadius" class="form-select" @change="updateMapRadius">
                      <option value="all">All</option>
                      <option value="5">5 km</option>
                      <option value="10">10 km</option>
                      <option value="15">15 km</option>
                      <option value="20">20 km</option>
                      <option value="50">50 km</option>
                    </select>
                  </div>
                  
                  <!-- Status selection -->
                  <div class="col-md-6">
                    <label class="form-label">Status</label>
                    <select v-model="selectedStatus" class="form-select" @change="filterMapMarkers">
                      <option value="">All Status</option>
                      <option value="Decommissioned">Decommissioned</option>
                      <option value="Non-operational">Non-operational</option>
                      <option value="Operational">Operational</option>
                      <option value="Operational - partial">Operational - partial</option>
                      <option value="Operational - proposed to decommission">Operational - proposed to decommission</option>
                      <option value="Operational - Requires Metered Hydrant">Operational - Requires Metered Hydrant</option>
                      <option value="Operational (Temporary)">Operational (Temporary)</option>
                    </select>
                  </div>
                </div>
              </div>
            </div>
          </div>
        </div>

        <!-- Map -->
        <div class="row">
          <div class="col-12">
            <div class="card shadow-sm">
              <div class="card-body p-0">
                <div id="map" style="height: 600px; width: 100%;"></div>
              </div>
            </div>
          </div>
        </div>
        
        <!-- Map Legend -->
        <div class="row mt-3">
          <div class="col-12">
            <div class="card shadow-sm">
              <div class="card-body py-3">
                <h6 class="mb-3">
                  <i class="material-icons me-2">legend_toggle</i>
                  Map Legend - Status Colors
                </h6>
                <div class="row">
                  <div class="col-md-6 col-lg-3 mb-2">
                    <div class="d-flex align-items-center">
                      <div class="me-2" style="width: 20px; height: 20px; background-color: #4CAF50; border-radius: 50%; border: 2px solid white; box-shadow: 0 0 0 2px #4CAF50;"></div>
                      <small class="text-muted">Operational</small>
                    </div>
                  </div>
                  <div class="col-md-6 col-lg-3 mb-2">
                    <div class="d-flex align-items-center">
                      <div class="me-2" style="width: 20px; height: 20px; background-color: #8BC34A; border-radius: 50%; border: 2px solid white; box-shadow: 0 0 0 2px #8BC34A;"></div>
                      <small class="text-muted">Partial</small>
                    </div>
                  </div>
                  <div class="col-md-6 col-lg-3 mb-2">
                    <div class="d-flex align-items-center">
                      <div class="me-2" style="width: 20px; height: 20px; background-color: #FF9800; border-radius: 50%; border: 2px solid white; box-shadow: 0 0 0 2px #FF9800;"></div>
                      <small class="text-muted">Proposed Decommission</small>
                    </div>
                  </div>
                  <div class="col-md-6 col-lg-3 mb-2">
                    <div class="d-flex align-items-center">
                      <div class="me-2" style="width: 20px; height: 20px; background-color: #2196F3; border-radius: 50%; border: 2px solid white; box-shadow: 0 0 0 2px #2196F3;"></div>
                      <small class="text-muted">Requires Meter</small>
                    </div>
                  </div>
                  <div class="col-md-6 col-lg-3 mb-2">
                    <div class="d-flex align-items-center">
                      <div class="me-2" style="width: 20px; height: 20px; background-color: #9C27B0; border-radius: 50%; border: 2px solid white; box-shadow: 0 0 0 2px #9C27B0;"></div>
                      <small class="text-muted">Temporary</small>
                    </div>
                  </div>
                  <div class="col-md-6 col-lg-3 mb-2">
                    <div class="d-flex align-items-center">
                      <div class="me-2" style="width: 20px; height: 20px; background-color: #F44336; border-radius: 50%; border: 2px solid white; box-shadow: 0 0 0 2px #F44336;"></div>
                      <small class="text-muted">Non-operational</small>
                    </div>
                  </div>
                  <div class="col-md-6 col-lg-3 mb-2">
                    <div class="d-flex align-items-center">
                      <div class="me-2" style="width: 20px; height: 20px; background-color: #9E9E9E; border-radius: 50%; border: 2px solid white; box-shadow: 0 0 0 2px #9E9E9E;"></div>
                      <small class="text-muted">Decommissioned</small>
                    </div>
                  </div>
                </div>
              </div>
            </div>
          </div>
        </div>

        <!-- Search result list -->
        <div class="row mt-4">
          <div class="col-12">
            <div class="card shadow-sm">
              <div class="card-header">
                <h5 class="mb-0">
                  <i class="material-icons me-2">location_on</i>
                  Nearby Water Sources ({{ filteredSources.length }} found, {{ displayedSources.length }} displayed)
                </h5>
              </div>
              <div class="card-body">
                <!-- Loading state -->
                <div v-if="loading" class="text-center py-4">
                  <div class="spinner-border text-primary" role="status">
                    <span class="visually-hidden">Loading...</span>
                  </div>
                  <p class="text-muted mt-2">Loading water source data...</p>
                </div>
                
                <!-- Error state -->
                <div v-else-if="error" class="text-center py-4">
                  <i class="material-icons text-danger" style="font-size: 3rem;">error</i>
                  <p class="text-danger mt-2">{{ error }}</p>
                  <button @click="fetchWaterSources" class="btn btn-outline-primary btn-sm">
                    <i class="material-icons me-1">refresh</i>
                    Retry
                  </button>
                </div>
                
                <!-- No data state -->
                <div v-else-if="filteredSources.length === 0" class="text-center py-4">
                  <i class="material-icons text-muted" style="font-size: 3rem;">water_drop</i>
                  <p class="text-muted mt-2">No water sources found in your area</p>
                </div>
                
                <div v-else class="row">
                  <div 
                    v-for="source in displayedSources" 
                    :key="source.id"
                    class="col-md-6 col-lg-4 mb-3"
                  >
                    <div class="card h-100 border-0 shadow-sm">
                      <div class="card-body">
                        <div class="d-flex align-items-start mb-3">
                          <div class="me-3">
                            <i 
                              :class="getSourceIcon(source.type)"
                              :style="{ color: getSourceColor(source.type) }"
                              style="font-size: 2rem;"
                            ></i>
                          </div>
                          <div class="flex-grow-1">
                            <h6 class="card-title mb-1">{{ source.site_name }}</h6>
                            <p class="text-muted small mb-2">{{ source.address }}</p>
                            <p class="text-muted small mb-1">{{ source.near_town }}, {{ source.lga }}</p>
                            <div class="mb-2">
                              <div class="d-flex align-items-center mb-1">
                                <span class="fw-bold text-dark me-2">Status:</span>
                                <span class="text-muted">{{ source.status }}</span>
                              </div>
                              <div class="d-flex align-items-center mb-1">
                                <span class="fw-bold text-dark me-2">Suitable Use:</span>
                                <span class="text-muted">{{ source.suitable_use }}</span>
                              </div>
                              <div class="d-flex align-items-center mb-1">
                                <span class="fw-bold text-dark me-2">Distance:</span>
                                <span class="text-muted">{{ source.distance }}km</span>
                              </div>
                              <div class="d-flex align-items-center mb-1">
                                <span class="fw-bold text-dark me-2">Type:</span>
                                <span class="text-muted">{{ source.type }}</span>
                              </div>
                            </div>
                          </div>
                        </div>
                        
                        <div class="d-flex justify-content-center">
                          <button 
                            @click="getDirections(source)"
                            class="btn btn-outline-primary btn-sm"
                            style="width: 35%;"
                          >
                            <i class="material-icons me-1" style="font-size: 1rem;">directions</i>
                            Directions
                          </button>
                        </div>
                      </div>
                    </div>
                  </div>
                </div>
                
                <!-- Display More Button -->
                <div v-if="hasMoreSources" class="text-center mt-4">
                  <button 
                    @click="displayMore"
                    class="btn btn-outline-primary"
                  >
                    <i class="material-icons me-2">expand_more</i>
                    Display More ({{ filteredSources.length - displayedSources.length }} remaining)
                  </button>
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

<script setup>
import { ref, onMounted, computed, watch } from 'vue';
import { Loader } from '@googlemaps/js-api-loader';
import NavbarDefault from "../components/navigation/NavbarDefault.vue";
import Header from "../components/layout/Header.vue";
import DefaultFooter from "../components/layout/FooterDefault.vue";
import heroBg from "@/assets/img/trusted-background.png";

// Reactive data
const searchRadius = ref('all');
const selectedStatus = ref('');
const map = ref(null);
const userLocation = ref(null);
const waterSources = ref([]);
const markers = ref([]);
const infoWindow = ref(null);
const loading = ref(false);
const error = ref(null);
const displayedCount = ref(6);

// API base URL - Auto-detect environment
const API_BASE_URL = import.meta.env.VITE_BACKEND_API_URL || 
  (import.meta.env.DEV ? 'http://localhost:8000' : '/api');

// Get all water source data
const fetchWaterSources = async () => {
  loading.value = true;
  error.value = null;
  
  try {
    // Use this for deployment
    const response = await fetch(`${API_BASE_URL}/water-sources/with-coordinates?limit=1000`);
    
    // Use this for local development
    // const response = await fetch(`http://localhost:8000/api/water-sources/with-coordinates?limit=1000`);
    if (!response.ok) {
      throw new Error(`HTTP error! status: ${response.status}`);
    }
    
    const data = await response.json();
    waterSources.value = data;
    console.log(`successfully got ${data.length} water sources`);
  } catch (err) {
    error.value = `failed to get water source data: ${err.message}`;
    console.error('API call failed:', err);
  } finally {
    loading.value = false;
  }
};

// Computed property
const filteredSources = computed(() => {
  let sources = waterSources.value;
  
  if (selectedStatus.value) {
    sources = sources.filter(s => s.status === selectedStatus.value);
  }
  
  // Calculate distance (based on user location)
  if (userLocation.value) {
    sources = sources.map(source => {
      const distance = calculateDistance(
        userLocation.value.lat,
        userLocation.value.lng,
        source.lat,
        source.lon
      );
      return { ...source, distance: Math.round(distance * 10) / 10 };
    }).filter(s => {
      if (searchRadius.value === 'all') return true;
      const radius = parseInt(searchRadius.value);
      return s.distance <= radius;
    }).sort((a, b) => a.distance - b.distance);
  }
  
  return sources;
});

// Computed property for displayed sources (with pagination)
const displayedSources = computed(() => {
  return filteredSources.value.slice(0, displayedCount.value);
});

// Check if there are more sources to display
const hasMoreSources = computed(() => {
  return displayedCount.value < filteredSources.value.length;
});

// Calculate distance (in kilometers)
const calculateDistance = (lat1, lon1, lat2, lon2) => {
  const R = 6371;
  const dLat = (lat2 - lat1) * Math.PI / 180;
  const dLon = (lon2 - lon1) * Math.PI / 180;
  const a = 
    Math.sin(dLat/2) * Math.sin(dLat/2) +
    Math.cos(lat1 * Math.PI / 180) * Math.cos(lat2 * Math.PI / 180) * 
    Math.sin(dLon/2) * Math.sin(dLon/2);
  const c = 2 * Math.atan2(Math.sqrt(a), Math.sqrt(1-a));
  return R * c;
};

// Get water source icon
const getSourceIcon = (type) => {
  const icons = {
    distribution: 'local_shipping',
    emergency: 'emergency',
    community: 'people',
    store: 'store',
    pharmacy: 'local_pharmacy'
  };
  return `material-icons ${icons[type] || 'water_drop'}`;
};

// Get water source color
const getSourceColor = (type) => {
  const colors = {
    distribution: '#2196F3',
    emergency: '#F44336',
    community: '#4CAF50',
    store: '#FF9800',
    pharmacy: '#9C27B0'
  };
  return colors[type] || '#757575';
};

// Get status badge style
const getStatusBadgeClass = (status) => {
  const classes = {
    active: 'bg-success',
    inactive: 'bg-danger',
    maintenance: 'bg-warning',
    temporary: 'bg-info'
  };
  return classes[status] || 'bg-secondary';
};



// Display more sources
const displayMore = () => {
  displayedCount.value += 6;
};

// Get navigation direction
const getDirections = (source) => {
  // Build Google Maps navigation link
  const destination = `${source.lat},${source.lon}`;
  const destinationName = encodeURIComponent(source.site_name);
  
  // If there is a user location, use the user location as the starting point
  let googleMapsUrl;
  if (userLocation.value) {
    // If there is a user location: navigate from the user location to the destination
    const origin = `${userLocation.value.lat},${userLocation.value.lng}`;
    googleMapsUrl = `https://www.google.com/maps/dir/${origin}/${destination}/${destinationName}`;
  } else {
    // If there is a user location: only show the destination
    googleMapsUrl = `https://www.google.com/maps/search/?api=1&query=${destination}`;
  }
  
  // Open Google Maps in a new tab
  window.open(googleMapsUrl, '_blank');
};



// Initialize Google Maps
const initMap = async () => {
  try {
    const loader = new Loader({
      apiKey: import.meta.env.VITE_GOOGLE_MAPS_API_KEY || 'YOUR_GOOGLE_MAPS_API_KEY',
      version: 'weekly',
      libraries: ['places']
    });

    const google = await loader.load();
    
    // Default center location (Melbourne)
    const defaultCenter = { lat: -37.8136, lng: 144.9631 };
    
    // Create map
    map.value = new google.maps.Map(document.getElementById('map'), {
      center: userLocation.value ? 
        { lat: userLocation.value.lat, lng: userLocation.value.lng } : 
        defaultCenter,
      zoom: 12,
      styles: [
        {
          featureType: 'poi',
          elementType: 'labels',
          stylers: [{ visibility: 'off' }]
        }
      ]
    });

    // Create info window
    infoWindow.value = new google.maps.InfoWindow();

    // Add water source markers
    addWaterSourceMarkers();

    // Add user location marker
    if (userLocation.value) {
      addUserLocationMarker();
    }

  } catch (error) {
    console.error('Error loading Google Maps:', error);
    const mapElement = document.getElementById('map');
    if (mapElement) {
      mapElement.innerHTML = `
        <div class="d-flex align-items-center justify-content-center h-100 bg-light">
          <div class="text-center">
            <i class="material-icons text-danger" style="font-size: 4rem;">error</i>
            <p class="text-danger mt-2">Failed to load Google Maps</p>
            <p class="text-muted small">Please check your API key and internet connection</p>
          </div>
        </div>
      `;
    }
  }
};

// Add water source markers
const addWaterSourceMarkers = () => {
  if (!map.value) return;

  // Clear existing markers
  markers.value.forEach(marker => marker.setMap(null));
  markers.value = [];

  waterSources.value.forEach(source => {
    // Only add sources with coordinates
    if (source.lat && source.lon) {
      const marker = new google.maps.Marker({
        position: { lat: source.lat, lng: source.lon },
        map: map.value,
        title: source.site_name,
        icon: {
          url: getMarkerIcon(source.status),
          scaledSize: new google.maps.Size(32, 32)
        }
      });

      // Add click event
      marker.addListener('click', () => {
        // Display basic information, including distance
        let distanceText = 'Unknown';
        if (userLocation.value && source.lat && source.lon) {
          const distance = calculateDistance(
            userLocation.value.lat,
            userLocation.value.lng,
            source.lat,
            source.lon
          );
          distanceText = `${Math.round(distance * 10) / 10}km`;
        }
        
        const content = `
          <div style="padding: 10px; max-width: 250px;">
            <h6 style="margin: 0 0 8px 0;">${source.site_name}</h6>
            <p style="margin: 0 0 5px 0; font-size: 12px; color: #666;">${source.address}</p>
            <p style="margin: 0 0 5px 0; font-size: 12px; color: #666;">${source.near_town}, ${source.lga}</p>
            <p style="margin: 0 0 5px 0; font-size: 12px;">
              <strong>Type:</strong> ${source.type}<br>
              <strong>Status:</strong> ${source.status}<br>
              <strong>Suitable Use:</strong> ${source.suitable_use}<br>
              <strong>Distance:</strong> ${distanceText}
            </p>
          </div>
        `;
        infoWindow.value.setContent(content);
        infoWindow.value.open(map.value, marker);
      });

      markers.value.push(marker);
    }
  });
  
  console.log(`添加了 ${markers.value.length} 个地图标记`);
};

// Get marker icon based on status
const getMarkerIcon = (status) => {
  const statusColors = {
    'Operational': '#4CAF50',                 
    'Operational - partial': '#8BC34A',
    'Operational - proposed to decommission': '#FF9800',
    'Operational - Requires Metered Hydrant': '#2196F3',
    'Operational (Temporary)': '#9C27B0',
    'Non-operational': '#F44336',
    'Decommissioned': '#9E9E9E'
  };
  
  const color = statusColors[status] || '#757575';
  return `data:image/svg+xml;charset=UTF-8,${encodeURIComponent(`
    <svg width="32" height="32" viewBox="0 0 32 32" xmlns="http://www.w3.org/2000/svg">
      <circle cx="16" cy="16" r="14" fill="${color}" stroke="white" stroke-width="2"/>
      <path d="M16 8l-2 2v6l2 2 2-2v-6l-2-2z" fill="white"/>
      <circle cx="16" cy="20" r="2" fill="white"/>
    </svg>
  `)}`;
};

// Add user location marker
const addUserLocationMarker = () => {
  if (!map.value || !userLocation.value) return;

  const userMarker = new google.maps.Marker({
    position: { lat: userLocation.value.lat, lng: userLocation.value.lng },
    map: map.value,
    title: 'Your Location',
    icon: {
      url: 'data:image/svg+xml;charset=UTF-8,' + encodeURIComponent(`
        <svg width="32" height="32" viewBox="0 0 32 32" xmlns="http://www.w3.org/2000/svg">
          <circle cx="16" cy="16" r="14" fill="#FF5722" stroke="white" stroke-width="2"/>
          <circle cx="16" cy="16" r="6" fill="white"/>
        </svg>
      `),
      scaledSize: new google.maps.Size(32, 32)
    }
  });

  markers.value.push(userMarker);
};



// Update map search radius (no longer creating circles)
const updateMapRadius = () => {
  displayedCount.value = 6; // Reset to show first 6 results
  filterMapMarkers();
};



// Filter map markers
const filterMapMarkers = () => {
  if (!map.value) return;

  console.log('Applying filters:', { 
    status: selectedStatus.value, 
    radius: searchRadius.value 
  });

  markers.value.forEach((marker, index) => {
    const source = waterSources.value[index];
    if (source && marker) {
      const statusMatch = !selectedStatus.value || source.status === selectedStatus.value;
      
      // Calculate distance if user location is available
      let distanceMatch = true;
      if (userLocation.value && searchRadius.value !== 'all') {
        const distance = calculateDistance(
          userLocation.value.lat,
          userLocation.value.lng,
          source.lat,
          source.lon
        );
        const radius = parseInt(searchRadius.value);
        distanceMatch = distance <= radius;
        
        console.log(`Source ${source.site_name}: status=${statusMatch}, distance=${distance}km <= ${radius}km = ${distanceMatch}`);
      }
      
      marker.setMap(statusMatch && distanceMatch ? map.value : null);
    }
  });
};

// Get user location
const getUserLocation = () => {
  if (navigator.geolocation) {
    navigator.geolocation.getCurrentPosition(
      (position) => {
        userLocation.value = {
          lat: position.coords.latitude,
          lng: position.coords.longitude
        };
        console.log('User location:', userLocation.value);
        
        // If map is loaded, update user location
        if (map.value) {
          map.value.setCenter({ lat: userLocation.value.lat, lng: userLocation.value.lng });
          addUserLocationMarker();
        }
      },
      (error) => {
        console.error('Error getting location:', error);
      }
    );
  }
};

// Watch filter changes
watch([selectedStatus, searchRadius], () => {
  displayedCount.value = 6; // Reset to show first 6 results
  filterMapMarkers();
});

// Initialize after component mount
onMounted(async () => {
  // First get water sources data
  await fetchWaterSources();
  
  // Then get user location and initialize map
  getUserLocation();
  initMap();
});
</script>

<style scoped>
.card {
  transition: transform 0.2s ease;
}

.card:hover {
  transform: translateY(-2px);
}

.badge {
  font-size: 0.75rem;
}

#map {
  border-radius: 0.5rem;
}

:deep(.gm-style) {
  border-radius: 0.5rem;
}
</style>
