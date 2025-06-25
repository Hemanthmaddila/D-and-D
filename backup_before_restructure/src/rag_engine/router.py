"""
Query Router for Hybrid RAG System

This module implements the intelligent routing mechanism that classifies user queries
as either 'structured' (requiring database queries) or 'unstructured' (requiring
vector search) based on their intent and content.
"""

from typing import Literal
from langchain.prompts import ChatPromptTemplate
from langchain_google_genai import ChatGoogleGenerativeAI
from langchain.schema.runnable import RunnableLambda

class QueryRouter:
    """
    Intelligent query router that uses Gemini to classify D&D-related queries.
    
    The router determines whether a query should be handled by:
    - Structured path: Text-to-SQL queries against BigQuery monster data
    - Unstructured path: Vector search against D&D SRD text content
    """
    
    def __init__(self, api_key: str, model_name: str = "gemini-1.5-flash"):
        """
        Initialize the query router.
        
        Args:
            api_key: Google API key for Gemini
            model_name: Gemini model to use for classification
        """
        self.llm = ChatGoogleGenerativeAI(
            model=model_name,
            google_api_key=api_key,
            temperature=0.1,  # Low temperature for consistent classification
        )
        
        self.router_prompt = ChatPromptTemplate.from_template(
            """You are an expert query routing assistant for a Dungeons & Dragons knowledge base. \
Your task is to classify the user's question into one of two categories based on its intent: 'structured' or 'unstructured'.

'structured' questions ask for specific, factual data about game entities, such as monster statistics. These questions often involve numbers, lists, comparisons, or filtering. \
Examples: 
- "What is a Beholder's armor class?"
- "List all monsters with resistance to cold damage."
- "Which dragon has more hit points, an adult red or an adult black?"
- "Show me all CR 5 monsters."
- "What monsters have a Strength score above 20?"

'unstructured' questions ask about rules, lore, spell descriptions, or ask for creative narrative content. These questions are typically explanatory or generative in nature. \
Examples: 
- "How does the grappling condition work?"
- "Can you describe a spooky, haunted forest?"
- "What is the history of the elves in the Forgotten Realms?"
- "Explain how spell slots work in D&D 5e."
- "Create a description for a tavern scene."

Based on the user's question below, output only the single word 'structured' or 'unstructured' and nothing else.

User Question: {question}
Classification:"""
        )
        
        # Create the router chain
        self.router_chain = self.router_prompt | self.llm
    
    async def route_query(self, question: str) -> Literal["structured", "unstructured"]:
        """
        Route a query to the appropriate retrieval path.
        
        Args:
            question: The user's question to classify
            
        Returns:
            Either "structured" or "unstructured" indicating the routing decision
        """
        try:
            # Get classification from Gemini
            result = await self.router_chain.ainvoke({"question": question})
            classification = result.content.strip().lower()
            
            # Ensure we return a valid classification
            if classification in ["structured", "unstructured"]:
                return classification
            else:
                # Default to unstructured if classification is unclear
                print(f"Warning: Unclear classification '{classification}', defaulting to 'unstructured'")
                return "unstructured"
                
        except Exception as e:
            print(f"Error in query routing: {e}")
            # Default to unstructured path on error
            return "unstructured"
    
    def create_routing_runnable(self):
        """
        Create a LangChain Runnable for integration with LCEL chains.
        
        Returns:
            A RunnableLambda that can be used in LangChain pipelines
        """
        async def route_function(inputs: dict) -> dict:
            question = inputs.get("question", "")
            route = await self.route_query(question)
            return {"question": question, "route": route}
        
        return RunnableLambda(route_function)


def create_conditional_chain(router: QueryRouter, structured_chain, unstructured_chain):
    """
    Create a conditional chain that routes queries based on classification.
    
    Args:
        router: QueryRouter instance
        structured_chain: Chain for handling structured queries
        unstructured_chain: Chain for handling unstructured queries
        
    Returns:
        A complete routing chain that directs queries to appropriate handlers
    """
    from langchain.schema.runnable import RunnableBranch
    
    async def route_to_chain(inputs: dict):
        """Route inputs to the appropriate chain based on classification."""
        route = inputs.get("route")
        question = inputs.get("question")
        
        if route == "structured":
            return await structured_chain.ainvoke({"question": question})
        else:
            return await unstructured_chain.ainvoke({"question": question})
    
    # Create the complete routing pipeline
    routing_chain = (
        router.create_routing_runnable() 
        | RunnableLambda(route_to_chain)
    )
    
    return routing_chain 