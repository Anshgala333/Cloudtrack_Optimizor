import time
import os
from fastapi import HTTPException,status
from algorithm.truckFilling import pack_trucks_from_csv
from fastapi.responses import JSONResponse
from config.config import settings
from pathlib import Path
from services.optimizer import optimize



UPLOAD_DIR = settings.upload_dir
ALLOWED_FORMAT = [".csv" , ".xlsx"]


async def upload_file(file):
    try:
        print(UPLOAD_DIR)
        ext = Path(file.filename).suffix
        print(ext)
        
        # only csv file upload
        if ext not in ALLOWED_FORMAT:
            raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=f"Only CSV files are allowed. {ext}"
            
        )

        name = f"{time.time()}_{file.filename}"
        path = os.path.join(UPLOAD_DIR, name)

        with open(path, "wb") as f:
            content = await file.read()
            f.write(content)

        # response = pack_trucks_from_csv(path)
        response = optimize(path)
        
        return JSONResponse(
            status_code=200,
            content={
                "message": "File uploaded and processed successfully",
                "fileName": name,
                "message1": response
            },
        )
    except Exception as e:
        return JSONResponse(
            status_code=500,
            content={"error": str(e), "message": "Failed to upload and process file"},
        )
