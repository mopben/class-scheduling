#!/bin/bash
echo "🎓 Starting CourseMatchAI..."
echo "Installing dependencies..."
pip install -r requirements.txt

echo "Launching Streamlit app..."
streamlit run app.py --server.port 8501 --server.address 0.0.0.0