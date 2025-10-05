# 🤖 CourseMatchAI Bedrock Agent Setup

## Overview
CourseMatchAI now includes a full Amazon Bedrock Agent implementation for intelligent course recommendations.

## 🏗️ Architecture
```
Student Query → Bedrock Agent → Lambda Action Group → Course Database → AI Response
```

## 📁 Agent Files
- `bedrock_agent.py` - Agent client wrapper
- `lambda_function.py` - Action group Lambda function  
- `agent_setup.py` - Agent configuration
- `agent_demo.py` - Test script

## 🚀 Setup Steps

### 1. Create Lambda Function
```bash
# Package the Lambda function
zip -r coursematch-lambda.zip lambda_function.py course_data.py schedule_parser.py

# Deploy via AWS CLI or Console
aws lambda create-function \
  --function-name coursematch-search \
  --runtime python3.9 \
  --role arn:aws:iam::ACCOUNT:role/lambda-execution-role \
  --handler lambda_function.lambda_handler \
  --zip-file fileb://coursematch-lambda.zip
```

### 2. Create Bedrock Agent
1. Go to Amazon Bedrock Console
2. Navigate to "Agents" 
3. Click "Create Agent"
4. Use configuration from `agent_setup.py`:
   - Name: CourseMatchAI-Agent
   - Foundation Model: Claude 3 Sonnet
   - Instructions: Copy from agent_setup.py

### 3. Add Action Group
1. In your agent, click "Add Action Group"
2. Name: CourseSearch
3. Lambda Function: coursematch-search
4. API Schema: Copy from agent_setup.py

### 4. Update Agent ID
Replace `COURSEMATCH_AGENT_ID` in `bedrock_agent.py` with your actual agent ID.

### 5. Test Agent
```bash
python agent_demo.py
```

## 🎯 Agent Capabilities
- **Natural Language Processing**: Understands student interests and goals
- **Schedule Analysis**: Parses current course schedules
- **Intelligent Matching**: Finds courses matching interests + schedule
- **Contextual Explanations**: Explains why courses are recommended
- **Knowledge Base Integration**: Can reference course catalogs and requirements

## 🔧 Streamlit Integration
The main app now offers two modes:
1. **AI Agent (Recommended)**: Full conversational AI with reasoning
2. **Direct Bedrock API**: Simple semantic matching

## 📊 Demo Queries
- "I'm interested in AI and cognitive science, recommend courses"
- "Find linguistics courses that fit my Tuesday/Thursday schedule"
- "What courses would help with machine learning career goals?"

## 🌟 Benefits Over Direct API
- **Conversational**: Natural language interaction
- **Contextual**: Remembers conversation history
- **Extensible**: Easy to add new capabilities
- **Traceable**: Full reasoning transparency
- **Scalable**: Handles complex multi-step queries

Perfect for hackathon demos showcasing advanced GenAI capabilities!