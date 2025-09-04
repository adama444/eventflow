from datetime import date, timedelta

from faker import Faker
from pydantic import BaseModel, EmailStr, Field, HttpUrl

faker = Faker()


class Event(BaseModel):
    name: str | None = None
    type: str | None = None
    start_date: date | None = None
    end_date: date | None = None
    start_time: str | None = None
    description: str | None = None
    pricing: str | None = None
    location: str | None = Field(
        ..., description="can be city name or full location address"
    )
    location_gps_link: HttpUrl | None = None
    country: str | None = None
    media_links: list[HttpUrl] = []
    organizer_email: EmailStr | None = None
    organizer_phone: str | None = None
    ticket_link: HttpUrl | None = None


def generate_sample_event() -> Event:
    """Generate a realistic sample JSON from your Event model using the faker library"""
    start_date = faker.date_this_year()
    end_date = start_date + timedelta(days=faker.random_int(min=0, max=2))

    return Event(
        name=faker.catch_phrase(),
        type=faker.random_element(
            elements=("Conference", "Concert", "Workshop", "Webinar")
        ),
        start_date=start_date,
        end_date=end_date,
        start_time=faker.time(),
        description=faker.text(max_nb_chars=200),
        pricing=faker.random_element(elements=("Free", "$10", "$20", "$50")),
        location=faker.address(),
        location_gps_link=HttpUrl(
            f"https://maps.google.com/?q={faker.latitude()},{faker.longitude()}"
        ),
        country=faker.country(),
        media_links=[HttpUrl(f"https://example.com/{faker.word()}.jpg")],
        organizer_email=faker.email(),
        organizer_phone=faker.phone_number(),
        ticket_link=HttpUrl(f"https://tickets.example.com/{faker.word()}"),
    )
