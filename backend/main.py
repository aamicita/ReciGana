from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from database import engine
from models import Base
from routers import usuarios, materiales

Base.metadata.create_all(bind=engine)

app = FastAPI(title="ReciGana API", version="1.0.0")

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

@app.get("/")
def inicio():
    return {"mensaje": "ReciGana API activa", "estado": "ok"}

@app.get("/health")
def health():
    return {"status": "ok"}

app.include_router(usuarios.router)
app.include_router(materiales.router)