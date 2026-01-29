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

## � Database Migrations

This package includes built-in database migration support using **Alembic**. Migrations allow you to version control your database schema changes and safely apply them across different environments.

### 📌 Migration Architecture

**Centralized Approach**: All migrations are maintained within the ORM package and distributed to consuming services (API, Admin, Workers, etc.).

```
aclimate_v3_orm/
└── src/
    └── aclimate_v3_orm/
        └── migrations/
            ├── alembic.ini       # Alembic configuration
            ├── env.py            # Migration environment setup
            └── versions/         # Migration scripts (versioned)
                └── xxxxx_description.py
```

**Benefits**:

- ✅ Single source of truth for schema changes
- ✅ Migrations versioned with the package
- ✅ Consistent schema across all services
- ✅ Automatic conflict prevention via `alembic_version` table

### 🛠️ Development Workflow (ORM Repository)

#### 1. Making Model Changes

After modifying SQLAlchemy models, generate a migration:

```bash
# Navigate to migrations directory
cd src/aclimate_v3_orm

# Generate migration automatically (detects model changes)
alembic revision --autogenerate -m "Add new table or modify existing"

# Review generated migration in migrations/versions/
# Edit if needed to ensure correctness
```

#### 2. Applying Migrations Locally

```bash
# Apply all pending migrations
alembic upgrade head

# View current migration status
alembic current

# View migration history
alembic history

# Rollback last migration (if needed)
alembic downgrade -1

# Rollback all migrations
alembic downgrade base
```

#### 3. Common Development Commands

```bash
# Preview SQL without executing
alembic upgrade head --sql

# Create empty migration (for data migrations)
alembic revision -m "Seed initial data"

# Upgrade to specific revision
alembic upgrade <revision_id>
```

### 🚀 Usage in Services (API/Admin/Workers)

When consuming this ORM package in your services:

#### Option 1: Programmatic Execution (Recommended)

```python
from aclimate_v3_orm.migrations import upgrade, current, downgrade

# Apply all pending migrations
upgrade()  # Equivalent to: alembic upgrade head

# Check current migration version
current()

# Rollback one migration
downgrade("-1")
```

#### Option 2: CLI Execution

```bash
# From your service directory
python -m alembic upgrade head
python -m alembic current
```

#### Option 3: Startup Integration

```python
# In your FastAPI/Flask app startup
from aclimate_v3_orm.migrations import upgrade
from aclimate_v3_orm.database import engine

@app.on_event("startup")
async def run_migrations():
    """Apply database migrations on application startup"""
    try:
        upgrade()
        print("✅ Database migrations applied successfully")
    except Exception as e:
        print(f"❌ Migration failed: {e}")
        raise
```

### 🔐 Multi-Service Safety

**Scenario**: Multiple services (API, Admin) sharing the same database.

**How it works**:

1. Alembic creates a table `alembic_version` in your database
2. This table tracks which migrations have been applied
3. When any service runs `upgrade()`:
   - ✅ **First service**: Acquires lock, applies migrations, updates `alembic_version`
   - ✅ **Second service**: Sees migrations already applied, skips execution
4. No duplicate migrations or conflicts occur

**Important**: Always use the **same package version** across all services:

```bash
# ✅ GOOD - Same version everywhere
API:   pip install aclimate_v3_orm==3.0.1
Admin: pip install aclimate_v3_orm==3.0.1

# ❌ BAD - Different versions
API:   pip install aclimate_v3_orm==3.0.0
Admin: pip install aclimate_v3_orm==3.0.1
```

### 📦 Migration Lifecycle

```
┌─────────────────────────────────────┐
│  1. Developer modifies models       │
│     in aclimate_v3_orm             │
└──────────────┬──────────────────────┘
               ↓
┌─────────────────────────────────────┐
│  2. Generate migration              │
│     alembic revision --autogenerate │
└──────────────┬──────────────────────┘
               ↓
┌─────────────────────────────────────┐
│  3. Test migration locally          │
│     alembic upgrade head            │
└──────────────┬──────────────────────┘
               ↓
┌─────────────────────────────────────┐
│  4. Commit migration to Git         │
│     + Publish new package version   │
└──────────────┬──────────────────────┘
               ↓
┌─────────────────────────────────────┐
│  5. Services upgrade package        │
│     pip install --upgrade ...       │
└──────────────┬──────────────────────┘
               ↓
┌─────────────────────────────────────┐
│  6. Services run migrations         │
│     upgrade() or alembic upgrade    │
└─────────────────────────────────────┘
```

### 🆘 Troubleshooting

**Problem**: Migration says already applied but table doesn't exist

```bash
# Reset migration state
alembic downgrade base
alembic upgrade head
```

**Problem**: Need to mark database as current without running migrations

```bash
# Useful for existing databases
alembic stamp head
```

**Problem**: Want to see what SQL will be executed

```bash
alembic upgrade head --sql > migration.sql
```

## �🚀 Usage

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
