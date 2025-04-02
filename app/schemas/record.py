from pydantic import BaseModel, Field
from typing import Dict, Any, Optional

class RecordBase(BaseModel):
    things_stored: str = Field(..., description="JSON string containing stored things")
    timestamp: int = Field(..., description="Unix timestamp")

class RecordCreate(RecordBase):
    pass

class RecordUpdate(BaseModel):
    things_stored: Optional[str] = Field(None, description="JSON string containing stored things")
    timestamp: Optional[int] = Field(None, description="Unix timestamp")

class RecordInDB(RecordBase):
    id: int

    class Config:
        from_attributes = True
