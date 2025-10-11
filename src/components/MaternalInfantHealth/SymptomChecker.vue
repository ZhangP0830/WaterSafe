<script setup>
import { ref, computed, onMounted } from "vue";
import { useMaternalInfantStore } from "@/stores/maternalInfantStore";

// Component state
const store = useMaternalInfantStore();
const currentStep = ref(1);
const selectedChips = ref([]);
const freeText = ref('');
const severity = ref('unknown');
const assessmentResult = ref(null);
const isLoading = ref(false);
const selectedCard = ref('');

// Common symptoms for chips
const commonSymptoms = {
  expecting: [
    'dizziness', 'nausea', 'headache', 'fatigue', 'back pain',
    'swelling', 'shortness of breath', 'chest pain', 'abdominal pain',
    'bleeding', 'contractions', 'fever', 'dehydration signs'
  ],
  baby: [
    'fever', 'crying', 'irritability', 'poor feeding', 'vomiting',
    'diarrhea', 'dehydration signs', 'difficulty breathing', 'rash',
    'lethargy', 'unusual sleep', 'temperature changes', 'feeding refusal'
  ]
};

// Computed properties
const canProceed = computed(() => {
  switch (currentStep.value) {
    case 1: return selectedChips.value.length > 0 || freeText.value.trim() !== '';
    case 2: return true;
    default: return true;
  }
});

const progressPercentage = computed(() => {
  return (currentStep.value / 2) * 100;
});

const currentSymptoms = computed(() => {
  if (!store) return [];
  return store.isExpecting ? commonSymptoms.expecting : commonSymptoms.baby;
});

// Step navigation methods
const initializeComponent = () => {
  currentStep.value = 1; // Start directly at symptom input
};

const toggleChip = (symptom) => {
  const index = selectedChips.value.indexOf(symptom);
  if (index > -1) {
    selectedChips.value.splice(index, 1);
  } else {
    selectedChips.value.push(symptom);
  }
};

const goBack = () => {
  if (currentStep.value > 1) {
    currentStep.value--;
    selectedCard.value = '';
  }
};

const startOver = () => {
  currentStep.value = 1;
  selectedChips.value = [];
  freeText.value = '';
  severity.value = 'unknown';
  assessmentResult.value = null;
  selectedCard.value = '';
};

const completeAssessment = async () => {
  isLoading.value = true;
  
  try {
    const response = await fetch('/api/symptoms/assess', {
      method: 'POST',
      headers: {
        'Content-Type': 'application/json',
      },
      body: JSON.stringify({
        subject: store && store.isExpecting ? 'expecting' : 'baby',
        chips: selectedChips.value,
        freeText: freeText.value,
        severityHints: severity.value,
        context: {
          mode: 'general',
          place: 'home'
        }
      })
    });

    if (!response.ok) {
      const errorText = await response.text();
      console.error('API Error:', response.status, errorText);
      throw new Error(`Assessment failed: ${response.status}`);
    }

    const result = await response.json();
    assessmentResult.value = result;
    currentStep.value = 2;
    
    // Auto-scroll to results after a short delay
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
  } catch (error) {
    console.error('Assessment error:', error);
    // Fallback safe result with enhanced details
    assessmentResult.value = {
      classification: 'seek_care',
      reason: 'We want to make sure you get the right care. Based on your symptoms, it\'s best to connect with a healthcare professional who can provide personalized guidance.',
      steps: [
        'Call your GP or healthcare provider within 24 hours',
        'If you have a regular obstetrician or pediatrician, contact them directly',
        'Keep a symptom diary to share with your healthcare provider',
        'Stay hydrated and rest as much as possible',
        'If symptoms worsen or you feel concerned, don\'t wait - seek care immediately'
      ],
      watch_for: [
        'Severe or worsening pain',
        'High fever (over 38°C)',
        'Difficulty breathing or shortness of breath',
        'Signs of dehydration (dry mouth, dizziness, reduced urination)',
        'Any new or concerning symptoms'
      ],
      timeline: 'Contact healthcare provider within 24 hours',
      severity: 'moderate',
      follow_up: [
        'How long have you been experiencing these symptoms?',
        'Have you tried any home remedies?',
        'Are you taking any medications?',
        'Have you been exposed to any potential contaminants?'
      ],
      references: [
        { label: 'Healthdirect Australia', url: 'https://www.healthdirect.gov.au/', description: 'Free health advice and information' },
        { label: 'Victorian Department of Health', url: 'https://www.health.vic.gov.au/', description: 'Local health resources and contacts' }
      ],
      disclaimer: 'This assessment is for guidance only and should not replace professional medical advice. Always consult with a healthcare provider for proper diagnosis and treatment.'
    };
    currentStep.value = 2;
    
    // Auto-scroll to results after a short delay
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
  } finally {
    isLoading.value = false;
  }
};

