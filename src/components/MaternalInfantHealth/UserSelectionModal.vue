<template>
  <div v-if="showModal" class="modal-overlay" @click="closeModal">
    <div class="modal-content" @click.stop>
      <div class="modal-header">
        <h2 class="modal-title">
          <i class="fas fa-heart me-2"></i>
          Welcome to Your Health Hub
        </h2>
        <p class="modal-subtitle">
          Let's personalize your experience to provide the most relevant guidance
        </p>
      </div>

      <div class="selection-cards">
        <div 
          class="selection-card" 
          :class="{ selected: selectedCard === 'expecting' }"
          @click="selectUserType('expecting')"
        >
          <div class="card-icon">🤱</div>
          <h3 class="card-title">I'm expecting</h3>
          <p class="card-subtitle">Get personalized guidance for your pregnancy journey</p>
          <div class="card-features">
            <p>• Trimester-specific hydration advice</p>
            <p>• Pregnancy health monitoring</p>
            <p>• Safe water practices</p>
          </div>
        </div>
        
        <div 
          class="selection-card" 
          :class="{ selected: selectedCard === 'baby' }"
          @click="selectUserType('baby')"
        >
          <div class="card-icon">👶</div>
          <h3 class="card-title">My little one</h3>
          <p class="card-subtitle">Get age-specific guidance for your baby's health</p>
          <div class="card-features">
            <p>• Age-appropriate feeding schedules</p>
            <p>• Baby health monitoring</p>
            <p>• Safe formula preparation</p>
          </div>
        </div>
      </div>

      <div class="modal-footer">
        <p class="privacy-note">
          <i class="fas fa-shield-alt me-2"></i>
          Your selection is saved locally and can be changed anytime
        </p>
      </div>
    </div>
  </div>
</template>

<script setup>
import { ref, computed } from 'vue'
import { useMaternalInfantStore } from '@/stores/maternalInfantStore'

const store = useMaternalInfantStore()
const selectedCard = ref('')

const showModal = computed(() => store.showUserSelectionModal)

const selectUserType = (type) => {
  selectedCard.value = type
  setTimeout(() => {
    store.setUserType(type)
    selectedCard.value = ''
  }, 300)
}

const closeModal = () => {
  // Don't allow closing without selection
  if (!store.hasSelectedUserType) {
    return
  }
  store.showUserSelectionModal = false
}
</script>

<style scoped>
.modal-overlay {
  position: fixed;
  top: 0;
  left: 0;
  right: 0;
  bottom: 0;
  background: rgba(0, 0, 0, 0.7);
  display: flex;
  align-items: center;
  justify-content: center;
  z-index: 9999;
  padding: 1rem;
}

.modal-content {
  background: white;
  border-radius: 25px;
  padding: 3rem;
  max-width: 800px;
  width: 100%;
  max-height: 90vh;
  overflow-y: auto;
  box-shadow: 0 20px 60px rgba(0, 0, 0, 0.3);
  animation: modalSlideIn 0.3s ease-out;
}

@keyframes modalSlideIn {
  from {
    opacity: 0;
    transform: translateY(-50px) scale(0.9);
  }
  to {
    opacity: 1;
    transform: translateY(0) scale(1);
  }
}

.modal-header {
  text-align: center;
  margin-bottom: 2rem;
}

.modal-title {
  color: #2c3e50;
  font-weight: 700;
  font-size: 2rem;
  margin-bottom: 1rem;
}

.modal-subtitle {
  color: #6c757d;
  font-size: 1.1rem;
  margin-bottom: 0;
}

.selection-cards {
  display: grid;
  grid-template-columns: repeat(auto-fit, minmax(300px, 1fr));
  gap: 2rem;
  margin-bottom: 2rem;
}

.selection-card {
  background: white;
  border: 3px solid #e9ecef;
  border-radius: 20px;
  padding: 2rem;
  text-align: center;
  cursor: pointer;
  transition: all 0.3s ease;
  box-shadow: 0 4px 15px rgba(0, 0, 0, 0.1);
}

.selection-card:hover {
  transform: translateY(-5px);
  box-shadow: 0 8px 25px rgba(0, 0, 0, 0.15);
  border-color: #007bff;
}

.selection-card.selected {
  border-color: #28a745;
  background: linear-gradient(135deg, #f8fff9 0%, #e8f5e8 100%);
  transform: translateY(-5px);
  box-shadow: 0 8px 25px rgba(40, 167, 69, 0.2);
}

.card-icon {
  font-size: 3rem;
  margin-bottom: 1rem;
}

.card-title {
  color: #2c3e50;
  font-weight: 700;
  font-size: 1.5rem;
  margin-bottom: 0.5rem;
}

.card-subtitle {
  color: #6c757d;
  margin-bottom: 1rem;
}

.card-features p {
  margin: 0.5rem 0;
  color: #495057;
  font-size: 0.95rem;
}

.modal-footer {
  text-align: center;
  padding-top: 1rem;
  border-top: 1px solid #e9ecef;
}

.privacy-note {
  color: #6c757d;
  font-size: 0.9rem;
  margin: 0;
  display: flex;
  align-items: center;
  justify-content: center;
}

/* Responsive Design */
@media (max-width: 768px) {
  .modal-content {
    padding: 2rem;
    margin: 1rem;
  }
  
  .modal-title {
    font-size: 1.5rem;
  }
  
  .selection-cards {
    grid-template-columns: 1fr;
    gap: 1rem;
  }
  
  .selection-card {
    padding: 1.5rem;
  }
}
</style>
