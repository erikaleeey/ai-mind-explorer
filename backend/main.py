from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from app.core.config import Settings
from app.core.database import test_neo4j_connection, close_graph_service
from app.api import reasoning
import uvicorn

# Initialize settings
settings = Settings()

# Create FastAPI app
app = FastAPI(
    title=settings.api_title,
    version=settings.api_version,
    description="AI Mind Explorer - Visualize and interact with AI reasoning processes"
)

# Configure CORS
app.add_middleware(
    CORSMiddleware,
    allow_origins=settings.cors_origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Include routers
app.include_router(reasoning.router)


# Startup event
@app.on_event("startup")
async def startup_event():
    print(f"Starting {settings.api_title} v{settings.api_version}")
    print(f"Environment: {settings.environment}")

    # Test Neo4j connection
    neo4j_status = await test_neo4j_connection()
    if neo4j_status["status"] == "connected":
        print(f"✓ Neo4j connected: {neo4j_status['uri']}")
    else:
        print(f"✗ Neo4j connection failed: {neo4j_status.get('error', 'Unknown error')}")


# Shutdown event
@app.on_event("shutdown")
async def shutdown_event():
    print("Shutting down...")
    close_graph_service()


# Health check endpoint
@app.get("/health")
async def health_check():
    neo4j_status = await test_neo4j_connection()

    return {
        "status": "healthy",
        "service": settings.api_title,
        "version": settings.api_version,
        "environment": settings.environment,
        "neo4j": neo4j_status
    }


@app.get("/")
async def root():
    return {
        "message": "AI Mind Explorer API",
        "docs": "/docs",
        "health": "/health"
    }

if __name__ == "__main__":
    uvicorn.run(
        "main:app",
        host=settings.api_host,
        port=settings.api_port,
        reload=True
    )
