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
</style>
<template>
  <nav
    class="navbar navbar-expand-lg top-0"
    :class="{
      'z-index-3 w-100 shadow-none navbar-transparent position-absolute my-3':
        props.transparent,
      'my-3 blur border-radius-lg z-index-3 py-2 shadow py-2 start-0 end-0 mx-4 position-absolute mt-4':
        props.sticky,
      'navbar-light bg-white py-3': props.light,
      ' navbar-dark bg-gradient-dark z-index-3 py-3': props.dark
    }"
  >
    <div
      :class="
        props.transparent || props.light || props.dark
          ? 'container'
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
        WaterSafety
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
        WaterSafety
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
              class="nav-link ps-2 d-flex cursor-pointer align-items-center"
              :class="getTextColor()"
              :to="{ name: 'water-safety-hub' }"
              @click="closeMobileMenu"
            >
              <i
                class="material-icons opacity-6 me-2 text-md"
                :class="getTextColor()"
                >water_drop</i
              >
              Water Safety Hub
            </RouterLink>
          </li>
          <li class="nav-item mx-2">
            <RouterLink
              class="nav-link ps-2 d-flex cursor-pointer align-items-center"
              :class="getTextColor()"
              :to="{ name: 'trusted-alternatives' }"
              @click="closeMobileMenu"
            >
              <i
                class="material-icons opacity-6 me-2 text-md"
                :class="getTextColor()"
                >map</i
              >
              Trusted Alternatives
            </RouterLink>
          </li>
          <li class="nav-item mx-2">
            <RouterLink
              class="nav-link ps-2 d-flex cursor-pointer align-items-center"
              :class="getTextColor()"
              :to="{ name: 'water-safety-companion' }"
            >
              <i
                class="material-icons opacity-6 me-2 text-md"
                :class="getTextColor()"
                >mic</i
              >
              Water Safety Companion
            </RouterLink>
          </li>
        </ul>
      </div>
    </div>
  </nav>
</template>
