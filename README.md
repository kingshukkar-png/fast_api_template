# 📝 FastAPI MongoDB To-Do Application

A modern, high-performance, asynchronous RESTful API for task management built with **FastAPI**, **MongoDB**, and **Beanie ODM**. The application implements clean modular architecture with JWT authentication, user isolation, advanced filtering/sorting/pagination, soft deletion, and unified response formats.

---

## 🚀 Features

- **⚡ Asynchronous & Fast**: Powered by [FastAPI](https://fastapi.tiangolo.com/) and [Uvicorn](https://www.uvicorn.org/) with native `async`/`await` support.
- **🔒 Secure Authentication & Authorization**:
  - JWT (JSON Web Tokens) Bearer authentication.
  - Password hashing using `bcrypt` with salt.
  - Dependency injection guards (`get_current_active_user`) to protect private endpoints.
  - User data isolation (users can only access and manage their own todos).
- **📋 Comprehensive Todo Management (CRUD)**:
  - Create new todos with title, description, and status.
  - Retrieve single todo by ID.
  - Full updates (`PUT`) and quick status toggle (`PATCH`).
  - **Soft Deletion**: Preserves records by setting `deleted_at` timestamps instead of hard deletes.
- **🔍 Advanced Querying, Search & Pagination**:
  - Offset-based pagination with comprehensive metadata (`page`, `page_size`, `total`, `total_pages`, `has_next`, `has_previous`).
  - Regex-based full-text search across `title` and `description` (case-insensitive & regex-escaped).
  - Status filtering (`completed=true|false`).
  - Multi-field sorting (`title`, `completed`, `created_at`, `updated_at`) in ascending (`asc`) or descending (`desc`) order.
- **🏛️ Clean Layered Architecture**:
  - Separation of concerns: **Routers / Controllers** ➔ **Services** ➔ **Repositories** ➔ **Beanie Models**.
- **📦 MongoDB & Beanie ODM**:
  - MongoDB integration using `Motor` (Async PyMongo driver).
  - Object Document Mapping (ODM) powered by [Beanie](https://beanie-odm.dev/) with automated index creation.
- **Standardized Response Envelope**: Consistent response contracts for success and error states across all endpoints.
- **🩺 Health Check**: Dedicated ping check verifying server and MongoDB connectivity.
- **📖 Auto-Generated Documentation**: Interactive Swagger UI (`/docs`) and ReDoc (`/redoc`) enabled in development.

---

## 🛠️ Tech Stack

| Technology | Purpose |
| :--- | :--- |
| **Python 3.10+** (tested on 3.14) | Core programming language |
| **FastAPI** | Modern, high-performance web framework |
| **Uvicorn** | Lightning-fast ASGI web server |
| **MongoDB** | NoSQL document database |
| **Beanie ODM** | Asynchronous ODM for MongoDB based on Motor and Pydantic |
| **Pydantic v2 & Pydantic Settings** | Data validation, serialization, and settings management |
| **PyJWT & Bcrypt** | Token generation and secure password hashing |

---

## 📁 Project Structure

```text
To Do APP/
├── app/
│   ├── api/                      # API Layer (Routers & Dependencies)
│   │   ├── deps.py               # Dependency injection (JWT auth verification)
│   │   └── v1/                   # API Version 1 Routers
│   │       ├── auth/             # Authentication endpoints (login, register)
│   │       ├── health/           # Health check endpoint
│   │       ├── todo/             # Todo CRUD endpoints
│   │       ├── user/             # User endpoints
│   │       └── router.py         # Main v1 router aggregator
│   ├── common/                   # Shared schemas, responses & error handlers
│   │   ├── exception.py          # Centralized exception handlers
│   │   ├── list_query_params.py  # Pagination & query parameters logic
│   │   ├── response.py           # Standardized response formatters
│   │   └── schemas.py            # Generic API Response & Error schemas
│   ├── config/                   # Configuration & Environment Settings
│   │   └── settings.py           # Pydantic BaseSettings class
│   ├── db/                       # Database connection management
│   │   └── mongo.py              # MongoManager with async client & ping
│   ├── modules/                  # Business Logic Modules (Domain Layer)
│   │   ├── auth/                 # Auth module (service, schemas, repo)
│   │   ├── todo/                 # Todo module (models, service, repo, schemas)
│   │   └── users/                # User module (models, schemas, repo, service)
│   ├── utils/                    # Utility functions
│   │   └── security.py           # Bcrypt hashing & JWT encode/decode helpers
│   └── main.py                   # Application entry point & lifespan manager
├── .env.example                  # Environment configuration template
├── .gitignore                    # Git ignored files & folders
├── requirements.txt              # Project dependencies
└── README.md                     # Project documentation
```

---

## ⚙️ Configuration & Environment Variables

Create a `.env` file in the root directory by copying `.env.example`:

```bash
cp .env.example .env
```

### Environment Configuration Reference

| Variable | Description | Default Value | Example Value |
| :--- | :--- | :--- | :--- |
| `PORT` | Port number the server listens on | `8000` | `8000` |
| `TITLE` | FastAPI application title | `"FastAPI To-Do App"` | `"FastAPI To-Do App"` |
| `DESCRIPTION` | Application description | `"A simple To-Do application built with FastAPI"` | `"Production To-Do API"` |
| `VERSION` | API version | `"1.0.0"` | `"1.0.0"` |
| `ENVIRONMENT` | Environment (`development` or `production`). In `production`, Swagger `/docs` and `/redoc` are disabled | `"development"` | `development` |
| `MONGODB_URL` | MongoDB connection URI | `"mongodb://localhost:27017"` | `mongodb://localhost:27017` or Atlas URI |
| `DB_NAME` | MongoDB database name | `"todo-app"` | `todo_db` |
| `JWT_SECRET_KEY` | Secret key used for signing JWT tokens | `"your_secret_key"` | `supersecretjwtkey123!` |
| `JWT_ALGORITHM` | JWT signing algorithm | `"HS256"` | `HS256` |
| `JWT_ACCESS_TOKEN_EXPIRE_MINUTES` | Access token lifespan in minutes | `60` | `60` |

---

## 📦 Getting Started

### 1. Prerequisites

- **Python 3.10+** installed
- **MongoDB** running locally or a cloud-hosted MongoDB Atlas URI

*(Optional)* Run MongoDB with Docker:
```bash
docker run -d --name mongodb -p 27017:27017 -e MONGO_INITDB_DATABASE=todo-app mongo:latest
```

---

### 2. Setup Virtual Environment

**On macOS / Linux:**
```bash
python3 -m venv venv
source venv/bin/activate
```

**On Windows:**
```powershell
python -m venv venv
venv\Scripts\activate
```

---

### 3. Install Dependencies

```bash
pip install --upgrade pip
pip install -r requirements.txt
```

---

### 4. Configure Environment

Copy `.env.example` and customize your values:
```bash
cp .env.example .env
```

---

### 5. Run the Server

You can run the server using either the Python module or Uvicorn directly:

**Using Uvicorn:**
```bash
uvicorn app.main:app --host 127.0.0.1 --port 8000 --reload
```

**Using Python:**
```bash
python -m app.main
```

The application will start at: `http://127.0.0.1:8000`

---

## 📖 API Documentation

When `ENVIRONMENT=development`, interactive API documentation is automatically generated:

- **Swagger UI**: [http://127.0.0.1:8000/docs](http://127.0.0.1:8000/docs)
- **ReDoc**: [http://127.0.0.1:8000/redoc](http://127.0.0.1:8000/redoc)
- **OpenAPI Schema**: [http://127.0.0.1:8000/openapi.json](http://127.0.0.1:8000/openapi.json)

---

## 📡 API Endpoints Overview

All v1 routes are prefixed with `/api/v1`.

### 1. Health
| Method | Endpoint | Auth | Description |
| :--- | :--- | :---: | :--- |
| `GET` | `/api/v1/` | ❌ | Checks API status and pings MongoDB |

---

### 2. Authentication
| Method | Endpoint | Auth | Description |
| :--- | :--- | :---: | :--- |
| `POST` | `/api/v1/auth/register` | ❌ | Register a new user account |
| `POST` | `/api/v1/auth/login` | ❌ | Login and receive a JWT Bearer token |

#### Register Request Body:
```json
{
  "first_name": "John",
  "last_name": "Doe",
  "email": "john.doe@example.com",
  "password": "strongpassword123",
  "is_active": true
}
```

#### Login Request Body:
```json
{
  "email": "john.doe@example.com",
  "password": "strongpassword123"
}
```

#### Login Response:
```json
{
  "success": true,
  "data": {
    "access_token": "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9...",
    "token_type": "bearer"
  },
  "message": "Login successful."
}
```

---

### 3. To-Do Management
All todo endpoints require the `Authorization: Bearer <access_token>` header.

| Method | Endpoint | Auth | Description |
| :--- | :--- | :---: | :--- |
| `POST` | `/api/v1/todos/` | ✅ | Create a new todo item |
| `GET` | `/api/v1/todos/` | ✅ | List todos with pagination, search, filter, and sorting |
| `GET` | `/api/v1/todos/{todo_id}` | ✅ | Retrieve a specific todo by ID |
| `PUT` | `/api/v1/todos/{todo_id}` | ✅ | Full update of a todo item |
| `PATCH` | `/api/v1/todos/{todo_id}/completed` | ✅ | Update only the completed status |
| `DELETE` | `/api/v1/todos/{todo_id}` | ✅ | Soft delete a todo item |

---

## 🔍 Query Parameters for Listing Todos

The `GET /api/v1/todos/` endpoint supports flexible querying:

| Parameter | Type | Default | Description |
| :--- | :--- | :--- | :--- |
| `page` | `integer` | `1` | Page number (1-indexed, $\ge 1$) |
| `page_size` | `integer` | `10` | Number of items per page ($\ge 1$) |
| `search` | `string` | `null` | Case-insensitive regex search in `title` and `description` |
| `completed`| `boolean` | `null` | Filter by status: `true` or `false` |
| `sort_by` | `string` | `created_at` | Field to sort by: `title`, `completed`, `created_at`, `updated_at` |
| `sort_order` | `string` | `asc` | Sort direction: `asc` (ascending) or `desc` (descending) |

**Example Query:**
```http
GET /api/v1/todos/?page=1&page_size=5&completed=false&search=meeting&sort_by=created_at&sort_order=desc
```

---

## 📬 Unified Response Structure

All endpoints return a standardized JSON format:

### Success Response
```json
{
  "success": true,
  "data": { ... },
  "message": "Operation description"
}
```

### Paginated List Response Example
```json
{
  "success": true,
  "data": {
    "items": [
      {
        "id": "671fb8a5c2d3e4f5a6b7c8d9",
        "title": "Finish report",
        "user": {
          "id": "671fb890c2d3e4f5a6b7c8d8",
          "first_name": "John",
          "last_name": "Doe",
          "email": "john.doe@example.com"
        },
        "description": "Prepare quarterly financial analysis",
        "completed": false,
        "created_at": "2026-10-29T18:00:00",
        "updated_at": null
      }
    ],
    "total": 1,
    "page": 1,
    "page_size": 10,
    "total_pages": 1,
    "has_next": false,
    "has_previous": false
  },
  "message": "Todos retrieved successfully."
}
```

### Error Response
```json
{
  "success": false,
  "error": "Todo not found."
}
```

---

## 💻 cURL Quickstart Examples

### 1. Register a User
```bash
curl -X POST "http://127.0.0.1:8000/api/v1/auth/register" \
  -H "Content-Type: application/json" \
  -d '{
    "first_name": "Alice",
    "last_name": "Smith",
    "email": "alice@example.com",
    "password": "securepassword123"
  }'
```

### 2. Login to get Access Token
```bash
curl -X POST "http://127.0.0.1:8000/api/v1/auth/login" \
  -H "Content-Type: application/json" \
  -d '{
    "email": "alice@example.com",
    "password": "securepassword123"
  }'
```

### 3. Create a Todo
```bash
curl -X POST "http://127.0.0.1:8000/api/v1/todos/" \
  -H "Content-Type: application/json" \
  -H "Authorization: Bearer <YOUR_ACCESS_TOKEN>" \
  -d '{
    "title": "Buy Groceries",
    "description": "Apples, Milk, Bread, and Coffee",
    "completed": false
  }'
```

### 4. Fetch Paginated Todos with Search
```bash
curl -X GET "http://127.0.0.1:8000/api/v1/todos/?page=1&page_size=10&search=groceries&sort_order=desc" \
  -H "Authorization: Bearer <YOUR_ACCESS_TOKEN>"
```

### 5. Mark Todo as Completed
```bash
curl -X PATCH "http://127.0.0.1:8000/api/v1/todos/<TODO_ID>/completed" \
  -H "Content-Type: application/json" \
  -H "Authorization: Bearer <YOUR_ACCESS_TOKEN>" \
  -d '{
    "completed": true
  }'
```

### 6. Delete a Todo (Soft Delete)
```bash
curl -X DELETE "http://127.0.0.1:8000/api/v1/todos/<TODO_ID>" \
  -H "Authorization: Bearer <YOUR_ACCESS_TOKEN>"
```

---

## 🗄️ Database Schema & Indexing

The application uses **Beanie Document Models** with MongoDB indexes:

### `User` Collection (`users`)
- `id`: Unique identifier (`PydanticObjectId`)
- `first_name`: string
- `last_name`: string
- `email`: string, validated email
- `password`: hashed string
- `is_active`: boolean (default: `True`)
- `created_at`, `updated_at`, `deleted_at`: datetime
- **Index**: Unique index on `email` ascending.

### `Todo` Collection (`todos`)
- `id`: Unique identifier (`PydanticObjectId`)
- `title`: string
- `description`: optional string
- `completed`: boolean (default: `False`)
- `user`: Embedded snapshot model `TodoUser` (`id`, `first_name`, `last_name`, `email`)
- `created_at`, `updated_at`, `deleted_at`: datetime
- **Indexes**:
  - `user.id` ascending (for fast lookup of a user's items)
  - `title` ascending (for quick searching and sorting)

---

## 🔒 Security & Best Practices

1. **Passwords**: Never stored in plain text. Always hashed using `bcrypt.hashpw` with automatically generated salts.
2. **JWT Security**: Protected with configurable expiration (`JWT_ACCESS_TOKEN_EXPIRE_MINUTES`) and cryptographic verification using `PyJWT`.
3. **Multi-Tenancy / Isolation**: Database queries enforce `Todo.user.id == current_user.id`, preventing horizontal privilege escalation.
4. **Soft Deletes**: Deletions mark `deleted_at = datetime.now()`, ensuring audit trails and preventing accidental permanent data loss.
5. **Input Validation**: Pydantic models validate email formats, string lengths, and schema types before data reaches the service layer.

---

## 📄 License

This project is open-source and available under the [MIT License](LICENSE).
