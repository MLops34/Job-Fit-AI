from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from Backend.routers import match
import uvicorn

app = FastAPI(
    title="JobFitAI - Intelligent Job Matching API",
    description="Backend API for matching resumes to job descriptions using ML and LLMs",
    version="1.0.0"
)

origins = [
    "http://localhost:8501",  # Streamlit frontend URL
]

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,   # allow frontend origin
    allow_credentials=True,
    allow_methods=["*"],     # allow all HTTP methods
    allow_headers=["*"],     # allow all headers
)

app.include_router(match.router, prefix="/api/jobfit", tags=["Job Matching"])

@app.get("/")
async def root():
    return {"message": "Welcome to JobFitAI API!"}

if __name__ == "__main__":
    uvicorn.run("main:app", host="0.0.0.0", port=8000, reload=True)
