import boto3
import json
import random

class CourseMatchAgent:
    def __init__(self, region='us-east-1'):
        self.region = region
        self.bedrock_agent_runtime = boto3.client(
            service_name="bedrock-agent-runtime",
            region_name=region
        )
        # You'll need to replace this with your actual agent ID after creating the agent
        self.agent_id = "COURSEMATCH_AGENT_ID"  # Replace with actual agent ID
        self.agent_alias_id = "TSTALIASID"
        self.knowledge_base_id = "COURSEMATCH_KB_ID"  # Replace with KB ID
    
    def generate_session_id(self):
        """Generate random 15-digit session ID"""
        return ''.join([str(random.randint(0, 9)) for _ in range(15)])
    
    def invoke_agent(self, query, session_attributes=None):
        """Invoke the CourseMatch agent with a query"""
        if session_attributes is None:
            session_attributes = {}
        
        try:
            response = self.bedrock_agent_runtime.invoke_agent(
                sessionState={
                    "sessionAttributes": session_attributes,
                    "promptSessionAttributes": {},
                    "knowledgeBaseConfigurations": [
                        {
                            "knowledgeBaseId": self.knowledge_base_id,
                            "retrievalConfiguration": {
                                "vectorSearchConfiguration": {
                                    "numberOfResults": 10
                                }
                            }
                        }
                    ]
                },
                agentId=self.agent_id,
                agentAliasId=self.agent_alias_id,
                sessionId=self.generate_session_id(),
                endSession=False,
                enableTrace=True,
                inputText=query,
            )
            
            return self.process_agent_response(response)
            
        except Exception as e:
            return {"error": f"Agent invocation failed: {str(e)}"}
    
    def process_agent_response(self, response):
        """Process the streaming response from the agent"""
        results = response.get("completion", [])
        final_answer = ""
        references = []
        
        for stream in results:
            try:
                # Process trace information
                trace = stream.get("trace", {}).get("trace", {}).get("orchestrationTrace", {})
                
                if trace:
                    # Knowledge base lookup
                    kb_input = trace.get("invocationInput", {}).get("knowledgeBaseLookupInput", {})
                    if kb_input:
                        print(f'Agent searching knowledge base: {kb_input.get("text", "")}')
                    
                    kb_output = trace.get("observation", {}).get("knowledgeBaseLookupOutput", {})
                    if kb_output:
                        retrieved_refs = kb_output.get("retrievedReferences", [])
                        references.extend(retrieved_refs)
                
                # Process final answer
                if "chunk" in stream:
                    chunk_text = stream["chunk"]["bytes"].decode("utf-8")
                    final_answer += chunk_text
                    
            except Exception as e:
                print(f"Error processing stream: {e}")
        
        # Clean up final answer
        final_answer = final_answer.strip()
        
        return {
            "answer": final_answer,
            "references": references,
            "success": True
        }

def create_course_recommendation_query(interests, current_schedule, filters=None):
    """Create a structured query for the agent"""
    schedule_text = ", ".join([f"{c.get('code', '')} ({c.get('days', '')}{c.get('start_time', '')}-{c.get('end_time', '')})" for c in current_schedule])
    
    query = f"""
    I am a UCLA student looking for course recommendations.
    
    My interests: {interests}
    My current schedule: {schedule_text}
    
    Please recommend courses that:
    1. Match my interests
    2. Don't conflict with my current schedule
    3. Are appropriate for my academic level
    
    """
    
    if filters:
        if filters.get('difficulty') and filters['difficulty'] != 'Any':
            query += f"Difficulty preference: {filters['difficulty']}\n"
        if filters.get('ge_area') and filters['ge_area'] != 'Any':
            query += f"GE area preference: {filters['ge_area']}\n"
        if filters.get('credits'):
            min_credits, max_credits = filters['credits']
            query += f"Credit range: {min_credits}-{max_credits} units\n"
    
    query += "\nPlease provide specific course recommendations with explanations."
    
    return query