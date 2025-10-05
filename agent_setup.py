import boto3
import json

def create_coursematch_agent():
    """
    Script to create the CourseMatch Bedrock Agent
    This would typically be run once to set up the agent infrastructure
    """
    
    # Agent configuration
    agent_config = {
        "agentName": "CourseMatchAI-Agent",
        "description": "AI agent that helps UCLA students find courses matching their interests and schedule",
        "foundationModel": "anthropic.claude-3-sonnet-20240229-v1:0",
        "instruction": """
        You are CourseMatchAI, an intelligent course recommendation agent for UCLA students.
        
        Your capabilities:
        1. Analyze student interests and academic goals
        2. Parse current course schedules 
        3. Recommend courses that match interests and fit schedules
        4. Explain why courses are good matches
        5. Consider factors like difficulty, GE requirements, and prerequisites
        
        When students ask for recommendations:
        1. Understand their interests and career goals
        2. Check their current schedule for conflicts
        3. Search the course catalog for relevant options
        4. Rank courses by relevance and compatibility
        5. Provide clear explanations for each recommendation
        
        Always be helpful, accurate, and consider the student's academic progression.
        """,
        "idleSessionTTLInSeconds": 1800
    }
    
    # Action groups for the agent
    action_groups = [
        {
            "actionGroupName": "CourseSearch",
            "description": "Search and filter UCLA course catalog",
            "actionGroupExecutor": {
                "lambda": "arn:aws:lambda:us-east-1:ACCOUNT:function:coursematch-search"
            },
            "apiSchema": {
                "payload": json.dumps({
                    "openapi": "3.0.0",
                    "info": {
                        "title": "Course Search API",
                        "version": "1.0.0"
                    },
                    "paths": {
                        "/search-courses": {
                            "post": {
                                "description": "Search for courses matching criteria",
                                "parameters": [
                                    {
                                        "name": "interests",
                                        "in": "query",
                                        "required": True,
                                        "schema": {"type": "string"}
                                    },
                                    {
                                        "name": "schedule",
                                        "in": "query", 
                                        "required": False,
                                        "schema": {"type": "string"}
                                    }
                                ],
                                "responses": {
                                    "200": {
                                        "description": "Course recommendations",
                                        "content": {
                                            "application/json": {
                                                "schema": {
                                                    "type": "object",
                                                    "properties": {
                                                        "courses": {
                                                            "type": "array",
                                                            "items": {"type": "object"}
                                                        }
                                                    }
                                                }
                                            }
                                        }
                                    }
                                }
                            }
                        }
                    }
                })
            }
        }
    ]
    
    print("Agent Configuration:")
    print(json.dumps(agent_config, indent=2))
    print("\nAction Groups:")
    print(json.dumps(action_groups, indent=2))
    
    print("\nTo create this agent:")
    print("1. Use AWS Console or CLI to create the Bedrock Agent")
    print("2. Create the Lambda function for course search")
    print("3. Set up knowledge base with UCLA course catalog")
    print("4. Update COURSEMATCH_AGENT_ID in bedrock_agent.py")
    
    return agent_config, action_groups

if __name__ == "__main__":
    create_coursematch_agent()