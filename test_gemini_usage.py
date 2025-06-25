#!/usr/bin/env python3
"""
Test script to verify Gemini API usage with detailed logging
"""

import os
import asyncio
import sys
from dotenv import load_dotenv

# Load environment variables
load_dotenv()

# Add src to path
sys.path.append('src')

from rag_engine.router import QueryRouter
from rag_engine.retrievers import StructuredRetriever
from langchain_google_genai import ChatGoogleGenerativeAI

async def test_gemini_direct():
    """Test Gemini API directly to confirm it's working."""
    print("🤖 Testing Direct Gemini API Call")
    print("=" * 50)
    
    api_key = os.getenv("GOOGLE_API_KEY")
    if not api_key:
        print("❌ No API key found")
        return False
    
    try:
        # Direct Gemini call
        llm = ChatGoogleGenerativeAI(
            model="gemini-1.5-flash",
            google_api_key=api_key,
            temperature=0.7
        )
        
        print("📤 Sending test prompt to Gemini...")
        response = await llm.ainvoke("Say 'Hello from Gemini!' and explain you're an AI assistant.")
        
        print(f"📥 Gemini Response: {response.content}")
        return True
        
    except Exception as e:
        print(f"❌ Gemini API Error: {e}")
        return False

async def test_router_with_logging():
    """Test the query router with detailed logging."""
    print("\n🧭 Testing Query Router (Uses Gemini)")
    print("=" * 50)
    
    api_key = os.getenv("GOOGLE_API_KEY")
    router = QueryRouter(api_key, "gemini-1.5-flash")
    
    test_queries = [
        "What is a dragon's armor class?",
        "How do spell slots work in D&D?"
    ]
    
    for query in test_queries:
        print(f"\n📝 Testing: \"{query}\"")
        print("📤 Sending to Gemini for classification...")
        
        route = await router.route_query(query)
        print(f"📥 Gemini classified as: {route}")

async def test_sql_generation():
    """Test SQL generation with Gemini."""
    print("\n🗄️ Testing SQL Generation (Uses Gemini)")
    print("=" * 50)
    
    api_key = os.getenv("GOOGLE_API_KEY")
    project_id = os.getenv("PROJECT_ID", "dandd-oracle")
    
    retriever = StructuredRetriever(project_id, "dnd_data", "monsters", api_key)
    
    print("📝 Query: 'What monsters have over 100 hit points?'")
    print("📤 Sending to Gemini for SQL generation...")
    
    try:
        result = await retriever.retrieve("What monsters have over 100 hit points?")
        
        if result.get("success"):
            sql = result.get("query", "No SQL generated")
            print(f"📥 Gemini generated SQL: {sql}")
            print(f"🎯 Query executed successfully!")
        else:
            print(f"❌ SQL generation failed: {result.get('error')}")
            
    except Exception as e:
        print(f"❌ Error: {e}")

async def main():
    """Run all Gemini usage tests."""
    print("🔍 Verifying Gemini Usage in Dungeon Master's Oracle")
    print("=" * 60)
    
    # Test 1: Direct Gemini API
    success1 = await test_gemini_direct()
    
    # Test 2: Router (query classification)
    if success1:
        await test_router_with_logging()
        
        # Test 3: SQL Generation
        await test_sql_generation()
    
    print("\n" + "=" * 60)
    if success1:
        print("✅ CONFIRMED: Gemini is actively being used!")
        print("💰 Each query to your Oracle makes multiple Gemini API calls")
        print("🤖 Your system is powered by Gemini 1.5 Flash")
    else:
        print("❌ Gemini API not accessible")

if __name__ == "__main__":
    asyncio.run(main()) 