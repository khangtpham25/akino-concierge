"""
Messaging tasks run by Celery workers.

When a booking is created, the API schedules these tasks with eta (execute at)
so they fire at the right time automatically.

Example flow for a new booking:
  1. POST /bookings → booking created
  2. API calls: send_welcome_message.delay(booking_id)         → fires immediately
  3. API calls: send_checkin_reminder.apply_async(             → fires day before check-in
         args=[booking_id], eta=checkin_date - timedelta(days=1)
     )
  4. API calls: send_checkout_reminder.apply_async(            → fires morning of checkout
         args=[booking_id], eta=checkout_date at 09:00
     )
"""

import asyncio

from app.tasks.celery_app import celery_app


@celery_app.task(bind=True, max_retries=3)  # type: ignore[misc]
def send_welcome_message(self, booking_id: str) -> None:  # type: ignore[misc]
    """Send welcome message immediately after booking is confirmed."""
    try:
        # Import here to avoid circular imports
        import uuid
        from datetime import datetime

        from app.core.database import AsyncSessionLocal
        from app.models.models import Booking, MessageLog
        from app.services.messaging.zalo import ZaloMessagingService

        async def _run() -> None:
            async with AsyncSessionLocal() as db:
                booking = await db.get(Booking, uuid.UUID(booking_id))
                if not booking or not booking.guest.zalo_user_id:
                    return

                service = ZaloMessagingService()
                success = await service.send_welcome(
                    booking.guest.zalo_user_id, booking_id
                )

                # Log the result
                log = MessageLog(
                    booking_id=booking.id,
                    channel="zalo",
                    message_type="welcome",
                    status="sent" if success else "failed",
                    sent_at=datetime.utcnow(),
                )
                db.add(log)

        asyncio.run(_run())

    except Exception as exc:
        # Retry up to 3 times with exponential backoff
        raise self.retry(exc=exc, countdown=60 * (self.request.retries + 1)) from exc


@celery_app.task(bind=True, max_retries=3)  # type: ignore[misc]
def send_checkin_reminder(self, booking_id: str) -> None:  # type: ignore[misc]
    """Send check-in reminder — scheduled for the day before arrival."""
    # Same pattern as above — omitted for brevity
    pass


@celery_app.task(bind=True, max_retries=3)  # type: ignore[misc]
def send_checkout_reminder(self, booking_id: str) -> None:  # type: ignore[misc]
    """Send checkout reminder — scheduled for morning of checkout day."""
    pass
