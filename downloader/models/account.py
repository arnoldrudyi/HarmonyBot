from sqlalchemy import Column, func
from sqlalchemy.types import Integer, Boolean, String, DateTime, BigInteger

from downloader.database.connect import Base


class Account(Base):
    __tablename__ = "accounts"

    id = Column(Integer, primary_key=True, autoincrement=True, unique=True, nullable=False)
    chatid = Column(BigInteger, unique=True, nullable=False)
    username = Column(String(100), unique=True, nullable=False)
    is_admin = Column(Boolean, default=False)
    language = Column(String(2), nullable=False)
    created_at = Column(DateTime, server_default=func.now())
