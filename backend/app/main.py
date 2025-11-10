from fastapi import FastAPI, HTTPException
from pydantic import BaseModel
from mistralai import Mistral
from mistralai.models.sdkerror import SDKError
from sentence_transformers import SentenceTransformer
from qdrant_client import QdrantClient
from qdrant_client.http import models
import os
from dotenv import load_dotenv

# Load environment variables first
load_dotenv()

# Ensure API key exists
MISTRAL_API_KEY = os.getenv("MISTRAL_API_KEY")
if not MISTRAL_API_KEY:
    raise RuntimeError("Mistral API key is missing. Set MISTRAL_API_KEY in your .env file.")

# Initialize Mistral client
client = Mistral(api_key=MISTRAL_API_KEY)

# Fetch all accessible models
try:
    available_models = client.models.list()

    # Get the internal list of models
    models_list = getattr(available_models, "models", None) or getattr(available_models, "data", None)
    if not models_list:
        raise RuntimeError("No models available for this API key.")

    # Pick the first model
    MODEL_TO_USE = models_list[0].id
    print(f"Using model: {MODEL_TO_USE}")

except SDKError as e:
    raise RuntimeError(f"Failed to fetch available models: {e}")


# Initialize embeddings and Qdrant client
embedder = SentenceTransformer("all-MiniLM-L6-v2")
qdrant = QdrantClient(url=os.getenv("QDRANT_URL", "http://localhost:6333"))

# FastAPI setup
app = FastAPI()

class InputData(BaseModel):
    resume_text: str
    job_description: str

@app.post("/analyze")
async def analyze(data: InputData):
    try:
        # Create embeddings
        resume_emb = embedder.encode(data.resume_text).tolist()
        jd_emb = embedder.encode(data.job_description).tolist()

        # Upsert embeddings into Qdrant
        qdrant.recreate_collection(
            collection_name="docs",
            vectors_config=models.VectorParams(size=len(resume_emb), distance=models.Distance.COSINE)
        )
        qdrant.upsert("docs", points=[
            models.PointStruct(id=1, vector=resume_emb, payload={"type": "resume"}),
            models.PointStruct(id=2, vector=jd_emb, payload={"type": "jd"}),
        ])

        # Prepare prompt for the model
        prompt = f"""
        You are an expert career assistant.

        Resume:
        {data.resume_text}

        Job Description:
        {data.job_description}

        Tasks:
        1. Suggest 3 specific resume edits.
        2. Provide 3 tailored interview questions.
        3. Write 2 bullet points suitable for a cover letter.
        """

        # Call Mistral API
        try:
            response = client.chat.complete(
                model=MODEL_TO_USE,
                messages=[{"role": "user", "content": prompt}]
            )
                    # Try common possibilities
            result_text = getattr(response, "output_text", None) \
                    or getattr(response, "result", None)

            # Some SDKs store it in choices[0].content
            if not result_text and hasattr(response, "choices"):
                result_text = response.choices[0].content if response.choices else None

            if not result_text:
                raise HTTPException(status_code=500, detail="Mistral response has no text")
        except SDKError as e:
            raise HTTPException(status_code=401, detail=f"Mistral API error: {e}")

        return {"result": result_text}

    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))
