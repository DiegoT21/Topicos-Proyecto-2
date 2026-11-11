"""Modelos de datos (spec: specs/data-model.md).

Las fechas son datetime naive en la hora del negocio (America/Panama), un solo criterio (RNF-03).
"""
import secrets
from datetime import datetime

from sqlalchemy import Boolean, CheckConstraint, Column, DateTime, ForeignKey, Index, Integer, String, Table
from sqlalchemy.orm import Mapped, mapped_column, relationship

from .config import local_now
from .database import Base
from .rules import STATUS_CANCELLED, STATUS_CONFIRMED, STATUS_DONE

VALID_STATUSES = (STATUS_CONFIRMED, STATUS_CANCELLED, STATUS_DONE)

tutor_subjects = Table(
    "tutor_subjects",
    Base.metadata,
    Column("tutor_id", ForeignKey("tutors.id"), primary_key=True),
    Column("subject_id", ForeignKey("subjects.id"), primary_key=True),
)


class Subject(Base):
    __tablename__ = "subjects"
    id: Mapped[int] = mapped_column(primary_key=True)
    name: Mapped[str] = mapped_column(String(100), unique=True)
    active: Mapped[bool] = mapped_column(Boolean, default=True)


class Tutor(Base):
    __tablename__ = "tutors"
    id: Mapped[int] = mapped_column(primary_key=True)
    name: Mapped[str] = mapped_column(String(100))
    email: Mapped[str] = mapped_column(String(120), unique=True)
    active: Mapped[bool] = mapped_column(Boolean, default=True)
    subjects: Mapped[list[Subject]] = relationship(secondary=tutor_subjects)


class Student(Base):
    __tablename__ = "students"
    id: Mapped[int] = mapped_column(primary_key=True)
    name: Mapped[str] = mapped_column(String(100))
    email: Mapped[str] = mapped_column(String(120), unique=True)
    token: Mapped[str] = mapped_column(String(64), unique=True, default=lambda: secrets.token_urlsafe(24))


class Availability(Base):
    """Bloque publicado por el tutor (RN-03)."""

    __tablename__ = "availabilities"
    __table_args__ = (CheckConstraint("end_at > start_at", name="ck_availability_interval"),)
    id: Mapped[int] = mapped_column(primary_key=True)
    tutor_id: Mapped[int] = mapped_column(ForeignKey("tutors.id"))
    start_at: Mapped[datetime] = mapped_column(DateTime)
    end_at: Mapped[datetime] = mapped_column(DateTime)


class Booking(Base):
    __tablename__ = "bookings"
    __table_args__ = (
        CheckConstraint("end_at > start_at", name="ck_booking_interval"),
        CheckConstraint("status IN ('confirmada','cancelada','realizada')", name="ck_booking_status"),
        Index("ix_booking_tutor_start", "tutor_id", "start_at"),
        Index("ix_booking_student_start", "student_id", "start_at"),
    )
    id: Mapped[int] = mapped_column(primary_key=True)
    tutor_id: Mapped[int] = mapped_column(ForeignKey("tutors.id"))
    student_id: Mapped[int] = mapped_column(ForeignKey("students.id"))
    subject_id: Mapped[int] = mapped_column(ForeignKey("subjects.id"))
    start_at: Mapped[datetime] = mapped_column(DateTime)
    end_at: Mapped[datetime] = mapped_column(DateTime)
    status: Mapped[str] = mapped_column(String(12), default=STATUS_CONFIRMED)
    created_at: Mapped[datetime] = mapped_column(DateTime, default=local_now)
