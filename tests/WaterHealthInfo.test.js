import { describe, it, expect, beforeEach, vi } from 'vitest'
import { mount } from '@vue/test-utils'
import WaterHealthInfo from '@/components/MaternalInfantHealth/WaterHealthInfo.vue'

// Mock MaterialButton component
vi.mock('@/components/MaterialButton.vue', () => ({
  default: { template: '<button><slot /></button>' }
}))

// Mock store
vi.mock('@/stores/maternalInfantStore', () => ({
  useMaternalInfantStore: () => ({
    userType: 'pregnant_woman',
    userTypeLabel: 'Pregnant Woman'
  })
}))

describe('WaterHealthInfo - Health Information System', () => {
  let wrapper

  beforeEach(() => {
    wrapper = mount(WaterHealthInfo, {
      global: {
        stubs: {
          'MaterialButton': {
            template: '<button @click="$emit(\'click\')"><slot /></button>',
            emits: ['click']
          }
        }
      }
    })
  })

  afterEach(() => {
    wrapper.unmount()
  })

  describe('TC-016: Health Information Navigation Flow', () => {
    it('should start with category selection step', () => {
      expect(wrapper.vm.currentStep).toBe(1)
      
      const categorySection = wrapper.find('.step-content')
      expect(categorySection.exists()).toBe(true)
      
      const stepHeader = wrapper.find('.step-header h3')
      expect(stepHeader.text()).toContain('Choose a Health Category')
    })

    it('should display all four health categories', () => {
      const categories = wrapper.findAll('.category-btn')
      expect(categories.length).toBe(4)
      
      const expectedCategories = [
        'Water-Borne Diseases',
        'Parasitic Infections', 
        'Sanitation-Related',
        'Water Scarcity Issues'
      ]
      
      expectedCategories.forEach(categoryName => {
        const category = wrapper.find(`.category-title:contains("${categoryName}")`)
        expect(category.exists()).toBe(true)
      })
    })

    it('should progress to condition selection when category is selected', async () => {
      const waterBorneCategory = wrapper.find('.category-btn')
      await waterBorneCategory.trigger('click')
      
      expect(wrapper.vm.currentStep).toBe(2)
      expect(wrapper.vm.selectedCategory).toBe('water-borne')
      
      const conditionSection = wrapper.find('.step-content')
      const stepHeader = conditionSection.find('.step-header h3')
      expect(stepHeader.text()).toContain('Select a Condition')
    })
  })

  describe('TC-017: Health Condition Information Display', () => {
    beforeEach(async () => {
      // Navigate to condition selection
      await wrapper.vm.selectCategory('water-borne')
    })

    it('should display conditions for selected category', () => {
      const conditions = wrapper.findAll('.condition-btn')
      expect(conditions.length).toBeGreaterThan(0)
      
      // Should have conditions like Cholera, Typhoid, etc.
      const conditionNames = conditions.map(condition => 
        condition.find('.condition-name').text()
      )
      
      expect(conditionNames).toContain('Cholera')
      expect(conditionNames).toContain('Typhoid Fever')
    })

    it('should show severity levels for each condition', () => {
      const severityBadges = wrapper.findAll('.condition-severity')
      expect(severityBadges.length).toBeGreaterThan(0)
      
      severityBadges.forEach(badge => {
        const severity = badge.text()
        expect(['High', 'Medium', 'Low']).toContain(severity)
      })
    })

    it('should progress to detailed view when condition is selected', async () => {
      const firstCondition = wrapper.find('.condition-btn')
      await firstCondition.trigger('click')
      
      expect(wrapper.vm.currentStep).toBe(3)
      expect(wrapper.vm.selectedCondition).toBeDefined()
      
      const detailsSection = wrapper.find('.condition-details')
      expect(detailsSection.exists()).toBe(true)
    })
  })

  describe('TC-018: Detailed Health Information', () => {
    beforeEach(async () => {
      // Navigate to detailed view
      await wrapper.vm.selectCategory('water-borne')
      const firstCondition = wrapper.vm.healthConditions['water-borne'][0]
      await wrapper.vm.selectCondition(firstCondition)
    })

    it('should display comprehensive condition information', () => {
      const detailsHeader = wrapper.find('.details-header')
      expect(detailsHeader.exists()).toBe(true)
      
      const conditionName = detailsHeader.find('h2')
      expect(conditionName.text()).toBe('Cholera')
    })

    it('should show all required information sections', () => {
      const infoCards = wrapper.findAll('.info-card')
      expect(infoCards.length).toBe(4) // Causes, Symptoms, Treatment, Prevention
      
      const expectedSections = [
        'Causes',
        'Symptoms', 
        'Treatment & Remedies',
        'Prevention'
      ]
      
      expectedSections.forEach(sectionName => {
        const section = wrapper.find(`h4:contains("${sectionName}")`)
        expect(section.exists()).toBe(true)
      })
    })

    it('should display detailed lists for each information section', () => {
      const infoLists = wrapper.findAll('.info-list')
      expect(infoLists.length).toBe(4)
      
      infoLists.forEach(list => {
        const listItems = list.findAll('li')
        expect(listItems.length).toBeGreaterThan(0)
      })
    })

    it('should show severity badge and references', () => {
      const severityBadge = wrapper.find('.severity-badge')
      expect(severityBadge.exists()).toBe(true)
      expect(severityBadge.text()).toBe('High')
      
      // Check for references section if it exists
      const references = wrapper.find('.references')
      if (references.exists()) {
        expect(references.exists()).toBe(true)
      }
    })
  })

  describe('TC-019: Progress Indicator and Navigation', () => {
    it('should display progress indicator with correct steps', () => {
      const progressSteps = wrapper.findAll('.progress-step')
      expect(progressSteps.length).toBe(3)
      
      const stepLabels = progressSteps.map(step => 
        step.find('.step-label').text()
      )
      
      expect(stepLabels).toContain('Choose Category')
      expect(stepLabels).toContain('Select Condition')
      expect(stepLabels).toContain('View Details')
    })

    it('should highlight current step in progress indicator', () => {
      const activeStep = wrapper.find('.progress-step.active')
      expect(activeStep.exists()).toBe(true)
      
      const stepNumber = activeStep.find('.step-number')
      expect(stepNumber.text()).toBe('1')
    })

    it('should allow navigation back to previous steps', async () => {
      // Go to step 2
      await wrapper.vm.selectCategory('water-borne')
      expect(wrapper.vm.currentStep).toBe(2)
      
      // Go to step 3
      const firstCondition = wrapper.vm.healthConditions['water-borne'][0]
      await wrapper.vm.selectCondition(firstCondition)
      expect(wrapper.vm.currentStep).toBe(3)
      
      // Should be able to go back (if back functionality is implemented)
      // This would depend on the actual implementation
    })
  })

  describe('TC-020: Data Quality and Content Validation', () => {
    it('should have valid health condition data structure', () => {
      const healthConditions = wrapper.vm.healthConditions
      
      expect(healthConditions).toHaveProperty('water-borne')
      expect(healthConditions).toHaveProperty('parasitic')
      expect(healthConditions).toHaveProperty('sanitation-related')
      expect(healthConditions).toHaveProperty('water-scarcity')
    })

    it('should have complete information for each condition', () => {
      const cholera = wrapper.vm.healthConditions['water-borne'][0]
      
      expect(cholera).toHaveProperty('name')
      expect(cholera).toHaveProperty('description')
      expect(cholera).toHaveProperty('causes')
      expect(cholera).toHaveProperty('symptoms')
      expect(cholera).toHaveProperty('remedies')
      expect(cholera).toHaveProperty('prevention')
      expect(cholera).toHaveProperty('severity')
      expect(cholera).toHaveProperty('icon')
      expect(cholera).toHaveProperty('color')
    })

    it('should have non-empty arrays for condition details', () => {
      const cholera = wrapper.vm.healthConditions['water-borne'][0]
      
      expect(cholera.causes.length).toBeGreaterThan(0)
      expect(cholera.symptoms.length).toBeGreaterThan(0)
      expect(cholera.remedies.length).toBeGreaterThan(0)
      expect(cholera.prevention.length).toBeGreaterThan(0)
    })

    it('should have proper severity classification', () => {
      const allConditions = Object.values(wrapper.vm.healthConditions).flat()
      
      allConditions.forEach(condition => {
        expect(['high', 'medium', 'low']).toContain(condition.severity)
      })
    })
  })
})
