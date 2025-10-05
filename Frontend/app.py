import streamlit as st
import json

# Inject custom CSS if style.css exists
import os
css_path = os.path.join(os.path.dirname(__file__), "style.css")
if os.path.exists(css_path):
	with open(css_path) as f:
		st.markdown(f"<style>{f.read()}</style>", unsafe_allow_html=True)

# loading JSON placeholder data

# Load placeholder data safely
data = []
json_path = os.path.join(os.path.dirname(__file__), "../Data/placeholder.json")
if os.path.exists(json_path):
	with open(json_path, 'r') as file:
		data = json.load(file)
else:
	st.error("Could not find Data/placeholder.json. Please check the path.")

# loading external HTML/CSS
# Optionally inject style.html if it exists
html_path = os.path.join(os.path.dirname(__file__), "style.html")
if os.path.exists(html_path):
	with open(html_path) as f:
		st.markdown(f.read(), unsafe_allow_html=True)

st.title('Class Schedule Planner')
st.markdown('<h3 class="blue-heading">Easily find courses that fit your schedule</h3>', unsafe_allow_html=True)

# each section
tab1, tab2 = st.tabs(["Upload Schedule", "Write Your Schedule"])

# upload file
with tab1:
	st.markdown('<h4 class="blue-heading">Upload Your Schedule File</h4>', unsafe_allow_html=True)
	schedule_file = st.file_uploader("Choose a file (CSV, XLSX, etc.)", type=["csv", "xlsx"])
	if schedule_file:
		st.success("File uploaded! Processing...")
		st.info("Course recommendations will appear here.")

# language input
with tab2:
	st.markdown('<h4 class="blue-heading">Describe Your Schedule</h4>', unsafe_allow_html=True)
	user_text = st.text_area("Enter your schedule or constraints in natural language", height=150)
	if st.button("Find Courses", key="nl_button"):
		if user_text:
			st.markdown('<h4 class="blue-heading">Recommended Classes</h4>', unsafe_allow_html=True)

			st.info("Course recommendations will appear here.")
			# box container
			st.markdown('<div class="recommendation-box">', unsafe_allow_html=True)
			with st.container(height=500):
				for i, class_obj in enumerate(data):
					for _, details in class_obj.items():
						st.markdown('<div class="recommendation-item">', unsafe_allow_html=True)
						st.markdown(f"### {details['title']}")
						st.write(details['description'])
						st.write("Schedule:")
						for sched in details['Schedule']:
							st.write(f"- {sched[0]} to {sched[1]}")
						st.markdown('<hr class="recommendation-divider">', unsafe_allow_html=True)
						st.markdown('</div>', unsafe_allow_html=True)
				st.markdown('</div>', unsafe_allow_html=True)
		else:
			st.warning("Please enter your schedule details.")
