<template>
  <!-- Navigation bar -->
  <div class="container position-sticky z-index-sticky top-0 navbar-container">
    <div class="row">
      <div class="col-12">
        <NavbarDefault :sticky="true" />
      </div>
    </div>
  </div>
    
  <!-- Main content -->
  <div class="container-fluid px-4 mt-6 pt-5 main-content">
    <!-- Page Introduction -->
    <div class="row mb-4">
      <div class="col-12">
        <div class="card shadow-sm border-0">
          <div class="card-body">
            <h4 class="mb-3 text-center">
              <i class="material-icons me-2 text-info">shield</i>
              Safe Sanitation & Hygiene Support
            </h4>
            <p class="text-muted mb-3 text-center">
              This tool provides step-by-step guidance for sanitation and hygiene during water emergencies. Simply follow the 3-step process below: First, choose your situation (General/Emergency mode), then select your location type, and finally specify your needs. The system will generate a personalized checklist and safety instructions tailored to your circumstances.
            </p>
          </div>
        </div>
      </div>
    </div>

    <!-- Progress Indicator -->
    <div class="progress-section">
      <div class="container">
        <div class="row">
          <div class="col-12">
            <div class="progress-steps">
              <div class="step" :class="{ active: currentStep >= 1, completed: currentStep > 1 }">
                 <div class="step-circle" :class="{ active: currentStep >= 1, completed: currentStep > 1 }">
                   <span class="step-number">1</span>
                 </div>
                 <div class="step-label">Who needs guidance</div>
              </div>
              <div class="step-line" :class="{ active: currentStep > 1 }"></div>
              <div class="step" :class="{ active: currentStep >= 2, completed: currentStep > 2 }">
                 <div class="step-circle" :class="{ active: currentStep >= 2, completed: currentStep > 2 }">
                   <span class="step-number">2</span>
                 </div>
                 <div class="step-label">Infant age</div>
              </div>
              <div class="step-line" :class="{ active: currentStep > 2 }"></div>
              <div class="step" :class="{ active: currentStep >= 3 }">
                 <div class="step-circle" :class="{ active: currentStep >= 3 }">
                   <span class="step-number">3</span>
                 </div>
                 <div class="step-label">Household & advisory</div>
              </div>
            </div>
          </div>
        </div>
      </div>
    </div>

    <!-- Mode Selection Cards -->
    <div v-if="currentStep === 1" class="selection-section">
      <div class="container">
        <div class="row">
          <div class="col-12">
            <h2 class="text-center mb-5">What's your situation?</h2>
            <div class="row g-4">
              <div class="col-12 col-md-6">
                <div class="mode-card" :class="{ selected: mode === 'general' }" @click="selectMode('general')">
                  <div class="card-content">
                    <h4>General Sanitation</h4>
                    <p>Short outages, low pressure, brief contamination</p>
                    <div class="card-features">
                      <span class="feature-tag">Low pressure</span>
                      <span class="feature-tag">Brief outages</span>
                      <span class="feature-tag">Minor contamination</span>
                    </div>
                  </div>
                </div>
              </div>
              <div class="col-12 col-md-6">
                <div class="mode-card" :class="{ selected: mode === 'flood' }" @click="selectMode('flood')">
                  <div class="card-content">
                    <h4>Flood / Water-logging</h4>
                    <p>Toilets unusable, services disrupted, displacement</p>
                    <div class="card-features">
                      <span class="feature-tag">Toilets unusable</span>
                      <span class="feature-tag">Service disruption</span>
                      <span class="feature-tag">Displacement</span>
                    </div>
                  </div>
                </div>
              </div>
            </div>
          </div>
        </div>
      </div>
    </div>

    <!-- Place Selection Cards -->
    <div v-if="currentStep === 2" class="selection-section">
      <div class="container">
        <div class="row">
          <div class="col-12">
            <h2 class="text-center mb-5">Where are you?</h2>
            <p class="text-center text-muted mb-4">Select your current location to get personalized guidance</p>
            
            <!-- Inline Validation Error -->
            <div v-if="placeValidationError" class="alert alert-danger text-center mb-4" role="alert">
              <i class="fas fa-exclamation-triangle me-2"></i>
              {{ placeValidationError }}
            </div>
            
            <div class="row g-4">
              <div class="col-12 col-md-6 col-lg-3" v-for="placeOption in placeOptions" :key="placeOption.value">
                <div 
                  class="place-card" 
                  :class="{ 
                    selected: place === placeOption.value,
                    'has-error': placeValidationError && !place
                  }" 
                  @click="selectPlace(placeOption.value)"
                  @keydown.enter="selectPlace(placeOption.value)"
                  @keydown.space.prevent="selectPlace(placeOption.value)"
                  :tabindex="0"
                  role="button"
                  :aria-pressed="place === placeOption.value"
                  :aria-label="`Select ${placeOption.label} - ${placeOption.description}`"
                >
                  <div class="card-content">
                    <h5>{{ placeOption.label }}</h5>
                    <p>{{ placeOption.description }}</p>
                  </div>
                </div>
              </div>
            </div>
          </div>
        </div>
      </div>
    </div>

    <!-- Profile Flags -->
    <div v-if="currentStep === 2" class="profile-section">
      <div class="container">
        <div class="row">
          <div class="col-12">
            <h3 class="text-center mb-4">Special considerations</h3>
            <div class="row g-3 justify-content-center">
              <div class="col-12 col-md-6">
                <div class="profile-card" :class="{ active: profile.pregnant }" @click="updateProfile('pregnant', !profile.pregnant)">
                  <div class="profile-content">
                    <h5>Pregnant</h5>
                    <p>Special hygiene needs during pregnancy</p>
                  </div>
                </div>
              </div>
              <div class="col-12 col-md-6">
                <div class="profile-card" :class="{ active: profile.infant }" @click="updateProfile('infant', !profile.infant)">
                  <div class="profile-content">
                    <h5>Infant in Household</h5>
                    <p>Extra care for baby's hygiene and safety</p>
                  </div>
                </div>
              </div>
            </div>
          </div>
        </div>
      </div>
    </div>

    <!-- Navigation Buttons -->
    <div v-if="currentStep < 3" class="navigation-section">
      <div class="container">
        <div class="row">
          <div class="col-12 text-center">
            <div class="navigation-buttons">
              <router-link to="/" class="btn btn-outline-primary me-3 mb-2">
                <i class="fas fa-home me-2"></i>Back to Home
              </router-link>
              <button v-if="currentStep > 1" class="btn btn-outline-secondary me-3 mb-2" @click="goBack">
                <i class="fas fa-arrow-left me-2"></i>Back
              </button>
              <button v-if="currentStep === 1 && mode" class="btn btn-primary btn-lg mb-2" @click="nextStep">
                Continue <i class="fas fa-arrow-right ms-2"></i>
              </button>
              <button v-if="currentStep === 2" class="btn btn-success btn-lg mb-2" @click="generateChecklist">
                <i class="fas fa-magic me-2"></i>Get My Checklist
              </button>
            </div>
          </div>
        </div>
      </div>
    </div>

    <!-- Loading State -->
    <div v-if="loading" class="loading-section">
      <div class="container">
        <div class="row">
          <div class="col-12 text-center">
            <div class="loading-spinner">
              <i class="fas fa-spinner fa-spin fa-3x text-primary mb-3"></i>
              <h4>Generating your personalized checklist...</h4>
              <p class="text-muted">This may take a few moments</p>
            </div>
          </div>
        </div>
      </div>
    </div>

    <!-- Error State -->
    <div v-if="error" class="error-section">
      <div class="container">
        <div class="row">
          <div class="col-12">
            <div class="alert alert-danger">
              <i class="fas fa-exclamation-triangle me-2"></i>
              {{ error }}
            </div>
          </div>
        </div>
      </div>
    </div>

    <!-- Results Section -->
    <div v-if="currentStep === 3 && checklist.length" class="results-section">
      <div class="container">
        <div class="row">
          <div class="col-12">
            <div class="results-header text-center mb-5">
              <h2 class="display-6 fw-bold text-success">
                <i class="fas fa-check-circle me-3"></i>
                Your Personalized Checklist
              </h2>
              <p class="lead">Tailored for {{ mode }} situation at {{ getPlaceLabel() }}</p>
            </div>
          </div>
        </div>

        <div class="row g-4">
          <!-- Main Checklist -->
          <div class="col-12 col-lg-8">
             <div class="action-plan-container">
               <div class="action-plan-header">
                 <h2 class="action-plan-title">Your Action Plan</h2>
                 <p class="action-plan-subtitle">These steps protect you and your baby. Proper sanitation prevents waterborne diseases and ensures safe living conditions during water emergencies.</p>
                 
                 <div class="progress-section">
                   <div class="progress-card">
                     <div class="progress-info">
                       <div class="progress-stats">
                         <span class="progress-number">{{ completedItems }}</span>
                         <span class="progress-label">of {{ checklist.length }} completed</span>
                </div>
                       <div class="progress-percentage">{{ completionPercentage }}%</div>
                     </div>
                     <div class="progress-bar-container">
                       <div class="progress-bar" :style="{ width: completionPercentage + '%' }"></div>
                     </div>
                     <div class="progress-message" v-if="completionPercentage > 0">
                       <span v-if="completionPercentage < 25">You're getting started! Every step counts.</span>
                       <span v-else-if="completionPercentage < 50">You're making good progress! Keep it up.</span>
                       <span v-else-if="completionPercentage < 75">You're doing great! Almost there.</span>
                       <span v-else-if="completionPercentage < 100">You're making excellent progress!</span>
                       <span v-else>🎉 Congratulations! You've completed your action plan!</span>
                     </div>
                   </div>
                 </div>
              </div>
              
              <!-- Priority Actions -->
              <div v-if="checklistData && checklistData.summary_top3 && checklistData.summary_top3.length > 0" class="priority-actions-section">
                <div class="section-header">
                  <h3 class="section-title">Priority Actions</h3>
                  <p class="section-subtitle">These steps protect you and your baby. Start with these critical actions.</p>
                </div>
                
                <div class="priority-cards">
                  <div v-for="(item, idx) in checklistData.summary_top3" :key="'urgent-' + (item.id || idx)" class="priority-card" :class="[getUrgencyClass(item.priority), { completed: item.done }]">
                      <div class="card-header">
                      <div class="priority-badge" :class="getUrgencyClass(item.priority)">
                          {{ getPriorityText(item.priority) }}
                        </div>
                        <div class="card-checkbox">
                          <input type="checkbox" :id="'urgent-' + idx" v-model="item.done" class="modern-checkbox" @change="onCheckboxChange(item)" />
                        </div>
                      </div>
                    
                    <div class="card-content">
                      <h4 class="card-title">{{ item.title }}</h4>
                      <p class="card-description">{{ getActionDescription(item) }}</p>
                      
                      <div class="card-actions" v-if="item.sources && item.sources.length > 0">
                        <div class="source-badges">
                          <span v-for="source in item.sources" :key="source.label" class="source-badge" @click="openReference(source.url)">
                            <i class="fas fa-external-link-alt me-1"></i>{{ source.label }}
                          </span>
                        </div>
                      </div>
                    </div>
                  </div>
                </div>
              </div>

              <!-- View Complete Checklist -->
              <div class="expand-section" v-if="!showFullChecklist">
                <div class="expand-card">
                  <div class="expand-content">
                    <h4 class="expand-title">Complete Checklist</h4>
                    <p class="expand-description">{{ remainingItems.length }} additional steps to ensure comprehensive sanitation and hygiene</p>
                  </div>
                  <button class="expand-btn" @click="showFullChecklist = true">
                    <i class="fas fa-arrow-down me-2"></i>View All Steps
                </button>
                </div>
              </div>

              <!-- Complete Action Plan -->
              <div v-if="showFullChecklist" class="complete-checklist">
                <div class="section-header">
                  <h3 class="section-title">Complete Checklist</h3>
                  <p class="section-subtitle">Comprehensive steps organized by category for complete sanitation coverage</p>
                </div>
                
                <!-- Organized by Category -->
                <div v-for="category in groupedChecklist" :key="category.name" class="category-section">
                  <div class="category-header">
                    <div class="category-info">
                      <div class="category-icon">{{ getCategoryIcon(category.name) }}</div>
                      <div class="category-details">
                        <h4 class="category-title">{{ category.displayName }}</h4>
                        <p class="category-description">{{ getCategoryDescription(category.name) }}</p>
                      </div>
                    </div>
                    <div class="category-progress">
                      <div class="progress-info">
                        <span class="progress-count">{{ category.completed }}/{{ category.items.length }}</span>
                        <span class="progress-percentage">{{ category.completionPercentage }}%</span>
                      </div>
                      <div class="progress-bar-container">
                        <div class="progress-bar" :style="{ width: category.completionPercentage + '%' }"></div>
                      </div>
                    </div>
                  </div>
                  
                  <div class="category-items">
                    <div v-for="(item, idx) in category.items" :key="'full-' + category.name + '-' + idx" 
                         class="action-card" :class="[item.category, { completed: item.done }]">
                      <div class="card-header">
                        <div class="priority-badge" :class="getPriorityClass(item.priority)">
                          {{ getPriorityText(item.priority) }}
                        </div>
                        <div class="card-checkbox">
                          <input type="checkbox" :id="'full-' + category.name + '-' + idx" v-model="item.done" class="modern-checkbox" @change="onCheckboxChange(item)" />
                      </div>
                        </div>
                      <div class="card-content">
                        <h5 class="card-title">{{ item.title }}</h5>
                        <p class="card-description" v-if="item.detail">{{ item.detail }}</p>
                      </div>
                    </div>
                  </div>
                </div>
              </div>
            </div>
          </div>

          <!-- Quick Actions Sidebar -->
          <div class="col-12 col-lg-4">
            <div class="quick-actions-panel">
              <div class="panel-header">
                <h4 class="panel-title">Quick Actions</h4>
                <p class="panel-subtitle">Essential tools and navigation</p>
              </div>
              
              <div class="action-buttons">
                <router-link to="/" class="action-button primary">
                  <i class="fas fa-home"></i>
                  <span>Back to Home</span>
                </router-link>
                
                <button class="action-button secondary" @click="downloadPDF">
                  <i class="fas fa-download"></i>
                  <span>Download PDF</span>
                </button>
                
                <button class="action-button tertiary" @click="startNewChecklist">
                  <i class="fas fa-redo"></i>
                  <span>Start Over</span>
          </button>
    </div>

              <!-- Progress Summary -->
              <div class="progress-summary">
                <h5 class="summary-title">Your Progress</h5>
                <div class="summary-stats">
                  <div class="stat-item">
                    <span class="stat-number">{{ completedItems }}</span>
                    <span class="stat-label">Completed</span>
        </div>
                  <div class="stat-item">
                    <span class="stat-number">{{ checklist.length - completedItems }}</span>
                    <span class="stat-label">Remaining</span>
              </div>
              </div>
                <div class="summary-progress">
                  <div class="progress-bar-container">
                    <div class="progress-bar" :style="{ width: completionPercentage + '%' }"></div>
              </div>
                  <span class="progress-text">{{ completionPercentage }}% Complete</span>
              </div>
            </div>
            </div>
          </div>
        </div>
      </div>
    </div>

    <!-- Consistent Footer -->
    <DefaultFooter />

    <!-- Why Modal -->
    <div v-if="showWhyModal" class="micro-flow-overlay" @click="showWhyModal = false">
      <div class="micro-flow-modal" @click.stop>
        <div class="modal-header">
          <h5>
            <span class="me-2">{{ selectedItem?.icon || '📋' }}</span>
            Why is this important?
          </h5>
          <button class="btn-close" @click="showWhyModal = false">
            <i class="fas fa-times"></i>
          </button>
        </div>
        <div class="modal-body">
          <div class="why-content">
            <div class="why-explanation">
              <h6 class="mb-3">{{ selectedItem?.title }}</h6>
              <p class="lead">{{ selectedItem?.why || 'This step helps maintain hygiene and safety during sanitation disruptions.' }}</p>
            </div>
            <div class="why-sources mt-4">
              <h6>Sources:</h6>
              <ul class="list-unstyled">
                <li><a href="https://www.who.int/health-topics/water-sanitation-and-hygiene-wash" target="_blank" rel="noopener">WHO WASH Guidelines</a></li>
                <li><a href="https://www.cdc.gov/hygiene/index.html" target="_blank" rel="noopener">CDC Hygiene Guidelines</a></li>
              </ul>
            </div>
          </div>
        </div>
      </div>
    </div>


    <!-- Chat Bot Drawer -->
    <div v-if="showChatBot" class="chat-drawer">
      <div class="chat-header">
        <h6>
          <i class="fas fa-robot me-2"></i>
          Hygiene Helper
        </h6>
        <button class="btn-close" @click="showChatBot = false">
          <i class="fas fa-times"></i>
        </button>
      </div>
      <div class="chat-messages">
        <div v-for="(message, idx) in chatMessages" :key="idx" class="chat-message" :class="message.role">
          <div class="message-content">
            <p>{{ message.content }}</p>
            <div v-if="message.sources && message.sources.length" class="message-sources">
              <a 
                v-for="source in message.sources" 
                :key="source.label"
                :href="source.url" 
                target="_blank" 
                rel="noopener"
                class="source-chip"
                :aria-label="`Reference: ${source.label}`"
              >
                {{ source.label }}
              </a>
            </div>
          </div>
          <small class="message-time">{{ message.timestamp.toLocaleTimeString() }}</small>
        </div>
        <div v-if="chatLoading" class="chat-message assistant">
          <div class="message-content">
            <div class="typing-indicator">
              <span></span>
              <span></span>
              <span></span>
            </div>
          </div>
        </div>
      </div>
      <div class="chat-input">
        <div class="input-group">
          <input 
            v-model="chatInput" 
            @keyup.enter="sendChatMessage"
            type="text" 
            class="form-control" 
            placeholder="Ask about hygiene and sanitation..."
            :disabled="chatLoading"
          />
          <button class="btn btn-primary" @click="sendChatMessage" :disabled="chatLoading || !chatInput.trim()">
            <i class="fas fa-paper-plane"></i>
          </button>
        </div>
      </div>
    </div>

      <!-- Toast Notification -->
      <div v-if="showToast" class="toast-container">
        <div class="toast" :class="'toast-' + toastType" role="alert" aria-live="polite">
          <div class="toast-header">
            <i :class="getToastIcon()" class="me-2"></i>
            <strong class="me-auto">{{ getToastTitle() }}</strong>
            <button type="button" class="btn-close" @click="hideToast" aria-label="Close"></button>
          </div>
          <div class="toast-body">
            {{ toastMessage }}
          </div>
        </div>
      </div>
    </div>
