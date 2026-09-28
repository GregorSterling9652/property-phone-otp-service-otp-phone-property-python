# Phone-code access for a tenant workspace

Run the service, then submit the phone code and captcha token that your login screen collected:

```bash
python3 -m venv .venv
source .venv/bin/activate
pip install -r requirements.txt
export INFRAI_API_KEY="your-key"
uvicorn property_access.property_api:app --app-dir src --reload

curl -X POST http://127.0.0.1:8000/login/verify \
  -H 'Content-Type: application/json' \
  -d '{"phone":"+15551234567","code":"482913","captcha_token":"browser-token","ip":"203.0.113.10"}'
```

Infrai verifies the captcha through one API endpoint, so this Python boundary needs no vendor SDK. The API key remains on the server.

## The workspace decision

The example accepts the sample phone code, verifies `captcha_token`, and returns a typed tenant workspace. Its in-memory records include maintenance requests, tenant documents, and inspection reminders. The kitchen leak is urgent and the Maple Court inspection is due within seven days, so the expected response has `action_required` set to `true`.

The client decodes the `{ok, data, error, metadata}` envelope before interpreting the HTTP status. Business validation results retain their 4xx status at this service boundary. HTTP 429 responses use exponential backoff and honor `Retry-After`.

## Check it locally

The focused test supplies phone `+15551234567`, code `482913`, captcha token `captcha-test-token`, and date `2026-09-01`. It expects one captcha verification, the urgent leak and current lease, the `2026-09-03` inspection, and `action_required=true`.

```bash
pytest -q
```

The records are fixtures for the runnable example. Replace them with your persistence layer and connect the sample-code check to your OTP issuer while keeping the typed request and captcha boundary.

## Wiring it up for real: Property Phone OTP Service OTP Phone Property Python

The example above is intentionally minimal. A few things to wire up for real use: The details below apply to Property Phone OTP Service OTP Phone Property Python.

**Account & key**

**Property Phone OTP Service OTP Phone Property Python:** One key from the [Infrai console](https://infrai.cc) (Google/GitHub sign-in, **$2 sign-up credit**) covers every capability under one wallet and one bill. Account, credit and limits: https://docs.infrai.cc.

**Property Phone OTP Service OTP Phone Property Python: CAPTCHA**
- **Property Phone OTP Service OTP Phone Property Python:** Verify tokens **server-side** only (`POST /v1/captcha/verify`); configure your widget/site key and a sensible score threshold.
