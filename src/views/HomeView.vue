<script setup>
import { onMounted, onUnmounted } from "vue";

// 导入组件
import NavbarDefault from "../components/navigation/NavbarDefault.vue";
import DefaultFooter from "../components/layout/FooterDefault.vue";
import Header from "../components/layout/Header.vue";
import FilledInfoCard from "../components/cards/infoCards/FilledInfoCard.vue";
import MaterialButton from "@/components/MaterialButton.vue";
import HomeInformation from "../components/HomeSection/HomeInformation.vue";
import HomeIntroduction from "../components/HomeSection/HomeIntroduction.vue";
// 导入视频资源
import heroVideo from "@/assets/video/opening_page_video_with_mother_infant.mp4";

// 页面生命周期
const body = document.getElementsByTagName("body")[0];
onMounted(() => {
  body.classList.add("home-page");
  body.classList.add("bg-gray-100");
});
onUnmounted(() => {
  body.classList.remove("home-page");
  body.classList.remove("bg-gray-100");
});

// Methods - removed scrollToLearnMore as Learn More buttons are no longer used
</script>

<template>
  <!-- navbar -->
  <div class="container position-sticky z-index-sticky top-0">
    <div class="row">
      <div class="col-12">
        <NavbarDefault :sticky="true" />
      </div>
    </div>
  </div>

  <!-- hero section -->
  <Header>
    <div class="page-header min-vh-100 hero-video-container">
      <!-- Video Background -->
      <video
        class="hero-video"
        :src="heroVideo"
        autoplay
        muted
        loop
        playsinline
        preload="metadata"
        aria-label="Water safety video background"
      >
        <!-- Fallback for browsers that don't support video -->
        <div class="hero-fallback">
          <div class="container">
            <div class="row justify-content-center align-items-center min-vh-100">
              <div class="col-lg-8 col-xl-6 text-center">
                <div class="hero-text-block">
                  <h1 class="hero-title">WaterSafe</h1>
                  <p class="hero-subtitle">Protecting Families from Water Contamination Risks</p>
                </div>
              </div>
            </div>
          </div>
        </div>
      </video>
      
      <!-- Content with Dark Black Block -->
      <div class="hero-content">
        <div class="container">
          <div class="row justify-content-center align-items-center min-vh-100">
            <div class="col-lg-8 col-xl-6 text-center">
                <div class="hero-text-block">
                  <h1 class="hero-title">
                    WaterSafe
                  </h1>
                  <p class="hero-subtitle">
                    Protecting Families from Water Contamination Risks
                  </p>
                </div>
            </div>
          </div>
        </div>
      </div>
    </div>
  </Header>

    <!-- main content section -->
  <div class="card card-body blur shadow-blur mx-3 mx-md-4 mt-n3 content-section">
    <!-- here you can add your content -->
     <div class="pt-4">
       <HomeIntroduction />
     </div>
     <HomeInformation />
     
     <!-- Sanitation Support Feature Section -->
     <section class="sanitation-feature-section py-5">
       <div class="container">
         <div class="row align-items-center">
           <div class="col-lg-6">
             <div class="sanitation-content">
               <div class="feature-badge mb-3">
                 <span class="badge bg-warning text-dark px-3 py-2">
                   <i class="fas fa-shield-alt me-2"></i>New Feature
                 </span>
               </div>
               <h2 class="display-6 fw-bold text-primary mb-4">
                 Safe Sanitation & Hygiene Support
               </h2>
               <p class="lead text-muted mb-4">
                 Get personalized hygiene guidance for pregnant women, infants, and families during sanitation disruptions. 
                 Choose your situation and location to receive tailored checklists and safety instructions.
               </p>
               <div class="feature-highlights mb-4">
                 <div class="row g-3">
                   <div class="col-md-6">
                     <div class="highlight-item">
                       <i class="fas fa-tools text-primary me-2"></i>
                       <span>General & Emergency Modes</span>
                     </div>
                   </div>
                   <div class="col-md-6">
                     <div class="highlight-item">
                       <i class="fas fa-baby text-success me-2"></i>
                       <span>Pregnancy & Infant Care</span>
                     </div>
                   </div>
                   <div class="col-md-6">
                     <div class="highlight-item">
                       <i class="fas fa-hands-wash text-info me-2"></i>
                       <span>Hygiene Micro-Flows</span>
                     </div>
                   </div>
                   <div class="col-md-6">
                     <div class="highlight-item">
                       <i class="fas fa-download text-warning me-2"></i>
                       <span>Offline Access</span>
                     </div>
                   </div>
                 </div>
               </div>
               <div class="cta-buttons">
                 <router-link to="/sanitation-support" class="btn btn-primary btn-lg">
                   <i class="fas fa-magic me-2"></i>Get Your Checklist
                 </router-link>
               </div>
             </div>
           </div>
           <div class="col-lg-6">
             <div class="sanitation-visual">
               <div class="feature-cards">
                 <div class="feature-card mode-card">
                   <div class="card-icon">
                     <i class="fas fa-tools"></i>
                   </div>
                   <h5>Choose Mode</h5>
                   <p>General or Emergency</p>
                 </div>
                 <div class="feature-card place-card">
                   <div class="card-icon">
                     <i class="fas fa-home"></i>
                   </div>
                   <h5>Select Location</h5>
                   <p>Home, Camp, or Shelter</p>
                 </div>
                 <div class="feature-card result-card">
                   <div class="card-icon">
                     <i class="fas fa-check-circle"></i>
                   </div>
                   <h5>Get Guidance</h5>
                   <p>Personalized Checklist</p>
                 </div>
               </div>
             </div>
           </div>
         </div>
       </div>
     </section>

     <!-- Maternal & Infant Health Shield Feature Section -->
     <section class="maternal-infant-feature-section py-5">
       <div class="container">
         <div class="row align-items-center">
           <div class="col-lg-6">
             <div class="maternal-infant-visual">
               <div class="feature-cards">
                 <div class="feature-card hydration-card">
                   <div class="card-icon">
                     <i class="fas fa-tint"></i>
                   </div>
                   <h5>Hydration Guidance</h5>
                   <p>Trimester-specific advice</p>
                 </div>
                 <div class="feature-card feeding-card">
                   <div class="card-icon">
                     <i class="fas fa-baby"></i>
                   </div>
                   <h5>Feeding & Tracking</h5>
                   <p>Safe feeding schedules</p>
                 </div>
                 <div class="feature-card health-card">
                   <div class="card-icon">
                     <i class="fas fa-stethoscope"></i>
                   </div>
                   <h5>Health Monitoring</h5>
                   <p>Symptom checker & tips</p>
                 </div>
               </div>
             </div>
           </div>
           <div class="col-lg-6">
             <div class="maternal-infant-content">
               <div class="feature-badge mb-3">
                 <span class="badge bg-success text-white px-3 py-2">
                   <i class="fas fa-shield-heart me-2"></i>Latest Feature
                 </span>
               </div>
               <h2 class="display-6 fw-bold text-success mb-4">
                 Maternal & Infant Health Shield
               </h2>
               <p class="lead text-muted mb-4">
                 Comprehensive protection for pregnant women and infants during water safety disruptions. 
                 Get personalized hydration, nutrition, hygiene, and health support in one integrated shield.
               </p>
               <div class="feature-highlights mb-4">
                 <div class="row g-3">
                   <div class="col-md-6">
                     <div class="highlight-item">
                       <i class="fas fa-tint text-success me-2"></i>
                       <span>Trimester-Specific Hydration</span>
                     </div>
                   </div>
                   <div class="col-md-6">
                     <div class="highlight-item">
                       <i class="fas fa-baby text-info me-2"></i>
                       <span>Safe Feeding Schedules</span>
                     </div>
                   </div>
                   <div class="col-md-6">
                     <div class="highlight-item">
                       <i class="fas fa-stethoscope text-warning me-2"></i>
                       <span>Symptom Checker</span>
                     </div>
                   </div>
                   <div class="col-md-6">
                     <div class="highlight-item">
                       <i class="fas fa-exclamation-triangle text-danger me-2"></i>
                       <span>Emergency Action Cards</span>
                     </div>
                   </div>
                 </div>
               </div>
               <div class="cta-buttons">
                 <router-link to="/maternal-infant-health" class="btn btn-success btn-lg">
                   <i class="fas fa-shield-heart me-2"></i>Get Your Shield
                 </router-link>
               </div>
             </div>
           </div>
         </div>
       </div>
     </section>
  </div>

  <!-- footer -->
  <DefaultFooter />
