<script setup>
import { ref, computed, watch, nextTick, onMounted } from "vue";
import MaterialButton from "@/components/MaterialButton.vue";
import { useMaternalInfantStore } from "@/stores/maternalInfantStore";

// Component state
const store = useMaternalInfantStore();
const trimester = ref('');
const infantAge = ref('');
const householdSize = ref(2);
const waterAdvisory = ref(false);
const currentStep = ref(1);
const showSuccessToast = ref(false);
const selectedCard = ref('');

// Hydration data
const hydrationData = {
  expecting: {
    first: {
      dailyIntake: '2.3-2.7 liters',
      breakdown: '8-9 glasses of water daily',
      additional: 'Extra 300ml for morning sickness',
      storage: 'Store 3-4 liters per day',
      notes: [
        { text: 'Extra fluids if experiencing morning sickness.', ref: { label: 'Healthdirect Australia', url: 'https://www.healthdirect.gov.au/morning-sickness', description: 'Australian health advice for pregnancy' } },
        { text: 'Small, frequent sips to prevent nausea.', ref: { label: 'Victorian Department of Health', url: 'https://www.health.vic.gov.au/pregnancy-and-birth', description: 'Victorian pregnancy health guidelines' } },
        { text: 'Use safe water for drinking and cooking.', ref: { label: 'Australian Government Health', url: 'https://www.health.gov.au/health-topics/water-quality', description: 'Australian water quality standards' } },
        { text: 'Monitor urine color for hydration signs.', ref: { label: 'RANZCOG', url: 'https://ranzcog.edu.au/', description: 'Royal Australian and New Zealand College of Obstetricians and Gynaecologists' } }
      ]
    },
    second: {
      dailyIntake: '2.7-3.1 liters',
      breakdown: '9-10 glasses of water daily',
      additional: 'Increased blood volume needs',
      storage: 'Store 4-5 liters per day',
      notes: [
        { text: 'Extra fluids if experiencing morning sickness.', ref: { label: 'Healthdirect Australia', url: 'https://www.healthdirect.gov.au/morning-sickness', description: 'Australian health advice for pregnancy' } },
        { text: 'Small, frequent sips to prevent nausea.', ref: { label: 'Victorian Department of Health', url: 'https://www.health.vic.gov.au/pregnancy-and-birth', description: 'Victorian pregnancy health guidelines' } },
        { text: 'Use safe water for drinking and cooking.', ref: { label: 'Australian Government Health', url: 'https://www.health.gov.au/health-topics/water-quality', description: 'Australian water quality standards' } },
        { text: 'Increased needs due to blood volume expansion.', ref: { label: 'RANZCOG', url: 'https://ranzcog.edu.au/', description: 'Royal Australian and New Zealand College of Obstetricians and Gynaecologists' } }
      ]
    },
    third: {
      dailyIntake: '3.1-3.5 liters',
      breakdown: '10-12 glasses of water daily',
      additional: 'Support for amniotic fluid',
      storage: 'Store 5-6 liters per day',
      notes: [
        { text: 'Extra fluids if experiencing morning sickness.', ref: { label: 'Healthdirect Australia', url: 'https://www.healthdirect.gov.au/morning-sickness', description: 'Australian health advice for pregnancy' } },
        { text: 'Small, frequent sips to prevent nausea.', ref: { label: 'Victorian Department of Health', url: 'https://www.health.vic.gov.au/pregnancy-and-birth', description: 'Victorian pregnancy health guidelines' } },
        { text: 'Use safe water for drinking and cooking.', ref: { label: 'Australian Government Health', url: 'https://www.health.gov.au/health-topics/water-quality', description: 'Australian water quality standards' } },
        { text: 'Support amniotic fluid and baby development.', ref: { label: 'RANZCOG', url: 'https://ranzcog.edu.au/', description: 'Royal Australian and New Zealand College of Obstetricians and Gynaecologists' } }
      ]
    }
  },
  baby: {
    newborn: {
      dailyIntake: 'Daily Intake: 150-200ml per kg body weight',
      breakdown: 'Formula: 60-90ml every 2-3 hours',
      additional: 'Use only safe, boiled water',
      storage: 'Store 1-2 liters per day',
      example: 'Example: a 5 kg infant needs ~750-1000ml/day.',
      notes: [
        { text: 'Extra fluids if fever or diarrhea.', ref: { label: 'Healthdirect Australia', url: 'https://www.healthdirect.gov.au/baby-feeding', description: 'Australian baby feeding guidelines' } },
        { text: 'Small, frequent sips to prevent nausea.', ref: { label: 'Victorian Department of Health', url: 'https://www.health.vic.gov.au/child-health', description: 'Victorian child health resources' } },
        { text: 'Use safe water for formula preparation.', ref: { label: 'Australian Government Health', url: 'https://www.health.gov.au/health-topics/water-quality', description: 'Australian water quality standards' } },
        { text: 'Monitor wet diapers for hydration signs.', ref: { label: 'RACP', url: 'https://www.racp.edu.au/', description: 'Royal Australasian College of Physicians' } }
      ]
    },
    '1-3months': {
      dailyIntake: 'Daily Intake: 120-150ml per kg body weight',
      breakdown: 'Formula: 90-120ml every 3-4 hours',
      additional: 'Monitor for dehydration signs',
      storage: 'Store 1.5-2.5 liters per day',
      example: 'Example: a 5 kg infant needs ~600-750ml/day.',
      notes: [
        { text: 'Extra fluids if fever or diarrhea.', ref: { label: 'Healthdirect Australia', url: 'https://www.healthdirect.gov.au/baby-feeding', description: 'Australian baby feeding guidelines' } },
        { text: 'Small, frequent sips to prevent nausea.', ref: { label: 'Victorian Department of Health', url: 'https://www.health.vic.gov.au/child-health', description: 'Victorian child health resources' } },
        { text: 'Use safe water for formula preparation.', ref: { label: 'Australian Government Health', url: 'https://www.health.gov.au/health-topics/water-quality', description: 'Australian water quality standards' } },
        { text: 'Watch for signs of overfeeding.', ref: { label: 'RACP', url: 'https://www.racp.edu.au/', description: 'Royal Australasian College of Physicians' } }
      ]
    },
    '3-6months': {
      dailyIntake: 'Daily Intake: 100-120ml per kg body weight',
      breakdown: 'Formula: 120-180ml every 4-5 hours',
      additional: 'May start introducing small amounts of water',
      storage: 'Store 2-3 liters per day',
      example: 'Example: a 5 kg infant needs ~500-600ml/day.',
      notes: [
        { text: 'Extra fluids if fever or diarrhea.', ref: { label: 'Healthdirect Australia', url: 'https://www.healthdirect.gov.au/baby-feeding', description: 'Australian baby feeding guidelines' } },
        { text: 'Small, frequent sips to prevent nausea.', ref: { label: 'Victorian Department of Health', url: 'https://www.health.vic.gov.au/child-health', description: 'Victorian child health resources' } },
        { text: 'Use safe water for formula preparation.', ref: { label: 'Australian Government Health', url: 'https://www.health.gov.au/health-topics/water-quality', description: 'Australian water quality standards' } },
        { text: 'Introduce water gradually after 6 months.', ref: { label: 'RACP', url: 'https://www.racp.edu.au/', description: 'Royal Australasian College of Physicians' } }
      ]
    }
  }
};

