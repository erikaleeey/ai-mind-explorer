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
    api_key = settings.openai_api_key
    if not api_key:
        raise HTTPException(
            status_code=500,
            detail="OpenAI API key not configured. Please set OPENAI_API_KEY in your .env file"
        )
    return LLMService(api_key=api_key.get_secret_value())


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

        # Create response
        reasoning_chain = ReasoningChain(
            session_id=session_id,
            prompt=request.prompt,
            nodes=reasoning_data["nodes"],
            edges=reasoning_data["edges"],
            status="completed",
            created_at=datetime.utcnow().isoformat()
        )

        logger.info(f"Successfully processed prompt for session {session_id}")

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
        "model": "gpt-4-turbo-preview"
    }
