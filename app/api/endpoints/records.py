from typing import List, Optional
from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from datetime import datetime

from app.db.session import get_db
from app.models.record import Record
from app.schemas.record import RecordCreate, RecordUpdate, RecordInDB

router = APIRouter()

@router.post("/", response_model=RecordInDB, status_code=status.HTTP_201_CREATED)
def create_record(record: RecordCreate, db: Session = Depends(get_db)):
    """Create a new record."""
    # Convert datetime.now() to Unix timestamp (seconds since epoch)
    current_timestamp = int(datetime.now().timestamp())
    
    db_record = Record(
        things_stored=record.things_stored,
        timestamp=current_timestamp
    )
    db.add(db_record)
    db.commit()
    db.refresh(db_record)
    return db_record

@router.get("/{record_id}", response_model=RecordInDB)
def read_record(record_id: int, db: Session = Depends(get_db)):
    """Get a specific record by ID."""
    db_record = db.query(Record).filter(Record.id == record_id).first()
    if db_record is None:
        raise HTTPException(status_code=404, detail="Record not found")
    return db_record

@router.get("/", response_model=List[RecordInDB])
def read_records(skip: int = 0, limit: int = 100, db: Session = Depends(get_db)):
    """Get a list of records."""
    records = db.query(Record).offset(skip).limit(limit).all()
    return records

@router.put("/{record_id}", response_model=RecordInDB)
def update_record(record_id: int, record: RecordUpdate, db: Session = Depends(get_db)):
    """Update a record."""
    db_record = db.query(Record).filter(Record.id == record_id).first()
    if db_record is None:
        raise HTTPException(status_code=404, detail="Record not found")
    
    update_data = record.model_dump(exclude_unset=True)
    # Ensure timestamp cannot be updated
    if 'timestamp' in update_data:
        del update_data['timestamp']
        
    for key, value in update_data.items():
        setattr(db_record, key, value)
    
    db.commit()
    db.refresh(db_record)
    return db_record

@router.delete("/{record_id}", status_code=status.HTTP_204_NO_CONTENT)
def delete_record(record_id: int, db: Session = Depends(get_db)):
    """Delete a record."""
    db_record = db.query(Record).filter(Record.id == record_id).first()
    if db_record is None:
        raise HTTPException(status_code=404, detail="Record not found")
    
    db.delete(db_record)
    db.commit()
    return None
