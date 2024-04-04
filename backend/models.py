from sqlalchemy import (
    Column,
    Integer,
    DateTime
)

from database import Base


class Robot(Base):
    __tablename__ = "robot"

    id = Column(Integer, primary_key=True)
    start_with = Column(Integer)
    created_at = Column(DateTime)
    stope_at = Column(DateTime)