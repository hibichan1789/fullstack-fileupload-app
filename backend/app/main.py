#main.py
from fastapi import FastAPI, UploadFile, File, HTTPException, Header
from contextlib import asynccontextmanager
import os
from .utils import file_ops
from .routes import image

upload_file_dir:str = "uploads/images"
@asynccontextmanager
async def lifespan(app:FastAPI):
    print("アプリが起動しました")
    os.makedirs(upload_file_dir, exist_ok=True)
    yield
    print("アプリが終了しました")

app = FastAPI(lifespan=lifespan)

#appにAPIrouterを登録するだけ
app.include_router(image.router)