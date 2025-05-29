from sqlalchemy.ext.asyncio import create_async_engine, AsyncSession
from sqlalchemy.orm import sessionmaker, declarative_base

# URL async para SQLite 
SQLALCHEMY_DATABASE_URL = "sqlite+aiosqlite:///./sql_app.db"

# Crear motor async
engine = create_async_engine(
    SQLALCHEMY_DATABASE_URL,
    echo=True,  # Opcional: muestra logs de SQL
)

# Crear sesión async
AsyncSessionLocal = sessionmaker(
    bind=engine,
    class_=AsyncSession,
    expire_on_commit=False,
)

# Base para modelos
Base = declarative_base()

# Dependencia para obtener sesión async en FastAPI (por ejemplo)
async def get_db():
    async with AsyncSessionLocal() as session:
        yield session
