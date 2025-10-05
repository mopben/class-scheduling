import streamlit as st
import pandas as pd
import re

st.set_page_config(page_title="Course Match", layout="wide")

# Custom CSS for styling
st.markdown("""
<style>
    .stApp {
        background-color: #0E1723;
        color: white;
    }
    .stButton > button {
        background-color: #262730;
        color: white;
        border: 1px solid #88E3FF;
    }
    .stSelectbox > div > div {
        background-color: #262730;
        color: white;
    }
    .stTextArea > div > div > textarea {
        background-color: #262730;
        color: white;
    }
    .stExpander {
        background-color: #262730;
    }
    .stProgress > div > div > div {
        background-color: #88E3FF;
    }
    .stAlert {
        background-color: #88E3FF;
        color: white;
    }
    .stSuccess {
        background-color: #262730;
        color: #88E3FF;
        border: 1px solid #88E3FF;
    }
    .stWarning {
        background-color: #262730;
        color: #88E3FF;
        border: 1px solid #88E3FF;
    }
    .stError {
        background-color: #262730;
        color: #88E3FF;
        border: 1px solid #88E3FF;
    }
    header[data-testid="stHeader"] {
        display: none;
    }
    .stApp > div:first-child {
        padding-top: 0;
    }
    .block-container {
        padding-top: 1rem;
    }
    .title-section {
        text-align: center;
        margin: 0 0 2rem 0;
    }
    .title-section h1 {
        color: #88E3FF;
        font-size: 4rem;
        font-weight: 600;
        margin: 0;
        letter-spacing: 3px;
        font-family: 'The Quick Brown', sans-serif;
    }
    .stElementContainer {
        border: none !important;
    }
    .stElementContainer > div {
        border: none !important;
    }
</style>
""", unsafe_allow_html=True)

@st.cache_data
def load_courses():
    try:
        df = pd.read_csv("ucla_courses.csv")
        return df
    except Exception as e:
        pass
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
            # Look for patterns like "MWF 1:30pm-2:30pm" or "TuTh 9am-10:30am"
            time_pattern = r'([MWFTuTh]+)\s+(\d{1,2}):?(\d{0,2})?\s*(am|pm)?\s*-\s*(\d{1,2}):?(\d{0,2})?\s*(am|pm)?'
            match = re.search(time_pattern, line, re.IGNORECASE)
            if match:
                days = match.group(1)
                start_hour = int(match.group(2))
                start_min = int(match.group(3)) if match.group(3) else 0
                start_period = match.group(4)
                end_hour = int(match.group(5))
                end_min = int(match.group(6)) if match.group(6) else 0
                end_period = match.group(7)
                
                # Convert to 24-hour format
                start_24h = convert_to_24h(start_hour, start_min, start_period)
                end_24h = convert_to_24h(end_hour, end_min, end_period)
                
                schedule.append({
                    'days': days,
                    'start_time': start_24h,
                    'end_time': end_24h
                })
    return schedule

def convert_to_24h(hour, minute, period):
    """Convert 12-hour time to minutes since midnight"""
    if period and period.lower() == 'pm' and hour != 12:
        hour += 12
    elif period and period.lower() == 'am' and hour == 12:
        hour = 0
    elif not period and hour < 8:  # Assume afternoon if no period and hour < 8
        hour += 12
    
    return hour * 60 + minute

