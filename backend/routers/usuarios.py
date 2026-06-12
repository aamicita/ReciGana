from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from database import get_db
from models import UsuarioDB
from schemas import UsuarioCreate, UsuarioResponse

router = APIRouter(prefix="/usuarios", tags=["usuarios"])

@router.post("/", response_model=UsuarioResponse)
def crear_usuario(usuario: UsuarioCreate, db: Session = Depends(get_db)):
    existe = db.query(UsuarioDB).filter(
        UsuarioDB.email == usuario.email
    ).first()
    if existe:
        raise HTTPException(status_code=400, detail="Email ya registrado")
    nuevo = UsuarioDB(
        nombre=usuario.nombre,
        email=usuario.email,
        ciudad=usuario.ciudad,
        puntos_totales=0
    )
    db.add(nuevo)
    db.commit()
    db.refresh(nuevo)
    return nuevo

@router.get("/", response_model=list[UsuarioResponse])
def listar_usuarios(db: Session = Depends(get_db)):
    return db.query(UsuarioDB).all()

@router.get("/{usuario_id}", response_model=UsuarioResponse)
def ver_usuario(usuario_id: int, db: Session = Depends(get_db)):
    usuario = db.query(UsuarioDB).filter(
        UsuarioDB.id == usuario_id
    ).first()
    if not usuario:
        raise HTTPException(status_code=404, detail="Usuario no encontrado")
    return usuario