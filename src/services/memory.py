import os
import uuid
from datetime import datetime
from qdrant_client import QdrantClient
from qdrant_client.models import Distance, VectorParams, PointStruct
from google import genai
from src.core.config import settings

# 1. CLIENT INITIALIZATION
qclient = QdrantClient(url=settings.qdrant_url, timeout=60)
gclient = genai.Client(api_key=settings.gemini_api_key)

COLLECTION_NAME = "content_memory"

def init_memory():
    """Creates collection in Qdrant if it doesn't exist yet."""
    try:
        collections = qclient.get_collections().collections
        exists = any(c.name == COLLECTION_NAME for c in collections)
        
        if not exists:
            print(f"LOG [MEMORY]: Creating new collection: {COLLECTION_NAME}")
            qclient.create_collection(
                collection_name=COLLECTION_NAME,
                vectors_config=VectorParams(size=768, distance=Distance.COSINE),
            )
            print("✅ LOG [MEMORY]: Collection created.")
    except Exception as e:
        print(f"❌ LOG [MEMORY]: Database initialization error: {e}")

def get_embedding(text: str):
    """Generates vector for given text."""
    result = gclient.models.embed_content(
        model="text-embedding-004",
        contents=text
    )
    return result.embeddings[0].values

def save_campaign_to_memory(brief_data: dict, topic: str):
    """Saves campaign report to Qdrant database with full metadata."""
    try:
        # 1. Initialization (in case collection doesn't exist)
        init_memory()

        print(f"LOG [MEMORY]: Generating embedding for topic: {topic}...")
        
        # 2. We get vector (based on topic and overall strategy)
        content_to_embed = f"Topic: {topic}. Strategy: {brief_data.get('overall_strategy', '')}"
        vector = get_embedding(content_to_embed)
        
        # 3. We prepare data point
        point_id = str(uuid.uuid4())
        timestamp_str = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        
        # Extraction of clip metadata
        clips_meta = []
        for c in brief_data.get('clip_strategies', []):
            clips_meta.append({
                "idx": c.get('clip_index'),
                "duration": c.get('duration_seconds'),
                "hook_sample": c.get('posts', [{}])[0].get('content', '')[:100]
            })
        
        # 4. Save to database
        qclient.upsert(
            collection_name=COLLECTION_NAME,
            points=[
                PointStruct(
                    id=point_id,
                    vector=vector,
                    payload={
                        "topic": topic,
                        "strategy": brief_data.get('overall_strategy'),
                        "clips": clips_meta,
                        "type": "campaign_brief",
                        "timestamp": timestamp_str,
                        "job_id": brief_data.get('job_id', 'unknown')
                    }
                )
            ]
        )
        print(f"✅ LOG [MEMORY]: Campaign '{topic}' successfully saved to long-term memory.")
        return point_id

    except Exception as e:
        print(f"❌ LOG [MEMORY]: Error while saving to memory: {e}")
        return None