// Initialize component
onMounted(() => {
  initializeComponent();
});

const refineAssessment = async () => {
  if (freeText.value.trim() === '') return;
  
  // Add new symptoms to existing ones
  const newSymptoms = freeText.value.split(',').map(s => s.trim()).filter(s => s);
  selectedChips.value = [...new Set([...selectedChips.value, ...newSymptoms])];
  
  // Re-run assessment
  await completeAssessment();
};

const openReference = (url) => {
  window.open(url, '_blank', 'noopener,noreferrer');
};
</script>

<template>
  <div class="symptom-checker-container">
    <!-- Progress Stepper -->
    <div class="progress-stepper">
      <div class="progress-bar" :style="{ width: progressPercentage + '%' }"></div>
      <div class="stepper-steps">
        <div class="step" :class="{ active: currentStep >= 1, completed: currentStep > 1 }">
          <span class="step-number">1</span>
          <span class="step-label">Symptoms</span>
        </div>
        <div class="step" :class="{ active: currentStep >= 2 }">
          <span class="step-number">2</span>
          <span class="step-label">Your Health Summary</span>
        </div>
      </div>
    </div>

    <!-- Step 1: Symptom Input -->
    <div v-if="currentStep === 1" class="step-container">
      <div class="step-header">
        <h2 class="step-title">Let's check your symptoms</h2>
        <p class="step-subtitle">Tell us what you're experiencing so we can provide personalized guidance</p>
        <div v-if="!store || (!store.isExpecting && !store.hasBaby)" class="alert alert-info">
          <i class="fas fa-info-circle me-2"></i>
          Please select your profile first to get personalized guidance.
        </div>
      </div>

      <div class="symptoms-section">
        <!-- Symptom Chips -->
        <div class="symptoms-chips">
          <h3 class="section-title">Common symptoms</h3>
          <div class="chips-container">
            <button
              v-for="symptom in currentSymptoms"
              :key="symptom"
              class="symptom-chip"
              :class="{ selected: selectedChips.includes(symptom) }"
              @click="toggleChip(symptom)"
            >
              {{ symptom }}
            </button>
          </div>
        </div>

        <!-- Free Text Input -->
        <div class="free-text-section">
          <h3 class="section-title">Additional symptoms</h3>
          <div class="input-group">
            <textarea
              v-model="freeText"
              class="symptom-textarea"
              placeholder="Type any other symptoms you're experiencing..."
              rows="3"
            ></textarea>
          </div>
        </div>

        <!-- Severity Picker -->
        <div class="severity-section">
          <h3 class="section-title">How severe are the symptoms?</h3>
          <div class="severity-options">
            <label class="severity-option">
              <input
                type="radio"
                v-model="severity"
                value="mild"
                class="severity-radio"
              >
              <span class="severity-label">Mild</span>
            </label>
            <label class="severity-option">
              <input
                type="radio"
                v-model="severity"
                value="moderate"
                class="severity-radio"
              >
              <span class="severity-label">Moderate</span>
            </label>
            <label class="severity-option">
              <input
                type="radio"
                v-model="severity"
                value="severe"
                class="severity-radio"
              >
              <span class="severity-label">Severe</span>
            </label>
            <label class="severity-option">
              <input
                type="radio"
                v-model="severity"
                value="unknown"
                class="severity-radio"
              >
              <span class="severity-label">Not sure</span>
            </label>
          </div>
        </div>

        <!-- Action Buttons -->
        <div class="action-buttons">
          <button 
            @click="completeAssessment" 
            class="btn-primary"
            :disabled="!canProceed || isLoading"
          >
            <span v-if="isLoading">Assessing...</span>
            <span v-else>Complete Assessment</span>
          </button>
        </div>
      </div>
    </div>

    <!-- Step 2: Results -->
    <div v-if="currentStep === 2" class="step-container">
      <div class="step-header">
        <button class="back-btn" @click="goBack">
          <i class="fas fa-arrow-left"></i> Back
        </button>
        <h2 class="step-title">Your Health Summary</h2>
        <p class="step-subtitle">Here's what this means for you and your next steps</p>
      </div>

      <div v-if="assessmentResult" class="results-section">
        <!-- Classification Banner -->
        <div 
          class="classification-banner"
          :class="{
            'self-care': assessmentResult.classification === 'self_care',
            'seek-care': assessmentResult.classification === 'seek_care',
            'urgent': assessmentResult.classification === 'urgent'
          }"
        >
          <div class="banner-icon">
            <i v-if="assessmentResult.classification === 'self_care'" class="fas fa-check-circle"></i>
            <i v-else class="fas fa-exclamation-triangle"></i>
          </div>
          <div class="banner-content">
            <h3 class="banner-title">
              <span v-if="assessmentResult.classification === 'self_care'">Self-Care</span>
              <span v-else-if="assessmentResult.classification === 'seek_care'">Seek Medical Care</span>
              <span v-else>Seek Immediate Care</span>
            </h3>
            <p class="banner-reason">{{ assessmentResult.reason }}</p>
          </div>
        </div>

        <!-- Timeline & Severity -->
        <div v-if="assessmentResult.timeline || assessmentResult.severity" class="timeline-severity">
          <div v-if="assessmentResult.timeline" class="timeline-info">
            <i class="fas fa-clock me-2"></i>
            <strong>Timeline:</strong> {{ assessmentResult.timeline }}
          </div>
          <div v-if="assessmentResult.severity" class="severity-info">
            <i class="fas fa-thermometer-half me-2"></i>
            <strong>Severity:</strong> 
            <span :class="'severity-' + assessmentResult.severity">{{ assessmentResult.severity }}</span>
          </div>
        </div>

        <!-- Next Steps -->
        <div class="next-steps">
          <h3 class="section-title">Your Action Plan</h3>
          <ul class="steps-list">
            <li v-for="(step, index) in assessmentResult.steps" :key="index" class="step-item">
              <i class="fas fa-arrow-right me-2"></i>{{ step }}
            </li>
          </ul>
        </div>

        <!-- Watch For -->
        <div v-if="assessmentResult.watch_for && assessmentResult.watch_for.length > 0" class="watch-for">
          <h3 class="section-title">Important Things to Watch For</h3>
          <ul class="watch-list">
            <li v-for="(item, index) in assessmentResult.watch_for" :key="index" class="watch-item">
              <i class="fas fa-eye me-2"></i>{{ item }}
            </li>
          </ul>
        </div>

        <!-- Follow-up Questions -->
        <div v-if="assessmentResult.follow_up && assessmentResult.follow_up.length > 0" class="follow-up">
          <h3 class="section-title">Questions to Consider</h3>
          <p class="follow-up-intro">These questions can help you provide more details to your healthcare provider:</p>
          <ul class="follow-up-list">
            <li v-for="(question, index) in assessmentResult.follow_up" :key="index" class="follow-up-item">
              <i class="fas fa-question-circle me-2"></i>{{ question }}
            </li>
          </ul>
        </div>

        <!-- References -->
        <div v-if="assessmentResult.references && assessmentResult.references.length > 0" class="references">
          <h3 class="section-title">Helpful Resources</h3>
          <div class="reference-cards">
            <div
              v-for="ref in assessmentResult.references"
              :key="ref.label"
              class="reference-card"
              @click="openReference(ref.url)"
            >
              <div class="reference-content">
                <h4 class="reference-title">{{ ref.label }}</h4>
                <p v-if="ref.description" class="reference-description">{{ ref.description }}</p>
                <i class="fas fa-external-link-alt reference-icon"></i>
              </div>
            </div>
          </div>
        </div>

        <!-- Disclaimer -->
        <div class="disclaimer">
          <p>{{ assessmentResult.disclaimer }}</p>
        </div>

        <!-- Refine Assessment -->
        <div class="refine-section">
          <h3 class="section-title">Need to add more symptoms?</h3>
          <div class="refine-input">
            <input
              v-model="freeText"
              type="text"
              placeholder="Type another symptom..."
              class="refine-text-input"
            >
            <button @click="refineAssessment" class="btn-secondary">
              Refine Assessment
            </button>
          </div>
        </div>

        <!-- Action Buttons -->
        <div class="action-buttons">
          <button @click="startOver" class="btn-outline">
            Start Over
          </button>
        </div>
      </div>
    </div>
  </div>
