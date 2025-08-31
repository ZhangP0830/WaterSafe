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
        class="page-header min-vh-75"
        style="background-image: url('https://images.unsplash.com/photo-1558618666-fcd25c85cd64?ixlib=rb-4.0.3&ixid=M3wxMjA3fDB8MHxwaG90by1wYWdlfHx8fGVufDB8fHx8fA%3D%3D&auto=format&fit=crop&w=2070&q=80')"
      >
        <div class="container">
          <div class="row">
            <div class="col-lg-8 mx-auto text-center">
              <h1 class="text-white mb-4">Trusted Alternatives Finder</h1>
              <p class="text-white opacity-8 mb-4">
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
                    <div class="d-flex align-items-center">
                      <select v-model="searchRadius" class="form-select me-2" @change="updateMapRadius">
                        <option value="5">5 km</option>
                        <option value="10">10 km</option>
                        <option value="15">15 km</option>
                        <option value="20">20 km</option>
                        <option value="50">50 km</option>
                        <option value="custom">Custom</option>
                      </select>
                      <input 
                        v-if="searchRadius === 'custom'"
                        v-model="customRadius"
                        type="number"
                        min="1"
                        max="100"
                        class="form-control"
                        style="width: 80px;"
                        placeholder="km"
                        @input="updateCustomRadius"
                      />
                    </div>
                  </div>
                  
                  <!-- Status selection -->
                  <div class="col-md-6">
                    <label class="form-label">Status</label>
                    <select v-model="selectedStatus" class="form-select" @change="filterMapMarkers">
                      <option value="">All Status</option>
                      <option value="active">Active</option>
                      <option value="inactive">Inactive</option>
                      <option value="maintenance">Maintenance</option>
                      <option value="temporary">Temporary</option>
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

        <!-- Search result list -->
        <div class="row mt-4">
          <div class="col-12">
            <div class="card shadow-sm">
              <div class="card-header">
                <h5 class="mb-0">
                  <i class="material-icons me-2">location_on</i>
                  Nearby Water Sources ({{ filteredSources.length }} found)
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
                    v-for="source in filteredSources" 
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
                            <div class="d-flex align-items-center mb-2">
                              <span 
                                class="badge me-2"
                                :class="getStatusBadgeClass(source.status)"
                              >
                                {{ source.status }}
                              </span>
                              <span class="badge bg-info">{{ source.distance }}km</span>
                              <span class="badge bg-secondary ms-1">{{ source.type }}</span>
                            </div>
                          </div>
                        </div>
                        
                        <div class="mb-3">
                          <small class="text-muted">
                            <i class="material-icons me-1" style="font-size: 1rem;">category</i>
                            {{ source.suitable_use }}
                          </small>
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

// Reactive data
const searchRadius = ref(50);
const customRadius = ref(50);
const selectedStatus = ref('');
const map = ref(null);
const userLocation = ref(null);
const waterSources = ref([]);
const markers = ref([]);
const infoWindow = ref(null);
const loading = ref(false);
const error = ref(null);

// API base URL
const API_BASE_URL = import.meta.env.VITE_BACKEND_API_URL || 'http://localhost:8000';

// Get all water source data
const fetchWaterSources = async () => {
  loading.value = true;
  error.value = null;
  
  try {
    const response = await fetch(`${API_BASE_URL}/api/water-sources/with-coordinates?limit=1000`);
    if (!response.ok) {
      throw new Error(`HTTP error! status: ${response.status}`);
    }
    
    const data = await response.json();
    waterSources.value = data;
    console.log(`成功获取 ${data.length} 个水源点`);
  } catch (err) {
    error.value = `获取水源点数据失败: ${err.message}`;
    console.error('API 调用失败:', err);
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
      const radius = searchRadius.value === 'custom' ? customRadius.value : searchRadius.value;
      return s.distance <= radius;
    }).sort((a, b) => a.distance - b.distance);
  }
  
  return sources;
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
    // If there is no user location: only show the destination
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
          url: getMarkerIcon(source.type),
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

// Get marker icon
const getMarkerIcon = (type) => {
  const colors = {
    distribution: '#2196F3',
    emergency: '#F44336',
    community: '#4CAF50',
    store: '#FF9800',
    pharmacy: '#9C27B0'
  };
  
  const color = colors[type] || '#757575';
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
  console.log('搜索半径已更新:', searchRadius.value, 'km');
};

// Update custom radius
const updateCustomRadius = () => {
  if (customRadius.value && customRadius.value > 0) {
    console.log('自定义半径已更新:', customRadius.value, 'km');
  }
};

// Filter map markers
const filterMapMarkers = () => {
  if (!map.value) return;

  markers.value.forEach((marker, index) => {
    const source = waterSources.value[index];
    if (source) {
      const statusMatch = !selectedStatus.value || source.status === selectedStatus.value;
      const distanceMatch = source.distance <= searchRadius.value;
      
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
