import os
from typing import List
from typing import Optional
from datetime import datetime
from uuid import UUID
# from email_validate import validate
from macros import MacrosStatus

from sqlalchemy import String, ForeignKey, create_engine
from sqlalchemy.orm import DeclarativeBase, \
    validates, mapped_column, Mapped, relationship, session

par_dir = os.path.dirname(os.path.abspath(__file__))
db_path = os.path.join(par_dir, "db.sqlite3")


# Create the base model class
class Base(DeclarativeBase):
    pass


class User(Base):
    __tablename__ = 'users'

    id: Mapped[int] = mapped_column(primary_key=True)
    email: Mapped[str] = mapped_column(String(255), nullable=False, unique=True)
    uploads: Mapped[List["Upload"]] = relationship(back_populates="user",
                                                   cascade="all, delete-orphan")


class Upload(Base):
    __tablename__ = 'uploads'

    id: Mapped[int] = mapped_column(primary_key=True)

    uid: Mapped[UUID] = mapped_column(nullable=False, unique=True)

    filename: Mapped[str] = mapped_column(nullable=False)

    upload_time: Mapped[datetime] = mapped_column(nullable=False)

    finish_time: Mapped[datetime] = mapped_column(nullable=True)

    status: Mapped[str] = mapped_column(nullable=False, default=MacrosStatus.PENDING.value)

    user_id: Mapped[Optional[int]] = mapped_column(ForeignKey("users.id"))

    user: Mapped["User"] = relationship(back_populates="uploads")


# create the database engine and create the tables
engine = create_engine(f"sqlite:///{db_path}")
Base.metadata.create_all(engine)

