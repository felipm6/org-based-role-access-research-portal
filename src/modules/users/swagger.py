# Users service Swagger examples

from src.modules.auth.swagger import UNAUTHORIZED_ERROR

# Simple example responses
GET_USERS_RESPONSES = {
    200: {
        "description": "Users retrieved successfully",
        "content": {
            "application/json": {
                "example": [
                    {
                        "id": 1,
                        "username": "john_doe",
                        "email": "john@company.com",
                        "full_name": "John Doe",
                        "role": "ADMIN",
                        "organization_id": 1,
                        "is_active": True,
                        "created_at": "2025-09-04T10:00:00Z",
                        "updated_at": "2025-09-04T10:00:00Z",
                    }
                ]
            }
        },
    },
    **UNAUTHORIZED_ERROR,
}

CREATE_USER_RESPONSES = {
    201: {
        "description": "User created successfully",
        "content": {
            "application/json": {
                "example": {
                    "id": 2,
                    "username": "new_user",
                    "email": "newuser@company.com",
                    "full_name": "New User",
                    "role": "RESEARCH_ASSISTANT",
                    "organization_id": 1,
                    "is_active": True,
                    "created_at": "2025-09-04T10:00:00Z",
                    "updated_at": "2025-09-04T10:00:00Z",
                }
            }
        },
    },
    **UNAUTHORIZED_ERROR,
}

GET_PROFILE_RESPONSES = {
    200: {
        "description": "User profile retrieved successfully",
        "content": {
            "application/json": {
                "example": {
                    "id": 1,
                    "username": "john_doe",
                    "email": "john@company.com",
                    "full_name": "John Doe",
                    "role": "ADMIN",
                    "organization_id": 1,
                    "is_active": True,
                    "created_at": "2025-09-04T10:00:00Z",
                    "updated_at": "2025-09-04T10:00:00Z",
                }
            }
        },
    },
    **UNAUTHORIZED_ERROR,
}
