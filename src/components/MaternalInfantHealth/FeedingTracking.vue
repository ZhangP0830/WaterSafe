<script setup>
import { ref, computed, onMounted, nextTick } from "vue";
import MaterialButton from "@/components/MaterialButton.vue";
import { useMaternalInfantStore } from "@/stores/maternalInfantStore";

// Component state
const store = useMaternalInfantStore();
const currentStep = ref(1);
const infantAge = ref('');
const feedingMethod = ref('');
const hydrationGoal = ref(8);
const hydrationIntake = ref(0);
const currentTime = ref(new Date());
const lastFeeding = ref(null);
const feedingHistory = ref([]);
const showToast = ref(false);
const selectedCard = ref('');

// Feeding schedules data
const feedingSchedules = {
  newborn: {
    formula: {
      frequency: 'Every 2-3 hours',
      amount: '60-90ml per feeding',
      dailyTotal: '8-12 feedings',
      notes: 'Use only safe, boiled water for formula preparation',
      schedule: [
        { time: '6:00 AM', amount: '60-90ml', icon: '🍼' },
        { time: '9:00 AM', amount: '60-90ml', icon: '🍼' },
        { time: '12:00 PM', amount: '60-90ml', icon: '🍼' },
        { time: '3:00 PM', amount: '60-90ml', icon: '🍼' },
        { time: '6:00 PM', amount: '60-90ml', icon: '🍼' },
        { time: '9:00 PM', amount: '60-90ml', icon: '🍼' },
        { time: '12:00 AM', amount: '60-90ml', icon: '🍼' },
        { time: '3:00 AM', amount: '60-90ml', icon: '🍼' }
      ]
    },
    breastmilk: {
      frequency: 'Every 2-3 hours',
      amount: 'On demand',
      dailyTotal: '8-12 feedings',
      notes: 'Ensure mother stays well hydrated',
      schedule: [
        { time: '6:00 AM', amount: 'On demand', icon: '🍼' },
        { time: '9:00 AM', amount: 'On demand', icon: '🍼' },
        { time: '12:00 PM', amount: 'On demand', icon: '🍼' },
        { time: '3:00 PM', amount: 'On demand', icon: '🍼' },
        { time: '6:00 PM', amount: 'On demand', icon: '🍼' },
        { time: '9:00 PM', amount: 'On demand', icon: '🍼' },
        { time: '12:00 AM', amount: 'On demand', icon: '🍼' },
        { time: '3:00 AM', amount: 'On demand', icon: '🍼' }
      ]
    }
  },
  '1-3months': {
    formula: {
      frequency: 'Every 3-4 hours',
      amount: '90-120ml per feeding',
      dailyTotal: '6-8 feedings',
      notes: 'May start sleeping longer at night',
      schedule: [
        { time: '6:00 AM', amount: '90-120ml', icon: '🍼' },
        { time: '10:00 AM', amount: '90-120ml', icon: '🍼' },
        { time: '2:00 PM', amount: '90-120ml', icon: '🍼' },
        { time: '6:00 PM', amount: '90-120ml', icon: '🍼' },
        { time: '10:00 PM', amount: '90-120ml', icon: '🍼' },
        { time: '2:00 AM', amount: '90-120ml', icon: '🍼' }
      ]
    },
    breastmilk: {
      frequency: 'Every 3-4 hours',
      amount: 'On demand',
      dailyTotal: '6-8 feedings',
      notes: 'Continue on-demand feeding',
      schedule: [
        { time: '6:00 AM', amount: 'On demand', icon: '🍼' },
        { time: '10:00 AM', amount: 'On demand', icon: '🍼' },
        { time: '2:00 PM', amount: 'On demand', icon: '🍼' },
        { time: '6:00 PM', amount: 'On demand', icon: '🍼' },
        { time: '10:00 PM', amount: 'On demand', icon: '🍼' },
        { time: '2:00 AM', amount: 'On demand', icon: '🍼' }
      ]
    }
  },
  '3-6months': {
    formula: {
      frequency: 'Every 4-5 hours',
      amount: '120-180ml per feeding',
      dailyTotal: '5-6 feedings',
      notes: 'May introduce small amounts of water',
      schedule: [
        { time: '7:00 AM', amount: '120-180ml', icon: '🍼' },
        { time: '12:00 PM', amount: '120-180ml', icon: '🍼' },
        { time: '4:00 PM', amount: '120-180ml', icon: '🍼' },
        { time: '8:00 PM', amount: '120-180ml', icon: '🍼' },
        { time: '12:00 AM', amount: '120-180ml', icon: '🍼' }
      ]
    },
    breastmilk: {
      frequency: 'Every 4-5 hours',
      amount: 'On demand',
      dailyTotal: '5-6 feedings',
      notes: 'Continue breastfeeding with possible water introduction',
      schedule: [
        { time: '7:00 AM', amount: 'On demand', icon: '🍼' },
        { time: '12:00 PM', amount: 'On demand', icon: '🍼' },
        { time: '4:00 PM', amount: 'On demand', icon: '🍼' },
        { time: '8:00 PM', amount: 'On demand', icon: '🍼' },
        { time: '12:00 AM', amount: 'On demand', icon: '🍼' }
      ]
    }
  }
};

