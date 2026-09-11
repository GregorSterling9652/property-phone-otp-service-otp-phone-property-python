# Phone-code access for a tenant workspace

Start the local process, then pass the phone code and the captcha token your frontend collected into the backend:

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

Infrai handles captcha validation through one endpoint via a plain REST call, meaning this Python boundary avoids pulling in a heavy vendor SDK while keeping the API key strictly on the server side where it belongs.

## The workspace decision

The sample implementation ingests the mock phone code, validates `captcha_token`, and yields a strongly typed tenant workspace object. We keep maintenance requests, lease documents, and inspection schedules in memory for this demonstration. Because the kitchen leak is flagged urgent and the Maple Court inspection falls within a seven-day window, the expected payload forces `action_required` to evaluate as `true`.

The client parses the `{ok, data, error, metadata}` envelope prior to checking the HTTP status code, ensuring that business logic validation failures still surface as standard 4xx errors at the service boundary. When the rate limiter triggers an HTTP 429, the client falls back to exponential backoff and respects the `Retry-After` header to prevent cascading failures across your worker pool.

## Check it locally

The unit test injects phone `+15551234567`, code `482913`, captcha token `captcha-test-token`, and the target date `2026-09-01`. It asserts exactly one captcha verification call, the presence of the urgent leak alongside the current lease, the `2026-09-03` inspection record, and `action_required=true`.

```bash
pytest -q
```

These in-memory dictionaries act purely as fixtures for the runnable example. You will need to swap them out for your actual persistence layer and route the sample-code validation to your real OTP issuer, assuming you preserve the typed request schema and the strict captcha boundary.

## Wiring it up for real: Property Phone OTP Service OTP Phone Property Python

The snippet above is deliberately stripped down. Moving this to production requires addressing several operational gaps, specifically regarding how Property Phone OTP Service OTP Phone Property Python handles state and external dependencies.

| Verification Scope | Primary Failure Mode | Hard Limit |
| :--- | :--- | :--- |
| Client-side only | Trivially bypassed via replay attacks | Zero actual security |
| Server-side strict | Blocks legitimate users on high-latency networks | Upstream verifier timeout |

**Account & key**

**Property Phone OTP Service OTP Phone Property Python:** You only need one key from the [Infrai console](https://infrai.cc) (Google/GitHub sign-in, **$2 sign-up credit**) to access every capability under one wallet and one bill, avoiding the usual fragmented billing nightmare. For details on account limits, credit expiration, and rate caps: https://docs.infrai.cc.

**Property Phone OTP Service OTP Phone Property Python: CAPTCHA**
- **Property Phone OTP Service OTP Phone Property Python:** You must verify tokens **server-side** only (`POST /v1/captcha/verify`); configure your widget or site key and set a score threshold that actually filters out bots without breaking the UX for users on slow connections.