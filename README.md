# Course Enrollment API

A FastAPI-based backend system for managing student course enrollments and grades.

**Deployed Link(backend)**
- https://course-enrollment-api.onrender.com

**Note**  
GET / is not defined, so the homepage shows “Not found”. Use endpoints like /students or /courses.

**Database Hosting Note:**  
Render gives only one free PostgreSQL instance and it expires quickly.  
My other project already uses that free database, so this backend uses PostgreSQL from Neon for a stable connection.

## Tech Stack

- **FastAPI**: Modern web framework for building APIs
- **SQLAlchemy**: ORM for database operations
- **Pydantic**: Data validation and serialization
- **PostgreSQL**: Relational database
- **uvicorn**: ASGI server
- **psycopg2-binary**: PostgreSQL driver
- **Python 3.11**: Programming language

## Project Architecture

This project follows a layered architecture pattern:

```
Router Layer (API endpoints)
    ↓
Service Layer (Business logic & validation)
    ↓
Repository Layer (Database queries)
    ↓
Database (PostgreSQL)
```

### Folder Structure

```
course-enrollment-api/
├── app/
│   ├── main.py                          # FastAPI app initialization
│   ├── database.py                      # Database connection setup
│   ├── models.py                        # SQLAlchemy ORM models
│   ├── schemas.py                       # Pydantic schemas
│   ├── routers/                         # API route handlers
│   │   ├── students_router.py
│   │   ├── courses_router.py
│   │   ├── enrollments_router.py
│   │   └── grades_router.py
│   ├── services/                        # Business logic layer
│   │   ├── students_service.py
│   │   ├── courses_service.py
│   │   ├── enrollments_service.py
│   │   └── grades_service.py
│   └── repositories/                    # Database query layer
│       ├── students_repository.py
│       ├── courses_repository.py
│       ├── enrollments_repository.py
│       └── grades_repository.py
├── screenshots/                         # Postman API screenshots
├── .env                                 # Environment variables
├── .gitignore
├── requirements.txt
└── README.md
```

## Database Schema

### Students Table
- `id`: Primary key (auto-increment)
- `name`: Student's full name
- `email`: Unique email address

### Courses Table
- `id`: Primary key (auto-increment)
- `course_name`: Full course name
- `course_code`: Unique course identifier
- `credits`: Number of credits

### Enrollments Table
- `id`: Primary key (auto-increment)
- `student_id`: Foreign key to students
- `course_id`: Foreign key to courses
- `enrollment_date`: Date of enrollment

### Grades Table
- `id`: Primary key (auto-increment)
- `enrollment_id`: Foreign key to enrollments
- `marks`: Numerical marks (0-100)
- `final_grade`: Letter grade (A, B, C, D, F)

## Setup Instructions

### 1. Clone the Repository

```bash
git clone https://github.com/nexpectArpit/course-enrollment-api.git
cd course-enrollment-api
```

### 2. Create Virtual Environment

```bash
python3.12 -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate
```

### 3. Install Dependencies

```bash
pip install -r requirements.txt
```

### 4. Configure Database

Create a `.env` file in the project root:

```env
# Production (Neon)
DATABASE_URL=your_neon_postgres_url

# Local development
# DATABASE_URL=postgresql://username:password@localhost:5432/course_enrollment_db
```
**Note**: Replace `username` and `password` with your PostgreSQL credentials.

Create the database:

```bash
psql -U your_username -c "CREATE DATABASE course_enrollment_db;"
```

### 5. Run the Server

```bash
uvicorn app.main:app --reload
```

The API will be available at: `http://localhost:8000`

### 6. Access API Documentation

FastAPI provides automatic interactive documentation:

- **Swagger UI**: http://localhost:8000/docs
- **ReDoc**: http://localhost:8000/redoc

### Deploy on Render

Add Environment Variables:
- DATABASE_URL = your_neon_postgres_url
- PYTHON_VERSION = 3.11.9

Start Command:
```bash
uvicorn app.main:app --host 0.0.0.0 --port $PORT
```

## API Endpoints

### Students

| Method | Endpoint | Description |
|--------|----------|-------------|
| POST | `/students/` | Create a new student |
| GET | `/students/` | Get all students |
| GET | `/students/{id}` | Get student by ID |
| PUT | `/students/{id}` | Update student |
| DELETE | `/students/{id}` | Delete student |

