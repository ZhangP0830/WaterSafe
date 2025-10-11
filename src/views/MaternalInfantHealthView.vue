<script setup>
import { ref, onMounted, onUnmounted, computed } from "vue";
import NavbarDefault from "../components/navigation/NavbarDefault.vue";
import DefaultFooter from "../components/layout/FooterDefault.vue";
import MaterialButton from "@/components/MaterialButton.vue";
import UserSelectionModal from "../components/MaternalInfantHealth/UserSelectionModal.vue";

// Import section components
import HydrationGuidance from "../components/MaternalInfantHealth/HydrationGuidance.vue";
import FeedingTracking from "../components/MaternalInfantHealth/FeedingTracking.vue";
import WaterHealthInfo from "../components/MaternalInfantHealth/WaterHealthInfo.vue";
import SymptomChecker from "../components/MaternalInfantHealth/SymptomChecker.vue";
import EmergencyTips from "../components/MaternalInfantHealth/EmergencyTips.vue";

// Import store
import { useMaternalInfantStore } from "@/stores/maternalInfantStore";

// Page state
const activeSection = ref('hydration');
const isMenuOpen = ref(false);
const store = useMaternalInfantStore();

// Navigation methods
const setActiveSection = (section) => {
  activeSection.value = section;
  isMenuOpen.value = false;
};

const scrollToSection = (sectionId) => {
  const element = document.getElementById(sectionId);
  if (element) {
    element.scrollIntoView({ behavior: 'smooth' });
  }
};

// Computed properties
const userTypeLabel = computed(() => store.userTypeLabel);

// Page lifecycle
const body = document.getElementsByTagName("body")[0];
onMounted(() => {
  body.classList.add("maternal-infant-page");
  body.classList.add("bg-light");
  store.loadUserType();
});
onUnmounted(() => {
  body.classList.remove("maternal-infant-page");
  body.classList.remove("bg-light");
});
</script>

<template>
  <!-- Navigation -->
  <div class="container position-sticky z-index-sticky top-0">
    <div class="row">
      <div class="col-12">
        <NavbarDefault :sticky="true" />
      </div>
    </div>
  </div>

  <!-- Hero Section -->
  <section class="hero-section py-5">
    <div class="container">
      <div class="row align-items-center">
        <div class="col-lg-8 mx-auto text-center">
          <div class="hero-badge mb-4">
            <span class="badge bg-gradient-primary text-white px-4 py-2 rounded-pill">
              <i class="fas fa-shield-heart me-2"></i>Maternal & Infant Health Shield
            </span>
          </div>
          <h1 class="display-3 fw-bold text-primary mb-4">
            Caring for You and Your Little One
          </h1>
          <p class="lead text-muted mb-5">
            Personalized guidance for hydration, nutrition, and health monitoring during water safety events. 
            <span v-if="userTypeLabel" class="fw-semibold text-primary">{{ userTypeLabel }}</span> - we're here to support you every step of the way.
          </p>
          <div class="hero-actions mb-5">
            <MaterialButton 
              :color="'primary'" 
              :size="'lg'"
              @click="setActiveSection('hydration')"
              class="me-3"
            >
              <i class="fas fa-play me-2"></i>Get Started
            </MaterialButton>
            <MaterialButton 
              :color="'outline-primary'" 
              :size="'lg'"
              @click="store.changeUserType"
            >
              <i class="fas fa-user-edit me-2"></i>Change Profile
            </MaterialButton>
          </div>
          <div class="hero-stats row g-4 mb-5">
            <div class="col-md-6">
              <div class="stat-item">
                <i class="fas fa-tint text-primary mb-3"></i>
                <h4 class="fw-bold">Hydration & Nutrition</h4>
                <p class="text-muted">Personalized daily guidance and safe feeding schedules</p>
              </div>
            </div>
            <div class="col-md-6">
              <div class="stat-item">
                <i class="fas fa-shield-heart text-success mb-3"></i>
                <h4 class="fw-bold">Health & Safety</h4>
                <p class="text-muted">Symptom monitoring and emergency preparedness</p>
              </div>
            </div>
          </div>
        </div>
      </div>
    </div>
  </section>

  <!-- Navigation Tabs -->
  <section class="navigation-section py-4 bg-white shadow-sm">
    <div class="container">
      <div class="row">
        <div class="col-12">
          <div class="nav-tabs-container">
            <div class="nav-tabs-wrapper">
              <button 
                v-for="tab in [
                  { id: 'hydration', label: 'Hydration Guidance', icon: 'fas fa-tint' },
                  { id: 'feeding', label: 'Feeding & Tracking', icon: 'fas fa-baby' },
                  { id: 'water-health', label: 'Water Health Info', icon: 'fas fa-info-circle' },
                  { id: 'symptoms', label: 'Symptom Checker', icon: 'fas fa-stethoscope' },
                  { id: 'emergency', label: 'Emergency Safety Guide', icon: 'fas fa-exclamation-triangle' }
                ]"
                :key="tab.id"
                @click="setActiveSection(tab.id)"
                :class="[
                  'nav-tab-btn',
                  { 'active': activeSection === tab.id }
                ]"
              >
                <i :class="tab.icon" class="me-2"></i>
                <span class="d-none d-md-inline">{{ tab.label }}</span>
                <span class="d-md-none">{{ tab.label.split(' ')[0] }}</span>
              </button>
            </div>
          </div>
        </div>
      </div>
    </div>
  </section>

  <!-- Main Content -->
  <main class="main-content py-5">
    <div class="container">
      <!-- Hydration Guidance Section -->
      <section v-if="activeSection === 'hydration'" id="hydration" class="content-section">
        <HydrationGuidance />
      </section>

      <!-- Feeding & Tracking Section -->
      <section v-if="activeSection === 'feeding'" id="feeding" class="content-section">
        <FeedingTracking />
      </section>

      <!-- Water Health Info Section -->
      <section v-if="activeSection === 'water-health'" id="water-health" class="content-section">
        <WaterHealthInfo />
      </section>

      <!-- Symptom Checker Section -->
      <section v-if="activeSection === 'symptoms'" id="symptoms" class="content-section">
        <SymptomChecker />
      </section>


      <!-- Emergency Tips Section -->
      <section v-if="activeSection === 'emergency'" id="emergency" class="content-section">
        <EmergencyTips />
      </section>
    </div>
  </main>

  <!-- Footer -->
  <DefaultFooter />

  <!-- User Selection Modal -->
  <UserSelectionModal />
