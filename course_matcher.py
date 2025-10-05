import boto3
import json
from course_data import get_sample_courses
from schedule_parser import check_schedule_conflicts

def match_courses_with_bedrock(interests, current_schedule, bedrock_client, filters=None):
    """Use Bedrock to match courses with student interests"""
    available_courses = get_sample_courses()
    
    # Filter courses by schedule conflicts first
    compatible_courses = []
    for course in available_courses:
        if not check_schedule_conflicts(current_schedule, course):
            compatible_courses.append(course)
    
    # Apply additional filters
    if filters:
        compatible_courses = apply_filters(compatible_courses, filters)
    
    if not compatible_courses:
        return {"recommendations": [], "message": "No courses available that fit your schedule and filters."}
    
    # Create prompt for Bedrock
    schedule_summary = create_schedule_summary(current_schedule)
    courses_json = json.dumps(compatible_courses, indent=2)
    
    prompt = f"""
    You are a course recommendation system for UCLA students.
    
    Student Profile:
    - Interests: {interests}
    - Current Schedule: {schedule_summary}
    
    Available Courses (already filtered for schedule compatibility):
    {courses_json}
    
    Task: Rank these courses by how well they match the student's interests. Consider:
    1. Semantic similarity between interests and course description/keywords
    2. Academic progression and complementary subjects
    3. Interdisciplinary connections
    
    Return ONLY valid JSON in this format:
    {{
        "recommendations": [
            {{
                "course_code": "LING 20",
                "relevance_score": 0.95,
                "explanation": "Perfect match for linguistics interest. Complements cognitive science background.",
                "interest_matches": ["linguistics", "language"]
            }}
        ]
    }}
    
    Rank all compatible courses, highest relevance first.
    """
    
    try:
        response = bedrock_client.invoke_model(
            modelId='us.amazon.nova-pro-v1:0',
            body=json.dumps({
                "messages": [{"role": "user", "content": [{"text": prompt}]}],
                "inferenceConfig": {"temperature": 0.3, "maxTokens": 2000}
            })
        )
        
        result = json.loads(response['body'].read())
        content = result['output']['message']['content'][0]['text']
        
        # Extract JSON from response
        json_start = content.find('{')
        json_end = content.rfind('}') + 1
        if json_start != -1 and json_end != -1:
            json_str = content[json_start:json_end]
            recommendations = json.loads(json_str)
            
            # Enrich recommendations with full course details
            enriched_recs = []
            for rec in recommendations.get('recommendations', []):
                course_info = next((c for c in compatible_courses if c['code'] == rec['course_code']), None)
                if course_info:
                    rec['course_info'] = course_info
                    enriched_recs.append(rec)
            
            return {"recommendations": enriched_recs}
        
    except Exception as e:
        print(f"Bedrock matching error: {e}")
    
    # Fallback: simple keyword matching
    return fallback_matching(interests, compatible_courses)

def apply_filters(courses, filters):
    """Apply user-selected filters to course list"""
    filtered = courses
    
    if filters.get('difficulty') and filters['difficulty'] != 'Any':
        filtered = [c for c in filtered if c.get('difficulty') == filters['difficulty']]
    
    if filters.get('ge_area') and filters['ge_area'] != 'Any':
        filtered = [c for c in filtered if c.get('ge_area') == filters['ge_area']]
    
    if filters.get('credits'):
        min_credits, max_credits = filters['credits']
        filtered = [c for c in filtered if min_credits <= c.get('credits', 0) <= max_credits]
    
    return filtered

def create_schedule_summary(schedule):
    """Create readable summary of current schedule"""
    if not schedule:
        return "No current courses"
    
    summary = []
    for course in schedule:
        course_str = f"{course.get('code', 'Unknown')} ({course.get('days', '')}{course.get('start_time', '')}-{course.get('end_time', '')})"
        summary.append(course_str)
    
    return ", ".join(summary)

def fallback_matching(interests, courses):
    """Simple keyword-based matching as fallback"""
    interest_words = interests.lower().split()
    recommendations = []
    
    for course in courses:
        score = 0
        matches = []
        
        # Check keywords
        for keyword in course.get('keywords', []):
            for interest in interest_words:
                if interest in keyword.lower() or keyword.lower() in interest:
                    score += 1
                    matches.append(keyword)
        
        # Check title and description
        text_to_check = f"{course.get('title', '')} {course.get('description', '')}".lower()
        for interest in interest_words:
            if interest in text_to_check:
                score += 0.5
                matches.append(interest)
        
        if score > 0:
            recommendations.append({
                "course_code": course['code'],
                "relevance_score": min(score / len(interest_words), 1.0),
                "explanation": f"Matches interests: {', '.join(set(matches))}",
                "interest_matches": list(set(matches)),
                "course_info": course
            })
    
    # Sort by relevance score
    recommendations.sort(key=lambda x: x['relevance_score'], reverse=True)
    
    return {"recommendations": recommendations}