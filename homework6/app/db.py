from sqlalchemy.ext.asyncio import create_async_engine, async_sessionmaker
from app.models import Base
from app.config import PG_CONN_URI

async_engine = create_async_engine(
    PG_CONN_URI,
    echo=True,
)

async_session = async_sessionmaker(
    bind=async_engine,
    expire_on_commit=False,
)


async def create_tables():
    async with async_engine.begin() as conn:
        await conn.run_sync(Base.metadata.drop_all)
        await conn.run_sync(Base.metadata.create_all)
