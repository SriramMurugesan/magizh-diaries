from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from app.routers import admin, public

app = FastAPI(
    title="Student Diary System",
    description="API for managing student diaries and marks with parent share links",
    version="1.0.0"
)

# CORS middleware
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # Configure this properly in production
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Include routers
app.include_router(admin.router, prefix="/api")
app.include_router(public.router, prefix="/api")


@app.get("/")
def root():
    return {
        "message": "Student Diary System API",
        "docs": "/docs",
        "admin_endpoints": "/api/admin",
        "public_endpoints": "/api/share"
    }


@app.get("/health")
def health_check():
    return {"status": "healthy"}
