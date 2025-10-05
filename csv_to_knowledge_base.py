import pandas as pd
import boto3
import json

def prepare_csv_for_knowledge_base(csv_file_path="ucla_courses.csv", output_dir="knowledge_base_docs"):
    """Convert CSV to individual JSON documents for Knowledge Base"""
    
    # Read CSV
    df = pd.read_csv(csv_file_path)
    
    # Create documents directory
    import os
    os.makedirs(output_dir, exist_ok=True)
    
    # Convert each row to a document
    for idx, row in df.iterrows():
        doc = {
            "course_id": f"{row.get('course_code', '')}-{idx}",
            "course_code": row.get('course_code', ''),
            "title": row.get('title', ''),
            "description": row.get('description', ''),
            "time": row.get('time', ''),
            "days": row.get('days', ''),
            "instructor": row.get('instructor', ''),
            "credits": row.get('credits', ''),
            "ge_area": row.get('ge_area', ''),
            "prerequisites": row.get('prerequisites', ''),
            "full_text": f"{row.get('course_code', '')} {row.get('title', '')} {row.get('description', '')} {row.get('time', '')} {row.get('days', '')}"
        }
        
        # Save as JSON file
        with open(f"{output_dir}/course_{idx}.json", 'w') as f:
            json.dump(doc, f, indent=2)
    
    print(f"Created {len(df)} course documents in {output_dir}/")
    return output_dir

def upload_to_s3(local_dir, bucket_name, s3_prefix="coursematch-kb/"):
    """Upload knowledge base documents to S3"""
    s3 = boto3.client('s3')
    
    import os
    for filename in os.listdir(local_dir):
        if filename.endswith('.json'):
            s3.upload_file(
                f"{local_dir}/{filename}",
                bucket_name,
                f"{s3_prefix}{filename}"
            )
    
    print(f"Uploaded documents to s3://{bucket_name}/{s3_prefix}")

if __name__ == "__main__":
    # Use the CSV file in the same directory
    csv_file = "ucla_courses.csv"
    
    print(f"Processing {csv_file}...")
    
    # Convert CSV to knowledge base format
    docs_dir = prepare_csv_for_knowledge_base(csv_file)
    
    print("\nNext steps:")
    print("1. Upload to S3: aws s3 sync knowledge_base_docs/ s3://your-bucket/coursematch-kb/")
    print("2. Create Knowledge Base in Bedrock Console")
    print("3. Update COURSEMATCH_KB_ID in bedrock_agent.py")