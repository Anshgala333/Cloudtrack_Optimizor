from fastapi import FastAPI
from routes.uploadCsv import upload 

app = FastAPI()


@app.get("/")
def greet():
    return{"hello world"}


app.include_router(upload)