// Computed properties
const currentSchedule = computed(() => {
  if (!infantAge.value || !feedingMethod.value) return null;
  return feedingSchedules[infantAge.value][feedingMethod.value];
});

const nextFeedingTime = computed(() => {
  if (!lastFeeding.value) return null;
  
  const lastTime = new Date(lastFeeding.value);
  const interval = infantAge.value === 'newborn' ? 2.5 : 
                   infantAge.value === '1-3months' ? 3.5 : 4.5;
  
  const nextTime = new Date(lastTime.getTime() + (interval * 60 * 60 * 1000));
  return nextTime;
});

const timeUntilNextFeeding = computed(() => {
  if (!nextFeedingTime.value) return null;
  
  const now = new Date();
  const diff = nextFeedingTime.value - now;
  
  if (diff <= 0) return 'Ready for feeding!';
  
  const hours = Math.floor(diff / (1000 * 60 * 60));
  const minutes = Math.floor((diff % (1000 * 60 * 60)) / (1000 * 60));
  
  if (hours > 0) {
    return `${hours}h ${minutes}m`;
  } else {
    return `${minutes}m`;
  }
});

const hydrationProgress = computed(() => {
  return Math.min((hydrationIntake.value / hydrationGoal.value) * 100, 100);
});

const todaysFeedings = computed(() => {
  const today = new Date().toDateString();
  return feedingHistory.value.filter(feeding => 
    new Date(feeding.time).toDateString() === today
  );
});

const canProceed = computed(() => {
  switch (currentStep.value) {
    case 1: return infantAge.value !== '';
    case 2: return feedingMethod.value !== '';
    case 3: return true;
    default: return true;
  }
});

const progressPercentage = computed(() => {
  return (currentStep.value / 4) * 100;
});

// Step navigation methods
const selectInfantAge = (age) => {
  infantAge.value = age;
  selectedCard.value = age;
  setTimeout(() => {
    currentStep.value = 2;
    selectedCard.value = '';
  }, 300);
};

const selectFeedingMethod = (method) => {
  feedingMethod.value = method;
  selectedCard.value = method;
  setTimeout(() => {
    currentStep.value = 3;
    selectedCard.value = '';
  }, 300);
};

const goToDailyLog = () => {
  currentStep.value = 4;
};

const goBack = () => {
  if (currentStep.value > 1) {
    currentStep.value--;
    selectedCard.value = '';
  }
};

const resetToday = () => {
  const today = new Date().toDateString();
  feedingHistory.value = feedingHistory.value.filter(feeding => 
    new Date(feeding.time).toDateString() !== today
  );
  hydrationIntake.value = 0;
  showToastMessage('Today\'s feeding log reset ✅');
};

const showToastMessage = (message) => {
  showToast.value = message;
  setTimeout(() => {
    showToast.value = false;
  }, 3000);
};

// Methods
const recordFeeding = () => {
  const feeding = {
    time: new Date(),
    age: infantAge.value,
    method: feedingMethod.value,
    amount: currentSchedule.value?.amount || 'On demand'
  };
  
  feedingHistory.value.unshift(feeding);
  lastFeeding.value = feeding.time;
  
  // Keep only last 50 feedings
  if (feedingHistory.value.length > 50) {
    feedingHistory.value = feedingHistory.value.slice(0, 50);
  }
  
  // Save to localStorage
  localStorage.setItem('feedingHistory', JSON.stringify(feedingHistory.value));
  localStorage.setItem('lastFeeding', lastFeeding.value.toISOString());
  
  // Show success toast
  showToastMessage('Feeding recorded ✅');
};

