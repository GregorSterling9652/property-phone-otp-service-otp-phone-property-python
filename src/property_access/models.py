from datetime import date
from dataclasses import dataclass
from typing import Literal


@dataclass(frozen=True)
class MaintenanceRequest:
    request_id: str
    summary: str
    priority: Literal["routine", "urgent"]
    status: Literal["open", "scheduled", "closed"]


@dataclass(frozen=True)
class TenantDocument:
    document_id: str
    title: str
    expires_on: date | None = None


@dataclass(frozen=True)
class InspectionReminder:
    reminder_id: str
    property_name: str
    due_on: date


@dataclass(frozen=True)
class TenantWorkspace:
    phone: str
    maintenance: list[MaintenanceRequest]
    documents: list[TenantDocument]
    inspection_reminders: list[InspectionReminder]
    action_required: bool
