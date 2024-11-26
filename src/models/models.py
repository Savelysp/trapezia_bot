from sqlalchemy import (
    BIGINT,
    BOOLEAN,
    DECIMAL,
    TIMESTAMP,
    VARCHAR,
    Column,
    ForeignKey,
)
from sqlalchemy.orm import relationship

from src.models.base import Base

__all__ = [
        "User",
        "Service",
        "Entry",
        "Base",
        ]


class User(Base):
    id = Column(BIGINT, primary_key=True)
    name = Column(VARCHAR(32), nullable=False)
    is_admin = Column(BOOLEAN, default=False)
    phone = Column(VARCHAR(16), nullable=False)
    entries = relationship(argument="Entry", back_populates="user")


class Service(Base):
    id = Column(BIGINT, primary_key=True)
    name = Column(VARCHAR(128), nullable=False)
    title = Column(VARCHAR(256), nullable=False)
    price = Column(DECIMAL(scale=2), nullable=False)
    entries = relationship(argument="Entry", back_populates="service")


class Entry(Base):
    entry_time = Column(TIMESTAMP, primary_key=True)
    user_id = Column(BIGINT, 
                     ForeignKey(column=User.id, ondelete="RESTRICT", onupdate="CASCADE"),
                     nullable=False)
    user = relationship(argument=User, back_populates="entries")

    service_id = Column(BIGINT, 
                        ForeignKey(column=Service.id, ondelete="RESTRICT", onupdate="CASCADE"), 
                        nullable=False)
    service = relationship(argument=Service, back_populates="entries")

