# Components Directory 🧩

This directory contains all reusable UI components for the WaterSafe application. These are the building blocks that create the user interface.

## 🎯 What's Inside

Components are organized by their purpose and functionality:
- **UI Elements** - Buttons, inputs, alerts, and other interface pieces
- **Page Sections** - Larger components for specific areas
- **Layout Components** - Headers, footers, and navigation
- **Specialized Components** - Water safety specific features

## 📁 Main Component Types

### 🎨 Material Design Components
Ready-to-use UI elements with consistent styling:
- **MaterialButton** - Styled buttons for actions
- **MaterialInput** - Text input fields with validation
- **MaterialAlert** - Notifications and messages
- **MaterialCard** - Information display cards
- **MaterialProgress** - Loading and progress indicators

### 🚨 Water Safety Components
Specialized components for water safety features:
- **AwarenessSection** - Educational content about water safety
- **ContaminationAlerts** - Warning and status displays
- **QualityIndicators** - Visual water quality displays

### 🏗️ Layout Components
Structure and navigation elements:
- **Header** - Main navigation and branding
- **Footer** - Links and additional information
- **Navigation** - Menu and routing components
- **Breadcrumbs** - Page location indicators

### 🃏 Card Components
Information display in card format:
- **InfoCards** - General information display
- **TeamCards** - Team member profiles
- **ReviewCards** - Testimonials and reviews
- **CounterCards** - Statistics and metrics

## 🚀 How to Use Components

### Basic Usage
Components are imported and used in Vue files:
```vue
<template>
  <MaterialButton @click="handleClick">
    Click Me
  </MaterialButton>
</template>
```

### Component Properties
Most components accept properties to customize their behavior:
- **variant** - Different visual styles (primary, secondary, etc.)
- **size** - Different sizes (small, medium, large)
- **disabled** - Enable/disable functionality

## 🎨 Styling and Design

### Material Design
All components follow Material Design principles:
- Consistent spacing and typography
- Smooth animations and transitions
- Accessible color schemes
- Touch-friendly interactions

### Responsive Design
Components automatically adapt to different screen sizes:
- **Mobile** - Optimized for touch interaction
- **Tablet** - Balanced layout for medium screens
- **Desktop** - Full feature set for large screens

## 🔧 Customization

### Theming
Components support theming through CSS variables:
- Primary and secondary colors
- Typography settings
- Spacing and sizing
- Dark/light mode support

### Adding New Components
When creating new components:
1. Follow the established naming pattern
2. Use Material Design principles
3. Make them responsive
4. Include proper documentation
5. Test across different devices

## 📱 Component Features

### Accessibility
- Keyboard navigation support
- Screen reader compatibility
- High contrast mode support
- Focus indicators

### Performance
- Lazy loading for heavy components
- Optimized rendering
- Minimal bundle size impact
- Efficient state management

## 🧪 Testing

Components are tested for:
- Visual appearance across devices
- User interaction functionality
- Accessibility compliance
- Performance benchmarks

## 📚 Resources

- [Material Design Guidelines](https://material.io/design)
- [Vue.js Component Guide](https://vuejs.org/guide/components/)
- [Accessibility Best Practices](https://web.dev/accessibility/)

---

<div align="center">
  <strong>Reusable UI Components</strong>
  <br>
  <em>Building blocks for the WaterSafe interface</em>
</div>
