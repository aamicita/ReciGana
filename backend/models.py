from sqlalchemy import Column, Integer, String, Float, DateTime, ForeignKey
from sqlalchemy.orm import relationship
from sqlalchemy.sql import func
from database import Base

class UsuarioDB(Base):
    __tablename__ = "usuarios"
    id = Column(Integer, primary_key=True, index=True)
    nombre = Column(String(100), nullable=False)
    email = Column(String(200), unique=True, nullable=False)
    ciudad = Column(String(100))
    puntos_totales = Column(Integer, default=0)
    created_at = Column(DateTime, server_default=func.now())
    reciclajes = relationship("RecilajeDB", back_populates="usuario")

class MaterialDB(Base):
    __tablename__ = "materiales"
    id = Column(Integer, primary_key=True, index=True)
    nombre = Column(String(100), nullable=False)
    tipo = Column(String(50))
    puntos_por_kg = Column(Integer, nullable=False)

class RecilajeDB(Base):
    __tablename__ = "reciclajes"
    id = Column(Integer, primary_key=True, index=True)
    usuario_id = Column(Integer, ForeignKey("usuarios.id"), nullable=False)
    material_id = Column(Integer, ForeignKey("materiales.id"), nullable=False)
    cantidad_kg = Column(Float, nullable=False)
    puntos_ganados = Column(Integer, default=0)
    fecha = Column(DateTime, server_default=func.now())
    usuario = relationship("UsuarioDB", back_populates="reciclajes")
    material = relationship("MaterialDB")