import { defineStore } from 'pinia'
import { ref, computed } from 'vue'

export const useMaternalInfantStore = defineStore('maternalInfant', () => {
  // State
  const userType = ref('') // 'expecting' or 'baby'
  const hasSelectedUserType = ref(false)
  const showUserSelectionModal = ref(false)

  // Getters
  const isExpecting = computed(() => userType.value === 'expecting')
  const hasBaby = computed(() => userType.value === 'baby')
  const userTypeLabel = computed(() => {
    switch (userType.value) {
      case 'expecting': return 'I\'m expecting'
      case 'baby': return 'My little one'
      default: return ''
    }
  })

  // Actions
  const setUserType = (type) => {
    userType.value = type
    hasSelectedUserType.value = true
    showUserSelectionModal.value = false
    
    // Save to localStorage
    localStorage.setItem('maternalInfantUserType', type)
    localStorage.setItem('maternalInfantHasSelected', 'true')
  }

  const loadUserType = () => {
    const savedType = localStorage.getItem('maternalInfantUserType')
    const hasSelected = localStorage.getItem('maternalInfantHasSelected')
    
    if (savedType && hasSelected === 'true') {
      userType.value = savedType
      hasSelectedUserType.value = true
    } else {
      showUserSelectionModal.value = true
    }
  }

  const changeUserType = () => {
    showUserSelectionModal.value = true
  }

  const resetUserType = () => {
    userType.value = ''
    hasSelectedUserType.value = false
    showUserSelectionModal.value = true
    localStorage.removeItem('maternalInfantUserType')
    localStorage.removeItem('maternalInfantHasSelected')
  }

  return {
    // State
    userType,
    hasSelectedUserType,
    showUserSelectionModal,
    
    // Getters
    isExpecting,
    hasBaby,
    userTypeLabel,
    
    // Actions
    setUserType,
    loadUserType,
    changeUserType,
    resetUserType
  }
})
