from sqlalchemy import Column, Integer, String, DateTime, Text, ForeignKey
from sqlalchemy.sql import func
from sqlalchemy.orm import relationship
from app.database import Base

class Trip(Base):
    __tablename__ = "trips"

    id = Column(Integer, primary_key=True, index=True)
    title = Column(String(255), nullable=False)
    description = Column(Text, nullable=True)
    destination = Column(String(255), nullable=True)
    prompt = Column(Text, nullable=True)
    style = Column(String(100), nullable=True)
    generated_video_url = Column(String(500), nullable=True)
    status = Column(String(50), default="draft")  # draft, processing, completed, failed
    owner_id = Column(Integer, ForeignKey("users.id"))
    created_at = Column(DateTime(timezone=True), server_default=func.now())
    updated_at = Column(DateTime(timezone=True), onupdate=func.now())
    
    # Relationships
    owner = relationship("User", back_populates="trips")
    media_files = relationship("MediaFile", back_populates="trip")