// Computed properties
const currentGuidance = computed(() => {
  if (store && store.isExpecting) {
    return hydrationData.expecting[trimester.value];
  } else {
    return hydrationData.baby[infantAge.value];
  }
});

const storageRecommendation = computed(() => {
  const baseStorage = store && store.isExpecting 
    ? parseInt(currentGuidance.value.storage.split('-')[1].split(' ')[0])
    : parseInt(currentGuidance.value.storage.split('-')[1].split(' ')[0]);
  
  const totalStorage = baseStorage * householdSize.value;
  return `${totalStorage} liters for ${householdSize.value} people`;
});

const advisoryMessage = computed(() => {
  if (!waterAdvisory.value) return null;
  
  return {
    title: '⚠️ Water Advisory Active',
    message: 'During water advisories, increase your safe water storage by 50% and use only boiled or bottled water for drinking and formula preparation.',
    action: 'Store extra water now'
  };
});

// Methods
const initializeUserType = () => {
  if (store && store.isExpecting) {
    trimester.value = 'first';
  } else {
    infantAge.value = 'newborn';
  }
  currentStep.value = 2;
};

const selectTrimester = (tri) => {
  trimester.value = tri;
  selectedCard.value = tri;
  nextTick(() => {
    currentStep.value = 3;
  });
};

const selectInfantAge = (age) => {
  infantAge.value = age;
  selectedCard.value = age;
  nextTick(() => {
    currentStep.value = 3;
  });
};

const completeAssessment = () => {
  currentStep.value = 4; // Move to results step
  
  // Scroll to results after a short delay
  setTimeout(() => {
    const resultsSection = document.querySelector('.results-section');
    if (resultsSection) {
      resultsSection.scrollIntoView({ 
        behavior: 'smooth',
        block: 'start'
      });
      // Add highlight animation
      resultsSection.classList.add('highlight-results');
      setTimeout(() => {
        resultsSection.classList.remove('highlight-results');
      }, 2000);
    }
  }, 500);
};

const goBack = () => {
  if (currentStep.value > 1) {
    currentStep.value--;
    // Reset the selected card for the current step
    if (currentStep.value === 2) {
      selectedCard.value = userType.value;
    } else if (currentStep.value === 1) {
      selectedCard.value = '';
    }
  }
};

