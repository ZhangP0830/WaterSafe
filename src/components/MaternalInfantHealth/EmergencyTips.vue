<script setup>
import { ref, computed, onMounted } from "vue";
import MaterialButton from "@/components/MaterialButton.vue";
import { useMaternalInfantStore } from "@/stores/maternalInfantStore";

// Component state
const store = useMaternalInfantStore();
const currentStep = ref(1);
const emergencyStatus = ref('');
const selectedActions = ref([]);

// Emergency status options
const emergencyStatuses = [
  {
    id: 'detected',
    title: 'Detected',
    description: 'Contamination has been confirmed in your area',
    priority: 'high',
    color: '#DC2626',
    icon: 'fas fa-exclamation-triangle'
  },
  {
    id: 'suspected',
    title: 'Suspected',
    description: 'Contamination is suspected but not yet confirmed',
    priority: 'medium',
    color: '#F59E0B',
    icon: 'fas fa-question-circle'
  },
  {
    id: 'cleared',
    title: 'Cleared',
    description: 'Contamination has been cleared and water is safe',
    priority: 'safe',
    color: '#10B981',
    icon: 'fas fa-check-circle'
  }
];


// Emergency actions based on status and target
const getEmergencyActions = () => {
  const actions = [];
  
  if (emergencyStatus.value === 'detected') {
    if (store && store.isExpecting) {
      actions.push(
        {
          id: 'stop-water',
          title: 'Stop Using Tap Water Immediately',
          description: 'Do not drink, cook with, or use tap water for any purpose',
          reason: 'Contaminated water can cause serious health issues for you and your baby',
          priority: 'high',
          color: '#DC2626',
          icon: 'fas fa-ban',
          steps: [
            'Turn off all water sources',
            'Do not use tap water for drinking, cooking, or brushing teeth',
            'Do not use tap water for washing dishes or preparing formula',
            'Do not use tap water for bathing or showering'
          ]
        },
        {
          id: 'use-safe-water',
          title: 'Use Safe Water Sources Only',
          description: 'Switch to bottled water or properly treated water immediately',
          reason: 'Safe water is essential for your health and your baby\'s development',
          priority: 'high',
          color: '#DC2626',
          icon: 'fas fa-tint',
          steps: [
            'Use only bottled water for drinking and cooking',
            'Use bottled water for preparing formula',
            'Use bottled water for brushing teeth',
            'Boil bottled water if formula preparation requires it'
          ]
        },
        {
          id: 'contact-doctor',
          title: 'Contact Your Healthcare Provider',
          description: 'Inform your doctor about the contamination and any symptoms',
          reason: 'Your doctor can provide specific guidance for your pregnancy',
          priority: 'medium',
          color: '#F59E0B',
          icon: 'fas fa-user-md',
          steps: [
            'Call your OB/GYN immediately',
            'Report any symptoms you may be experiencing',
            'Ask about additional precautions for pregnancy',
            'Schedule an appointment if recommended'
          ]
        },
        {
          id: 'monitor-health',
          title: 'Monitor Your Health',
          description: 'Watch for any symptoms related to water contamination',
          reason: 'Early detection of symptoms can prevent complications',
          priority: 'medium',
          color: '#F59E0B',
          icon: 'fas fa-heartbeat',
          steps: [
            'Watch for nausea, vomiting, or diarrhea',
            'Monitor for fever or unusual fatigue',
            'Check for any changes in baby movement',
            'Keep a symptom diary'
          ]
        }
      );
    } else if (store && store.hasBaby) {
      actions.push(
        {
          id: 'stop-baby-water',
          title: 'Stop Using Tap Water for Baby',
          description: 'Immediately stop all tap water use for your infant',
          reason: 'Infants are more vulnerable to water contamination',
          priority: 'high',
          color: '#DC2626',
          icon: 'fas fa-baby',
          steps: [
            'Do not use tap water for formula preparation',
            'Do not use tap water for baby bottles or sippy cups',
            'Do not use tap water for baby food preparation',
            'Do not use tap water for baby bathing'
          ]
        },
        {
          id: 'use-safe-baby-water',
          title: 'Switch to Safe Water Sources',
          description: 'Use only safe water for all baby needs',
          reason: 'Safe water is critical for your baby\'s health and development',
          priority: 'high',
          color: '#DC2626',
          icon: 'fas fa-shield-alt',
          steps: [
            'Use bottled water for formula preparation',
            'Use bottled water for baby bottles',
            'Use bottled water for baby food',
            'Boil bottled water before use if recommended'
          ]
        },
        {
          id: 'contact-pediatrician',
          title: 'Contact Pediatrician',
          description: 'Inform your baby\'s doctor about the contamination',
          reason: 'Your pediatrician can provide specific guidance for your baby',
          priority: 'medium',
          color: '#F59E0B',
          icon: 'fas fa-stethoscope',
          steps: [
            'Call your pediatrician immediately',
            'Report any symptoms your baby may have',
            'Ask about additional precautions for infants',
            'Schedule an appointment if recommended'
          ]
        },
        {
          id: 'monitor-baby-health',
          title: 'Monitor Baby\'s Health',
          description: 'Watch for signs of illness in your baby',
          reason: 'Early detection of symptoms can prevent serious complications',
          priority: 'medium',
          color: '#F59E0B',
          icon: 'fas fa-baby-carriage',
          steps: [
            'Watch for changes in feeding patterns',
            'Monitor for unusual fussiness or lethargy',
            'Check for fever, vomiting, or diarrhea',
            'Count wet diapers to monitor hydration'
          ]
        }
      );
    }
  } else if (emergencyStatus.value === 'suspected') {
    if (store && store.isExpecting) {
      actions.push(
        {
          id: 'take-precautions',
          title: 'Take Precautions',
          description: 'Use caution until contamination is confirmed or cleared',
          reason: 'Better to be safe than sorry during pregnancy',
          priority: 'medium',
          color: '#F59E0B',
          icon: 'fas fa-exclamation-circle',
          steps: [
            'Consider using bottled water for drinking',
            'Boil tap water before using for cooking',
            'Avoid using tap water for formula preparation',
            'Monitor local news for updates'
          ]
        },
        {
          id: 'prepare-supplies',
          title: 'Prepare Emergency Supplies',
          description: 'Get ready in case contamination is confirmed',
          reason: 'Being prepared helps reduce stress and ensures safety',
          priority: 'safe',
          color: '#10B981',
          icon: 'fas fa-shopping-cart',
          steps: [
            'Stock up on bottled water',
            'Prepare emergency water storage',
            'Have backup formula ready',
            'Keep emergency contacts handy'
          ]
        }
      );
    } else if (store && store.hasBaby) {
      actions.push(
        {
          id: 'take-baby-precautions',
          title: 'Take Precautions for Baby',
          description: 'Use extra caution with your baby\'s water needs',
          reason: 'Infants need extra protection from potential contamination',
          priority: 'medium',
          color: '#F59E0B',
          icon: 'fas fa-baby',
          steps: [
            'Use bottled water for formula preparation',
            'Boil tap water before using for baby food',
            'Avoid using tap water for baby bottles',
            'Monitor baby for any unusual symptoms'
          ]
        },
        {
          id: 'prepare-baby-supplies',
          title: 'Prepare Emergency Supplies',
          description: 'Get ready with safe water supplies for your baby',
          reason: 'Having supplies ready ensures your baby\'s safety',
          priority: 'safe',
          color: '#10B981',
          icon: 'fas fa-box',
          steps: [
            'Stock up on bottled water for baby',
            'Have extra formula ready',
            'Prepare emergency baby food',
            'Keep pediatrician\'s number handy'
          ]
        }
      );
    }
  } else if (emergencyStatus.value === 'cleared') {
    if (store && store.isExpecting) {
      actions.push(
        {
          id: 'follow-guidance',
          title: 'Follow Official Guidance',
          description: 'Wait for official confirmation before resuming normal water use',
          reason: 'Official clearance ensures the water is truly safe',
          priority: 'safe',
          color: '#10B981',
          icon: 'fas fa-check-circle',
          steps: [
            'Wait for official clearance announcement',
            'Follow any flushing instructions provided',
            'Start with cold water taps first',
            'Run water for recommended time before use'
          ]
        },
        {
          id: 'resume-gradually',
          title: 'Gradually Resume Normal Use',
          description: 'Slowly return to normal water usage patterns',
          reason: 'Gradual resumption helps ensure safety and peace of mind',
          priority: 'safe',
          color: '#10B981',
          icon: 'fas fa-arrow-up',
          steps: [
            'Start with drinking water first',
            'Gradually resume cooking with tap water',
            'Return to normal bathing routines',
            'Continue monitoring your health'
          ]
        }
      );
    } else if (store && store.hasBaby) {
      actions.push(
        {
          id: 'follow-baby-guidance',
          title: 'Follow Official Guidance for Baby',
          description: 'Wait for official confirmation before resuming normal water use for baby',
          reason: 'Official clearance ensures the water is safe for your baby',
          priority: 'safe',
          color: '#10B981',
          icon: 'fas fa-baby',
          steps: [
            'Wait for official clearance announcement',
            'Follow any flushing instructions provided',
            'Start with cold water taps first',
            'Run water for recommended time before use'
          ]
        },
        {
          id: 'resume-baby-gradually',
          title: 'Gradually Resume Baby Water Use',
          description: 'Slowly return to normal water usage for your baby',
          reason: 'Gradual resumption ensures your baby\'s safety',
          priority: 'safe',
          color: '#10B981',
          icon: 'fas fa-arrow-up',
          steps: [
            'Start with formula preparation first',
            'Gradually resume baby food preparation',
            'Return to normal baby bathing routines',
            'Continue monitoring baby\'s health'
          ]
        }
      );
    }
  }
  
  return actions;
};

