import os
from typing import AsyncGenerator
from sqlalchemy.orm import DeclarativeBase
from app.config import settings

class Base(DeclarativeBase):
    pass

db_url = settings.database_url

# Determine driver
if "asyncpg" in db_url:
    from sqlalchemy.ext.asyncio import create_async_engine, async_sessionmaker, AsyncSession
    engine = create_async_engine(db_url, echo=False, pool_pre_ping=True)
    AsyncSessionLocal = async_sessionmaker(bind=engine, expire_on_commit=False, class_=AsyncSession)

    async def get_db() -> AsyncGenerator[AsyncSession, None]:
        async with AsyncSessionLocal() as session:
            try:
                yield session
            except Exception:
                await session.rollback()
                raise
            finally:
                await session.close()

    async def create_all_tables():
        from app.models import Base as ModelBase
        async with engine.begin() as conn:
            await conn.run_sync(ModelBase.metadata.create_all)

else:
    # Standard PostgreSQL (psycopg2) or SQLite engine with async wrapper
    from sqlalchemy import create_engine
    from sqlalchemy.orm import sessionmaker, Session

    # Clean URL for psycopg2 if needed
    clean_url = db_url.replace("sqlite+aiosqlite://", "sqlite://")
    if clean_url.startswith("postgres://"):
        clean_url = clean_url.replace("postgres://", "postgresql+psycopg2://", 1)
    elif clean_url.startswith("postgresql://") and "+psycopg2" not in clean_url and "+asyncpg" not in clean_url and "+psycopg" not in clean_url:
        clean_url = clean_url.replace("postgresql://", "postgresql+psycopg2://", 1)

    connect_args = {}
    if "sqlite" in clean_url:
        connect_args["check_same_thread"] = False

    engine = create_engine(clean_url, connect_args=connect_args, pool_pre_ping=True)
    SyncSessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

    class AsyncSessionAdapter:
        def __init__(self, sync_session: Session):
            self._sync = sync_session

        async def __aenter__(self):
            return self

        async def __aexit__(self, exc_type, exc_val, exc_tb):
            if exc_type is not None:
                self._sync.rollback()
            self._sync.close()

        async def execute(self, statement, *args, **kwargs):
            return self._sync.execute(statement, *args, **kwargs)

        async def commit(self):
            self._sync.commit()

        async def flush(self):
            self._sync.flush()

        async def refresh(self, instance):
            self._sync.refresh(instance)

        async def rollback(self):
            self._sync.rollback()

        def add(self, instance):
            self._sync.add(instance)

        async def delete(self, instance):
            self._sync.delete(instance)

        async def refresh(self, instance):
            self._sync.refresh(instance)

        async def close(self):
            self._sync.close()

    def AsyncSessionLocal():
        return AsyncSessionAdapter(SyncSessionLocal())

    async def get_db() -> AsyncGenerator:
        adapter = AsyncSessionAdapter(SyncSessionLocal())
        try:
            yield adapter
        except Exception:
            await adapter.rollback()
            raise
        finally:
            await adapter.close()

    async def create_all_tables():
        from app.models import Base as ModelBase
        ModelBase.metadata.create_all(bind=engine)
