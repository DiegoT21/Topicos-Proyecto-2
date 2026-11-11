import re
from datetime import datetime
from zoneinfo import ZoneInfo

from pydantic import BaseModel, ConfigDict, Field, field_validator

from .config import settings

_HTML = re.compile(r"[<>]")


class StudentCreate(BaseModel):
    name: str = Field(min_length=2, max_length=100)
    email: str = Field(max_length=120, pattern=r"^[^@\s<>]+@[^@\s<>]+\.[^@\s<>]+$")

    @field_validator("name")
    @classmethod
    def no_html(cls, v: str) -> str:  # RN-11, CA-10
        v = v.strip()
        if _HTML.search(v):
            raise ValueError("El nombre no puede contener HTML")
        return v


class StudentOut(BaseModel):
    model_config = ConfigDict(from_attributes=True)
    id: int
    name: str
    email: str
    token: str


class BookingCreate(BaseModel):
    tutor_id: int
    subject_id: int
    start_at: datetime

    @field_validator("start_at")
    @classmethod
    def to_business_local(cls, v: datetime) -> datetime:
        """Si llega con zona horaria, se convierte a la hora del negocio (naive), RNF-03."""
        if v.tzinfo is not None:
            return v.astimezone(ZoneInfo(settings.business_timezone)).replace(tzinfo=None)
        return v


class BookingOut(BaseModel):
    model_config = ConfigDict(from_attributes=True)
    id: int
    tutor_id: int
    student_id: int
    subject_id: int
    start_at: datetime
    end_at: datetime
    status: str