// Emergency contacts
const emergencyContacts = [
  {
    name: 'Emergency Services',
    number: '000',
    priority: 'urgent',
    color: '#DC2626',
    icon: 'fas fa-ambulance',
    description: 'Police, Fire, Ambulance'
  },
  {
    name: 'Poisons Information Centre',
    number: '13 11 26',
    priority: 'high',
    color: '#F59E0B',
    icon: 'fas fa-exclamation-triangle',
    description: '24/7 poison advice'
  },
  {
    name: 'Victorian Department of Health',
    number: '1300 650 172',
    priority: 'medium',
    color: '#10B981',
    icon: 'fas fa-building',
    description: 'Health advice and information'
  },
  {
    name: 'Melbourne Water',
    number: '131 722',
    priority: 'medium',
    color: '#10B981',
    icon: 'fas fa-tint',
    description: 'Water quality and supply issues'
  },
  {
    name: 'Healthdirect Australia',
    number: '1800 022 222',
    priority: 'medium',
    color: '#007bff',
    icon: 'fas fa-phone',
    description: 'Free health advice 24/7'
  },
  {
    name: 'Australian Red Cross',
    number: '1800 733 276',
    priority: 'medium',
    color: '#dc3545',
    icon: 'fas fa-cross',
    description: 'Emergency assistance'
  },
  {
    name: 'Victorian Emergency Management',
    number: '1800 226 226',
    priority: 'medium',
    color: '#6c757d',
    icon: 'fas fa-shield-alt',
    description: 'Emergency management advice'
  },
  {
    name: 'Maternal & Child Health Line',
    number: '13 22 29',
    priority: 'medium',
    color: '#e83e8c',
    icon: 'fas fa-baby',
    description: '24/7 parenting support'
  }
];

