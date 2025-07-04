import datetime

from pydantic import BaseModel


class MovieEvent(BaseModel):
    movie_id: int | None = None
    title: str | None = None
    action: str | None = None
    user_id: int | None = None
    rating: float | None = None
    genres: list | None = None
    description: str | None = None


class UserEvent(BaseModel):
    user_id: int | None = None
    username: str | None = None
    email: str | None = None
    action: str | None = None
    timestamp: datetime.datetime | None = None


class PaymentEvent(BaseModel):
    payment_id: int | None = None
    user_id: int | None = None
    amount: float | None = None
    status: str | None = None
    timestamp: datetime.datetime | None = None
    method_type: str | None = None


class Event(BaseModel):
    id: str | None = None
    type: str | None = None
    timestamp: datetime.datetime | None = None
    payload: dict | None = None


class EventResponse(BaseModel):
    status: str | None = None
    partition: int | None = None
    offset: int | None = None
    event: Event | None = None
