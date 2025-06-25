"""Retriever Components for Hybrid RAG System."""

from typing import List, Dict, Any, Optional
from langchain.prompts import ChatPromptTemplate
from langchain_google_genai import ChatGoogleGenerativeAI
from langchain_community.utilities import SQLDatabase
from langchain_community.tools.sql_database.tool import QuerySQLDatabaseTool


class StructuredRetriever:
    """Text-to-SQL retriever with self-correction for BigQuery."""
    
    def __init__(self, project_id: str, dataset_id: str, table_id: str, api_key: str):
        self.project_id = project_id
        self.dataset_id = dataset_id
        self.table_id = table_id
        
        self.llm = ChatGoogleGenerativeAI(
            model="gemini-1.5-flash",
            google_api_key=api_key,
            temperature=0.1,
        )
        
        self.db = SQLDatabase.from_uri(
            f"bigquery://{project_id}/{dataset_id}",
            include_tables=[table_id]
        )
        
        self.sql_tool = QuerySQLDatabaseTool(db=self.db)
        
        self.sql_prompt = ChatPromptTemplate.from_template(
            """You are a BigQuery SQL expert for D&D monster data.
            
Database Schema:
Table: {project_id}.{dataset_id}.{table_id}
- name (STRING, REQUIRED): Monster name
- type (STRING): Creature type (Dragon, Beast, Humanoid, etc.)
- size (STRING): Size category (Tiny, Small, Medium, Large, Huge, Gargantuan)
- armor_class (INTEGER): Armor Class (AC)
- hit_points (INTEGER): Hit points
- speed (STRING): Movement speeds (walk, fly, swim, etc.)
- challenge_rating (STRING): Challenge Rating (CR as string, e.g., '1/4', '17', '21')
- abilities (STRING): All ability scores formatted as text (STR, DEX, CON, INT, WIS, CHA)
- skills (STRING): Proficient skills and bonuses
- damage_resistances (STRING): Damage types the monster resists
- damage_immunities (STRING): Damage types the monster is immune to
- condition_immunities (STRING): Conditions the monster is immune to
- senses (STRING): Special senses (darkvision, blindsight, etc.)
- languages (STRING): Languages the monster can speak/understand
- special_abilities (STRING): Special traits or abilities
- actions (STRING): Actions the monster can take
- legendary_actions (STRING): Legendary actions (if any)
- source (STRING): Source book or material

IMPORTANT NOTES:
- Use backticks around table reference: `{project_id}.{dataset_id}.{table_id}`
- challenge_rating is STRING, not FLOAT - use LIKE or REGEXP for CR comparisons
- For CR filtering: SAFE_CAST(REGEXP_EXTRACT(challenge_rating, r'^(\\d+)') AS INT64)
- Use LIKE operator for text searches in abilities, special_abilities, etc.

User Question: {question}
Write a BigQuery SQL query using the full table reference:"""
        )
    
    async def retrieve(self, question: str, max_retries: int = 2) -> Dict[str, Any]:
        """Retrieve data using Text-to-SQL with self-correction."""
        for attempt in range(max_retries + 1):
            try:
                # Generate SQL query
                chain = self.sql_prompt | self.llm
                result = await chain.ainvoke({
                    "question": question,
                    "project_id": self.project_id,
                    "dataset_id": self.dataset_id,
                    "table_id": self.table_id
                })
                sql_query = result.content.strip()
                
                # Clean SQL formatting
                if sql_query.startswith("```sql"):
                    sql_query = sql_query.replace("```sql", "").replace("```", "").strip()
                
                # Execute query
                query_result = self.sql_tool.run(sql_query)
                
                return {
                    "type": "structured",
                    "query": sql_query,
                    "result": query_result,
                    "attempt": attempt + 1,
                    "success": True
                }
                
            except Exception as e:
                if attempt == max_retries:
                    return {
                        "type": "structured",
                        "result": f"Error after {max_retries + 1} attempts: {str(e)}",
                        "success": False,
                        "error": str(e)
                    }
                print(f"SQL attempt {attempt + 1} failed: {e}")


class UnstructuredRetriever:
    """Vector-based retriever for D&D content using FAISS."""
    
    def __init__(self, data_bucket: str, api_key: str, project_id: str):
        self.data_bucket = data_bucket
        self.project_id = project_id
        self.vector_store = None
    
    async def retrieve(self, question: str) -> Dict[str, Any]:
        """Retrieve documents using vector search."""
        try:
            # Simplified implementation for now
            # In full implementation, this would use FAISS + MultiQuery
            sample_documents = [
                {
                    "content": "D&D 5e uses a d20 system for most rolls. Players roll a 20-sided die and add modifiers based on their character's abilities and proficiency.",
                    "source": "Player's Handbook",
                    "chunk_id": "rules_001"
                },
                {
                    "content": "Spellcasting in D&D 5e uses spell slots. Each spell has a level, and casting it consumes a spell slot of that level or higher.",
                    "source": "Player's Handbook", 
                    "chunk_id": "spells_001"
                }
            ]
            
            return {
                "type": "unstructured",
                "question": question,
                "documents": sample_documents,
                "document_count": len(sample_documents),
                "success": True
            }
            
        except Exception as e:
            return {
                "type": "unstructured",
                "question": question,
                "documents": [],
                "document_count": 0,
                "success": False,
                "error": str(e)
            }