from fastapi import FastAPI

app = FastAPI(
    title="Water Quality Monitoring API",
    description="IoT backend for water quality sensor data",
    version="1.0.0"
)


@app.get("/")
async def root():
    return {"message": "Water Quality API"}


@app.get("/health")
async def health():
    return {"status": "healthy"}