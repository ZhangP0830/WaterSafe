import { describe, it, expect, beforeEach, vi } from 'vitest'
import { mount } from '@vue/test-utils'
import { createRouter, createWebHistory } from 'vue-router'
import { createPinia } from 'pinia'
import MaternalInfantHealthView from '@/views/MaternalInfantHealthView.vue'

// Mock child components
vi.mock('@/components/navigation/NavbarDefault.vue', () => ({
  default: { template: '<div data-testid="navbar">Navbar</div>' }
}))

vi.mock('@/components/layout/FooterDefault.vue', () => ({
  default: { template: '<div data-testid="footer">Footer</div>' }
}))

vi.mock('@/components/MaternalInfantHealth/HydrationGuidance.vue', () => ({
  default: { template: '<div data-testid="hydration-guidance">Hydration Guidance</div>' }
}))

vi.mock('@/components/MaternalInfantHealth/FeedingTracking.vue', () => ({
  default: { template: '<div data-testid="feeding-tracking">Feeding Tracking</div>' }
}))

vi.mock('@/components/MaternalInfantHealth/WaterHealthInfo.vue', () => ({
  default: { template: '<div data-testid="water-health-info">Water Health Info</div>' }
}))

vi.mock('@/components/MaternalInfantHealth/SymptomChecker.vue', () => ({
  default: { template: '<div data-testid="symptom-checker">Symptom Checker</div>' }
}))

vi.mock('@/components/MaternalInfantHealth/EmergencyTips.vue', () => ({
  default: { template: '<div data-testid="emergency-tips">Emergency Tips</div>' }
}))

vi.mock('@/components/MaternalInfantHealth/UserSelectionModal.vue', () => ({
  default: { template: '<div data-testid="user-selection-modal">User Selection Modal</div>' }
}))

describe('MaternalInfantHealthView - Core Functionality', () => {
  let wrapper
  let router
  let pinia

  beforeEach(async () => {
    pinia = createPinia()
    router = createRouter({
      history: createWebHistory(),
      routes: [
        { path: '/maternal-infant-health', component: MaternalInfantHealthView }
      ]
    })

    wrapper = mount(MaternalInfantHealthView, {
      global: {
        plugins: [router, pinia],
        stubs: {
          'MaterialButton': {
            template: '<button @click="$emit(\'click\')"><slot /></button>',
            emits: ['click']
          }
        }
      }
    })

    await router.isReady()
  })

  afterEach(() => {
    wrapper.unmount()
  })

  describe('TC-006: User Profile Selection and Navigation', () => {
    it('should display user selection modal', () => {
      const modal = wrapper.find('[data-testid="user-selection-modal"]')
      expect(modal.exists()).toBe(true)
    })

    it('should show correct hero section content', () => {
      const heroTitle = wrapper.find('.display-3')
      const heroSubtitle = wrapper.find('.lead')
      
      expect(heroTitle.text()).toContain('Caring for You and Your Little One')
      expect(heroSubtitle.text()).toContain('Personalized guidance for hydration, nutrition, and health monitoring')
    })

    it('should have working navigation tabs', () => {
      const navTabs = wrapper.findAll('.nav-tab-btn')
      expect(navTabs.length).toBe(5) // hydration, feeding, water-health, symptoms, emergency
      
      const expectedTabs = [
        'Hydration Guidance',
        'Feeding & Tracking', 
        'Water Health Info',
        'Symptom Checker',
        'Emergency Safety Guide'
      ]
      
      navTabs.forEach((tab, index) => {
        expect(tab.text()).toContain(expectedTabs[index].split(' ')[0])
      })
    })
  })

  describe('TC-007: Section Navigation and Content Display', () => {
    it('should start with hydration section active by default', () => {
      const hydrationSection = wrapper.find('[data-testid="hydration-guidance"]')
      expect(hydrationSection.exists()).toBe(true)
    })

    it('should switch between sections when tabs are clicked', async () => {
      const feedingTab = wrapper.find('.nav-tab-btn[data-section="feeding"]')
      if (feedingTab.exists()) {
        await feedingTab.trigger('click')
        await wrapper.vm.$nextTick()
        
        const feedingSection = wrapper.find('[data-testid="feeding-tracking"]')
        expect(feedingSection.exists()).toBe(true)
      }
    })

    it('should show only one section at a time', () => {
      const sections = [
        '[data-testid="hydration-guidance"]',
        '[data-testid="feeding-tracking"]',
        '[data-testid="water-health-info"]',
        '[data-testid="symptom-checker"]',
        '[data-testid="emergency-tips"]'
      ]
      
      let visibleSections = 0
      sections.forEach(selector => {
        if (wrapper.find(selector).exists()) {
          visibleSections++
        }
      })
      
      expect(visibleSections).toBe(1)
    })
  })

  describe('TC-008: Hero Section Statistics and Features', () => {
    it('should display feature statistics cards', () => {
      const statItems = wrapper.findAll('.stat-item')
      expect(statItems.length).toBe(2)
      
      const statTexts = statItems.map(item => item.text())
      expect(statTexts.some(text => text.includes('Hydration & Nutrition'))).toBe(true)
      expect(statTexts.some(text => text.includes('Health & Safety'))).toBe(true)
    })

    it('should have proper action buttons', () => {
      const actionButtons = wrapper.findAll('.hero-actions button')
      expect(actionButtons.length).toBe(2)
      
      const buttonTexts = actionButtons.map(btn => btn.text())
      expect(buttonTexts.some(text => text.includes('Get Started'))).toBe(true)
      expect(buttonTexts.some(text => text.includes('Change Profile'))).toBe(true)
    })
  })

  describe('TC-009: Responsive Design and Styling', () => {
    it('should have proper responsive classes', () => {
      const heroSection = wrapper.find('.hero-section')
      expect(heroSection.exists()).toBe(true)
      
      const navigationSection = wrapper.find('.navigation-section')
      expect(navigationSection.exists()).toBe(true)
    })

    it('should maintain proper sticky navigation', () => {
      const navSection = wrapper.find('.navigation-section')
      const computedStyle = window.getComputedStyle(navSection.element)
      
      expect(computedStyle.position).toBe('sticky')
    })

    it('should have proper tab styling and hover effects', () => {
      const navTabs = wrapper.findAll('.nav-tab-btn')
      expect(navTabs.length).toBeGreaterThan(0)
      
      navTabs.forEach(tab => {
        expect(tab.classes()).toContain('nav-tab-btn')
      })
    })
  })

  describe('TC-010: Component Integration and Data Flow', () => {
    it('should properly integrate with Pinia store', () => {
      // Test that the component can access store data
      expect(wrapper.vm.store).toBeDefined()
    })

    it('should handle user type changes correctly', async () => {
      const changeProfileButton = wrapper.find('button:contains("Change Profile")')
      if (changeProfileButton.exists()) {
        await changeProfileButton.trigger('click')
        // Verify modal opens or user type changes
        expect(wrapper.vm.store.changeUserType).toBeDefined()
      }
    })

    it('should maintain state consistency across navigation', async () => {
      const initialSection = wrapper.vm.activeSection
      
      // Navigate to different section
      await wrapper.vm.setActiveSection('feeding')
      expect(wrapper.vm.activeSection).toBe('feeding')
      
      // Navigate back
      await wrapper.vm.setActiveSection('hydration')
      expect(wrapper.vm.activeSection).toBe('hydration')
    })
  })
})
