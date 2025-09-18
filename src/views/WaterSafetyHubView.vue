<script setup>
import { onMounted, onUnmounted } from "vue";

import NavbarDefault from "../components/navigation/NavbarDefault.vue";
import DefaultFooter from "../components/layout/FooterDefault.vue";
import Header from "../components/layout/Header.vue";
import AwarenessNavTab from "../components/AwarenessSection/AwarenessNavTab.vue";

import heroBg from "@/assets/img/awarenesshubbackground.png";

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
  <div class="container position-sticky z-index-sticky top-0">
    <div class="row">
      <div class="col-12">
        <NavbarDefault :sticky="true" />
      </div>
    </div>
  </div>

  <!-- Head -->
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
              Water Safety Awareness Hub
            </h1>
            <p class="lead text-white px-5 mt-4 mb-5" :style="{ fontWeight: '500', fontSize: '1.25rem' }">
              Comprehensive water safety guidance and step-by-step procedures for different contamination stages to protect your family.
            </p>
          </div>
        </div>
      </div>
    </div>
  </Header>

  <!-- Main -->
  <div class="card card-body blur shadow-blur mx-3 mx-md-4 mt-n6">
    <!-- Page Introduction -->
    <div class="container mb-4">
      <div class="row">
        <div class="col-12">
          <div class="card shadow-sm border-0">
            <div class="card-body">
              <div class="row align-items-center">
                <div class="col-12">
                  <h4 class="mb-3">
                    <i class="material-icons me-2 text-info">info</i>
                    Water Safety Awareness Hub
                  </h4>
                  <p class="text-muted mb-3">
                    This hub provides comprehensive water safety information and procedures. Browse through different contamination stages using the navigation tabs below. Each section contains detailed guidance on signs to watch for, safety measures to take, and recovery procedures to follow. Click on any tab to access specific information for that contamination level.
                  </p>
                </div>
              </div>
            </div>
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


