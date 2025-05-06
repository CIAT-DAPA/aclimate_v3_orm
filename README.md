# Aclimate V3 ORM

The goal of this project is to provide a well-structured and scalable Object-Relational Mapping (ORM) system to support the Aclimate platform, a tool designed to process and manage agroclimatic information for decision-making. This ORM facilitates database interactions for models related to climate data, forecast systems, agricultural zones, and administrative boundaries, enabling seamless integration with other components of the Aclimate system.

![GitHub release (latest by date)](https://img.shields.io/github/v/release/CIAT-DAPA/aclimate_v3_orm) ![](https://img.shields.io/github/v/tag/CIAT-DAPA/aclimate_v3_orm)

This is an ORM (Object-Relational Mapping) built with the SQLAlchemy library for interfacing with relational databases.

## Features

- Modular structure organized by domain (climate, forecast, catalog, administrative, etc.)
- Built using SQLAlchemy for efficient relational mapping
- Compatible with Python 3.x
- Designed for integration into larger Aclimate infrastructure

## Getting Started

To use this ORM, you must have a working relational database instance and Python environment.

### Prerequisites

- Python 3.x
- A relational database (PostgreSQL recommended, but also supports MySQL and SQLite)
- [SQLAlchemy](https://www.sqlalchemy.org/) and other dependencies (see `requirements.txt`)

### Environment Configuration

To run the ORM models or integrate them with a database, it's recommended to use a `.env` file for setting environment variables. These are typically loaded using python-dotenv.

Create a `.env` file in the root directory of your project with the following content:

```bash
DATABASE_URL=postgresql://username:password@localhost:5432/aclimate_db
```

### Installation

To install this ORM as a Python package directly from GitHub:

```bash
pip install git+https://github.com/CIAT-DAPA/aclimate_v3_orm
```

To install a specific version:

```bash
pip install git+https://github.com/CIAT-DAPA/aclimate_v3_orm@v0.1.0
```

### Usage

You can import models directly from the `src/aclimate_v3_orm/models` module in your project:

```bash
from models.climate import ClimateHistoricalDaily
from models.catalog import ClimateMeasure
from models.administrative import Location
```

To explore the full model structure, navigate to the `src/aclimate_v3_orm/models` directory.
