from uuid import UUID

from fastapi import APIRouter, Depends, Response, status

from auth.users import get_current_user
from services.abc import NotificationSettingsServiceABC
from services.notification_settings import NotificationSettingsService


router = APIRouter()


@router.post(
    "/change-channel-settings/",
    response_model=None,
    summary="Change user settings",
    description='Change user channel notifications settings by sending boolean in "ENABLED" parameter',
    responses={
        status.HTTP_401_UNAUTHORIZED: {"description": "Missing token or inactive user."}
    },
)
async def change_channel_settings(
    channel: str,
    enabled: bool,
    user = Depends(get_current_user),
    notification_settings_service: NotificationSettingsServiceABC = Depends(get_notification_settings_service),
) -> Response(status_code=status.HTTP_200_OK):
    pass


@router.post(
    "/change-notification-settings/",
    response_model=None,
    summary="Change user exact notification setting",
    description='Receive or not exact notification by sending boolean in "DISABLED" parameter',
    responses={
        status.HTTP_401_UNAUTHORIZED: {"description": "Missing token or inactive user."}
    },
)
async def change_notification_settings(
    notification_id: UUID,
    disabled: bool,
    user = Depends(get_current_user),
    notification_settings_service: NotificationSettingsServiceABC = Depends(get_notification_settings_service),
) -> Response(status_code=status.HTTP_200_OK):
    pass
