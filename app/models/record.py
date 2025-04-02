from sqlalchemy import Column, Integer, String, JSON, BigInteger
from sqlalchemy.ext.declarative import declarative_base

from app.db.session import Base

class Record(Base):
    __tablename__ = "records"

    id = Column(Integer, primary_key=True, index=True)
    things_stored = Column(JSON, nullable=False)
    timestamp = Column(BigInteger, nullable=False)
