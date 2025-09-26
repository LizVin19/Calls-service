from pydantic import BaseModel, Field
from datetime import datetime
from typing import Optional, List


class RecordingOut(BaseModel):
    filename: str
    duration: Optional[int] = Field(None, alias='duration_sec')
    transcription: Optional[str]
    silence_ranges: Optional[List[List[int]]]

    class Config:
        from_attributes = True
        populate_by_name = True


class CallCreate(BaseModel):
    caller: str
    receiver: str
    started_at: datetime


class CallOut(BaseModel):
    id: int
    caller: str
    receiver: str
    started_at: datetime
    status: str
    recording: Optional[RecordingOut] = None

    class Config:
        from_attributes = True