### Courses

| Method | Endpoint | Description |
|--------|----------|-------------|
| POST | `/courses/` | Create a new course |
| GET | `/courses/` | Get all courses |
| GET | `/courses/{id}` | Get course by ID |
| PUT | `/courses/{id}` | Update course |
| DELETE | `/courses/{id}` | Delete course |

### Enrollments

| Method | Endpoint | Description |
|--------|----------|-------------|
| POST | `/enrollments/` | Enroll student in course |
| GET | `/enrollments/` | Get all enrollments |
| GET | `/enrollments/{id}` | Get enrollment by ID |
| GET | `/enrollments/student/{id}` | Get student's enrollments |
| GET | `/enrollments/course/{id}` | Get course enrollments |
| DELETE | `/enrollments/{id}` | Delete enrollment |

### Grades

| Method | Endpoint | Description |
|--------|----------|-------------|
| POST | `/grades/` | Create grade for enrollment |
| GET | `/grades/` | Get all grades |
| GET | `/grades/{id}` | Get grade by ID |
| GET | `/grades/enrollment/{id}` | Get grade by enrollment |
| PUT | `/grades/{id}` | Update grade |
| DELETE | `/grades/{id}` | Delete grade |

## Request/Response Examples

### Create Student

**Request:**
```bash
curl -X POST http://localhost:8000/students/ \
  -H "Content-Type: application/json" \
  -d '{
    "name": "John Doe",
    "email": "john@example.com"
  }'
```

**Response:**
```json
{
  "id": 1,
  "name": "John Doe",
  "email": "john@example.com"
}
```

### Create Course

**Request:**
```bash
curl -X POST http://localhost:8000/courses/ \
  -H "Content-Type: application/json" \
  -d '{
    "course_name": "Data Structures",
    "course_code": "CS101",
    "credits": 4
  }'
```

**Response:**
```json
{
  "id": 1,
  "course_name": "Data Structures",
  "course_code": "CS101",
  "credits": 4
}
```

### Create Enrollment

**Request:**
```bash
curl -X POST http://localhost:8000/enrollments/ \
  -H "Content-Type: application/json" \
  -d '{
    "student_id": 1,
    "course_id": 1,
    "enrollment_date": "2024-01-15"
  }'
```

**Response:**
```json
{
  "id": 1,
  "student_id": 1,
  "course_id": 1,
  "enrollment_date": "2024-01-15"
}
```

### Create Grade

**Request:**
```bash
curl -X POST http://localhost:8000/grades/ \
  -H "Content-Type: application/json" \
  -d '{
    "enrollment_id": 1,
    "marks": 95
  }'
```

**Response:**
```json
{
  "id": 1,
  "enrollment_id": 1,
  "marks": 95.0,
  "final_grade": "A"
}
```

## Grade Calculation

The system automatically calculates letter grades based on marks:

| Marks Range | Letter Grade |
|-------------|--------------|
| 90 - 100 | A |
| 80 - 89 | B |
| 70 - 79 | C |
| 60 - 69 | D |
| 0 - 59 | F |

## Business Rules

### Students
- Email must be unique
- Email format is validated

### Courses
- Course code must be unique
- Credits must be a positive integer

### Enrollments
- Student must exist
- Course must exist
- One student can only enroll in a course once (no duplicates)

### Grades
- Enrollment must exist
- Marks must be between 0 and 100
- One grade per enrollment (no duplicates)
- Final grade is automatically calculated

## Demo Script for Evaluation

Follow these steps to demonstrate the complete API functionality:

### Step 1: Create Students

```bash
# Create first student
curl -X POST http://localhost:8000/students/ \
  -H "Content-Type: application/json" \
  -d '{"name": "Alice Johnson", "email": "alice@example.com"}'

# Create second student
curl -X POST http://localhost:8000/students/ \
  -H "Content-Type: application/json" \
  -d '{"name": "Bob Smith", "email": "bob@example.com"}'
```

### Step 2: Create Courses

