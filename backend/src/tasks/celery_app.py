"""
Celery handles two things here:
1. Background tasks  — fire-and-forget (e.g. send welcome message immediately after booking)
2. Scheduled tasks   — run at a specific time (e.g. checkin reminder at 10am the day before)

Celery Beat is the scheduler process that triggers tasks on schedule.
The worker process actually executes them.
"""

from app.core.config import settings
from celery import Celery

celery_app = Celery(
    "hms",
    broker=settings.redis_url,
    backend=settings.redis_url,
    include=["app.tasks.messaging_tasks"],
)

celery_app.conf.update(
    task_serializer="json",
    result_serializer="json",
    accept_content=["json"],
    timezone="Asia/Ho_Chi_Minh",  # Change to your timezone
    enable_utc=True,
)
