from sqlalchemy.orm import DeclarativeBase, declared_attr
# from sqlalchemy.ext.asyncio import AsyncAttrs

__all__ = ["Base"]


class Base(DeclarativeBase):

    @declared_attr.directive
    def __tablename__(self):
        return self.__name__.lower()

