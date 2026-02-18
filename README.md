# **FastAPI Microservices Architecture with API Gateway**

---

# **Overview**
This repository contains a **microservices-based backend system built with FastAPI**, implementing a centralized **API Gateway**, **JWT Authentication Service**, and **Student Service**. The architecture demonstrates secure request routing, service isolation, and scalable backend design using modern asynchronous Python technologies.

The **API Gateway acts as the single entry point**, handling authentication, validating JWT tokens, and forwarding requests to appropriate microservices.

---

# **Architecture**

## **System Architecture Diagram**

```
                ┌─────────────┐
                │   Client    │
                └──────┬──────┘
                       │
                       ▼
              ┌─────────────────┐
              │   API Gateway   │  (Port 8000)
              └──────┬──────────┘
                     │
        ┌────────────┴────────────┐
        │                         │
        ▼                         ▼
┌───────────────┐        ┌───────────────┐
│ Auth Service  │        │ Student Service│
│ (Port 8002)   │        │ (Port 8001)   │
└───────────────┘        └───────────────┘
```

---

# **Features**

## **Core Features**
- **API Gateway for centralized request routing**
- **JWT-based authentication and authorization**
- **Secure protected endpoints**
- **Microservices architecture with independent services**
- **Asynchronous service-to-service communication**
- **FastAPI automatic validation and documentation**
- **Scalable and modular design**

## **Security Features**
- **JWT token generation**
- **JWT token validation**
- **Protected routes**
- **Token expiration support**
- **Gateway-level authentication enforcement**

---

# **Technologies Used**

## **Backend**
- **Python 3.10+**
- **FastAPI**
- **Uvicorn**
- **HTTPX**
- **Pydantic**

## **Authentication**
- **JWT (JSON Web Token)**

## **Tools**
- **Git**
- **GitHub**
- **Virtual Environment (venv)**

---

# **Project Structure**

```
microservices-fastapi/
│
├── gateway/
│   ├── main.py
│   ├── middleware.py
│   └── routes/
│
├── auth_service/
│   ├── main.py
│   ├── auth.py
│   └── models.py
│
├── student_service/
│   ├── main.py
│   ├── routes.py
│   └── models.py
│
├── requirements.txt
└── README.md
```

---

# **Installation**

## **Clone the Repository**

```
git clone https://github.com/your-username/microservices-fastapi.git
cd microservices-fastapi
```

---

## **Create Virtual Environment**

```
python -m venv venv
```

---

## **Activate Virtual Environment**

### **Windows**
```
venv\Scripts\activate
```

### **Linux / Mac**
```
source venv/bin/activate
```

---

## **Install Dependencies**

```
pip install -r requirements.txt
```

---

# **Running the Services**

## **Run Authentication Service**
```
cd auth_service
uvicorn main:app --reload --port 8002
```

---

## **Run Student Service**
```
cd student_service
uvicorn main:app --reload --port 8001
```

---

## **Run API Gateway**
```
cd gateway
uvicorn main:app --reload --port 8000
```

---

# **API Documentation**

## **Gateway**
```
http://localhost:8000/docs
```

## **Auth Service**
```
http://localhost:8002/docs
```

## **Student Service**
```
http://localhost:8001/docs
```

---

# **API Usage**

## **Login to Get JWT Token**

```
POST /auth/login
```

**Example**
```
curl -X POST http://localhost:8000/auth/login ^
-H "Content-Type: application/json" ^
-d "{\"username\":\"admin\",\"password\":\"admin\"}"
```

**Response**
```
{
  "access_token": "your_jwt_token",
  "token_type": "bearer"
}
```

---

## **Access Protected Student Endpoint**

```
GET /students/
```

**Example**
```
curl -H "Authorization: Bearer YOUR_TOKEN" ^
http://localhost:8000/students/
```

---

# **Request Flow**

## **Authentication Flow**
1. Client sends login request to API Gateway
2. Gateway forwards request to Auth Service
3. Auth Service validates credentials
4. JWT token returned to client

## **Protected Resource Flow**
1. Client sends request with JWT token
2. Gateway validates JWT token
3. Gateway forwards request to Student Service
4. Student Service returns response
5. Gateway returns response to client

---

# **Security**

## **Authentication**
- JWT-based authentication
- Secure token generation
- Token expiration handling

## **Gateway Protection**
- Centralized authentication enforcement
- Prevents unauthorized access

---

# **Development Commands**

## **Run Gateway**
```
uvicorn main:app --reload --port 8000
```

## **Run Auth Service**
```
uvicorn main:app --reload --port 8002
```

## **Run Student Service**
```
uvicorn main:app --reload --port 8001
```

---

# **Future Improvements**

- Add PostgreSQL database integration
- Add Docker support
- Add Kubernetes deployment
- Add role-based access control
- Add load balancing
- Add production configuration

---


**Author**

Kajanthan Kirubakaran
---



