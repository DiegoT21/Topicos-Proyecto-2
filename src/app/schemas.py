import re
from datetime import datetime
from zoneinfo import ZoneInfo

from pydantic import BaseModel, ConfigDict, Field, field_validator

from .config import settings

_HTML = re.compile(r"[<>]")


def institutional_email(v: str) -> str:
    """RN-11 / D-01 (B-01): solo correos del dominio institucional. Se guarda en minúsculas."""
    v = v.strip().lower()
    if not v.endswith("@" + settings.institutional_domain):
        raise ValueError(f"Solo se aceptan correos @{settings.institutional_domain}")
    return v


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

    @field_validator("email", mode="before")
    @classmethod
    def normalize(cls, v):
        return v.strip().lower() if isinstance(v, str) else v

    @field_validator("email")
    @classmethod
    def domain(cls, v: str) -> str:
        return institutional_email(v)


class StudentOut(BaseModel):
    model_config = ConfigDict(from_attributes=True)
    id: int
    name: str
    email: str
    token: str


def _clean_name(v: str) -> str:
    v = v.strip()
    if _HTML.search(v):
        raise ValueError("El nombre no puede contener HTML")
    return v


_EMAIL = r"^[^@\s<>]+@[^@\s<>]+\.[^@\s<>]+$"


class SubjectCreate(BaseModel):
    name: str = Field(min_length=2, max_length=100)

    @field_validator("name")
    @classmethod
    def clean(cls, v: str) -> str:
        return _clean_name(v)


class SubjectOut(BaseModel):
    model_config = ConfigDict(from_attributes=True)
    id: int
    name: str


class TutorCreate(BaseModel):
    name: str = Field(min_length=2, max_length=100)
    email: str = Field(max_length=120, pattern=_EMAIL)
    subject_ids: list[int] = Field(default_factory=list)

    @field_validator("name")
    @classmethod
    def clean(cls, v: str) -> str:
        return _clean_name(v)

    @field_validator("email", mode="before")
    @classmethod
    def normalize(cls, v):
        return v.strip().lower() if isinstance(v, str) else v

    @field_validator("email")
    @classmethod
    def domain(cls, v: str) -> str:
        return institutional_email(v)


class TutorPublic(BaseModel):
    """Lo que ve cualquier estudiante: sin correo ni token."""

    model_config = ConfigDict(from_attributes=True)
    id: int
    name: str
    subjects: list[SubjectOut]


class TutorCreatedOut(TutorPublic):
    email: str
    token: str


class AvailabilityCreate(BaseModel):
    start_at: datetime
    end_at: datetime

    @field_validator("start_at", "end_at")
    @classmethod
    def to_local(cls, v: datetime) -> datetime:
        if v.tzinfo is not None:
            return v.astimezone(ZoneInfo(settings.business_timezone)).replace(tzinfo=None)
        return v


class AvailabilityOut(BaseModel):
    model_config = ConfigDict(from_attributes=True)
    id: int
    tutor_id: int
    start_at: datetime
    end_at: datetime


class SubjectSlot(BaseModel):
    tutor_id: int
    tutor_name: str
    start_at: datetime


class SubjectSlotsOut(BaseModel):
    """B-10: espacios libres de todos los tutores de una materia en un día, ordenados por hora."""

    subject_id: int
    date: str
    session_minutes: int
    slots: list[SubjectSlot]


class SlotsOut(BaseModel):
    tutor_id: int
    date: str
    session_minutes: int
    slots: list[datetime]


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


class AdminBookingOut(BaseModel):
    """Reserva con nombres, para el listado del admin. Los nombres son texto de usuario: escapar al mostrarlos."""

    id: int
    tutor_id: int
    tutor_name: str
    student_id: int
    student_name: str
    subject_id: int
    subject_name: str
    start_at: datetime
    end_at: datetime
    status: str


class BookingOut(BaseModel):
    model_config = ConfigDict(from_attributes=True)
    id: int
    tutor_id: int
    student_id: int
    subject_id: int
    start_at: datetime
    end_at: datetime
    status: str
