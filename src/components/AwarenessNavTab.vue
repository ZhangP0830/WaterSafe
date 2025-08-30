<script setup>
import { onMounted, ref } from "vue";
import BoilWaterAdvisory from "./BoilWaterAdvisory.vue";
import DoNotDrinkAdvisory from "./DoNotDrinkAdvisory.vue";
import LowWaterPressure from "./LowWaterPressure.vue";
import AdvisoryLifted from "./AdvisoryLifted.vue";

// nav-pill
import setNavPills from "@/assets/js/nav-pills.js";

// 当前激活的tab
const activeTab = ref('boil-water');

// 切换tab
const switchTab = (tabName) => {
  activeTab.value = tabName;
};

onMounted(() => {
  setNavPills();
});
</script>
<template>
  <section class="py-7">
    <div class="container">
      <div class="row">
        <div class="col-12">
          <div class="nav-wrapper position-relative">
            <ul class="nav nav-pills nav-fill p-1" role="tablist">
              <li class="nav-item">
                <a
                  class="nav-link mb-0 px-2 py-2"
                  :class="{ active: activeTab === 'boil-water' }"
                  href="#"
                  @click.prevent="switchTab('boil-water')"
                  role="tab"
                  :aria-selected="activeTab === 'boil-water'"
                >
                  Boil Water Advisory
                </a>
              </li>
              <li class="nav-item">
                <a
                  class="nav-link mb-0 px-2 py-2"
                  :class="{ active: activeTab === 'do-not-drink' }"
                  href="#"
                  @click.prevent="switchTab('do-not-drink')"
                  role="tab"
                  :aria-selected="activeTab === 'do-not-drink'"
                >
                  Do Not Drink
                </a>
              </li>
              <li class="nav-item">
                <a
                  class="nav-link mb-0 px-2 py-2"
                  :class="{ active: activeTab === 'low-pressure' }"
                  href="#"
                  @click.prevent="switchTab('low-pressure')"
                  role="tab"
                  :aria-selected="activeTab === 'low-pressure'"
                >
                  Low Pressure
                </a>
              </li>

              <li class="nav-item">
                <a
                  class="nav-link mb-0 px-2 py-2"
                  :class="{ active: activeTab === 'advisory-lifted' }"
                  href="#"
                  @click.prevent="switchTab('advisory-lifted')"
                  role="tab"
                  :aria-selected="activeTab === 'advisory-lifted'"
                >
                  Advisory Lifted
                </a>
              </li>
            </ul>
          </div>
          
          <!-- 标签内容区域 -->
          <div class="tab-content mt-4">
            <!-- Boil Water Advisory Tab -->
            <div v-if="activeTab === 'boil-water'" class="tab-pane fade show active">
              <BoilWaterAdvisory />
            </div>
            
            <!-- Do Not Drink Advisory Tab -->
            <div v-if="activeTab === 'do-not-drink'" class="tab-pane fade show active">
              <DoNotDrinkAdvisory />
            </div>
            
            <!-- Low Pressure Tab -->
            <div v-if="activeTab === 'low-pressure'" class="tab-pane fade show active">
              <LowWaterPressure />
            </div>
            
            <!-- Advisory Lifted Tab -->
            <div v-if="activeTab === 'advisory-lifted'" class="tab-pane fade show active">
              <AdvisoryLifted />
            </div>
          </div>
        </div>
      </div>
    </div>
  </section>
</template>

<style scoped>
.nav-pills .nav-link {
  white-space: nowrap;
  font-size: 0.9rem;
  min-width: 0;
  flex: 1;
}

.nav-pills .nav-item {
  flex: 1;
}

/* 响应式调整 */
@media (max-width: 768px) {
  .nav-pills .nav-link {
    font-size: 0.8rem;
    padding: 0.5rem 0.75rem !important;
  }
}
</style>
