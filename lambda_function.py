import json
import boto3
from course_data import get_sample_courses
from schedule_parser import check_schedule_conflicts, parse_schedule_text

def lambda_handler(event, context):
    """
    Lambda function to be used as action group for Bedrock Agent
    Handles course search and recommendation logic
    """
    
    try:
        # Parse the agent request
        agent_request = event.get('messageVersion', '')
        input_text = event.get('inputText', '')
        action_group = event.get('actionGroup', '')
        api_path = event.get('apiPath', '')
        
        print(f"Agent request: {agent_request}")
        print(f"Input text: {input_text}")
        print(f"Action group: {action_group}")
        print(f"API path: {api_path}")
        
        # Extract parameters from the request
        parameters = {}
        if 'parameters' in event:
            for param in event['parameters']:
                parameters[param['name']] = param['value']
        
        interests = parameters.get('interests', '')
        schedule_text = parameters.get('schedule', '')
        
        # Parse current schedule
        current_schedule = []
        if schedule_text:
            current_schedule = parse_schedule_text(schedule_text)
        
        # Get available courses
        available_courses = get_sample_courses()
        
        # Filter courses by schedule conflicts
        compatible_courses = []
        for course in available_courses:
            if not current_schedule or not check_schedule_conflicts(current_schedule, course):
                compatible_courses.append(course)
        
        # Simple interest matching
        recommendations = match_courses_by_interests(interests, compatible_courses)
        
        # Format response for agent
        response_body = {
            "TEXT": {
                "body": format_recommendations_for_agent(recommendations, interests)
            }
        }
        
        action_response = {
            "messageVersion": "1.0",
            "response": response_body
        }
        
        return action_response
        
    except Exception as e:
        print(f"Error in lambda_handler: {str(e)}")
        
        error_response = {
            "messageVersion": "1.0", 
            "response": {
                "TEXT": {
                    "body": f"I encountered an error while searching for courses: {str(e)}"
                }
            }
        }
        
        return error_response

def match_courses_by_interests(interests, courses):
    """Simple keyword-based course matching"""
    if not interests:
        return courses[:3]  # Return top 3 if no interests specified
    
    interest_words = interests.lower().split()
    scored_courses = []
    
    for course in courses:
        score = 0
        matches = []
        
        # Check against keywords
        for keyword in course.get('keywords', []):
            for interest in interest_words:
                if interest in keyword.lower() or keyword.lower() in interest:
                    score += 2
                    matches.append(keyword)
        
        # Check against title and description
        searchable_text = f"{course.get('title', '')} {course.get('description', '')}".lower()
        for interest in interest_words:
            if interest in searchable_text:
                score += 1
                matches.append(interest)
        
        if score > 0:
            course['match_score'] = score
            course['match_reasons'] = list(set(matches))
            scored_courses.append(course)
    
    # Sort by score and return top matches
    scored_courses.sort(key=lambda x: x['match_score'], reverse=True)
    return scored_courses[:5]

def format_recommendations_for_agent(recommendations, interests):
    """Format course recommendations for the agent response"""
    if not recommendations:
        return f"I couldn't find any courses matching your interests in '{interests}'. You might want to try broader search terms or check if there are prerequisites you need to complete first."
    
    response = f"Based on your interests in '{interests}', here are my top course recommendations:\n\n"
    
    for i, course in enumerate(recommendations, 1):
        response += f"{i}. **{course['code']} - {course['title']}**\n"
        response += f"   Time: {course['time']}\n"
        response += f"   Credits: {course['credits']} units\n"
        response += f"   Difficulty: {course['difficulty']}\n"
        response += f"   GE Area: {course['ge_area']}\n"
        response += f"   Description: {course['description']}\n"
        
        if course.get('match_reasons'):
            response += f"   Why it matches: This course aligns with your interest in {', '.join(course['match_reasons'])}\n"
        
        response += f"   Match Score: {course.get('match_score', 0)}/10\n\n"
    
    response += "These courses have been filtered to avoid conflicts with your current schedule. Would you like more details about any of these courses or need help with enrollment information?"
    
    return response