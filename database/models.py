from sqlalchemy import Column, Integer, String, ForeignKey, Numeric
from sqlalchemy.orm import DeclarativeBase, relationship, sessionmaker


class Base(DeclarativeBase):
    pass


class User(Base):
    __tablename__ = "users"
    id = Column(Integer(), primary_key=True, nullable=False)
    vk_id = Column(Integer(), unique=True, nullable=False)
    city = Column(String(), unique=True, nullable=False)
