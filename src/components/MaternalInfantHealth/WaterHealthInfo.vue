<script setup>
import { ref, computed, onMounted } from "vue";
import MaterialButton from "@/components/MaterialButton.vue";
import { useMaternalInfantStore } from "@/stores/maternalInfantStore";

const store = useMaternalInfantStore();
const selectedCategory = ref('');
const selectedCondition = ref(null);
const currentStep = ref(1);

// Water contamination health conditions
const healthConditions = {
  'water-borne': [
    {
      id: 'cholera',
      name: 'Cholera',
      description: 'Severe diarrheal disease caused by contaminated water',
      causes: [
        'Drinking water contaminated with Vibrio cholerae bacteria',
        'Poor sanitation and hygiene practices',
        'Consuming food prepared with contaminated water',
        'Contact with infected person\'s feces'
      ],
      symptoms: [
        'Severe watery diarrhea (rice-water stools)',
        'Vomiting and nausea',
        'Rapid dehydration',
        'Muscle cramps and weakness',
        'Low blood pressure and rapid heart rate'
      ],
      remedies: [
        'Immediate rehydration with oral rehydration solution (ORS)',
        'Seek medical attention immediately',
        'Use only safe, treated water for drinking',
        'Practice proper hand hygiene',
        'Avoid raw or undercooked food'
      ],
      prevention: [
        'Drink only boiled or treated water',
        'Wash hands frequently with soap',
        'Use proper sanitation facilities',
        'Cook food thoroughly',
        'Avoid street food during outbreaks'
      ],
      severity: 'high',
      icon: 'fas fa-tint',
      color: '#dc3545',
      references: [
        { label: 'WHO Cholera Fact Sheet', url: 'https://www.who.int/news-room/fact-sheets/detail/cholera', description: 'World Health Organization cholera information' },
        { label: 'Victorian Department of Health', url: 'https://www.health.vic.gov.au/infectious-diseases/cholera', description: 'Victorian cholera guidelines' }
      ]
    },
    {
      id: 'typhoid',
      name: 'Typhoid Fever',
      description: 'Bacterial infection spread through contaminated food and water',
      causes: [
        'Consuming water contaminated with Salmonella typhi',
        'Eating food prepared with contaminated water',
        'Poor personal hygiene',
        'Contact with infected person'
      ],
      symptoms: [
        'High fever (up to 104°F)',
        'Headache and body aches',
        'Loss of appetite and weight loss',
        'Diarrhea or constipation',
        'Rose-colored spots on chest and abdomen'
      ],
      remedies: [
        'Antibiotic treatment as prescribed by doctor',
        'Rest and adequate fluid intake',
        'Use only safe, treated water',
        'Maintain good hygiene practices',
        'Complete the full course of antibiotics'
      ],
      prevention: [
        'Drink only boiled or treated water',
        'Wash hands before eating and after using toilet',
        'Avoid raw vegetables and fruits',
        'Cook food thoroughly',
        'Get vaccinated if traveling to high-risk areas'
      ],
      severity: 'high',
      icon: 'fas fa-thermometer-full',
      color: '#fd7e14',
      references: [
        { label: 'Healthdirect Australia', url: 'https://www.healthdirect.gov.au/typhoid-fever', description: 'Australian typhoid fever information' },
        { label: 'CDC Typhoid Fever', url: 'https://www.cdc.gov/typhoid-fever/index.html', description: 'Centers for Disease Control typhoid information' }
      ]
    },
    {
      id: 'hepatitis-a',
      name: 'Hepatitis A',
      description: 'Viral infection affecting the liver, spread through contaminated food and water',
      causes: [
        'Drinking water contaminated with Hepatitis A virus',
        'Eating food prepared with contaminated water',
        'Poor sanitation and hygiene',
        'Contact with infected person'
      ],
      symptoms: [
        'Fatigue and weakness',
        'Nausea and vomiting',
        'Abdominal pain and discomfort',
        'Dark urine and pale stools',
        'Jaundice (yellowing of skin and eyes)'
      ],
      remedies: [
        'Rest and adequate nutrition',
        'Avoid alcohol and certain medications',
        'Stay hydrated with safe water',
        'Seek medical monitoring',
        'Practice good hygiene to prevent spread'
      ],
      prevention: [
        'Get vaccinated against Hepatitis A',
        'Drink only safe, treated water',
        'Wash hands frequently with soap',
        'Cook food thoroughly',
        'Avoid raw shellfish from contaminated waters'
      ],
      severity: 'medium',
      icon: 'fas fa-liver',
      color: '#6f42c1',
      references: [
        { label: 'Healthdirect Australia', url: 'https://www.healthdirect.gov.au/hepatitis-a', description: 'Australian Hepatitis A information' },
        { label: 'Victorian Department of Health', url: 'https://www.health.vic.gov.au/infectious-diseases/hepatitis-a', description: 'Victorian Hepatitis A guidelines' }
      ]
    }
  ],
  'parasitic': [
    {
      id: 'giardia',
      name: 'Giardiasis',
      description: 'Parasitic infection causing diarrhea and stomach problems',
      causes: [
        'Drinking water contaminated with Giardia parasites',
        'Swimming in contaminated water',
        'Poor sanitation and hygiene',
        'Contact with infected person or animal'
      ],
      symptoms: [
        'Watery, foul-smelling diarrhea',
        'Stomach cramps and bloating',
        'Nausea and vomiting',
        'Fatigue and weakness',
        'Weight loss and dehydration'
      ],
      remedies: [
        'Antiparasitic medication as prescribed',
        'Stay well hydrated',
        'Eat bland, easy-to-digest foods',
        'Rest and avoid strenuous activities',
        'Practice good hygiene to prevent spread'
      ],
      prevention: [
        'Drink only treated or boiled water',
        'Avoid swimming in potentially contaminated water',
        'Wash hands frequently with soap',
        'Use proper sanitation facilities',
        'Filter water when camping or traveling'
      ],
      severity: 'medium',
      icon: 'fas fa-bug',
      color: '#20c997',
      references: [
        { label: 'Healthdirect Australia', url: 'https://www.healthdirect.gov.au/giardiasis', description: 'Australian giardiasis information' },
        { label: 'CDC Giardiasis', url: 'https://www.cdc.gov/parasites/giardia/index.html', description: 'CDC giardiasis information' }
      ]
    },
    {
      id: 'cryptosporidium',
      name: 'Cryptosporidiosis',
      description: 'Parasitic infection causing severe diarrhea, especially dangerous for infants',
      causes: [
        'Drinking water contaminated with Cryptosporidium',
        'Swimming in contaminated pools or water',
        'Contact with infected animals',
        'Poor sanitation practices'
      ],
      symptoms: [
        'Watery diarrhea lasting 1-2 weeks',
        'Stomach cramps and pain',
        'Nausea and vomiting',
        'Fever and headache',
        'Dehydration (especially dangerous for babies)'
      ],
      remedies: [
        'Stay hydrated with oral rehydration solution',
        'Rest and eat bland foods',
        'Seek medical attention for infants immediately',
        'Use antiparasitic medication if prescribed',
        'Practice strict hygiene to prevent spread'
      ],
      prevention: [
        'Use only treated or boiled water',
        'Avoid swimming in potentially contaminated water',
        'Wash hands frequently with soap',
        'Use proper sanitation facilities',
        'Be extra careful with infant formula preparation'
      ],
      severity: 'high',
      icon: 'fas fa-baby',
      color: '#e83e8c',
      references: [
        { label: 'Healthdirect Australia', url: 'https://www.healthdirect.gov.au/cryptosporidiosis', description: 'Australian cryptosporidiosis information' },
        { label: 'Victorian Department of Health', url: 'https://www.health.vic.gov.au/infectious-diseases/cryptosporidiosis', description: 'Victorian cryptosporidiosis guidelines' }
      ]
    },
    {
      id: 'amoebic-dysentery',
      name: 'Amoebic Dysentery',
      description: 'Parasitic infection causing bloody diarrhea and intestinal inflammation',
      causes: [
        'Drinking water contaminated with Entamoeba histolytica',
        'Poor sanitation and hygiene practices',
        'Consuming contaminated food',
        'Contact with infected person\'s feces'
      ],
      symptoms: [
        'Bloody or mucus-filled diarrhea',
        'Severe stomach cramps',
        'Fever and chills',
        'Nausea and vomiting',
        'Fatigue and weight loss'
      ],
      remedies: [
        'Antiparasitic medication as prescribed',
        'Stay hydrated with oral rehydration solution',
        'Rest and eat bland foods',
        'Seek medical attention immediately',
        'Practice strict hygiene to prevent spread'
      ],
      prevention: [
        'Drink only safe, treated water',
        'Wash hands frequently with soap',
        'Use proper sanitation facilities',
        'Cook food thoroughly',
        'Avoid raw vegetables in high-risk areas'
      ],
      severity: 'high',
      icon: 'fas fa-bacteria',
      color: '#dc3545',
      references: [
        { label: 'Healthdirect Australia', url: 'https://www.healthdirect.gov.au/amoebic-dysentery', description: 'Australian amoebic dysentery information' },
        { label: 'WHO Amoebiasis', url: 'https://www.who.int/news-room/fact-sheets/detail/amoebiasis', description: 'WHO amoebiasis information' }
      ]
    }
  ],
  'sanitation-related': [
    {
      id: 'shigellosis',
      name: 'Shigellosis (Bacillary Dysentery)',
      description: 'Bacterial infection causing severe diarrhea and intestinal inflammation',
      causes: [
        'Poor sanitation and hygiene practices',
        'Contaminated water and food',
        'Crowded living conditions',
        'Lack of proper waste disposal',
        'Contact with infected person'
      ],
      symptoms: [
        'Bloody or mucus-filled diarrhea',
        'Severe stomach cramps',
        'Fever and chills',
        'Nausea and vomiting',
        'Dehydration and weakness'
      ],
      remedies: [
        'Antibiotic treatment as prescribed',
        'Stay hydrated with oral rehydration solution',
        'Rest and eat bland foods',
        'Seek medical attention immediately',
        'Practice strict hygiene to prevent spread'
      ],
      prevention: [
        'Use proper sanitation facilities',
        'Drink only safe, treated water',
        'Wash hands frequently with soap',
        'Cook food thoroughly',
        'Improve living conditions and waste disposal'
      ],
      severity: 'high',
      icon: 'fas fa-toilet',
      color: '#dc3545',
      references: [
        { label: 'Healthdirect Australia', url: 'https://www.healthdirect.gov.au/shigellosis', description: 'Australian shigellosis information' },
        { label: 'Victorian Department of Health', url: 'https://www.health.vic.gov.au/infectious-diseases/shigellosis', description: 'Victorian shigellosis guidelines' }
      ]
    },
    {
      id: 'campylobacter',
      name: 'Campylobacter Infection',
      description: 'Bacterial infection causing diarrhea, often from contaminated water',
      causes: [
        'Drinking water contaminated with Campylobacter bacteria',
        'Poor sanitation and hygiene',
        'Consuming contaminated food',
        'Contact with infected animals'
      ],
      symptoms: [
        'Watery or bloody diarrhea',
        'Stomach cramps and pain',
        'Fever and headache',
        'Nausea and vomiting',
        'Dehydration and weakness'
      ],
      remedies: [
        'Stay hydrated with clear fluids',
        'Rest and eat bland foods',
        'Use oral rehydration solution if needed',
        'Seek medical attention if symptoms worsen',
        'Practice good hygiene to prevent spread'
      ],
      prevention: [
        'Drink only safe, treated water',
        'Wash hands frequently with soap',
        'Cook food thoroughly',
        'Use proper sanitation facilities',
        'Avoid contact with potentially contaminated animals'
      ],
      severity: 'medium',
      icon: 'fas fa-virus',
      color: '#ffc107',
      references: [
        { label: 'Healthdirect Australia', url: 'https://www.healthdirect.gov.au/campylobacter-infection', description: 'Australian campylobacter information' },
        { label: 'CDC Campylobacter', url: 'https://www.cdc.gov/campylobacter/index.html', description: 'CDC campylobacter information' }
      ]
    },
    {
      id: 'leptospirosis',
      name: 'Leptospirosis (Weil\'s Disease)',
      description: 'Bacterial infection spread through contaminated water and soil',
      causes: [
        'Contact with water contaminated with animal urine',
        'Poor sanitation and drainage',
        'Flooding and standing water',
        'Contact with infected animals',
        'Poor waste disposal practices'
      ],
      symptoms: [
        'High fever and chills',
        'Severe headache and muscle pain',
        'Nausea and vomiting',
        'Jaundice (yellowing of skin)',
        'Kidney and liver problems'
      ],
      remedies: [
        'Antibiotic treatment as prescribed',
        'Rest and adequate fluid intake',
        'Seek medical attention immediately',
        'Avoid contact with contaminated water',
        'Practice good hygiene'
      ],
      prevention: [
        'Avoid contact with flood water',
        'Wear protective clothing when working with animals',
        'Improve drainage and sanitation',
        'Control rodent populations',
        'Use proper waste disposal methods'
      ],
      severity: 'high',
      icon: 'fas fa-flood',
      color: '#17a2b8',
      references: [
        { label: 'Healthdirect Australia', url: 'https://www.healthdirect.gov.au/leptospirosis', description: 'Australian leptospirosis information' },
        { label: 'Victorian Department of Health', url: 'https://www.health.vic.gov.au/infectious-diseases/leptospirosis', description: 'Victorian leptospirosis guidelines' }
      ]
    }
  ],
  'water-scarcity': [
    {
      id: 'dehydration',
      name: 'Severe Dehydration',
      description: 'Life-threatening condition caused by lack of safe drinking water',
      causes: [
        'Limited access to safe drinking water',
        'Water contamination preventing consumption',
        'Inadequate water storage and distribution',
        'Extreme weather conditions',
        'Infrastructure failures'
      ],
      symptoms: [
        'Extreme thirst and dry mouth',
        'Dark yellow or no urine output',
        'Dizziness and confusion',
        'Rapid heartbeat and breathing',
        'Sunken eyes and dry skin'
      ],
      remedies: [
        'Immediate rehydration with oral rehydration solution',
        'Seek emergency medical attention',
        'Use any available safe water source',
        'Rest in cool, shaded area',
        'Monitor vital signs closely'
      ],
      prevention: [
        'Store adequate safe water supplies',
        'Have emergency water purification methods',
        'Monitor water quality regularly',
        'Plan for water shortages',
        'Educate community about water conservation'
      ],
      severity: 'high',
      icon: 'fas fa-tint-slash',
      color: '#dc3545',
      references: [
        { label: 'Healthdirect Australia', url: 'https://www.healthdirect.gov.au/dehydration', description: 'Australian dehydration information' },
        { label: 'WHO Dehydration', url: 'https://www.who.int/news-room/fact-sheets/detail/dehydration', description: 'WHO dehydration information' }
      ]
    },
    {
      id: 'water-stress',
      name: 'Water Stress-Related Illness',
      description: 'Health problems caused by limited access to clean water for hygiene',
      causes: [
        'Insufficient water for personal hygiene',
        'Water rationing and restrictions',
        'Poor water quality discouraging use',
        'Lack of water infrastructure',
        'Economic barriers to water access'
      ],
      symptoms: [
        'Skin infections and rashes',
        'Eye infections and irritation',
        'Respiratory infections',
        'Gastrointestinal problems',
        'Increased susceptibility to other diseases'
      ],
      remedies: [
        'Use minimal water for essential hygiene',
        'Prioritize hand washing and food preparation',
        'Seek medical attention for infections',
        'Use alternative hygiene methods when possible',
        'Advocate for improved water access'
      ],
      prevention: [
        'Conserve water for essential uses',
        'Use water-efficient hygiene practices',
        'Store water safely when available',
        'Support water infrastructure improvements',
        'Educate about water conservation'
      ],
      severity: 'medium',
      icon: 'fas fa-hand-holding-water',
      color: '#ffc107',
      references: [
        { label: 'Victorian Department of Health', url: 'https://www.health.vic.gov.au/water-quality', description: 'Victorian water quality guidelines' },
        { label: 'Australian Government Health', url: 'https://www.health.gov.au/health-topics/water-quality', description: 'Australian water quality standards' }
      ]
    }
  ]
};

