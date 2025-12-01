from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from typing import List
from uuid import UUID

from app.database import get_db
from app.models import Student, DiaryEntry, Mark
from app.schemas import (
    StudentCreate, StudentResponse,
    DiaryEntryCreate, DiaryEntryResponse,
    MarkCreate, MarkResponse
)
from app.utils import generate_share_key

router = APIRouter(prefix="/admin", tags=["Admin"])


# ==================== STUDENT ROUTES ====================
@router.post("/students", response_model=StudentResponse, status_code=status.HTTP_201_CREATED)
def create_student(student: StudentCreate, db: Session = Depends(get_db)):
    """Create a new student"""
    db_student = Student(**student.model_dump())
    db.add(db_student)
    db.commit()
    db.refresh(db_student)
    return db_student


@router.get("/students", response_model=List[StudentResponse])
def list_students(skip: int = 0, limit: int = 100, db: Session = Depends(get_db)):
    """List all students"""
    students = db.query(Student).offset(skip).limit(limit).all()
    return students


@router.get("/students/{student_id}", response_model=StudentResponse)
def get_student(student_id: UUID, db: Session = Depends(get_db)):
    """Get a specific student"""
    student = db.query(Student).filter(Student.id == student_id).first()
    if not student:
        raise HTTPException(status_code=404, detail="Student not found")
    return student


@router.put("/students/{student_id}", response_model=StudentResponse)
def update_student(student_id: UUID, student_update: StudentCreate, db: Session = Depends(get_db)):
    """Update a student"""
    student = db.query(Student).filter(Student.id == student_id).first()
    if not student:
        raise HTTPException(status_code=404, detail="Student not found")
    
    for key, value in student_update.model_dump().items():
        setattr(student, key, value)
    
    db.commit()
    db.refresh(student)
    return student


@router.delete("/students/{student_id}", status_code=status.HTTP_204_NO_CONTENT)
def delete_student(student_id: UUID, db: Session = Depends(get_db)):
    """Delete a student (cascades to diary entries and marks)"""
    student = db.query(Student).filter(Student.id == student_id).first()
    if not student:
        raise HTTPException(status_code=404, detail="Student not found")
    
    db.delete(student)
    db.commit()
    return None


# ==================== DIARY ENTRY ROUTES ====================
@router.post("/diary-entries", response_model=DiaryEntryResponse, status_code=status.HTTP_201_CREATED)
def create_diary_entry(entry: DiaryEntryCreate, db: Session = Depends(get_db)):
    """Create a new diary entry"""
    # Check if student exists
    student = db.query(Student).filter(Student.id == entry.student_id).first()
    if not student:
        raise HTTPException(status_code=404, detail="Student not found")
    
    # Generate unique share key
    share_key = generate_share_key()
    
    db_entry = DiaryEntry(**entry.model_dump(), share_key=share_key)
    db.add(db_entry)
    db.commit()
    db.refresh(db_entry)
    return db_entry


@router.get("/diary-entries", response_model=List[DiaryEntryResponse])
def list_diary_entries(
    student_id: UUID = None,
    skip: int = 0,
    limit: int = 100,
    db: Session = Depends(get_db)
):
    """List diary entries, optionally filtered by student"""
    query = db.query(DiaryEntry)
    if student_id:
        query = query.filter(DiaryEntry.student_id == student_id)
    entries = query.offset(skip).limit(limit).all()
    return entries


@router.get("/diary-entries/{entry_id}", response_model=DiaryEntryResponse)
def get_diary_entry(entry_id: UUID, db: Session = Depends(get_db)):
    """Get a specific diary entry"""
    entry = db.query(DiaryEntry).filter(DiaryEntry.id == entry_id).first()
    if not entry:
        raise HTTPException(status_code=404, detail="Diary entry not found")
    return entry


@router.put("/diary-entries/{entry_id}", response_model=DiaryEntryResponse)
def update_diary_entry(entry_id: UUID, entry_update: DiaryEntryCreate, db: Session = Depends(get_db)):
    """Update a diary entry"""
    entry = db.query(DiaryEntry).filter(DiaryEntry.id == entry_id).first()
    if not entry:
        raise HTTPException(status_code=404, detail="Diary entry not found")
    
    for key, value in entry_update.model_dump(exclude={'student_id'}).items():
        setattr(entry, key, value)
    
    db.commit()
    db.refresh(entry)
    return entry


@router.delete("/diary-entries/{entry_id}", status_code=status.HTTP_204_NO_CONTENT)
def delete_diary_entry(entry_id: UUID, db: Session = Depends(get_db)):
    """Delete a diary entry"""
    entry = db.query(DiaryEntry).filter(DiaryEntry.id == entry_id).first()
    if not entry:
        raise HTTPException(status_code=404, detail="Diary entry not found")
    
    db.delete(entry)
    db.commit()
    return None


# ==================== MARKS ROUTES ====================
@router.post("/marks", response_model=MarkResponse, status_code=status.HTTP_201_CREATED)
def create_mark(mark: MarkCreate, db: Session = Depends(get_db)):
    """Create a new mark entry"""
    # Check if student exists
    student = db.query(Student).filter(Student.id == mark.student_id).first()
    if not student:
        raise HTTPException(status_code=404, detail="Student not found")
    
    # Generate unique share key
    share_key = generate_share_key()
    
    db_mark = Mark(**mark.model_dump(), share_key=share_key)
    db.add(db_mark)
    db.commit()
    db.refresh(db_mark)
    return db_mark


@router.get("/marks", response_model=List[MarkResponse])
def list_marks(
    student_id: UUID = None,
    skip: int = 0,
    limit: int = 100,
    db: Session = Depends(get_db)
):
    """List marks, optionally filtered by student"""
    query = db.query(Mark)
    if student_id:
        query = query.filter(Mark.student_id == student_id)
    marks = query.offset(skip).limit(limit).all()
    return marks


@router.get("/marks/{mark_id}", response_model=MarkResponse)
def get_mark(mark_id: UUID, db: Session = Depends(get_db)):
    """Get a specific mark entry"""
    mark = db.query(Mark).filter(Mark.id == mark_id).first()
    if not mark:
        raise HTTPException(status_code=404, detail="Mark not found")
    return mark


@router.put("/marks/{mark_id}", response_model=MarkResponse)
def update_mark(mark_id: UUID, mark_update: MarkCreate, db: Session = Depends(get_db)):
    """Update a mark entry"""
    mark = db.query(Mark).filter(Mark.id == mark_id).first()
    if not mark:
        raise HTTPException(status_code=404, detail="Mark not found")
    
    for key, value in mark_update.model_dump(exclude={'student_id'}).items():
        setattr(mark, key, value)
    
    db.commit()
    db.refresh(mark)
    return mark


@router.delete("/marks/{mark_id}", status_code=status.HTTP_204_NO_CONTENT)
def delete_mark(mark_id: UUID, db: Session = Depends(get_db)):
    """Delete a mark entry"""
    mark = db.query(Mark).filter(Mark.id == mark_id).first()
    if not mark:
        raise HTTPException(status_code=404, detail="Mark not found")
    
    db.delete(mark)
    db.commit()
    return None
