import { describe, it, expect, beforeEach, vi } from 'vitest'
import { mount } from '@vue/test-utils'
import { createRouter, createWebHistory } from 'vue-router'
import HomeView from '@/views/HomeView.vue'

// Mock the video file
vi.mock('@/assets/video/opening_page_video_with_mother_infant.mp4', () => ({
  default: 'mocked-video-path.mp4'
}))

// Mock child components
vi.mock('@/components/navigation/NavbarDefault.vue', () => ({
  default: { template: '<div data-testid="navbar">Navbar</div>' }
}))

vi.mock('@/components/layout/FooterDefault.vue', () => ({
  default: { template: '<div data-testid="footer">Footer</div>' }
}))

vi.mock('@/components/HomeSection/HomeIntroduction.vue', () => ({
  default: { template: '<div data-testid="home-intro">Home Introduction</div>' }
}))

vi.mock('@/components/HomeSection/HomeInformation.vue', () => ({
  default: { template: '<div data-testid="home-info">Home Information</div>' }
}))

describe('HomeView - Core Functionality', () => {
  let wrapper
  let router

  beforeEach(async () => {
    router = createRouter({
      history: createWebHistory(),
      routes: [
        { path: '/', component: HomeView },
        { path: '/sanitation-support', component: { template: '<div>Sanitation Support</div>' } },
        { path: '/maternal-infant-health', component: { template: '<div>Maternal Infant Health</div>' } }
      ]
    })

    wrapper = mount(HomeView, {
      global: {
        plugins: [router],
        stubs: {
          'router-link': {
            template: '<a><slot /></a>',
            props: ['to']
          }
        }
      }
    })

    await router.isReady()
  })

  afterEach(() => {
    wrapper.unmount()
  })

  describe('TC-001: Video Background Integration', () => {
    it('should display video background with correct attributes', () => {
      const video = wrapper.find('video')
      
      expect(video.exists()).toBe(true)
      expect(video.attributes('autoplay')).toBeDefined()
      expect(video.attributes('muted')).toBeDefined()
      expect(video.attributes('loop')).toBeDefined()
      expect(video.attributes('playsinline')).toBeDefined()
      expect(video.attributes('aria-label')).toBe('Water safety video background')
    })

    it('should have proper video source', () => {
      const video = wrapper.find('video')
      expect(video.attributes('src')).toBe('mocked-video-path.mp4')
    })

    it('should maintain video brightness and contrast', () => {
      const video = wrapper.find('video')
      const videoElement = video.element
      const computedStyle = window.getComputedStyle(videoElement)
      
      // Check that video has proper styling for brightness
      expect(videoElement.style.filter).toContain('brightness(1)')
    })
  })

  describe('TC-002: Hero Section Content', () => {
    it('should display correct hero title and subtitle', () => {
      const title = wrapper.find('.hero-title')
      const subtitle = wrapper.find('.hero-subtitle')
      
      expect(title.text()).toBe('WaterSafe')
      expect(subtitle.text()).toBe('Protecting Families from Water Contamination Risks')
    })

    it('should have semi-transparent text block with proper styling', () => {
      const textBlock = wrapper.find('.hero-text-block')
      
      expect(textBlock.exists()).toBe(true)
      expect(textBlock.classes()).toContain('hero-text-block')
      
      // Check for glass-morphism effect
      const computedStyle = window.getComputedStyle(textBlock.element)
      expect(computedStyle.backdropFilter).toContain('blur')
    })
  })

  describe('TC-003: Navigation and Feature Sections', () => {
    it('should render all main components', () => {
      expect(wrapper.find('[data-testid="navbar"]').exists()).toBe(true)
      expect(wrapper.find('[data-testid="home-intro"]').exists()).toBe(true)
      expect(wrapper.find('[data-testid="home-info"]').exists()).toBe(true)
      expect(wrapper.find('[data-testid="footer"]').exists()).toBe(true)
    })

    it('should display sanitation support feature section', () => {
      const sanitationSection = wrapper.find('.sanitation-feature-section')
      expect(sanitationSection.exists()).toBe(true)
      
      const title = sanitationSection.find('h2')
      expect(title.text()).toContain('Safe Sanitation & Hygiene Support')
    })

    it('should display maternal infant health feature section', () => {
      const maternalSection = wrapper.find('.maternal-infant-feature-section')
      expect(maternalSection.exists()).toBe(true)
      
      const title = maternalSection.find('h2')
      expect(title.text()).toContain('Maternal & Infant Health Shield')
    })
  })

  describe('TC-004: Call-to-Action Buttons', () => {
    it('should have working CTA buttons without Learn More buttons', () => {
      const ctaButtons = wrapper.findAll('.cta-buttons .btn')
      
      // Should only have primary action buttons, no Learn More buttons
      expect(ctaButtons.length).toBeGreaterThan(0)
      
      const buttonTexts = ctaButtons.map(btn => btn.text())
      expect(buttonTexts.some(text => text.includes('Get Your Checklist'))).toBe(true)
      expect(buttonTexts.some(text => text.includes('Get Your Shield'))).toBe(true)
      expect(buttonTexts.some(text => text.includes('Learn More'))).toBe(false)
    })

    it('should have proper router links for navigation', () => {
      const routerLinks = wrapper.findAllComponents({ name: 'router-link' })
      expect(routerLinks.length).toBeGreaterThan(0)
      
      const links = routerLinks.map(link => link.props('to'))
      expect(links).toContain('/sanitation-support')
      expect(links).toContain('/maternal-infant-health')
    })
  })

  describe('TC-005: Responsive Design and Accessibility', () => {
    it('should have proper responsive classes', () => {
      const heroContent = wrapper.find('.hero-content')
      expect(heroContent.exists()).toBe(true)
      
      const container = wrapper.find('.container')
      expect(container.exists()).toBe(true)
    })

    it('should have proper semantic structure', () => {
      const mainContent = wrapper.find('.content-section')
      expect(mainContent.exists()).toBe(true)
      
      const sections = wrapper.findAll('section')
      expect(sections.length).toBeGreaterThan(0)
    })

    it('should maintain proper z-index layering', () => {
      const heroVideo = wrapper.find('.hero-video')
      const heroContent = wrapper.find('.hero-content')
      
      if (heroVideo.exists() && heroContent.exists()) {
        const videoStyle = window.getComputedStyle(heroVideo.element)
        const contentStyle = window.getComputedStyle(heroContent.element)
        
        expect(parseInt(videoStyle.zIndex)).toBeLessThan(parseInt(contentStyle.zIndex))
      }
    })
  })
})
