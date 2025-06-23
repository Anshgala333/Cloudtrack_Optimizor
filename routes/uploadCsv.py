from fastapi import APIRouter,UploadFile,File
from datetime import datetime
from Algorithm.truckFilling import pack_trucks_from_csv
import time
import os

upload = APIRouter(prefix="/upload" , tags=["upload csv"])
UPLOAD_DIR = "uploads"


@upload.post("/upload-csv")
async def uploadFile(file : UploadFile = File(...)):
    print(file)
    name = f'{time.time()}_{file.filename}'
    path = os.path.join(UPLOAD_DIR , name)
    
    with open(path , "wb") as f:
        content = await file.read()
        f.write(content)
        

    response = pack_trucks_from_csv(path)
    
@upload.get('/')
def greet():
    return {"from file route"}
    