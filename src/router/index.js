import { createRouter, createWebHistory } from "vue-router";
import HomeView from "../views/HomeView.vue";
import WaterSafetyHubView from "../views/WaterSafetyHubView.vue";
import TrustedAlternativesView from "../views/TrustedAlternativesView.vue";
import VoiceAssistantView from "../views/VoiceAssistantView.vue";

const router = createRouter({
  history: createWebHistory(import.meta.env.BASE_URL),
  routes: [
    {
      path: "/",
      name: "home",
      component: HomeView,
    },
    {
      path: "/water-safety-hub",
      name: "water-safety-hub",
      component: WaterSafetyHubView,
    },
    {
      path: "/trusted-alternatives",
      name: "trusted-alternatives",
      component: TrustedAlternativesView,
    },
    {
      path: "/water-safety-companion",
      name: "water-safety-companion",
      component: VoiceAssistantView,
    },
  ],
});

export default router;
