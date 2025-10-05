# 📊 CSV Course Data Integration Guide

## Quick Setup for CSV → Knowledge Base → Agent

### 1. Prepare Your CSV File
Ensure your CSV has these columns:
```
course_code,title,description,time,days,instructor,credits,ge_area,prerequisites
CS188,Artificial Intelligence,Introduction to AI concepts,MWF 10-11,MWF,Prof Smith,4,STEM,CS61B
LING20,Intro to Linguistics,Basic linguistic concepts,TuTh 2-3:30,TuTh,Prof Jones,4,Humanities,None
```

### 2. Convert CSV to Knowledge Base Format
```bash
python csv_to_knowledge_base.py
```
This creates individual JSON documents for each course.

### 3. Upload to S3
```bash
aws s3 mb s3://your-coursematch-bucket
aws s3 sync knowledge_base_docs/ s3://your-coursematch-bucket/coursematch-kb/
```

### 4. Create Knowledge Base
1. **OpenSearch Serverless Collection**:
   - Name: `coursematch-kb`
   - Type: Vector search
   - Encryption: AWS owned key

2. **Bedrock Knowledge Base**:
   - Name: CourseMatchAI-KB
   - Embedding model: Amazon Titan Text Embeddings
   - Data source: S3 bucket with course JSON files

### 5. Update Agent Configuration
Replace IDs in `bedrock_agent.py`:
```python
self.knowledge_base_id = "YOUR_ACTUAL_KB_ID"
```

### 6. Test Integration
```bash
python test_knowledge_base.py
```

## 🔄 How It Works

1. **CSV → JSON**: Each course becomes a searchable document
2. **S3 Storage**: Documents stored in S3 for Knowledge Base access
3. **Vector Embeddings**: Titan creates semantic embeddings for each course
4. **Agent Retrieval**: Agent searches KB for relevant courses based on student query
5. **Smart Recommendations**: Agent combines KB results with reasoning to recommend courses

## 🎯 Agent Queries That Now Work

- "Find me AI courses that don't conflict with my Tuesday schedule"
- "What linguistics courses are offered in the fall?"
- "Show me all computer science courses with Prof Smith"
- "I need 4-unit courses that satisfy GE requirements"

## 📈 Benefits

- **Real Course Data**: Uses actual UCLA course catalog
- **Semantic Search**: Finds courses by meaning, not just keywords
- **Always Updated**: Easy to refresh with new CSV data
- **Scalable**: Handles thousands of courses efficiently

The agent now has access to your complete course catalog and can make intelligent recommendations based on real scheduling data!