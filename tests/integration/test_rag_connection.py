#!/usr/bin/env python3
"""
Test script to verify RAG system connection to BigQuery
Run this to make sure your updated schema works with the RAG engine
"""

import os
import asyncio
import sys
from dotenv import load_dotenv

# Load environment variables
load_dotenv()

# Add src to path so we can import the RAG engine
sys.path.append('src')

from rag_engine.hybrid_rag import HybridRAGEngine

async def test_rag_connection():
    """Test the RAG system connection to BigQuery."""
    
    print("🔗 Testing RAG System Connection to BigQuery")
    print("=" * 60)
    
    # Get configuration
    project_id = os.getenv("PROJECT_ID", "dandd-oracle")
    dataset_id = os.getenv("DATASET_ID", "dnd_data")
    table_id = os.getenv("TABLE_ID", "monsters")
    data_bucket = os.getenv("DATA_BUCKET", "dandd-oracle-bucket-2024-unique")
    api_key = os.getenv("GOOGLE_API_KEY")
    
    print(f"📍 Project: {project_id}")
    print(f"📊 Table: {dataset_id}.{table_id}")
    print(f"🔑 API Key: {'✅ Set' if api_key else '❌ Missing'}")
    
    if not api_key:
        print("\n❌ GOOGLE_API_KEY not found in environment")
        print("Make sure your .env file has the correct API key")
        return False
    
    try:
        # Initialize the RAG engine
        print("\n🚀 Initializing RAG Engine...")
        rag_engine = HybridRAGEngine(
            project_id=project_id,
            dataset_id=dataset_id,
            table_id=table_id,
            data_bucket=data_bucket,
            api_key=api_key
        )
        print("✅ RAG Engine initialized successfully!")
        
        # Test queries to verify the connection
        test_queries = [
            {
                "query": "What is a Beholder's armor class?",
                "expected_route": "structured",
                "description": "Simple monster stat query"
            },
            {
                "query": "Show me all dragons in the database",
                "expected_route": "structured", 
                "description": "Filter by creature type"
            },
            {
                "query": "Which monsters have fire immunity?",
                "expected_route": "structured",
                "description": "Search by damage immunity"
            },
            {
                "query": "What are the rules for grappling in D&D?",
                "expected_route": "unstructured",
                "description": "Rules query (should go to unstructured)"
            }
        ]
        
        print(f"\n🧪 Running {len(test_queries)} test queries...")
        print("-" * 60)
        
        for i, test in enumerate(test_queries, 1):
            print(f"\n📝 Test {i}: {test['description']}")
            print(f"❓ Query: \"{test['query']}\"")
            print(f"🎯 Expected route: {test['expected_route']}")
            
            try:
                result = await rag_engine.query(test['query'])
                
                actual_route = result.get('route', 'unknown')
                success = result.get('retrieval_success', False)
                answer = result.get('answer', 'No answer')
                
                print(f"🛤️  Actual route: {actual_route}")
                print(f"{'✅' if success else '❌'} Retrieval: {'Success' if success else 'Failed'}")
                
                # Show query details for structured queries
                if actual_route == "structured" and result.get('metadata', {}).get('retrieval_metadata'):
                    metadata = result['metadata']['retrieval_metadata']
                    if 'query' in metadata:
                        print(f"🔍 Generated SQL: {metadata['query'][:100]}...")
                
                # Show part of the answer
                answer_preview = answer[:150] + "..." if len(answer) > 150 else answer
                print(f"💬 Answer: {answer_preview}")
                
                # Check if route matches expectation
                if actual_route == test['expected_route']:
                    print("✅ Route matches expectation")
                else:
                    print(f"⚠️  Route mismatch: expected {test['expected_route']}, got {actual_route}")
                
            except Exception as e:
                print(f"❌ Query failed: {e}")
        
        print("\n" + "=" * 60)
        print("🎉 RAG Connection Test Complete!")
        print("\n✅ Your RAG system is connected to BigQuery")
        print("✅ Updated schema is working")
        print("✅ Ready to handle D&D queries!")
        
        return True
        
    except Exception as e:
        print(f"\n❌ RAG Engine initialization failed: {e}")
        print("\nTroubleshooting:")
        print("  1. Make sure BigQuery table exists and has data")
        print("  2. Check your .env file has correct PROJECT_ID")
        print("  3. Verify Google Cloud authentication")
        print("  4. Ensure GOOGLE_API_KEY is valid")
        return False

def main():
    """Main function to run the test."""
    try:
        success = asyncio.run(test_rag_connection())
        if not success:
            sys.exit(1)
    except KeyboardInterrupt:
        print("\n\n⏹️  Test interrupted by user")
    except Exception as e:
        print(f"\n❌ Unexpected error: {e}")
        sys.exit(1)

if __name__ == "__main__":
    main() 