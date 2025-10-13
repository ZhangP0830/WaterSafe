<script setup>
import { RouterLink } from "vue-router";
import { ref, watch, onMounted } from "vue";
import { useWindowsWidth } from "../../assets/js/useWindowsWidth";

// images
import ArrDark from "@/assets/img/down-arrow-dark.svg";
import downArrow from "@/assets/img/down-arrow.svg";
import DownArrWhite from "@/assets/img/down-arrow-white.svg";

const props = defineProps({
  action: {
    type: Object,
    route: String,
    color: String,
    label: String,
    default: () => ({
      route: "https://www.creative-tim.com/product/vue-material-kit",
      color: "bg-gradient-success",
      label: "Free Download"
    })
  },
  transparent: {
    type: Boolean,
    default: false
  },
  light: {
    type: Boolean,
    default: false
  },
  dark: {
    type: Boolean,
    default: false
  },
  sticky: {
    type: Boolean,
    default: false
  },
  darkText: {
    type: Boolean,
    default: false
  }
});

// set arrow  color
function getArrowColor() {
  if (props.transparent && textDark.value) {
    return ArrDark;
  } else if (props.transparent) {
    return DownArrWhite;
  } else {
    return ArrDark;
  }
}

// set text color
const getTextColor = () => {
  let color;
  if (props.transparent && textDark.value) {
    color = "text-dark";
  } else if (props.transparent) {
    color = "text-white";
  } else {
    color = "text-dark";
  }

  return color;
};

// set nav color on mobile && desktop
let textDark = ref(props.darkText);
const { type } = useWindowsWidth();

// Mobile menu state
const isMenuOpen = ref(false);

// Toggle mobile menu
const toggleMobileMenu = () => {
  isMenuOpen.value = !isMenuOpen.value;
};

// Close mobile menu when clicking on a link
const closeMobileMenu = () => {
  isMenuOpen.value = false;
};

if (type.value === "mobile") {
  textDark.value = true;
} else if (type.value === "desktop" && textDark.value == false) {
  textDark.value = false;
}

watch(
  () => type.value,
  (newValue) => {
    if (newValue === "mobile") {
      textDark.value = true;
    } else {
      textDark.value = false;
    }
  }
);
</script>

<style scoped>
/* Mobile menu styles */
.navbar-collapse {
  transition: all 0.3s ease;
}

.navbar-collapse.collapse {
  display: none;
}

.navbar-collapse.show {
  display: block;
}

/* Ensure mobile menu is visible on small screens */
@media (max-width: 991.98px) {
  .navbar-collapse.collapse {
    display: none !important;
  }
  
  .navbar-collapse.show {
    display: block !important;
  }
}

/* Desktop menu should always be visible */
@media (min-width: 992px) {
  .navbar-collapse {
    display: flex !important;
  }
}

/* Enhanced Navigation Styling */
.navbar {
  backdrop-filter: blur(20px);
  background: rgba(255, 255, 255, 0.95) !important;
  border-radius: 20px;
  box-shadow: 0 8px 32px rgba(0, 0, 0, 0.1);
  border: 1px solid rgba(255, 255, 255, 0.2);
}

.navbar-transparent {
  background: rgba(255, 255, 255, 0.1) !important;
  backdrop-filter: blur(20px);
}

.nav-link {
  transition: all 0.3s ease;
  font-weight: 500;
  font-size: 0.95rem;
  position: relative;
  overflow: hidden;
}

.nav-link:hover {
  background: rgba(0, 123, 255, 0.1);
  transform: translateY(-1px);
  box-shadow: 0 4px 12px rgba(0, 123, 255, 0.15);
}

.nav-link.router-link-active {
  background: rgba(0, 123, 255, 0.15);
  color: #007bff !important;
  font-weight: 600;
}

.nav-text {
  white-space: nowrap;
  line-height: 1.2;
}

.material-icons {
  transition: all 0.3s ease;
}

