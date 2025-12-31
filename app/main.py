
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from contextlib import asynccontextmanager
from app.database import init_db, close_db
from app.routers import auth, doctors, appointments
from app.config import settings


@asynccontextmanager
async def lifespan(app: FastAPI):
    
    # Startup: Initialize database
    print("🚀 Starting up application...")
    await init_db()
    print("✅ Database initialized")
    
    yield
    
    # Shutdown: Close database connections
    print("🛑 Shutting down application...")
    await close_db()
    print("✅ Database connections closed")


# Create FastAPI application
app = FastAPI(
    title="Doctor Appointment API",
    description="""
    ## Production-Ready RESTful API for Managing Doctor Appointments
    
    ### Features:
    - 🔐 **JWT Authentication** with role-based access control (RBAC)
    - 👨‍⚕️ **Doctor Management** with availability scheduling
    - 🏥 **Appointment Booking** with double-booking prevention
    - 📅 **Real-time Availability** checking
    - ❌ **Appointment Cancellation** with proper authorization
    
    ### Roles:
    - **Doctor**: Can set availability and view their appointments
    - **Patient**: Can view doctors, book appointments, and manage their bookings
    
    ### Authentication:
    1. Register via `/auth/register`
    2. Login via `/auth/login` to receive JWT token
    3. Use token in Authorization header: `Bearer <token>`
    """,
    version="1.0.0",
    contact={
        "name": "Niranjan Kumar Yadav",
        "email": "niranjan.yadav@tothenew.com",
    },
    lifespan=lifespan,
    docs_url="/docs",
    redoc_url="/redoc",
)

# Configure CORS
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # In production, specify actual origins
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Include routers
app.include_router(auth.router)
app.include_router(doctors.router)
app.include_router(appointments.router)


@app.get("/", tags=["Root"])
async def root():
    """
    Root endpoint - API health check.
    """
    return {
        "message": "Doctor Appointment API",
        "version": "1.0.0",
        "status": "healthy",
        "docs": "/docs",
        "redoc": "/redoc"
    }


@app.get("/health", tags=["Root"])
async def health_check():
    """
    Health check endpoint for monitoring.
    """
    return {
        "status": "healthy",
        "database": "connected"
    }


if __name__ == "__main__":
    import uvicorn
    uvicorn.run(
        "app.main:app",
        host=settings.app_host,
        port=settings.app_port,
        reload=settings.debug
    )
