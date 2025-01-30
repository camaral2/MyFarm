from fastapi import FastAPI, Depends
from routers import health, users

app = FastAPI()

# Include routers
app.include_router(health.router)

@app.get("/")
def read_root():
    return {"message": "Welcome to the API!"}