const resetAssessment = () => {
  trimester.value = '';
  infantAge.value = '';
  currentStep.value = 1;
  selectedCard.value = '';
  showSuccessToast.value = false;
};

const getTrimesterLabel = (tri) => {
  const labels = {
    first: '1st Trimester (0-12 weeks)',
    second: '2nd Trimester (13-26 weeks)',
    third: '3rd Trimester (27-40 weeks)'
  };
  return labels[tri];
};

const getInfantAgeLabel = (age) => {
  const labels = {
    newborn: 'Newborn (0-1 month)',
    '1-3months': '1-3 months',
    '3-6months': '3-6 months'
  };
  return labels[age];
};

// Watch for changes to update storage recommendations
watch([trimester, infantAge, householdSize], () => {
  // Storage recommendations will automatically update via computed properties
});

// Initialize when component mounts
onMounted(() => {
  initializeUserType();
});

const openCalculator = () => {
  // Simple calculator - could be expanded to a modal
  const weight = prompt('Enter your baby\'s weight in kg:');
  if (weight && !isNaN(weight)) {
    const numWeight = parseFloat(weight);
    const minIntake = numWeight * 100;
    const maxIntake = numWeight * 200;
    alert(`For a ${weight}kg baby:\nDaily intake: ${minIntake}-${maxIntake}ml\nFormula: ${Math.round(minIntake/6)}-${Math.round(maxIntake/6)}ml every 2-3 hours`);
  }
};
</script>

