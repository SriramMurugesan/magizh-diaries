from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session

from app.database import get_db
from app.models import DiaryEntry, Mark
from app.schemas import DiaryEntryPublic, MarkPublic

router = APIRouter(prefix="/share", tags=["Public"])


@router.get("/diary/{share_key}", response_model=DiaryEntryPublic)
def get_diary_by_share_key(share_key: str, db: Session = Depends(get_db)):
    """Public endpoint for parents to view diary entry via share link"""
    entry = db.query(DiaryEntry).filter(DiaryEntry.share_key == share_key).first()
    
    if not entry:
        raise HTTPException(status_code=404, detail="Diary entry not found")
    
    # Build public response with student info
    return DiaryEntryPublic(
        entry_date=entry.entry_date,
        homework=entry.homework,
        classwork=entry.classwork,
        remarks=entry.remarks,
        attendance=entry.attendance,
        student_name=entry.student.name,
        class_name=entry.student.class_name,
        section=entry.student.section
    )


@router.get("/marks/{share_key}", response_model=MarkPublic)
def get_mark_by_share_key(share_key: str, db: Session = Depends(get_db)):
    """Public endpoint for parents to view marks via share link"""
    mark = db.query(Mark).filter(Mark.share_key == share_key).first()
    
    if not mark:
        raise HTTPException(status_code=404, detail="Mark not found")
    
    # Build public response with student info
    return MarkPublic(
        test_date=mark.test_date,
        subject=mark.subject,
        mark=mark.mark,
        max_mark=mark.max_mark,
        remarks=mark.remarks,
        student_name=mark.student.name,
        class_name=mark.student.class_name,
        section=mark.student.section
    )
