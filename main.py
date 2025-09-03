from fastapi import FastAPI

from src.constants import APP_ENV, VERSION
from src.api.routes import api_router


def create_application() -> FastAPI:
    app = FastAPI(
        title="Org-Based Role Access Control",
        description="Org-Based Role Access Control for Research Portal",
        version=VERSION,
    )

    app.include_router(api_router)

    return app


app = create_application()


@app.get("/")
async def root():
    return {"message": "Research Portal API is running"}


@app.get("/health")
async def health_check():
    return {"status": "healthy", "version": VERSION, "environment": APP_ENV}
