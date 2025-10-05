import streamlit as st
import boto3
import json
from io import BytesIO
import pandas as pd
from schedule_parser import extract_schedule_with_bedrock
from course_matcher import match_courses_with_bedrock
from course_data import get_sample_courses
from bedrock_agent import CourseMatchAgent, create_course_recommendation_query

st.set_page_config(page_title="CourseMatchAI", page_icon="🎓", layout="wide")

# Initialize AWS clients
@st.cache_resource
def init_aws_clients():
    return {
        'bedrock': boto3.client('bedrock-runtime', region_name='us-east-1'),
        'textract': boto3.client('textract', region_name='us-east-1'),
        'dynamodb': boto3.resource('dynamodb', region_name='us-east-1')
    }

clients = init_aws_clients()

# Initialize CourseMatch Agent
@st.cache_resource
def init_agent():
    return CourseMatchAgent()

agent = init_agent()







# Main UI
st.title("🎓 CourseMatchAI")
st.subheader("Personalized Class Recommender for UCLA Students")

col1, col2 = st.columns([1, 1])

with col1:
    st.header("📅 Current Schedule")
    
    # Schedule input options
    input_method = st.radio("How would you like to input your schedule?", 
                           ["Text Input", "Upload File"])
    
    current_schedule = []
    
    if input_method == "Text Input":
        schedule_text = st.text_area("Enter your current schedule:", 
                                   placeholder="MATH 31A (MWF 9-10), ENGL 4 (TuTh 11-12:30)")
        if schedule_text:
            current_schedule = extract_schedule_with_bedrock(schedule_text, clients['bedrock']).get('courses', [])
    
    elif input_method == "Upload File":
        uploaded_file = st.file_uploader("Upload schedule (PDF/Image)", 
                                       type=['pdf', 'png', 'jpg', 'jpeg'])
        if uploaded_file:
            st.info("File processing with Textract would be implemented here")
            # Textract integration would go here
    
    if current_schedule:
        st.success(f"Detected {len(current_schedule)} courses in your schedule")
        for course in current_schedule:
            st.write(f"• {course.get('code', 'Unknown')} - {course.get('days', '')}{course.get('time', '')}")

with col2:
    st.header("🎯 Interests & Preferences")
    
    interests = st.text_area("What are you interested in?", 
                           placeholder="AI ethics, neuroscience, linguistics, cognitive science...")

# Method selection
st.subheader("🤖 Recommendation Method")
method = st.radio("Choose recommendation approach:", 
                 ["AI Agent (Recommended)", "Direct Bedrock API"])

# Generate recommendations
if st.button("🔍 Find Matching Courses", type="primary"):
    if interests and current_schedule:
        with st.spinner("Finding your perfect courses..."):
            filters = {
                'difficulty': difficulty,
                'ge_area': ge_area,
                'credits': credits
            }
            
            if method == "AI Agent (Recommended)":
                # Use Bedrock Agent
                query = create_course_recommendation_query(interests, current_schedule, filters)
                agent_response = agent.invoke_agent(query)
                
                if agent_response.get('success'):
                    st.header("🤖 AI Agent Recommendations")
                    st.write(agent_response['answer'])
                    
                    if agent_response.get('references'):
                        with st.expander("📚 Knowledge Base References"):
                            for ref in agent_response['references']:
                                content = ref.get('content', {}).get('text', '')
                                location = ref.get('location', {}).get('s3Location', {}).get('uri', '')
                                st.write(f"**Source:** {location}")
                                st.write(f"**Content:** {content[:200]}...")
                else:
                    st.error(f"Agent Error: {agent_response.get('error', 'Unknown error')}")
                    st.info("Falling back to direct API method...")
                    recommendations = match_courses_with_bedrock(interests, current_schedule, clients['bedrock'], filters)
            else:
                # Use direct Bedrock API
                recommendations = match_courses_with_bedrock(interests, current_schedule, clients['bedrock'], filters)
            
            if method == "Direct Bedrock API":
                st.header("📚 Recommended Courses")
                
                if recommendations.get('recommendations'):
                    for i, rec in enumerate(recommendations['recommendations'][:5], 1):
                        course_info = rec.get('course_info', {})
                        course_code = rec.get('course_code', '')
                        
                        with st.expander(f"{i}. {course_code} - {course_info.get('title', '')}", expanded=i==1):
                            col_a, col_b = st.columns([2, 1])
                            with col_a:
                                st.write(f"**Time:** {course_info.get('time', 'TBA')}")
                                st.write(f"**GE Area:** {course_info.get('ge_area', 'N/A')}")
                                st.write(f"**Credits:** {course_info.get('credits', 'N/A')}")
                                st.write(f"**Description:** {course_info.get('description', '')}")
                                st.write(f"**Why it matches:** {rec.get('explanation', '')}")
                            with col_b:
                                relevance = rec.get('relevance_score', 0)
                                st.metric("Relevance", f"{relevance:.1%}")
                                st.write(f"**Difficulty:** {course_info.get('difficulty', 'N/A')}")
                else:
                    message = recommendations.get('message', 'No matching courses found. Try adjusting your interests or filters.')
                    st.warning(message)
    else:
        st.error("Please enter both your schedule and interests to get recommendations.")

# Footer
st.markdown("---")
st.markdown("*Powered by AWS Bedrock, Textract, and DynamoDB*")