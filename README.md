# User Service

A FastAPI-based microservice that handles user authentication and management for the DolceIQ platform.

## API Endpoints

The root of the endpoint is /api/user

### Public endpoints

#### `GET /`

Service health check endpoint.

#### `POST /register`

Create a new user account.

#### `POST /token`

Authenticate user and receive access token.

### Protected Endpoints

#### `GET /me`

Get current user profile.

### Internal Endpoints

#### `GET /verify-token`

Internal endpoint for API Gateway token verification.

## Running (Docker)

From the orchestrator root directory, with the rest of service repositories cloned inside:

```bash
docker compose up --build
```

## Testing

From the orchestrator root:

```bash
make test-users
```
