
import streamlit as st
from streamlit_option_menu import option_menu

# Custom CSS for background and text colors
st.markdown(
	"""
	<style>
	body {
		background-color: #fff !important;
	}
	.main {
		background-color: #fff !important;
	}
	h1, h2, h3, h4, h5, h6 {
		color: #0056b3 !important;
	}
	.stTextInput > label, .stFileUploader > label, .stButton > button {
		color: #222 !important;
	}
	.stButton > button {
		background-color: #0056b3 !important;
		color: #fff !important;
		border-radius: 6px;
		border: none;
		padding: 8px 16px;
		font-weight: 600;
	}
	.stTextInput > div > input {
		border: 1px solid #0056b3 !important;
		color: #222 !important;
	}
	.stFileUploader > div > input {
		border: 1px solid #0056b3 !important;
		color: #222 !important;
	}
	</style>
	""",
	unsafe_allow_html=True
)

st.title('Class Schedule Planner')
st.markdown('<h3 style="color:#0056b3;">Easily find courses that fit your schedule</h3>', unsafe_allow_html=True)

tab1, tab2 = st.tabs(["Upload Schedule", "Describe Schedule (Natural Language)"])

with tab1:
	st.markdown('<h4 style="color:#0056b3;">Upload Your Schedule File</h4>', unsafe_allow_html=True)
	schedule_file = st.file_uploader("Choose a file (CSV, XLSX, etc.)", type=["csv", "xlsx"])
	if schedule_file:
		st.success("File uploaded! Processing...")
		# Placeholder for file processing logic
		st.info("Course recommendations will appear here.")

with tab2:
	st.markdown('<h4 style="color:#0056b3;">Describe Your Schedule</h4>', unsafe_allow_html=True)
	user_text = st.text_area("Enter your schedule or constraints in natural language", height=150)
	if st.button("Find Courses", key="nl_button"):
		if user_text:
			st.success("Processing your input...")
			# Placeholder for NLP logic
			st.info("Course recommendations will appear here.")
		else:
			st.warning("Please enter your schedule details.")

