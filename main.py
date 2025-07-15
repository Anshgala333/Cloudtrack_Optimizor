from fastapi import FastAPI
from routes.uploadCsv import upload
from fastapi.middleware.cors import CORSMiddleware
from fastapi.middleware.gzip import GZipMiddleware
import uvicorn
from fastapi.staticfiles import StaticFiles

app = FastAPI()

# to reduce size of api response
app.add_middleware(GZipMiddleware, minimum_size=1000)
origins = [
    "*",
]

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

if __name__ == "__main__":
    uvicorn.run("main:app", host="0.0.0.0", port=4000, reload=True)