.nav-link:hover .material-icons {
  transform: scale(1.1);
}

/* Responsive adjustments */
@media (max-width: 1600px) {
  .nav-item {
    margin: 0 0.15rem !important;
  }
  
  .nav-link {
    padding: 0.4rem 0.7rem !important;
    font-size: 0.9rem;
    white-space: nowrap;
    overflow: hidden;
    text-overflow: ellipsis;
    max-width: 180px;
  }
  
  .nav-text {
    font-size: 0.9rem;
    white-space: nowrap;
    overflow: hidden;
    text-overflow: ellipsis;
  }
}

@media (max-width: 1400px) {
  .nav-item {
    margin: 0 0.1rem !important;
  }
  
  .nav-link {
    padding: 0.35rem 0.6rem !important;
    font-size: 0.85rem;
    max-width: 160px;
  }
  
  .nav-text {
    font-size: 0.85rem;
  }
}

@media (max-width: 1200px) {
  .nav-item {
    margin: 0 0.05rem !important;
  }
  
  .nav-link {
    padding: 0.3rem 0.5rem !important;
    font-size: 0.8rem;
    max-width: 140px;
  }
  
  .nav-text {
    font-size: 0.8rem;
  }
}

@media (max-width: 1100px) {
  .nav-link {
    padding: 0.25rem 0.4rem !important;
    font-size: 0.75rem;
    max-width: 120px;
  }
  
  .nav-text {
    font-size: 0.75rem;
  }
  
  /* Hide icons on very small screens to save space */
  .nav-link .material-icons {
    display: none;
  }
  
  .nav-link {
    padding: 0.3rem 0.5rem !important;
  }
}