</template>

<style scoped>
.bg-gray-100 {
  background-color: #f8f9fa !important;
}

.bg-gray-200 {
  background-color: #e9ecef !important;
}

/* Hero Video Container */
.hero-video-container {
  position: relative;
  overflow: hidden;
  display: flex;
  align-items: center;
  justify-content: center;
  margin-bottom: 2rem;
}

/* Hero Video Styling */
.hero-video {
  position: absolute;
  top: 50%;
  left: 50%;
  min-width: 100%;
  min-height: 100%;
  width: auto;
  height: auto;
  transform: translate(-50%, -50%);
  z-index: 1;
  object-fit: cover;
  filter: brightness(1) contrast(1);
}

/* Hero Content */
.hero-content {
  position: relative;
  z-index: 2;
  width: 100%;
  height: 100%;
  display: flex;
  align-items: center;
  justify-content: center;
}

/* Dark Black Text Block */
.hero-text-block {
  background: rgba(26, 26, 26, 0.4); /* Dark black with much reduced opacity */
  padding: 3rem 2.5rem;
  border-radius: 20px;
  box-shadow: 
    0 20px 40px rgba(0, 0, 0, 0.2),
    0 10px 20px rgba(0, 0, 0, 0.15),
    inset 0 1px 0 rgba(255, 255, 255, 0.1);
  position: relative;
  overflow: hidden;
  backdrop-filter: blur(20px);
  border: 1px solid rgba(255, 255, 255, 0.3);
  max-width: 600px;
  margin: 0 auto;
}

