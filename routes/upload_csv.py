from fastapi import APIRouter,UploadFile,File
from algorithm.truckFilling import pack_trucks_from_csv
from algorithm.DifferentSize.differentsize import main as differentSize
from controller.upload_controller import upload_file
import os

upload = APIRouter(prefix="/upload" , tags=["upload csv"])
UPLOAD_DIR = "uploads"


@upload.post("/upload-csv")
async def uploadFile(file : UploadFile = File(...)):
    return await upload_file(file)
    

@upload.get("/getDataForThisCSV/boxOfSameSize/{filename}")
def getDataForThisCSV1(filename:str):
    
    path = os.path.join(UPLOAD_DIR, filename)
    response = pack_trucks_from_csv(path)
    return {"message":response}

# @upload.get("/getDataForThisCSV/boxOfDifferentSize/{filename}")
# def getDataForThisCSV1(filename:str):
    
#     path = os.path.join(UPLOAD_DIR, filename)
#     response = differentSize(path)
#     return response

    