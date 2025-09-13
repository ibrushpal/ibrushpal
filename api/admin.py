from fastapi import APIRouter, UploadFile, File, Depends, HTTPException
from fastapi.security import OAuth2PasswordBearer
from typing import List
import os
from datetime import datetime

router = APIRouter()
oauth2_scheme = OAuth2PasswordBearer(tokenUrl="token")

# 模拟用户验证
async def get_current_user(token: str = Depends(oauth2_scheme)):
    if token != "admin_token":
        raise HTTPException(status_code=401, detail="Invalid credentials")
    return {"username": "admin"}

@router.post("/upload-reference")
async def upload_reference_file(
    file: UploadFile = File(...),
    user: dict = Depends(get_current_user)
):
    """上传参考文件接口"""
    upload_dir = "references"
    os.makedirs(upload_dir, exist_ok=True)
    
    timestamp = datetime.now().strftime("%Y%m%d%H%M%S")
    filename = f"{timestamp}_{file.filename}"
    filepath = os.path.join(upload_dir, filename)
    
    with open(filepath, "wb") as buffer:
        content = await file.read()
        buffer.write(content)
    
    return {
        "status": "success",
        "filepath": filepath,
        "filename": filename
    }

@router.get("/list-references")
async def list_reference_files(user: dict = Depends(get_current_user)):
    """列出所有参考文件"""
    ref_dir = "references"
    if not os.path.exists(ref_dir):
        return []
    
    files = []
    for filename in os.listdir(ref_dir):
        path = os.path.join(ref_dir, filename)
        files.append({
            "filename": filename,
            "path": path,
            "size": os.path.getsize(path)
        })
    
    return files