.hero-text-block::before {
  content: '';
  position: absolute;
  top: 0;
  left: 0;
  right: 0;
  height: 2px;
  background: linear-gradient(90deg, transparent, #ffffff, transparent);
  opacity: 0.3;
}

.hero-text-block::after {
  content: '';
  position: absolute;
  top: 0;
  left: 0;
  right: 0;
  bottom: 0;
  background: linear-gradient(135deg, 
    rgba(255, 255, 255, 0.05) 0%, 
    transparent 30%, 
    transparent 70%, 
    rgba(255, 255, 255, 0.05) 100%
  );
  pointer-events: none;
}

/* Hero Typography */
.hero-title {
  font-family: 'Inter', 'Segoe UI', 'Roboto', 'Helvetica Neue', sans-serif;
  font-size: clamp(2.5rem, 6vw, 4rem);
  font-weight: 700;
  color: #ffffff;
  margin-bottom: 1.5rem;
  line-height: 1.2;
  letter-spacing: -0.02em;
  text-shadow: 0 2px 4px rgba(0, 0, 0, 0.5);
  position: relative;
}

.hero-subtitle {
  font-family: 'Inter', 'Segoe UI', 'Roboto', 'Helvetica Neue', sans-serif;
  font-size: clamp(1.1rem, 2.5vw, 1.5rem);
  font-weight: 400;
  color: #e0e0e0;
  margin-bottom: 0;
  line-height: 1.5;
  letter-spacing: 0.01em;
  opacity: 0.95;
  position: relative;
}

/* Fallback styling for browsers that don't support video */
.hero-fallback {
  position: absolute;
  top: 0;
  left: 0;
  width: 100%;
  height: 100%;
  background: linear-gradient(135deg, #f5f5dc 0%, #f0e68c 100%);
  display: flex;
  align-items: center;
  justify-content: center;
  z-index: 1;
}

/* Content Section Spacing */
.content-section {
  position: relative;
  z-index: 10;
  background: white;
  border-radius: 20px;
  box-shadow: 0 10px 30px rgba(0, 0, 0, 0.1);
}

.icon-shape {
  display: flex;
  align-items: center;
  justify-content: center;
}

.ni {
  font-family: 'Nucleo Icons';
}

/* Sanitation Feature Section */
.sanitation-feature-section {
  background: linear-gradient(135deg, #f8f9fa 0%, #e9ecef 100%);
  border-radius: 20px;
  margin: 2rem 0;
  position: relative;
  overflow: hidden;
}

/* Maternal & Infant Health Feature Section */
.maternal-infant-feature-section {
  background: linear-gradient(135deg, #e8f5e8 0%, #d4edda 100%);
  border-radius: 20px;
  margin: 2rem 0;
  position: relative;
  overflow: hidden;
}

.sanitation-feature-section::before {
  content: '';
  position: absolute;
  top: 0;
  left: 0;
  right: 0;
  height: 4px;
  background: linear-gradient(90deg, #007bff, #28a745, #ffc107, #dc3545);
}

.maternal-infant-feature-section::before {
  content: '';
  position: absolute;
  top: 0;
  left: 0;
  right: 0;
  height: 4px;
  background: linear-gradient(90deg, #28a745, #20c997, #17a2b8, #6f42c1);
}

.feature-badge .badge {
  font-size: 0.9rem;
  font-weight: 600;
  border-radius: 20px;
  animation: pulse 2s infinite;
}

@keyframes pulse {
  0% { transform: scale(1); }
  50% { transform: scale(1.05); }
  100% { transform: scale(1); }
}

.highlight-item {
  display: flex;
  align-items: center;
  padding: 0.75rem;
  background: white;
  border-radius: 15px;
  box-shadow: 0 2px 10px rgba(0,0,0,0.1);
  transition: all 0.3s ease;
  font-weight: 500;
}

.highlight-item:hover {
  transform: translateY(-2px);
  box-shadow: 0 4px 15px rgba(0,0,0,0.15);
}

.highlight-item i {
  font-size: 1.2rem;
}

.cta-buttons .btn {
  border-radius: 15px;
  padding: 0.75rem 2rem;
  font-weight: 600;
  transition: all 0.3s ease;
}

.cta-buttons .btn:hover {
  transform: translateY(-2px);
  box-shadow: 0 4px 15px rgba(0,0,0,0.2);
}

/* Feature Cards Visual */
.feature-cards {
  display: flex;
  flex-direction: column;
  gap: 1.5rem;
  align-items: center;
}

.feature-card {
  background: white;
  border-radius: 20px;
  padding: 2rem;
  text-align: center;
  box-shadow: 0 4px 15px rgba(0,0,0,0.1);
  transition: all 0.3s ease;
  width: 100%;
  max-width: 300px;
  position: relative;
}

.feature-card:hover {
  transform: translateY(-5px);
  box-shadow: 0 8px 25px rgba(0,0,0,0.15);
}

.feature-card .card-icon {
  width: 60px;
  height: 60px;
  border-radius: 50%;
  background: linear-gradient(135deg, #007bff 0%, #0056b3 100%);
  color: white;
  display: flex;
  align-items: center;
  justify-content: center;
  font-size: 1.5rem;
  margin: 0 auto 1rem;
  transition: all 0.3s ease;
}

.feature-card.place-card .card-icon {
  background: linear-gradient(135deg, #28a745 0%, #1e7e34 100%);
}

.feature-card.result-card .card-icon {
  background: linear-gradient(135deg, #ffc107 0%, #e0a800 100%);
}

.feature-card.hydration-card .card-icon {
  background: linear-gradient(135deg, #17a2b8 0%, #138496 100%);
}

.feature-card.feeding-card .card-icon {
  background: linear-gradient(135deg, #28a745 0%, #1e7e34 100%);
}

.feature-card.health-card .card-icon {
  background: linear-gradient(135deg, #6f42c1 0%, #5a32a3 100%);
}

.feature-card h5 {
  margin-bottom: 0.5rem;
  color: #333;
  font-weight: 600;
}

.feature-card p {
  margin-bottom: 0;
  color: #6c757d;
  font-size: 0.9rem;
}

/* Add connecting lines between cards */
.feature-card:not(:last-child)::after {
  content: '';
  position: absolute;
  bottom: -1.5rem;
  left: 50%;
  transform: translateX(-50%);
  width: 2px;
  height: 1.5rem;
  background: linear-gradient(180deg, #007bff, #28a745);
}

/* Responsive adjustments */
@media (max-width: 768px) {
  .display-3 {
    font-size: 2.5rem;
  }
  
  .lead {
    font-size: 1.1rem !important;
  }
  
  .sanitation-feature-section {
    margin: 1rem 0;
    padding: 2rem 0 !important;
  }
  
  .feature-cards {
    margin-top: 2rem;
  }
  
  .feature-card {
    padding: 1.5rem;
  }
  
  .cta-buttons .btn {
    width: 100%;
  }
  
  /* Mobile video optimizations */
  .hero-video {
    filter: brightness(1.1) contrast(1.1);
  }
  
  /* Mobile Hero Adjustments */
  .hero-text-block {
    padding: 2rem 1.5rem;
    margin: 0 1rem;
    border-radius: 15px;
  }
  
  .hero-title {
    font-size: clamp(2rem, 8vw, 2.8rem);
    margin-bottom: 1rem;
  }
  
  .hero-subtitle {
    font-size: clamp(1rem, 4vw, 1.2rem);
  }
}

/* Tablet adjustments */
@media (max-width: 992px) and (min-width: 769px) {
  .hero-text-block {
    padding: 2.5rem 2rem;
  }
  
  .hero-title {
    font-size: clamp(2.2rem, 5vw, 3.2rem);
  }
  
  .hero-subtitle {
    font-size: clamp(1.1rem, 3vw, 1.4rem);
  }
}

@media (min-width: 992px) {
  .feature-cards {
    flex-direction: row;
    justify-content: space-around;
    align-items: flex-start;
  }
  
  .feature-card {
    flex: 1;
    margin: 0 0.5rem;
  }
  
  .feature-card:not(:last-child)::after {
    bottom: 50%;
    right: -1rem;
    left: auto;
    transform: translateY(50%);
    width: 1.5rem;
    height: 2px;
    background: linear-gradient(90deg, #007bff, #28a745);
  }
  
  /* Large screen optimizations */
  .hero-text-block {
    padding: 3.5rem 3rem;
    max-width: 600px;
    margin: 0 auto;
  }
  
  .hero-title {
    font-size: clamp(3rem, 4vw, 4.5rem);
  }
  
  .hero-subtitle {
    font-size: clamp(1.3rem, 2vw, 1.8rem);
  }
}
</style>

