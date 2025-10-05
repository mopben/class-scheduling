import boto3
import json

def create_knowledge_base_config():
    """Configuration for creating CourseMatch Knowledge Base"""
    
    config = {
        "name": "CourseMatchAI-KB",
        "description": "UCLA course catalog for CourseMatchAI recommendations",
        "roleArn": "arn:aws:iam::ACCOUNT:role/AmazonBedrockExecutionRoleForKnowledgeBase",
        "knowledgeBaseConfiguration": {
            "type": "VECTOR",
            "vectorKnowledgeBaseConfiguration": {
                "embeddingModelArn": "arn:aws:bedrock:us-east-1::foundation-model/amazon.titan-embed-text-v1"
            }
        },
        "storageConfiguration": {
            "type": "OPENSEARCH_SERVERLESS",
            "opensearchServerlessConfiguration": {
                "collectionArn": "arn:aws:aoss:us-east-1:ACCOUNT:collection/coursematch-kb",
                "vectorIndexName": "coursematch-index",
                "fieldMapping": {
                    "vectorField": "vector",
                    "textField": "text",
                    "metadataField": "metadata"
                }
            }
        }
    }
    
    data_source_config = {
        "name": "UCLA-Courses-CSV",
        "description": "UCLA course data from CSV",
        "knowledgeBaseId": "KB_ID_PLACEHOLDER",
        "dataSourceConfiguration": {
            "type": "S3",
            "s3Configuration": {
                "bucketArn": "arn:aws:s3:::your-coursematch-bucket",
                "inclusionPrefixes": ["coursematch-kb/"]
            }
        },
        "vectorIngestionConfiguration": {
            "chunkingConfiguration": {
                "chunkingStrategy": "FIXED_SIZE",
                "fixedSizeChunkingConfiguration": {
                    "maxTokens": 300,
                    "overlapPercentage": 20
                }
            }
        }
    }
    
    return config, data_source_config

def print_setup_instructions():
    """Print step-by-step setup instructions"""
    
    print("📚 CourseMatch Knowledge Base Setup")
    print("=" * 50)
    
    print("\n1. Prepare Your CSV Data:")
    print("   - Ensure CSV has columns: course_code, title, description, time, days, instructor, credits, ge_area")
    print("   - Run: python csv_to_knowledge_base.py")
    
    print("\n2. Create S3 Bucket:")
    print("   aws s3 mb s3://your-coursematch-bucket")
    print("   aws s3 sync knowledge_base_docs/ s3://your-coursematch-bucket/coursematch-kb/")
    
    print("\n3. Create OpenSearch Serverless Collection:")
    print("   - Go to OpenSearch Service Console")
    print("   - Create Serverless Collection: 'coursematch-kb'")
    print("   - Type: Vector search")
    
    print("\n4. Create Knowledge Base:")
    print("   - Go to Bedrock Console > Knowledge bases")
    print("   - Create knowledge base with S3 data source")
    print("   - Use Titan embeddings model")
    
    print("\n5. Update Agent Configuration:")
    print("   - Add Knowledge Base to your Bedrock Agent")
    print("   - Update COURSEMATCH_KB_ID in bedrock_agent.py")
    
    print("\n6. Test Knowledge Base:")
    print("   python test_knowledge_base.py")

if __name__ == "__main__":
    config, data_source = create_knowledge_base_config()
    
    print("Knowledge Base Configuration:")
    print(json.dumps(config, indent=2))
    print("\nData Source Configuration:")
    print(json.dumps(data_source, indent=2))
    
    print("\n" + "=" * 50)
    print_setup_instructions()