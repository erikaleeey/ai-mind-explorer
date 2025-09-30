# backend/services/graph_service.py
from __future__ import annotations

from datetime import datetime
from typing import Any, Optional, Dict

from neo4j import GraphDatabase
from app.services.base_graph_service import BaseGraphService
import uuid


class GraphService(BaseGraphService):
    """
    Neo4j implementation of the graph service.
    graph database that excels at:
    - Storing nodes (entities) and relationships between them
    - Fast traversals across connected data
    - Pattern matching with Cypher query language
    
    """
    def __init__(self, uri: str, user: str, password: str) -> None:
        """
        Initialize connection to Neo4j database.
        
        Args:
            uri: Neo4j connection string (e.g., "bolt://localhost:7687")
            user: Database username
            password: Database password
        """
        self.driver = GraphDatabase.driver(uri, auth=(user, password))

    def close(self) -> None:
        """Clean up the database driver connection."""
        self.driver.close()

    def create_node(self, label: str, properties: Dict[str, Any]) -> str:
        """
        Create a new node in Neo4j with automatic ID and timestamp generation.
        
        This method automatically adds:
        - A unique UUID as the 'id' property
        - A 'created_at' timestamp
        
        """
        # Generate unique identifier for the node using UUID 128 bit value 
        node_id = str(uuid.uuid4())
        # Merge user properties with system properties
        #props is a dictionary for properties
        props = {**properties, "id": node_id, "created_at": datetime.utcnow().isoformat()}
        
        # Cypher query to create node with dynamic label
        cypher = f"""
        CREATE (n:{label})
        SET n += $props
        RETURN n.id AS id
        """
        #create new node with label, assign all key value pairs from the props dictionary
        #cypher return node id
        
        # run a cypher query within a session (auto-closes connection)
        #driver sends query, neo4j engine parses cypher query into syntax tree, neo4j executes, results sent back over bolt connection
        with self.driver.session() as session:
            rec = session.run(cypher, props=props).single()
            return rec["id"]

    def get_node(self, node_id: str) -> Optional[Dict[str, Any]]:
        """
        Retrieve a node by its unique ID.
        
        Args:
            node_id: The UUID assigned when the node was created
            
        Returns:
            Dictionary of node properties, or None if node doesn't exist
        """
        # Cypher query to find node by ID property
        cypher = """
        MATCH (n {id: $id})
        RETURN n AS node
        """
        
        with self.driver.session() as session:
            rec = session.run(cypher, id=node_id).single()
            if not rec:
                return None
            node = rec["node"]
            # Convert Neo4j Node object to plain Python dictionary
            return dict(node)

    def create_relationship(
        self,
        from_id: str,
        to_id: str,
        rel_type: str,
        properties: Optional[Dict[str, Any]] = None,
    ) -> bool:
        """
        Create a directed relationship between two nodes.
        
        This is the core of graph database functionality - connecting entities.
        Uses MERGE to avoid duplicate relationships (idempotent operation).

        
        Args:
            from_id: Source node ID
            to_id: Target node ID
            rel_type: Relationship type (will be uppercase in Neo4j)
            properties: Optional data to store on the relationship
            
        Returns:
            bool: True if relationship was created/updated successfully
        """
        props = properties or {}
        
        # Cypher query using MERGE to create relationship if it doesn't exist
        cypher = f"""
        MATCH (a {{id: $from_id}}), (b {{id: $to_id}})
        MERGE (a)-[r:{rel_type}]->(b)
        SET r += $props
        RETURN count(r) AS c
        """
        
        with self.driver.session() as session:
            result = session.run(cypher, from_id=from_id, to_id=to_id, props=props).single()
            return result["c"] > 0