@media (max-width: 992px) {
  .navbar {
    border-radius: 15px;
  }
  
  .nav-link {
    border-radius: 10px;
    margin: 0.25rem 0;
  }
}
</style>
<template>
  <nav
    class="navbar navbar-expand-lg top-0"
    :class="{
      'z-index-3 w-100 shadow-none navbar-transparent position-absolute my-3':
        props.transparent,
      'my-3 blur border-radius-lg z-index-3 py-3 shadow py-3 start-0 end-0 mx-1 position-absolute mt-4':
        props.sticky,
      'navbar-light bg-white py-3': props.light,
      ' navbar-dark bg-gradient-dark z-index-3 py-3': props.dark
    }"
  >
    <div
      :class="
        props.transparent || props.light || props.dark
          ? 'container-fluid px-2'
          : 'container-fluid px-0'
      "
    >
      <RouterLink
        class="navbar-brand d-none d-md-block"
        :class="[
          (props.transparent && textDark.value) || !props.transparent
            ? 'text-dark font-weight-bolder ms-sm-3'
            : 'text-white font-weight-bolder ms-sm-3'
        ]"
        :to="{ name: 'home' }"
        rel="tooltip"
        title="WaterSafe"
        data-placement="bottom"
      >
        WaterSafetyGuard
      </RouterLink>
      <RouterLink
        class="navbar-brand d-block d-md-none"
        :class="
          props.transparent || props.dark
            ? 'text-white'
            : 'font-weight-bolder ms-sm-3'
        "
        to="/"
        rel="tooltip"
        title="WaterSafe"
        data-placement="bottom"
      >
        WaterSafetyGuard
      </RouterLink>
      <button
        class="navbar-toggler shadow-none ms-2"
        type="button"
        @click="toggleMobileMenu"
        aria-controls="navigation"
        :aria-expanded="isMenuOpen"
        aria-label="Toggle navigation"
      >
        <span class="navbar-toggler-icon mt-2">
          <span class="navbar-toggler-bar bar1"></span>
          <span class="navbar-toggler-bar bar2"></span>
          <span class="navbar-toggler-bar bar3"></span>
        </span>
      </button>
      <div
        class="navbar-collapse w-100 pt-3 pb-2 py-lg-0"
        :class="{ 'collapse': !isMenuOpen, 'show': isMenuOpen }"
        id="navigation"
      >
        <ul class="navbar-nav navbar-nav-hover ms-auto">
          <li class="nav-item mx-2">
            <RouterLink
              class="nav-link ps-2 pe-2 d-flex cursor-pointer align-items-center rounded-pill"
              :class="getTextColor()"
              :to="{ name: 'water-quality-prediction' }"
              @click="closeMobileMenu"
            >
              <i
                class="material-icons opacity-7 me-2 text-md"
                :class="getTextColor()"
                >analytics</i
              >
              <span class="nav-text d-none d-xl-inline">Water Quality Prediction</span>
              <span class="nav-text d-inline d-xl-none">Quality Prediction</span>
            </RouterLink>
          </li>
          <li class="nav-item mx-2">
            <RouterLink
              class="nav-link ps-2 pe-2 d-flex cursor-pointer align-items-center rounded-pill"
              :class="getTextColor()"
              :to="{ name: 'trusted-alternatives' }"
              @click="closeMobileMenu"
            >
              <i
                class="material-icons opacity-7 me-2 text-md"
                :class="getTextColor()"
                >map</i
              >
              <span class="nav-text d-none d-xl-inline">Trusted Alternatives</span>
              <span class="nav-text d-inline d-xl-none">Alternatives</span>
            </RouterLink>
          </li>
          <li class="nav-item mx-2">
            <RouterLink
              class="nav-link ps-2 pe-2 d-flex cursor-pointer align-items-center rounded-pill"
              :class="getTextColor()"
              :to="{ name: 'water-safety-hub' }"
              @click="closeMobileMenu"
            >
              <i
                class="material-icons opacity-7 me-2 text-md"
                :class="getTextColor()"
                >water_drop</i
              >
              <span class="nav-text d-none d-xl-inline">Water Safety Hub</span>
              <span class="nav-text d-inline d-xl-none">Safety Hub</span>
            </RouterLink>
          </li>
          <li class="nav-item mx-2">
            <RouterLink
              class="nav-link ps-2 pe-2 d-flex cursor-pointer align-items-center rounded-pill"
              :class="getTextColor()"
              :to="{ name: 'sanitation-support' }"
              @click="closeMobileMenu"
            >
              <i
                class="material-icons opacity-7 me-2 text-md"
                :class="getTextColor()"
                >sanitizer</i
              >
              <span class="nav-text d-none d-xl-inline">Sanitation Support</span>
              <span class="nav-text d-inline d-xl-none">Sanitation</span>
            </RouterLink>
          </li>
          <li class="nav-item mx-2">
            <RouterLink
              class="nav-link ps-2 pe-2 d-flex cursor-pointer align-items-center rounded-pill"
              :class="getTextColor()"
              :to="{ name: 'maternal-infant-health' }"
              @click="closeMobileMenu"
            >
              <i
                class="material-icons opacity-7 me-2 text-md"
                :class="getTextColor()"
                >pregnant_woman</i
              >
              <span class="nav-text d-none d-xl-inline">Maternal & Infant Health</span>
              <span class="nav-text d-inline d-xl-none">Maternal Health</span>
            </RouterLink>
          </li>
          <li class="nav-item mx-2">
            <RouterLink
              class="nav-link ps-2 pe-2 d-flex cursor-pointer align-items-center rounded-pill"
              :class="getTextColor()"
              :to="{ name: 'water-safety-companion' }"
              @click="closeMobileMenu"
            >
              <i
                class="material-icons opacity-7 me-2 text-md"
                :class="getTextColor()"
                >mic</i
              >
              <span class="nav-text d-none d-xl-inline">Water Safety Companion</span>
              <span class="nav-text d-inline d-xl-none">Companion</span>
            </RouterLink>
          </li>
        </ul>
      </div>
    </div>
  </nav>
</template>
