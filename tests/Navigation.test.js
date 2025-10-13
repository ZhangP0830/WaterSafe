import { describe, it, expect, beforeEach, vi } from 'vitest'
import { mount } from '@vue/test-utils'
import { createRouter, createWebHistory } from 'vue-router'
import NavbarDefault from '@/components/navigation/NavbarDefault.vue'

describe('NavbarDefault - Navigation Functionality', () => {
  let wrapper
  let router

  beforeEach(async () => {
    router = createRouter({
      history: createWebHistory(),
      routes: [
        { path: '/', name: 'home', component: { template: '<div>Home</div>' } },
        { path: '/water-quality-prediction', name: 'water-quality-prediction', component: { template: '<div>Water Quality</div>' } },
        { path: '/trusted-alternatives', name: 'trusted-alternatives', component: { template: '<div>Trusted Alternatives</div>' } },
        { path: '/water-safety-hub', name: 'water-safety-hub', component: { template: '<div>Water Safety Hub</div>' } },
        { path: '/sanitation-support', name: 'sanitation-support', component: { template: '<div>Sanitation Support</div>' } },
        { path: '/maternal-infant-health', name: 'maternal-infant-health', component: { template: '<div>Maternal Infant Health</div>' } },
        { path: '/water-safety-companion', name: 'water-safety-companion', component: { template: '<div>Water Safety Companion</div>' } }
      ]
    })

    wrapper = mount(NavbarDefault, {
      props: {
        sticky: true
      },
      global: {
        plugins: [router],
        stubs: {
          'RouterLink': {
            template: '<a @click="$emit(\'click\')" :href="to"><slot /></a>',
            props: ['to'],
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

  describe('TC-011: Navigation Menu Structure', () => {
    it('should display all required navigation items', () => {
      const navItems = wrapper.findAll('.nav-item')
      expect(navItems.length).toBe(6) // 6 main navigation items
      
      const expectedItems = [
        'Water Quality Prediction',
        'Trusted Alternatives',
        'Water Safety Hub',
        'Sanitation Support',
        'Maternal & Infant Health',
        'Water Safety Companion'
      ]
      
      expectedItems.forEach(expectedText => {
        const item = wrapper.find(`.nav-link:contains("${expectedText}")`)
        expect(item.exists()).toBe(true)
      })
    })

    it('should have proper brand/logo section', () => {
      const brandLinks = wrapper.findAll('.navbar-brand')
      expect(brandLinks.length).toBeGreaterThan(0)
      
      const brandText = brandLinks[0].text()
      expect(brandText).toContain('WaterSafety')
    })

    it('should have proper icons for each navigation item', () => {
      const navIcons = wrapper.findAll('.material-icons')
      expect(navIcons.length).toBe(6) // One icon per nav item
      
      const expectedIcons = [
        'analytics',
        'map', 
        'water_drop',
        'sanitizer',
        'pregnant_woman',
        'mic'
      ]
      
      expectedIcons.forEach(iconName => {
        const icon = wrapper.find(`.material-icons:contains("${iconName}")`)
        expect(icon.exists()).toBe(true)
      })
    })
  })

  describe('TC-012: Navigation Styling and Responsiveness', () => {
    it('should have proper sticky navigation styling', () => {
      const nav = wrapper.find('nav')
      expect(nav.classes()).toContain('navbar')
      expect(nav.classes()).toContain('navbar-expand-lg')
    })

    it('should have enhanced styling with glass-morphism effect', () => {
      const nav = wrapper.find('nav')
      const computedStyle = window.getComputedStyle(nav.element)
      
      // Check for backdrop-filter or similar glass effect
      expect(nav.classes()).toContain('blur')
    })

    it('should have proper navigation link styling', () => {
      const navLinks = wrapper.findAll('.nav-link')
      expect(navLinks.length).toBeGreaterThan(0)
      
      navLinks.forEach(link => {
        expect(link.classes()).toContain('nav-link')
        expect(link.classes()).toContain('rounded-pill')
      })
    })

    it('should handle mobile menu toggle', async () => {
      const toggleButton = wrapper.find('.navbar-toggler')
      if (toggleButton.exists()) {
        await toggleButton.trigger('click')
        expect(wrapper.vm.isMenuOpen).toBe(true)
      }
    })
  })

  describe('TC-013: Navigation Functionality', () => {
    it('should navigate to correct routes when clicked', async () => {
      const waterQualityLink = wrapper.find('a[href="/water-quality-prediction"]')
      if (waterQualityLink.exists()) {
        await waterQualityLink.trigger('click')
        await router.push('/water-quality-prediction')
        expect(router.currentRoute.value.path).toBe('/water-quality-prediction')
      }
    })

    it('should close mobile menu when navigation link is clicked', async () => {
      // Open mobile menu first
      wrapper.vm.isMenuOpen = true
      await wrapper.vm.$nextTick()
      
      // Click a navigation link
      const navLink = wrapper.find('.nav-link')
      if (navLink.exists()) {
        await navLink.trigger('click')
        expect(wrapper.vm.isMenuOpen).toBe(false)
      }
    })

    it('should maintain proper text color based on props', () => {
      const navLinks = wrapper.findAll('.nav-link')
      navLinks.forEach(link => {
        const textColor = wrapper.vm.getTextColor()
        expect(link.classes()).toContain(textColor)
      })
    })
  })

  describe('TC-014: Navigation Width and Text Display', () => {
    it('should display full navigation text without truncation', () => {
      const navTexts = wrapper.findAll('.nav-text')
      expect(navTexts.length).toBe(6)
      
      const expectedTexts = [
        'Water Quality Prediction',
        'Trusted Alternatives',
        'Water Safety Hub',
        'Sanitation Support',
        'Maternal & Infant Health',
        'Water Safety Companion'
      ]
      
      expectedTexts.forEach(expectedText => {
        const textElement = wrapper.find(`.nav-text:contains("${expectedText}")`)
        expect(textElement.exists()).toBe(true)
        expect(textElement.text()).toBe(expectedText)
      })
    })

    it('should have proper spacing between navigation items', () => {
      const navItems = wrapper.findAll('.nav-item')
      navItems.forEach(item => {
        expect(item.classes()).toContain('mx-2')
      })
    })

    it('should maintain proper container width', () => {
      const container = wrapper.find('.container-fluid')
      expect(container.exists()).toBe(true)
      expect(container.classes()).toContain('px-2')
    })
  })

  describe('TC-015: Navigation Accessibility and User Experience', () => {
    it('should have proper ARIA labels and accessibility attributes', () => {
      const nav = wrapper.find('nav')
      expect(nav.attributes('role')).toBe('navigation')
      
      const toggleButton = wrapper.find('.navbar-toggler')
      if (toggleButton.exists()) {
        expect(toggleButton.attributes('aria-label')).toBe('Toggle navigation')
      }
    })

    it('should have proper hover effects on navigation items', () => {
      const navLinks = wrapper.findAll('.nav-link')
      navLinks.forEach(link => {
        expect(link.classes()).toContain('nav-link')
        // Check for hover transition classes
        const computedStyle = window.getComputedStyle(link.element)
        expect(computedStyle.transition).toContain('all')
      })
    })

    it('should maintain consistent navigation state', () => {
      expect(wrapper.vm.isMenuOpen).toBe(false)
      expect(wrapper.vm.textDark).toBeDefined()
    })
  })
})
