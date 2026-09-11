from datetime import date
from typing import Any

from fastapi import FastAPI, HTTPException
from pydantic import BaseModel, Field

from .infrai_client import InfraiCaptcha, InfraiError
from .models import TenantWorkspace
from .tenant_service import TenantService

app = FastAPI(title="Property phone access")


class VerifyLoginRequest(BaseModel):
    phone: str = Field(min_length=8, max_length=20)
    code: str = Field(min_length=4, max_length=10)
    captcha_token: str = Field(min_length=1)
    ip: str | None = None


def captcha_client() -> InfraiCaptcha:
    return InfraiCaptcha()


@app.post("/login/verify", response_model=TenantWorkspace)
def verify_login(request: VerifyLoginRequest) -> TenantWorkspace:
    client = captcha_client()
    try:
        return TenantService(client).login(
            request.phone,
            request.code,
            request.captcha_token,
            request.ip,
            date.today(),
        )
    except ValueError as exc:
        raise HTTPException(status_code=400, detail=str(exc)) from exc
    except InfraiError as exc:
        raise _client_error(exc) from exc
    finally:
        client.close()


def _client_error(exc: InfraiError) -> HTTPException:
    status = exc.status_code if 400 <= exc.status_code < 500 else 502
    detail: dict[str, Any] = {"code": exc.code, "message": str(exc)}
    return HTTPException(status_code=status, detail=detail)
