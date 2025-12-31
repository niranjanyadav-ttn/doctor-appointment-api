"""
Availability model for doctor working hours.
"""

from sqlalchemy import Column, Integer, ForeignKey, DateTime
from sqlalchemy.orm import relationship
from app.database import Base


class Availability(Base):
    __tablename__ = "availabilities"
    
    id = Column(Integer, primary_key=True, index=True, autoincrement=True)
    doctor_id = Column(
        Integer,
        ForeignKey("users.id", ondelete="CASCADE"),
        nullable=False,
        index=True
    )
    start_time = Column(DateTime, nullable=False, index=True)
    end_time = Column(DateTime, nullable=False, index=True)
    
    # Relationships
    doctor = relationship("User", back_populates="availabilities")
    
    def __repr__(self) -> str:
        return f"<Availability(id={self.id}, doctor_id={self.doctor_id})>"
