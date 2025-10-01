from fastapi import APIRouter, HTTPException, Depends
from app.models.thought_models import (
    ProcessPromptRequest,
    ReasoningChain,
    UpdateNodeRequest,
    ThoughtNode
)
from app.services.llm_service import LLMService
from app.core.config import Settings
from app.core.database import get_graph_service
from app.services.graph_service import GraphService
import uuid
import logging
from datetime import datetime

logger = logging.getLogger(__name__)

router = APIRouter(prefix="/api/reasoning", tags=["reasoning"])

# Initialize settings
settings = Settings()


def get_llm_service() -> LLMService:
    """Dependency to get LLM service"""
    # Try Gemini first (preferred), fallback to OpenAI
    gemini_key = settings.gemini_api_key if hasattr(settings, 'gemini_api_key') else None
    openai_key = settings.openai_api_key

    if gemini_key:
        return LLMService(api_key=gemini_key.get_secret_value(), provider="gemini")
    elif openai_key:
        return LLMService(api_key=openai_key.get_secret_value(), provider="openai")
    else:
        raise HTTPException(
            status_code=500,
            detail="No API key configured. Please set GEMINI_API_KEY or OPENAI_API_KEY in your .env file"
        )


@router.post("/process", response_model=ReasoningChain)
async def process_prompt(
    request: ProcessPromptRequest,
    llm_service: LLMService = Depends(get_llm_service)
):
    """
    Process a user prompt and generate a reasoning chain.

    This endpoint:
    1. Takes a user prompt
    2. Uses LLM to generate explicit reasoning steps
    3. Returns the reasoning chain as a graph structure

    The reasoning chain includes:
    - Thought nodes (question, retrieval, reasoning, conclusion)
    - Edges showing how thoughts connect
    - Confidence levels for each step
    """
    try:
        # Generate unique session ID
        session_id = str(uuid.uuid4())

        logger.info(f"Processing prompt for session {session_id}: {request.prompt[:100]}...")

        # Generate reasoning chain using LLM
        reasoning_data = await llm_service.generate_reasoning_chain(
            prompt=request.prompt,
            session_id=session_id
        )

        # Get graph service and persist to Neo4j
        graph = get_graph_service()

        # Store session node
        session_node_id = graph.create_node("Session", {
            "session_id": session_id,
            "prompt": request.prompt,
            "status": "completed"
        })

        # Store thought nodes in Neo4j
        node_id_map = {}  # Map internal IDs to Neo4j IDs
        for node_data in reasoning_data["nodes"]:
            neo4j_id = graph.create_node("ThoughtNode", {
                "node_id": node_data["id"],
                "type": node_data["type"],
                "content": node_data["content"],
                "confidence": node_data["confidence"],
                "session_id": session_id
            })
            node_id_map[node_data["id"]] = neo4j_id

            # Link thought to session
            graph.create_relationship(session_node_id, neo4j_id, "HAS_THOUGHT")

        # Store edges in Neo4j
        for edge_data in reasoning_data["edges"]:
            source_neo4j_id = node_id_map.get(edge_data["source_id"])
            target_neo4j_id = node_id_map.get(edge_data["target_id"])

            if source_neo4j_id and target_neo4j_id:
                graph.create_relationship(
                    source_neo4j_id,
                    target_neo4j_id,
                    "LEADS_TO",
                    {"label": edge_data["label"], "confidence": edge_data.get("confidence", 1.0)}
                )

        # Create response
        reasoning_chain = ReasoningChain(
            session_id=session_id,
            prompt=request.prompt,
            nodes=reasoning_data["nodes"],
            edges=reasoning_data["edges"],
            status="completed",
            created_at=datetime.utcnow().isoformat()
        )

        logger.info(f"Successfully processed and saved prompt for session {session_id}")

        return reasoning_chain

    except Exception as e:
        logger.error(f"Error processing prompt: {e}")
        raise HTTPException(
            status_code=500,
            detail=f"Failed to process prompt: {str(e)}"
        )


@router.get("/session/{session_id}", response_model=ReasoningChain)
async def get_reasoning_session(session_id: str):
    """
    Retrieve a reasoning chain by session ID.

    Note: In this MVP version, we return a not found error.
    In Phase 1.5, we'll add Neo4j persistence to store and retrieve sessions.
    """
    raise HTTPException(
        status_code=404,
        detail="Session retrieval not yet implemented. Coming in Phase 1.5!"
    )


@router.put("/session/{session_id}/node/{node_id}")
async def update_node(
    session_id: str,
    node_id: str,
    update: UpdateNodeRequest
):
    """
    Update a thought node and re-run reasoning from that point.

    This is the key innovation: users can edit reasoning steps
    and see how it affects the conclusion!

    Note: Full implementation coming in Phase 2 (Interactive Editing)
    """
    raise HTTPException(
        status_code=501,
        detail="Node editing coming in Phase 2! Stay tuned..."
    )


@router.get("/health")
async def reasoning_health():
    """Health check for reasoning service"""
    api_key_configured = settings.openai_api_key is not None

    return {
        "status": "healthy",
        "llm_configured": api_key_configured,
        "model": "gpt-4o-mini"
    }
