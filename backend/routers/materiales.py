from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from database import get_db
from models import MaterialDB
from schemas import MaterialCreate, MaterialResponse

router = APIRouter(prefix="/materiales", tags=["materiales"])

@router.post("/", response_model=MaterialResponse)
def crear_material(material: MaterialCreate, db: Session = Depends(get_db)):
    nuevo = MaterialDB(
        nombre=material.nombre,
        tipo=material.tipo,
        puntos_por_kg=material.puntos_por_kg
    )
    db.add(nuevo)
    db.commit()
    db.refresh(nuevo)
    return nuevo

@router.get("/", response_model=list[MaterialResponse])
def listar_materiales(db: Session = Depends(get_db)):
    return db.query(MaterialDB).all()