// Computed properties
const categories = computed(() => [
  { id: 'water-borne', name: 'Water-Borne Diseases', icon: 'fas fa-tint', color: '#dc3545' },
  { id: 'parasitic', name: 'Parasitic Infections', icon: 'fas fa-bug', color: '#20c997' },
  { id: 'sanitation-related', name: 'Sanitation-Related', icon: 'fas fa-toilet', color: '#fd7e14' },
  { id: 'water-scarcity', name: 'Water Scarcity Issues', icon: 'fas fa-tint-slash', color: '#17a2b8' }
]);

const currentConditions = computed(() => {
  return selectedCategory.value ? healthConditions[selectedCategory.value] : [];
});

const currentCondition = computed(() => {
  return selectedCondition.value;
});

// Methods
const selectCategory = (categoryId) => {
  selectedCategory.value = categoryId;
  selectedCondition.value = null;
  currentStep.value = 2;
};

const selectCondition = (condition) => {
  selectedCondition.value = condition;
  currentStep.value = 3;
};

const goBack = () => {
  if (currentStep.value === 3) {
    currentStep.value = 2;
    selectedCondition.value = null;
  } else if (currentStep.value === 2) {
    currentStep.value = 1;
    selectedCategory.value = '';
  }
};

const resetComponent = () => {
  currentStep.value = 1;
  selectedCategory.value = '';
  selectedCondition.value = null;
};