// Computed properties
const currentEmergencyStatus = computed(() => {
  return emergencyStatuses.find(status => status.id === emergencyStatus.value);
});

const currentGuidanceTarget = computed(() => {
  return guidanceTargets.find(target => target.id === guidanceTarget.value);
});

const availableActions = computed(() => {
  return getEmergencyActions();
});

const isStepComplete = (step) => {
  switch (step) {
    case 1: return emergencyStatus.value !== '';
    case 2: return emergencyStatus.value !== '' && availableActions.value.length > 0;
    case 3: return currentStep.value >= 3;
    default: return false;
  }
};

const canProceed = computed(() => {
  return isStepComplete(currentStep.value);
});

const canGoBack = computed(() => {
  return currentStep.value > 1;
});

// Methods
const selectEmergencyStatus = (statusId) => {
  emergencyStatus.value = statusId;
  nextStep();
};

const initializeComponent = () => {
  currentStep.value = 1; // Start at emergency status selection
};

const nextStep = () => {
  if (currentStep.value < 3) {
    currentStep.value++;
  }
};

const prevStep = () => {
  if (currentStep.value > 1) {
    currentStep.value--;
  }
};

const resetGuide = () => {
  currentStep.value = 1;
  emergencyStatus.value = '';
  selectedActions.value = [];
};