def expand_days(day_string):
    """Convert day abbreviations to full day names"""
    day_map = {
        'M': 'Monday',
        'Tu': 'Tuesday', 
        'W': 'Wednesday',
        'Th': 'Thursday',
        'F': 'Friday',
        'Sa': 'Saturday',
        'Su': 'Sunday'
    }
    
    if not day_string:
        return 'TBA'
    
    # Handle common patterns
    day_string = str(day_string).strip()
    
    # Replace common abbreviations
    if 'MWF' in day_string:
        return 'Monday, Wednesday, Friday'
    elif 'TuTh' in day_string or 'TTh' in day_string:
        return 'Tuesday, Thursday'
    elif 'MW' in day_string:
        return 'Monday, Wednesday'
    elif 'WF' in day_string:
        return 'Wednesday, Friday'
    
    # Handle individual days or other patterns
    result = []
    i = 0
    while i < len(day_string):
        if i < len(day_string) - 1 and day_string[i:i+2] in day_map:
            result.append(day_map[day_string[i:i+2]])
            i += 2
        elif day_string[i] in day_map:
            result.append(day_map[day_string[i]])
            i += 1
        else:
            i += 1
    
    return ', '.join(result) if result else day_string

def convert_military_to_standard(time_string):
    """Convert military time format to standard time format"""
    if not time_string or time_string == 'TBA':
        return 'TBA'
    
    time_string = str(time_string).strip()
    
    # Handle time ranges like "13:00-14:00" or "13-14"
    if '-' in time_string:
        start_time, end_time = time_string.split('-', 1)
        start_converted = convert_single_time(start_time.strip())
        end_converted = convert_single_time(end_time.strip())
        return f"{start_converted} - {end_converted}"
    else:
        return convert_single_time(time_string)

def convert_single_time(time_str):
    """Convert single military time to standard format"""
    try:
        # Handle formats like "13:00" or "13"
        if ':' in time_str:
            hour, minute = time_str.split(':')
            hour = int(hour)
            minute = int(minute)
        else:
            hour = int(time_str)
            minute = 0
        
        # Convert to 12-hour format
        if hour == 0:
            return f"12:{minute:02d} AM"
        elif hour < 12:
            return f"{hour}:{minute:02d} AM"
        elif hour == 12:
            return f"12:{minute:02d} PM"
        else:
            return f"{hour-12}:{minute:02d} PM"
    except:
        return time_str

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
st.markdown("""
<div class="title-section">
    <h1>Course Match</h1>
</div>
""", unsafe_allow_html=True)

courses_df = load_courses()

if courses_df.empty:
    st.stop()

col1, col2 = st.columns([1, 1])

with col1:
    st.header("Current Schedule")
    schedule_text = st.text_area("Enter your current schedule:", 
                               placeholder="COM SCI 188 (MWF 1pm-2pm), LING 20 (TuTh 3:00pm-4:30pm)")
    
    current_schedule = parse_current_schedule(schedule_text)
    
    if schedule_text and current_schedule:
        for course in current_schedule:
            days = course.get('days', '')
            start_h = course.get('start_time', 0) // 60
            start_m = course.get('start_time', 0) % 60
            end_h = course.get('end_time', 0) // 60
            end_m = course.get('end_time', 0) % 60
            st.write(f"- {days} {start_h:02d}:{start_m:02d}-{end_h:02d}:{end_m:02d}")

with col2:
    st.header("Interests & Preferences")
    interests = st.text_area("What are you interested in?", 
                           placeholder="artificial intelligence, linguistics, cognitive science...")
    


if st.button("Find Matching Courses", type="primary"):
    if interests:
        with st.spinner("Finding courses that don't conflict with your schedule..."):
            recommendations = simple_course_match(interests, current_schedule, courses_df, {})
            
            st.header("Recommended Courses")
            
            if recommendations:
                for i, rec in enumerate(recommendations, 1):
                    course = rec['course']
                    
                    with st.expander(f"{i}. {course.get('course_code', '')} - {course.get('course_title', '')}", expanded=i==1):
                        st.write(f"**Days:** {expand_days(course.get('days', 'TBA'))}")
                        time_display = f"{course.get('start_time', '')}-{course.get('end_time', '')}"
                        st.write(f"**Time:** {convert_military_to_standard(time_display)}")
                        st.write(f"**GE Area:** {course.get('GE', 'N/A')}")
                        st.write(f"**Description:** {course.get('description', '')}")


st.markdown("---")