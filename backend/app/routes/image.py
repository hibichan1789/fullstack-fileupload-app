#image.py
from fastapi import APIRouter, UploadFile, File, HTTPException, Header
import os
from ..utils import file_ops
upload_file_dir:str = "uploads/images"
router = APIRouter()
@router.post("/uploads", status_code=201)
async def post_file(
    file:UploadFile=File(..., media_type="multipart/form-data"),
    content_length:int=Header(None, include_in_schema=False)
    ):
    file_name = file.filename
    if not file_name:
        raise HTTPException(status_code=400, detail="ファイル名がありません")
    original_file_name = os.path.basename(file_name)
    file_extension = os.path.splitext(original_file_name)[-1]
    if not file_ops.validate_extension(file_extension):
        raise HTTPException(status_code=400, detail=f"{file_extension}は認められてない拡張子です")
    content_type = file.content_type
    if not content_type or not file_ops.validate_content_type(content_type):
        raise HTTPException(status_code=400, detail="認められてないcontent typeです")
    if content_length is not None and not file_ops.validate_file_size(content_length):
        raise HTTPException(status_code=413, detail="ファイルサイズが大きすぎます(申告値)")
    file_size = file_ops.get_file_size(file)
    if not file_ops.validate_file_size(file_size):
        raise HTTPException(status_code=413, detail="ファイルサイズが大きすぎます(実測値)")
    
    stored_file_name = file_ops.generate_store_name(file_extension)
    os.makedirs(upload_file_dir, exist_ok=True)
    stored_file_path = os.path.join(upload_file_dir, stored_file_name)
    try:
        await file_ops.save_file(stored_file_path, file, chunk_size=1024)
    except Exception as e:
        raise HTTPException(status_code=500, detail="ファイルの保存に失敗しました")
    return {"status": "ok"}