<template>
  <div class="hydration-guidance">

    <!-- Header -->
    <div class="section-header text-center mb-5">
      <h2 class="display-5 fw-bold text-primary mb-3">
        <i class="fas fa-tint me-3"></i>Hydration Guidance
      </h2>
      <p class="lead text-muted">
        Get personalized daily hydration advice tailored to your pregnancy stage or your infant's needs
      </p>
    </div>

    <!-- Progress Indicator -->
    <div class="progress-indicator mb-5">
      <div class="container">
        <div class="row justify-content-center">
          <div class="col-lg-8">
            <div class="progress-steps">
              <div class="step" :class="{ 'active': currentStep >= 1, 'completed': currentStep > 1 }">
                <div class="step-number">1</div>
                <div class="step-label">Who needs guidance</div>
              </div>
              <div class="step" :class="{ 'active': currentStep >= 2, 'completed': currentStep > 2 }">
                <div class="step-number">2</div>
                <div class="step-label">{{ userType === 'pregnant' ? 'Pregnancy stage' : 'Infant age' }}</div>
              </div>
              <div class="step" :class="{ 'active': currentStep >= 3, 'completed': currentStep > 3 }">
                <div class="step-number">3</div>
                <div class="step-label">Household & advisory</div>
              </div>
            </div>
          </div>
        </div>
      </div>
    </div>


    <!-- Step 1: Pregnancy Stage or Infant Age -->
    <div v-if="currentStep === 2" class="step-content mb-5">
      <div class="row justify-content-center">
        <div class="col-lg-8">
          <div class="step-card">
            <div class="step-header">
              <h3 class="step-title">
                <i class="fas fa-calendar-alt me-2"></i>
                {{ store && store.isExpecting ? 'Choose Your Trimester' : 'Choose Your Little One\'s Age' }}
              </h3>
              <p class="step-instruction">Select the option that best describes your current stage</p>
              <div v-if="!store || (!store.isExpecting && !store.hasBaby)" class="alert alert-info">
                <i class="fas fa-info-circle me-2"></i>
                Please select your profile first to get personalized hydration guidance.
              </div>
            </div>
            
            <!-- Pregnancy Trimester Selection -->
            <div v-if="store && store.isExpecting" class="row g-3">
              <div class="col-md-4" v-for="(tri, key) in hydrationData.expecting" :key="key">
                <button 
                  @click="selectTrimester(key)"
                  :class="[
                    'selection-card small',
                    { 'selected': selectedCard === key }
                  ]"
                  :aria-label="`Select ${getTrimesterLabel(key)}`"
                >
                  <div class="card-content">
                    <i class="fas fa-baby-carriage card-icon"></i>
                    <h5 class="card-title">{{ getTrimesterLabel(key) }}</h5>
                    <div v-if="selectedCard === key" class="selected-indicator">
                      <i class="fas fa-check-circle"></i>
                      <span>Selected</span>
                    </div>
                  </div>
                </button>
              </div>
            </div>

            <!-- Infant Age Selection -->
            <div v-else class="row g-3">
              <div class="col-md-4" v-for="(age, key) in hydrationData.baby" :key="key">
                <button 
                  @click="selectInfantAge(key)"
                  :class="[
                    'selection-card small',
                    { 'selected': selectedCard === key }
                  ]"
                  :aria-label="`Select ${getInfantAgeLabel(key)}`"
                >
                  <div class="card-content">
                    <i class="fas fa-baby card-icon"></i>
                    <h5 class="card-title">{{ getInfantAgeLabel(key) }}</h5>
                    <div v-if="selectedCard === key" class="selected-indicator">
                      <i class="fas fa-check-circle"></i>
                      <span>Selected</span>
                    </div>
                  </div>
                </button>
              </div>
            </div>
          </div>
        </div>
      </div>
    </div>

    <!-- Step 2: Household & Advisory -->
    <div v-if="currentStep === 3" class="step-content mb-5">
      <div class="row justify-content-center">
        <div class="col-lg-8">
          <div class="step-card">
            <div class="step-header">
              <h3 class="step-title">
                <i class="fas fa-home me-2"></i>Household & Advisory
              </h3>
              <p class="step-instruction">Complete these final details to get your personalized plan</p>
            </div>
            
            <div class="row g-4">
              <!-- Household Size -->
              <div class="col-md-6">
                <div class="input-section">
                  <h5 class="input-label">
                    <i class="fas fa-users me-2"></i>Household Size
                  </h5>
                  <p class="input-description">How many people in your household?</p>
                  <select v-model="householdSize" class="form-select form-select-lg" aria-label="Select household size">
                    <option :value="1">1 person</option>
                    <option :value="2">2 people</option>
                    <option :value="3">3 people</option>
                    <option :value="4">4 people</option>
                    <option :value="5">5+ people</option>
                  </select>
                </div>
              </div>

              <!-- Water Advisory -->
              <div class="col-md-6">
                <div class="input-section">
                  <h5 class="input-label">
                    <i class="fas fa-exclamation-triangle me-2"></i>Water Advisory Status
                  </h5>
                  <p class="input-description">Is there a current water advisory?</p>
                  <div class="advisory-toggle-container">
                    <div class="advisory-toggle" :class="{ 'active': waterAdvisory }" @click="waterAdvisory = !waterAdvisory">
                      <div class="toggle-slider">
                        <div class="toggle-knob"></div>
                      </div>
                      <div class="toggle-labels">
                        <span class="toggle-label" :class="{ 'active': !waterAdvisory }">No Advisory</span>
                        <span class="toggle-label" :class="{ 'active': waterAdvisory }">Advisory Active</span>
                      </div>
                    </div>
                    <p class="toggle-description">
                      <small class="text-muted">Check this if there's a boil water notice or contamination advisory</small>
                    </p>
                  </div>
                </div>
              </div>
            </div>

            <!-- Action Buttons -->
            <div class="text-center mt-4">
              <div class="row g-3 justify-content-center">
                <div class="col-md-6">
                  <MaterialButton 
                    :color="'secondary'" 
                    :size="'lg'"
                    @click="goBack"
                    class="w-100 back-btn"
                  >
                    <i class="fas fa-arrow-left me-2"></i>Back
                  </MaterialButton>
                </div>
                <div class="col-md-6">
                  <MaterialButton 
                    :color="'success'" 
                    :size="'lg'"
                    @click="completeAssessment"
                    class="w-100 continue-btn"
                  >
                    <i class="fas fa-arrow-right me-2"></i>Get My Hydration Plan
                  </MaterialButton>
                </div>
              </div>
            </div>
          </div>
        </div>
      </div>
    </div>

    <!-- Results Section -->
    <div v-if="currentStep > 3" class="results-section">
      <div class="row justify-content-center">
        <div class="col-lg-10">
          <div class="results-card">
            <div class="results-header text-center mb-5">
              <h2 class="results-title">
                <i class="fas fa-tint me-3"></i>Here's your personalized hydration plan 💧
              </h2>
              <p class="results-subtitle">
                Tailored specifically for {{ store && store.isExpecting ? 'your pregnancy stage' : 'your little one\'s age' }}
              </p>
            </div>

            <!-- Advisory Alert -->
            <div v-if="advisoryMessage" class="advisory-alert mb-4">
              <div class="alert-content">
                <i class="fas fa-exclamation-triangle alert-icon"></i>
                <div class="alert-text">
                  <h5 class="alert-title">{{ advisoryMessage.title }}</h5>
                  <p class="alert-message">{{ advisoryMessage.message }}</p>
                  <MaterialButton 
                    :color="'warning'" 
                    :size="'sm'"
                    class="alert-action"
                  >
                    <i class="fas fa-download me-2"></i>{{ advisoryMessage.action }}
                  </MaterialButton>
                </div>
              </div>
            </div>

            <!-- Main Recommendations -->
            <div class="recommendations-grid">
              <div class="recommendation-item primary">
                <div class="recommendation-content">
                  <h4 class="recommendation-title">Daily Intake</h4>
                  <p class="recommendation-value">{{ currentGuidance.dailyIntake }}</p>
                  <p class="recommendation-detail">{{ currentGuidance.breakdown }}</p>
                  <p v-if="currentGuidance.example" class="recommendation-example">{{ currentGuidance.example }}</p>
                  <div v-if="userType === 'infant'" class="calculator-link">
                    <button class="calc-btn" @click="openCalculator">
                      <i class="fas fa-calculator me-2"></i>Calculate for your baby's weight
                    </button>
                  </div>
                </div>
              </div>

              <div class="recommendation-item secondary">
                <div class="recommendation-content">
                  <h4 class="recommendation-title">Important Notes</h4>
                  <p class="recommendation-detail">{{ currentGuidance.additional }}</p>
                  
                  <!-- Notes with References -->
                  <div v-if="currentGuidance.notes" class="notes-section">
                    <h5 class="notes-title">Key Guidelines:</h5>
                    <ul class="notes-list">
                      <li v-for="(note, index) in currentGuidance.notes" :key="index" class="note-item">
                        <span class="note-text">{{ note.text }}</span>
                        <a 
                          :href="note.ref.url" 
                          target="_blank" 
                          rel="noopener noreferrer"
                          class="reference-chip"
                          :title="`Learn more from ${note.ref.label}`"
                        >
                          {{ note.ref.label }}
                        </a>
                      </li>
                    </ul>
                  </div>
                </div>
              </div>

              <div class="recommendation-item storage">
                <div class="recommendation-content">
                  <h4 class="recommendation-title">Water Storage Recommendation</h4>
                  <p class="recommendation-value">{{ storageRecommendation }}</p>
                  <p class="recommendation-detail">
                    Based on {{ userType === 'pregnant' ? getTrimesterLabel(trimester) : getInfantAgeLabel(infantAge) }} 
                    and household of {{ householdSize }} {{ householdSize === 1 ? 'person' : 'people' }}
                  </p>
                </div>
              </div>
            </div>

            <!-- Trusted Resources -->
            <div class="trusted-resources mt-5">
              <h4 class="resources-title">
                <i class="fas fa-shield-alt me-2"></i>Trusted Resources
              </h4>
              <div class="resources-grid">
                <div class="resource-card">
                  <div class="resource-content">
                    <h5 class="resource-name">World Health Organization</h5>
                    <p class="resource-description">Global health guidelines and recommendations</p>
                    <a href="https://www.who.int/news-room/fact-sheets/detail/infant-and-young-child-feeding" target="_blank" rel="noopener noreferrer" class="resource-link">
                      <i class="fas fa-external-link-alt me-2"></i>Visit WHO
                    </a>
                  </div>
                </div>
                
                
                <div class="resource-card">
                  <div class="resource-content">
                    <h5 class="resource-name">American College of Obstetricians</h5>
                    <p class="resource-description">Pregnancy and nutrition guidelines</p>
                    <a href="https://www.acog.org/womens-health/faqs/nutrition-during-pregnancy" target="_blank" rel="noopener noreferrer" class="resource-link">
                      <i class="fas fa-external-link-alt me-2"></i>Visit ACOG
                    </a>
                  </div>
                </div>
              </div>
            </div>

            <!-- Action Buttons -->
            <div class="action-buttons mt-5">
              <div class="row g-3 justify-content-center">
                <div class="col-md-4">
                  <MaterialButton 
                    :color="'secondary'" 
                    :size="'lg'"
                    @click="resetAssessment"
                    class="w-100"
                  >
                    <i class="fas fa-undo me-2"></i>Start Over
                  </MaterialButton>
                </div>
              </div>
            </div>
          </div>
        </div>
      </div>
    </div>
  </div>