```bash
# Create first course
curl -X POST http://localhost:8000/courses/ \
  -H "Content-Type: application/json" \
  -d '{"course_name": "Data Structures", "course_code": "CS101", "credits": 4}'

# Create second course
curl -X POST http://localhost:8000/courses/ \
  -H "Content-Type: application/json" \
  -d '{"course_name": "Database Systems", "course_code": "CS201", "credits": 3}'
```

### Step 3: Enroll Students

```bash
# Enroll Alice in CS101
curl -X POST http://localhost:8000/enrollments/ \
  -H "Content-Type: application/json" \
  -d '{"student_id": 1, "course_id": 1, "enrollment_date": "2024-01-15"}'

# Enroll Bob in CS101
curl -X POST http://localhost:8000/enrollments/ \
  -H "Content-Type: application/json" \
  -d '{"student_id": 2, "course_id": 1, "enrollment_date": "2024-01-15"}'

# Enroll Alice in CS201
curl -X POST http://localhost:8000/enrollments/ \
  -H "Content-Type: application/json" \
  -d '{"student_id": 1, "course_id": 2, "enrollment_date": "2024-01-20"}'
```

### Step 4: Add Grades

```bash
# Grade for Alice in CS101 (95 marks = A)
curl -X POST http://localhost:8000/grades/ \
  -H "Content-Type: application/json" \
  -d '{"enrollment_id": 1, "marks": 95}'

# Grade for Bob in CS101 (75 marks = C)
curl -X POST http://localhost:8000/grades/ \
  -H "Content-Type: application/json" \
  -d '{"enrollment_id": 2, "marks": 75}'

# Grade for Alice in CS201 (88 marks = B)
curl -X POST http://localhost:8000/grades/ \
  -H "Content-Type: application/json" \
  -d '{"enrollment_id": 3, "marks": 88}'
```

### Step 5: Query Data

```bash
# Get all students
curl http://localhost:8000/students/

# Get Alice's enrollments
curl http://localhost:8000/enrollments/student/1

# Get CS101 enrollments (class roster)
curl http://localhost:8000/enrollments/course/1

# Get all grades
curl http://localhost:8000/grades/
```

### Step 6: Update Grade

```bash
# Update Bob's grade from 75 to 85 (C to B)
curl -X PUT http://localhost:8000/grades/2 \
  -H "Content-Type: application/json" \
  -d '{"marks": 85}'
```

## Testing with Postman

### Setup Postman Collection

1. Open Postman
2. Create a new collection named "Course Enrollment API"
3. Add requests for each endpoint
4. Set base URL: `http://localhost:8000`

### Taking Screenshots

1. Execute each request in Postman
2. Take screenshots showing:
   - Request details (method, URL, body)
   - Response (status code, body)
3. Save screenshots in the `screenshots/` folder with descriptive names:
   - `01-create-student.png`
   - `02-get-students.png`
   - `03-create-course.png`
   - etc.

### Adding Screenshots to README

Place screenshots in the `screenshots/` folder and reference them:

```markdown
![Create Student](screenshots/01-create-student.png)
```

## Features Implemented

✅ Complete CRUD operations for Students  
✅ Complete CRUD operations for Courses  
✅ Enrollment management with validation  
✅ Automatic grade calculation (A-F)  
✅ Duplicate prevention (emails, course codes, enrollments)  
✅ Foreign key validation  
✅ Marks validation (0-100 range)  
✅ Comprehensive error handling  
✅ Interactive API documentation (Swagger UI)  
✅ Layered architecture (Router → Service → Repository)  
✅ Database relationships (One-to-Many, Many-to-Many)  

## Development Notes

### Code Organization

- **Routers**: Handle HTTP requests/responses
- **Services**: Contain business logic and validation
- **Repositories**: Execute database queries
- **Models**: Define database schema
- **Schemas**: Define request/response formats

### Error Handling

The API returns appropriate HTTP status codes:
- `200`: Success
- `201`: Created
- `400`: Bad Request (validation error)
- `404`: Not Found
- `500`: Internal Server Error

## Future Enhancements

Potential features for future development:
- User authentication and authorization
- Soft delete functionality
- Audit logging
- Email notifications
- Report generation
- Bulk operations
- Advanced filtering and search
- Docker containerization
- Database migrations with Alembic

## Author

Arpit Tripathi

## License

This project is for educational purposes (OJT Project).
