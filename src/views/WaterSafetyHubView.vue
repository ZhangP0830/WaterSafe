<script setup>
import { onMounted, onUnmounted } from "vue";

import NavbarDefault from "../components/navigation/NavbarDefault.vue";
import DefaultFooter from "../components/layout/FooterDefault.vue";
import AwarenessNavTab from "../components/AwarenessSection/AwarenessNavTab.vue";

const body = document.getElementsByTagName("body")[0];
onMounted(() => {
  body.classList.add("water-safety-hub-page");
  body.classList.add("bg-gray-100");
});
onUnmounted(() => {
  body.classList.remove("water-safety-hub-page");
  body.classList.remove("bg-gray-100");
});
</script>

<template>
  <!-- NavBar -->
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
              <i class="material-icons me-2 text-info">info</i>
              Water Safety Awareness Hub
            </h4>
            <p class="text-muted mb-3 text-center">
              This hub provides comprehensive water safety information and procedures. Browse through different contamination stages using the navigation tabs below. Each section contains detailed guidance on signs to watch for, safety measures to take, and recovery procedures to follow. Click on any tab to access specific information for that contamination level.
            </p>
          </div>
        </div>
      </div>
    </div>
    
    <!-- Content -->
    <AwarenessNavTab />
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

.bg-gray-100 {
  background-color: #f8f9fa !important;
}

/* Phone */
@media (max-width: 768px) {
  .display-3 {
    font-size: 2.5rem;
  }
  
  .lead {
    font-size: 1.1rem !important;
  }
}
</style>


