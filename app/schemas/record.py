from pydantic import BaseModel, Field
from typing import Dict, Any, Optional

class RecordBase(BaseModel):
    things_stored: str = Field(..., description="JSON string containing stored things")

class RecordCreate(RecordBase):
    pass

class RecordUpdate(BaseModel):
    things_stored: Optional[str] = Field(None, description="JSON string containing stored things")

class RecordInDB(RecordBase):
    id: int
    timestamp: int = Field(..., description="Unix timestamp")

    class Config:
        from_attributes = True
