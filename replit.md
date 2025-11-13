# FitRecommender - Sistema de Recomendación Deportiva Multiparadigma

## Overview

FitRecommender is an intelligent sports routine recommendation system built with Django. The system analyzes user characteristics (age, weight, height, BMI) and preferences (available days, fitness goals) to recommend personalized workout routines from a catalog of over 10 professional programs.

The core innovation is the integration of three programming paradigms working together:
- **Imperative** for request/response flow control
- **Functional** for pure data transformations and filtering
- **Logic-based** for rule inference and safety validation

The system calculates BMI, determines safe intensity levels, applies logical rules for recommendations, and computes compatibility scores to match users with optimal workout routines.

## User Preferences

Preferred communication style: Simple, everyday language.

## System Architecture

### Web Framework
- **Django 4.2.7** - Full-stack web framework handling routing, templating, and HTTP layer
- **No database models** - The system operates entirely with in-memory data structures. Workout routines are defined in `datos.py` as Python dictionaries
- **Template-based rendering** - Server-side HTML generation using Django templates with Bootstrap-inspired CSS

### Multi-Paradigm Design Pattern

The architecture deliberately separates concerns across three programming paradigms:

**1. Imperative Layer (`views.py`)**
- Handles HTTP request/response cycle
- Sequential flow control and validation
- Coordinates between functional and logic modules
- Renders final responses

**2. Functional Layer (`processor.py`)**
- Pure functions for calculations: `calcular_imc()`, `clasificar_imc()`, `calcular_compatibilidad()`
- Functional operations: `filter()` for routine filtering, `map()` for transformations, `sorted()` for ranking, `reduce()` for aggregations
- Immutable data transformations
- No side effects in computation logic

**3. Logic Layer (`logic_rules.py`)**
- Custom rule engine (`MotorReglasLogicas`) compatible with Python 3.11
- Inference rules for safety and recommendations:
  - Age-based intensity limits (e.g., age > 50 → low intensity)
  - BMI-based objective suggestions (e.g., BMI > 25 → weight loss)
  - Availability-based level recommendations (e.g., days < 3 → beginner)
- Declarative rule definitions with explanation generation

### Data Flow Architecture

1. User submits form (age, weight, height, days available, objective)
2. **Imperative layer** validates input and extracts POST data
3. **Functional layer** processes user data:
   - Calculates IMC and classifies it
   - Filters routines by compatibility
   - Maps and transforms data structures
   - Ranks routines by score
4. **Logic layer** applies inference rules:
   - Determines safe intensity levels
   - Validates routine safety for user profile
   - Generates explanations for recommendations
5. **Imperative layer** selects top result and renders response

### Frontend Architecture
- **Static files** organized in `recommender/static/`:
  - `css/styles.css` - Custom CSS with CSS variables for theming
  - `js/script.js` - Client-side validation and interactive features (FAQ accordion)
- **Template inheritance** - Base template (`base.html`) with navbar/footer, extended by page-specific templates
- **Responsive design** - Mobile-first approach with flexbox/grid layouts

### URL Routing Structure
```
/ → index (home + recommendation form)
/recomendar/ → POST endpoint for processing recommendations
/rutinas/ → catalog view with filtering
/acerca-de/ → about page explaining paradigms
```

### State Management
- **Stateless** - No session or database storage
- **Request-scoped** - All data processed per-request
- Form data → Processing → Response (no persistence)

### Data Structures
- Routines stored as list of dictionaries in `datos.py`
- Each routine contains: id, name, description, level, objective, duration, intensity, exercises, weekly plan
- User data transformed through functional pipeline
- Results passed to templates as context dictionaries

## External Dependencies

### Python Packages
- **Django 4.2.7** - Web framework for routing, templating, and request handling
- **Pillow 10.0.0** - Image processing library (included but may not be actively used)

### No External Services
- No database required (SQLite not used, no migrations needed)
- No external APIs or third-party integrations
- No authentication/authorization system
- No cloud services or remote storage

### Development Environment
- Python 3.11+ required for compatibility with custom logic engine
- Built-in Django development server for local testing
- Static files served by Django in development mode

### Browser Requirements
- Modern JavaScript support for client-side validation
- CSS Grid and Flexbox support for responsive layouts
- No heavy frontend framework dependencies (vanilla JS)