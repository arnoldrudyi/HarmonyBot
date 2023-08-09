from sqlalchemy import Column, func
from sqlalchemy.types import Integer, String, DateTime

from downloader.database.connect import Base


class Audio(Base):
    __tablename__ = 'audios'

    id = Column(Integer, primary_key=True, unique=True, autoincrement=True, nullable=False)
    url = Column(String(512), unique=True, nullable=False)
    unique_id = Column(String(1024), unique=True, nullable=False)
    created_at = Column(DateTime, server_default=func.now(), nullable=False)
