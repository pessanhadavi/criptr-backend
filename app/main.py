from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from app.core.config import settings
from app.routes import auth, user
# alembic responsável pelo gerenciamento de migrações do bd
# from app.database import Base, engine
# Base.metadata.create_all(bind=engine)

app = FastAPI(title="CriptoTrack API")

# Configurações de CORS
app.add_middleware(
    CORSMiddleware,
    allow_origins=settings.CORS_ORIGINS, # <-- Usar a lista de settings
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

app.include_router(auth.router, prefix="/auth", tags=["auth"])
app.include_router(user.router, prefix="/users", tags=["users"])

@app.get("/")
def read_root():
    return {"message": "Welcome to CriptoTrack API"}
