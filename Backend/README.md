# Smart Lock Backend
Backend service for a fingerprint-based smart lock system built with FastAPI.

The system provides:
- secure admin authentication
- fingerprint-based access control
- device communication for smart locks
- append-only audit logging of all system activity

The backend is designed to operate alongside:
- an ESP32-based hardware smart lock device
- a web-based admin interface

## Architecture Overview
The system follows a service-oriented, layered architecture designed for security,
auditability, and future expansion.

## Tech Stack
Backend
- FastAPI
- Python
- SQLAlchemy
- Alembic

Database
- PostgreSQL

Infrastructure
- Docker
- Docker Compose

Authentication
- JWT Access Tokens

## Security Model
The backend enforces multiple security layers:

Admin Authentication
- Admin users authenticate via JWT access tokens.
- Tokens expire after 24 hours.

Device Authentication
- Hardware devices authenticate using a shared device API key.

Audit Logging
- All access attempts and admin actions are recorded.
- Logs are append-only and cannot be modified or deleted.

Data Integrity
- All destructive operations use soft deletes to preserve historical records.

Biometric Privacy
- Raw fingerprint biometric data is never stored.
- Only hardware template identifiers are persisted.

## How to Run
### Prerequisites
- Docker
- Docker Compose

### Setup
1. Clone the repository and go to the backend directory
```bash
  git clone https://github.com/03IJC/Smart_Lock.git
  cd smart-lock/Backend
```
2. Copy the example environment file and edit `.env` and fill in your values.
```bash
  cp .env.example .env
```
3. Start the services
```bash
  docker compose up --build
```
4. Run database migrations
```bash
  docker compose exec api alembic upgrade head
```
5. Create first admin user and insert them into the database
```bash
   docker compose exec api python3 -c "from src.core.security import hash_password; print(hash_password('yourpassword'))"
```
```bash
   docker compose exec db psql -U $DB_USER -d $DB_NAME
```
```sql
   INSERT INTO users (name, username, password_hash, role, created_at)
   VALUES ('Admin', 'admin', '<PASTE_HASH_HERE>', 'admin', NOW());
```
6. Access the API docs
```
   http://localhost:8000/docs
```

### Stopping the services
```bash
  docker compose down
```

### Resetting the database
```bash
  docker compose down -v
```

## File Structure
The backend follows a layered architecture to separate concerns and improve maintainability.

- `src/`
  - `main.py` - FastAPI application entry point.
  - `api/` - API route definitions.
    - `authentication.py`
    - `device.py`
    - `fingerprints.py`
    - `locks.py`
    - `logs.py`
    - `users.py`
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
    - `fingerprint_service.py`
    - `lock_service.py`
    - `log_service.py`
    - `user_service.py`

### File Structure Notes
Each layer has a single responsibility:
- **API**: HTTP and request validation
- **Core** App configuration and security
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
- PATCH /users/{id}/password | Change a user's password.
- DELETE /users/{id} | Soft delete a user.
### Fingerprint Endpoints
- GET /fingerprints | List of fingerprints.
  - ?enabled=true | List of enabled fingerprints.
- POST /fingerprints | Register a new fingerprint.
- GET /fingerprints/{id} | Get fingerprint details.
- PATCH /fingerprints/{id} | Enable, disable, or update a fingerprint.
- DELETE /fingerprints/{id} | Soft delete a fingerprint.
### Lock Endpoints
- GET /locks | List all registered locks.
- POST /locks | Create new lock.
- GET /locks/{id} | Get lock details.
- POST /locks/{id}/unlock | Trigger an unlock action.
- POST /locks/{id}/lock | Trigger a lock action.
- GET /locks/{id}/state | Get current lock state.
- DELETE /locks/{id} | Delete a lock.
### Log Endpoints
- GET /logs | Retrieve access and system logs.
  - ?event_type= | Filter by event type (e.g. unlock_attempt, admin_login)
  - ?lock_id= | Filter logs by associated lock
  - ?user_id= | Filter logs by associated admin user
  - ?success= | Filter by outcome (true or false)
  - ?start_time= | Filter logs after this timestamp (ISO 8601)
  - ?end_time= | Filter logs before this timestamp (ISO 8601)
  - ?limit= | Number of results per page (default: 50)
  - ?offset= | Number of results to skip for pagination (default: 0)
### System Endpoints
- GET /health | Retrieves backend status.
### Device Endpoints
- POST /device/heartbeat/{lock_id} | Lock heartbeat and status update.
- POST /device/access | Submit fingerprint scan and get access decision.

#### Endpoint Notes
- All admin endpoints require authentication via JWT.
- Device endpoints use separate API key authentication.
- Access tokens expire after 24 hours.
- Logs support pagination and filtering via query parameters.
- Logs are append-only and never modified or deleted.

## Device Communication Flow
1. The ESP32 device scans a fingerprint using the onboard sensor.
2. The device sends the fingerprint template ID and lock ID to the backend `/device/access` endpoint.
3. The backend validates the fingerprint and determines access permissions.
4. The backend returns an allow/deny decision.
5. The device unlocks the door if access is granted.
6. The access attempt is recorded in the audit log.

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


