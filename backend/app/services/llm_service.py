from openai import OpenAI
from typing import Dict, List, Optional
import json
import logging
from app.models.thought_models import ThoughtNode, ReasoningEdge, ThoughtType

logger = logging.getLogger(__name__)


class LLMService:
    """Service for interacting with LLMs to extract reasoning chains"""

    def __init__(self, api_key: str, model: str = "gpt-4-turbo-preview"):
        """
        Initialize the LLM service.

        Args:
            api_key: OpenAI API key
            model: Model to use (default: gpt-4-turbo-preview)
        """
        self.client = OpenAI(api_key=api_key)
        self.model = model

    async def generate_reasoning_chain(self, prompt: str, session_id: str) -> Dict:
        """
        Generate a structured reasoning chain from a user prompt.

        This method forces the LLM to externalize its reasoning process
        as a series of connected thought nodes.

        Args:
            prompt: User's question or prompt
            session_id: Session identifier for tracking

        Returns:
            Dict containing nodes and edges of the reasoning chain
        """

        system_prompt = """You are a reasoning engine that externalizes its thought process.

For any question, output your reasoning as a JSON object with this exact structure:
{
  "thoughts": [
    {"id": "1", "type": "question", "content": "Rephrase the question to understand it", "confidence": 0.9},
    {"id": "2", "type": "retrieval", "content": "What information do I need?", "confidence": 0.85},
    {"id": "3", "type": "reasoning", "content": "Apply logic to the information", "confidence": 0.8},
    {"id": "4", "type": "conclusion", "content": "Final answer", "confidence": 0.9}
  ],
  "edges": [
    {"from": "1", "to": "2", "label": "requires"},
    {"from": "2", "to": "3", "label": "informs"},
    {"from": "3", "to": "4", "label": "concludes"}
  ]
}

Types available:
- "question": Understanding/rephrasing the problem
- "retrieval": Identifying needed information or facts
- "reasoning": Applying logic, making connections
- "conclusion": Final answer or result

Rules:
1. Create 3-7 thought nodes
2. Be explicit about your reasoning steps
3. Confidence is 0.0-1.0 (how sure you are of this step)
4. Each thought should be clear and specific
5. Edges show how thoughts connect
6. Content should be detailed enough to understand your thinking

Example for "Why is the sky blue?":
{
  "thoughts": [
    {"id": "1", "type": "question", "content": "The user wants to understand why the sky appears blue to human observers", "confidence": 0.95},
    {"id": "2", "type": "retrieval", "content": "I need to recall information about light, atmosphere, and scattering", "confidence": 0.9},
    {"id": "3", "type": "reasoning", "content": "Sunlight contains all colors. When it hits Earth's atmosphere, shorter wavelengths (blue) scatter more than longer wavelengths due to Rayleigh scattering", "confidence": 0.92},
    {"id": "4", "type": "reasoning", "content": "This scattered blue light comes from all directions in the sky, making it appear blue", "confidence": 0.88},
    {"id": "5", "type": "conclusion", "content": "The sky appears blue because of Rayleigh scattering - blue light's shorter wavelength causes it to scatter more in the atmosphere than other colors", "confidence": 0.93}
  ],
  "edges": [
    {"from": "1", "to": "2", "label": "requires information"},
    {"from": "2", "to": "3", "label": "retrieved knowledge"},
    {"from": "3", "to": "4", "label": "extends reasoning"},
    {"from": "4", "to": "5", "label": "synthesizes into conclusion"}
  ]
}

Now process the user's question and output your reasoning chain."""

        try:
            logger.info(f"Generating reasoning chain for prompt: {prompt[:100]}...")

            response = self.client.chat.completions.create(
                model=self.model,
                messages=[
                    {"role": "system", "content": system_prompt},
                    {"role": "user", "content": prompt}
                ],
                response_format={"type": "json_object"},
                temperature=0.7
            )

            reasoning_data = json.loads(response.choices[0].message.content)

            # Validate and transform the response
            nodes = []
            for thought in reasoning_data.get("thoughts", []):
                # Create ThoughtNode from the LLM response
                node = ThoughtNode(
                    id=f"{session_id}_node_{thought['id']}",
                    type=ThoughtType(thought["type"]),
                    content=thought["content"],
                    confidence=float(thought["confidence"]),
                    session_id=session_id,
                    metadata={"original_id": thought["id"]}
                )
                nodes.append(node)

            # Transform edges to use full node IDs
            edges = []
            for edge in reasoning_data.get("edges", []):
                reasoning_edge = ReasoningEdge(
                    source_id=f"{session_id}_node_{edge['from']}",
                    target_id=f"{session_id}_node_{edge['to']}",
                    label=edge["label"],
                    confidence=edge.get("confidence", 1.0)
                )
                edges.append(reasoning_edge)

            logger.info(f"Generated {len(nodes)} thought nodes with {len(edges)} edges")

            return {
                "nodes": [node.model_dump() for node in nodes],
                "edges": [edge.model_dump() for edge in edges]
            }

        except Exception as e:
            logger.error(f"Error generating reasoning chain: {e}")
            # Return a fallback reasoning chain
            return self._create_fallback_chain(prompt, session_id)

    def _create_fallback_chain(self, prompt: str, session_id: str) -> Dict:
        """
        Create a simple fallback reasoning chain when LLM fails.

        Args:
            prompt: Original user prompt
            session_id: Session ID

        Returns:
            Basic reasoning chain
        """
        nodes = [
            ThoughtNode(
                id=f"{session_id}_node_1",
                type=ThoughtType.QUESTION,
                content=f"Understanding the question: {prompt}",
                confidence=0.7,
                session_id=session_id
            ),
            ThoughtNode(
                id=f"{session_id}_node_2",
                type=ThoughtType.REASONING,
                content="Processing the request...",
                confidence=0.5,
                session_id=session_id
            ),
            ThoughtNode(
                id=f"{session_id}_node_3",
                type=ThoughtType.CONCLUSION,
                content="Unable to generate detailed reasoning at this time.",
                confidence=0.6,
                session_id=session_id
            )
        ]

        edges = [
            ReasoningEdge(
                source_id=f"{session_id}_node_1",
                target_id=f"{session_id}_node_2",
                label="analyzing"
            ),
            ReasoningEdge(
                source_id=f"{session_id}_node_2",
                target_id=f"{session_id}_node_3",
                label="concludes"
            )
        ]

        return {
            "nodes": [node.model_dump() for node in nodes],
            "edges": [edge.model_dump() for edge in edges]
        }