</template>

<style scoped>
.hydration-guidance {
  max-width: 1200px;
  margin: 0 auto;
  font-family: 'Inter', -apple-system, BlinkMacSystemFont, sans-serif;
}

/* Back Button */
.back-btn {
  border-radius: 15px;
  padding: 0.75rem 1.5rem;
  font-weight: 600;
  transition: all 0.3s ease;
}

.back-btn:hover {
  transform: translateY(-2px);
  box-shadow: 0 4px 15px rgba(0,0,0,0.2);
}

/* Section Header */
.section-header h2 {
  color: #2c3e50;
  font-weight: 700;
}

/* Progress Indicator */
.progress-indicator {
  background: linear-gradient(135deg, #f8f9fa 0%, #e9ecef 100%);
  border-radius: 20px;
  padding: 2rem 0;
}

.progress-steps {
  display: flex;
  justify-content: space-between;
  align-items: center;
  position: relative;
}

.progress-steps::before {
  content: '';
  position: absolute;
  top: 25px;
  left: 12.5%;
  right: 12.5%;
  height: 3px;
  background: #e9ecef;
  z-index: 1;
}

.step {
  display: flex;
  flex-direction: column;
  align-items: center;
  position: relative;
  z-index: 2;
}

.step-number {
  width: 50px;
  height: 50px;
  border-radius: 50%;
  background: #e9ecef;
  color: #6c757d;
  display: flex;
  align-items: center;
  justify-content: center;
  font-weight: 700;
  font-size: 1.2rem;
  margin-bottom: 0.5rem;
  transition: all 0.3s ease;
}

.step.active .step-number {
  background: linear-gradient(135deg, #007bff 0%, #0056b3 100%);
  color: white;
  transform: scale(1.1);
}

.step.completed .step-number {
  background: linear-gradient(135deg, #28a745 0%, #20c997 100%);
  color: white;
}

.step-label {
  font-size: 0.9rem;
  font-weight: 600;
  color: #6c757d;
  text-align: center;
  max-width: 120px;
}

.step.active .step-label {
  color: #007bff;
}

.step.completed .step-label {
  color: #28a745;
}

/* Step Content */
.step-card {
  background: white;
  border-radius: 25px;
  padding: 3rem;
  box-shadow: 0 8px 30px rgba(0,0,0,0.1);
  border: 1px solid #f8f9fa;
}

.step-header {
  text-align: center;
  margin-bottom: 2rem;
}

.step-title {
  color: #2c3e50;
  font-weight: 700;
  font-size: 1.8rem;
  margin-bottom: 0.5rem;
}

.step-instruction {
  color: #6c757d;
  font-size: 1.1rem;
  font-weight: 500;
  margin-bottom: 0;
}

/* Selection Cards */
.selection-card {
  background: white;
  border: 3px solid #e9ecef;
  border-radius: 20px;
  padding: 0;
  transition: all 0.3s ease;
  cursor: pointer;
  position: relative;
  overflow: hidden;
  min-height: 200px;
  display: flex;
  align-items: center;
  justify-content: center;
}

.selection-card:hover {
  transform: translateY(-5px);
  box-shadow: 0 12px 30px rgba(0,0,0,0.15);
  border-color: #007bff;
}

.selection-card.selected {
  border-color: #28a745;
  background: linear-gradient(135deg, #f8fff9 0%, #e8f5e8 100%);
  transform: translateY(-5px);
  box-shadow: 0 12px 30px rgba(40, 167, 69, 0.2);
}

.selection-card.small {
  min-height: 150px;
}

.card-content {
  padding: 2rem;
  text-align: center;
  width: 100%;
}

.card-icon {
  font-size: 3rem;
  color: #007bff;
  margin-bottom: 1rem;
  display: block;
}

.selection-card.selected .card-icon {
  color: #28a745;
}

.card-title {
  color: #2c3e50;
  font-weight: 700;
  font-size: 1.3rem;
  margin-bottom: 0.5rem;
}

.card-description {
  color: #6c757d;
  font-size: 1rem;
  margin-bottom: 0;
}

.selected-indicator {
  position: absolute;
  top: 15px;
  right: 15px;
  background: #28a745;
  color: white;
  padding: 0.5rem 1rem;
  border-radius: 20px;
  font-size: 0.8rem;
  font-weight: 600;
  display: flex;
  align-items: center;
  gap: 0.5rem;
  animation: fadeIn 0.3s ease-out;
}

@keyframes fadeIn {
  from {
    opacity: 0;
    transform: scale(0.8);
  }
  to {
    opacity: 1;
    transform: scale(1);
  }
}

/* Input Sections */
.input-section {
  background: #f8f9fa;
  border-radius: 15px;
  padding: 1.5rem;
  height: 100%;
}

.input-label {
  color: #2c3e50;
  font-weight: 700;
  font-size: 1.2rem;
  margin-bottom: 0.5rem;
}

.input-description {
  color: #6c757d;
  font-size: 1rem;
  margin-bottom: 1rem;
}

.form-select {
  border-radius: 15px;
  border: 2px solid #e9ecef;
  font-weight: 600;
  font-size: 1.1rem;
  padding: 0.75rem 1rem;
}

.form-select:focus {
  border-color: #007bff;
  box-shadow: 0 0 0 0.2rem rgba(0, 123, 255, 0.25);
}

.form-switch-lg .form-check-input {
  width: 3rem;
  height: 1.5rem;
}

/* Advisory Toggle */
.advisory-toggle-container {
  text-align: center;
}

.advisory-toggle {
  display: inline-block;
  cursor: pointer;
  margin-bottom: 1rem;
}

.toggle-slider {
  width: 120px;
  height: 40px;
  background: #e9ecef;
  border-radius: 20px;
  position: relative;
  transition: all 0.3s ease;
  margin: 0 auto 1rem;
}

.advisory-toggle.active .toggle-slider {
  background: linear-gradient(135deg, #ffc107 0%, #ff8c00 100%);
}

.toggle-knob {
  width: 36px;
  height: 36px;
  background: white;
  border-radius: 50%;
  position: absolute;
  top: 2px;
  left: 2px;
  transition: all 0.3s ease;
  box-shadow: 0 2px 8px rgba(0,0,0,0.2);
}

.advisory-toggle.active .toggle-knob {
  transform: translateX(80px);
}

.toggle-labels {
  display: flex;
  justify-content: space-between;
  width: 120px;
  margin: 0 auto;
}

.toggle-label {
  font-size: 0.8rem;
  font-weight: 600;
  color: #6c757d;
  transition: all 0.3s ease;
}

.toggle-label.active {
  color: #ffc107;
  font-weight: 700;
}

.toggle-description {
  margin-top: 0.5rem;
  margin-bottom: 0;
}

.continue-btn {
  border-radius: 15px;
  padding: 1rem 2rem;
  font-weight: 700;
  font-size: 1.1rem;
  box-shadow: 0 4px 15px rgba(40, 167, 69, 0.3);
}

/* Results Section */
.results-card {
  background: white;
  border-radius: 25px;
  padding: 3rem;
  box-shadow: 0 12px 40px rgba(0,0,0,0.1);
  border: 1px solid #f8f9fa;
}

.results-title {
  color: #2c3e50;
  font-weight: 700;
  font-size: 2.2rem;
  margin-bottom: 1rem;
}

.results-subtitle {
  color: #6c757d;
  font-size: 1.2rem;
  font-weight: 500;
  margin-bottom: 0;
}

/* Advisory Alert */
.advisory-alert {
  background: linear-gradient(135deg, #fff3cd 0%, #ffeaa7 100%);
  border: 2px solid #ffc107;
  border-radius: 20px;
  padding: 1.5rem;
}

.alert-content {
  display: flex;
  align-items: flex-start;
  gap: 1rem;
}

.alert-icon {
  font-size: 2rem;
  color: #856404;
  margin-top: 0.25rem;
}

.alert-title {
  color: #856404;
  font-weight: 700;
  margin-bottom: 0.5rem;
}

.alert-message {
  color: #856404;
  margin-bottom: 1rem;
}

.alert-action {
  border-radius: 10px;
  font-weight: 600;
}

/* Recommendations Grid */
.recommendations-grid {
  display: grid;
  grid-template-columns: 1fr;
  gap: 1.5rem;
}

.recommendation-item {
  background: white;
  border-radius: 20px;
  padding: 2rem;
  box-shadow: 0 4px 15px rgba(0,0,0,0.1);
  border: 2px solid #f8f9fa;
  display: flex;
  align-items: center;
  gap: 1.5rem;
  transition: all 0.3s ease;
}

.recommendation-item:hover {
  transform: translateY(-3px);
  box-shadow: 0 8px 25px rgba(0,0,0,0.15);
}

.recommendation-item.primary {
  border-color: #007bff;
  background: linear-gradient(135deg, #f8f9ff 0%, #e3f2fd 100%);
}

.recommendation-item.secondary {
  border-color: #17a2b8;
  background: linear-gradient(135deg, #f0f9ff 0%, #e0f7fa 100%);
}

.recommendation-item.storage {
  border-color: #28a745;
  background: linear-gradient(135deg, #f8fff9 0%, #e8f5e8 100%);
}



.recommendation-title {
  color: #2c3e50;
  font-weight: 700;
  font-size: 1.3rem;
  margin-bottom: 0.5rem;
}

.recommendation-value {
  color: #007bff;
  font-weight: 700;
  font-size: 1.5rem;
  margin-bottom: 0.5rem;
}

.recommendation-item.storage .recommendation-value {
  color: #28a745;
}

.recommendation-detail {
  color: #6c757d;
  font-size: 1rem;
  margin-bottom: 0;
}

.recommendation-example {
  color: #17a2b8;
  font-size: 0.9rem;
  font-weight: 600;
  margin-bottom: 1rem;
  font-style: italic;
}

/* Calculator Button */
.calculator-link {
  margin-top: 1rem;
}

.calc-btn {
  background: linear-gradient(135deg, #17a2b8 0%, #138496 100%);
  color: white;
  border: none;
  border-radius: 10px;
  padding: 0.5rem 1rem;
  font-size: 0.9rem;
  font-weight: 600;
  cursor: pointer;
  transition: all 0.3s ease;
}

.calc-btn:hover {
  transform: translateY(-2px);
  box-shadow: 0 4px 15px rgba(23, 162, 184, 0.3);
}

/* Notes Section */
.notes-section {
  margin-top: 1.5rem;
  padding-top: 1.5rem;
  border-top: 1px solid #e9ecef;
}

.notes-title {
  color: #2c3e50;
  font-weight: 700;
  font-size: 1.1rem;
  margin-bottom: 1rem;
}

.notes-list {
  list-style: none;
  padding: 0;
  margin: 0;
}

.note-item {
  display: flex;
  align-items: center;
  justify-content: space-between;
  padding: 0.75rem 0;
  border-bottom: 1px solid #f8f9fa;
}

.note-item:last-child {
  border-bottom: none;
}

.note-text {
  color: #2c3e50;
  font-size: 0.95rem;
  flex: 1;
  margin-right: 1rem;
}

.reference-chip {
  background: #e8f5e8;
  color: #20c997;
  padding: 0.25rem 0.75rem;
  border-radius: 15px;
  font-size: 0.8rem;
  font-weight: 600;
  text-decoration: none;
  border: 1px solid #20c997;
  transition: all 0.3s ease;
  white-space: nowrap;
}

.reference-chip:hover {
  background: #20c997;
  color: white;
  text-decoration: none;
  transform: translateY(-1px);
  box-shadow: 0 2px 8px rgba(32, 201, 151, 0.3);
}

/* Results Section */
.results-section {
  transition: all 0.3s ease;
}

.highlight-results {
  animation: pulse-highlight 2s ease-in-out;
  box-shadow: 0 0 20px rgba(0, 123, 255, 0.3);
  border-radius: 15px;
}

@keyframes pulse-highlight {
  0% { 
    transform: scale(1);
    box-shadow: 0 0 20px rgba(0, 123, 255, 0.3);
  }
  50% { 
    transform: scale(1.02);
    box-shadow: 0 0 30px rgba(0, 123, 255, 0.5);
  }
  100% { 
    transform: scale(1);
    box-shadow: 0 0 20px rgba(0, 123, 255, 0.3);
  }
}

/* Trusted Resources */
.trusted-resources {
  background: #f8f9fa;
  border-radius: 20px;
  padding: 2rem;
}

.resources-title {
  color: #2c3e50;
  font-weight: 700;
  margin-bottom: 1.5rem;
}

.resources-grid {
  display: grid;
  grid-template-columns: repeat(auto-fit, minmax(250px, 1fr));
  gap: 1.5rem;
}

.resource-card {
  background: white;
  border-radius: 15px;
  padding: 1.5rem;
  box-shadow: 0 4px 15px rgba(0,0,0,0.1);
  transition: all 0.3s ease;
  border: 2px solid #f8f9fa;
}

.resource-card:hover {
  transform: translateY(-3px);
  box-shadow: 0 8px 25px rgba(0,0,0,0.15);
  border-color: #007bff;
}


.resource-name {
  color: #2c3e50;
  font-weight: 700;
  font-size: 1.1rem;
  margin-bottom: 0.5rem;
}

.resource-description {
  color: #6c757d;
  font-size: 0.9rem;
  margin-bottom: 1rem;
}

.resource-link {
  color: #007bff;
  text-decoration: none;
  font-weight: 600;
  font-size: 0.9rem;
  transition: all 0.3s ease;
  display: inline-flex;
  align-items: center;
}

.resource-link:hover {
  color: #0056b3;
  text-decoration: none;
  transform: translateX(3px);
}

/* Action Buttons */
.action-buttons .btn {
  border-radius: 15px;
  padding: 0.75rem 1.5rem;
  font-weight: 600;
  transition: all 0.3s ease;
}

.action-buttons .btn:hover {
  transform: translateY(-2px);
  box-shadow: 0 4px 15px rgba(0,0,0,0.2);
}

/* Responsive Design */
@media (max-width: 768px) {
  .progress-steps {
    flex-direction: column;
    gap: 1rem;
  }
  
  .progress-steps::before {
    display: none;
  }
  
  .step-card {
    padding: 2rem;
  }
  
  .step-title {
    font-size: 1.5rem;
  }
  
  .selection-card {
    min-height: 150px;
  }
  
  .card-content {
    padding: 1.5rem;
  }
  
  .card-icon {
    font-size: 2rem;
  }
  
  .recommendation-item {
    flex-direction: column;
    text-align: center;
    padding: 1.5rem;
  }
  
  
  .results-title {
    font-size: 1.8rem;
  }
  
  .alert-content {
    flex-direction: column;
    text-align: center;
  }
}

@media (max-width: 576px) {
  .step-card {
    padding: 1.5rem;
  }
  
  .step-title {
    font-size: 1.3rem;
  }
  
  .selection-card {
    min-height: 120px;
  }
  
  .card-content {
    padding: 1rem;
  }
  
  .card-title {
    font-size: 1.1rem;
  }
  
  .results-title {
    font-size: 1.5rem;
  }
  
  .recommendation-value {
    font-size: 1.3rem;
  }
  
  .resources-grid {
    grid-template-columns: 1fr;
  }
  
  .resource-card {
    padding: 1rem;
  }
  
  .note-item {
    flex-direction: column;
    align-items: flex-start;
    gap: 0.5rem;
  }
  
  .reference-chip {
    align-self: flex-end;
  }
  
  .toggle-slider {
    width: 100px;
  }
  
  .advisory-toggle.active .toggle-knob {
    transform: translateX(60px);
  }
  
  .toggle-labels {
    width: 100px;
  }
}
</style>
