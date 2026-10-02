from fastapi import FastAPI

app = FastAPI(title="BarberForge AI API")

@app.get("/")
def read_root():
    return {"message": "API BarberForge AI activa"}

@app.get("/health")
def health_check():
    return {"status": "ok", "service": "backend"}