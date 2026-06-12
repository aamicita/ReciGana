from pydantic import BaseModel, EmailStr

class UsuarioCreate(BaseModel):
    nombre: str
    email: EmailStr
    ciudad: str

class UsuarioResponse(BaseModel):
    id: int
    nombre: str
    email: str
    ciudad: str
    puntos_totales: int

    class Config:
        from_attributes = True

class MaterialCreate(BaseModel):
    nombre: str
    tipo: str
    puntos_por_kg: int

class MaterialResponse(BaseModel):
    id: int
    nombre: str
    tipo: str
    puntos_por_kg: int

    class Config:
        from_attributes = True

class ReciclajeCreate(BaseModel):
    usuario_id: int
    material_id: int
    cantidad_kg: float