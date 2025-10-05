# Course Match

## Problem

Students waste hours searching through UCLA's course catalog, trying to find classes that:

- Don't conflict with their existing schedule
- Actually align with their interests or career goals
- Manual filtering = time-consuming, repetitive, and inefficient

## Solution

CourseMatchAI uses AWS-powered GenAI to automatically:

- Parse a student's current schedule (from text, PDF, or image)
- Understand their academic and personal interests (natural language input)
- Rank and recommend UCLA classes that fit within schedule and match interests

## AWS Components

- **Amazon Bedrock**: Natural language understanding and course matching
- **AWS Lambda**: Filtering & ranking logic
- **Streamlit**: Interactive frontend

## Run it

```bash
pip install -r requirements.txt
streamlit run app_fixed.py --server.port 8517
```

## Contributors:
Divit Purwar, Abhiram Godavarthy, Benjamin Qiao, Arya Somasundaram
