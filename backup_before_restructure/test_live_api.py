#!/usr/bin/env python3
"""
Test the live Dungeon Master's Oracle API
"""

import requests
import json
import time

API_BASE = "http://127.0.0.1:8080"

def test_health():
    """Test the health endpoint."""
    print("🏥 Testing Health Endpoint...")
    response = requests.get(f"{API_BASE}/health")
    print(f"Status: {response.status_code}")
    print(f"Response: {response.json()}")
    return response.status_code == 200

def test_query(query_text, description):
    """Test a query endpoint."""
    print(f"\n📝 Testing: {description}")
    print(f"❓ Query: \"{query_text}\"")
    
    payload = {
        "query": query_text,
        "session_id": "test-session-001"
    }
    
    start_time = time.time()
    
    try:
        response = requests.post(f"{API_BASE}/query", json=payload, timeout=30)
        end_time = time.time()
        
        print(f"⏱️  Response time: {(end_time - start_time):.2f}s")
        print(f"📊 Status: {response.status_code}")
        
        if response.status_code == 200:
            result = response.json()
            print(f"🛤️  Route: {result.get('route', 'unknown')}")
            print(f"✅ Success: {result.get('retrieval_success', False)}")
            
            answer = result.get('answer', 'No answer')
            print(f"💬 Answer: {answer[:200]}{'...' if len(answer) > 200 else ''}")
            
            sources = result.get('sources', [])
            if sources:
                print(f"📚 Sources: {', '.join(sources)}")
            
            return True
        else:
            print(f"❌ Error: {response.text}")
            return False
            
    except Exception as e:
        print(f"❌ Request failed: {e}")
        return False

def test_narrate():
    """Test the narrative generation endpoint."""
    print(f"\n🎭 Testing Narrative Generation...")
    
    payload = {
        "prompt": "Describe a spooky, abandoned tavern in a haunted forest",
        "style": "mysterious"
    }
    
    try:
        response = requests.post(f"{API_BASE}/narrate", json=payload, timeout=30)
        
        if response.status_code == 200:
            result = response.json()
            print(f"✅ Narrative generated successfully!")
            narrative = result.get('text', 'No narrative')
            print(f"📖 Story: {narrative[:300]}{'...' if len(narrative) > 300 else ''}")
            return True
        else:
            print(f"❌ Error: {response.text}")
            return False
            
    except Exception as e:
        print(f"❌ Request failed: {e}")
        return False

def main():
    """Run all API tests."""
    print("🎲 Testing Dungeon Master's Oracle API")
    print("=" * 60)
    
    # Test health first
    if not test_health():
        print("❌ Health check failed! Server may not be running.")
        return
    
    print("\n" + "=" * 60)
    print("🧪 Running Query Tests...")
    
    # Test queries
    test_queries = [
        ("What is a Beholder's armor class?", "Structured Query - Monster Stats"),
        ("Show me all dragons", "Structured Query - Filter by Type"),
        ("Which monsters have fire immunity?", "Structured Query - Search Abilities"),
        ("How does grappling work in D&D?", "Unstructured Query - Rules"),
        ("Tell me about spellcasting", "Unstructured Query - Game Mechanics")
    ]
    
    successful_tests = 0
    for query, description in test_queries:
        if test_query(query, description):
            successful_tests += 1
        time.sleep(1)  # Small delay between requests
    
    # Test narrative generation
    print("\n" + "=" * 60)
    if test_narrate():
        successful_tests += 1
    
    # Summary
    total_tests = len(test_queries) + 1  # +1 for narrative test
    print("\n" + "=" * 60)
    print("📊 Test Summary")
    print(f"✅ Successful: {successful_tests}/{total_tests}")
    print(f"🌐 API Documentation: {API_BASE}/docs")
    print(f"📋 Alternative Docs: {API_BASE}/redoc")
    
    if successful_tests == total_tests:
        print("\n🎉 All tests passed! Your Dungeon Master's Oracle is working perfectly!")
    else:
        print(f"\n⚠️  {total_tests - successful_tests} tests failed. Check the logs above.")

if __name__ == "__main__":
    main() 