const addHydration = (amount) => {
  hydrationIntake.value += amount;
  localStorage.setItem('hydrationIntake', hydrationIntake.value.toString());
};

const resetDailyHydration = () => {
  hydrationIntake.value = 0;
  localStorage.setItem('hydrationIntake', '0');
};

const getAgeLabel = (age) => {
  const labels = {
    newborn: 'Newborn (0-1 month)',
    '1-3months': '1-3 months',
    '3-6months': '3-6 months'
  };
  return labels[age];
};

const formatTime = (date) => {
  return date.toLocaleTimeString([], { hour: '2-digit', minute: '2-digit' });
};

const formatDate = (date) => {
  return date.toLocaleDateString();
};

// Initialize component
const initializeComponent = () => {
  if (store && store.hasBaby) {
    infantAge.value = 'newborn';
    currentStep.value = 2; // Skip age selection if baby is selected
  } else {
    currentStep.value = 1; // Keep age selection if no baby is selected
  }
};

// Load data from localStorage on mount
onMounted(() => {
  initializeComponent();
  
  const savedHistory = localStorage.getItem('feedingHistory');
  if (savedHistory) {
    feedingHistory.value = JSON.parse(savedHistory).map(f => ({
      ...f,
      time: new Date(f.time)
    }));
  }
  
  const savedLastFeeding = localStorage.getItem('lastFeeding');
  if (savedLastFeeding) {
    lastFeeding.value = new Date(savedLastFeeding);
  }
  
  const savedHydration = localStorage.getItem('hydrationIntake');
  if (savedHydration) {
    hydrationIntake.value = parseInt(savedHydration);
  }
  
  // Update time every minute
  setInterval(() => {
    currentTime.value = new Date();
  }, 60000);
});
</script>