const getSeverityColor = (severity) => {
  switch (severity) {
    case 'high': return '#dc3545';
    case 'medium': return '#ffc107';
    case 'low': return '#28a745';
    default: return '#6c757d';
  }
};

const getSeverityLabel = (severity) => {
  switch (severity) {
    case 'high': return 'HIGH RISK';
    case 'medium': return 'MODERATE RISK';
    case 'low': return 'LOW RISK';
    default: return 'UNKNOWN';
  }
};

const openReference = (url) => {
  window.open(url, '_blank', 'noopener,noreferrer');
};

// Initialize component
onMounted(() => {
  // Component initialization if needed
});
</script>

<template>
  <div class="water-health-info">
    <!-- Header -->
    <div class="section-header text-center mb-5">
      <h1 class="display-6 fw-bold mb-3">Water Health Information</h1>
      <p class="lead text-muted">Learn about water-related health conditions, their causes, symptoms, and how to prevent them</p>
    </div>

    <!-- Progress Indicator -->
    <div class="progress-indicator mb-5">
      <div class="progress-container">
        <div class="progress-step" v-for="step in 3" :key="step" :class="{ 
          active: step === currentStep, 
          completed: step < currentStep 
        }">
          <div class="step-number">{{ step }}</div>
          <div class="step-label">
            <span v-if="step === 1">Choose Category</span>
            <span v-else-if="step === 2">Select Condition</span>
            <span v-else-if="step === 3">View Details</span>
          </div>
        </div>
      </div>
    </div>

    <!-- Step 1: Category Selection -->
    <div v-if="currentStep === 1" class="step-content">
      <div class="step-header text-center mb-5">
        <h3 class="fw-bold mb-2 text-primary">Choose a Health Category</h3>
        <p class="text-muted lead">Select the type of water-related health condition you want to learn about</p>
      </div>

      <div class="row g-4">
        <div class="col-md-6 col-lg-3" v-for="category in categories" :key="category.id">
          <div class="category-card">
            <button 
              @click="selectCategory(category.id)"
              class="category-btn"
              :style="{ borderColor: category.color }"
            >
              <i :class="category.icon" class="category-icon" :style="{ color: category.color }"></i>
              <h5 class="category-title">{{ category.name }}</h5>
            </button>
          </div>
        </div>
      </div>
    </div>

    <!-- Step 2: Condition Selection -->
    <div v-if="currentStep === 2" class="step-content">
      <div class="step-header text-center mb-5">
        <h3 class="fw-bold mb-2 text-primary">Select a Condition</h3>
        <p class="text-muted lead">Choose a specific condition to learn more about</p>
      </div>

      <div class="row g-4">
        <div class="col-lg-6" v-for="condition in currentConditions" :key="condition.id">
          <div class="condition-card">
            <button 
              @click="selectCondition(condition)"
              class="condition-btn"
            >
              <div class="condition-header">
                <i :class="condition.icon" class="condition-icon" :style="{ color: condition.color }"></i>
                <div class="condition-severity" :style="{ backgroundColor: getSeverityColor(condition.severity) }">
                  {{ getSeverityLabel(condition.severity) }}
                </div>
              </div>
              
              <div class="condition-content">
                <h4 class="condition-name">{{ condition.name }}</h4>
                <p class="condition-description">{{ condition.description }}</p>
              </div>
            </button>
          </div>
        </div>
      </div>
    </div>

    <!-- Step 3: Condition Details -->
    <div v-if="currentStep === 3 && currentCondition" class="step-content">
      <div class="condition-details">
        <!-- Condition Header -->
        <div class="details-header text-center mb-5">
          <div class="condition-icon-large mb-3">
            <i :class="currentCondition.icon" :style="{ color: currentCondition.color }"></i>
          </div>
          <h2 class="fw-bold mb-2">{{ currentCondition.name }}</h2>
          <p class="lead text-muted">{{ currentCondition.description }}</p>
          <div class="severity-badge" :style="{ backgroundColor: getSeverityColor(currentCondition.severity) }">
            {{ getSeverityLabel(currentCondition.severity) }}
          </div>
        </div>

        <!-- Condition Information -->
        <div class="row g-4">
          <!-- Causes -->
          <div class="col-lg-6">
            <div class="info-card">
              <div class="info-header">
                <i class="fas fa-exclamation-triangle text-warning me-2"></i>
                <h4 class="fw-bold">Causes</h4>
              </div>
              <ul class="info-list">
                <li v-for="(cause, index) in currentCondition.causes" :key="index">
                  <i class="fas fa-arrow-right me-2"></i>{{ cause }}
                </li>
              </ul>
            </div>
          </div>

          <!-- Symptoms -->
          <div class="col-lg-6">
            <div class="info-card">
              <div class="info-header">
                <i class="fas fa-heartbeat text-danger me-2"></i>
                <h4 class="fw-bold">Symptoms</h4>
              </div>
              <ul class="info-list">
                <li v-for="(symptom, index) in currentCondition.symptoms" :key="index">
                  <i class="fas fa-arrow-right me-2"></i>{{ symptom }}
                </li>
              </ul>
            </div>
          </div>

          <!-- Remedies -->
          <div class="col-lg-6">
            <div class="info-card">
              <div class="info-header">
                <i class="fas fa-medkit text-success me-2"></i>
                <h4 class="fw-bold">Treatment & Remedies</h4>
              </div>
              <ul class="info-list">
                <li v-for="(remedy, index) in currentCondition.remedies" :key="index">
                  <i class="fas fa-arrow-right me-2"></i>{{ remedy }}
                </li>
              </ul>
            </div>
          </div>

          <!-- Prevention -->
          <div class="col-lg-6">
            <div class="info-card">
              <div class="info-header">
                <i class="fas fa-shield-alt text-primary me-2"></i>
                <h4 class="fw-bold">Prevention</h4>
              </div>
              <ul class="info-list">
                <li v-for="(prevention, index) in currentCondition.prevention" :key="index">
                  <i class="fas fa-arrow-right me-2"></i>{{ prevention }}
                </li>
              </ul>
            </div>
          </div>
        </div>

        <!-- References -->
        <div v-if="currentCondition.references && currentCondition.references.length > 0" class="references-section mt-5">
          <div class="references-card">
            <div class="references-header">
              <i class="fas fa-external-link-alt me-2"></i>
              <h4 class="fw-bold mb-0">References & Resources</h4>
            </div>
            <div class="references-list">
              <div 
                v-for="ref in currentCondition.references" 
                :key="ref.label"
                class="reference-item"
                @click="openReference(ref.url)"
              >
                <div class="reference-content">
                  <h6 class="reference-title">{{ ref.label }}</h6>
                  <p class="reference-description">{{ ref.description }}</p>
                </div>
                <i class="fas fa-external-link-alt reference-icon"></i>
              </div>
            </div>
          </div>
        </div>

        <!-- Important Notice -->
        <div class="important-notice mt-5">
          <div class="notice-content">
            <i class="fas fa-info-circle me-3"></i>
            <div>
              <h5 class="fw-bold mb-2">Important Notice</h5>
              <p class="mb-0">
                This information is for educational purposes only. If you or your child experience any of these symptoms, 
                seek medical attention immediately. Always consult with healthcare professionals for proper diagnosis and treatment.
              </p>
            </div>
          </div>
        </div>
      </div>
    </div>

    <!-- Navigation -->
    <div class="navigation-footer">
      <div class="container">
        <div class="footer-content">
          <div class="footer-actions">
            <MaterialButton 
              v-if="currentStep > 1"
              @click="goBack"
              :color="'secondary'"
              :size="'lg'"
              class="me-3"
            >
              <i class="fas fa-arrow-left me-2"></i>
              Back
            </MaterialButton>
            
            <MaterialButton 
              v-if="currentStep < 3"
              @click="resetComponent"
              :color="'outline-primary'"
              :size="'lg'"
            >
              <i class="fas fa-home me-2"></i>
              Start Over
            </MaterialButton>
          </div>
        </div>
      </div>
    </div>
  </div>
