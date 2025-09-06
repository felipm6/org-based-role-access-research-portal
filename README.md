# Research Portal API

**Author:** Felip Martínez

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
├── api/                     # API routes and main router
├── guards/                  # Authentication & authorization logic
├── models/                  # Database models & relationships
├── modules/                 # Feature-based modules
│   ├── auth/               # JWT authentication service
│   └── users/              # User management (CRUD + role changes)
└── connection.py           # Database connection setup
configuration/              # JWT and environment settings
database_setup.py          # Database creation script
populate_database.py       # Sample data seeding
main.py                    # FastAPI app creation and entry point
requirements.txt           # Python dependencies
```

## Architecture

This project implements an organization-based role access control system for a research portal.

### Roles:

- **Participant**: View only their own sessions and assigned study info
- **Research Assistant**: View/edit sessions within their org
- **Study Coordinator**: Same as RA, plus create/edit studies
- **Admin**: Full access to users, studies, sessions within their organization

## Architecture & Design Choices

### Role-Based Access Control Implementation

This project implements **organization-scoped role-based access control** using:

1. **JWT Authentication**: Secure token-based authentication with configurable expiration
2. **Dependency Injection Guards**: FastAPI dependencies that validate roles at the endpoint level
3. **Organization Filtering**: All data access is automatically scoped to the user's organization

### Access Control Enforcement

**Guards (`src/guards/`):**

- `get_current_user()`: Validates JWT tokens and retrieves user from database
- `require_admin()`: Restricts access to Admin users only
- `require_coordinator_or_admin()`: Allows Study Coordinators and Admins

**Permission:**

- **View users**: All authenticated users (within their org)
- **Create users**: Admin only
- **Change user roles**: Admin only
- **Organization scope**: All operations filtered by `user.org_id`

## API Testing

For detailed API examples and cURL commands, see [API_EXAMPLES.md](API_EXAMPLES.md)
