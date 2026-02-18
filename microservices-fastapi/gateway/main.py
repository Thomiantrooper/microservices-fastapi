# gateway/main.py
from fastapi import FastAPI, HTTPException, Request, Depends
from fastapi.security import OAuth2PasswordRequestForm
from fastapi.responses import JSONResponse
import httpx
import logging
import time
from typing import Any
from datetime import timedelta
from auth import (
    authenticate_user, create_access_token, get_current_user,
    fake_users_db, hash_password,
    Token, UserCreate, UserResponse,
    ACCESS_TOKEN_EXPIRE_MINUTES
)

# Activity 3: Configure request logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger("api_gateway")

app = FastAPI(title="API Gateway", version="1.0.0")

# Service URLs
SERVICES = {
    "student": "http://localhost:8001",
    "course": "http://localhost:8002"
}

# Activity 3: Request Logging Middleware
@app.middleware("http")
async def log_requests(request: Request, call_next):
    start_time = time.time()
    logger.info(f"Incoming request: {request.method} {request.url}")
    response = await call_next(request)
    process_time = time.time() - start_time
    logger.info(f"Response: {request.method} {request.url} - Status: {response.status_code} - Time: {process_time:.4f}s")
    return response

async def forward_request(service: str, path: str, method: str, **kwargs) -> Any:
    """Forward request to the appropriate microservice"""
    if service not in SERVICES:
        raise HTTPException(status_code=404, detail=f"Service '{service}' not found. Available services: {list(SERVICES.keys())}")

    url = f"{SERVICES[service]}{path}"

    async with httpx.AsyncClient() as client:
        try:
            if method == "GET":
                response = await client.get(url, **kwargs)
            elif method == "POST":
                response = await client.post(url, **kwargs)
            elif method == "PUT":
                response = await client.put(url, **kwargs)
            elif method == "DELETE":
                response = await client.delete(url, **kwargs)
            else:
                raise HTTPException(status_code=405, detail=f"Method '{method}' not allowed")

            # Activity 4: Enhanced error handling
            if response.status_code >= 400:
                error_detail = response.json() if response.text else {"detail": "Unknown error from service"}
                return JSONResponse(
                    content=error_detail,
                    status_code=response.status_code
                )

            return JSONResponse(
                content=response.json() if response.text else None,
                status_code=response.status_code
            )
        except httpx.ConnectError:
            raise HTTPException(
                status_code=503,
                detail=f"Service '{service}' is unavailable. Please ensure the service is running on {SERVICES[service]}"
            )
        except httpx.TimeoutException:
            raise HTTPException(
                status_code=504,
                detail=f"Request to service '{service}' timed out"
            )
        except httpx.RequestError as e:
            raise HTTPException(
                status_code=503,
                detail=f"Service unavailable: {str(e)}"
            )

@app.get("/")
def read_root():
    return {"message": "API Gateway is running", "available_services": list(SERVICES.keys())}


@app.post("/auth/login", response_model=Token)
async def login(form_data: OAuth2PasswordRequestForm = Depends()):
    """Authenticate user and return JWT token"""
    user = authenticate_user(form_data.username, form_data.password)
    if not user:
        raise HTTPException(
            status_code=401,
            detail="Incorrect username or password",
            headers={"WWW-Authenticate": "Bearer"},
        )
    access_token = create_access_token(
        data={"sub": user["username"]},
        expires_delta=timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES)
    )
    return {"access_token": access_token, "token_type": "bearer"}

@app.post("/auth/register", response_model=UserResponse)
async def register(user: UserCreate):
    """Register a new user"""
    if user.username in fake_users_db:
        raise HTTPException(status_code=400, detail="Username already exists")
    fake_users_db[user.username] = {
        "username": user.username,
        "hashed_password": hash_password(user.password),
        "role": "user"
    }
    return {"username": user.username, "role": "user"}


@app.get("/gateway/students")
async def get_all_students(current_user: dict = Depends(get_current_user)):
    """Get all students through gateway"""
    return await forward_request("student", "/api/students", "GET")

@app.get("/gateway/students/{student_id}")
async def get_student(student_id: int, current_user: dict = Depends(get_current_user)):
    """Get a student by ID through gateway"""
    return await forward_request("student", f"/api/students/{student_id}", "GET")

@app.post("/gateway/students")
async def create_student(request: Request, current_user: dict = Depends(get_current_user)):
    """Create a new student through gateway"""
    body = await request.json()
    return await forward_request("student", "/api/students", "POST", json=body)

@app.put("/gateway/students/{student_id}")
async def update_student(student_id: int, request: Request, current_user: dict = Depends(get_current_user)):
    """Update a student through gateway"""
    body = await request.json()
    return await forward_request("student", f"/api/students/{student_id}", "PUT", json=body)

@app.delete("/gateway/students/{student_id}")
async def delete_student(student_id: int, current_user: dict = Depends(get_current_user)):
    """Delete a student through gateway"""
    return await forward_request("student", f"/api/students/{student_id}", "DELETE")


@app.get("/gateway/courses")
async def get_all_courses(current_user: dict = Depends(get_current_user)):
    """Get all courses through gateway"""
    return await forward_request("course", "/api/courses", "GET")

@app.get("/gateway/courses/{course_id}")
async def get_course(course_id: int, current_user: dict = Depends(get_current_user)):
    """Get a course by ID through gateway"""
    return await forward_request("course", f"/api/courses/{course_id}", "GET")

@app.post("/gateway/courses")
async def create_course(request: Request, current_user: dict = Depends(get_current_user)):
    """Create a new course through gateway"""
    body = await request.json()
    return await forward_request("course", "/api/courses", "POST", json=body)

@app.put("/gateway/courses/{course_id}")
async def update_course(course_id: int, request: Request, current_user: dict = Depends(get_current_user)):
    """Update a course through gateway"""
    body = await request.json()
    return await forward_request("course", f"/api/courses/{course_id}", "PUT", json=body)

@app.delete("/gateway/courses/{course_id}")
async def delete_course(course_id: int, current_user: dict = Depends(get_current_user)):
    """Delete a course through gateway"""
    return await forward_request("course", f"/api/courses/{course_id}", "DELETE")
