from sqlalchemy import Column, Integer, String, DateTime, ForeignKey
from sqlalchemy.sql import func
from .database import Base

class URL(Base):
    __tablename__ = "urls"
    id = Column(Integer, primary_key=True, index=True)
    original_url = Column(String, nullable=False)
    short_id = Column(String, unique=True, index=True, nullable=False)
    clicks = Column(Integer, default=0)

class Click(Base):
    __tablename__ = "clicks"
    id = Column(Integer, primary_key=True, index=True)
    url_id = Column(Integer, ForeignKey("urls.id"))
    timestamp = Column(DateTime(timezone=True), server_default=func.now())
    ip = Column(String)
    user_agent = Column(String)
