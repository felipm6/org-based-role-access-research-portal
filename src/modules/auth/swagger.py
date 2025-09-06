# Authentication service Swagger examples

AUTH_RESPONSES = {
    200: {
        "description": "Authentication successful",
        "content": {
            "application/json": {
                "example": {"access_token": "string", "token_type": "bearer"}
            }
        },
    },
    401: {
        "description": "Invalid credentials",
        "content": {"application/json": {"example": {"detail": "Invalid credentials"}}},
    },
}

# Common error for protected endpoints
UNAUTHORIZED_ERROR = {
    401: {
        "description": "Authentication required",
        "content": {"application/json": {"example": {"detail": "Not authenticated"}}},
    }
}
