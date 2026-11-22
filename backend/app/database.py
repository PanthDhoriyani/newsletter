import os
from typing import AsyncGenerator
from sqlalchemy.orm import DeclarativeBase
from app.config import settings

class Base(DeclarativeBase):
    pass

# Check if aiosqlite or asyncpg is available for async engine
use_async = True
try:
    if "sqlite" in settings.database_url:
        import aiosqlite
    elif "postgres" in settings.database_url:
        import asyncpg
except ImportError:
    use_async = False

if use_async:
    from sqlalchemy.ext.asyncio import create_async_engine, async_sessionmaker, AsyncSession
    connect_args = {}
    if "sqlite" in settings.database_url:
        connect_args = {"check_same_thread": False}

    engine = create_async_engine(
        settings.database_url,
        echo=False,
        connect_args=connect_args,
        pool_pre_ping=True
    )
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
    # Standard SQLite fallback for local running environments where aiosqlite is not yet installed
    from sqlalchemy import create_engine
    from sqlalchemy.orm import sessionmaker, Session
    sync_url = settings.database_url.replace("sqlite+aiosqlite://", "sqlite://")
    engine = create_engine(sync_url, connect_args={"check_same_thread": False})
    SyncSessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

    # Asynchronous adapter wrapper
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