</template>

<style scoped>
.maternal-infant-page {
  background: linear-gradient(135deg, #f8f9fa 0%, #e3f2fd 100%);
  min-height: 100vh;
}

/* Hero Section */
.hero-section {
  background: linear-gradient(135deg, #e3f2fd 0%, #f8f9fa 100%);
  position: relative;
  overflow: hidden;
}

.hero-section::before {
  content: '';
  position: absolute;
  top: 0;
  left: 0;
  right: 0;
  bottom: 0;
  background: url('data:image/svg+xml,<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 100 100"><defs><pattern id="grain" width="100" height="100" patternUnits="userSpaceOnUse"><circle cx="25" cy="25" r="1" fill="%23ffffff" opacity="0.1"/><circle cx="75" cy="75" r="1" fill="%23ffffff" opacity="0.1"/><circle cx="50" cy="10" r="0.5" fill="%23ffffff" opacity="0.1"/><circle cx="10" cy="60" r="0.5" fill="%23ffffff" opacity="0.1"/><circle cx="90" cy="40" r="0.5" fill="%23ffffff" opacity="0.1"/></pattern></defs><rect width="100" height="100" fill="url(%23grain)"/></svg>');
  opacity: 0.3;
}

.hero-badge .badge {
  font-size: 1rem;
  font-weight: 600;
  padding: 0.75rem 1.5rem;
  border-radius: 50px;
  box-shadow: 0 4px 15px rgba(0, 123, 255, 0.3);
  animation: gentle-pulse 3s ease-in-out infinite;
}

@keyframes gentle-pulse {
  0%, 100% { transform: scale(1); }
  50% { transform: scale(1.05); }
}

.hero-stats .stat-item {
  text-align: center;
  padding: 2rem;
  background: white;
  border-radius: 20px;
  box-shadow: 0 4px 15px rgba(0,0,0,0.1);
  transition: all 0.3s ease;
  height: 100%;
  border: 2px solid transparent;
}

.hero-stats .stat-item:hover {
  transform: translateY(-5px);
  box-shadow: 0 8px 25px rgba(0,0,0,0.15);
  border-color: #007bff;
}

.hero-stats .stat-item i {
  font-size: 3rem;
  display: block;
}

.hero-stats .stat-item h4 {
  font-size: 1.3rem;
  margin-bottom: 0.75rem;
  color: #2c3e50;
}

.hero-stats .stat-item p {
  font-size: 1rem;
  line-height: 1.5;
}

.hero-actions {
  margin-top: 2rem;
}

/* Navigation Tabs */
.navigation-section {
  border-bottom: 1px solid #e9ecef;
  position: sticky;
  top: 80px;
  z-index: 10;
}

.nav-tabs-container {
  display: flex;
  justify-content: center;
  overflow-x: auto;
  padding: 0.5rem 0;
}

.nav-tabs-wrapper {
  display: flex;
  gap: 0.5rem;
  min-width: max-content;
}

.nav-tab-btn {
  background: transparent;
  border: 2px solid #e9ecef;
  color: #6c757d;
  padding: 0.75rem 1.5rem;
  border-radius: 25px;
  font-weight: 600;
  transition: all 0.3s ease;
  white-space: nowrap;
  display: flex;
  align-items: center;
  text-decoration: none;
  cursor: pointer;
}

.nav-tab-btn:hover {
  background: #f8f9fa;
  border-color: #007bff;
  color: #007bff;
  transform: translateY(-2px);
}

.nav-tab-btn.active {
  background: linear-gradient(135deg, #007bff 0%, #0056b3 100%);
  border-color: #007bff;
  color: white;
  box-shadow: 0 4px 15px rgba(0, 123, 255, 0.3);
}

.nav-tab-btn i {
  font-size: 1.1rem;
}

/* Main Content */
.main-content {
  min-height: 60vh;
}

.content-section {
  animation: fadeInUp 0.5s ease-out;
}

@keyframes fadeInUp {
  from {
    opacity: 0;
    transform: translateY(30px);
  }
  to {
    opacity: 1;
    transform: translateY(0);
  }
}

/* Responsive Design */
@media (max-width: 768px) {
  .display-4 {
    font-size: 2.5rem;
  }
  
  .hero-stats .stat-item {
    padding: 1rem;
  }
  
  .hero-stats .stat-item i {
    font-size: 2rem;
  }
  
  .nav-tab-btn {
    padding: 0.5rem 1rem;
    font-size: 0.9rem;
  }
  
  .nav-tab-btn span {
    font-size: 0.8rem;
  }
}

@media (max-width: 576px) {
  .hero-section {
    padding: 3rem 0;
  }
  
  .hero-stats {
    margin-bottom: 2rem;
  }
  
  .nav-tabs-wrapper {
    gap: 0.25rem;
  }
  
  .nav-tab-btn {
    padding: 0.5rem 0.75rem;
    font-size: 0.8rem;
  }
}
</style>
