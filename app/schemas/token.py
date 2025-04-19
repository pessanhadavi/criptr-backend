from pydantic import BaseModel
from typing import Optional

class Token(BaseModel):
    """Schema para a resposta do token de acesso."""
    access_token: str
    token_type: str

class TokenData(BaseModel):
    """Schema para os dados contidos dentro do token JWT (o payload)."""
    username: Optional[str] = None
    # Lembrete: adicionar outros campos no payload do token
    # ex: user_id: Optional[int] = None
    # ex: roles: Optional[list[str]] = None
