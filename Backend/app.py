from fastapi import FastAPI

app = FastAPI()

@app.get("/hello")
def say_hello():
    return {"message": "Hello from your new FastAPI app!"}


@app.get("/")
def root():
    return {"message": "Welcome to JobFitAI API!"}