<template>
  <div class="feeding-tracking-container">
    <!-- Progress Indicator -->
    <div class="progress-indicator">
      <div class="progress-bar" :style="{ width: progressPercentage + '%' }"></div>
      <div class="progress-steps">
        <div class="step" :class="{ active: currentStep >= 1, completed: currentStep > 1 }">
          <span class="step-number">1</span>
          <span class="step-label">Age</span>
        </div>
        <div class="step" :class="{ active: currentStep >= 2, completed: currentStep > 2 }">
          <span class="step-number">2</span>
          <span class="step-label">Method</span>
        </div>
        <div class="step" :class="{ active: currentStep >= 3, completed: currentStep > 3 }">
          <span class="step-number">3</span>
          <span class="step-label">Schedule</span>
        </div>
        <div class="step" :class="{ active: currentStep >= 4 }">
          <span class="step-number">4</span>
          <span class="step-label">Log</span>
        </div>
      </div>
    </div>

    <!-- Step 1: Infant Age Selection -->
    <div v-if="currentStep === 1" class="step-container">
      <div class="step-header">
        <h2 class="step-title">Choose Your Baby's Age</h2>
        <p class="step-subtitle">Select the age range that best fits your little one</p>
        <div v-if="!store || !store.hasBaby" class="alert alert-info">
          <i class="fas fa-info-circle me-2"></i>
          This feature is designed for parents with babies. Please select "My little one" in your profile.
        </div>
      </div>
      
      <div class="selection-cards">
        <div 
          class="selection-card" 
          :class="{ selected: selectedCard === 'newborn' }"
          @click="selectInfantAge('newborn')"
        >
          <div class="card-icon">👶</div>
          <h3 class="card-title">Newborn</h3>
          <p class="card-subtitle">0-1 month old</p>
          <div class="card-details">
            <p>• Every 2-3 hours</p>
            <p>• 8-12 feedings daily</p>
          </div>
        </div>
        
        <div 
          class="selection-card" 
          :class="{ selected: selectedCard === '1-3months' }"
          @click="selectInfantAge('1-3months')"
        >
          <div class="card-icon">🍼</div>
          <h3 class="card-title">1-3 Months</h3>
          <p class="card-subtitle">Growing baby</p>
          <div class="card-details">
            <p>• Every 3-4 hours</p>
            <p>• 6-8 feedings daily</p>
          </div>
        </div>
        
        <div 
          class="selection-card" 
          :class="{ selected: selectedCard === '3-6months' }"
          @click="selectInfantAge('3-6months')"
        >
          <div class="card-icon">🌟</div>
          <h3 class="card-title">3-6 Months</h3>
          <p class="card-subtitle">More active baby</p>
          <div class="card-details">
            <p>• Every 4-5 hours</p>
            <p>• 5-6 feedings daily</p>
          </div>
        </div>
      </div>
    </div>

    <!-- Step 2: Feeding Method Selection -->
    <div v-if="currentStep === 2" class="step-container">
      <div class="step-header">
        <button class="back-btn" @click="goBack">
          <i class="fas fa-arrow-left"></i> Back
        </button>
        <h2 class="step-title">Choose Feeding Method</h2>
        <p class="step-subtitle">Select how you're feeding your baby</p>
      </div>
      
      <div class="selection-cards">
        <div 
          class="selection-card" 
          :class="{ selected: selectedCard === 'breastmilk' }"
          @click="selectFeedingMethod('breastmilk')"
        >
          <div class="card-icon">🤱</div>
          <h3 class="card-title">Breastfeeding</h3>
          <p class="card-subtitle">Natural feeding</p>
          <div class="card-details">
            <p>• On-demand feeding</p>
            <p>• Stay hydrated</p>
            <p>• No preparation needed</p>
          </div>
        </div>
        
        <div 
          class="selection-card" 
          :class="{ selected: selectedCard === 'formula' }"
          @click="selectFeedingMethod('formula')"
        >
          <div class="card-icon">🍼</div>
          <h3 class="card-title">Formula Feeding</h3>
          <p class="card-subtitle">Prepared feeding</p>
          <div class="card-details">
            <p>• Measured amounts</p>
            <p>• Safe water needed</p>
            <p>• Preparation required</p>
          </div>
        </div>
      </div>
    </div>

    <!-- Step 3: Schedule & Hydration -->
    <div v-if="currentStep === 3" class="step-container">
      <div class="step-header">
        <button class="back-btn" @click="goBack">
          <i class="fas fa-arrow-left"></i> Back
        </button>
        <h2 class="step-title">Your Feeding Schedule</h2>
        <p class="step-subtitle">Here's your personalized plan</p>
      </div>

      <div class="schedule-section">
        <!-- Feeding Schedule -->
        <div class="schedule-card">
          <h3 class="schedule-title">
            <i class="fas fa-clock me-2"></i>
            Daily Feeding Schedule
          </h3>
          
          <div class="schedule-grid">
            <div 
              v-for="(feeding, index) in currentSchedule?.schedule" 
              :key="index"
              class="schedule-item"
              :class="{ 'alternate': index % 2 === 1 }"
            >
              <div class="schedule-time">
                <span class="time-icon">🕐</span>
                {{ feeding.time }}
              </div>
              <div class="schedule-amount">
                <span class="amount-icon">🍼</span>
                {{ feeding.amount }}
              </div>
            </div>
          </div>
        </div>

        <!-- Hydration Section -->
        <div class="hydration-section">
          <div v-if="feedingMethod === 'breastmilk'" class="breastfeeding-note">
            <div class="note-icon">💧</div>
            <div class="note-content">
              <h4>Stay Hydrated</h4>
              <p>Drink water before and after each feeding to support your milk supply</p>
            </div>
          </div>
          
          <div v-else class="hydration-tracker">
            <h3 class="hydration-title">
              <i class="fas fa-tint me-2"></i>
              Your Daily Hydration Goal
            </h3>
            
            <div class="hydration-circle">
              <div class="hydration-progress" :style="{ '--progress': hydrationProgress + '%' }">
                <span class="hydration-percentage">{{ hydrationProgress }}%</span>
              </div>
            </div>
            
            <div class="hydration-stats">
              <span class="current">{{ hydrationIntake }}</span> / 
              <span class="goal">{{ hydrationGoal }}</span> glasses
            </div>
            
            <div class="hydration-buttons">
              <button @click="addHydration(1)" class="hydration-btn">
                +1 Glass
              </button>
              <button @click="addHydration(2)" class="hydration-btn">
                +2 Glasses
              </button>
              <button @click="resetDailyHydration" class="hydration-btn reset">
                Reset
              </button>
            </div>
          </div>
        </div>

        <!-- Safe Formula Prep (only for formula feeding) -->
        <div v-if="feedingMethod === 'formula'" class="formula-prep">
          <h3 class="prep-title">
            <i class="fas fa-shield-alt me-2"></i>
            Safe Formula Preparation
          </h3>
          
          <div class="prep-steps">
            <div class="prep-step">
              <div class="step-number">1</div>
              <div class="step-content">
                <h4>Wash Hands</h4>
                <p>Clean hands thoroughly with soap and water</p>
              </div>
            </div>
            <div class="prep-step">
              <div class="step-number">2</div>
              <div class="step-content">
                <h4>Boil Water</h4>
                <p>Bring water to rolling boil for 1 minute</p>
              </div>
            </div>
            <div class="prep-step">
              <div class="step-number">3</div>
              <div class="step-content">
                <h4>Cool & Mix</h4>
                <p>Let water cool to room temperature, then add formula</p>
              </div>
            </div>
            <div class="prep-step">
              <div class="step-number">4</div>
              <div class="step-content">
                <h4>Feed Immediately</h4>
                <p>Use within 2 hours or refrigerate for 24 hours</p>
              </div>
            </div>
          </div>
        </div>

        <!-- Action Buttons -->
        <div class="action-buttons">
          <button @click="goToDailyLog" class="btn-primary">
            Start Daily Log
            <i class="fas fa-arrow-right ms-2"></i>
          </button>
        </div>
      </div>
    </div>

    <!-- Step 4: Daily Log -->
    <div v-if="currentStep === 4" class="step-container">
      <div class="step-header">
        <button class="back-btn" @click="goBack">
          <i class="fas fa-arrow-left"></i> Back
        </button>
        <h2 class="step-title">Daily Feeding Log</h2>
        <p class="step-subtitle">Track your baby's feedings today</p>
      </div>

      <div class="log-section">
        <!-- Quick Actions -->
        <div class="quick-actions">
          <button @click="recordFeeding" class="record-btn">
            <i class="fas fa-plus me-2"></i>
            Record Feeding
          </button>
          <button @click="resetToday" class="reset-btn">
            <i class="fas fa-undo me-2"></i>
            Reset Today
          </button>
        </div>

        <!-- Today's Feedings -->
        <div class="feedings-list">
          <h3 class="list-title">Today's Feedings</h3>
          
          <div v-if="todaysFeedings.length === 0" class="empty-state">
            <div class="empty-icon">🍼</div>
            <p>No feedings recorded today yet</p>
          </div>
          
          <div v-else class="feedings-grid">
            <div 
              v-for="feeding in todaysFeedings" 
              :key="feeding.time"
              class="feeding-item"
            >
              <div class="feeding-time">
                {{ new Date(feeding.time).toLocaleTimeString([], { hour: '2-digit', minute: '2-digit' }) }}
              </div>
              <div class="feeding-details">
                <span class="feeding-method" :class="feeding.method">
                  {{ feeding.method === 'formula' ? 'Formula' : 'Breastmilk' }}
                </span>
                <span class="feeding-amount">{{ feeding.amount }}</span>
              </div>
            </div>
          </div>
        </div>
      </div>
    </div>

    <!-- Success Toast -->
    <div v-if="showToast" class="toast-container">
      <div class="success-toast">
        <i class="fas fa-check-circle me-2"></i>
        {{ showToast }}
      </div>
    </div>
  </div>
