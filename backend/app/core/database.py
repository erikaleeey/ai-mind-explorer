from app.core.config import Settings
from app.services.graph_service import GraphService
from typing import Generator, Optional
import logging

logger = logging.getLogger(__name__)

# Global settings instance
settings = Settings()

# Global graph service instance (lazy-initialized)
_graph_service: Optional[GraphService] = None


def get_graph_service() -> GraphService:
    """
    Get or create the Neo4j graph service instance.
    This follows the singleton pattern to reuse database connections.
    """
    global _graph_service

    if _graph_service is None:
        logger.info(f"Initializing Neo4j connection to {settings.neo4j_uri}")
        _graph_service = GraphService(
            uri=settings.neo4j_uri,
            user=settings.neo4j_user,
            password=settings.neo4j_password.get_secret_value()
        )

    return _graph_service


async def test_neo4j_connection() -> dict:
    """
    Test the Neo4j database connection.
    Returns connection status and basic info.
    """
    try:
        graph = get_graph_service()

        # Simple query to test connection
        with graph.driver.session() as session:
            result = session.run("RETURN 1 AS test")
            result.single()

        logger.info("Neo4j connection test successful")
        return {
            "status": "connected",
            "uri": settings.neo4j_uri,
            "user": settings.neo4j_user
        }
    except Exception as e:
        logger.error(f"Neo4j connection test failed: {e}")
        return {
            "status": "error",
            "error": str(e),
            "uri": settings.neo4j_uri
        }


def close_graph_service():
    """Close the graph service connection on shutdown"""
    global _graph_service
    if _graph_service is not None:
        _graph_service.close()
        _graph_service = None
        logger.info("Neo4j connection closed")
