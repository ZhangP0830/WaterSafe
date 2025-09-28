# WaterSafe Project Structure 📁

This document provides a comprehensive overview of the WaterSafe project structure and organization.

## 🏗️ Root Directory Structure

```
WaterSafe/
├── 📁 backend/                 # Backend API and services
├── 📁 src/                     # Frontend Vue.js application
├── 📁 public/                  # Static assets and public files
├── 📁 dist/                    # Built frontend files (production)
├── 📁 node_modules/            # Frontend dependencies
├── 📄 package.json             # Frontend dependencies and scripts
├── 📄 package-lock.json        # Frontend dependency lock file
├── 📄 vite.config.js           # Vite build configuration
├── 📄 genezio.yaml             # Genezio deployment configuration
├── 📄 index.html               # Main HTML entry point
├── 📄 README.md                # Main project documentation
├── 📄 CONTRIBUTING.md          # Contribution guidelines
├── 📄 CHANGELOG.md             # Version history and changes
├── 📄 PROJECT_STRUCTURE.md     # This file
└── 📄 LICENSE                  # Project license
```

## 🎨 Frontend Structure (`src/`)

```
src/
├── 📁 components/              # Reusable Vue components
│   ├── 📁 AwarenessSection/    # Water safety awareness components
│   │   ├── AwarenessNavTab.vue
│   │   ├── ConfirmedContamination.vue
│   │   ├── ContaminationCleared.vue
│   │   ├── EarlySignsOfContamination.vue
│   │   └── SevereContamination.vue
│   ├── 📁 cards/               # Card components
│   │   ├── 📁 blogCards/       # Blog card components
│   │   ├── 📁 counterCards/    # Counter display cards
│   │   ├── 📁 infoCards/       # Information cards
│   │   ├── 📁 reviewCards/     # Review/testimonial cards
│   │   ├── 📁 rotatingCards/   # Rotating card components
│   │   └── 📁 teamCards/       # Team member cards
│   ├── 📁 HomeSection/         # Home page components
│   │   └── HomeInformation.vue
│   ├── 📁 layout/              # Layout components
│   │   ├── Breadcrumbs.vue
│   │   ├── FooterCentered.vue
│   │   ├── FooterDefault.vue
│   │   └── Header.vue
│   ├── 📁 navigation/          # Navigation components
│   │   └── NavbarDefault.vue
│   ├── 📁 tables/              # Table components
│   │   └── Table.vue
│   ├── MaterialAlert.vue       # Material Design alert component
│   ├── MaterialAvatar.vue      # Material Design avatar component
│   ├── MaterialBadge.vue       # Material Design badge component
│   ├── MaterialButton.vue      # Material Design button component
│   ├── MaterialCheckbox.vue    # Material Design checkbox component
│   ├── MaterialInput.vue       # Material Design input component
│   ├── MaterialPagination.vue  # Material Design pagination component
│   ├── MaterialPaginationItem.vue
│   ├── MaterialProgress.vue    # Material Design progress component
│   ├── MaterialSocialButton.vue
│   ├── MaterialSwitch.vue      # Material Design switch component
│   └── MaterialTextArea.vue    # Material Design textarea component
├── 📁 views/                   # Page components (routes)
│   ├── HomeView.vue            # Home page
│   ├── SanitationSupportView.vue # Sanitation support page
│   ├── TrustedAlternativesView.vue # Trusted alternatives page
│   ├── VoiceAssistantView.vue  # AI assistant page
│   ├── WaterQualityPredictionView.vue # Water quality prediction page
│   └── WaterSafetyHubView.vue  # Water safety hub page
├── 📁 router/                  # Vue Router configuration
│   └── index.js                # Route definitions
├── 📁 stores/                  # Pinia state management
│   └── index.js                # Store configuration
├── 📁 assets/                  # Static assets
│   ├── 📁 css/                 # CSS files
│   │   ├── material-kit-pro.css
│   │   ├── material-kit-pro.css.map
│   │   ├── material-kit-pro.min.css
│   │   ├── nucleo-icons.css
│   │   └── nucleo-svg.css
│   ├── 📁 fonts/               # Font files
│   │   ├── nucleo-icons.eot
│   │   ├── nucleo-icons.svg
│   │   ├── nucleo-icons.ttf
│   │   ├── nucleo-icons.woff
│   │   ├── nucleo-icons.woff2
│   │   ├── nucleo.eot
│   │   ├── nucleo.ttf
│   │   └── nucleo.woff
│   ├── 📁 img/                 # Image assets
│   │   ├── ai-background.png
│   │   ├── awarenesshubbackground.png
│   │   ├── down-arrow-dark.svg
│   │   ├── down-arrow-white.svg
│   │   ├── down-arrow.svg
│   │   ├── homebackground.png
│   │   ├── rotatecard-background.png
│   │   ├── team-1.jpg
│   │   ├── team-2.jpg
│   │   ├── team-3.jpg
│   │   ├── team-4.jpg
│   │   ├── trusted-background.jpg
│   │   ├── trusted-background.png
│   │   └── waves-white.svg
│   ├── 📁 js/                  # JavaScript files
│   │   ├── 📁 core/            # Core JavaScript modules
│   │   ├── 📁 plugins/         # Plugin JavaScript files
│   │   ├── material-input.js
│   │   ├── material-kit-pro.js
│   │   ├── material-kit-pro.js.map
│   │   ├── material-kit-pro.min.js
│   │   ├── nav-pills.js
│   │   ├── popover.js
│   │   ├── ripple-effect.js
│   │   ├── tooltip.js
│   │   └── useWindowsWidth.js
│   └── 📁 scss/                # SCSS source files
│       ├── 📁 material-kit/    # Material Kit SCSS files
│       └── material-kit.scss
├── 📁 layouts/                 # Layout templates
│   └── 📁 sections/            # Layout sections
│       ├── 📁 attention-catchers/ # Attention-grabbing components
│       ├── 📁 components/      # Layout components
│       ├── 📁 elements/        # UI elements
│       ├── 📁 input-areas/     # Input form components
│       ├── 📁 navigation/      # Navigation components
│       └── 📁 page-sections/   # Page section components
├── App.vue                     # Root Vue component
├── main.js                     # Application entry point
└── material-kit.js             # Material Kit initialization
```

