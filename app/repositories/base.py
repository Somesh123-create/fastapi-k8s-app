"""Repository pattern implementation for data access."""

from typing import Any, Generic, Optional, Sequence, TypeVar

from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

T = TypeVar("T")


class BaseRepository(Generic[T]):
    """Base repository class with common CRUD operations."""

    def __init__(self, session: AsyncSession, model: type[T]) -> None:
        """Initialize repository.

        Args:
            session: AsyncSession instance
            model: SQLAlchemy model class
        """
        self.session = session
        self.model = model

    async def create(self, obj_in: dict[str, Any]) -> T:
        """Create new object.

        Args:
            obj_in: Object data dictionary

        Returns:
            Created object
        """
        db_obj = self.model(**obj_in)
        self.session.add(db_obj)
        await self.session.commit()
        await self.session.refresh(db_obj)
        return db_obj

    async def get(self, obj_id: str) -> Optional[T]:
        """Get object by ID.

        Args:
            obj_id: Object ID

        Returns:
            Object or None
        """
        statement = select(self.model).where(self.model.id == obj_id)  # type: ignore[attr-defined]
        result = await self.session.execute(statement)
        return result.scalars().first()

    async def get_all(self, skip: int = 0, limit: int = 100) -> Sequence[T]:
        """Get all objects with pagination.

        Args:
            skip: Number of records to skip
            limit: Maximum number of records to return

        Returns:
            Sequence of objects
        """
        statement = select(self.model).offset(skip).limit(limit)
        result = await self.session.execute(statement)
        return result.scalars().all()

    async def update(self, obj_id: str, obj_in: dict[str, Any]) -> Optional[T]:
        """Update object.

        Args:
            obj_id: Object ID
            obj_in: Update data dictionary

        Returns:
            Updated object or None
        """
        db_obj = await self.get(obj_id)
        if not db_obj:
            return None

        for field, value in obj_in.items():
            if value is not None:
                setattr(db_obj, field, value)

        self.session.add(db_obj)
        await self.session.commit()
        await self.session.refresh(db_obj)
        return db_obj

    async def delete(self, obj_id: str) -> bool:
        """Delete object.

        Args:
            obj_id: Object ID

        Returns:
            True if deleted, False otherwise
        """
        db_obj = await self.get(obj_id)
        if not db_obj:
            return False

        await self.session.delete(db_obj)
        await self.session.commit()
        return True

    async def exists(self, obj_id: str) -> bool:
        """Check if object exists.

        Args:
            obj_id: Object ID

        Returns:
            True if exists, False otherwise
        """
        obj = await self.get(obj_id)
        return obj is not None
