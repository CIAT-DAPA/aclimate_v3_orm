# AClimate V3 ORM ⛅️💾

## 🏷️ Version & Tags

![GitHub release (latest by date)](https://img.shields.io/github/v/release/CIAT-DAPA/aclimate_v3_orm) ![](https://img.shields.io/github/v/tag/CIAT-DAPA/aclimate_v3_orm)

## 📌 Introduction

AClimate V3 ORM is an Object-Relational Mapping package designed for the AClimate platform. It facilitates interaction with relational databases for climate data models, forecast systems, agricultural zones, and administrative boundaries. The package provides a structured interface for accessing and manipulating climate historical data at different temporal resolutions.

This is an ORM (Object-Relational Mapping) built with the SQLAlchemy library for interfacing with relational databases.

## Documentation

For complete documentation, visit the [![Ask DeepWiki](https://deepwiki.com/badge.svg)](https://deepwiki.com/CIAT-DAPA/aclimate_v3_orm)

## Features

- Modular structure organized by domain (climate, forecast, catalog, administrative, etc.)
- Built using SQLAlchemy for efficient relational mapping
- Compatible with Python > 3.10
- Designed for integration into larger AClimate infrastructure

## ✅ Requirements

- Python > 3.10
- Relational database (PostgreSQL recommended, also compatible with MySQL and SQLite)
- Dependencies: SQLAlchemy, psycopg2, python-dotenv, typing_extensions, pydantic

# Installation

Install directly from GitHub:

```bash
pip install git+https://github.com/CIAT-DAPA/aclimate_v3_orm
```

To install a specific version:

```bash
pip install git+https://github.com/CIAT-DAPA/aclimate_v3_orm@v0.0.9
```

## 🔧 Environment Configuration

You can configure the database connection either by:

1. Creating a `.env` file in your project root, OR
2. Setting environment variables directly in your system

### Option 1: Using .env file

Create a file named `.env` with these configurations:

#### PostgreSQL

```ini
DATABASE_URL=postgresql://username:password@localhost:5432/database
```

### Option 2: Setting Environment Variables

- Windows (CMD/PowerShell)

```bash
set DATABASE_URL=postgresql://username:password@localhost:5432/database
```

- Linux/Ubuntu (Terminal)

```bash
export DATABASE_URL="postgresql://username:password@localhost:5432/database"
```

> [!NOTE]  
> Replace username, password and localhost with your actual credentials

## 🚀 Usage

### Import

Examples

```python
# Models
from aclimate_v3_orm.models import (
    ClimateHistoricalMonthly,
    MngCountry,
    MngLocation
)
#Services
from aclimate_v3_orm.services import (
    ClimateHistoricalMonthlyService,
    MngCountryService,
    MngLocationService
)
#Schemas
from aclimate_v3_orm.schemas import (
    LocationCreate, LocationRead, LocationUpdate,
    CountryCreate, CountryRead, CountryUpdate,
    ClimateHistoricalClimatologyCreate, ClimateHistoricalClimatologyRead, ClimateHistoricalClimatologyUpdate
)
```

### Using

```python

#Init service
country_service = MngCountryService()

#Create new register
new_country = CountryCreate(
    name= "Colombia",
    iso2= "CL",
    enable= True
)

country = country_service.create(obj_in=new_country)

print(country)

#Get register
countries = country_service.get_all()
print(countries)

```

## 🧪 Testing

### Test Structure

The test suite is organized to validate all service components:

```bash
tests/
├── conftest.py #test config
├── test_climate_historical_climatology_service.py
├── test_climate_historical_daily_service.py
├── test_climate_historical_monthly_service.py
├── test_mng_admin_1_service.py
├── test_mng_admin_2_service.py
├── test_mng_climate_measure_service.py
├── test_mng_country_service.py
└── test_mng_location_service.py
```

### Key Characteristics

1. **Service-Centric Testing**:

   - Each production service has a dedicated test file
   - Tests validate both business logic and database interactions

2. **Test Categories**:

   - **Climate Services**: Focus on temporal data operations
   - **Management Services**: Validate CRUD operations for reference data

3. **Configuration**:

   - `conftest.py` contains:
     - Database fixtures (in-memory SQLite)
     - Mock configurations
     - Shared test utilities

4. **Testing Approach**:
   - 100% service layer coverage
   - Integration-style tests with real database operations
   - Mocking only for external dependencies

### Example Test Execution

```bash
# Set up environment
python -m venv env
source env/bin/activate
# Install test dependencies
pip install pytest pytest-mock pytest-cov
# Run all tests
PYTHONPATH=$PYTHONPATH:./src pytest tests/

# Specific test examples:
pytest tests/test_climate_historical_daily_service.py -v  # Run specific test file
pytest -k "test_get_daily_data"  # Run tests matching pattern
```

> [!NOTE]  
> All tests use an isolated SQLite in-memory database configured in conftest.py, ensuring test independence and execution speed.

## 🔄 CI/CD Pipeline Overview

### Workflow Architecture

Our GitHub Actions pipeline implements a three-stage deployment process:

```bash
Code Push → Test Stage → Merge Stage → Release Stage
```

### 1. Test & Validate Phase

**Purpose**: Quality assurance  
**Trigger**:

- Pushes to `stage` branch
- New version tags (`v*`)  
  **Key Actions**:
- Creates isolated Python 3.10 environment
- Installs dependencies + test packages
- Executes complete test suite against in-memory SQLite
- Generates coverage reports
- Enforces 100% service layer test coverage

**Exit Criteria**: All tests must pass before progression

### 2. Merge Phase

**Purpose**: Stable code promotion  
**Dependencies**: Requires Test Phase success  
**Automation**:

- Auto-merges `stage` → `main` using branch protection rules
- Validates no merge conflicts exist
- Maintains linear commit history

### 3. Release Phase

**Purpose**: Versioned artifact delivery  
**Key Processes**:

1. **Semantic Versioning**:

   - Analyzes commit history for version bump type
   - Generates new `vX.Y.Z` tag
   - Updates `setup.py` version automatically

2. **Artifact Packaging**:

   - Creates production-ready ZIP bundle
   - Includes all runtime dependencies

3. **Release Management**:
   - Publishes GitHub Release with changelog
   - Attaches versioned binary asset
   - Notifies stakeholders

**Key Benefits**:

- Zero-touch deployment from commit to production
- Enforced quality standards
- Traceable version history
- Automated semantic versioning

## 📊 Project Structure

```bash
aclimate_v3_orm/
│
├── .github/
│ └── workflows/ # CI/CD pipeline configurations
│
├── src/
│ └── aclimate_v3_orm/
│     ├── models/ # SQLAlchemy ORM models
│     ├── schemas/ # Pydantic schemas for validation
│     ├── services/ # Service layer for database operations
│     ├── validations/ # Validation logic
│     ├── enums/ # Application enumerations for type-safe fixed value sets
│     └── database/ # Database connection management
│
├── tests/ # Test suite organized by service
├── pyproject.toml # Package configuration
└── requirements.txt # Package dependencies
```
