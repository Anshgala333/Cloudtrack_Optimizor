from fastapi import FastAPI
from routes.uploadCsv import upload
from fastapi.middleware.cors import CORSMiddleware
from fastapi.middleware.gzip import GZipMiddleware
import uvicorn

app = FastAPI()

# to reduce size of api response
app.add_middleware(GZipMiddleware, minimum_size=1000)
origins = [
    "http://localhost:4001",
]


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
    uvicorn.run("main:app", port=4000, reload=True)
