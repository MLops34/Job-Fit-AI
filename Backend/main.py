from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from Backend.routers import match

app = FastAPI()

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=False,
    allow_methods=["*"],
    allow_headers=["*"],
)

app.include_router(match.router, prefix="/api/jobfit")

@app.get("/")
async def root():
    return {"message": "Welcome to the JobFit API!"}