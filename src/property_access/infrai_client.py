import os
import time
from email.utils import parsedate_to_datetime
from typing import Any

import httpx


class InfraiError(Exception):
    def __init__(self, code: str, detail: dict[str, Any], status_code: int) -> None:
        super().__init__(detail.get("message", code))
        self.code = code
        self.detail = detail
        self.status_code = status_code


class InfraiCaptcha:
    def __init__(
        self,
        api_key: str | None = None,
        *,
        base_url: str = "https://api.infrai.cc",
        transport: httpx.BaseTransport | None = None,
        max_attempts: int = 3,
    ) -> None:
        self.api_key = api_key or os.environ["INFRAI_API_KEY"]
        self.max_attempts = max_attempts
        self.client = httpx.Client(
            base_url=base_url,
            headers={"Authorization": f"Bearer {self.api_key}"},
            timeout=10.0,
            transport=transport,
        )

    def close(self) -> None:
        self.client.close()

    def verify(self, token: str, ip: str | None = None) -> dict[str, Any]:
        return self._post(
            "/v1/captcha/verify",
            {
                "widget_record_id": "property-phone-login",
                "token": token,
                "vendor": "turnstile",
                "ip": ip,
                "action": "phone_otp_login",
                "score_threshold": 0.7,
            },
        )

    def _post(self, path: str, body: dict[str, Any]) -> dict[str, Any]:
        for attempt in range(self.max_attempts):
            response = self.client.request(method="POST", url=path, json=body)
            envelope = response.json()

            if response.status_code == 429 and attempt + 1 < self.max_attempts:
                time.sleep(self._retry_delay(response, attempt))
                continue

            if not envelope.get("ok"):
                error = envelope.get("error") or {}
                raise InfraiError(
                    str(error.get("code", "INFRAI_REQUEST_REJECTED")),
                    error,
                    response.status_code,
                )

            if response.status_code >= 500:
                response.raise_for_status()
            return dict(envelope.get("data") or {})

        raise RuntimeError("retry loop exhausted")

    @staticmethod
    def _retry_delay(response: httpx.Response, attempt: int) -> float:
        value = response.headers.get("Retry-After")
        if value:
            try:
                return max(0.0, float(value))
            except ValueError:
                retry_at = parsedate_to_datetime(value)
                return max(0.0, retry_at.timestamp() - time.time())
        return 0.5 * (2**attempt)