</template>

<style scoped>
/* Container */
.feeding-tracking-container {
  min-height: 100vh;
  background: linear-gradient(135deg, #f8f9fa 0%, #e3f2fd 100%);
  padding: 2rem 1rem;
}

/* Progress Indicator */
.progress-indicator {
  max-width: 800px;
  margin: 0 auto 3rem;
  position: relative;
}

.progress-bar {
  height: 4px;
  background: linear-gradient(90deg, #007bff, #0056b3);
  border-radius: 2px;
  transition: width 0.3s ease;
}

.progress-steps {
  display: flex;
  justify-content: space-between;
  margin-top: 1rem;
}

.step {
  display: flex;
  flex-direction: column;
  align-items: center;
  gap: 0.5rem;
}

.step-number {
  width: 40px;
  height: 40px;
  border-radius: 50%;
  background: #e9ecef;
  color: #6c757d;
  display: flex;
  align-items: center;
  justify-content: center;
  font-weight: 700;
  transition: all 0.3s ease;
}

.step.active .step-number {
  background: linear-gradient(135deg, #007bff 0%, #0056b3 100%);
  color: white;
  box-shadow: 0 0 0 4px rgba(0, 123, 255, 0.3);
}

.step.completed .step-number {
  background: linear-gradient(135deg, #28a745 0%, #20c997 100%);
  color: white;
}

.step-label {
  font-size: 0.9rem;
  font-weight: 600;
  color: #6c757d;
}

.step.active .step-label {
  color: #007bff;
}

/* Step Container */
.step-container {
  max-width: 900px;
  margin: 0 auto;
}

.step-header {
  text-align: center;
  margin-bottom: 3rem;
  position: relative;
}

.back-btn {
  position: absolute;
  left: 0;
  top: 0;
  background: rgba(255, 255, 255, 0.9);
  border: 2px solid #A7D8F0;
  border-radius: 12px;
  padding: 0.75rem 1.5rem;
  color: #2c3e50;
  font-weight: 600;
  transition: all 0.3s ease;
  cursor: pointer;
}

.back-btn:hover {
  background: #A7D8F0;
  color: white;
  transform: translateX(-3px);
}

.step-title {
  font-size: 2.5rem;
  font-weight: 700;
  color: #2c3e50;
  margin-bottom: 1rem;
}

.step-subtitle {
  font-size: 1.2rem;
  color: #6c757d;
  margin-bottom: 0;
}

/* Selection Cards */
.selection-cards {
  display: grid;
  grid-template-columns: repeat(auto-fit, minmax(280px, 1fr));
  gap: 2rem;
  margin-bottom: 2rem;
}

.selection-card {
  background: rgba(255, 255, 255, 0.9);
  border-radius: 16px;
  padding: 2rem;
  text-align: center;
  cursor: pointer;
  transition: all 0.3s ease;
  border: 3px solid transparent;
  box-shadow: 0 4px 15px rgba(0, 0, 0, 0.1);
}

.selection-card:hover {
  transform: translateY(-5px);
  box-shadow: 0 8px 25px rgba(0, 0, 0, 0.15);
}

.selection-card.selected {
  border-color: #A7D8F0;
  background: rgba(167, 216, 240, 0.1);
  transform: translateY(-5px);
  box-shadow: 0 8px 25px rgba(167, 216, 240, 0.3);
}

.card-icon {
  font-size: 3rem;
  margin-bottom: 1rem;
}

.card-title {
  font-size: 1.5rem;
  font-weight: 700;
  color: #2c3e50;
  margin-bottom: 0.5rem;
}

.card-subtitle {
  color: #6c757d;
  margin-bottom: 1rem;
}

.card-details p {
  margin: 0.5rem 0;
  color: #495057;
  font-size: 0.95rem;
}

/* Schedule Section */
.schedule-section {
  display: flex;
  flex-direction: column;
  gap: 2rem;
}

.schedule-card {
  background: rgba(255, 255, 255, 0.9);
  border-radius: 16px;
  padding: 2rem;
  box-shadow: 0 4px 15px rgba(0, 0, 0, 0.1);
}

.schedule-title {
  font-size: 1.5rem;
  font-weight: 700;
  color: #2c3e50;
  margin-bottom: 1.5rem;
  display: flex;
  align-items: center;
}

.schedule-grid {
  display: flex;
  flex-direction: column;
  gap: 0.5rem;
}

.schedule-item {
  display: flex;
  justify-content: space-between;
  align-items: center;
  padding: 1rem;
  border-radius: 12px;
  background: #f8f9fa;
  transition: all 0.3s ease;
}

.schedule-item.alternate {
  background: #F9FAFB;
}

.schedule-item:hover {
  background: rgba(167, 216, 240, 0.1);
  transform: translateX(5px);
}

.schedule-time, .schedule-amount {
  display: flex;
  align-items: center;
  gap: 0.5rem;
  font-weight: 600;
  color: #2c3e50;
}

.time-icon, .amount-icon {
  font-size: 1.2rem;
}

/* Hydration Section */
.hydration-section {
  background: rgba(255, 255, 255, 0.9);
  border-radius: 16px;
  padding: 2rem;
  box-shadow: 0 4px 15px rgba(0, 0, 0, 0.1);
}

.breastfeeding-note {
  display: flex;
  align-items: center;
  gap: 1.5rem;
  padding: 1.5rem;
  background: linear-gradient(135deg, #F9C5D1, #A7D8F0);
  border-radius: 12px;
  color: #2c3e50;
}

.note-icon {
  font-size: 3rem;
}

.note-content h4 {
  font-size: 1.3rem;
  font-weight: 700;
  margin-bottom: 0.5rem;
}

.note-content p {
  margin: 0;
  font-size: 1rem;
}

.hydration-tracker {
  text-align: center;
}

.hydration-title {
  font-size: 1.5rem;
  font-weight: 700;
  color: #2c3e50;
  margin-bottom: 1.5rem;
  display: flex;
  align-items: center;
  justify-content: center;
}

.hydration-circle {
  width: 150px;
  height: 150px;
  margin: 0 auto 1.5rem;
  position: relative;
}

.hydration-progress {
  width: 100%;
  height: 100%;
  border-radius: 50%;
  background: conic-gradient(#20C997 0deg, #20C997 calc(var(--progress) * 3.6deg), #e9ecef calc(var(--progress) * 3.6deg));
  display: flex;
  align-items: center;
  justify-content: center;
  position: relative;
}

.hydration-progress::before {
  content: '';
  position: absolute;
  width: 80%;
  height: 80%;
  background: white;
  border-radius: 50%;
}

.hydration-percentage {
  position: relative;
  z-index: 1;
  font-size: 1.5rem;
  font-weight: 700;
  color: #2c3e50;
}

.hydration-stats {
  font-size: 1.2rem;
  margin-bottom: 1.5rem;
}

.hydration-stats .current {
  font-weight: 700;
  color: #20C997;
  font-size: 1.5rem;
}

.hydration-stats .goal {
  color: #6c757d;
}

.hydration-buttons {
  display: flex;
  gap: 1rem;
  justify-content: center;
  flex-wrap: wrap;
}

.hydration-btn {
  background: rgba(167, 216, 240, 0.2);
  border: 2px solid #A7D8F0;
  border-radius: 12px;
  padding: 0.75rem 1.5rem;
  color: #2c3e50;
  font-weight: 600;
  cursor: pointer;
  transition: all 0.3s ease;
}

.hydration-btn:hover {
  background: #A7D8F0;
  color: white;
  transform: translateY(-2px);
}

.hydration-btn.reset {
  border-color: #F9C5D1;
  background: rgba(249, 197, 209, 0.2);
}

.hydration-btn.reset:hover {
  background: #F9C5D1;
}

/* Formula Prep */
.formula-prep {
  background: rgba(255, 255, 255, 0.9);
  border-radius: 16px;
  padding: 2rem;
  box-shadow: 0 4px 15px rgba(0, 0, 0, 0.1);
}

.prep-title {
  font-size: 1.5rem;
  font-weight: 700;
  color: #2c3e50;
  margin-bottom: 1.5rem;
  display: flex;
  align-items: center;
}

.prep-steps {
  display: grid;
  grid-template-columns: repeat(auto-fit, minmax(200px, 1fr));
  gap: 1.5rem;
}

.prep-step {
  display: flex;
  align-items: flex-start;
  gap: 1rem;
  padding: 1.5rem;
  background: #f8f9fa;
  border-radius: 12px;
  border: 2px solid transparent;
  transition: all 0.3s ease;
}

.prep-step:hover {
  border-color: #A7D8F0;
  background: rgba(167, 216, 240, 0.1);
  transform: translateY(-2px);
}

.prep-step .step-number {
  width: 40px;
  height: 40px;
  border-radius: 50%;
  background: #A7D8F0;
  color: white;
  display: flex;
  align-items: center;
  justify-content: center;
  font-weight: 700;
  flex-shrink: 0;
}

.step-content h4 {
  font-size: 1.1rem;
  font-weight: 700;
  color: #2c3e50;
  margin-bottom: 0.5rem;
}

.step-content p {
  margin: 0;
  color: #6c757d;
  font-size: 0.95rem;
}

/* Action Buttons */
.action-buttons {
  text-align: center;
  margin-top: 2rem;
}

.btn-primary {
  background: linear-gradient(135deg, #A7D8F0, #B3E3C0);
  border: none;
  border-radius: 16px;
  padding: 1rem 2rem;
  color: #2c3e50;
  font-size: 1.1rem;
  font-weight: 700;
  cursor: pointer;
  transition: all 0.3s ease;
  display: inline-flex;
  align-items: center;
}

.btn-primary:hover {
  transform: translateY(-3px);
  box-shadow: 0 8px 25px rgba(167, 216, 240, 0.4);
}

/* Log Section */
.log-section {
  display: flex;
  flex-direction: column;
  gap: 2rem;
}

.quick-actions {
  display: flex;
  gap: 1rem;
  justify-content: center;
  flex-wrap: wrap;
}

.record-btn, .reset-btn {
  border: none;
  border-radius: 16px;
  padding: 1rem 2rem;
  font-size: 1.1rem;
  font-weight: 700;
  cursor: pointer;
  transition: all 0.3s ease;
  display: inline-flex;
  align-items: center;
}

.record-btn {
  background: linear-gradient(135deg, #B3E3C0, #A7D8F0);
  color: #2c3e50;
}

.reset-btn {
  background: linear-gradient(135deg, #F9C5D1, #A7D8F0);
  color: #2c3e50;
}

.record-btn:hover, .reset-btn:hover {
  transform: translateY(-3px);
  box-shadow: 0 8px 25px rgba(0, 0, 0, 0.2);
}

.feedings-list {
  background: rgba(255, 255, 255, 0.9);
  border-radius: 16px;
  padding: 2rem;
  box-shadow: 0 4px 15px rgba(0, 0, 0, 0.1);
}

.list-title {
  font-size: 1.5rem;
  font-weight: 700;
  color: #2c3e50;
  margin-bottom: 1.5rem;
  text-align: center;
}

.empty-state {
  text-align: center;
  padding: 3rem;
  color: #6c757d;
}

.empty-icon {
  font-size: 4rem;
  margin-bottom: 1rem;
}

.feedings-grid {
  display: flex;
  flex-direction: column;
  gap: 1rem;
}

.feeding-item {
  display: flex;
  justify-content: space-between;
  align-items: center;
  padding: 1rem;
  background: #f8f9fa;
  border-radius: 12px;
  transition: all 0.3s ease;
}

.feeding-item:hover {
  background: rgba(167, 216, 240, 0.1);
  transform: translateX(5px);
}

.feeding-time {
  font-weight: 700;
  color: #2c3e50;
  font-size: 1.1rem;
}

.feeding-details {
  display: flex;
  flex-direction: column;
  align-items: flex-end;
  gap: 0.25rem;
}

.feeding-method {
  padding: 0.25rem 0.75rem;
  border-radius: 20px;
  font-size: 0.85rem;
  font-weight: 600;
}

.feeding-method.formula {
  background: #A7D8F0;
  color: #2c3e50;
}

.feeding-method.breastmilk {
  background: #B3E3C0;
  color: #2c3e50;
}

.feeding-amount {
  font-size: 0.9rem;
  color: #6c757d;
}

/* Toast */
.toast-container {
  position: fixed;
  top: 20px;
  right: 20px;
  z-index: 1000;
}

.success-toast {
  background: linear-gradient(135deg, #B3E3C0, #A7D8F0);
  color: #2c3e50;
  padding: 1rem 1.5rem;
  border-radius: 12px;
  box-shadow: 0 4px 15px rgba(0, 0, 0, 0.2);
  font-weight: 600;
  display: flex;
  align-items: center;
  animation: slideInRight 0.3s ease;
}

@keyframes slideInRight {
  from {
    transform: translateX(100%);
    opacity: 0;
  }
  to {
    transform: translateX(0);
    opacity: 1;
  }
}

/* Responsive Design */
@media (max-width: 768px) {
  .feeding-tracking-container {
    padding: 1rem 0.5rem;
  }
  
  .step-title {
    font-size: 2rem;
  }
  
  .selection-cards {
    grid-template-columns: 1fr;
    gap: 1rem;
  }
  
  .selection-card {
    padding: 1.5rem;
  }
  
  .schedule-item {
    flex-direction: column;
    gap: 0.5rem;
    text-align: center;
  }
  
  .prep-steps {
    grid-template-columns: 1fr;
  }
  
  .quick-actions {
    flex-direction: column;
    align-items: center;
  }
  
  .feeding-item {
    flex-direction: column;
    gap: 0.5rem;
    text-align: center;
  }
  
  .feeding-details {
    align-items: center;
  }
  
  .back-btn {
    position: relative;
    margin-bottom: 1rem;
  }
}
</style>