const callEmergency = (number) => {
  if (number === '911') {
    window.location.href = 'tel:911';
  } else if (number.startsWith('1-800')) {
    window.location.href = `tel:${number}`;
  } else {
    // For local numbers, show a message
    alert(`Please call: ${number}`);
  }
};

const getPriorityColor = (priority) => {
  switch (priority) {
    case 'urgent': return '#DC2626';
    case 'high': return '#DC2626';
    case 'medium': return '#F59E0B';
    case 'safe': return '#10B981';
    default: return '#6B7280';
  }
};

const getPriorityLabel = (priority) => {
  switch (priority) {
    case 'urgent': return 'URGENT';
    case 'high': return 'HIGH PRIORITY';
    case 'medium': return 'MEDIUM PRIORITY';
    case 'safe': return 'SAFE';
    default: return 'UNKNOWN';
  }
};

// Initialize component
onMounted(() => {
  initializeComponent();
});
</script>

<template>
  <div class="emergency-safety-guide">
    <!-- Header -->
    <div class="section-header text-center mb-5">
      <h1 class="display-6 fw-bold mb-3">Emergency Safety Guide</h1>
      <p class="lead text-muted">Follow these steps calmly and act promptly during water contamination events</p>
    </div>

    <!-- Enhanced Progress Indicator -->
    <div class="progress-indicator mb-5">
      <div class="progress-container">
        <div class="progress-line"></div>
        <div class="progress-step" v-for="step in 3" :key="step" :class="{ 
          active: step === currentStep, 
          completed: isStepComplete(step) 
        }">
          <div class="step-circle">
            <span v-if="!isStepComplete(step) || step >= currentStep" class="step-number">{{ step }}</span>
            <div v-else class="step-completed">
              <span class="step-number-small">{{ step }}</span>
              <i class="fas fa-check step-check"></i>
            </div>
          </div>
           <div class="step-label">
             <span v-if="step === 1">1. Emergency Status</span>
             <span v-else-if="step === 2">2. Action Plan</span>
             <span v-else-if="step === 3">3. Emergency Contacts</span>
           </div>
        </div>
      </div>
    </div>

    <!-- Step 1: Emergency Status -->
    <div v-if="currentStep === 1" class="step-content">
      <div class="step-header text-center mb-5">
        <h3 class="fw-bold mb-2 text-danger">Emergency Status Check</h3>
        <p class="text-muted lead">First, let's understand your current situation</p>
        <div v-if="!store || (!store.isExpecting && !store.hasBaby)" class="alert alert-warning mt-3">
          <i class="fas fa-user-circle me-2"></i>
          Please select your profile first to get personalized emergency guidance.
        </div>
      </div>
      
      <div class="row g-4">
        <div class="col-md-4" v-for="status in emergencyStatuses" :key="status.id">
          <div class="emergency-status-card">
            <button 
              @click="selectEmergencyStatus(status.id)"
              class="status-btn"
              :class="{ selected: emergencyStatus === status.id }"
              :style="{ borderColor: status.color }"
            >
              <i :class="status.icon" class="status-icon" :style="{ color: status.color }"></i>
              <h5 class="status-title">{{ status.title }}</h5>
              <p class="status-description">{{ status.description }}</p>
              <div class="priority-badge" :style="{ backgroundColor: status.color }">
                {{ status.priority.toUpperCase() }}
              </div>
            </button>
          </div>
        </div>
      </div>
    </div>

    <!-- Step 2: Emergency Actions -->
    <div v-if="currentStep === 2" class="step-content">
      <div class="step-header text-center mb-5">
        <h3 class="fw-bold mb-2 text-primary">Your Action Plan</h3>
        <p class="text-muted lead">Follow these steps in order of priority</p>
      </div>

      <div class="row g-4">
        <div class="col-lg-6" v-for="action in availableActions" :key="action.id">
          <div class="action-card">
            <div class="action-header">
              <div class="action-icon">
                <i :class="action.icon" :style="{ color: action.color }"></i>
              </div>
              <div class="action-priority" :style="{ backgroundColor: action.color }">
                {{ getPriorityLabel(action.priority) }}
              </div>
            </div>
            
            <div class="action-content">
              <h4 class="action-title">{{ action.title }}</h4>
              <p class="action-description">{{ action.description }}</p>
              <div class="action-reason">
                <strong>Why this matters:</strong> {{ action.reason }}
              </div>
              
              <div class="action-steps">
                <h6 class="fw-bold mb-3">Do this now:</h6>
                <ol class="steps-list">
                  <li v-for="(step, index) in action.steps" :key="index">
                    {{ step }}
                  </li>
                </ol>
              </div>
            </div>
          </div>
        </div>
      </div>
    </div>

    <!-- Step 3: Emergency Contacts & Resources -->
    <div v-if="currentStep === 3" class="step-content">
      <div class="step-header text-center mb-5">
        <h3 class="fw-bold mb-2 text-success">Emergency Contacts</h3>
        <p class="text-muted lead">Save these contacts for quick access</p>
      </div>

      <div class="row g-4">
        <div class="col-md-6 col-lg-3" v-for="contact in emergencyContacts" :key="contact.name">
          <div class="contact-card">
            <div class="contact-header">
              <div class="contact-priority" :style="{ backgroundColor: contact.color }">
                {{ getPriorityLabel(contact.priority) }}
              </div>
            </div>
            
            <div class="contact-content">
              <h5 class="contact-name">{{ contact.name }}</h5>
              <p class="contact-number">{{ contact.number }}</p>
              <p v-if="contact.description" class="contact-description">{{ contact.description }}</p>
              
              <MaterialButton 
                @click="callEmergency(contact.number)"
                :color="contact.priority === 'urgent' ? 'danger' : contact.priority === 'high' ? 'warning' : 'success'"
                :size="'lg'"
                class="w-100"
              >
                <i class="fas fa-phone me-2"></i>
                Call Now
              </MaterialButton>
            </div>
          </div>
        </div>
      </div>

      <!-- Quick Actions -->
      <div class="quick-actions mt-5">
        <div class="row g-3 justify-content-center">
          <div class="col-md-4">
            <MaterialButton 
              :color="'secondary'"
              :size="'lg'"
              @click="resetGuide"
              class="w-100"
            >
              <i class="fas fa-undo me-2"></i>
              Start Over
            </MaterialButton>
          </div>
        </div>
      </div>
    </div>

    <!-- Navigation Footer -->
    <div class="navigation-footer">
      <div class="container">
        <div class="footer-content">
          <div class="footer-actions">
            <MaterialButton 
              v-if="canGoBack"
              @click="prevStep"
              :color="'secondary'"
              :size="'lg'"
              class="me-3"
            >
              <i class="fas fa-arrow-left me-2"></i>
              Previous
            </MaterialButton>
            
            <MaterialButton 
              v-if="currentStep < 4"
              @click="nextStep"
              :color="'primary'"
              :size="'lg'"
              :disabled="!canProceed"
            >
              Next
              <i class="fas fa-arrow-right ms-2"></i>
            </MaterialButton>
          </div>
        </div>
      </div>
    </div>
  </div>
