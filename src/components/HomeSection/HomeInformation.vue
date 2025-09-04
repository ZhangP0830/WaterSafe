<script setup>
import RotatingCard from "../cards/rotatingCards/RotatingCard.vue";
import RotatingCardFront from "../cards/rotatingCards/RotatingCardFront.vue";
import RotatingCardBack from "../cards/rotatingCards/RotatingCardBack.vue";
import DefaultInfoCard from "../cards/infoCards/DefaultInfoCard.vue";
</script>
<template>
  <section class="my-5 py-5">
    <div class="container">
      <div class="row align-items-center">
        <div class="col-lg-4 ms-auto me-auto p-lg-4 mt-lg-0 mt-4">
          <RotatingCard>
            <RotatingCardFront
              image="/src/assets/img/rotatecard-background.png"
              icon="home"
              title="Welcome to <br /> WaterSafety"
              description="Your trusted platform for comprehensive water safety information and community protection resources."
            />

            <RotatingCardBack
              image="/src/assets/img/rotatecard-background.png"
              title="Explore Our Platform"
              description="Discover water safety guidelines, trusted alternatives, and get instant water safety guidance to keep your family safe."
              :action="[
                {
                  route: '/water-safety-hub',
                  label: 'Get Started',
                },
              ]"
            />
          </RotatingCard>
        </div>
        <div class="col-lg-6 ms-auto">
          <div class="row justify-content-start">
            <DefaultInfoCard
              icon="location_on"
              title="Find Safe Water Sources"
              description="Locate nearby safe drinking water sources during water advisories with our interactive map and real-time updates."
            />
            <DefaultInfoCard
              icon="water_drop"
              title="Water Safety Hub"
              description="Access comprehensive water safety guidance, contamination stages, and step-by-step procedures to protect your family during water emergencies."
            />
          </div>
          <div class="row justify-content-start mt-5">
            <DefaultInfoCard
              class="mt-3"
              icon="family_restroom"
              title="Family Safety First"
              description="Protect your family with expert guidance on water safety for infants, children, and vulnerable populations during contamination events."
            />
            <DefaultInfoCard
              class="mt-3"
              icon="phone_android"
              title="Mobile Ready"
              description="Access critical water safety information anywhere, anytime. Our responsive design works perfectly on all devices."
            />
          </div>
        </div>
      </div>
    </div>
  </section>
</template>
