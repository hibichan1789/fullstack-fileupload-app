from fastapi import FastAPI, UploadFile, File, HTTPException, Header
from contextlib import asynccontextmanager
import aiofiles
import uuid
import os

upload_file_dir:str = "uploads/images"
@asynccontextmanager
async def lifespan(app:FastAPI):
    print("アプリが起動しました")
    os.makedirs(upload_file_dir, exist_ok=True)
    yield
    print("アプリが終了しました")

app = FastAPI(lifespan=lifespan)

@app.post("/uploads", status_code=201)
async def post_file(
    file:UploadFile=File(..., media_type="multipart/form-data"),
    content_length:int=Header(None)
    ):
    file_name = file.filename
    if not file_name:
        raise HTTPException(status_code=400, detail="ファイル名がありません")
    original_file_name = os.path.basename(file_name)
    file_extension = os.path.splitext(original_file_name)[-1]
    if not validate_extension(file_extension):
        raise HTTPException(status_code=400, detail=f"{file_extension}は認められてない拡張子です")
    content_type = file.content_type
    if not content_type or not validate_content_type(content_type):
        raise HTTPException(status_code=400, detail="認められてないcontent typeです")
    if content_length is not None and not validate_file_size(content_length):
        raise HTTPException(status_code=413, detail="ファイルサイズが大きすぎます(申告値)")
    file_size = get_file_size(file)
    if not validate_file_size(file_size):
        raise HTTPException(status_code=413, detail="ファイルサイズが大きすぎます(実測値)")
    
    stored_file_name = generate_store_name(file_extension)
    os.makedirs(upload_file_dir, exist_ok=True)
    stored_file_path = os.path.join(upload_file_dir, stored_file_name)
    try:
        await save_file(stored_file_path, file, chunk_size=1024)
    except Exception as e:
        raise HTTPException(status_code=500, detail="ファイルの保存に失敗しました")
    return {"status": "ok"}


def validate_extension(file_extension:str)->bool:
    allowed_extensions = [".jpg", ".jpeg", ".png", ".gif"]
    return file_extension.lower() in allowed_extensions
def validate_file_size(file_size:int, max_mb:int=5)->bool:
    return file_size <= max_mb*1024*1024
def get_file_size(file:UploadFile)->int:
    file.file.seek(0,2)
    file_size = file.file.tell()
    file.file.seek(0)
    return file_size
def validate_content_type(content_type:str)->bool:
    allowed_content_type = [
        "image/jpeg",
        "image/png",
        "image/gif"
    ]
    return content_type in allowed_content_type

def generate_store_name(file_extension:str)->str:
    """引数に拡張子を入れることでuuidに基づいた一意なfile名が生成される"""
    return f"{uuid.uuid4()}{file_extension}"
async def save_file(file_path:str, content:UploadFile, chunk_size:int=1024*1024):
    try:
        async with aiofiles.open(file_path, "wb") as f:
            while True:
                chunk = await content.read(chunk_size)
                if not chunk:
                    break
                await f.write(chunk)
    finally:
        #書き込みが失敗してもカーソルを先頭に戻す
        await content.seek(0)