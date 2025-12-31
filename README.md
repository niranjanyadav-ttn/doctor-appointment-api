# 🏥 Doctor Appointment API

A production-ready RESTful API for managing doctor appointments with JWT authentication, role-based access control, and double-booking prevention.

![Python](https://img.shields.io/badge/Python-3.12+-blue.svg)
![FastAPI](https://img.shields.io/badge/FastAPI-0.109.0-green.svg)
![MySQL](https://img.shields.io/badge/MySQL-8.0-orange.svg)
![License](https://img.shields.io/badge/license-MIT-blue.svg)

## 📋 Table of Contents

- [Features](#-features)
- [Tech Stack](#-tech-stack)
- [Architecture](#-architecture)
- [Prerequisites](#-prerequisites)
- [Installation](#-installation)
- [Configuration](#-configuration)
- [Running the Application](#-running-the-application)
- [API Documentation](#-api-documentation)
- [API Endpoints](#-api-endpoints)
- [Authentication](#-authentication)
- [Authentication Flow & Design](#-authentication-flow--design)
- [RBAC Design](#-role-based-access-control-rbac-design)
- [Double-Booking Prevention](#-double-booking-prevention-logic)
- [Security Best Practices](#-security-best-practices-implemented)
- [Database Schema](#-database-schema)
- [Testing](#-testing)
- [Docker Deployment](#-docker-deployment)
- [Project Structure](#-project-structure)

---

## ✨ Features

- 🔐 **JWT Authentication** - Secure token-based authentication
- 👥 **Role-Based Access Control (RBAC)** - Doctor and Patient roles with specific permissions
- 📅 **Availability Management** - Doctors can set their available time slots
- 🏥 **Appointment Booking** - Patients can book appointments with doctors
- ⛔ **Double-Booking Prevention** - Automatic conflict detection prevents overlapping appointments
- ❌ **Appointment Cancellation** - Patients can cancel their appointments
- 🔍 **Real-time Availability** - Check doctor availability before booking
- 📝 **Comprehensive API Documentation** - Interactive Swagger UI and ReDoc
- ⚡ **Async Operations** - High-performance async database operations
- 🛡️ **Input Validation** - Pydantic schemas for request/response validation
- 🗄️ **Relational Database** - MySQL with proper foreign keys and indexes

---

## 🛠️ Tech Stack

### Backend
- **FastAPI** - Modern, fast web framework for building APIs
- **Python 3.12+** - Programming language
- **Uvicorn** - ASGI server for production

### Database
- **MySQL 8.0** - Relational database
- **SQLAlchemy** - ORM with async support
- **Alembic** - Database migrations

### Authentication & Security
- **JWT (JSON Web Tokens)** - Stateless authentication
- **Bcrypt** - Password hashing
- **python-jose** - JWT encoding/decoding

### Development Tools
- **Pydantic** - Data validation
- **Pytest** - Testing framework
- **Docker** - Containerization
- **Git** - Version control

---

## 🏗️ Architecture

```
┌─────────────┐
│   Client    │
│  (Browser)  │
└──────┬──────┘
       │
       ▼
┌─────────────────────────────────────┐
│          FastAPI Application         │
│  ┌───────────────────────────────┐  │
│  │         API Routers           │  │
│  │  - Auth    - Doctors          │  │
│  │  - Appointments               │  │
│  └──────────┬────────────────────┘  │
│             │                        │
│  ┌──────────▼────────────────────┐  │
│  │      Service Layer            │  │
│  │  - AuthService                │  │
│  │  - DoctorService              │  │
│  │  - PatientService             │  │
│  └──────────┬────────────────────┘  │
│             │                        │
│  ┌──────────▼────────────────────┐  │
│  │    Repository Layer           │  │
│  │  - UserRepository             │  │
│  │  - AvailabilityRepository     │  │
│  │  - AppointmentRepository      │  │
│  └──────────┬────────────────────┘  │
│             │                        │
└─────────────┼────────────────────────┘
              │
              ▼
      ┌───────────────┐
      │  MySQL DB     │
      │  - users      │
      │  - availabilities │
      │  - appointments   │
      └───────────────┘
```

### Design Patterns

- **Repository Pattern** - Separates data access logic
- **Service Layer Pattern** - Encapsulates business logic
- **Dependency Injection** - FastAPI's built-in DI system
- **DTO Pattern** - Pydantic schemas for data transfer

---

## 📦 Prerequisites

- **Python 3.12+**
- **Docker & Docker Compose** (for MySQL)
- **Git**
- **pip** (Python package manager)

---

## 🚀 Installation

### 1. Clone the Repository

```bash
git clone https://github.com/niranjanyadav-ttn/doctor-appointment-api.git
cd doctor-appointment-api
```

### 2. Create Virtual Environment

```bash
# Create virtual environment
python -m venv venv

# Activate virtual environment
# On Linux/Mac:
source venv/bin/activate

# On Windows:
venv\Scripts\activate
```

### 3. Install Dependencies

```bash
pip install --upgrade pip
pip install -r requirements.txt
```

### 4. Setup MySQL Database

```bash
# Start MySQL container
docker compose up -d mysql

# Wait 30 seconds for MySQL to initialize
# Verify it's running
docker ps
```

### 5. Configure Environment Variables

```bash
# Copy environment template
cp .env.example .env

# Edit .env with your configuration (optional)
nano .env
```

### 6. Initialize Database

The database tables will be created automatically when you start the application.

---

## ⚙️ Configuration

### Environment Variables (`.env`)

```env
# Database Configuration
DATABASE_URL=mysql+aiomysql://root:rootpassword@localhost:3306/doctor_appointments

# JWT Configuration
SECRET_KEY=your-secret-key-here-change-in-production
ALGORITHM=HS256
ACCESS_TOKEN_EXPIRE_MINUTES=30

# Application Configuration
DEBUG=True
APP_HOST=0.0.0.0
APP_PORT=8000
```

**🔒 Security Note:** Change `SECRET_KEY` in production!

Generate a secure secret key:
```bash
python -c "import secrets; print(secrets.token_urlsafe(32))"
```

---

## 🏃 Running the Application

### Development Mode

```bash
uvicorn app.main:app --reload --host 0.0.0.0 --port 8000
```

### Production Mode

```bash
uvicorn app.main:app --host 0.0.0.0 --port 8000 --workers 4
```

### Access the Application

- **API Base URL:** http://localhost:8000
- **Swagger UI (Interactive Docs):** http://localhost:8000/docs
- **ReDoc:** http://localhost:8000/redoc
- **Health Check:** http://localhost:8000/health

---

## 📚 API Documentation

Interactive API documentation is available at:

- **Swagger UI:** http://localhost:8000/docs
- **ReDoc:** http://localhost:8000/redoc

---

## 🔌 API Endpoints

### Authentication Endpoints

| Method | Endpoint | Description | Auth Required |
|--------|----------|-------------|---------------|
| POST | `/auth/register` | Register new user (Doctor/Patient) | ❌ |
| POST | `/auth/login` | Login and receive JWT token | ❌ |
| POST | `/auth/forgot-password` | Request password reset | ❌ |

### Doctor Endpoints

| Method | Endpoint | Description | Auth Required |
|--------|----------|-------------|---------------|
| GET | `/doctors` | Get all doctors | ❌ |
| GET | `/doctors/{id}/availability` | Get doctor's availability | ❌ |
| POST | `/doctors/availability` | Set availability (Doctor only) | ✅ Doctor |
| GET | `/doctors/my-appointments` | Get doctor's appointments | ✅ Doctor |

### Appointment Endpoints

| Method | Endpoint | Description | Auth Required |
|--------|----------|-------------|---------------|
| POST | `/appointments` | Book appointment (Patient only) | ✅ Patient |
| DELETE | `/appointments/{id}` | Cancel appointment (Patient only) | ✅ Patient |
| GET | `/appointments/my-appointments` | Get user's appointments | ✅ Any |

---

## 🔐 Authentication

### Registration

**POST** `/auth/register`

```json
{
  "email": "doctor@example.com",
  "name": "Dr. John Smith",
  "role": "Doctor",
  "password": "securepassword123"
}
```

### Login

**POST** `/auth/login`

```json
{
  "email": "doctor@example.com",
  "password": "securepassword123"
}
```

**Response:**
```json
{
  "access_token": "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9...",
  "token_type": "bearer"
}
```

### Using the Token

Add the token to the Authorization header:

```
Authorization: Bearer <your-token-here>
```

### Role-Based Access Control

- **Doctor Role:**
  - Can set availability
  - Can view their appointments
  - Cannot book appointments

- **Patient Role:**
  - Can view all doctors
  - Can book appointments
  - Can cancel their appointments
  - Cannot set availability

---

## 🔐 Authentication Flow & Design

### JWT Authentication Flow

```
Step 1: User Registration
--------------------------
Client                                    Server
  |                                         |
  | POST /auth/register                     |
  | {email, password, name, role}           |
  |---------------------------------------->|
  |                                         |
  |                        Hash password    |
  |                        Store in DB      |
  |                                         |
  | Return user (without password)          |
  |<----------------------------------------|


Step 2: User Login
-------------------
Client                                    Server
  |                                         |
  | POST /auth/login                        |
  | {email, password}                       |
  |---------------------------------------->|
  |                                         |
  |                        Verify password  |
  |                        Generate JWT     |
  |                                         |
  | Return JWT token                        |
  |<----------------------------------------|


Step 3: Authenticated Request
------------------------------
Client                                    Server
  |                                         |
  | GET /doctors/my-appointments            |
  | Authorization: Bearer <token>           |
  |---------------------------------------->|
  |                                         |
  |                        Decode JWT       |
  |                        Verify token     |
  |                        Check role       |
  |                        Get user data    |
  |                                         |
  | Return appointments                     |
  |<----------------------------------------|
```

### Authentication Components

#### 1. Password Security
- **Hashing Algorithm:** Bcrypt with 12 rounds
- **Password Requirements:** Minimum 8 characters
- **Storage:** Only hashed passwords stored, never plaintext
- **Verification:** Constant-time comparison to prevent timing attacks

**Password hashing implementation:**

```python
def get_password_hash(password: str) -> str:
    password_bytes = password.encode('utf-8')[:72]  # Bcrypt limit
    salt = bcrypt.gensalt(rounds=12)
    hashed = bcrypt.hashpw(password_bytes, salt)
    return hashed.decode('utf-8')
```

#### 2. JWT Token Structure

```json
{
  "sub": "user@example.com",      // Subject (user identifier)
  "role": "Doctor",                // User role for RBAC
  "exp": 1704067200                // Expiration timestamp
}
```

- **Algorithm:** HS256 (HMAC with SHA-256)
- **Expiration:** 30 minutes (configurable)
- **Secret Key:** Stored in environment variables
- **Payload:** Contains user email and role for authorization

#### 3. Token Validation Process

1. Extract token from `Authorization: Bearer <token>` header
2. Decode JWT using secret key
3. Verify token signature
4. Check expiration timestamp
5. Extract user information from payload
6. Query database to get current user state
7. Return authenticated user object

---

## 👥 Role-Based Access Control (RBAC) Design

### Role Hierarchy

```
User (Base)
├── id
├── email
├── name
├── password_hash
└── role
    ├── DOCTOR
    │   ├── Can set availability
    │   ├── Can view their appointments
    │   └── Cannot book appointments
    │
    └── PATIENT
        ├── Can view all doctors
        ├── Can book appointments
        ├── Can cancel their appointments
        └── Cannot set availability
```

### Permission Matrix

| Action | Endpoint | Doctor | Patient | Public |
|--------|----------|--------|---------|--------|
| Register User | `POST /auth/register` | ✅ | ✅ | ✅ |
| Login | `POST /auth/login` | ✅ | ✅ | ✅ |
| View All Doctors | `GET /doctors` | ✅ | ✅ | ✅ |
| View Doctor Availability | `GET /doctors/{id}/availability` | ✅ | ✅ | ✅ |
| **Set Availability** | `POST /doctors/availability` | ✅ | ❌ | ❌ |
| **View Doctor's Appointments** | `GET /doctors/my-appointments` | ✅ | ❌ | ❌ |
| **Book Appointment** | `POST /appointments` | ❌ | ✅ | ❌ |
| **Cancel Appointment** | `DELETE /appointments/{id}` | ❌ | ✅ | ❌ |
| View My Appointments | `GET /appointments/my-appointments` | ✅ | ✅ | ❌ |

### RBAC Implementation

#### 1. Role Definition

```python
class UserRole(str, Enum):
    """User roles for role-based access control."""
    DOCTOR = "Doctor"
    PATIENT = "Patient"
```

#### 2. Role Verification (Dependency Injection)

```python
async def get_current_doctor(
    current_user: User = Depends(get_current_user)
) -> User:
    """Verify user has Doctor role."""
    if current_user.role != UserRole.DOCTOR:
        raise HTTPException(
            status_code=403,
            detail="Only doctors can access this endpoint"
        )
    return current_user
```

#### 3. Endpoint Protection

```python
@router.post("/doctors/availability")
async def set_availability(
    availability_data: AvailabilityCreate,
    current_user: User = Depends(get_current_doctor),  # Role check here
    db: AsyncSession = Depends(get_db)
):
    # Only executed if user is a Doctor
    ...
```

### Authorization Flow Examples

**Example 1: Patient Tries to Set Availability (Denied)**

```
POST /doctors/availability
Authorization: Bearer <patient_jwt_token>

Flow:
1. Extract JWT token from header ✅
2. Decode and verify token signature ✅
3. Get user from database (Role: Patient) ✅
4. Check if user.role == DOCTOR ❌
5. Raise HTTPException(403, "Only doctors can access")

Result: 403 Forbidden
```

**Example 2: Doctor Sets Availability (Allowed)**

```
POST /doctors/availability
Authorization: Bearer <doctor_jwt_token>

Flow:
1. Extract JWT token from header ✅
2. Decode and verify token signature ✅
3. Get user from database (Role: Doctor) ✅
4. Check if user.role == DOCTOR ✅
5. Check for availability conflicts ✅
6. Create availability slot ✅

Result: 201 Created
```

### Resource Ownership Validation

Patients can only cancel their own appointments:

```python
async def cancel_appointment(appointment_id: int, patient_id: int):
    appointment = await get_appointment(appointment_id)

    # Verify ownership
    if appointment.patient_id != patient_id:
        raise HTTPException(
            status_code=403,
            detail="You can only cancel your own appointments"
        )

    # Proceed with cancellation
    return await repository.cancel_appointment(appointment_id)
```

---

## 🎯 Double-Booking Prevention Logic

### How It Works

The system implements a two-step validation process to prevent double-booking:

#### Step 1: Availability Validation

```python
# Check if requested time slot is within doctor's availability
availabilities = await get_doctor_availabilities(doctor_id)
is_within_availability = False

for availability in availabilities:
    if (availability.start_time <= requested_start and 
        availability.end_time >= requested_end):
        is_within_availability = True
        break

if not is_within_availability:
    raise HTTPException(400, "Time slot not within doctor's availability")
```

#### Step 2: Conflict Detection

```python
# Check for existing confirmed appointments that overlap
existing_appointments = await get_doctor_appointments(
    doctor_id=doctor_id,
    status="confirmed"
)

for appointment in existing_appointments:
    # Check if time slots overlap
    if (requested_start < appointment.end_time and 
        requested_end > appointment.start_time):
        raise HTTPException(400, "This time slot is already booked")

# No conflicts found - create appointment
return await create_appointment(...)
```

### Overlap Detection Algorithm

**Mathematical Condition for Overlapping:**
```
Appointment 1: [start1, end1]
Appointment 2: [start2, end2]

Overlap if: start2 < end1 AND end2 > start1
```

**Example Scenarios:**

```
Existing Appointment: [10:00, 11:00]

Scenario 1: New [10:30, 11:30] → CONFLICT ❌ (overlaps)
Scenario 2: New [11:00, 12:00] → SUCCESS ✅ (no overlap)
Scenario 3: New [09:00, 10:00] → SUCCESS ✅ (no overlap)
Scenario 4: New [09:30, 10:30] → CONFLICT ❌ (overlaps)
Scenario 5: New [10:00, 11:00] → CONFLICT ❌ (exact match)
```

### Database-Level Protection

The system uses database transactions and proper indexing to ensure data consistency:

- Foreign key constraints ensure referential integrity
- Indexed queries on `doctor_id`, `start_time`, and `status` for fast lookups
- Async operations with proper transaction handling

---

## 🔒 Security Best Practices Implemented

1. ✅ **Password Security**
   - Bcrypt hashing with salt
   - 12-round cost factor
   - 72-byte limit compliance
   - Constant-time verification

2. ✅ **JWT Security**
   - Secret key stored in environment variables
   - Token expiration (30 minutes)
   - Signature verification on every request
   - HS256 algorithm

3. ✅ **RBAC Implementation**
   - Role stored in JWT payload
   - Role verified on protected endpoints
   - Cannot be forged or bypassed
   - Resource ownership validation

4. ✅ **Input Validation**
   - Pydantic schemas validate all inputs
   - Email format validation
   - Password length requirements
   - DateTime validation

5. ✅ **Database Security**
   - Parameterized queries (SQL injection prevention)
   - Foreign key constraints
   - Cascade deletion for data integrity
   - Proper indexing for performance

6. ✅ **Error Handling**
   - No sensitive information in error messages
   - Consistent error responses
   - Proper HTTP status codes

7. ✅ **Environment Security**
   - Secrets in `.env` file (not committed)
   - `.env.example` for documentation
   - `.gitignore` prevents secret exposure

---

## 🗄️ Database Schema

### Users Table

```sql
CREATE TABLE users (
    id INT PRIMARY KEY AUTO_INCREMENT,
    email VARCHAR(255) UNIQUE NOT NULL,
    password_hash VARCHAR(255) NOT NULL,
    name VARCHAR(255) NOT NULL,
    role ENUM('Doctor', 'Patient') NOT NULL,
    INDEX idx_email (email),
    INDEX idx_role (role)
);
```

### Availabilities Table

```sql
CREATE TABLE availabilities (
    id INT PRIMARY KEY AUTO_INCREMENT,
    doctor_id INT NOT NULL,
    start_time DATETIME NOT NULL,
    end_time DATETIME NOT NULL,
    FOREIGN KEY (doctor_id) REFERENCES users(id) ON DELETE CASCADE,
    INDEX idx_doctor_id (doctor_id),
    INDEX idx_start_time (start_time)
);
```

### Appointments Table

```sql
CREATE TABLE appointments (
    id INT PRIMARY KEY AUTO_INCREMENT,
    doctor_id INT NOT NULL,
    patient_id INT NOT NULL,
    start_time DATETIME NOT NULL,
    end_time DATETIME NOT NULL,
    status ENUM('confirmed', 'cancelled') NOT NULL DEFAULT 'confirmed',
    FOREIGN KEY (doctor_id) REFERENCES users(id) ON DELETE CASCADE,
    FOREIGN KEY (patient_id) REFERENCES users(id) ON DELETE CASCADE,
    INDEX idx_doctor_id (doctor_id),
    INDEX idx_patient_id (patient_id),
    INDEX idx_status (status)
);
```

---

## 🧪 Testing

### Manual Testing via Swagger UI

1. **Register Doctor and Patient**
   - POST `/auth/register` with Doctor role
   - POST `/auth/register` with Patient role

2. **Login and Authorize**
   - POST `/auth/login` to get JWT token
   - Click "Authorize" button in Swagger UI
   - Paste the token

3. **Set Availability (as Doctor)**
   - POST `/doctors/availability`

4. **Book Appointment (as Patient)**
   - POST `/appointments`

5. **Test Double-Booking Prevention**
   - Try to book the same time slot twice
   - Should receive 400 error: "This time slot is already booked"

6. **Cancel Appointment**
   - DELETE `/appointments/{id}`

### Example: Test Double-Booking Prevention

```bash
# Book first appointment (Success ✅)
POST /appointments
{
  "doctor_id": 1,
  "start_time": "2026-01-15T10:00:00",
  "end_time": "2026-01-15T11:00:00"
}

# Try to book overlapping appointment (Failure ❌)
POST /appointments
{
  "doctor_id": 1,
  "start_time": "2026-01-15T10:30:00",
  "end_time": "2026-01-15T11:30:00"
}
# Response: 400 Bad Request
# "This time slot is already booked. Please choose another time."
```

---

## 🐳 Docker Deployment

### Using Docker Compose

```bash
# Build and start all services
docker compose up -d

# View logs
docker compose logs -f

# Stop services
docker compose down

# Stop and remove data
docker compose down -v
```

### Access the Application

```
http://localhost:8000/docs
```

---

## 📁 Project Structure

```
doctor-appointment-api/
├── app/
│   ├── __init__.py
│   ├── main.py                 # FastAPI application entry point
│   ├── config.py               # Configuration management
│   ├── database.py             # Database connection & session
│   │
│   ├── models/                 # SQLAlchemy ORM models
│   │   ├── __init__.py
│   │   ├── user.py
│   │   ├── availability.py
│   │   └── appointment.py
│   │
│   ├── schemas/                # Pydantic schemas
│   │   ├── __init__.py
│   │   ├── user.py
│   │   ├── auth.py
│   │   ├── availability.py
│   │   └── appointment.py
│   │
│   ├── repositories/           # Data access layer
│   │   ├── __init__.py
│   │   ├── user.py
│   │   ├── availability.py
│   │   └── appointment.py
│   │
│   ├── services/               # Business logic layer
│   │   ├── __init__.py
│   │   ├── auth.py
│   │   ├── doctor.py
│   │   └── patient.py
│   │
│   ├── routers/                # API endpoints
│   │   ├── __init__.py
│   │   ├── auth.py
│   │   ├── doctors.py
│   │   └── appointments.py
│   │
│   └── dependencies/           # FastAPI dependencies
│       ├── __init__.py
│       └── auth.py
│
├── tests/                      # Test files
│   └── __init__.py
│
├── .env                        # Environment variables (not in git)
├── .env.example                # Environment template
├── .gitignore                  # Git ignore rules
├── docker-compose.yml          # Docker services configuration
├── requirements.txt            # Python dependencies
├── pytest.ini                  # Pytest configuration
└── README.md                   # This file
```

---

## 🤝 Contributing

Contributions are welcome! Please follow these steps:

1. Fork the repository
2. Create a feature branch (`git checkout -b feature/AmazingFeature`)
3. Commit your changes (`git commit -m 'Add some AmazingFeature'`)
4. Push to the branch (`git push origin feature/AmazingFeature`)
5. Open a Pull Request

---

## 📝 License

This project is licensed under the MIT License.

---

## 👤 Author

**Niranjan Kumar Yadav**

- GitHub: [@niranjanyadav-ttn](https://github.com/niranjanyadav-ttn)

---

## 🙏 Acknowledgments

- FastAPI documentation and community
- SQLAlchemy async support
- Python asyncio ecosystem

---

## 🔄 Changelog

### Version 1.0.0 (2025-12-31)

- ✅ Initial release
- ✅ JWT authentication with bcrypt
- ✅ Role-based access control
- ✅ Doctor availability management
- ✅ Appointment booking system
- ✅ Double-booking prevention
- ✅ Appointment cancellation
- ✅ Complete API documentation

---

**Made with ❤️ using FastAPI and Python**
