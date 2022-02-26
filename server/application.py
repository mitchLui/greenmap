from turtle import st
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import JSONResponse
from sqlalchemy import JSON
import uvicorn

origins = ["*"]

app = FastAPI()

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["GET", "POST"],
    allow_headers=["*"],
)

@app.get("/")
def app_root() -> JSONResponse:
    return JSONResponse(content={"message": "app is running"}, status_code=200)

if __name__ == "__main__":
    uvicorn.run("application:app", host="0.0.0.0", port=5001, reload=True)