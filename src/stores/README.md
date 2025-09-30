# Stores Directory 🏪

This directory manages application data and state using Pinia, Vue's official state management library. It keeps track of user data, water quality information, and application settings.

## 🎯 What's Inside

Stores provide centralized data management:
- **User Data** - Authentication, preferences, and profile
- **Water Quality** - Predictions, historical data, and analysis
- **Water Sources** - Location data, filtering, and search
- **Application State** - UI state, notifications, and settings

## 📁 Main Files

### index.js
The main store configuration that sets up Pinia and defines how data is managed across the application.

## 🏪 Store Types

### Water Quality Store
Manages water quality data and predictions:
- **Current Predictions** - Latest water quality forecasts
- **Historical Data** - Past water quality measurements
- **Site Information** - Details about monitoring sites
- **Risk Assessments** - Safety levels and recommendations

### Water Sources Store
Handles water source information and location data:
- **Source Database** - All available water sources
- **Location Services** - GPS and map integration
- **Search & Filtering** - Find sources by criteria
- **Status Updates** - Real-time availability information

### User Store
Manages user account and preferences:
- **Authentication** - Login status and user profile
- **Preferences** - Theme, language, and settings
- **Favorites** - Saved water sources and locations
- **History** - Previously viewed content

### App Store
Controls global application state:
- **UI State** - Loading indicators, errors, and notifications
- **Navigation** - Current page and sidebar state
- **Theme** - Light/dark mode and visual preferences
- **System Settings** - Application-wide configuration

## 🚀 How Stores Work

### Data Flow
1. **User Action** - User interacts with the interface
2. **Store Update** - Data is updated in the appropriate store
3. **Reactive Update** - All components using that data update automatically
4. **UI Refresh** - Interface reflects the new data

### State Management
- **Centralized** - All data in one place
- **Reactive** - Changes automatically update the UI
- **Persistent** - Important data saved between sessions
- **Efficient** - Only updates what's necessary

## 🔧 Store Features

### Data Persistence
Important data is automatically saved:
- **User Preferences** - Theme, language, and settings
- **Favorites** - Saved water sources and locations
- **Authentication** - Login status and tokens
- **Recent Searches** - Previous search queries

### Real-time Updates
Stores handle live data:
- **Water Quality** - Latest predictions and measurements
- **Source Status** - Real-time availability updates
- **Notifications** - System alerts and messages
- **Location Data** - GPS and map updates

### Error Handling
Robust error management:
- **API Errors** - Handle network and server issues
- **Validation** - Check data before saving
- **Fallbacks** - Provide default values when needed
- **User Feedback** - Show clear error messages

## 📱 Mobile Considerations

### Performance
- **Efficient Updates** - Minimal data transfer
- **Offline Support** - Work without internet connection
- **Memory Management** - Optimize for mobile devices
- **Battery Optimization** - Reduce background processing

### User Experience
- **Fast Loading** - Quick data access
- **Smooth Interactions** - Responsive interface updates
- **Data Sync** - Keep data current across devices
- **Offline Mode** - Access cached data when offline

## 🔄 Data Synchronization

### Server Communication
Stores communicate with the backend:
- **API Calls** - Fetch and send data
- **Real-time Updates** - WebSocket connections
- **Caching** - Store frequently accessed data
- **Conflict Resolution** - Handle data conflicts

### Local Storage
Data is stored locally for:
- **Performance** - Faster access to cached data
- **Offline Use** - Work without internet
- **User Experience** - Immediate data availability
- **Bandwidth** - Reduce data usage

## 🧪 Testing Stores

### Quality Assurance
Stores are tested for:
- **Data Accuracy** - Correct information storage
- **State Updates** - Proper data changes
- **Error Handling** - Graceful failure recovery
- **Performance** - Fast data operations

### Integration Testing
- **Component Integration** - Stores work with UI components
- **API Integration** - Backend communication works
- **Cross-Store** - Multiple stores work together
- **User Flows** - Complete user journeys function

## 📚 Resources

- [Pinia Documentation](https://pinia.vuejs.org/)
- [State Management Best Practices](https://vuejs.org/guide/scaling-up/state-management.html)
- [Vue.js Reactivity Guide](https://vuejs.org/guide/extras/reactivity-in-depth.html)

---

<div align="center">
  <strong>Data Management for WaterSafe</strong>
  <br>
  <em>Centralized state with Pinia</em>
</div>
