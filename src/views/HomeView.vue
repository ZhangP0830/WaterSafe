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
// 导入图片资源
import heroBg from "@/assets/img/homebackground.png";

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

// Methods
const scrollToLearnMore = () => {
  // Scroll to the HomeInformation section to show more details
  const element = document.querySelector('.sanitation-feature-section');
  if (element) {
    element.scrollIntoView({ behavior: 'smooth' });
  }
};
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
    <div
      class="page-header min-vh-100"
      :style="`background-image: url(${heroBg})`"
      loading="lazy"
    >
      <div class="container">
        <div class="row">
          <div class="col-lg-8 text-center mx-auto position-relative">
            <h1
              class="text-white pt-3 mt-n5 me-2 display-5 fw-bold"
              :style="{ display: 'inline-block' }"
            >
              Water Safety
            </h1>
            <p class="lead text-white px-5 mt-4 mb-5" :style="{ fontWeight: '500', fontSize: '1.25rem' }">
              Safe Water for Every Stage of Life.
            </p>
            <div class="d-flex justify-content-center gap-3 flex-wrap">
            </div>
          </div>
        </div>
      </div>
    </div>
  </Header>

    <!-- main content section -->
  <div class="card card-body blur shadow-blur mx-3 mx-md-4 mt-n6">
    <!-- here you can add your content -->
     <HomeIntroduction />
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
                 <router-link to="/sanitation-support" class="btn btn-primary btn-lg me-3 mb-2">
                   <i class="fas fa-magic me-2"></i>Get Your Checklist
                 </router-link>
                 <button class="btn btn-outline-primary btn-lg mb-2" @click="scrollToLearnMore">
                   <i class="fas fa-info-circle me-2"></i>Learn More
                 </button>
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

.sanitation-feature-section::before {
  content: '';
  position: absolute;
  top: 0;
  left: 0;
  right: 0;
  height: 4px;
  background: linear-gradient(90deg, #007bff, #28a745, #ffc107, #dc3545);
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
    margin-bottom: 1rem;
  }
  
  .cta-buttons .btn:last-child {
    margin-bottom: 0;
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
}
</style>

