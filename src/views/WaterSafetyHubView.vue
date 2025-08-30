<script setup>
import { onMounted, onUnmounted } from "vue";

import NavbarDefault from "../components/navigation/NavbarDefault.vue";
import DefaultFooter from "../components/layout/FooterDefault.vue";
import Header from "../components/layout/Header.vue";
import AwarenessNavTab from "../components/AwarenessNavTab.vue";

import heroBg from "@/assets/img/bg9.jpg";

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
      class="page-header min-vh-75"
      :style="`background-image: url(${heroBg})`"
      loading="lazy"
    >
      <div class="container">
        <div class="row">
          <div class="col-lg-8 text-center mx-auto position-relative">
            <h1
              class="text-white pt-3 mt-n5 me-2 display-3 fw-bold"
              :style="{ display: 'inline-block' }"
            >
              Water Safety Awareness Hub
            </h1>
            <p class="lead text-white px-5 mt-4 mb-5" :style="{ fontWeight: '500', fontSize: '1.25rem' }">
              Need add more content here
            </p>
          </div>
        </div>
      </div>
    </div>
  </Header>

  <!-- Main -->
  <div class="card card-body blur shadow-blur mx-3 mx-md-4 mt-n6">
    <!-- Content -->
    <AwarenessNavTab />
    
    <!-- Need add more -->
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