</template>

<style scoped>
/* Container */
.symptom-checker-container {
  min-height: 100vh;
  background: linear-gradient(135deg, #f8f9fa 0%, #e3f2fd 100%);
  padding: 2rem 1rem;
}

/* Progress Stepper */
.progress-stepper {
  max-width: 600px;
  margin: 0 auto 3rem;
  position: relative;
}

.progress-bar {
  height: 4px;
  background: linear-gradient(90deg, #007bff, #0056b3);
  border-radius: 2px;
  transition: width 0.3s ease;
}

.stepper-steps {
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
  background: #E5E7EB;
  color: #6B7280;
  display: flex;
  align-items: center;
  justify-content: center;
  font-weight: 700;
  transition: all 0.3s ease;
}

.step.active .step-number {
  background: linear-gradient(135deg, #007bff 0%, #0056b3 100%);
  color: white;
}

.step.completed .step-number {
  background: linear-gradient(135deg, #28a745 0%, #20c997 100%);
  color: white;
}

.step-label {
  font-size: 0.9rem;
  font-weight: 600;
  color: #6B7280;
}

.step.active .step-label {
  color: #007bff;
}

/* Step Container */
.step-container {
  max-width: 800px;
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
  background: white;
  border: 2px solid #0EA5A3;
  border-radius: 12px;
  padding: 0.75rem 1.5rem;
  color: #1F2A37;
  font-weight: 600;
  transition: all 0.3s ease;
  cursor: pointer;
}

.back-btn:hover {
  background: #0EA5A3;
  color: white;
  transform: translateX(-3px);
}

.step-title {
  font-size: 2.5rem;
  font-weight: 700;
  color: #1F2A37;
  margin-bottom: 1rem;
}

.step-subtitle {
  font-size: 1.2rem;
  color: #4B5563;
  margin-bottom: 0;
}

/* Subject Cards */
.subject-cards {
  display: grid;
  grid-template-columns: repeat(auto-fit, minmax(300px, 1fr));
  gap: 2rem;
  margin-bottom: 2rem;
}

.subject-card {
  background: white;
  border-radius: 16px;
  padding: 2rem;
  text-align: center;
  cursor: pointer;
  transition: all 0.3s ease;
  border: 3px solid transparent;
  box-shadow: 0 6px 18px rgba(2, 6, 23, 0.06);
}

.subject-card:hover {
  transform: translateY(-2px);
  box-shadow: 0 8px 25px rgba(2, 6, 23, 0.1);
}

.subject-card.selected {
  border-color: #0EA5A3;
  transform: translateY(-2px);
  box-shadow: 0 8px 25px rgba(14, 165, 163, 0.2);
}

.card-icon {
  font-size: 3rem;
  margin-bottom: 1rem;
}

.card-title {
  font-size: 1.5rem;
  font-weight: 700;
  color: #1F2A37;
  margin-bottom: 0.5rem;
}

.card-subtitle {
  color: #4B5563;
  margin-bottom: 0;
}

/* Symptoms Section */
.symptoms-section {
  display: flex;
  flex-direction: column;
  gap: 2rem;
}

.section-title {
  font-size: 1.2rem;
  font-weight: 700;
  color: #1F2A37;
  margin-bottom: 1rem;
}

/* Symptom Chips */
.symptoms-chips {
  background: white;
  border-radius: 16px;
  padding: 2rem;
  box-shadow: 0 6px 18px rgba(2, 6, 23, 0.06);
}

.chips-container {
  display: flex;
  flex-wrap: wrap;
  gap: 0.75rem;
}

.symptom-chip {
  background: #F3F4F6;
  border: 2px solid #E5E7EB;
  border-radius: 20px;
  padding: 0.5rem 1rem;
  color: #4B5563;
  font-weight: 600;
  cursor: pointer;
  transition: all 0.3s ease;
}

.symptom-chip:hover {
  background: #E5E7EB;
  border-color: #0EA5A3;
}

.symptom-chip.selected {
  background: #0EA5A3;
  border-color: #0EA5A3;
  color: white;
}

/* Free Text Section */
.free-text-section {
  background: white;
  border-radius: 16px;
  padding: 2rem;
  box-shadow: 0 6px 18px rgba(2, 6, 23, 0.06);
}

.symptom-textarea {
  width: 100%;
  border: 2px solid #E5E7EB;
  border-radius: 12px;
  padding: 1rem;
  font-size: 1rem;
  color: #1F2A37;
  resize: vertical;
  transition: border-color 0.3s ease;
}

.symptom-textarea:focus {
  outline: none;
  border-color: #0EA5A3;
}

/* Severity Section */
.severity-section {
  background: white;
  border-radius: 16px;
  padding: 2rem;
  box-shadow: 0 6px 18px rgba(2, 6, 23, 0.06);
}

.severity-options {
  display: flex;
  gap: 1rem;
  flex-wrap: wrap;
}

.severity-option {
  display: flex;
  align-items: center;
  gap: 0.5rem;
  cursor: pointer;
}

.severity-radio {
  width: 18px;
  height: 18px;
  accent-color: #0EA5A3;
}

.severity-label {
  color: #4B5563;
  font-weight: 600;
}

/* Results Section */
.results-section {
  display: flex;
  flex-direction: column;
  gap: 2rem;
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

/* Classification Banner */
.classification-banner {
  display: flex;
  align-items: center;
  gap: 1rem;
  padding: 1.5rem;
  border-radius: 16px;
  border-left: 6px solid;
  background: white;
  box-shadow: 0 6px 18px rgba(2, 6, 23, 0.06);
}

.classification-banner.self-care {
  border-left-color: #10B981;
}

.classification-banner.seek-care {
  border-left-color: #F59E0B;
}

.classification-banner.urgent {
  border-left-color: #DC2626;
}

.banner-icon {
  font-size: 2rem;
}

.self-care .banner-icon {
  color: #10B981;
}

.seek-care .banner-icon {
  color: #F59E0B;
}

.urgent .banner-icon {
  color: #DC2626;
}

.banner-title {
  font-size: 1.5rem;
  font-weight: 700;
  color: #1F2A37;
  margin-bottom: 0.5rem;
}

.banner-reason {
  color: #4B5563;
  margin: 0;
}

/* Next Steps */
.next-steps {
  background: white;
  border-radius: 16px;
  padding: 2rem;
  box-shadow: 0 6px 18px rgba(2, 6, 23, 0.06);
}

.steps-list {
  list-style: none;
  padding: 0;
  margin: 0;
}

.step-item {
  padding: 0.75rem 0;
  border-bottom: 1px solid #F3F4F6;
  color: #4B5563;
  position: relative;
  padding-left: 1.5rem;
}

.step-item:last-child {
  border-bottom: none;
}

.step-item::before {
  content: '•';
  color: #0EA5A3;
  font-weight: bold;
  position: absolute;
  left: 0;
}

/* Watch For */
.watch-for {
  background: white;
  border-radius: 16px;
  padding: 2rem;
  box-shadow: 0 6px 18px rgba(2, 6, 23, 0.06);
}

.watch-list {
  list-style: none;
  padding: 0;
  margin: 0;
}

.watch-item {
  padding: 0.75rem 0;
  border-bottom: 1px solid #F3F4F6;
  color: #4B5563;
  position: relative;
  padding-left: 1.5rem;
}

.watch-item:last-child {
  border-bottom: none;
}

.watch-item::before {
  content: '⚠';
  color: #F59E0B;
  position: absolute;
  left: 0;
}

/* References */
.references {
  background: white;
  border-radius: 16px;
  padding: 2rem;
  box-shadow: 0 6px 18px rgba(2, 6, 23, 0.06);
}

.reference-chips {
  display: flex;
  flex-wrap: wrap;
  gap: 0.75rem;
}

.reference-chip {
  background: #F0FDFA;
  border: 2px solid #0EA5A3;
  border-radius: 20px;
  padding: 0.5rem 1rem;
  color: #0EA5A3;
  font-weight: 600;
  cursor: pointer;
  transition: all 0.3s ease;
  text-decoration: none;
}

.reference-chip:hover {
  background: #0EA5A3;
  color: white;
  text-decoration: none;
}

/* Disclaimer */
.disclaimer {
  background: #FEF3C7;
  border: 1px solid #F59E0B;
  border-radius: 12px;
  padding: 1rem;
  text-align: center;
}

.disclaimer p {
  color: #92400E;
  margin: 0;
  font-size: 0.9rem;
}

/* Refine Section */
.refine-section {
  background: white;
  border-radius: 16px;
  padding: 2rem;
  box-shadow: 0 6px 18px rgba(2, 6, 23, 0.06);
}

.refine-input {
  display: flex;
  gap: 1rem;
  align-items: center;
}

.refine-text-input {
  flex: 1;
  border: 2px solid #E5E7EB;
  border-radius: 12px;
  padding: 0.75rem 1rem;
  font-size: 1rem;
  color: #1F2A37;
  transition: border-color 0.3s ease;
}

.refine-text-input:focus {
  outline: none;
  border-color: #0EA5A3;
}

/* Action Buttons */
.action-buttons {
  text-align: center;
  margin-top: 2rem;
}

.btn-primary {
  background: #0EA5A3;
  border: none;
  border-radius: 12px;
  padding: 1rem 2rem;
  color: white;
  font-size: 1.1rem;
  font-weight: 700;
  cursor: pointer;
  transition: all 0.3s ease;
}

.btn-primary:hover:not(:disabled) {
  background: #0D9488;
  transform: translateY(-2px);
}

.btn-primary:disabled {
  background: #9CA3AF;
  cursor: not-allowed;
}

.btn-secondary {
  background: #F3F4F6;
  border: 2px solid #0EA5A3;
  border-radius: 12px;
  padding: 0.75rem 1.5rem;
  color: #0EA5A3;
  font-weight: 600;
  cursor: pointer;
  transition: all 0.3s ease;
}

.btn-secondary:hover {
  background: #0EA5A3;
  color: white;
}

.btn-outline {
  background: transparent;
  border: 2px solid #0EA5A3;
  border-radius: 12px;
  padding: 1rem 2rem;
  color: #0EA5A3;
  font-size: 1.1rem;
  font-weight: 700;
  cursor: pointer;
  transition: all 0.3s ease;
}

.btn-outline:hover {
  background: #0EA5A3;
  color: white;
}

/* Responsive Design */
@media (max-width: 768px) {
  .symptom-checker-container {
    padding: 1rem 0.5rem;
  }
  
  .step-title {
    font-size: 2rem;
  }
  
  .subject-cards {
    grid-template-columns: 1fr;
    gap: 1rem;
  }
  
  .subject-card {
    padding: 1.5rem;
  }
  
  .chips-container {
    gap: 0.5rem;
  }
  
  .symptom-chip {
    padding: 0.4rem 0.8rem;
    font-size: 0.9rem;
  }
  
  .severity-options {
    flex-direction: column;
    gap: 0.75rem;
  }
  
  .refine-input {
    flex-direction: column;
    align-items: stretch;
  }
  
  .back-btn {
    position: relative;
    margin-bottom: 1rem;
  }
  
  .classification-banner {
    flex-direction: column;
    text-align: center;
    gap: 0.75rem;
  }
}

/* Timeline & Severity */
.timeline-severity {
  display: flex;
  gap: 2rem;
  margin-bottom: 2rem;
  flex-wrap: wrap;
}

.timeline-info, .severity-info {
  background: white;
  padding: 1rem 1.5rem;
  border-radius: 12px;
  box-shadow: 0 2px 8px rgba(0,0,0,0.1);
  border-left: 4px solid #007bff;
}

.severity-mild { color: #28a745; }
.severity-moderate { color: #ffc107; }
.severity-severe { color: #dc3545; }

/* Follow-up Questions */
.follow-up {
  margin-top: 2rem;
}

.follow-up-intro {
  color: #6c757d;
  margin-bottom: 1rem;
  font-style: italic;
}

.follow-up-list {
  list-style: none;
  padding: 0;
}

.follow-up-item {
  background: #f8f9fa;
  padding: 1rem;
  margin-bottom: 0.5rem;
  border-radius: 8px;
  border-left: 3px solid #007bff;
  color: #495057;
}

/* Enhanced References */
.reference-cards {
  display: grid;
  grid-template-columns: repeat(auto-fit, minmax(300px, 1fr));
  gap: 1rem;
}

.reference-card {
  background: white;
  border: 2px solid #e9ecef;
  border-radius: 12px;
  padding: 1.5rem;
  cursor: pointer;
  transition: all 0.3s ease;
  position: relative;
}

.reference-card:hover {
  border-color: #007bff;
  transform: translateY(-2px);
  box-shadow: 0 4px 15px rgba(0, 123, 255, 0.2);
}

.reference-content {
  position: relative;
}

.reference-title {
  color: #2c3e50;
  font-weight: 700;
  margin-bottom: 0.5rem;
  font-size: 1.1rem;
}

.reference-description {
  color: #6c757d;
  margin-bottom: 0;
  font-size: 0.9rem;
}

.reference-icon {
  position: absolute;
  top: 0;
  right: 0;
  color: #007bff;
  font-size: 1.2rem;
}
</style>