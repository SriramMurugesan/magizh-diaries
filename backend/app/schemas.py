from pydantic import BaseModel, Field
from datetime import date
from uuid import UUID
from typing import Optional


# Student Schemas
class StudentBase(BaseModel):
    name: str
    class_name: str
    section: str
    roll_no: Optional[int] = None


class StudentCreate(StudentBase):
    pass


class StudentResponse(StudentBase):
    id: UUID
    created_at: date

    class Config:
        from_attributes = True


# Diary Entry Schemas
class DiaryEntryBase(BaseModel):
    entry_date: date
    homework: Optional[str] = None
    classwork: Optional[str] = None
    remarks: Optional[str] = None
    attendance: Optional[str] = Field(None, pattern="^(Present|Absent)$")


class DiaryEntryCreate(DiaryEntryBase):
    student_id: UUID


class DiaryEntryResponse(DiaryEntryBase):
    id: UUID
    student_id: UUID
    share_key: str
    created_at: date

    class Config:
        from_attributes = True


class DiaryEntryPublic(DiaryEntryBase):
    """Public view for parents - no student_id exposed"""
    student_name: str
    class_name: str
    section: str

    class Config:
        from_attributes = True


# Mark Schemas
class MarkBase(BaseModel):
    test_date: date
    subject: str
    mark: int
    max_mark: int
    remarks: Optional[str] = None


class MarkCreate(MarkBase):
    student_id: UUID


class MarkResponse(MarkBase):
    id: UUID
    student_id: UUID
    share_key: str
    created_at: date

    class Config:
        from_attributes = True


class MarkPublic(MarkBase):
    """Public view for parents - no student_id exposed"""
    student_name: str
    class_name: str
    section: str

    class Config:
        from_attributes = True