## 🚀 Backend Structure (`backend/`)

```
backend/
├── 📁 api/                     # API route handlers
│   ├── guidance.py             # AI guidance and sanitation endpoints
│   ├── water_quality_prediction.py # Water quality prediction endpoints
│   └── water_sources.py        # Water source management endpoints
├── 📁 model/                   # Machine learning models and data
│   ├── Merged_Top6_pH_Avg_Cleaned.csv # Cleaned water quality data
│   ├── Pridict_Model.ipynb     # Model training notebook
│   ├── site_model_params_1Month.json # Trained model parameters
│   └── site_suburb_data.csv    # Site and suburb data
├── 📁 __pycache__/             # Python bytecode cache
├── 📄 main.py                  # FastAPI application entry point
├── 📄 database.py              # Database configuration and connection
├── 📄 models.py                # SQLAlchemy data models
├── 📄 crud.py                  # Database CRUD operations
├── 📄 requirements.txt         # Python dependencies
├── 📄 README.md                # Backend documentation
├── 📄 test_guidance_cache.py   # Guidance system cache tests
├── 📄 test_integration_guidance.py # Integration tests
├── 📄 test_llm_debug.py        # LLM debugging tests
├── 📄 test_simple.py           # Basic functionality tests
└── 📄 test_sources_implementation.py # Water sources API tests
```

## 📊 Data Models

### Water Sources Model
```python
class WaterSource:
    id: int
    name: str
    type: str
    status: str
    latitude: float
    longitude: float
    lga: str
    town: str
    created_at: datetime
    updated_at: datetime
```

### Site Suburb Data Model
```python
class SiteSuburbData:
    id: int
    site_id: str
    chloride_cl: float
    calcium_total: float
    magnesium_total: float
    sodium_na: float
    potassium_k: float
    salinity_ec: float
    ph_value: float
    value_date: date
    nearest_suburb: str
    created_at: datetime
```

## 🔧 Configuration Files

### Frontend Configuration
- **`package.json`**: Dependencies, scripts, and project metadata
- **`vite.config.js`**: Vite build tool configuration
- **`genezio.yaml`**: Genezio deployment configuration

### Backend Configuration
- **`requirements.txt`**: Python dependencies
- **`main.py`**: FastAPI application configuration
- **`database.py`**: Database connection and configuration

## 🧪 Testing Structure

### Frontend Tests
- Component unit tests
- Integration tests
- E2E tests with Cypress/Playwright

### Backend Tests
- API endpoint tests
- Database operation tests
- ML model tests
- Integration tests

## 📦 Build and Deployment

### Frontend Build
```bash
npm run build          # Production build
npm run dev            # Development server
npm run preview        # Preview production build
```

### Backend Deployment
```bash
python main.py         # Development server
uvicorn main:app       # Production server
```

## 🔄 Development Workflow

1. **Frontend Development**
   - Work in `src/` directory
   - Use Vue.js 3 Composition API
   - Follow Material Design principles
   - Test components in isolation

2. **Backend Development**
   - Work in `backend/` directory
   - Use FastAPI for API development
   - Follow RESTful API principles
   - Write comprehensive tests

3. **Database Management**
   - Use SQLAlchemy ORM
   - Migrate schema changes
   - Maintain data integrity
   - Optimize queries

## 📈 Performance Considerations

### Frontend Optimization
- Code splitting with Vite
- Lazy loading of components
- Image optimization
- Bundle size monitoring

### Backend Optimization
- Database query optimization
- Caching strategies
- API response compression
- Connection pooling

## 🔒 Security Structure

### Frontend Security
- Input validation
- XSS prevention
- CSRF protection
- Secure API communication

### Backend Security
- Input sanitization
- SQL injection prevention
- CORS configuration
- Authentication and authorization

## 📚 Documentation Structure

- **README.md**: Main project documentation
- **CONTRIBUTING.md**: Contribution guidelines
- **CHANGELOG.md**: Version history
- **PROJECT_STRUCTURE.md**: This file
- **backend/README.md**: Backend-specific documentation

---

<div align="center">
  <strong>Well-organized code is the foundation of maintainable software</strong>
  <br>
  <em>WaterSafe Project Structure Documentation</em>
</div>
