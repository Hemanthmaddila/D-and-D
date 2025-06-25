"""Hybrid RAG Engine for the Dungeon Master's Oracle."""

from typing import Dict, Any, Optional
from langchain.prompts import ChatPromptTemplate
from langchain_google_genai import ChatGoogleGenerativeAI

from .router import QueryRouter
from .retrievers import StructuredRetriever, UnstructuredRetriever


class HybridRAGEngine:
    """Main orchestrator for the hybrid RAG system."""
    
    def __init__(
        self,
        project_id: str,
        dataset_id: str,
        table_id: str,
        data_bucket: str,
        api_key: str,
        model_name: str = "gemini-1.5-flash"
    ):
        self.project_id = project_id
        self.dataset_id = dataset_id
        self.table_id = table_id
        self.data_bucket = data_bucket
        self.api_key = api_key
        
        # Initialize components
        self.router = QueryRouter(api_key, model_name)
        self.structured_retriever = StructuredRetriever(
            project_id, dataset_id, table_id, api_key
        )
        self.unstructured_retriever = UnstructuredRetriever(
            data_bucket, api_key, project_id
        )
        
        # Response generator
        self.response_llm = ChatGoogleGenerativeAI(
            model=model_name,
            google_api_key=api_key,
            temperature=0.7,
        )
        
        # Response prompts
        self.structured_response_prompt = ChatPromptTemplate.from_template(
            """You are a helpful Dungeon Master assistant with access to D&D monster data.

The user asked: "{question}"

Database results:
{retrieved_data}

Provide a clear, helpful answer based on this data:"""
        )
        
        self.unstructured_response_prompt = ChatPromptTemplate.from_template(
            """You are a master Dungeon Master, an expert in D&D 5th Edition.

The user asked: "{question}"

Relevant D&D information:
{retrieved_documents}

Provide a comprehensive and engaging answer:"""
        )
    
    async def query(self, question: str, session_id: Optional[str] = None) -> Dict[str, Any]:
        """Process a user query through the hybrid RAG pipeline."""
        try:
            # Route the query
            route = await self.router.route_query(question)
            print(f"Query routed to: {route}")
            
            # Retrieve information
            if route == "structured":
                retrieval_result = await self.structured_retriever.retrieve(question)
                response = await self._generate_structured_response(question, retrieval_result)
            else:
                retrieval_result = await self.unstructured_retriever.retrieve(question)
                response = await self._generate_unstructured_response(question, retrieval_result)
            
            return {
                "answer": response,
                "route": route,
                "sources": self._extract_sources(retrieval_result),
                "retrieval_success": retrieval_result.get("success", False),
                "session_id": session_id,
                "metadata": {
                    "query_type": route,
                    "retrieval_metadata": retrieval_result
                }
            }
            
        except Exception as e:
            print(f"Error in hybrid RAG query: {e}")
            return {
                "answer": f"I encountered an error: {str(e)}. Please try rephrasing your question.",
                "route": "error",
                "sources": [],
                "retrieval_success": False,
                "session_id": session_id,
                "error": str(e)
            }
    
    async def _generate_structured_response(self, question: str, retrieval_result: Dict[str, Any]) -> str:
        """Generate response for structured data."""
        try:
            if not retrieval_result.get("success"):
                return f"Database error: {retrieval_result.get('result', 'Unknown error')}"
            
            chain = self.structured_response_prompt | self.response_llm
            result = await chain.ainvoke({
                "question": question,
                "retrieved_data": retrieval_result.get("result", "No data found")
            })
            return result.content.strip()
            
        except Exception as e:
            return f"Error generating response: {str(e)}"
    
    async def _generate_unstructured_response(self, question: str, retrieval_result: Dict[str, Any]) -> str:
        """Generate response for unstructured data."""
        try:
            if not retrieval_result.get("success"):
                return f"Knowledge base error: {retrieval_result.get('error', 'Unknown error')}"
            
            documents = retrieval_result.get("documents", [])
            doc_text = "\n\n".join([
                f"Source: {doc.get('source', 'Unknown')}\nContent: {doc.get('content', '')}"
                for doc in documents
            ])
            
            chain = self.unstructured_response_prompt | self.response_llm
            result = await chain.ainvoke({
                "question": question,
                "retrieved_documents": doc_text or "No relevant information found."
            })
            return result.content.strip()
            
        except Exception as e:
            return f"Error generating response: {str(e)}"
    
    def _extract_sources(self, retrieval_result: Dict[str, Any]) -> list:
        """Extract sources from retrieval results."""
        sources = []
        
        if retrieval_result.get("type") == "structured":
            if retrieval_result.get("success"):
                sources.append("D&D Monster Database")
        elif retrieval_result.get("type") == "unstructured":
            documents = retrieval_result.get("documents", [])
            for doc in documents:
                source = doc.get("source", "D&D SRD")
                if source not in sources:
                    sources.append(source)
        
        return sources
    
    async def narrate(self, prompt: str, style: str = "descriptive") -> Dict[str, Any]:
        """Generate creative narrative content."""
        try:
            narrative_prompt = ChatPromptTemplate.from_template(
                """You are a master Dungeon Master and expert storyteller.
Your tone is {style}, engaging, and immersive.

Create narrative content for: "{prompt}"

Use vivid descriptions and sensory details. Keep it suitable for D&D games.

Narrative:"""
            )
            
            chain = narrative_prompt | self.response_llm
            result = await chain.ainvoke({
                "prompt": prompt,
                "style": style
            })
            
            return {
                "text": result.content.strip(),
                "style": style,
                "success": True
            }
            
        except Exception as e:
            return {
                "text": f"Error creating narrative: {str(e)}",
                "style": style,
                "success": False,
                "error": str(e)
            }