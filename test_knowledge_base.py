import boto3
import json

def test_knowledge_base_retrieval(kb_id, query):
    """Test Knowledge Base retrieval directly"""
    
    bedrock_agent = boto3.client('bedrock-agent-runtime', region_name='us-east-1')
    
    try:
        response = bedrock_agent.retrieve(
            knowledgeBaseId=kb_id,
            retrievalQuery={'text': query},
            retrievalConfiguration={
                'vectorSearchConfiguration': {
                    'numberOfResults': 5
                }
            }
        )
        
        print(f"Query: {query}")
        print("=" * 50)
        
        results = response.get('retrievalResults', [])
        print(f"Found {len(results)} relevant courses:")
        
        for i, result in enumerate(results, 1):
            content = result.get('content', {}).get('text', '')
            score = result.get('score', 0)
            location = result.get('location', {}).get('s3Location', {}).get('uri', '')
            
            print(f"\n{i}. Score: {score:.3f}")
            print(f"   Source: {location}")
            print(f"   Content: {content[:200]}...")
        
        return results
        
    except Exception as e:
        print(f"Error testing Knowledge Base: {e}")
        return []

def test_agent_with_kb():
    """Test the full agent with Knowledge Base"""
    from bedrock_agent import CourseMatchAgent
    
    agent = CourseMatchAgent()
    
    test_queries = [
        "Find me computer science courses on Tuesday and Thursday",
        "What linguistics courses are available?", 
        "Show me beginner-level courses in cognitive science",
        "I need courses that satisfy GE requirements"
    ]
    
    for query in test_queries:
        print(f"\n🤖 Testing: {query}")
        print("-" * 40)
        
        response = agent.invoke_agent(query)
        
        if response.get('success'):
            print("✅ Agent Response:")
            print(response['answer'][:300] + "...")
            
            if response.get('references'):
                print(f"\n📚 KB References: {len(response['references'])} found")
        else:
            print(f"❌ Error: {response.get('error')}")

if __name__ == "__main__":
    # Replace with your actual Knowledge Base ID
    KB_ID = "COURSEMATCH_KB_ID"
    
    print("🧪 Testing Knowledge Base Retrieval")
    print("=" * 50)
    
    # Test direct KB retrieval
    test_knowledge_base_retrieval(KB_ID, "computer science artificial intelligence")
    
    print("\n\n🤖 Testing Agent with Knowledge Base")
    print("=" * 50)
    
    # Test full agent
    test_agent_with_kb()