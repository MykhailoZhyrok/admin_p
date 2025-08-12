
from uuid import uuid4
import aiofiles
from fastapi import HTTPException, UploadFile
from pathlib import Path 


UPLOAD_DIR = Path("uploads")
UPLOAD_DIR.mkdir(parents=True, exist_ok=True)

MAX_FILE_SIZE = 5 * 1024 * 1024  

async def uploaderImg(file: UploadFile):
    print(file, "FILE___")
    if not file:
        return None
    

    if not file.content_type.startswith("image/"):
        raise HTTPException(status_code=400, detail="File must be an image")

    content = await file.read()
    if len(content) > MAX_FILE_SIZE:
        raise HTTPException(status_code=400, detail="File too large")

    file_extension = file.filename.split(".")[-1]
    file_name = f"{uuid4()}.{file_extension}"
    file_path = UPLOAD_DIR / file_name

    async with aiofiles.open(file_path, "wb") as out_file:
        await out_file.write(content)

    return f"/uploads/{file_name}"
