from fastapi import FastAPI

app = FastAPI(
    title="Personal AI Command Center",
    version="0.1.0",
)


@app.get("/")
def root():
    return {
        "message": "Personal AI Command Center API",
        "status": "running",
    }