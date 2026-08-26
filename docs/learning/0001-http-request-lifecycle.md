# Learning 0001: FastAPI HTTP request lifecycle

## Visible result

`GET /health/live` returns the process status, service version, and active environment.
The response also carries the same `X-Trace-ID` recorded in the structured request log.

```json
{
  "status": "ok",
  "service": "ScenicOps API",
  "version": "0.1.0",
  "environment": "local"
}
```

## Request path

1. Uvicorn receives the HTTP request and passes it to FastAPI.
2. The HTTP middleware validates or generates the Trace ID.
3. The top-level router delegates `/health/*` requests to the health router.
4. The route function reads validated application settings.
5. `HealthResponse` defines and validates the public response contract.
6. FastAPI serializes the model into JSON.
7. The middleware adds `X-Trace-ID` and records status and duration.

## Why the environment is not hard-coded

The same application package can run in `local`, `test`, `staging`, or `production`.
The route reads `settings.environment`, so deployment configuration selects the value without
changing application code.

## Why the test changes with the response

An API response is a contract with its clients. The test protects that contract by checking the
status code, fields, and values. A code change without a matching contract test is not complete.

## Interview explanation

The liveness route stays independent of PostgreSQL, Redis, Kafka, and model providers. It proves
that the process can answer HTTP requests. Readiness will check mandatory dependencies and can
return `503` while liveness still returns `200`.
