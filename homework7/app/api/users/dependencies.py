from collections.abc import AsyncGenerator
from typing import Annotated

from fastapi import Depends
from sqlalchemy.ext.asyncio import AsyncSession

from .crud import UsersCRUD
from models.base import async_session


async def get_async_session() -> AsyncGenerator[AsyncSession]:
    async with async_session() as session:
        yield session


def users_crud(
    session: Annotated[
        AsyncSession,
        Depends(get_async_session),
    ],
) -> UsersCRUD:
    return UsersCRUD(session)