</template>

<style scoped>
.emergency-safety-guide {
  background: linear-gradient(135deg, #f8f9fa 0%, #e3f2fd 100%);
  min-height: 100vh;
  padding-bottom: 120px; /* Space for navigation footer */
}

/* Section Header */
.section-header h1 {
  color: #2c3e50;
  font-weight: 700;
}

/* Progress Indicator */
.progress-indicator {
  margin: 2rem 0;
}

.progress-line {
  position: absolute;
  top: 25px;
  left: 12.5%;
  right: 12.5%;
  height: 2px;
  background: #e9ecef;
  z-index: 1;
}

.progress-step.completed + .progress-step .progress-line,
.progress-step.active .progress-line {
  background: #007bff;
}

.progress-step.completed .progress-line {
  background: #28a745;
}

.progress-container {
  display: flex;
  justify-content: center;
  align-items: center;
  gap: 2rem;
  flex-wrap: wrap;
}

.progress-step {
  display: flex;
  flex-direction: column;
  align-items: center;
  gap: 0.5rem;
}

.step-circle {
  width: 40px;
  height: 40px;
  border-radius: 50%;
  background: #E5E7EB;
  color: #6B7280;
  display: flex;
  align-items: center;
  justify-content: center;
  font-weight: 700;
  font-size: 1rem;
  transition: all 0.3s ease;
  border: 2px solid #E5E7EB;
  position: relative;
}

.step-number {
  font-weight: 700;
  font-size: 1rem;
}

.step-completed {
  display: flex;
  flex-direction: column;
  align-items: center;
  justify-content: center;
  gap: 2px;
}

.step-number-small {
  font-weight: 600;
  font-size: 0.7rem;
  line-height: 1;
}

.step-check {
  font-size: 0.8rem;
  color: white;
  line-height: 1;
}

.progress-step.active .step-circle {
  background: #007bff;
  color: white;
  border-color: #007bff;
  box-shadow: 0 0 0 3px rgba(0, 123, 255, 0.2);
}

.progress-step.completed .step-circle {
  background: #28a745;
  color: white;
  border-color: #28a745;
}

.step-label {
  font-size: 0.875rem;
  font-weight: 500;
  color: #6B7280;
  text-align: center;
}

.progress-step.active .step-label {
  color: #1E293B;
  font-weight: 600;
}


/* Step Content */
.step-content {
  max-width: 1000px;
  margin: 0 auto;
}

.step-header h3 {
  color: #1E293B;
}

/* Emergency Status Cards */
.emergency-status-card {
  transition: all 0.3s ease;
}

.status-btn {
  width: 100%;
  background: white;
  border: 3px solid #E5E7EB;
  border-radius: 16px;
  padding: 2rem;
  text-align: center;
  transition: all 0.3s ease;
  box-shadow: 0 6px 18px rgba(2, 6, 23, 0.06);
  min-height: 200px;
  display: flex;
  flex-direction: column;
  align-items: center;
  justify-content: center;
}

.status-btn:hover {
  transform: translateY(-4px);
  box-shadow: 0 12px 24px rgba(2, 6, 23, 0.12);
}

.status-btn.selected {
  border-color: #1E293B;
  background: #F8FAFC;
  box-shadow: 0 0 0 3px rgba(30, 41, 59, 0.1);
}

.status-icon {
  font-size: 2.5rem;
  margin-bottom: 1rem;
}

.status-title {
  color: #1E293B;
  font-weight: 600;
  margin-bottom: 0.5rem;
  font-size: 1.2rem;
}

.status-description {
  color: #4B5563;
  font-size: 0.9rem;
  margin-bottom: 1rem;
}

.priority-badge {
  color: white;
  padding: 0.25rem 0.75rem;
  border-radius: 20px;
  font-weight: 600;
  font-size: 0.75rem;
}

/* Guidance Target Cards */
.guidance-target-card {
  transition: all 0.3s ease;
}

.target-btn {
  width: 100%;
  background: white;
  border: 3px solid #E5E7EB;
  border-radius: 16px;
  padding: 2rem;
  text-align: center;
  transition: all 0.3s ease;
  box-shadow: 0 6px 18px rgba(2, 6, 23, 0.06);
  min-height: 180px;
  display: flex;
  flex-direction: column;
  align-items: center;
  justify-content: center;
}

.target-btn:hover {
  transform: translateY(-4px);
  box-shadow: 0 12px 24px rgba(2, 6, 23, 0.12);
  border-color: #0EA5A3;
}

.target-btn.selected {
  border-color: #0EA5A3;
  background: #E6F7F6;
  box-shadow: 0 0 0 3px rgba(14, 165, 163, 0.1);
}

.target-icon {
  font-size: 2.5rem;
  color: #0EA5A3;
  margin-bottom: 1rem;
}

.target-title {
  color: #1E293B;
  font-weight: 600;
  margin-bottom: 0.5rem;
  font-size: 1.2rem;
}

.target-description {
  color: #4B5563;
  font-size: 0.9rem;
  margin: 0;
}

/* Action Cards */
.action-card {
  background: white;
  border-radius: 16px;
  padding: 1.5rem;
  box-shadow: 0 6px 18px rgba(2, 6, 23, 0.06);
  transition: all 0.3s ease;
  height: 100%;
}

.action-card:hover {
  transform: translateY(-2px);
  box-shadow: 0 12px 24px rgba(2, 6, 23, 0.12);
}

.action-header {
  display: flex;
  justify-content: space-between;
  align-items: center;
  margin-bottom: 1rem;
}

.action-icon {
  font-size: 2rem;
}

.action-priority {
  color: white;
  padding: 0.25rem 0.75rem;
  border-radius: 20px;
  font-weight: 600;
  font-size: 0.75rem;
}

.action-title {
  color: #1E293B;
  font-weight: 600;
  margin-bottom: 0.5rem;
  font-size: 1.1rem;
}

.action-description {
  color: #4B5563;
  font-size: 0.9rem;
  margin-bottom: 1rem;
}

.action-reason {
  background: #F8FAFC;
  padding: 0.75rem;
  border-radius: 8px;
  margin-bottom: 1rem;
  font-size: 0.9rem;
  color: #1E293B;
  border-left: 3px solid #0EA5A3;
}

.action-steps h6 {
  color: #1E293B;
  margin-bottom: 0.75rem;
}

.steps-list {
  margin: 0;
  padding-left: 1.5rem;
}

.steps-list li {
  color: #4B5563;
  font-size: 0.9rem;
  margin-bottom: 0.5rem;
  line-height: 1.5;
}

/* Contact Cards */
.contact-card {
  background: white;
  border-radius: 16px;
  padding: 1.5rem;
  box-shadow: 0 6px 18px rgba(2, 6, 23, 0.06);
  transition: all 0.3s ease;
  height: 100%;
  text-align: center;
}

.contact-card:hover {
  transform: translateY(-2px);
  box-shadow: 0 12px 24px rgba(2, 6, 23, 0.12);
}

.contact-header {
  display: flex;
  justify-content: space-between;
  align-items: center;
  margin-bottom: 1rem;
}


.contact-priority {
  color: white;
  padding: 0.25rem 0.5rem;
  border-radius: 12px;
  font-weight: 600;
  font-size: 0.7rem;
}

.contact-name {
  color: #1E293B;
  font-weight: 600;
  margin-bottom: 0.5rem;
  font-size: 1rem;
}

.contact-number {
  color: #4B5563;
  font-size: 0.9rem;
  margin-bottom: 0.5rem;
  font-weight: 500;
}

.contact-description {
  font-size: 0.8rem;
  color: #6B7280;
  margin-bottom: 1rem;
  font-style: italic;
}

/* Quick Actions */
.quick-actions {
  background: white;
  border-radius: 16px;
  padding: 2rem;
  box-shadow: 0 6px 18px rgba(2, 6, 23, 0.06);
}

/* Navigation Footer */
.navigation-footer {
  position: fixed;
  bottom: 0;
  left: 0;
  right: 0;
  background: white;
  border-top: 1px solid #E5E7EB;
  padding: 1rem 0;
  z-index: 100;
}

.footer-content {
  display: flex;
  justify-content: center;
  align-items: center;
}

.footer-actions {
  display: flex;
  align-items: center;
  gap: 1rem;
}

/* Responsive Design */
@media (max-width: 768px) {
  .progress-container {
    gap: 1rem;
  }
  
  .step-circle {
    width: 32px;
    height: 32px;
    font-size: 0.875rem;
  }
  
  .step-label {
    font-size: 0.75rem;
  }
  
  .status-btn,
  .target-btn {
    min-height: 160px;
    padding: 1.5rem;
  }
  
  .action-card {
    margin-bottom: 1rem;
  }
  
  .contact-card {
    margin-bottom: 1rem;
  }
  
  .footer-actions {
    flex-direction: column;
    gap: 0.5rem;
  }
}

@media (max-width: 576px) {
  .section-header h1 {
    font-size: 2rem;
  }
  
  .status-btn,
  .target-btn {
    min-height: 140px;
    padding: 1rem;
  }
  
  .action-card {
    padding: 1rem;
  }
  
  .contact-card {
    padding: 1rem;
  }
  
  .quick-actions {
    padding: 1rem;
  }
}
</style>