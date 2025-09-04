<script setup>
import { onMounted, ref } from "vue";
import ConfirmedContamination from "./ConfirmedContamination.vue";
import SevereContamination from "./SevereContamination.vue";
import ContaminationCleared from "./ContaminationCleared.vue";
import EarlySignsOfContamination from "./EarlySignsOfContamination.vue";

// nav-pill
import setNavPills from "@/assets/js/nav-pills.js";

// current active tab
const activeTab = ref('early-signs');

// switch tab
const switchTab = (tabName) => {
  console.log('Switching to tab:', tabName);
  activeTab.value = tabName;
  console.log('Active tab is now:', activeTab.value);
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
                  :class="{ active: activeTab === 'early-signs' }"
                  href="#"
                  @click.prevent="switchTab('early-signs')"
                  role="tab"
                  :aria-selected="activeTab === 'early-signs'"
                >
                  Early Signs of Contamination
                </a>
              </li>
              <li class="nav-item">
                <a
                  class="nav-link mb-0 px-2 py-2"
                  :class="{ active: activeTab === 'confirmed-contamination' }"
                  href="#"
                  @click.prevent="switchTab('confirmed-contamination')"
                  role="tab"
                  :aria-selected="activeTab === 'confirmed-contamination'"
                >
                  Confirmed Contamination
                </a>
              </li>
              <li class="nav-item">
                <a
                  class="nav-link mb-0 px-2 py-2"
                  :class="{ active: activeTab === 'severe-contamination' }"
                  href="#"
                  @click.prevent="switchTab('severe-contamination')"
                  role="tab"
                  :aria-selected="activeTab === 'severe-contamination'"
                >
                  Severe Contamination
                </a>
              </li>
              <li class="nav-item">
                <a
                  class="nav-link mb-0 px-2 py-2"
                  :class="{ active: activeTab === 'contamination-cleared' }"
                  href="#"
                  @click.prevent="switchTab('contamination-cleared')"
                  role="tab"
                  :aria-selected="activeTab === 'contamination-cleared'"
                >
                  Contamination Cleared
                </a>
              </li>

              
            </ul>
          </div>
          
          <!-- label content area -->
          <div class="mt-4">
            <!-- Early Signs of Contamination Tab -->
            <div v-if="activeTab === 'early-signs'">
              <EarlySignsOfContamination />
            </div>
            
            <!-- Confirmed Contamination Tab -->
            <div v-if="activeTab === 'confirmed-contamination'">
              <ConfirmedContamination />
            </div>
            
            <!-- Severe Contamination Tab -->
            <div v-if="activeTab === 'severe-contamination'">
              <SevereContamination />
            </div>
            
            <!-- Contamination Cleared Tab -->
            <div v-if="activeTab === 'contamination-cleared'">
              <ContaminationCleared />
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

/* responsive adjustment */
@media (max-width: 768px) {
  .nav-pills .nav-link {
    font-size: 0.8rem;
    padding: 0.5rem 0.75rem !important;
  }
}
</style>
