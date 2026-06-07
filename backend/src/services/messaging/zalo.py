import httpx
from app.core.config import settings
from app.services.messaging.base import BaseMessagingService

ZALO_API_BASE = "https://openapi.zalo.me/v3.0/oa"


class ZaloMessagingService(BaseMessagingService):
    """
    Sends messages via Zalo Official Account API.

    Docs: https://developers.zalo.me/docs/official-account
    Note: Guest must be following your OA to receive messages.
    """

    def __init__(self) -> None:
        self._client = httpx.AsyncClient(
            headers={"access_token": settings.zalo_access_token},
            timeout=10.0,
        )

    async def _send(self, zalo_user_id: str, text: str) -> bool:
        """Low-level send — all public methods call this."""
        payload = {
            "recipient": {"user_id": zalo_user_id},
            "message": {"text": text},
        }
        response = await self._client.post(f"{ZALO_API_BASE}/message/cs", json=payload)
        return response.status_code == 200

    async def send_welcome(self, zalo_user_id: str, booking_id: str) -> bool:
        message = (
            "Xin chào! Cảm ơn bạn đã đặt phòng.\n"
            f"Mã đặt phòng của bạn: {booking_id}\n"
            "Chúng tôi sẽ liên hệ trước khi nhận phòng. Chúc bạn một kỳ nghỉ vui vẻ! 🏨"
        )
        return await self._send(zalo_user_id, message)

    async def send_checkin_reminder(self, zalo_user_id: str, booking_id: str) -> bool:
        message = (
            "Nhắc nhở nhận phòng!\n"
            "Ngày mai là ngày nhận phòng của bạn.\n"
            "Giờ nhận phòng: 14:00. Vui lòng xuất trình mã đặt phòng tại quầy lễ tân."
        )
        return await self._send(zalo_user_id, message)

    async def send_checkout_reminder(self, zalo_user_id: str, booking_id: str) -> bool:
        message = (
            "Nhắc nhở trả phòng!\n"
            "Hôm nay là ngày trả phòng của bạn.\n"
            "Giờ trả phòng: 12:00. Cảm ơn bạn đã lưu trú cùng chúng tôi! 🙏"
        )
        return await self._send(zalo_user_id, message)

    async def send_custom(self, zalo_user_id: str, message: str) -> bool:
        return await self._send(zalo_user_id, message)
