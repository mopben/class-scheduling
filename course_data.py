import boto3
import json

def setup_dynamodb_table():
    """Setup DynamoDB table for UCLA courses"""
    dynamodb = boto3.resource('dynamodb', region_name='us-east-1')
    
    # Sample UCLA course data
    courses = [
        {
            "course_id": "LING20",
            "code": "LING 20",
            "title": "Introduction to Linguistics",
            "time": "TuTh 3:00-4:30",
            "days": ["Tuesday", "Thursday"],
            "start_time": "15:00",
            "end_time": "16:30",
            "description": "Basic concepts in linguistics including phonetics, phonology, morphology, syntax, and semantics",
            "ge_area": "Arts & Humanities",
            "credits": 4,
            "difficulty": "Beginner",
            "keywords": ["linguistics", "language", "phonetics", "syntax", "semantics"]
        },
        {
            "course_id": "CS188",
            "code": "COM SCI 188",
            "title": "Ethics in AI",
            "time": "MWF 1:00-2:00",
            "days": ["Monday", "Wednesday", "Friday"],
            "start_time": "13:00",
            "end_time": "14:00",
            "description": "Ethical implications of artificial intelligence and machine learning systems",
            "ge_area": "Social Sciences",
            "credits": 4,
            "difficulty": "Intermediate",
            "keywords": ["AI", "ethics", "artificial intelligence", "machine learning", "technology"]
        },
        {
            "course_id": "COGSCI1",
            "code": "COG SCI 1",
            "title": "Introduction to Cognitive Science",
            "time": "TuTh 9:00-10:30",
            "days": ["Tuesday", "Thursday"],
            "start_time": "09:00",
            "end_time": "10:30",
            "description": "Interdisciplinary study of mind and cognition from psychology, neuroscience, AI perspectives",
            "ge_area": "Social Sciences",
            "credits": 4,
            "difficulty": "Beginner",
            "keywords": ["cognitive science", "psychology", "neuroscience", "mind", "cognition"]
        },
        {
            "course_id": "PSYC85",
            "code": "PSYC 85",
            "title": "Introduction to Cognitive Science",
            "time": "MWF 11:00-12:00",
            "days": ["Monday", "Wednesday", "Friday"],
            "start_time": "11:00",
            "end_time": "12:00",
            "description": "Cognitive processes, mental representations, and computational approaches to mind",
            "ge_area": "Social Sciences",
            "credits": 4,
            "difficulty": "Beginner",
            "keywords": ["psychology", "cognitive processes", "mental representations", "computation"]
        },
        {
            "course_id": "PHIL7",
            "code": "PHIL 7",
            "title": "Introduction to Philosophy of Mind",
            "time": "TuTh 2:00-3:30",
            "days": ["Tuesday", "Thursday"],
            "start_time": "14:00",
            "end_time": "15:30",
            "description": "Nature of consciousness, mental states, and the mind-body problem",
            "ge_area": "Arts & Humanities",
            "credits": 4,
            "difficulty": "Intermediate",
            "keywords": ["philosophy", "consciousness", "mind", "mental states", "philosophy of mind"]
        }
    ]
    
    return courses

def get_sample_courses():
    """Return sample course data for demo purposes"""
    return setup_dynamodb_table()