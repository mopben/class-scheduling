# 🎓 CourseMatchAI – Personalized Class Recommender for UCLA Students

## 💡 One-Line Summary
"Upload your current schedule and interests — get AI-curated class recommendations that fit your timetable and passions."

## 🧩 Problem
Students waste hours searching through UCLA's course catalog, trying to find classes that:
- Don't conflict with their existing schedule
- Actually align with their interests or career goals
- Manual filtering = time-consuming, repetitive, and inefficient

## 🚀 Solution
CourseMatchAI uses AWS-powered GenAI to automatically:
- Parse a student's current schedule (from text, PDF, or image)
- Understand their academic and personal interests (natural language input)
- Rank and recommend UCLA classes that fit within schedule and match interests

## ⚙️ User Flow
1. **Input**: Upload schedule + enter interests
2. **Processing**: Extract schedule data, fetch courses, match via Bedrock
3. **Output**: Ranked course recommendations with explanations

## 🧠 Core AWS Components
- **Amazon Bedrock**: Natural language understanding and course matching
- **Amazon Textract**: Document parsing (PDF/Image schedules)
- **Amazon DynamoDB**: Course catalog storage
- **AWS Lambda**: Filtering & ranking logic
- **Amazon S3**: File storage
- **Streamlit**: Interactive frontend

## 🚀 Quick Start
```bash
pip install -r requirements.txt
streamlit run app.py
```

## 🌟 Features
- Multi-modal schedule input (text, PDF, image)
- AI-powered semantic course matching
- Schedule conflict detection
- Personalized explanations
- Interactive filtering (difficulty, GE areas, credits)

## 🔧 Architecture
```
Student Input → Textract → Bedrock → Lambda → DynamoDB → Streamlit UI
```

Built for AWS hackathons - showcasing real-world GenAI applications with immediate student value.