</template>

<style scoped>
.water-health-info {
  background: linear-gradient(135deg, #f8f9fa 0%, #e3f2fd 100%);
  min-height: 100vh;
  padding-bottom: 120px;
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

.progress-container {
  display: flex;
  justify-content: center;
  align-items: center;
  gap: 3rem;
  flex-wrap: wrap;
}

.progress-step {
  display: flex;
  flex-direction: column;
  align-items: center;
  gap: 0.75rem;
  position: relative;
}

.step-number {
  width: 50px;
  height: 50px;
  border-radius: 50%;
  background: #E5E7EB;
  color: #6B7280;
  display: flex;
  align-items: center;
  justify-content: center;
  font-weight: 700;
  font-size: 1.2rem;
  transition: all 0.3s ease;
  border: 3px solid #E5E7EB;
}

.progress-step.active .step-number {
  background: #007bff;
  color: white;
  border-color: #007bff;
  box-shadow: 0 0 0 4px rgba(0, 123, 255, 0.2);
  transform: scale(1.1);
}

.progress-step.completed .step-number {
  background: #28a745;
  color: white;
  border-color: #28a745;
}

.step-label {
  font-size: 0.9rem;
  font-weight: 600;
  color: #6B7280;
  text-align: center;
  min-width: 120px;
}

.progress-step.active .step-label {
  color: #007bff;
  font-weight: 700;
}

.progress-step.completed .step-label {
  color: #28a745;
}

/* Step Content */
.step-content {
  max-width: 1200px;
  margin: 0 auto;
}

.step-header h3 {
  color: #1E293B;
}

/* Category Cards */
.category-card {
  transition: all 0.3s ease;
}

.category-btn {
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

.category-btn:hover {
  transform: translateY(-4px);
  box-shadow: 0 12px 24px rgba(2, 6, 23, 0.12);
}

.category-icon {
  font-size: 3rem;
  margin-bottom: 1rem;
}

.category-title {
  color: #1E293B;
  font-weight: 600;
  margin: 0;
  font-size: 1.1rem;
}

/* Condition Cards */
.condition-card {
  transition: all 0.3s ease;
}

.condition-btn {
  width: 100%;
  background: white;
  border: 2px solid #E5E7EB;
  border-radius: 16px;
  padding: 1.5rem;
  text-align: left;
  transition: all 0.3s ease;
  box-shadow: 0 6px 18px rgba(2, 6, 23, 0.06);
  height: 100%;
}

.condition-btn:hover {
  transform: translateY(-2px);
  box-shadow: 0 12px 24px rgba(2, 6, 23, 0.12);
  border-color: #007bff;
}

.condition-header {
  display: flex;
  justify-content: space-between;
  align-items: center;
  margin-bottom: 1rem;
}

.condition-icon {
  font-size: 2rem;
}

.condition-severity {
  color: white;
  padding: 0.25rem 0.5rem;
  border-radius: 12px;
  font-weight: 600;
  font-size: 0.7rem;
}

.condition-name {
  color: #1E293B;
  font-weight: 600;
  margin-bottom: 0.5rem;
  font-size: 1.2rem;
}

.condition-description {
  color: #4B5563;
  font-size: 0.9rem;
  margin: 0;
}

/* Condition Details */
.condition-details {
  max-width: 1000px;
  margin: 0 auto;
}

.details-header {
  background: white;
  border-radius: 20px;
  padding: 3rem;
  box-shadow: 0 6px 18px rgba(2, 6, 23, 0.06);
  margin-bottom: 2rem;
}

.condition-icon-large {
  width: 80px;
  height: 80px;
  border-radius: 50%;
  background: #f8f9fa;
  display: flex;
  align-items: center;
  justify-content: center;
  margin: 0 auto;
  font-size: 2.5rem;
}

.severity-badge {
  color: white;
  padding: 0.5rem 1rem;
  border-radius: 20px;
  font-weight: 600;
  font-size: 0.9rem;
  display: inline-block;
  margin-top: 1rem;
}

/* Info Cards */
.info-card {
  background: white;
  border-radius: 16px;
  padding: 2rem;
  box-shadow: 0 6px 18px rgba(2, 6, 23, 0.06);
  height: 100%;
  transition: all 0.3s ease;
}

.info-card:hover {
  transform: translateY(-2px);
  box-shadow: 0 12px 24px rgba(2, 6, 23, 0.12);
}

.info-header {
  display: flex;
  align-items: center;
  margin-bottom: 1.5rem;
  padding-bottom: 1rem;
  border-bottom: 2px solid #f8f9fa;
}

.info-header h4 {
  color: #1E293B;
  margin: 0;
  font-size: 1.2rem;
}

.info-list {
  list-style: none;
  padding: 0;
  margin: 0;
}

.info-list li {
  color: #4B5563;
  font-size: 0.95rem;
  margin-bottom: 0.75rem;
  line-height: 1.5;
  display: flex;
  align-items: flex-start;
}

.info-list li i {
  color: #007bff;
  margin-top: 0.2rem;
  flex-shrink: 0;
}

/* References Section */
.references-section {
  margin-top: 2rem;
}

.references-card {
  background: white;
  border-radius: 16px;
  padding: 2rem;
  box-shadow: 0 6px 18px rgba(2, 6, 23, 0.06);
}

.references-header {
  display: flex;
  align-items: center;
  margin-bottom: 1.5rem;
  padding-bottom: 1rem;
  border-bottom: 2px solid #f8f9fa;
}

.references-header h4 {
  color: #1E293B;
  margin: 0;
  font-size: 1.2rem;
}

.references-header i {
  color: #007bff;
  font-size: 1.2rem;
}

.references-list {
  display: flex;
  flex-direction: column;
  gap: 1rem;
}

.reference-item {
  display: flex;
  align-items: center;
  justify-content: space-between;
  padding: 1rem;
  background: #f8f9fa;
  border-radius: 12px;
  cursor: pointer;
  transition: all 0.3s ease;
  border: 2px solid transparent;
}

.reference-item:hover {
  background: #e3f2fd;
  border-color: #007bff;
  transform: translateY(-2px);
  box-shadow: 0 4px 12px rgba(0, 123, 255, 0.15);
}

.reference-content {
  flex: 1;
}

.reference-title {
  color: #1E293B;
  font-weight: 600;
  margin-bottom: 0.25rem;
  font-size: 1rem;
}

.reference-description {
  color: #6B7280;
  font-size: 0.85rem;
  margin: 0;
}

.reference-icon {
  color: #007bff;
  font-size: 1rem;
  margin-left: 1rem;
}

/* Important Notice */
.important-notice {
  background: linear-gradient(135deg, #fff3cd, #ffeaa7);
  border: 1px solid #ffc107;
  border-radius: 16px;
  padding: 2rem;
}

.notice-content {
  display: flex;
  align-items: flex-start;
}

.notice-content i {
  color: #856404;
  font-size: 1.5rem;
  flex-shrink: 0;
}

.notice-content h5 {
  color: #856404;
  margin: 0;
}

.notice-content p {
  color: #856404;
  margin: 0;
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
    gap: 1.5rem;
  }
  
  .step-number {
    width: 40px;
    height: 40px;
    font-size: 1rem;
  }
  
  .step-label {
    font-size: 0.8rem;
    min-width: 100px;
  }
  
  .category-btn {
    min-height: 140px;
    padding: 1.5rem;
  }
  
  .condition-btn {
    margin-bottom: 1rem;
  }
  
  .details-header {
    padding: 2rem;
  }
  
  .info-card {
    margin-bottom: 1rem;
  }
  
  .references-card {
    padding: 1.5rem;
  }
  
  .reference-item {
    padding: 0.75rem;
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
  
  .category-btn {
    min-height: 120px;
    padding: 1rem;
  }
  
  .category-icon {
    font-size: 2rem;
  }
  
  .details-header {
    padding: 1.5rem;
  }
  
  .info-card {
    padding: 1.5rem;
  }
  
  .important-notice {
    padding: 1.5rem;
  }
}
</style>
