from abc import ABC, abstractmethod
from typing import Dict, Optional, List
import logging

logger = logging.getLogger(__name__)

class BaseGraphService(ABC):
    """
    Abstract base class for graph database operations.
    
    This provides a common interface for interacting with graph databases,
    allowing the system to switch between different graph database implementations
    (like Neo4j) without changing the calling code.
    """
    
    @abstractmethod
    def create_node(self, label: str, properties: Dict) -> str:
        """
        Create a node in the graph database.
        
        Args:
            label: The type/category of the node (e.g., 'Concept', 'Document', 'Person')
            properties: Key-value pairs of data to store on the node
            
        Returns:
            str: Unique identifier for the created node
        """
        pass
    
    @abstractmethod
    def get_node(self, node_id: str) -> Optional[Dict]:
        """
        Retrieve a node and its properties by unique ID.
        
        Args:
            node_id: The unique identifier of the node
            
        Returns:
            Dict containing the node's properties, or None if not found
        """
        pass
    
    @abstractmethod
    def create_relationship(self, from_id: str, to_id: str, 
                          rel_type: str, properties: Dict = None) -> bool:
        """
        Create a directed relationship between two nodes.
        
        This is where graph databases shine - representing how entities relate.
        Examples: 'REFERENCES', 'CONTAINS', 'AUTHORED_BY', 'RELATED_TO'
        
        Args:
            from_id: ID of the source node
            to_id: ID of the target node  
            rel_type: Type of relationship (e.g., 'REFERENCES', 'CONTAINS')
            properties: Optional data to store on the relationship
            
        Returns:
            bool: True if relationship was created successfully
        """
        pass

