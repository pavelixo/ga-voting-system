from sqlalchemy import Column, Integer, Boolean
from db.database import Base


class Candidate(Base):
  __tablename__ = 'candidates'

  user_id = Column(Integer, primary_key=True, index=True)
  votes = Column(Integer, nullable=False, default=0)
  is_active = Column(Boolean, default=True)
