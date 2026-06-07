"""
Messaging service architecture.

Using an abstract base class here is intentional:
- ZaloMessagingService implements the interface for Zalo
- Later you can add SMSMessagingService, EmailMessagingService, etc.
- The rest of the system only talks to the base class, so adding a new
  channel never requires changing booking logic.

This pattern is called "Dependency Inversion" — high-level code (booking)
does not depend on low-level code (Zalo API details).
"""

from abc import ABC, abstractmethod


class BaseMessagingService(ABC):
    """Abstract interface all messaging channels must implement."""

    @abstractmethod
    async def send_welcome(self, guest_id: str, booking_id: str) -> bool:
        """Send welcome message after booking is confirmed."""
        ...

    @abstractmethod
    async def send_checkin_reminder(self, guest_id: str, booking_id: str) -> bool:
        """Send check-in instructions, sent ~24h before arrival."""
        ...

    @abstractmethod
    async def send_checkout_reminder(self, guest_id: str, booking_id: str) -> bool:
        """Send checkout reminder, sent morning of checkout day."""
        ...

    @abstractmethod
    async def send_custom(self, guest_id: str, message: str) -> bool:
        """Send a one-off custom message from staff."""
        ...
