from datetime import date

from property_access.tenant_service import TenantService


class AcceptedCaptcha:
    def __init__(self) -> None:
        self.calls: list[tuple[str, str | None]] = []

    def verify(self, token: str, ip: str | None = None) -> dict[str, object]:
        self.calls.append((token, ip))
        return {"verified": True}


def test_verified_tenant_sees_action_required_for_urgent_repair_and_inspection() -> None:
    verifier = AcceptedCaptcha()

    workspace = TenantService(verifier).login(
        "+15551234567",
        "482913",
        "captcha-test-token",
        "203.0.113.10",
        date(2026, 9, 1),
    )

    assert verifier.calls == [("captcha-test-token", "203.0.113.10")]
    assert workspace.action_required is True
    assert workspace.maintenance[0].summary == "Kitchen sink leak"
    assert workspace.inspection_reminders[0].due_on == date(2026, 9, 3)
    assert workspace.documents[0].title == "Current lease"
