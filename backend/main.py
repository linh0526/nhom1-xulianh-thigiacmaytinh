import os
import tempfile
import requests
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
    temp_path = None
    try:
        # Tạo file tạm thời và đóng handle ngay lập tức để tránh lỗi Permission trên Windows
        fd, temp_path = tempfile.mkstemp(suffix=".jpg")
        os.close(fd)
        
        # Thiết lập Headers để tránh bị chặn 403 Forbidden
        headers = {
            "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36"
        }
        
        # Tải ảnh từ URL sử dụng requests với timeout
        response = requests.get(request.image_url, stream=True, timeout=10, headers=headers)
        response.raise_for_status() # Ném lỗi nếu HTTP code không phải 2xx

        # Ghi nội dung ảnh vào file tạm
        with open(temp_path, 'wb') as f:
            for chunk in response.iter_content(chunk_size=8192):
                f.write(chunk)

        # Gọi hàm dự đoán
        result = predict_fake_news(temp_path, request.text)

        return result
        
    except requests.exceptions.RequestException as e:
        # Xử lý riêng các lỗi liên quan đến việc tải ảnh (URL sai, timeout, 403, 404...)
        raise HTTPException(status_code=400, detail=f"Không thể tải ảnh từ URL: {str(e)}")
    except Exception as e:
        # Lỗi hệ thống hoặc lỗi trong lúc model inference
        raise HTTPException(status_code=500, detail=f"Lỗi xử lý nội bộ: {str(e)}")
    finally:
        # Luôn luôn dọn dẹp file tạm dù có lỗi hay không
        if temp_path and os.path.exists(temp_path):
            os.remove(temp_path)

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