import streamlit as st
import pandas as pd
import json

st.set_page_config(page_title="CourseMatchAI", page_icon="🎓", layout="wide")

# Load CSV data
@st.cache_data
def load_courses():
    try:
        df = pd.read_csv("ucla_courses.csv")
        return df
    except Exception as e:
        st.error(f"Error loading CSV: {e}")
        return pd.DataFrame()

def simple_course_match(interests, schedule_conflicts, courses_df, filters):
    """Simple course matching without Bedrock"""
    if courses_df.empty:
        return []
    
    # Filter by interests (simple keyword matching)
    interest_words = interests.lower().split()
    matched_courses = []
    
    for _, course in courses_df.iterrows():
        score = 0
        course_text = f"{course.get('course_title', '')} {course.get('description', '')}".lower()
        
        # Check interest matches
        for word in interest_words:
            if word in course_text:
                score += 1
        
        # Apply filters
        if filters.get('difficulty') and filters['difficulty'] != 'Any':
            if str(course.get('difficulty', '')) != str(filters['difficulty']):
                continue
        
        if score > 0:
            matched_courses.append({
                'course': course,
                'score': score,
                'matches': [w for w in interest_words if w in course_text]
            })
    
    # Sort by score
    matched_courses.sort(key=lambda x: x['score'], reverse=True)
    return matched_courses[:5]

# Main UI
st.title("🎓 CourseMatchAI")
st.subheader("Personalized Class Recommender for UCLA Students")

# Load courses
courses_df = load_courses()

if not courses_df.empty:
    st.success(f"Loaded {len(courses_df)} courses from CSV")
else:
    st.error("Could not load course data")
    st.stop()

col1, col2 = st.columns([1, 1])

with col1:
    st.header("📅 Current Schedule")
    schedule_text = st.text_area("Enter your current schedule:", 
                               placeholder="COM SCI 188 (MWF 1-2), LING 20 (TuTh 3-4:30)")
    
    current_schedule = []
    if schedule_text:
        # Simple parsing
        lines = schedule_text.split(',')
        for line in lines:
            line = line.strip()
            if line:
                current_schedule.append(line)
        
        if current_schedule:
            st.success(f"Detected {len(current_schedule)} courses")
            for course in current_schedule:
                st.write(f"• {course}")

with col2:
    st.header("🎯 Interests & Preferences")
    interests = st.text_area("What are you interested in?", 
                           placeholder="artificial intelligence, linguistics, cognitive science...")
    
    # Filters
    st.subheader("Filters")
    difficulty = st.selectbox("Difficulty Level", ["Any", "1", "2", "3", "4", "5"])
    ge_area = st.selectbox("GE Area", ["Any"] + list(courses_df['GE'].unique()) if 'GE' in courses_df.columns else ["Any"])

# Generate recommendations
if st.button("🔍 Find Matching Courses", type="primary"):
    if interests:
        with st.spinner("Finding your perfect courses..."):
            filters = {
                'difficulty': difficulty,
                'ge_area': ge_area
            }
            
            recommendations = simple_course_match(interests, current_schedule, courses_df, filters)
            
            st.header("📚 Recommended Courses")
            
            if recommendations:
                for i, rec in enumerate(recommendations, 1):
                    course = rec['course']
                    
                    with st.expander(f"{i}. {course.get('course_code', '')} - {course.get('course_title', '')}", expanded=i==1):
                        col_a, col_b = st.columns([2, 1])
                        with col_a:
                            st.write(f"**Days:** {course.get('days', 'TBA')}")
                            st.write(f"**Time:** {course.get('start_time', '')}-{course.get('end_time', '')}")
                            st.write(f"**GE Area:** {course.get('GE', 'N/A')}")
                            st.write(f"**Description:** {course.get('description', '')}")
                            st.write(f"**Matching keywords:** {', '.join(rec['matches'])}")
                        with col_b:
                            st.metric("Match Score", f"{rec['score']}")
                            st.write(f"**Difficulty:** {course.get('difficulty', 'N/A')}")
            else:
                st.warning("No matching courses found. Try different interests or filters.")
    else:
        st.error("Please enter your interests to get recommendations.")

# Footer
st.markdown("---")
st.markdown("*CourseMatchAI - Simple CSV-based course recommendations*")