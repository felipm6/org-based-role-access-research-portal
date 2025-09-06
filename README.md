# Research Portal API

## Setup

1. Install Python 3.11+
2. Create virtual environment:
   ```bash
   python -m venv .venv
   .venv\Scripts\activate  # Windows
   ```
3. Install dependencies:
   ```bash
   pip install -r requirements.txt
   ```

## Database Setup

1. Create the SQLite database:
   ```bash
   python database_setup.py
   ```

2. Populate with sample data:
   ```bash
   python populate_database.py
   ```

**Test Credentials:**
- Admin: `admin` / `admin1234`
- Study Coordinator: `study_coordinator` / `study_coordinator1234`
- Research Assistant: `research_assistant` / `research_assistant1234`
- Participant: `participant` / `participant1234`

## Run Development Server

```bash
# with uvicorn (from project root)
uvicorn main:app --reload --host 0.0.0.0 --port 8000
```

Visit: http://localhost:8000 for the API
Visit: http://localhost:8000/docs for Swagger documentation

## Project Structure

```
src/
├── __init__.py
├── api/                     # API routes and endpoints
│   └── __init__.py
├── models/                  # Database models
│   └── __init__.py
├── modules/                  # Database models
│   └── __init__.py
└── schemas/                 # Pydantic schemas (request/response models)
    └── __init__.py
tests/                       # Test files
requirements.txt             # Python dependencies
main.py                  # FastAPI app creation and entry point
```

## Architecture

This project implements an organization-based role access control system for a research portal.

### Roles:

- **Participant**: View only their own sessions and assigned study info
- **Research Assistant**: View/edit sessions within their org
- **Study Coordinator**: Same as RA, plus create/edit studies
- **Admin**: Full access to users, studies, sessions within their organization
