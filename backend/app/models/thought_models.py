from pydantic import BaseModel, Field
from enum import Enum
from typing import List, Optional, Dict, Any
from datetime import datetime


class ThoughtType(str, Enum):
    """Types of reasoning steps in the thought process"""
    QUESTION = "question"
    RETRIEVAL = "retrieval"
    REASONING = "reasoning"
    CONCLUSION = "conclusion"


class ThoughtNode(BaseModel):
    """Represents a single step in the AI's reasoning process"""
    id: str = Field(..., description="Unique identifier for this thought node")
    type: ThoughtType = Field(..., description="Type of reasoning step")
    content: str = Field(..., description="The actual thought content")
    confidence: float = Field(..., ge=0.0, le=1.0, description="Confidence level (0-1)")
    session_id: str = Field(..., description="ID of the reasoning session this belongs to")
    metadata: Dict[str, Any] = Field(default_factory=dict, description="Additional metadata")
    created_at: Optional[str] = None

    class Config:
        json_schema_extra = {
            "example": {
                "id": "node_1",
                "type": "question",
                "content": "What factors contribute to sky color?",
                "confidence": 0.95,
                "session_id": "session_123",
                "metadata": {}
            }
        }


class ReasoningEdge(BaseModel):
    """Represents a connection between two thought nodes"""
    source_id: str = Field(..., description="ID of the source thought node")
    target_id: str = Field(..., description="ID of the target thought node")
    label: str = Field(..., description="Relationship description")
    confidence: float = Field(default=1.0, ge=0.0, le=1.0)

    class Config:
        json_schema_extra = {
            "example": {
                "source_id": "node_1",
                "target_id": "node_2",
                "label": "requires information",
                "confidence": 0.9
            }
        }


class ReasoningChain(BaseModel):
    """Complete reasoning process for a user prompt"""
    session_id: str = Field(..., description="Unique session identifier")
    prompt: str = Field(..., description="Original user prompt")
    nodes: List[ThoughtNode] = Field(..., description="All thought nodes in the chain")
    edges: List[ReasoningEdge] = Field(..., description="Connections between nodes")
    status: str = Field(default="completed", description="Status: active, completed, failed")
    created_at: Optional[str] = None
    metadata: Dict[str, Any] = Field(default_factory=dict)

    class Config:
        json_schema_extra = {
            "example": {
                "session_id": "session_123",
                "prompt": "Why is the sky blue?",
                "nodes": [],
                "edges": [],
                "status": "completed"
            }
        }


class ProcessPromptRequest(BaseModel):
    """Request to process a user prompt and generate reasoning"""
    prompt: str = Field(..., min_length=1, max_length=2000, description="User's question or prompt")

    class Config:
        json_schema_extra = {
            "example": {
                "prompt": "Why is the sky blue?"
            }
        }


class UpdateNodeRequest(BaseModel):
    """Request to update a thought node"""
    content: str = Field(..., description="Updated thought content")
    confidence: float = Field(..., ge=0.0, le=1.0, description="Updated confidence level")

    class Config:
        json_schema_extra = {
            "example": {
                "content": "The sky appears blue due to Rayleigh scattering",
                "confidence": 0.92
            }
        }