</template>

<script>
import NavbarDefault from "../components/navigation/NavbarDefault.vue";
import DefaultFooter from "../components/layout/FooterDefault.vue";

export default {
  name: "SanitationSupportView",
  components: {
    NavbarDefault,
    DefaultFooter
  },
  data() {
    return {
      // Step management
      currentStep: 1,
      
      // Selection data
      mode: "",
      place: "",
      profile: {
        pregnant: false,
        infant: false
      },
      issues: [],
      
      // API state
      loading: false,
      error: "",
      checklistData: null, // New structured checklist data
      checklist: [], // Legacy format for backward compatibility
      
      // Validation state
      placeValidationError: "",
      showToast: false,
      toastMessage: "",
      toastType: "error", // error, success, info
      
      // Micro-flows
      showHandwashTimer: false,
      showDilution: false,
      showWhyModal: false,
      selectedItem: null,
      showFullChecklist: false,
      
      // Chat bot
      showChatBot: false,
      chatMessages: [],
      chatInput: "",
      chatLoading: false,
      
      // Handwash timer
      handwashActive: false,
      handwashSeconds: 20,
      handwashProgress: 0,
      handwashInterval: null,
      
      // Dilution calculator
      targetPpm: 200,
      solutionLitres: 1,
      bleachPercent: 5,
      bleachMl: null,
      
      // Reminders
      reminderTimer: null,
      lastReminder: "",
      
      // Place options
      placeOptions: [
        {
          value: "home",
          label: "Home",
          description: "Your own residence",
          icon: "fas fa-home",
          iconClass: "home"
        },
        {
          value: "safe-site",
          label: "Safe Community Site",
          description: "Designated safe area",
          icon: "fas fa-shield-alt",
          iconClass: "safe"
        },
        {
          value: "rescue",
          label: "Rescue Centre",
          description: "Emergency evacuation center",
          icon: "fas fa-first-aid",
          iconClass: "rescue"
        },
        {
          value: "temporary",
          label: "Temporary Accommodation",
          description: "Friend, relative, or hotel",
          icon: "fas fa-bed",
          iconClass: "temporary"
        }
      ]
    };
  },
  computed: {
    completedItems() {
      return this.checklist.filter(item => item.done).length;
    },
    completionPercentage() {
      return this.checklist.length > 0 ? Math.round((this.completedItems / this.checklist.length) * 100) : 0;
    },
    topThreeUrgent() {
      if (this.checklistData && this.checklistData.summary_top3) {
        return this.checklistData.summary_top3;
      }
      return this.checklist.filter(item => item.priority <= 2).slice(0, 3);
    },
    remainingItems() {
      if (this.checklistData && this.checklistData.sections) {
        return this.checklistData.sections.flatMap(section => section.items);
      }
      return this.checklist.filter(item => item.priority > 2);
    },
    groupedChecklist() {
      if (this.checklistData && this.checklistData.sections) {
        return this.checklistData.sections.map(section => ({
          name: section.name,
          displayName: section.name,
          icon: this.getCategoryIcon(section.name),
          items: section.items,
          completed: section.items.filter(item => item.done).length,
          completionPercentage: this.getSectionCompletionPercentage(section),
          progressClass: 'bg-success'
        }));
      }
      
      // Fallback to legacy grouping
      const groups = {};
      this.checklist.forEach(item => {
        const category = item.category || 'general';
        if (!groups[category]) {
          groups[category] = {
            name: category,
            displayName: this.getCategoryDisplayName(category),
            icon: this.getCategoryIcon(category),
            items: [],
            completed: 0,
            progressClass: this.getCategoryProgressClass(category)
          };
        }
        groups[category].items.push(item);
        if (item.done) {
          groups[category].completed++;
        }
      });
      
      // Calculate completion percentage for each category
      Object.values(groups).forEach(group => {
        group.completionPercentage = group.items.length > 0 
          ? Math.round((group.completed / group.items.length) * 100) 
          : 0;
      });
      
      return Object.values(groups);
    }
  },
  methods: {
    // Step navigation
    selectMode(mode) {
      this.mode = mode;
      this.nextStep();
    },
    selectPlace(place) {
      this.place = place;
      this.placeValidationError = ""; // Clear validation error when place is selected
    },
    nextStep() {
      if (this.currentStep < 3) {
        this.currentStep++;
      }
    },
    goBack() {
      if (this.currentStep > 1) {
        this.currentStep--;
        // Clear validation errors when going back
        this.placeValidationError = "";
      }
    },
    getPlaceLabel() {
      const place = this.placeOptions.find(p => p.value === this.place);
      return place ? place.label : this.place;
    },
    
    // Checklist generation
    async generateChecklist() {
      // Validate place selection
      if (!this.place) {
        this.placeValidationError = "Please select your location to continue";
        this.showToastMessage("Please select your location to get personalized guidance", "error");
        return;
      }
      
      this.error = "";
      this.placeValidationError = "";
      this.loading = true;
      this.checklistData = null;
      this.checklist = [];
      this.currentStep = 3;
      
      try {
        const context = {
          mode: this.mode,
          place: this.place,
          profile: this.profile,
          issues: this.issues
        };
        
        // Always use force=true when user clicks "Get My Checklist" to ensure fresh LLM call
        const res = await fetch("/api/guidance/checklist?force=true", {
          method: "POST",
          headers: { "Content-Type": "application/json" },
          body: JSON.stringify(context),
        });
        
        if (!res.ok) throw new Error("Failed to fetch guidance");
        const data = await res.json();
        this.checklistData = data;
        
        // Convert to legacy format for backward compatibility
        const allItems = [
          ...(data.summary_top3 || []),
          ...(data.sections?.flatMap(section => section.items) || [])
        ];
        this.checklist = allItems;
        
        // Initialize chat with context
        this.initializeChatBot();
        
        // Show success message
        this.showToastMessage("Your personalized checklist is ready!", "success");
        
      } catch (e) {
        this.error = e?.message || "Error generating checklist";
        this.currentStep = 2; // Go back to place selection on error
        this.showToastMessage("Sorry, we couldn't generate your checklist. Please try again.", "error");
      } finally {
        this.loading = false;
      }
    },
    
    // Auto-load checklist (for page revisits, allows cache)
    async loadChecklistFromCache() {
      if (!this.place || !this.mode) return;
      
      try {
        const context = {
          mode: this.mode,
          place: this.place,
          profile: this.profile,
          issues: this.issues
        };
        
        // Use force=false to allow cache hits for auto-loading
        const res = await fetch("/api/guidance/checklist?force=false", {
          method: "POST",
          headers: { "Content-Type": "application/json" },
          body: JSON.stringify(context),
        });
        
        if (!res.ok) return; // Silently fail for auto-loading
        
        const data = await res.json();
        this.checklistData = data;
        
        // Convert to legacy format for backward compatibility
        const allItems = [
          ...(data.summary_top3 || []),
          ...(data.sections?.flatMap(section => section.items) || [])
        ];
        this.checklist = allItems;
        
        // Initialize chat with context
        this.initializeChatBot();
        
      } catch (e) {
        // Silently fail for auto-loading
        console.log("Auto-load failed:", e);
      }
    },
    
    ensureSpecialActions() {
      if (this.isPregnant) {
        const hasPreg = this.checklist.some(i => /pregnan|postpartum|maternity/i.test(i.title || ""));
        if (!hasPreg) {
          this.checklist.unshift({
            title: "Pregnancy: use pads/liners; avoid tampons/cups",
            detail: "Infection risk during pregnancy/postpartum; change frequently; dispose sealed.",
            done: false,
          });
        }
      }
      if (this.hasInfant) {
        const hasInf = this.checklist.some(i => /infant|baby|nappy|diaper/i.test(i.title || ""));
        if (!hasInf) {
          this.checklist.unshift({
            title: "Infant: clean hands before/after nappy change; disinfect surface",
            detail: "Keep wipes/nappies sealed; store away from food; follow camp bin etiquette.",
            done: false,
          });
        }
      }
    },
    
    // Handwash timer
    startHandwashTimer() {
      this.handwashActive = true;
      this.handwashInterval = setInterval(() => {
        this.handwashSeconds--;
        this.handwashProgress = ((20 - this.handwashSeconds) / 20) * 100;
        
        if (this.handwashSeconds <= 0) {
          this.stopHandwashTimer();
          this.showHandwashTimer = false;
          alert("Great job! You've completed proper hand washing.");
        }
      }, 1000);
    },
    
    stopHandwashTimer() {
      this.handwashActive = false;
      if (this.handwashInterval) {
        clearInterval(this.handwashInterval);
        this.handwashInterval = null;
      }
    },
    
    resetHandwashTimer() {
      this.stopHandwashTimer();
      this.handwashSeconds = 20;
      this.handwashProgress = 0;
    },
    
    // Dilution calculator
    computeBleach() {
      const ppm = Math.max(10, Number(this.targetPpm || 0));
      const L = Math.max(0.1, Number(this.solutionLitres || 0));
      const pct = Math.max(0.5, Number(this.bleachPercent || 0));
      const ml = (ppm * L) / (pct * 10);
      this.bleachMl = ml;
    },
    
    // Offline functionality
    downloadPDF() {
      // Simple print-to-PDF functionality
      window.print();
    },
    
    cacheOffline() {
      // Store checklist in localStorage for offline access
      const cacheData = {
        checklist: this.checklist,
        mode: this.mode,
        place: this.place,
        isPregnant: this.isPregnant,
        hasInfant: this.hasInfant,
        timestamp: new Date().toISOString()
      };
      localStorage.setItem('sanitationChecklist', JSON.stringify(cacheData));
      alert("Checklist cached for offline access!");
    },
    
    startNewChecklist() {
      this.currentStep = 1;
      this.mode = "";
      this.place = "";
      this.isPregnant = false;
      this.hasInfant = false;
      this.checklist = [];
      this.error = "";
    },
    
    // Reminders (simplified for demo)
    startHandwashReminders() {
      this.stopReminders();
      this.reminderTimer = setInterval(() => {
        alert("Reminder: Wash hands at key moments (before food prep/eating; after toilet/nappy handling). Use ABHR ≥60% if no water.");
        this.lastReminder = new Date().toLocaleString();
      }, 90 * 60 * 1000);
      alert("Hand-wash reminders started. You'll get a reminder every 90 minutes.");
      this.lastReminder = new Date().toLocaleString();
    },
    
    stopReminders() {
      if (this.reminderTimer) {
        clearInterval(this.reminderTimer);
        this.reminderTimer = null;
      }
    },
    
    promptFormulaPrepClean() {
      alert("Before formula prep: Clean hands; disinfect prep surface; use bottled or cooled-boiled water for critical steps.");
      this.lastReminder = new Date().toLocaleString();
    },
    
    promptPostNappyDisinfect() {
      alert("After nappy change: Clean hands and disinfect the change surface. Seal nappies/wipes.");
      this.lastReminder = new Date().toLocaleString();
    },
    
    // Enhanced checklist methods
    openWhyModal(item) {
      this.selectedItem = item;
      this.showWhyModal = true;
    },
    
    getCategoryDisplayName(category) {
      const names = {
        'pregnancy': 'Pregnancy Care',
        'infant': 'Infant Hygiene',
        'waste': 'Waste Disposal',
        'water': 'Water Safety',
        'general': 'General Hygiene'
      };
      return names[category] || 'General';
    },
    
    getCategoryIcon(category) {
      const icons = {
        'pregnancy': '🤱',
        'infant': '👶',
        'waste': '🗑️',
        'water': '💧',
        'general': '🧼'
      };
      return icons[category] || '📋';
    },
    
    getCategoryProgressClass(category) {
      const classes = {
        'pregnancy': 'bg-warning',
        'infant': 'bg-info',
        'waste': 'bg-secondary',
        'water': 'bg-primary',
        'general': 'bg-success'
      };
      return classes[category] || 'bg-success';
    },
    
    getPriorityClass(priority) {
      if (priority <= 1) return 'urgent';
      if (priority <= 2) return 'high';
      if (priority <= 3) return 'medium';
      return 'low';
    },
    
    getPriorityText(priority) {
      if (priority === 'critical') return '🔴 Critical';
      if (priority === 'high') return '🟠 High';
      if (priority === 'medium') return '🟡 Medium';
      return '🟢 Low';
    },
    
    // Chat bot methods
    initializeChatBot() {
      this.chatMessages = [
        {
          role: 'assistant',
          content: `Hi! I'm here to help with your ${this.mode} sanitation situation at ${this.getPlaceLabel()}. What would you like to know?`,
          timestamp: new Date()
        }
      ];
    },
    
    toggleChatBot() {
      this.showChatBot = !this.showChatBot;
      if (this.showChatBot && this.chatMessages.length === 0) {
        this.initializeChatBot();
      }
    },
    
    async sendChatMessage() {
      if (!this.chatInput.trim()) return;
      
      const userMessage = {
        role: 'user',
        content: this.chatInput.trim(),
        timestamp: new Date()
      };
      
      this.chatMessages.push(userMessage);
      this.chatInput = '';
      this.chatLoading = true;
      
      try {
        const context = {
          mode: this.mode,
          place: this.place,
          profile: this.profile,
          issues: this.issues
        };
        
        // Collect all sources from checklist items for chat bot context
        const allSources = [];
        if (this.checklistData) {
          // Add sources from top 3 urgent actions
          if (this.checklistData.summary_top3) {
            this.checklistData.summary_top3.forEach(item => {
              if (item.sources) {
                allSources.push(...item.sources);
              }
            });
          }
          // Add sources from sections
          if (this.checklistData.sections) {
            this.checklistData.sections.forEach(section => {
              if (section.items) {
                section.items.forEach(item => {
                  if (item.sources) {
                    allSources.push(...item.sources);
                  }
                });
              }
            });
          }
          // Add general sources
          if (this.checklistData.sources) {
            allSources.push(...this.checklistData.sources);
          }
        }
        
        const res = await fetch("/api/guidance/chat", {
          method: "POST",
          headers: { "Content-Type": "application/json" },
          body: JSON.stringify({
            messages: this.chatMessages.map(msg => ({ role: msg.role, content: msg.content })),
            context: context,
            checklist: this.checklistData,
            sources: allSources
          }),
        });
        
        if (!res.ok) throw new Error("Failed to get response");
        const data = await res.json();
        
        this.chatMessages.push({
          role: 'assistant',
          content: data.message,
          sources: data.sources || [],
          timestamp: new Date()
        });
        
      } catch (e) {
        this.chatMessages.push({
          role: 'assistant',
          content: "I'm sorry, I'm having trouble right now. Please check local health guidance for specific requirements.",
          timestamp: new Date()
        });
      } finally {
        this.chatLoading = false;
      }
    },
    
    // Profile management
    updateProfile(field, value) {
      this.profile[field] = value;
    },
    
    // Toast notification methods
    showToastMessage(message, type = "info") {
      this.toastMessage = message;
      this.toastType = type;
      this.showToast = true;
      
      // Auto-hide after 5 seconds
      setTimeout(() => {
        this.hideToast();
      }, 5000);
    },
    
    hideToast() {
      this.showToast = false;
      this.toastMessage = "";
      this.toastType = "info";
    },
    
    getToastIcon() {
      switch (this.toastType) {
        case "error": return "fas fa-exclamation-triangle";
        case "success": return "fas fa-check-circle";
        case "info": return "fas fa-info-circle";
        default: return "fas fa-info-circle";
      }
    },
    
    getToastTitle() {
      switch (this.toastType) {
        case "error": return "Error";
        case "success": return "Success";
        case "info": return "Information";
        default: return "Information";
      }
    },
    
    // Section completion helpers
    getSectionCompletionPercentage(section) {
      if (!section.items || section.items.length === 0) return 0;
      const completed = section.items.filter(item => item.done).length;
      return Math.round((completed / section.items.length) * 100);
    },
    
    getSectionCompletedCount(section) {
      if (!section.items) return 0;
      return section.items.filter(item => item.done).length;
    },
    
    getCategoryDescription(categoryName) {
      const descriptions = {
        'water': 'Water safety and treatment procedures',
        'hygiene': 'Personal and environmental hygiene practices',
        'waste': 'Waste management and disposal methods',
        'food': 'Food safety and preparation guidelines',
        'emergency': 'Emergency response and safety measures',
        'general': 'General sanitation and maintenance tasks'
      };
      return descriptions[categoryName] || 'Important sanitation and hygiene steps';
    },
    
    getUrgencyClass(priority) {
      switch (priority) {
        case 'urgent': return 'urgency-critical';
        case 'high': return 'urgency-high';
        case 'medium': return 'urgency-medium';
        case 'low': return 'urgency-low';
        default: return 'urgency-medium';
      }
    },
    
    getActionIcon(priority) {
      switch (priority) {
        case 'urgent': return 'fas fa-exclamation-triangle';
        case 'high': return 'fas fa-shield-alt';
        case 'medium': return 'fas fa-check-circle';
        case 'low': return 'fas fa-info-circle';
        default: return 'fas fa-check-circle';
      }
    },
    
    getActionDescription(item) {
      // Return a one-line description about the action with specific reasoning
      if (item.body && item.body.length > 0) {
        // Take the first sentence or first 80 characters
        const firstSentence = item.body.split('.')[0];
        return firstSentence.length > 80 ? firstSentence.substring(0, 80) + '...' : firstSentence;
      }
      
      // Provide specific descriptions based on action title/content
      const title = (item.title || '').toLowerCase();
      
      // Water-related actions
      if (title.includes('water') || title.includes('boil') || title.includes('purify')) {
        return 'Ensures safe drinking water and prevents waterborne diseases.';
      }
      
      // Toilet and sanitation facilities
      if (title.includes('toilet') || title.includes('bathroom') || title.includes('restroom') || title.includes('facility')) {
        return 'Prevents contamination and reduces risk of waterborne illnesses.';
      }
      
      // Hand hygiene actions
      if (title.includes('hand') || title.includes('wash') || title.includes('hygiene') || title.includes('soap')) {
        return 'Prevents the spread of germs and infections.';
      }
      
      // Food safety actions
      if (title.includes('food') || title.includes('cook') || title.includes('prepare') || title.includes('kitchen')) {
        return 'Prevents food contamination and foodborne illnesses.';
      }
      
      // Waste management actions
      if (title.includes('waste') || title.includes('dispose') || title.includes('garbage') || title.includes('trash') || title.includes('bin')) {
        return 'Prevents contamination and maintains clean environment.';
      }
      
      // Cleaning and sanitizing actions
      if (title.includes('sanitize') || title.includes('disinfect') || title.includes('clean') || title.includes('surface')) {
        return 'Eliminates harmful bacteria and viruses from surfaces.';
      }
      
      // Personal hygiene items
      if (title.includes('toothbrush') || title.includes('brush') || title.includes('dental') || title.includes('oral')) {
        return 'Maintains oral hygiene and prevents bacterial infections.';
      }
      
      // Laundry and clothing
      if (title.includes('laundry') || title.includes('clothes') || title.includes('wash') || title.includes('garment')) {
        return 'Removes contaminants and prevents skin infections.';
      }
      
      // Storage and containers
      if (title.includes('store') || title.includes('container') || title.includes('seal') || title.includes('cover')) {
        return 'Protects items from contamination and maintains cleanliness.';
      }
      
      // Emergency and urgent actions
      if (title.includes('emergency') || title.includes('urgent') || title.includes('immediate') || title.includes('critical')) {
        return 'Critical for immediate safety and preventing health risks.';
      }
      
      // Pregnancy-specific actions
      if (title.includes('pregnant') || title.includes('pregnancy') || title.includes('maternal') || title.includes('expecting')) {
        return 'Protects both mother and developing baby from health risks.';
      }
      
      // Infant and child-specific actions
      if (title.includes('infant') || title.includes('baby') || title.includes('child') || title.includes('nappy') || title.includes('diaper')) {
        return 'Essential for protecting your little one\'s developing immune system.';
      }
      
      // Water treatment and filtration
      if (title.includes('filter') || title.includes('treatment') || title.includes('chlorine') || title.includes('bleach')) {
        return 'Removes harmful contaminants and makes water safe for consumption.';
      }
      
      // Ventilation and air quality
      if (title.includes('ventilate') || title.includes('air') || title.includes('breath') || title.includes('mold')) {
        return 'Improves air quality and prevents respiratory issues.';
      }
      
      // Personal protective equipment
      if (title.includes('glove') || title.includes('mask') || title.includes('protective') || title.includes('ppe')) {
        return 'Provides barrier protection against contaminants and infections.';
      }
      
      // Default meaningful description
      return 'Essential step to maintain health and safety during water emergencies.';
    },
    
    openReference(url) {
      if (url) {
        window.open(url, '_blank', 'noopener,noreferrer');
      }
    },
    
    // Handle checkbox changes to ensure progress updates
    onCheckboxChange(item) {
      // Force reactivity update
      this.$nextTick(() => {
        this.$forceUpdate();
      });
      
      // Optional: Add haptic feedback or sound
      if (item.done) {
        // Item completed
        console.log('Item completed:', item.title);
      } else {
        // Item unchecked
        console.log('Item unchecked:', item.title);
      }
    }
  },
  
  beforeUnmount() {
    this.stopHandwashTimer();
    this.stopReminders();
  }
};
</script>

