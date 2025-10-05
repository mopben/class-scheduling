import streamlit as st
import pandas as pd
import re

st.set_page_config(page_title="CourseMatchAI", layout="wide")

@st.cache_data
def load_courses():
    try:
        df = pd.read_csv("ucla_courses.csv")
        return df
    except Exception as e:
        st.error(f"Error loading CSV: {e}")
        return pd.DataFrame()

def parse_current_schedule(schedule_text):
    """Parse current schedule into structured format"""
    schedule = []
    if not schedule_text:
        return schedule
    
    lines = schedule_text.split(',')
    for line in lines:
        line = line.strip()
        if line:
            # Look for patterns like "MWF 13:00-14:00" or "TuTh 15:00-16:30"
            time_pattern = r'([MWFTuTh]+)\s+(\d{1,2}):?(\d{0,2})?-(\d{1,2}):?(\d{0,2})?'
            match = re.search(time_pattern, line)
            if match:
                days = match.group(1)
                start_hour = int(match.group(2))
                start_min = int(match.group(3)) if match.group(3) else 0
                end_hour = int(match.group(4))
                end_min = int(match.group(5)) if match.group(5) else 0
                
                schedule.append({
                    'days': days,
                    'start_time': start_hour * 60 + start_min,
                    'end_time': end_hour * 60 + end_min
                })
    return schedule

def check_time_conflict(current_schedule, course_days, course_start, course_end):
    """Check if course conflicts with current schedule"""
    if not current_schedule:
        return False
    
    # Convert course times to minutes
    try:
        if isinstance(course_start, str) and ':' in course_start:
            start_parts = course_start.split(':')
            course_start_min = int(start_parts[0]) * 60 + int(start_parts[1])
        else:
            course_start_min = int(float(course_start)) * 60
            
        if isinstance(course_end, str) and ':' in course_end:
            end_parts = course_end.split(':')
            course_end_min = int(end_parts[0]) * 60 + int(end_parts[1])
        else:
            course_end_min = int(float(course_end)) * 60
    except:
        return False
    
    # Parse course days
    if isinstance(course_days, str):
        course_days_clean = course_days.replace('[', '').replace(']', '').replace("'", '').replace('"', '')
        course_day_list = [d.strip() for d in course_days_clean.split(',')]
    else:
        course_day_list = []
    
    # Check each scheduled course
    for scheduled in current_schedule:
        scheduled_days = scheduled['days']
        
        # Check if any days overlap
        day_overlap = False
        for course_day in course_day_list:
            if course_day in scheduled_days or any(d in course_day for d in scheduled_days):
                day_overlap = True
                break
        
        if day_overlap:
            # Check if times overlap
            if (course_start_min < scheduled['end_time'] and 
                course_end_min > scheduled['start_time']):
                return True
    
    return False

def simple_course_match(interests, current_schedule, courses_df, filters):
    """Course matching with conflict detection"""
    if courses_df.empty:
        return []
    
    interest_words = interests.lower().split()
    matched_courses = []
    
    for _, course in courses_df.iterrows():
        # Check for schedule conflicts first
        if check_time_conflict(current_schedule, 
                             course.get('days', ''), 
                             course.get('start_time', 0), 
                             course.get('end_time', 0)):
            continue  # Skip conflicting courses
        
        score = 0
        course_text = f"{course.get('course_title', '')} {course.get('description', '')}".lower()
        
        # Check interest matches
        matches = []
        for word in interest_words:
            if word in course_text:
                score += 1
                matches.append(word)
        
        # Apply filters
        if filters.get('difficulty') and filters['difficulty'] != 'Any':
            if str(course.get('difficulty', '')) != str(filters['difficulty']):
                continue
        
        if score > 0:
            matched_courses.append({
                'course': course,
                'score': score,
                'matches': matches
            })
    
    matched_courses.sort(key=lambda x: x['score'], reverse=True)
    return matched_courses[:5]

# Main UI
st.title("CourseMatchAI")
st.subheader("Personalized Class Recommender for UCLA Students")

courses_df = load_courses()

if not courses_df.empty:
    st.success(f"Loaded {len(courses_df)} courses from CSV")
else:
    st.error("Could not load course data")
    st.stop()

col1, col2 = st.columns([1, 1])

with col1:
    st.header("Current Schedule")
    schedule_text = st.text_area("Enter your current schedule:", 
                               placeholder="COM SCI 188 (MWF 13-14), LING 20 (TuTh 15:00-16:30)")
    
    current_schedule = parse_current_schedule(schedule_text)
    
    if schedule_text:
        if current_schedule:
            st.success(f"Parsed {len(current_schedule)} courses - conflict detection enabled")
            for course in current_schedule:
                days = course.get('days', '')
                start_h = course.get('start_time', 0) // 60
                start_m = course.get('start_time', 0) % 60
                end_h = course.get('end_time', 0) // 60
                end_m = course.get('end_time', 0) % 60
                st.write(f"- {days} {start_h:02d}:{start_m:02d}-{end_h:02d}:{end_m:02d}")
        else:
            st.warning("Could not parse schedule. Use format: 'COURSE (MWF 13-14), COURSE (TuTh 15:00-16:30)'")

with col2:
    st.header("Interests & Preferences")
    interests = st.text_area("What are you interested in?", 
                           placeholder="artificial intelligence, linguistics, cognitive science...")
    
    st.subheader("Filters")
    difficulty = st.selectbox("Difficulty Level", ["Any", "1", "2", "3", "4", "5"])
    ge_area = st.selectbox("GE Area", ["Any"] + list(courses_df['GE'].unique()) if 'GE' in courses_df.columns else ["Any"])

if st.button("Find Matching Courses", type="primary"):
    if interests:
        with st.spinner("Finding courses that don't conflict with your schedule..."):
            filters = {'difficulty': difficulty, 'ge_area': ge_area}
            recommendations = simple_course_match(interests, current_schedule, courses_df, filters)
            
            st.header("Recommended Courses")
            
            if recommendations:
                st.info(f"Found {len(recommendations)} courses with no schedule conflicts")
                for i, rec in enumerate(recommendations, 1):
                    course = rec['course']
                    
                    with st.expander(f"{i}. {course.get('course_code', '')} - {course.get('course_title', '')}", expanded=i==1):
                        col_a, col_b = st.columns([2, 1])
                        st.write(f"**Days:** {course.get('days', 'TBA')}")
                        st.write(f"**Time:** {course.get('start_time', '')}-{course.get('end_time', '')}")
                        st.write(f"**GE Area:** {course.get('GE', 'N/A')}")
                        st.write(f"**Description:** {course.get('description', '')}")
                        st.write(f"**Matching keywords:** {', '.join(rec['matches'])}")
            else:
                st.warning("No matching courses found that don't conflict with your schedule. Try different interests or adjust your current schedule.")
    else:
        st.error("Please enter your interests to get recommendations.")

st.markdown("---")
st.markdown("*CourseMatchAI - Schedule-aware course recommendations*")