import os
import uuid
from datetime import datetime
from qdrant_client import QdrantClient
from qdrant_client.models import Distance, VectorParams, PointStruct
from google import genai
from src.core.config import settings

# 1. INICJALIZACJA KLIENTÓW
qclient = QdrantClient(url=settings.qdrant_url, timeout=60)
gclient = genai.Client(api_key=settings.gemini_api_key)

COLLECTION_NAME = "content_memory"

def init_memory():
    """Tworzy kolekcję w Qdrant, jeśli jeszcze nie istnieje."""
    try:
        collections = qclient.get_collections().collections
        exists = any(c.name == COLLECTION_NAME for c in collections)
        
        if not exists:
            print(f"LOG [MEMORY]: Tworzę nową kolekcję: {COLLECTION_NAME}")
            qclient.create_collection(
                collection_name=COLLECTION_NAME,
                vectors_config=VectorParams(size=768, distance=Distance.COSINE),
            )
            print("✅ LOG [MEMORY]: Kolekcja utworzona.")
    except Exception as e:
        print(f"❌ LOG [MEMORY]: Błąd inicjalizacji bazy: {e}")

def get_embedding(text: str):
    """Generuje wektor dla podanego tekstu."""
    result = gclient.models.embed_content(
        model="text-embedding-004",
        contents=text
    )
    return result.embeddings[0].values

def save_campaign_to_memory(brief_data: dict, topic: str):
    """Zapisuje raport kampanii do bazy Qdrant z pełnymi metadanymi."""
    try:
        # 1. Inicjalizacja (na wypadek gdyby kolekcji nie było)
        init_memory()

        print(f"LOG [MEMORY]: Generowanie embeddingu dla tematu: {topic}...")
        
        # 2. Pobieramy wektor (na podstawie tematu i strategii ogólnej)
        content_to_embed = f"Topic: {topic}. Strategy: {brief_data.get('overall_strategy', '')}"
        vector = get_embedding(content_to_embed)
        
        # 3. Przygotowujemy punkt danych
        point_id = str(uuid.uuid4())
        timestamp_str = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        
        # Ekstrakcja metadanych klipów
        clips_meta = []
        for c in brief_data.get('clip_strategies', []):
            clips_meta.append({
                "idx": c.get('clip_index'),
                "duration": c.get('duration_seconds'),
                "hook_sample": c.get('posts', [{}])[0].get('content', '')[:100]
            })
        
        # 4. Zapis do bazy
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
        print(f"✅ LOG [MEMORY]: Kampania '{topic}' pomyślnie zapisana do pamięci długotrwałej.")
        return point_id

    except Exception as e:
        print(f"❌ LOG [MEMORY]: Błąd podczas zapisu do pamięci: {e}")
        return None
