# Student Diary System - Backend

A FastAPI-based backend for managing student diaries and marks with secure parent share links.

## 🏗️ Architecture

### Database Schema (PostgreSQL)

**3 Tables:**
- `students` - Student information
- `diary_entries` - Daily diary entries (homework, classwork, attendance, remarks)
- `marks` - Test marks per subject

**Key Features:**
- Fully normalized (3NF)
- UUID primary keys
- Cascade deletes
- Unique share keys for parent access
- Unique constraint on student + date for diary entries

### Tech Stack

- **FastAPI** - Modern async web framework
- **SQLAlchemy** - ORM with relationship management
- **Alembic** - Database migrations
- **Pydantic** - Data validation
- **PostgreSQL** - Production database (Supabase)

## 📁 Project Structure

```
backend/
├── app/
│   ├── __init__.py
│   ├── config.py          # Settings management
│   ├── database.py        # DB connection & session
│   ├── models.py          # SQLAlchemy models
│   ├── schemas.py         # Pydantic schemas
│   ├── utils.py           # Helper functions
│   └── routers/
│       ├── admin.py       # Admin CRUD endpoints
│       └── public.py      # Public share endpoints
├── alembic/               # Database migrations
├── main.py                # FastAPI app entry point
├── requirements.txt       # Python dependencies
└── .env                   # Environment variables
```

## 🚀 Setup Instructions

### 1. Install Dependencies

```bash
pip install -r requirements.txt
```

### 2. Environment Configuration

The `.env` file is already configured with your Supabase PostgreSQL URL.

### 3. Run Migrations

```bash
# Generate migration (already done)
alembic revision --autogenerate -m "migration message"

# Apply migration to database
alembic upgrade head
```

### 4. Start the Server

```bash
uvicorn main:app --reload --host 0.0.0.0 --port 8000
```

## 📚 API Endpoints

### Admin Endpoints (Protected)

**Students:**
- `POST /api/admin/students` - Create student
- `GET /api/admin/students` - List students
- `GET /api/admin/students/{id}` - Get student
- `PUT /api/admin/students/{id}` - Update student
- `DELETE /api/admin/students/{id}` - Delete student

**Diary Entries:**
- `POST /api/admin/diary-entries` - Create diary entry
- `GET /api/admin/diary-entries?student_id={id}` - List entries
- `GET /api/admin/diary-entries/{id}` - Get entry
- `PUT /api/admin/diary-entries/{id}` - Update entry
- `DELETE /api/admin/diary-entries/{id}` - Delete entry

**Marks:**
- `POST /api/admin/marks` - Create mark
- `GET /api/admin/marks?student_id={id}` - List marks
- `GET /api/admin/marks/{id}` - Get mark
- `PUT /api/admin/marks/{id}` - Update mark
- `DELETE /api/admin/marks/{id}` - Delete mark

### Public Endpoints (For Parents)

- `GET /api/share/diary/{share_key}` - View diary entry via share link
- `GET /api/share/marks/{share_key}` - View marks via share link

## 🔑 Share Key System

Each diary entry and mark record gets a unique `share_key` generated automatically. Parents can access records via:

```
https://your-domain.com/api/share/diary/{share_key}
https://your-domain.com/api/share/marks/{share_key}
```

**No authentication required** for share links - perfect for parents!

## 📖 API Documentation

Once the server is running, visit:
- **Swagger UI:** http://localhost:8000/docs
- **ReDoc:** http://localhost:8000/redoc

## 🧪 Example Usage

### Create a Student

```bash
curl -X POST "http://localhost:8000/api/admin/students" \
  -H "Content-Type: application/json" \
  -d '{
    "name": "John Doe",
    "class_name": "10",
    "section": "A",
    "roll_no": 15
  }'
```

### Create a Diary Entry

```bash
curl -X POST "http://localhost:8000/api/admin/diary-entries" \
  -H "Content-Type: application/json" \
  -d '{
    "student_id": "uuid-here",
    "entry_date": "2025-12-01",
    "homework": "Math: Chapter 5, Science: Lab report",
    "classwork": "Completed exercises 1-10",
    "attendance": "Present",
    "remarks": "Good participation"
  }'
```

Response includes `share_key` for parent access!

## 🔄 Database Migrations

```bash
# Create new migration after model changes
alembic revision --autogenerate -m "description"

# Apply migrations
alembic upgrade head

# Rollback one version
alembic downgrade -1

# View migration history
alembic history
```

## 🛡️ Production Considerations

1. **Add Authentication** - Implement JWT for admin endpoints
2. **CORS Configuration** - Update allowed origins in `main.py`
3. **Rate Limiting** - Add rate limiting for public endpoints
4. **Logging** - Implement structured logging
5. **Error Handling** - Add global exception handlers
6. **Validation** - Add more robust input validation

## 📝 Notes

- Database uses UUID for all primary keys
- Automatic timestamp tracking with `created_at`
- Cascade deletes: removing a student removes all their entries/marks
- Share keys are cryptographically secure (16 characters)
- Connection pooling configured for production use
