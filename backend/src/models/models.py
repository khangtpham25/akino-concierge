"""
Database models — these map directly to PostgreSQL tables.
Alembic reads these to generate migration files automatically.
"""

import uuid
from datetime import date, datetime

from app.core.database import Base
from sqlalchemy import UUID, Boolean, DateTime, Float, ForeignKey, Integer, String, Text
from sqlalchemy.orm import Mapped, mapped_column, relationship
from sqlalchemy.sql import func


class Property(Base):
    """A hotel or property managed by the system."""

    __tablename__ = "properties"

    id: Mapped[uuid.UUID] = mapped_column(UUID, primary_key=True, default=uuid.uuid4)
    name: Mapped[str] = mapped_column(String(200))
    address: Mapped[str] = mapped_column(Text)
    phone: Mapped[str] = mapped_column(String(50))
    zalo_oa_id: Mapped[str | None] = mapped_column(
        String(100)
    )  # Each property may have its own Zalo OA

    rooms: Mapped[list["Room"]] = relationship(back_populates="property")
    created_at: Mapped[datetime] = mapped_column(DateTime, server_default=func.now())


class Room(Base):
    """A single room within a property."""

    __tablename__ = "rooms"

    id: Mapped[uuid.UUID] = mapped_column(UUID, primary_key=True, default=uuid.uuid4)
    property_id: Mapped[uuid.UUID] = mapped_column(ForeignKey("properties.id"))
    room_number: Mapped[str] = mapped_column(String(20))
    room_type: Mapped[str] = mapped_column(String(100))  # e.g. "Deluxe", "Suite"
    floor: Mapped[int | None] = mapped_column(Integer)
    base_price: Mapped[float] = mapped_column(Float)
    is_active: Mapped[bool] = mapped_column(Boolean, default=True)

    property: Mapped["Property"] = relationship(back_populates="rooms")
    bookings: Mapped[list["Booking"]] = relationship(back_populates="room")


class Guest(Base):
    """A guest profile — reused across multiple bookings."""

    __tablename__ = "guests"

    id: Mapped[uuid.UUID] = mapped_column(UUID, primary_key=True, default=uuid.uuid4)
    full_name: Mapped[str] = mapped_column(String(200))
    phone: Mapped[str] = mapped_column(String(50))
    email: Mapped[str | None] = mapped_column(String(200))
    zalo_user_id: Mapped[str | None] = mapped_column(
        String(100)
    )  # Linked when guest follows OA

    bookings: Mapped[list["Booking"]] = relationship(back_populates="guest")
    created_at: Mapped[datetime] = mapped_column(DateTime, server_default=func.now())


class Booking(Base):
    """A reservation linking a guest to a room."""

    __tablename__ = "bookings"

    id: Mapped[uuid.UUID] = mapped_column(UUID, primary_key=True, default=uuid.uuid4)
    room_id: Mapped[uuid.UUID] = mapped_column(ForeignKey("rooms.id"))
    guest_id: Mapped[uuid.UUID] = mapped_column(ForeignKey("guests.id"))

    check_in_date: Mapped[date]
    check_out_date: Mapped[date]
    status: Mapped[str] = mapped_column(String(50), default="confirmed")
    # Status flow: confirmed → checked_in → checked_out → cancelled

    source: Mapped[str] = mapped_column(String(50), default="direct")
    # Source: "direct", "booking_com", "agoda" — important for future OTA integration

    total_price: Mapped[float] = mapped_column(Float)
    notes: Mapped[str | None] = mapped_column(Text)

    room: Mapped["Room"] = relationship(back_populates="bookings")
    guest: Mapped["Guest"] = relationship(back_populates="bookings")
    messages: Mapped[list["MessageLog"]] = relationship(back_populates="booking")
    created_at: Mapped[datetime] = mapped_column(DateTime, server_default=func.now())


class MessageLog(Base):
    """
    Every automated message sent is logged here.
    Useful for debugging and avoiding duplicate sends.
    """

    __tablename__ = "message_logs"

    id: Mapped[uuid.UUID] = mapped_column(UUID, primary_key=True, default=uuid.uuid4)
    booking_id: Mapped[uuid.UUID] = mapped_column(ForeignKey("bookings.id"))
    channel: Mapped[str] = mapped_column(String(50))  # "zalo", "sms", "email"
    message_type: Mapped[str] = mapped_column(
        String(100)
    )  # "welcome", "checkin_reminder", etc.
    status: Mapped[str] = mapped_column(String(50))  # "sent", "failed", "pending"
    sent_at: Mapped[datetime | None] = mapped_column(DateTime)
    error: Mapped[str | None] = mapped_column(Text)  # Store error details if failed

    booking: Mapped["Booking"] = relationship(back_populates="messages")
