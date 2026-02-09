#main.py
from fastapi import FastAPI, UploadFile, File, HTTPException, Header
from contextlib import asynccontextmanager
import os
from .utils import file_ops
from .routes import image
from fastapi.middleware.cors import CORSMiddleware
frontend_url = os.environ.get("FRONTEND_URL", "http://localhost:5173")
frontend_urls = [frontend_url]
upload_file_dir:str = "uploads/images"
@asynccontextmanager
async def lifespan(app:FastAPI):
    print("アプリが起動しました")
    os.makedirs(upload_file_dir, exist_ok=True)
    if frontend_url:
        frontend_urls.append(frontend_url)
    yield
    print("アプリが終了しました")

app = FastAPI(lifespan=lifespan)
app.add_middleware(
    CORSMiddleware,
    allow_origins=frontend_urls,
    allow_credentials=True,
    allow_methods=["*"], 
    allow_headers=["*"]
)
#appにAPIrouterを登録するだけ
app.include_router(image.router)