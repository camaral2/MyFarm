from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
 
from . import models
from .database import engine 
#from routers import health, users
from .routers import culture, user, auth, event_culture

app = FastAPI()

origins = [
    "http://localhost.teste.com",
    "https://localhost.teste.com",
    "http://localhost",
    "http://localhost:8080",
]

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

@app.get("/")
def root():
    return {"message": "Welcome To !"}

# Include routers
#app.include_router(health.router)
app.include_router(culture.router)
app.include_router(user.router)
app.include_router(auth.router)
app.include_router(event_culture.router)