<style scoped>
/* Ensure proper spacing between navigation and content */
.navbar-container {
  margin-bottom: 3rem;
}

.main-content {
  margin-top: 4rem;
  padding-top: 2rem;
}

/* Main Layout */
.sanitation-support {
  min-height: 100vh;
  background: linear-gradient(135deg, #f8f9fa 0%, #e9ecef 100%);
}

/* Breadcrumb Navigation */
.breadcrumb-section {
  background: white;
  padding: 1rem 0;
  border-bottom: 1px solid #e9ecef;
  box-shadow: 0 2px 4px rgba(0,0,0,0.05);
}

.breadcrumb {
  margin-bottom: 0;
  background: none;
  padding: 0;
}

.breadcrumb-item {
  display: flex;
  align-items: center;
}

.breadcrumb-link {
  color: #007bff;
  text-decoration: none;
  font-weight: 500;
  transition: color 0.3s ease;
}

.breadcrumb-link:hover {
  color: #0056b3;
  text-decoration: underline;
}

.breadcrumb-item.active {
  color: #6c757d;
  font-weight: 500;
}

/* Design Tokens */
:root {
  --teal-50: #f0fdfa;
  --teal-100: #ccfbf1;
  --teal-600: #0d9488;
  --cyan-50: #ecfeff;
  --coral-500: #ff6b6b;
  --slate-700: #334155;
  --slate-900: #0f172a;
  --radius-2xl: 1rem;
  --shadow-lg: 0 10px 15px -3px rgba(0, 0, 0, 0.1), 0 4px 6px -2px rgba(0, 0, 0, 0.05);
}

/* Photo Hero Section */
.hero-section {
  position: relative;
  min-height: 60vh;
  display: flex;
  align-items: center;
  justify-content: center;
  margin-bottom: 2rem;
  border-radius: var(--radius-2xl);
  overflow: hidden;
  box-shadow: var(--shadow-lg);
}

.hero-background {
  position: absolute;
  top: 0;
  left: 0;
  right: 0;
  bottom: 0;
  background-image: url('https://images.unsplash.com/photo-1581578731548-c6a0c3f2f6c5?ixlib=rb-4.0.3&ixid=M3wxMjA3fDB8MHxwaG90by1wYWdlfHx8fGVufDB8fHx8fA%3D%3D&auto=format&fit=crop&w=2070&q=80');
  background-size: cover;
  background-position: center;
  background-repeat: no-repeat;
}

.hero-overlay {
  position: absolute;
  top: 0;
  left: 0;
  right: 0;
  bottom: 0;
  background: linear-gradient(135deg, rgba(13, 148, 136, 0.8) 0%, rgba(135, 206, 235, 0.7) 50%, rgba(13, 148, 136, 0.8) 100%);
  backdrop-filter: blur(1px);
}

.hero-content {
  position: relative;
  z-index: 2;
  padding: 3rem 0;
  text-align: center;
}

.hero-title {
  color: white;
  font-weight: 800;
  letter-spacing: -0.025em;
  line-height: 1.1;
  font-size: 3rem;
  text-shadow: 0 4px 8px rgba(0, 0, 0, 0.3);
  margin-bottom: 1.5rem;
}

.hero-subtitle {
  color: rgba(255, 255, 255, 0.95);
  font-size: 1.25rem;
  line-height: 1.6;
  max-width: 68ch;
  margin: 0 auto;
  text-shadow: 0 2px 4px rgba(0, 0, 0, 0.2);
}

.highlight-text {
  color: var(--coral-500);
  font-weight: 700;
  text-decoration: underline;
  text-decoration-color: var(--coral-500);
  text-decoration-thickness: 4px;
  text-underline-offset: 4px;
}

/* Progress Steps */
.progress-section {
  margin-bottom: 3rem;
}

.progress-steps {
  display: flex;
  align-items: center;
  justify-content: center;
  max-width: 600px;
  margin: 0 auto;
}

.step {
  display: flex;
  flex-direction: column;
  align-items: center;
  position: relative;
}


.step-circle {
  width: 50px;
  height: 50px;
  border-radius: 50%;
  background: #CBD5E1;
  display: flex;
  align-items: center;
  justify-content: center;
  margin-bottom: 0.5rem;
  transition: all 0.3s ease;
  border: 3px solid #CBD5E1;
}

.step-circle.active {
  background: #2563EB;
  border-color: #2563EB;
}

.step-circle.completed {
  background: #10B981;
  border-color: #10B981;
}

.step-number {
  color: white;
  font-weight: 600;
  font-size: 1.1rem;
}

.step-circle:not(.active):not(.completed) .step-number {
  color: #64748B;
}

.step-label {
  font-size: 0.9rem;
  font-weight: 600;
  color: #1E293B;
  text-align: center;
  max-width: 120px;
  line-height: 1.3;
}

.step.active .step-label {
  color: #2563EB;
  font-weight: 600;
}

.step.completed .step-label {
  color: #10B981;
  font-weight: 600;
}

.step-line {
  width: 100px;
  height: 3px;
  background: #CBD5E1;
  margin: 0 1rem;
  transition: all 0.3s ease;
}

.step-line.active {
  background: #10B981;
}

/* Selection Cards */
.selection-section {
  margin-bottom: 3rem;
}

.mode-card, .place-card {
  background: white;
  border-radius: var(--radius-2xl);
  padding: 2rem;
  text-align: center;
  cursor: pointer;
  transition: all 0.3s ease;
  border: 3px solid transparent;
  box-shadow: var(--shadow-lg);
  height: 100%;
  position: relative;
  overflow: hidden;
  display: flex;
  flex-direction: column;
  justify-content: space-between;
}

.mode-card::before, .place-card::before {
  content: '';
  position: absolute;
  top: 0;
  left: -100%;
  width: 100%;
  height: 100%;
  background: linear-gradient(90deg, transparent, rgba(13, 148, 136, 0.1), transparent);
  transition: left 0.6s ease;
  z-index: 1;
}

.mode-card:hover::before, .place-card:hover::before {
  left: 100%;
}

.mode-card:hover, .place-card:hover {
  transform: translateY(-12px) scale(1.02);
  box-shadow: 0 25px 50px rgba(13, 148, 136, 0.25);
  border-color: var(--teal-600);
  background: linear-gradient(135deg, #f8f9ff 0%, #e3f2fd 100%);
}

.mode-card:active, .place-card:active {
  transform: translateY(-6px) scale(1.01);
  box-shadow: 0 15px 30px rgba(13, 148, 136, 0.3);
}

.mode-card.selected, .place-card.selected {
  border-color: var(--teal-600);
  background: linear-gradient(135deg, var(--teal-50) 0%, var(--cyan-50) 100%);
  transform: translateY(-8px) scale(1.03);
  box-shadow: 0 20px 40px rgba(13, 148, 136, 0.3);
  border-width: 4px;
}

.mode-card.selected:hover, .place-card.selected:hover {
  transform: translateY(-12px) scale(1.05);
  box-shadow: 0 30px 60px rgba(13, 148, 136, 0.4);
  background: linear-gradient(135deg, var(--teal-100) 0%, var(--cyan-100) 100%);
}


.card-content {
  flex: 1;
  display: flex;
  flex-direction: column;
  justify-content: center;
}

.mode-card h4, .place-card h5 {
  margin-bottom: 1rem;
  color: var(--slate-900);
  font-weight: 700;
  font-size: 1.5rem;
  transition: color 0.3s ease;
  position: relative;
  z-index: 2;
}

.mode-card:hover h4, .place-card:hover h5 {
  color: var(--teal-700);
}

.mode-card.selected h4, .place-card.selected h5 {
  color: var(--teal-800);
}

.mode-card p, .place-card p {
  color: var(--slate-700);
  margin-bottom: 1.5rem;
  line-height: 1.6;
  font-size: 1rem;
  transition: color 0.3s ease;
  position: relative;
  z-index: 2;
}

.mode-card:hover p, .place-card:hover p {
  color: var(--teal-600);
}

.mode-card.selected p, .place-card.selected p {
  color: var(--teal-700);
}

.card-features {
  display: flex;
  flex-wrap: wrap;
  gap: 0.5rem;
  justify-content: center;
  margin-bottom: 1rem;
}

.feature-tag {
  background: rgba(13, 148, 136, 0.1);
  color: var(--teal-700);
  padding: 0.25rem 0.75rem;
  border-radius: 1rem;
  font-size: 0.8rem;
  font-weight: 500;
  border: 1px solid rgba(13, 148, 136, 0.2);
}


/* Place Card Error State */
.place-card.has-error {
  border-color: #dc3545;
  background: linear-gradient(135deg, #f8d7da 0%, #f5c6cb 100%);
  animation: shake 0.5s ease-in-out;
}

@keyframes shake {
  0%, 100% { transform: translateX(0); }
  25% { transform: translateX(-5px); }
  75% { transform: translateX(5px); }
}

/* Toast Notifications */
.toast-container {
  position: fixed;
  top: 2rem;
  right: 2rem;
  z-index: 1050;
  max-width: 400px;
}

.toast {
  background: white;
  border-radius: var(--radius-2xl);
  box-shadow: var(--shadow-lg);
  border: 1px solid #e9ecef;
  animation: slideInRight 0.3s ease-out;
}

.toast-error {
  border-left: 4px solid #dc3545;
}

.toast-success {
  border-left: 4px solid #28a745;
}

.toast-info {
  border-left: 4px solid #17a2b8;
}

.toast-header {
  background: transparent;
  border-bottom: 1px solid #e9ecef;
  padding: 1rem 1.5rem 0.5rem;
  display: flex;
  align-items: center;
}

.toast-body {
  padding: 0.5rem 1.5rem 1rem;
  color: var(--slate-700);
  line-height: 1.5;
}

.toast .btn-close {
  background: none;
  border: none;
  font-size: 1.2rem;
  color: #6c757d;
  cursor: pointer;
  padding: 0;
  width: 20px;
  height: 20px;
  display: flex;
  align-items: center;
  justify-content: center;
  transition: all 0.3s ease;
  border-radius: 50%;
}

.toast .btn-close:hover {
  background: #e9ecef;
  color: #333;
  transform: scale(1.2);
}

.toast .btn-close:active {
  background: #dee2e6;
  transform: scale(0.9);
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

/* Enhanced Place Card Styling */
.place-card {
  position: relative;
  transition: all 0.3s ease;
}

.place-card:focus {
  outline: 2px solid var(--teal-600);
  outline-offset: 2px;
}

.place-card:hover {
  transform: translateY(-8px);
  box-shadow: 0 20px 40px rgba(13, 148, 136, 0.15);
  border-color: var(--teal-600);
}

.place-card.selected {
  border-color: var(--teal-600);
  background: linear-gradient(135deg, var(--teal-50) 0%, var(--cyan-50) 100%);
  transform: translateY(-5px);
  box-shadow: 0 20px 40px rgba(13, 148, 136, 0.25);
}

.place-card .card-content {
  flex: 1;
  display: flex;
  flex-direction: column;
  justify-content: center;
  text-align: center;
}

.place-card h5 {
  color: var(--slate-900);
  font-weight: 700;
  font-size: 1.25rem;
  margin-bottom: 0.75rem;
}

.place-card p {
  color: var(--slate-700);
  font-size: 0.9rem;
  line-height: 1.5;
  margin-bottom: 0;
}

.card-badge {
  position: absolute;
  top: 1rem;
  right: 1rem;
  background: #28a745;
  color: white;
  padding: 0.25rem 0.75rem;
  border-radius: 15px;
  font-size: 0.8rem;
  font-weight: 500;
}

.card-badge.emergency {
  background: #dc3545;
}

/* Profile Cards */
.profile-section {
  margin-bottom: 3rem;
}

.profile-card {
  background: white;
  border-radius: 15px;
  padding: 1.5rem;
  cursor: pointer;
  transition: all 0.3s ease;
  border: 2px solid #e9ecef;
  display: flex;
  align-items: center;
  gap: 1rem;
  position: relative;
  overflow: hidden;
}

.profile-card::before {
  content: '';
  position: absolute;
  top: 0;
  left: -100%;
  width: 100%;
  height: 100%;
  background: linear-gradient(90deg, transparent, rgba(0, 123, 255, 0.1), transparent);
  transition: left 0.5s ease;
  z-index: 1;
}

.profile-card:hover::before {
  left: 100%;
}

.profile-card:hover {
  border-color: #007bff;
  transform: translateY(-4px) scale(1.02);
  box-shadow: 0 8px 25px rgba(0, 123, 255, 0.2);
  background: linear-gradient(135deg, #f8f9ff 0%, #e3f2fd 100%);
}

.profile-card:active {
  transform: translateY(-2px) scale(1.01);
  box-shadow: 0 4px 15px rgba(0, 123, 255, 0.3);
}

.profile-card.active {
  border-color: #28a745;
  background: linear-gradient(135deg, #d4edda 0%, #c3e6cb 100%);
  transform: translateY(-3px) scale(1.03);
  box-shadow: 0 6px 20px rgba(40, 167, 69, 0.3);
  border-width: 3px;
}

.profile-card.active:hover {
  transform: translateY(-5px) scale(1.05);
  box-shadow: 0 10px 30px rgba(40, 167, 69, 0.4);
  background: linear-gradient(135deg, #c3e6cb 0%, #a3d9a4 100%);
}


.profile-content {
  flex: 1;
}

.profile-content h5 {
  margin-bottom: 0.5rem;
  color: #333;
  font-weight: 600;
  transition: color 0.3s ease;
  position: relative;
  z-index: 2;
}

.profile-card:hover .profile-content h5 {
  color: #007bff;
}

.profile-card.active .profile-content h5 {
  color: #155724;
}

.profile-content p {
  margin-bottom: 0;
  color: #6c757d;
  font-size: 0.9rem;
  transition: color 0.3s ease;
  position: relative;
  z-index: 2;
}

.profile-card:hover .profile-content p {
  color: #0056b3;
}

.profile-card.active .profile-content p {
  color: #0d4a1a;
}


/* Navigation */
.navigation-section {
  margin-bottom: 3rem;
}

.navigation-buttons {
  display: flex;
  flex-wrap: wrap;
  justify-content: center;
  align-items: center;
  gap: 1rem;
}

.navigation-buttons .btn {
  border-radius: 15px;
  padding: 0.75rem 1.5rem;
  font-weight: 500;
  transition: all 0.3s ease;
  text-decoration: none;
  border: 2px solid transparent;
  position: relative;
  overflow: hidden;
  cursor: pointer;
}

.navigation-buttons .btn::before {
  content: '';
  position: absolute;
  top: 0;
  left: -100%;
  width: 100%;
  height: 100%;
  background: linear-gradient(90deg, transparent, rgba(255,255,255,0.3), transparent);
  transition: left 0.5s;
}

.navigation-buttons .btn:hover::before {
  left: 100%;
}

.navigation-buttons .btn:hover {
  transform: translateY(-3px);
  box-shadow: 0 8px 25px rgba(0,0,0,0.2);
  border-color: var(--teal-600);
}

.navigation-buttons .btn:active {
  transform: translateY(-1px);
  box-shadow: 0 4px 15px rgba(0,0,0,0.3);
}

.navigation-buttons .btn-outline-primary {
  background-color: transparent;
  border-color: #007bff;
  color: #007bff;
}

.navigation-buttons .btn-outline-primary:hover {
  background-color: #007bff;
  border-color: #007bff;
  color: white;
  transform: translateY(-3px) scale(1.05);
}

.navigation-buttons .btn-outline-primary:active {
  background-color: #0056b3;
  border-color: #0056b3;
  transform: translateY(-1px) scale(1.02);
}

.navigation-buttons .btn-outline-secondary {
  background-color: transparent;
  border-color: #6c757d;
  color: #6c757d;
}

.navigation-buttons .btn-outline-secondary:hover {
  background-color: #6c757d;
  border-color: #6c757d;
  color: white;
  transform: translateY(-3px) scale(1.05);
}

.navigation-buttons .btn-outline-secondary:active {
  background-color: #495057;
  border-color: #495057;
  transform: translateY(-1px) scale(1.02);
}

.navigation-buttons .btn-primary {
  background-color: #007bff;
  border-color: #007bff;
  color: white;
}

.navigation-buttons .btn-primary:hover {
  background-color: #0056b3;
  border-color: #0056b3;
  transform: translateY(-3px) scale(1.05);
  box-shadow: 0 8px 25px rgba(0, 123, 255, 0.4);
}

.navigation-buttons .btn-primary:active {
  background-color: #004085;
  border-color: #004085;
  transform: translateY(-1px) scale(1.02);
}

.navigation-buttons .btn-success {
  background-color: #28a745;
  border-color: #28a745;
  color: white;
}

.navigation-buttons .btn-success:hover {
  background-color: #1e7e34;
  border-color: #1e7e34;
  transform: translateY(-3px) scale(1.05);
  box-shadow: 0 8px 25px rgba(40, 167, 69, 0.4);
}

.navigation-buttons .btn-success:active {
  background-color: #155724;
  border-color: #155724;
  transform: translateY(-1px) scale(1.02);
}

/* Loading State */
.loading-section {
  padding: 4rem 0;
}

.loading-spinner {
  max-width: 400px;
  margin: 0 auto;
}

/* Results Section */
.results-section {
  padding: 2rem 0;
  background: #F9FAFB;
  min-height: 100vh;
}

.results-header h2 {
  color: #28a745;
}

/* Action Plan Container */
.action-plan-container {
  background: white;
  border-radius: 20px;
  padding: 2rem;
  box-shadow: 0 8px 25px rgba(0,0,0,0.08);
  border: 1px solid #f8f9fa;
  margin-bottom: 1.5rem;
}

.action-plan-header {
  text-align: center;
  margin-bottom: 2rem;
}

.action-plan-title {
  color: #2c3e50;
  font-weight: 700;
  font-size: 2.2rem;
  margin-bottom: 1rem;
}

.action-plan-subtitle {
  color: #6c757d;
  font-size: 1.2rem;
  font-weight: 500;
  margin-bottom: 2rem;
}

/* Progress Section */
.progress-section {
  margin-bottom: 2rem;
}

.progress-card {
  background: linear-gradient(135deg, #f8f9ff 0%, #e3f2fd 100%);
  border: 2px solid #007bff;
  border-radius: 15px;
  padding: 1.5rem;
  text-align: center;
}

.progress-info {
  display: flex;
  justify-content: space-between;
  align-items: center;
  margin-bottom: 1rem;
}

.progress-stats {
  display: flex;
  flex-direction: column;
  align-items: flex-start;
}

.progress-number {
  font-size: 2.5rem;
  font-weight: 700;
  color: #007bff;
  line-height: 1;
}

.progress-label {
  color: #6c757d;
  font-size: 1rem;
  font-weight: 500;
}

.progress-percentage {
  font-size: 2rem;
  font-weight: 700;
  color: #28a745;
}

.progress-bar-container {
  width: 100%;
  height: 12px;
  background: #e9ecef;
  border-radius: 6px;
  overflow: hidden;
  margin-bottom: 1rem;
}

.progress-bar {
  height: 100%;
  background: linear-gradient(90deg, #007bff 0%, #28a745 100%);
  transition: width 0.3s ease;
}

.progress-message {
  color: #2c3e50;
  font-size: 1.1rem;
  font-weight: 600;
  font-style: italic;
}

/* Enhanced Checklist Cards */
.urgent-actions {
  background: linear-gradient(135deg, #fff3cd 0%, #ffeaa7 100%);
  border-radius: 20px;
  padding: 2rem;
  border: 2px solid #ffc107;
}

.checklist-card {
  background: white;
  border-radius: 20px;
  box-shadow: 0 4px 15px rgba(0,0,0,0.1);
  transition: all 0.3s ease;
  border: 2px solid transparent;
  overflow: hidden;
  margin-bottom: 1rem;
}

.checklist-card:hover {
  transform: translateY(-3px);
  box-shadow: 0 8px 25px rgba(0,0,0,0.15);
}

.checklist-card.completed {
  background: linear-gradient(135deg, #d4edda 0%, #c3e6cb 100%);
  border-color: #28a745;
}

.checklist-card.urgent {
  border-color: #dc3545;
  background: linear-gradient(135deg, #f8d7da 0%, #f5c6cb 100%);
}

.checklist-card.pregnancy {
  border-color: #ffc107;
}

.checklist-card.infant {
  border-color: #17a2b8;
}

.checklist-card.waste {
  border-color: #6c757d;
}

.checklist-card.water {
  border-color: #007bff;
}

.card-header {
  display: flex;
  justify-content: space-between;
  align-items: center;
  padding: 1rem 1.5rem 0.5rem;
}


.item-priority-badge {
  padding: 0.25rem 0.75rem;
  border-radius: 15px;
  font-size: 0.8rem;
  font-weight: 600;
  background: #e9ecef;
  color: #6c757d;
}

.item-priority-badge.urgent {
  background: #dc3545;
  color: white;
}

.item-priority-badge.high {
  background: #fd7e14;
  color: white;
}

.item-priority-badge.medium {
  background: #ffc107;
  color: #212529;
}

.item-priority-badge.low {
  background: #28a745;
  color: white;
}

.card-body {
  display: flex;
  align-items: flex-start;
  gap: 1rem;
  padding: 0.5rem 1.5rem 1.5rem;
}

.item-checkbox {
  flex-shrink: 0;
  margin-top: 0.25rem;
}


.item-content {
  flex: 1;
}

.item-title {
  margin-bottom: 0.5rem;
  color: #333;
  font-weight: 600;
  font-size: 1.1rem;
}

.item-detail {
  margin-bottom: 0.5rem;
  color: #6c757d;
  font-size: 0.9rem;
  line-height: 1.4;
}

/* Source References */
.item-sources {
  margin-top: 0.75rem;
  display: flex;
  flex-wrap: wrap;
  gap: 0.5rem;
  align-items: center;
}

.source-chip {
  display: inline-flex;
  align-items: center;
  padding: 0.25rem 0.75rem;
  background: var(--teal-50);
  color: var(--teal-700);
  text-decoration: none;
  border-radius: 1rem;
  font-size: 0.75rem;
  font-weight: 500;
  border: 1px solid var(--teal-200);
  transition: all 0.2s ease;
  line-height: 1.2;
}

.source-chip:hover {
  background: var(--teal-100);
  color: var(--teal-800);
  text-decoration: underline;
  transform: translateY(-1px);
  box-shadow: 0 2px 4px rgba(13, 148, 136, 0.1);
}

.source-chip:focus {
  outline: 2px solid var(--teal-600);
  outline-offset: 2px;
}

/* Brand-specific source chip colors */
.source-chip[href*="who.int"] {
  background: #e3f2fd;
  color: #1976d2;
  border-color: #bbdefb;
}

.source-chip[href*="who.int"]:hover {
  background: #bbdefb;
  color: #0d47a1;
}

.source-chip[href*="cdc.gov"] {
  background: #f3e5f5;
  color: #7b1fa2;
  border-color: #e1bee7;
}

.source-chip[href*="cdc.gov"]:hover {
  background: #e1bee7;
  color: #4a148c;
}

.source-chip[href*="health.gov"] {
  background: #e8f5e8;
  color: #2e7d32;
  border-color: #c8e6c9;
}

.source-chip[href*="health.gov"]:hover {
  background: #c8e6c9;
  color: #1b5e20;
}

/* Category Groups */
.category-group {
  background: white;
  border-radius: 20px;
  padding: 1.5rem;
  box-shadow: 0 2px 10px rgba(0,0,0,0.1);
}

.category-header {
  display: flex;
  justify-content: space-between;
  align-items: center;
  margin-bottom: 1rem;
  padding-bottom: 1rem;
  border-bottom: 2px solid #e9ecef;
}

.category-title {
  display: flex;
  align-items: center;
  gap: 0.5rem;
  margin-bottom: 0;
  color: #333;
  font-weight: 600;
}

.category-icon {
  font-size: 1.5rem;
}

.category-progress {
  display: flex;
  align-items: center;
  gap: 0.5rem;
}

.category-progress .progress {
  width: 100px;
  height: 8px;
}

.category-items {
  display: flex;
  flex-direction: column;
  gap: 1rem;
}

/* Why Modal */
.why-content {
  text-align: center;
}

.why-explanation {
  background: linear-gradient(135deg, #e3f2fd 0%, #bbdefb 100%);
  border-radius: 15px;
  padding: 2rem;
  margin-bottom: 1rem;
}

.why-explanation h6 {
  color: #1976d2;
  font-weight: 600;
}

.why-explanation .lead {
  color: #333;
  font-size: 1.1rem;
  line-height: 1.6;
}

.why-sources {
  text-align: left;
}

.why-sources h6 {
  color: #333;
  font-weight: 600;
  margin-bottom: 0.5rem;
}

.why-sources a {
  color: #007bff;
  text-decoration: none;
}

.why-sources a:hover {
  text-decoration: underline;
}

/* Chat Bot Styles */

.chat-drawer {
  position: fixed;
  bottom: 2rem;
  right: 2rem;
  width: 350px;
  height: 500px;
  background: white;
  border-radius: var(--radius-2xl);
  box-shadow: var(--shadow-lg);
  display: flex;
  flex-direction: column;
  z-index: 1001;
  border: 1px solid var(--teal-100);
}

.chat-header {
  padding: 1rem 1.5rem;
  border-bottom: 1px solid var(--teal-100);
  display: flex;
  justify-content: space-between;
  align-items: center;
  background: var(--teal-50);
  border-radius: var(--radius-2xl) var(--radius-2xl) 0 0;
}

.chat-header h6 {
  margin: 0;
  color: var(--slate-900);
  font-weight: 600;
}

.chat-messages {
  flex: 1;
  padding: 1rem;
  overflow-y: auto;
  display: flex;
  flex-direction: column;
  gap: 1rem;
}

.chat-message {
  display: flex;
  flex-direction: column;
  max-width: 80%;
}

.chat-message.user {
  align-self: flex-end;
}

.chat-message.assistant {
  align-self: flex-start;
}

.message-content {
  background: var(--teal-50);
  padding: 0.75rem 1rem;
  border-radius: 1rem;
  border-bottom-left-radius: 0.25rem;
}

.chat-message.user .message-content {
  background: var(--teal-600);
  color: white;
  border-bottom-left-radius: 1rem;
  border-bottom-right-radius: 0.25rem;
}

.message-content p {
  margin: 0;
  font-size: 0.9rem;
  line-height: 1.4;
}

.message-sources {
  margin-top: 0.5rem;
  display: flex;
  flex-wrap: wrap;
  gap: 0.25rem;
}

.source-chip {
  background: rgba(255, 255, 255, 0.2);
  padding: 0.2rem 0.5rem;
  border-radius: 0.5rem;
  font-size: 0.7rem;
}

.source-chip a {
  color: inherit;
  text-decoration: none;
}

.message-time {
  color: var(--slate-700);
  font-size: 0.7rem;
  margin-top: 0.25rem;
  align-self: flex-end;
}

.chat-message.user .message-time {
  align-self: flex-start;
}

.typing-indicator {
  display: flex;
  gap: 0.25rem;
  align-items: center;
}

.typing-indicator span {
  width: 6px;
  height: 6px;
  background: var(--teal-600);
  animation: typing 1.4s infinite ease-in-out;
}

.typing-indicator span:nth-child(2) {
  animation-delay: 0.2s;
}

.typing-indicator span:nth-child(3) {
  animation-delay: 0.4s;
}

@keyframes typing {
  0%, 60%, 100% {
    transform: translateY(0);
  }
  30% {
    transform: translateY(-10px);
  }
}

.chat-input {
  padding: 1rem 1.5rem;
  border-top: 1px solid var(--teal-100);
  background: white;
  border-radius: 0 0 var(--radius-2xl) var(--radius-2xl);
}

.chat-input .form-control {
  border: 1px solid var(--teal-200);
  border-radius: 1rem;
  padding: 0.5rem 1rem;
  font-size: 0.9rem;
}

.chat-input .form-control:focus {
  border-color: var(--teal-600);
  box-shadow: 0 0 0 0.2rem rgba(13, 148, 136, 0.25);
}

.chat-input .btn {
  width: 40px;
  height: 40px;
  padding: 0;
  display: flex;
  align-items: center;
  justify-content: center;
  border-radius: 50%;
  transition: all 0.3s ease;
  cursor: pointer;
}

.chat-input .btn:hover {
  transform: scale(1.1);
  box-shadow: 0 4px 15px rgba(0, 123, 255, 0.4);
}

.chat-input .btn:active {
  transform: scale(0.95);
  box-shadow: 0 2px 8px rgba(0, 123, 255, 0.6);
}


/* Checklist Header */
.checklist-title-section h4 {
  color: #333;
  font-weight: 700;
}

.progress-container {
  background: #f8f9fa;
  border-radius: 10px;
  padding: 1rem;
}

.progress-stats {
  display: flex;
  align-items: center;
  justify-content: space-between;
  font-size: 0.9rem;
}

.completion-percentage {
  font-size: 1.1rem;
}

/* Section Headers */
.section-header {
  text-align: center;
  margin-bottom: 2rem;
}

.section-title {
  color: #2c3e50;
  font-weight: 700;
  font-size: 1.8rem;
  margin-bottom: 0.5rem;
}

.section-subtitle {
  color: #6c757d;
  font-size: 1.1rem;
  font-weight: 500;
  margin-bottom: 0;
}

/* Priority Actions Section */
.priority-actions-section {
  margin: 3rem 0;
}

.priority-cards {
  display: flex;
  flex-direction: column;
  gap: 1.5rem;
}

.priority-card {
  background: white;
  border-radius: 20px;
  padding: 2rem;
  box-shadow: 0 4px 12px rgba(0,0,0,0.05);
  border: 2px solid #f8f9fa;
  transition: all 0.3s ease;
}

.priority-card:hover {
  transform: translateY(-3px);
  box-shadow: 0 8px 25px rgba(0,0,0,0.1);
}

.priority-card.urgency-critical {
  border-color: #dc3545;
  background: linear-gradient(135deg, #fff5f5 0%, #ffeaea 100%);
}

.priority-card.urgency-high {
  border-color: #fd7e14;
  background: linear-gradient(135deg, #fff8f0 0%, #ffe8d1 100%);
}

.priority-card.urgency-medium {
  border-color: #ffc107;
  background: linear-gradient(135deg, #fffdf0 0%, #fff8e1 100%);
}

.priority-card.urgency-low {
  border-color: #28a745;
  background: linear-gradient(135deg, #f8fff8 0%, #e8f5e8 100%);
}

.priority-card.completed {
  background: linear-gradient(135deg, #e8f5e8 0%, #d4edda 100%);
  border-color: #28a745;
  opacity: 0.9;
}

.priority-card.completed .card-title {
  text-decoration: line-through;
  color: #6c757d;
}

.priority-card.completed .card-description {
  color: #6c757d;
}

.card-header {
  display: flex;
  justify-content: space-between;
  align-items: center;
  margin-bottom: 1rem;
}

.priority-badge {
  padding: 0.5rem 1rem;
  border-radius: 15px;
  font-size: 0.9rem;
  font-weight: 600;
  text-transform: uppercase;
  letter-spacing: 0.5px;
}

.priority-badge.urgency-critical {
  background: #dc3545;
  color: white;
}

.priority-badge.urgency-high {
  background: #fd7e14;
  color: white;
}

.priority-badge.urgency-medium {
  background: #ffc107;
  color: #212529;
}

.priority-badge.urgency-low {
  background: #28a745;
  color: white;
}

.card-checkbox {
  flex-shrink: 0;
}

.modern-checkbox {
  width: 24px;
  height: 24px;
  border: 2px solid #dee2e6;
  background: white;
  cursor: pointer;
  transition: all 0.3s ease;
  border-radius: 4px;
  appearance: none;
  -webkit-appearance: none;
  -moz-appearance: none;
  position: relative;
  flex-shrink: 0;
}

.modern-checkbox:hover {
  border-color: #007bff;
  box-shadow: 0 0 0 2px rgba(0, 123, 255, 0.1);
}

.modern-checkbox:checked {
  background: #28a745;
  border-color: #28a745;
  box-shadow: 0 0 0 2px rgba(40, 167, 69, 0.2);
}

.modern-checkbox:checked::after {
  content: '✓';
  position: absolute;
  top: 50%;
  left: 50%;
  transform: translate(-50%, -50%);
  color: white;
  font-size: 14px;
  font-weight: bold;
  line-height: 1;
  text-shadow: 0 1px 2px rgba(0, 0, 0, 0.2);
}

.modern-checkbox:focus {
  outline: none;
  box-shadow: 0 0 0 3px rgba(0, 123, 255, 0.25);
}

.modern-checkbox:checked:focus {
  box-shadow: 0 0 0 3px rgba(40, 167, 69, 0.25);
}

.card-content {
  flex: 1;
}

.card-title {
  color: #2c3e50;
  font-weight: 700;
  font-size: 1.3rem;
  margin-bottom: 0.75rem;
  line-height: 1.3;
}

.card-description {
  color: #6c757d;
  font-size: 1rem;
  line-height: 1.5;
  margin-bottom: 1rem;
}

.card-actions {
  display: flex;
  flex-wrap: wrap;
  gap: 1rem;
  align-items: center;
}

.learn-more-btn {
  background: transparent;
  border: 2px solid #007bff;
  color: #007bff;
  padding: 0.5rem 1rem;
  border-radius: 10px;
  font-size: 0.9rem;
  font-weight: 600;
  cursor: pointer;
  transition: all 0.2s ease;
}

.learn-more-btn:hover {
  background: #007bff;
  color: white;
}

.source-badges {
  display: flex;
  flex-wrap: wrap;
  gap: 0.5rem;
}

.source-badge {
  display: inline-flex;
  align-items: center;
  padding: 0.4rem 0.8rem;
  background: rgba(0, 123, 255, 0.1);
  color: #007bff;
  border-radius: 12px;
  font-size: 0.8rem;
  font-weight: 500;
  cursor: pointer;
  transition: all 0.2s ease;
  border: 1px solid rgba(0, 123, 255, 0.2);
}

.source-badge:hover {
  background: rgba(0, 123, 255, 0.15);
  color: #0056b3;
  transform: translateY(-1px);
}

/* Expand Section */
.expand-section {
  margin: 2rem 0;
}

.expand-card {
  background: linear-gradient(135deg, #f8f9ff 0%, #e3f2fd 100%);
  border: 2px solid #007bff;
  border-radius: 20px;
  padding: 2rem;
  display: flex;
  justify-content: space-between;
  align-items: center;
  transition: all 0.3s ease;
}

.expand-card:hover {
  transform: translateY(-3px);
  box-shadow: 0 8px 25px rgba(0, 123, 255, 0.15);
}

.expand-content {
  flex: 1;
}

.expand-title {
  color: #2c3e50;
  font-weight: 700;
  font-size: 1.3rem;
  margin-bottom: 0.5rem;
}

.expand-description {
  color: #6c757d;
  font-size: 1rem;
  margin-bottom: 0;
}

.expand-btn {
  background: linear-gradient(135deg, #007bff 0%, #0056b3 100%);
  color: white;
  border: none;
  border-radius: 15px;
  padding: 1rem 2rem;
  font-weight: 600;
  font-size: 1rem;
  cursor: pointer;
  transition: all 0.3s ease;
  box-shadow: 0 4px 15px rgba(0, 123, 255, 0.3);
  position: relative;
  overflow: hidden;
}

.expand-btn::before {
  content: '';
  position: absolute;
  top: 0;
  left: -100%;
  width: 100%;
  height: 100%;
  background: linear-gradient(90deg, transparent, rgba(255,255,255,0.2), transparent);
  transition: left 0.5s;
}

.expand-btn:hover::before {
  left: 100%;
}

.expand-btn:hover {
  background: linear-gradient(135deg, #0056b3 0%, #004085 100%);
  transform: translateY(-3px) scale(1.05);
  box-shadow: 0 8px 25px rgba(0, 123, 255, 0.5);
}

.expand-btn:active {
  background: linear-gradient(135deg, #004085 0%, #003366 100%);
  transform: translateY(-1px) scale(1.02);
  box-shadow: 0 4px 15px rgba(0, 123, 255, 0.6);
}

/* Complete Checklist */
.complete-checklist {
  margin-top: 2rem;
}

/* Category Sections */
.category-section {
  background: white;
  border-radius: 20px;
  padding: 2rem;
  box-shadow: 0 4px 12px rgba(0,0,0,0.05);
  border: 1px solid #f8f9fa;
  margin-bottom: 2rem;
}

.category-header {
  display: flex;
  justify-content: space-between;
  align-items: flex-start;
  margin-bottom: 2rem;
  padding-bottom: 1.5rem;
  border-bottom: 2px solid #f8f9fa;
}

.category-info {
  display: flex;
  align-items: center;
  gap: 1rem;
  flex: 1;
}

.category-icon {
  font-size: 2rem;
  width: 60px;
  height: 60px;
  display: flex;
  align-items: center;
  justify-content: center;
  background: linear-gradient(135deg, #f8f9ff 0%, #e3f2fd 100%);
  border-radius: 15px;
  border: 2px solid #007bff;
}

.category-details {
  flex: 1;
}

.category-title {
  color: #2c3e50;
  font-weight: 700;
  font-size: 1.4rem;
  margin-bottom: 0.5rem;
}

.category-description {
  color: #6c757d;
  font-size: 1rem;
  margin-bottom: 0;
}

.category-progress {
  display: flex;
  flex-direction: column;
  align-items: flex-end;
  gap: 0.5rem;
}

.progress-info {
  display: flex;
  align-items: center;
  gap: 1rem;
}

.progress-count {
  color: #2c3e50;
  font-weight: 600;
  font-size: 1.1rem;
}

.progress-percentage {
  color: #28a745;
  font-weight: 700;
  font-size: 1.2rem;
}

.category-items {
  display: flex;
  flex-direction: column;
  gap: 1.5rem;
}

.action-card {
  background: white;
  border-radius: 15px;
  padding: 1.5rem;
  box-shadow: 0 2px 8px rgba(0,0,0,0.05);
  border: 1px solid #f8f9fa;
  transition: all 0.3s ease;
}

.action-card:hover {
  transform: translateY(-2px);
  box-shadow: 0 4px 15px rgba(0,0,0,0.1);
}

.action-card.completed {
  background: linear-gradient(135deg, #f8fff8 0%, #e8f5e8 100%);
  border-color: #28a745;
  opacity: 0.9;
}

.action-card.completed .card-title {
  text-decoration: line-through;
  color: #6c757d;
}

.action-card.completed .card-description {
  color: #6c757d;
}

/* Complete Checklist */
.complete-header h5 {
  color: #333;
  font-weight: 700;
}

/* Category Sections */
.category-section {
  background: white;
  border-radius: 15px;
  padding: 1.5rem;
  box-shadow: 0 2px 10px rgba(0, 0, 0, 0.08);
  border: 1px solid #e9ecef;
}

.category-header {
  display: flex;
  justify-content: space-between;
  align-items: flex-start;
  margin-bottom: 1.5rem;
  padding-bottom: 1rem;
  border-bottom: 2px solid #f8f9fa;
}

.category-info {
  flex: 1;
}

.category-title {
  color: #333;
  font-weight: 600;
  margin-bottom: 0.25rem;
}

.category-description {
  color: #6c757d;
  font-size: 0.9rem;
  margin-bottom: 0;
}

.category-progress {
  display: flex;
  flex-direction: column;
  align-items: flex-end;
  gap: 0.5rem;
}

.category-progress .progress {
  width: 120px;
  height: 8px;
  background: #e9ecef;
  border-radius: 4px;
}

.progress-text {
  font-size: 0.85rem;
}

.category-items {
  display: flex;
  flex-direction: column;
  gap: 1rem;
}

/* Quick Actions Panel */
.quick-actions-panel {
  background: white;
  border-radius: 20px;
  padding: 2rem;
  box-shadow: 0 4px 12px rgba(0,0,0,0.05);
  border: 1px solid #f8f9fa;
  height: fit-content;
  position: sticky;
  top: 2rem;
}

.panel-header {
  text-align: center;
  margin-bottom: 2rem;
  padding-bottom: 1.5rem;
  border-bottom: 2px solid #f8f9fa;
}

.panel-title {
  color: #2c3e50;
  font-weight: 700;
  font-size: 1.4rem;
  margin-bottom: 0.5rem;
}

.panel-subtitle {
  color: #6c757d;
  font-size: 1rem;
  margin-bottom: 0;
}

.action-buttons {
  display: flex;
  flex-direction: column;
  gap: 1rem;
  margin-bottom: 2rem;
}

.action-button {
  display: flex;
  align-items: center;
  gap: 1rem;
  padding: 1rem 1.5rem;
  border-radius: 15px;
  font-size: 1rem;
  font-weight: 600;
  text-decoration: none;
  transition: all 0.3s ease;
  cursor: pointer;
  border: 2px solid transparent;
  position: relative;
  overflow: hidden;
}

.action-button::before {
  content: '';
  position: absolute;
  top: 0;
  left: -100%;
  width: 100%;
  height: 100%;
  background: linear-gradient(90deg, transparent, rgba(255,255,255,0.2), transparent);
  transition: left 0.5s;
}

.action-button:hover::before {
  left: 100%;
}

.action-button.primary {
  background: linear-gradient(135deg, #007bff 0%, #0056b3 100%);
  color: white;
  box-shadow: 0 4px 15px rgba(0, 123, 255, 0.3);
}

.action-button.primary:hover {
  transform: translateY(-3px) scale(1.05);
  box-shadow: 0 8px 25px rgba(0, 123, 255, 0.5);
  text-decoration: none;
  color: white;
  background: linear-gradient(135deg, #0056b3 0%, #004085 100%);
}

.action-button.primary:active {
  transform: translateY(-1px) scale(1.02);
  box-shadow: 0 4px 15px rgba(0, 123, 255, 0.6);
  background: linear-gradient(135deg, #004085 0%, #003366 100%);
}

.action-button.secondary {
  background: linear-gradient(135deg, #28a745 0%, #1e7e34 100%);
  color: white;
  box-shadow: 0 4px 15px rgba(40, 167, 69, 0.3);
}

.action-button.secondary:hover {
  transform: translateY(-3px) scale(1.05);
  box-shadow: 0 8px 25px rgba(40, 167, 69, 0.5);
  text-decoration: none;
  color: white;
  background: linear-gradient(135deg, #1e7e34 0%, #155724 100%);
}

.action-button.secondary:active {
  transform: translateY(-1px) scale(1.02);
  box-shadow: 0 4px 15px rgba(40, 167, 69, 0.6);
  background: linear-gradient(135deg, #155724 0%, #0d4a1a 100%);
}

.action-button.tertiary {
  background: linear-gradient(135deg, #6c757d 0%, #495057 100%);
  color: white;
  box-shadow: 0 4px 15px rgba(108, 117, 125, 0.3);
}

.action-button.tertiary:hover {
  transform: translateY(-3px) scale(1.05);
  box-shadow: 0 8px 25px rgba(108, 117, 125, 0.5);
  text-decoration: none;
  color: white;
  background: linear-gradient(135deg, #495057 0%, #343a40 100%);
}

.action-button.tertiary:active {
  transform: translateY(-1px) scale(1.02);
  box-shadow: 0 4px 15px rgba(108, 117, 125, 0.6);
  background: linear-gradient(135deg, #343a40 0%, #212529 100%);
}

.action-button i {
  width: 20px;
  text-align: center;
  font-size: 1.1rem;
}

/* Progress Summary */
.progress-summary {
  background: linear-gradient(135deg, #f8f9ff 0%, #e3f2fd 100%);
  border: 2px solid #007bff;
  border-radius: 15px;
  padding: 1.5rem;
}

.summary-title {
  color: #2c3e50;
  font-weight: 700;
  font-size: 1.2rem;
  margin-bottom: 1rem;
  text-align: center;
}

.summary-stats {
  display: flex;
  justify-content: space-around;
  margin-bottom: 1.5rem;
}

.stat-item {
  text-align: center;
}

.stat-number {
  display: block;
  font-size: 1.8rem;
  font-weight: 700;
  color: #007bff;
  line-height: 1;
  margin-bottom: 0.25rem;
}

.stat-label {
  color: #6c757d;
  font-size: 0.9rem;
  font-weight: 500;
}

.summary-progress {
  text-align: center;
}

.summary-progress .progress-bar-container {
  width: 100%;
  height: 10px;
  background: #e9ecef;
  border-radius: 5px;
  overflow: hidden;
  margin-bottom: 0.5rem;
}

.summary-progress .progress-bar {
  height: 100%;
  background: linear-gradient(90deg, #007bff 0%, #28a745 100%);
  transition: width 0.3s ease;
}

.progress-text {
  color: #2c3e50;
  font-size: 1rem;
  font-weight: 600;
}






/* Responsive Design */
@media (max-width: 768px) {
  .hero-section {
    min-height: 50vh;
  }
  
  .hero-title {
    font-size: 2rem;
  }
  
  .hero-subtitle {
    font-size: 1rem;
  }
  
  .progress-steps {
    flex-direction: column;
    gap: 1rem;
  }
  
  .step-line {
    width: 3px;
    height: 50px;
    margin: 0;
  }
  
  .mode-card, .place-card {
    padding: 1.5rem;
  }
  
  .card-icon {
    width: 60px;
    height: 60px;
    font-size: 1.5rem;
  }
  
  .checklist-container, .quick-actions {
    padding: 1.5rem;
  }
  
  .navigation-buttons {
    flex-direction: column;
    gap: 0.5rem;
  }
  
  .navigation-buttons .btn {
    width: 100%;
    margin-bottom: 0.5rem;
  }
  
  .chat-drawer {
    width: 100%;
    height: 70vh;
    bottom: 0;
    right: 0;
    border-radius: var(--radius-2xl) var(--radius-2xl) 0 0;
  }
  
  .floating-chat-button {
    bottom: 1rem;
    right: 1rem;
  }
  
  .toast-container {
    top: 1rem;
    right: 1rem;
    left: 1rem;
    max-width: none;
  }
  
  .micro-flow-modal {
    margin: 1rem;
    max-width: none;
  }
  
  .timer-circle {
    width: 150px;
    height: 150px;
  }
  
  .timer-text {
    width: 120px;
    height: 120px;
  }
  
  .timer-seconds {
    font-size: 2rem;
  }
  
  /* Mobile source chips */
  .item-sources {
    margin-top: 0.5rem;
    gap: 0.375rem;
  }
  
  .source-chip {
    font-size: 0.7rem;
    padding: 0.2rem 0.6rem;
  }
  
  .message-sources {
    margin-top: 0.375rem;
    gap: 0.25rem;
  }
  
  .message-sources .source-chip {
    font-size: 0.65rem;
    padding: 0.15rem 0.5rem;
  }
}

/* Print Styles */
@media print {
  .sanitation-support {
    background: white;
  }
  
  .header-section {
    background: white;
    color: black;
    border-bottom: 2px solid #333;
  }
  
  .progress-section, .navigation-section, .quick-actions {
    display: none;
  }
  
  .checklist-item {
    break-inside: avoid;
    background: white;
    border: 1px solid #333;
  }
  
  .checklist-item.completed {
    background: #f0f0f0;
  }
}
</style>


