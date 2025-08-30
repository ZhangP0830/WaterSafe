import { createRouter, createWebHistory } from "vue-router";
import HomeView from "../views/HomeView.vue";
import WaterSafetyHubView from "../views/WaterSafetyHubView.vue";

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
  ],
});

export default router;
