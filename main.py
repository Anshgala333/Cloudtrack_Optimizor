from fastapi import FastAPI
from routes.upload_csv import upload
from fastapi.middleware.cors import CORSMiddleware
from fastapi.middleware.gzip import GZipMiddleware
import uvicorn
from fastapi.staticfiles import StaticFiles
import logging
from config.config import settings
from config.logger import create_logger


app = FastAPI()

# to reduce size of api response
app.add_middleware(GZipMiddleware, minimum_size=1000)
origins = ["*", "https://cloudtrack-optimizer.netlify.app/"]

app.mount("/maps", StaticFiles(directory="maps"), name="maps")


app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


@app.get("/")
def greet():
    return {"hello world"}


app.include_router(upload)

port = settings.port

        
if __name__ == "__main__":
    print(port)
    create_logger()
    uvicorn.run("main:app", host="0.0.0.0", port=port, reload=True)
    
