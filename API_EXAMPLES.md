# API Examples

This document provides practical cURL examples for testing the Research Portal API endpoints.

## Prerequisites

1. Server running on `http://localhost:8000`
2. Database populated with sample data (run `python populate_database.py`)

## 🔐 Authentication

**Login to get JWT token:**

```bash
curl -X POST "http://localhost:8000/api/auth" \
  -H "Content-Type: application/json" \
  -d '{
    "client_id": "admin",
    "client_secret": "admin1234"
  }'
```

**Response:**

```json
{
  "access_token": "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9...",
  "token_type": "Bearer"
}
```

## 👥 User Management

**Get all users in organization:**

```bash
curl -X GET "http://localhost:8000/api/users/" \
  -H "Authorization: Bearer YOUR_JWT_TOKEN"
```

**Response:**

```json
[
  {
    "id": "550e8400-e29b-41d4-a716-446655440000",
    "client_id": "admin",
    "email": "admin@research.edu",
    "name": "Admin User",
    "org_id": "550e8400-e29b-41d4-a716-446655440001",
    "role": "admin"
  },
  {
    "id": "550e8400-e29b-41d4-a716-446655440002",
    "client_id": "study_coordinator",
    "email": "coordinator@research.edu",
    "name": "Study Coordinator User",
    "org_id": "550e8400-e29b-41d4-a716-446655440001",
    "role": "study_coordinator"
  }
]
```

**Create a new user (Admin only):**

```bash
curl -X POST "http://localhost:8000/api/users/" \
  -H "Authorization: Bearer YOUR_JWT_TOKEN" \
  -H "Content-Type: application/json" \
  -d '{
    "client_id": "new_user",
    "client_secret": "password123",
    "email": "newuser@research.edu",
    "name": "New User",
    "role": "research_assistant"
  }'
```

**Response:**

```json
{
  "id": "550e8400-e29b-41d4-a716-446655440003",
  "client_id": "new_user",
  "email": "newuser@research.edu",
  "name": "New User",
  "org_id": "550e8400-e29b-41d4-a716-446655440001",
  "role": "research_assistant"
}
```

**Change user role (Admin only):**

```bash
curl -X PUT "http://localhost:8000/api/users/550e8400-e29b-41d4-a716-446655440003/role" \
  -H "Authorization: Bearer YOUR_JWT_TOKEN" \
  -H "Content-Type: application/json" \
  -d '{
    "role": "study_coordinator"
  }'
```

**Response:**

```json
{
  "id": "550e8400-e29b-41d4-a716-446655440003",
  "client_id": "new_user",
  "email": "newuser@research.edu",
  "name": "New User",
  "org_id": "550e8400-e29b-41d4-a716-446655440001",
  "role": "study_coordinator"
}
```

## 📝 Complete Workflow Example

1. **Login as admin:**

```bash
# Get token
TOKEN=$(curl -s -X POST "http://localhost:8000/api/auth" \
  -H "Content-Type: application/json" \
  -d '{"client_id": "admin", "client_secret": "admin1234"}' \
  | jq -r '.access_token')
```

2. **View current users:**

```bash
curl -X GET "http://localhost:8000/api/users/" \
  -H "Authorization: Bearer $TOKEN"
```

**Response:**

```json
[
  {
    "id": "550e8400-e29b-41d4-a716-446655440000",
    "client_id": "admin",
    "email": "admin@research.edu",
    "name": "Admin User",
    "org_id": "550e8400-e29b-41d4-a716-446655440001",
    "role": "admin"
  }
]
```

3. **Create a new research assistant:**

```bash
curl -X POST "http://localhost:8000/api/users/" \
  -H "Authorization: Bearer $TOKEN" \
  -H "Content-Type: application/json" \
  -d '{
    "client_id": "researcher1",
    "client_secret": "secure123",
    "email": "researcher1@research.edu",
    "name": "Research Assistant 1",
    "role": "research_assistant"
  }'
```

**Response:**

```json
{
  "id": "550e8400-e29b-41d4-a716-446655440004",
  "client_id": "researcher1",
  "email": "researcher1@research.edu",
  "name": "Research Assistant 1",
  "org_id": "550e8400-e29b-41d4-a716-446655440001",
  "role": "research_assistant"
}
```

4. **Promote user to Study Coordinator:**

```bash
curl -X PUT "http://localhost:8000/api/users/550e8400-e29b-41d4-a716-446655440004/role" \
  -H "Authorization: Bearer $TOKEN" \
  -H "Content-Type: application/json" \
  -d '{"role": "study_coordinator"}'
```

**Response:**

```json
{
  "id": "550e8400-e29b-41d4-a716-446655440004",
  "client_id": "researcher1",
  "email": "researcher1@research.edu",
  "name": "Research Assistant 1",
  "org_id": "550e8400-e29b-41d4-a716-446655440001",
  "role": "study_coordinator"
}
```

## 🔒 Permission Examples

**What happens with wrong permissions:**

```bash
# Try to create user as non-admin (will fail with 403)
curl -X POST "http://localhost:8000/api/users/" \
  -H "Authorization: Bearer PARTICIPANT_TOKEN" \
  -H "Content-Type: application/json" \
  -d '{"client_id": "test", "client_secret": "test", "email": "test@test.com", "name": "Test", "role": "admin"}'
```

**Error Response:**

```json
{
  "detail": "Admin access required"
}
```

**Invalid credentials:**

```bash
curl -X POST "http://localhost:8000/api/auth" \
  -H "Content-Type: application/json" \
  -d '{
    "client_id": "admin",
    "client_secret": "wrong_password"
  }'
```

**Error Response:**

```json
{
  "detail": "Invalid credentials"
}
```

**Try to modify user from different organization:**

```bash
curl -X PUT "http://localhost:8000/api/users/different-org-user-id/role" \
  -H "Authorization: Bearer $TOKEN" \
  -H "Content-Type: application/json" \
  -d '{"role": "admin"}'
```

**Error Response:**

```json
{
  "detail": "Cannot modify users from other organizations"
}
```

## Test Credentials

- **Admin**: `admin` / `admin1234`
- **Study Coordinator**: `study_coordinator` / `study_coordinator1234`
- **Research Assistant**: `research_assistant` / `research_assistant1234`
- **Participant**: `participant` / `participant1234`
