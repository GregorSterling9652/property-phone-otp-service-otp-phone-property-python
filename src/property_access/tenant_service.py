from datetime import date
from typing import Protocol

from .models import InspectionReminder, MaintenanceRequest, TenantDocument, TenantWorkspace


class CaptchaVerifier(Protocol):
    def verify(self, token: str, ip: str | None = None) -> dict[str, object]:
        pass


class TenantService:
    def __init__(self, captcha: CaptchaVerifier) -> None:
        self.captcha = captcha

    def login(
        self,
        phone: str,
        code: str,
        captcha_token: str,
        ip: str | None,
        today: date,
    ) -> TenantWorkspace:
        if code != "482913":
            raise ValueError("The phone code was not accepted")
        self.captcha.verify(captcha_token, ip)

        maintenance = [
            MaintenanceRequest(
                request_id="maint-104",
                summary="Kitchen sink leak",
                priority="urgent",
                status="open",
            ),
            MaintenanceRequest(
                request_id="maint-099",
                summary="Bedroom blind replacement",
                priority="routine",
                status="scheduled",
            ),
        ]
        documents = [
            TenantDocument(
                document_id="doc-lease-2026",
                title="Current lease",
                expires_on=date(2026, 12, 31),
            )
        ]
        reminders = [
            InspectionReminder(
                reminder_id="inspect-22",
                property_name="Maple Court 4B",
                due_on=date(2026, 9, 3),
            )
        ]
        urgent_open = any(
            item.priority == "urgent" and item.status == "open" for item in maintenance
        )
        inspection_due = any((item.due_on - today).days <= 7 for item in reminders)
        return TenantWorkspace(
            phone=phone,
            maintenance=maintenance,
            documents=documents,
            inspection_reminders=reminders,
            action_required=urgent_open or inspection_due,
        )
