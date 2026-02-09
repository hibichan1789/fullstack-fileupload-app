#utils/file_ops.py
from fastapi import UploadFile
import uuid
import aiofiles
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