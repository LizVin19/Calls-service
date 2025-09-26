from fastapi import FastAPI
from sqlalchemy import Column, Integer, String, DateTime, Enum, func, ForeignKey, JSON, UniqueConstraint
from sqlalchemy.orm import declarative_base, relationship
import enum

Base = declarative_base()


class CallStatus(str, enum.Enum):
    created = 'created'
    processing = 'processing'
    ready = 'ready'


class Call(Base):
    __tablename__ = 'calls'

    id = Column(Integer, primary_key=True)
    caller = Column(String(20), nullable=False, index=True)
    receiver = Column(String(20), nullable=False, index=True)
    started_at = Column(DateTime(timezone=True), nullable=False, index=True)
    status = Column(Enum(CallStatus), nullable=False, default=CallStatus.created)
    created_at = Column(DateTime(timezone=True), server_default=func.now())
    updated_at = Column(DateTime(timezone=True), server_default=func.now(), onupdate=func.now())

    recording = relationship('Recording', back_populates='call', uselist=False, lazy='selectin')

class Recording(Base):
    __tablename__ = 'recordings'

    id = Column(Integer, primary_key=True)
    call_id = Column(Integer, ForeignKey('calls.id'), nullable=False, unique=True, index=True)
    filename = Column(String, nullable=False)
    duration_sec = Column(Integer)  #
    transcription = Column(String)  #
    silence_ranges = Column(JSON)  #
    created_at = Column(DateTime(timezone=True), server_default=func.now())

    call = relationship('Call', back_populates='recording')

