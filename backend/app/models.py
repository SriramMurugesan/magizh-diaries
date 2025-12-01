from sqlalchemy import Column, String, Integer, Text, Date, ForeignKey, CheckConstraint, UniqueConstraint
from sqlalchemy.dialects.postgresql import UUID
from sqlalchemy.sql import func
from sqlalchemy.orm import relationship
from datetime import datetime
import uuid

from app.database import Base


class Student(Base):
    __tablename__ = "students"

    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    name = Column(Text, nullable=False)
    class_name = Column(Text, nullable=False)
    section = Column(Text, nullable=False)
    roll_no = Column(Integer, nullable=True)
    created_at = Column(Date, server_default=func.now())

    # Relationships
    diary_entries = relationship("DiaryEntry", back_populates="student", cascade="all, delete-orphan")
    marks = relationship("Mark", back_populates="student", cascade="all, delete-orphan")


class DiaryEntry(Base):
    __tablename__ = "diary_entries"

    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    student_id = Column(UUID(as_uuid=True), ForeignKey("students.id", ondelete="CASCADE"), nullable=False)
    entry_date = Column(Date, nullable=False)
    homework = Column(Text, nullable=True)
    classwork = Column(Text, nullable=True)
    remarks = Column(Text, nullable=True)
    attendance = Column(Text, nullable=True)
    share_key = Column(Text, unique=True, nullable=False)
    created_at = Column(Date, server_default=func.now())

    # Constraints
    __table_args__ = (
        UniqueConstraint('student_id', 'entry_date', name='uq_student_entry_date'),
        CheckConstraint("attendance IN ('Present', 'Absent')", name='check_attendance'),
    )

    # Relationships
    student = relationship("Student", back_populates="diary_entries")


class Mark(Base):
    __tablename__ = "marks"

    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    student_id = Column(UUID(as_uuid=True), ForeignKey("students.id", ondelete="CASCADE"), nullable=False)
    test_date = Column(Date, nullable=False)
    subject = Column(Text, nullable=False)
    mark = Column(Integer, nullable=False)
    max_mark = Column(Integer, nullable=False)
    remarks = Column(Text, nullable=True)
    share_key = Column(Text, unique=True, nullable=False)
    created_at = Column(Date, server_default=func.now())

    # Relationships
    student = relationship("Student", back_populates="marks")
