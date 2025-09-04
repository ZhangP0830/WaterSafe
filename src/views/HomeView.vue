<script setup>
import { onMounted, onUnmounted } from "vue";

// 导入组件
import NavbarDefault from "../components/navigation/NavbarDefault.vue";
import DefaultFooter from "../components/layout/FooterDefault.vue";
import Header from "../components/layout/Header.vue";
import FilledInfoCard from "../components/cards/infoCards/FilledInfoCard.vue";
import MaterialButton from "@/components/MaterialButton.vue";
import HomeInformation from "../components/HomeSection/HomeInformation.vue";
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
     <HomeInformation />
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

/* 响应式调整 */
@media (max-width: 768px) {
  .display-3 {
    font-size: 2.5rem;
  }
  
  .lead {
    font-size: 1.1rem !important;
  }
}
</style>

