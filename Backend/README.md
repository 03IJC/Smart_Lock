# Smart Lock Backend
Backend service for a fingerprint-based smart lock system with audit logging.
Provides authentication, access control, lock management, and full audit logging via a REST API.

Built with Python and FastAPI and designed for use with:
- A hardware smart lock device
- A web-based admin UI

## Architecture Overview
The system follows a service-oriented, layered architecture designed for security,
auditability, and future expansion.

## File Structure
The backend follows a layered architecture to separate concerns and improve maintainability.

- `src/`
  - `main.py` - FastAPI application entry point.
  - `api/` - API route definitions.
    - `authentication.py`
    - `users.py`
    - `fingerprints.py`
    - `locks.py`
    - `logs.py`
  - `core/` - App configuration and security.
    - `config.py`
    - `security.py`
    - `logging.py`
  - `database/` - Database setup and migrations.
    - `session.py`
    - `migrations/`
  - `models/` - Database models.
    - `base.py`
    - `fingerprint.py`
    - `lock.py`
    - `log.py`
    - `user.py`
  - `repositories/` - Data access layer.
    - `fingerprint_repository.py`
    - `lock_repository.py`
    - `log_repository.py`
    - `user_repository.py`
  - `schemas/` - Pydantic request/response schemas.
    - `authentication.py`
    - `device.py`
    - `fingerprint.py`
    - `lock.py`
    - `log.py`
    - `user.py`
  - `services/` - Business logic.
    - `authentication_service.py`
    - `access_service.py`
    - `logging_service.py`
  - `utils/` - Helper utilities
    - `time.py`

### File Structure Notes
Each layer has a single responsibility:
- **API**: HTTP and request validation
- **Services**: Business rules
- **Repositories**: Database access
- **Models/Schemas**: Data representation

## REST Endpoints
### Authentication Endpoints
- POST /auth/login | Authenticate user and return access tokens.
- GET /auth/me | Get current authenticated user.
### User Endpoints
- GET /users | List all users.
- POST /users | Create new user.
- GET /users/{id} | Get user by ID.
- PATCH /users/{id} | Update user details.
- DELETE /users/{id} | Soft delete a user.
### Fingerprint Endpoints
- GET /fingerprints | List approved fingerprints.
- POST /fingerprints | Register a new fingerprint.
- GET /fingerprints/{id} | Get fingerprint details.
- PATCH /fingerprints/{id} | Enable, disable, or update a fingerprint.
- DELETE /fingerprints/{id} | Soft delete a fingerprint.
### Lock Endpoints
- GET /locks | List all registered locks.
- GET /locks/{id} | Get lock details.
- POST /locks/{id}/unlock | Trigger an unlock action.
- POST /locks/{id}/lock | Trigger a lock action.
- GET /locks/{id}/state | Get current lock state.
- POST /locks/{id}/heartbeat | Device heartbeat and status update.
### Log Endpoints
- GET /logs | Retrieve access and system logs.
### System Endpoints
- GET /health | Retrieves backend status

#### Endpoint Notes
- All endpoints (except authentication and device heartbeat) require authentication via JWT.
- Access tokens will expire after 24 hours (requiring logging in again)
- Logs endpoint supports pagination and filtering via query parameters.
- Logs are expected to grow large and should be queried using pagination.
- Device-facing endpoints use separate authentication from admin users.


## Database Schema
The backend uses a relational database to persist system state and audit data.
All destructive operations use soft deletes to preserve historical records.
All timestamps are stored in UTC.

### Users
Admin users who can access the admin UI.

| Field         | Type      | Description                        |
|---------------|-----------|------------------------------------|
| id            | Int       | Unique user identifier             |
| name          | String    | Name                               |
| username      | String    | Unique login name                  |
| password_hash | String    | Hashed user password               |
| role          | String    | Authorization role (e.g., `admin`) |
| created_at    | Timestamp | User creation time                 |
| deleted_at    | Timestamp | Soft delete timestamp (nullable)   |

### Fingerprints
Approved fingerprint credentials.  
Raw biometric data is **never stored**.

| Field       | Type      | Description                             |
|-------------|-----------|-----------------------------------------|
| id          | Int       | Unique fingerprint identifier           |
| name        | String    | Name                                    |
| template_id | String    | Hardware fingerprint template reference |
| enabled     | Boolean   | Whether fingerprint is active           |
| created_at  | Timestamp | Enrollment timestamp                    |
| deleted_at  | Timestamp | Soft delete timestamp (nullable)        |

### Locks
Registered smart lock devices.

| Field          | Type      | Description                        |
|----------------|-----------|------------------------------------|
| id             | Int       | Unique lock identifier             |
| name           | String    | Human-readable lock name           |
| status         | Enum      | `locked`, `unlocked`, or `offline` |
| last_heartbeat | Timestamp | Last device heartbeat              |
| created_at     | Timestamp | Lock registration timestamp        |
| deleted_at     | Timestamp | Soft delete timestamp (nullable)   |

### Logs
Append-only audit log of system and lock events.  
Logs are **never modified or deleted**.

| Field          | Type      | Description                       |
|----------------|-----------|-----------------------------------|
| id             | Int       | Unique log identifier             |
| event_type     | Enum      | Type of event                     |
| lock_id        | Int       | Associated lock (nullable)        |
| fingerprint_id | Int       | Associated fingerprint (nullable) |
| user_id        | Int       | Associated admin user (nullable)  |
| success        | Boolean   | Whether the action succeeded      |
| timestamp      | Timestamp | Event timestamp                   |
| event_metadata | JSON      | Additional structured event data  |


