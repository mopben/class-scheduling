import boto3
import json
import re

def parse_schedule_text(text):
    """Parse schedule from text input"""
    courses = []
    
    # Simple regex patterns for common schedule formats
    patterns = [
        r'([A-Z]+\s*\d+[A-Z]*)\s*\(([MWF]+|[TR]+|[MTWRF]+)\s*(\d{1,2}:\d{2})-(\d{1,2}:\d{2})\)',
        r'([A-Z]+\s*\d+[A-Z]*)\s*([MWF]+|[TR]+|[MTWRF]+)\s*(\d{1,2})-(\d{1,2})',
        r'([A-Z]+\s*\d+[A-Z]*)\s*-\s*([MWF]+|[TR]+|[MTWRF]+)\s*(\d{1,2}:\d{2})-(\d{1,2}:\d{2})'
    ]
    
    for pattern in patterns:
        matches = re.findall(pattern, text, re.IGNORECASE)
        for match in matches:
            course = {
                'code': match[0].strip(),
                'days': match[1].strip(),
                'start_time': match[2] if ':' in match[2] else f"{match[2]}:00",
                'end_time': match[3] if ':' in match[3] else f"{match[3]}:00"
            }
            courses.append(course)
    
    return courses

def extract_schedule_with_bedrock(text, bedrock_client):
    """Use Bedrock to extract schedule information"""
    prompt = f"""
    Extract course schedule information from this text. Return only valid JSON.
    
    Text: {text}
    
    Format:
    {{
        "courses": [
            {{
                "code": "MATH 31A",
                "days": "MWF", 
                "start_time": "09:00",
                "end_time": "10:00"
            }}
        ]
    }}
    """
    
    try:
        response = bedrock_client.invoke_model(
            modelId='us.amazon.nova-pro-v1:0',
            body=json.dumps({
                "messages": [{"role": "user", "content": [{"text": prompt}]}],
                "inferenceConfig": {"temperature": 0.1}
            })
        )
        result = json.loads(response['body'].read())
        content = result['output']['message']['content'][0]['text']
        
        # Extract JSON from response
        json_start = content.find('{')
        json_end = content.rfind('}') + 1
        if json_start != -1 and json_end != -1:
            json_str = content[json_start:json_end]
            return json.loads(json_str)
        
    except Exception as e:
        print(f"Bedrock parsing error: {e}")
    
    # Fallback to regex parsing
    courses = parse_schedule_text(text)
    return {"courses": courses}

def check_schedule_conflicts(current_schedule, new_course):
    """Check if new course conflicts with current schedule"""
    new_days = set(new_course.get('days', ''))
    new_start = new_course.get('start_time', '')
    new_end = new_course.get('end_time', '')
    
    for course in current_schedule:
        existing_days = set(course.get('days', ''))
        existing_start = course.get('start_time', '')
        existing_end = course.get('end_time', '')
        
        # Check for day overlap
        if new_days & existing_days:
            # Check for time overlap
            if time_overlap(new_start, new_end, existing_start, existing_end):
                return True
    
    return False

def time_overlap(start1, end1, start2, end2):
    """Check if two time ranges overlap"""
    try:
        start1_min = time_to_minutes(start1)
        end1_min = time_to_minutes(end1)
        start2_min = time_to_minutes(start2)
        end2_min = time_to_minutes(end2)
        
        return start1_min < end2_min and start2_min < end1_min
    except:
        return False

def time_to_minutes(time_str):
    """Convert time string to minutes since midnight"""
    try:
        hours, minutes = map(int, time_str.split(':'))
        return hours * 60 + minutes
    except:
        return 0