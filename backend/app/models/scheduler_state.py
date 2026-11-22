from datetime import datetime
from sqlalchemy import Column, Integer, String, DateTime, Boolean
from app.database import Base

class SchedulerState(Base):
    __tablename__ = "scheduler_state"

    id = Column(Integer, primary_key=True, default=1)
    last_successful_cutoff = Column(DateTime, nullable=True)
    last_generation_start = Column(DateTime, nullable=True)
    last_generation_end = Column(DateTime, nullable=True)
    last_status = Column(String(50), nullable=True)
    
    current_coverage_start = Column(DateTime, nullable=True)
    current_coverage_end = Column(DateTime, nullable=True)
    
    retry_count = Column(Integer, default=0, nullable=False)
    is_running = Column(Boolean, default=False, nullable=False)
    updated_at = Column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow, nullable=False)
