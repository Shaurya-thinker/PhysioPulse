import os
import shutil
import uuid
import json
from fastapi import FastAPI, File, UploadFile
from fastapi.responses import JSONResponse
from src.video_analyzer import run_pipeline

app = FastAPI(title="Telerehab AI API")

UPLOAD_DIR = "input_videos"
OUTPUT_DIR = "output_data"
os.makedirs(UPLOAD_DIR, exist_ok=True)
os.makedirs(OUTPUT_DIR, exist_ok=True)

@app.post("/analyze")
async def analyze_pose(video: UploadFile = File(...)):
    # Save uploaded file
    file_id = str(uuid.uuid4())
    video_path = os.path.join(UPLOAD_DIR, f"{file_id}_{video.filename}")
    
    with open(video_path, "wb") as buffer:
        shutil.copyfileobj(video.file, buffer)
 
    # Run the analysis pipeline
    result_paths = run_pipeline(video_path, OUTPUT_DIR)

    # Load scores JSON
    with open(result_paths["scores_file"], "r") as f:
        scores_data = json.load(f)

    # Load landmarks JSON
    with open(result_paths["landmarks_file"], "r") as f:
        landmarks_data = json.load(f)

    return JSONResponse(content={
        "status": "success",
        "video_file": video.filename,
        "scores": scores_data,
        "landmarks": landmarks_data
    })

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)
