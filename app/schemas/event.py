from datetime import date

from pydantic import BaseModel, EmailStr, HttpUrl


class Event(BaseModel):
    name: str | None = None
    start_date: date | None = None
    end_date: date | None = None
    start_time: str | None = None
    description: str | None = None
    pricing: str | None = None
    location: str | None = None
    location_gps_link: HttpUrl | None = None
    country: str | None = None
    media_links: list[HttpUrl] = []
    organizer_email: EmailStr | None = None
    organizer_phone: str | None = None
    ticket_link: HttpUrl | None = None
