#!/usr/bin/env python3
"""
Demo script for CourseMatchAI Bedrock Agent
Run this to test the agent functionality
"""

from bedrock_agent import CourseMatchAgent, create_course_recommendation_query

def demo_agent():
    """Demonstrate the CourseMatch agent capabilities"""
    
    print("🎓 CourseMatchAI Agent Demo")
    print("=" * 50)
    
    # Initialize agent
    agent = CourseMatchAgent()
    
    # Sample student data
    interests = "artificial intelligence, cognitive science, linguistics"
    current_schedule = [
        {"code": "MATH 31A", "days": "MWF", "start_time": "09:00", "end_time": "10:00"},
        {"code": "ENGL 4", "days": "TuTh", "start_time": "11:00", "end_time": "12:30"}
    ]
    
    filters = {
        "difficulty": "Beginner",
        "ge_area": "Any",
        "credits": (3, 5)
    }
    
    print(f"Student Interests: {interests}")
    print(f"Current Schedule: {[f\"{c['code']} ({c['days']} {c['start_time']}-{c['end_time']})\" for c in current_schedule]}")
    print(f"Filters: {filters}")
    print("\n" + "=" * 50)
    
    # Create query for agent
    query = create_course_recommendation_query(interests, current_schedule, filters)
    
    print("Generated Query:")
    print(query)
    print("\n" + "=" * 50)
    
    # Invoke agent
    print("Invoking CourseMatch Agent...")
    try:
        response = agent.invoke_agent(query)
        
        if response.get('success'):
            print("\n✅ Agent Response:")
            print(response['answer'])
            
            if response.get('references'):
                print(f"\n📚 Knowledge Base References ({len(response['references'])} found):")
                for i, ref in enumerate(response['references'], 1):
                    content = ref.get('content', {}).get('text', '')
                    location = ref.get('location', {}).get('s3Location', {}).get('uri', '')
                    print(f"{i}. Source: {location}")
                    print(f"   Content: {content[:100]}...")
        else:
            print(f"\n❌ Agent Error: {response.get('error')}")
            
    except Exception as e:
        print(f"\n❌ Demo Error: {str(e)}")
        print("\nNote: Make sure to:")
        print("1. Replace COURSEMATCH_AGENT_ID with your actual agent ID")
        print("2. Create the Bedrock Agent in AWS Console")
        print("3. Set up proper IAM permissions")

if __name__ == "__main__":
    demo_agent()