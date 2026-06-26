import os
import tempfile
import urllib.request
from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel

from src.inference.predictor import predict_fake_news

app = FastAPI(title="Fake News Detection API")

# Setup CORS for the extension
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # Allows all origins
    allow_credentials=True,
    allow_methods=["*"],  # Allows all methods
    allow_headers=["*"],  # Allows all headers
)

class AnalyzeRequest(BaseModel):
    image_url: str
    text: str

@app.post("/analyze")
def analyze_endpoint(request: AnalyzeRequest):
    try:
        # Download the image to a temporary file
        fd, temp_path = tempfile.mkstemp(suffix=".jpg")
        os.close(fd)
        
        # Download image from URL
        urllib.request.urlretrieve(request.image_url, temp_path)

        # Call predict_fake_news
        result = predict_fake_news(temp_path, request.text)

        # Clean up temp file
        os.remove(temp_path)

        return result
    except Exception as e:
        if os.path.exists(temp_path):
            os.remove(temp_path)
        raise HTTPException(status_code=500, detail=str(e))

class FeedbackRequest(BaseModel):
    image_url: str
    text: str
    is_correct: bool
    user_feedback: str

@app.post("/feedback")
def feedback_endpoint(request: FeedbackRequest):
    import json
    from datetime import datetime
    os.makedirs("data", exist_ok=True)
    with open("data/feedback_log.jsonl", "a", encoding="utf-8") as f:
        log_entry = {
            "timestamp": datetime.now().isoformat(),
            "image_url": request.image_url,
            "text": request.text,
            "is_correct": request.is_correct,
            "user_feedback": request.user_feedback
        }
        f.write(json.dumps(log_entry, ensure_ascii=False) + "\n")
    return {"status": "success", "message": "Feedback received"}

if __name__ == "__main__":
    import uvicorn
    uvicorn.run("backend.main:app", host="0.0.0.0", port=8000, reload=True)
