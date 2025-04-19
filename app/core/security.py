from datetime import datetime, timedelta, timezone
from typing import Optional
from fastapi import Depends, HTTPException, status
from fastapi.security import OAuth2PasswordBearer
from jose import JWTError, jwt
from passlib.context import CryptContext
from sqlalchemy.orm import Session
from app.core.config import settings
from app.database import get_db
from app.models.user import User
from app.schemas.token import TokenData

# --- Configuração de Hashing de Senha ---
pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")

# --- Esquema OAuth2 ---
# Define o endpoint que o cliente deve usar para obter o token.
oauth2_scheme = OAuth2PasswordBearer(tokenUrl="/auth/token")

# --- Funções Utilitárias de Senha ---
def verify_password(plain_password: str, hashed_password: str) -> bool:
    """Verifica se a senha fornecida corresponde ao hash armazenado."""
    return pwd_context.verify(plain_password, hashed_password)

def hash_password(password: str) -> str:
    """Gera o hash de uma senha."""
    return pwd_context.hash(password)

# --- Funções Utilitárias de Token JWT ---
def create_access_token(data: dict, expires_delta: Optional[timedelta] = None) -> str:
    """Cria um novo token de acesso JWT."""
    to_encode = data.copy()
    if expires_delta:
        expire = datetime.now(timezone.utc) + expires_delta
    else:
        # tempo de expiração das configurações
        expire = datetime.now(timezone.utc) + timedelta(minutes=settings.ACCESS_TOKEN_EXPIRE_MINUTES)

    to_encode.update({"exp": expire})
    encoded_jwt = jwt.encode(to_encode, settings.SECRET_KEY, algorithm=settings.ALGORITHM)
    return encoded_jwt

# --- Dependência Principal: get_current_user ---
async def get_current_user(
    token: str = Depends(oauth2_scheme), db: Session = Depends(get_db)
) -> User:
    """
    Dependência FastAPI para obter o usuário atual a partir do token JWT.

    Decodifica o token, valida as credenciais e busca o usuário no banco de dados.
    Levanta HTTPException 401 se o token for inválido ou o usuário não for encontrado.
    """
    credentials_exception = HTTPException(
        status_code=status.HTTP_401_UNAUTHORIZED,
        detail="Could not validate credentials",
        headers={"WWW-Authenticate": "Bearer"}, # Padrão para indicar autenticação Bearer
    )
    try:
        # Decodifica o token usando a chave secreta e o algoritmo das configurações
        payload = jwt.decode(
            token, settings.SECRET_KEY, algorithms=[settings.ALGORITHM]
        )
        # Extrai o username do campo 'sub' do payload
        username: str = payload.get("sub")
        if username is None:
            raise credentials_exception

        # Valida o payload usando o schema TokenData
        token_data = TokenData(username=username)

    except JWTError:
        raise credentials_exception

    # Busca o usuário no banco de dados pelo username extraído
    user = db.query(User).filter(User.username == token_data.username).first()
    if user is None:
        raise credentials_exception
    return user
