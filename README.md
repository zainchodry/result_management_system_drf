# 🎓 Result Management System — Django REST Framework

<div align="center">

![Django](https://img.shields.io/badge/Django-5.2-092E20?style=for-the-badge&logo=django&logoColor=white)
![DRF](https://img.shields.io/badge/DRF-3.15-ff1709?style=for-the-badge&logo=django&logoColor=white)
![PostgreSQL](https://img.shields.io/badge/PostgreSQL-14+-336791?style=for-the-badge&logo=postgresql&logoColor=white)
![Celery](https://img.shields.io/badge/Celery-5.4-37814a?style=for-the-badge&logo=celery&logoColor=white)
![Redis](https://img.shields.io/badge/Redis-7.0-DC382D?style=for-the-badge&logo=redis&logoColor=white)
![License](https://img.shields.io/badge/License-MIT-blue?style=for-the-badge)

**A production-ready REST API for managing university academic results, built with Django REST Framework.**  
Supports role-based access for Admins, Teachers, and Students with JWT authentication, OTP email verification, automated grade calculation, and Swagger documentation.

</div>

---

## 📑 Table of Contents

- [Features](#-features)
- [System Architecture](#-system-architecture)
- [Tech Stack](#-tech-stack)
- [API Endpoints](#-api-endpoints)
- [Project Structure](#-project-structure)
- [Prerequisites](#-prerequisites)
- [Installation & Setup](#-installation--setup)
- [Environment Variables](#-environment-variables)
- [Running the Project](#-running-the-project)
- [API Documentation](#-api-documentation)
- [Role-Based Access Control](#-role-based-access-control)
- [Grade Scale Configuration](#-grade-scale-configuration)
- [Deployment](#-deployment)
- [Contributing](#-contributing)

---

## ✨ Features

### 🔐 Authentication & Security
- **JWT Authentication** with access & refresh tokens (via `djangorestframework-simplejwt`)
- **Token Blacklisting** on logout for security
- **OTP Email Verification** — users must verify email before login
- **OTP-based Password Reset** flow (Forgot → Verify OTP → Reset)
- **Temporary Password** system — admin-created accounts must change password on first login
- **Rate Throttling** — 100 req/hour (anon), 1000 req/hour (authenticated)
- **CORS** support for frontend integration

### 👥 Role-Based Access Control
- **ADMIN** — Full system access: create users, manage academics, publish results
- **TEACHER** — Upload results for assigned courses
- **STUDENT** — View own results, transcript, merit list

### 🏛️ Academic Management
- Departments, Programs, Semesters, Courses
- Teacher-to-Course assignment with session tracking
- Semester course enrollment

### 📊 Result Management
- Teacher uploads marks per course per student
- **Automatic Grade Calculation** from configurable grade scales
- **Automatic GPA/CGPA Calculation** using credit-hour weighted average
- Result **locking** (prevents edits) and **publishing** (makes visible to students)
- Full **transcript** endpoint for students
- **Merit list** ordered by CGPA

### 📧 Async Email (Celery + Redis)
- OTP delivery emails (verification & reset)
- Account credentials email for newly created students/teachers

### 🧾 API Documentation
- Interactive **Swagger UI** at `/api/docs/`
- **ReDoc** at `/api/redoc/`
- Machine-readable schema at `/api/schema/`

### 🛡️ Production-Ready
- `python-decouple` — all secrets in `.env`, never in code
- `whitenoise` — static file serving
- Configurable `ALLOWED_HOSTS`, `CORS_ALLOWED_ORIGINS`
- Full `Django admin` panel with all models registered

---

## 🏗️ System Architecture

```
┌─────────────────────────────────────────────────────────────┐
│                     Client (Frontend / Postman)             │
└──────────────────────────┬──────────────────────────────────┘
                           │ HTTPS + JWT Bearer Token
                           ▼
┌─────────────────────────────────────────────────────────────┐
│                   Django REST Framework API                  │
│                                                             │
│  ┌─────────────┐  ┌──────────────┐  ┌────────────────────┐ │
│  │  accounts   │  │   students   │  │      teachers      │ │
│  │  (Auth/JWT) │  │  (CRUD+CGPA) │  │  (CRUD+Courses)    │ │
│  └─────────────┘  └──────────────┘  └────────────────────┘ │
│  ┌─────────────┐  ┌──────────────┐                         │
│  │  academics  │  │   results    │                         │
│  │  (Dept/Prog │  │ (Grades/GPA) │                         │
│  │  /Semester) │  │              │                         │
│  └─────────────┘  └──────────────┘                         │
└──────────────────────────┬──────────────────────────────────┘
                           │
              ┌────────────┴────────────┐
              ▼                         ▼
     ┌─────────────────┐      ┌──────────────────┐
     │   PostgreSQL DB │      │  Redis + Celery  │
     │  (primary data) │      │  (async emails)  │
     └─────────────────┘      └──────────────────┘
```

---

## 🛠️ Tech Stack

| Component | Technology |
|-----------|-----------|
| Backend Framework | Django 5.2 |
| REST API | Django REST Framework 3.15 |
| Authentication | JWT (`djangorestframework-simplejwt`) |
| Database | PostgreSQL |
| Task Queue | Celery 5.4 |
| Message Broker | Redis 7.0 |
| API Docs | drf-spectacular (Swagger / ReDoc) |
| CORS | django-cors-headers |
| Static Files | WhiteNoise |
| Environment Config | python-decouple |
| Image Handling | Pillow |
| WSGI Server | Gunicorn (production) |

---

## 📡 API Endpoints

### Auth (`/api/accounts/`)

| Method | Endpoint | Description | Auth Required |
|--------|----------|-------------|:---:|
| `POST` | `/register` | Register new user account | ❌ |
| `POST` | `/login` | Login and get JWT tokens | ❌ |
| `POST` | `/logout/` | Blacklist refresh token | ✅ |
| `POST` | `/verify-email/` | Verify account via OTP | ❌ |
| `POST` | `/forget-password/` | Request password reset OTP | ❌ |
| `POST` | `/verify-reset-otp/` | Verify reset OTP | ❌ |
| `POST` | `/reset-password/` | Reset password with OTP | ❌ |
| `POST` | `/change-password/` | Change logged-in user's password | ✅ |
| `GET` | `/profile/` | Get own profile | ✅ |
| `PUT` | `/profile/` | Update own profile | ✅ |

### Students (`/api/students/`)

| Method | Endpoint | Description | Role |
|--------|----------|-------------|------|
| `GET` | `/` | List all students | Admin |
| `POST` | `/create/` | Create student (auto-generates credentials) | Admin |
| `GET` | `/{id}/` | Get student detail | Admin |
| `PUT/PATCH` | `/{id}/` | Update student | Admin |
| `DELETE` | `/{id}/` | Delete student | Admin |
| `GET` | `/search/?roll_number=X` | Search student by roll number | Public |
| `GET` | `/dashboard/` | Student's own dashboard | Student |

### Teachers (`/api/teachers/`)

| Method | Endpoint | Description | Role |
|--------|----------|-------------|------|
| `GET` | `/` | List all teachers | Admin |
| `POST` | `/create/` | Create teacher (auto-generates credentials) | Admin |
| `GET` | `/{id}/` | Get teacher detail | Admin |
| `GET` | `/dashboard/` | Teacher's own dashboard | Teacher |
| `GET` | `/assigned-courses/` | Courses assigned to teacher | Teacher |

### Academics (`/api/academics/`)

| Method | Endpoint | Description | Role |
|--------|----------|-------------|------|
| `GET/POST` | `/departments/` | List / Create departments | Admin |
| `GET/POST` | `/programs/` | List / Create programs | Admin |
| `GET/POST` | `/semesters/` | List / Create semesters | Admin |
| `GET/POST` | `/courses/` | List / Create courses | Admin |
| `GET/POST` | `/teacher-assignments/` | List / Create teacher-course assignments | Admin |

### Results (`/api/results/`)

| Method | Endpoint | Description | Role |
|--------|----------|-------------|------|
| `POST` | `/upload/` | Upload marks for a student/course | Teacher |
| `GET` | `/search/?roll_number=X` | Get published results by roll number | Public |
| `GET` | `/transcript/` | Get own full transcript | Student |
| `GET` | `/merit-list/` | Get CGPA merit list | Public |
| `POST` | `/publish/{semester_id}/` | Publish semester results | Admin |
| `POST` | `/lock/{semester_id}/` | Lock semester results | Admin |
| `GET` | `/student/{student_id}/` | Get a student's full result summary | Admin/Teacher |

### Token (`/api/`)

| Method | Endpoint | Description |
|--------|----------|-------------|
| `POST` | `/token/refresh/` | Refresh access token |

---

## 📁 Project Structure

```
result_management_system_drf/
│
├── config/                    # Django project configuration
│   ├── settings.py            # Production-ready settings (uses .env)
│   ├── urls.py                # Root URL configuration + Swagger
│   ├── celery.py              # Celery app configuration
│   ├── wsgi.py
│   └── asgi.py
│
├── accounts/                  # User auth, JWT, OTP, profiles
│   ├── models.py              # User, PasswordResetOtp, Profile
│   ├── serializers.py         # Register, Login, OTP, Password, Profile
│   ├── views.py               # Auth API views
│   ├── urls.py                # Auth URL patterns
│   ├── tasks.py               # Celery async email tasks
│   ├── utils.py               # OTP generation, JWT helper
│   ├── signals.py             # Auto-create Profile on User save
│   └── admin.py
│
├── academics/                 # Academic structure
│   ├── models.py              # Department, Program, Semester, Course, etc.
│   ├── serializers.py
│   ├── views.py               # ModelViewSet-based views
│   ├── urls.py
│   ├── permissions.py
│   └── admin.py
│
├── students/                  # Student management
│   ├── models.py              # Student (with CGPA), Documents, History
│   ├── serializers.py
│   ├── views.py
│   ├── urls.py
│   ├── services.py            # create_student with auto roll/reg number
│   ├── permissions.py
│   └── admin.py
│
├── teachers/                  # Teacher management
│   ├── models.py              # Teacher, Qualifications, Documents
│   ├── serializers.py
│   ├── views.py
│   ├── urls.py
│   ├── services.py            # create_teacher with auto employee ID
│   └── admin.py
│
├── results/                   # Result management core
│   ├── models.py              # GradeScale, SemesterResult, ResultItem
│   ├── serializers.py
│   ├── views.py               # Upload, Transcript, Merit, Publish, Lock
│   ├── urls.py
│   ├── services.py            # Grade/GPA/CGPA calculation
│   ├── permissions.py
│   └── admin.py
│
├── manage.py
├── requirements.txt
├── .env.example               # Environment variable template
└── README.md
```

---

## ✅ Prerequisites

Ensure you have the following installed:

- **Python** 3.11+
- **PostgreSQL** 14+
- **Redis** 7.0+
- **pip** (Python package manager)

---

## 🚀 Installation & Setup

### 1. Clone the Repository

```bash
git clone https://github.com/yourusername/result_management_system_drf.git
cd result_management_system_drf
```

### 2. Create & Activate Virtual Environment

```bash
python -m venv venv
source venv/bin/activate        # Linux/macOS
# venv\Scripts\activate.bat    # Windows
```

### 3. Install Dependencies

```bash
pip install -r requirements.txt
```

### 4. Configure Environment Variables

```bash
cp .env.example .env
```

Edit `.env` with your actual values (see [Environment Variables](#-environment-variables) below).

### 5. Set Up PostgreSQL Database

```bash
# Connect to PostgreSQL
psql -U postgres

# Create database and user
CREATE DATABASE result_management;
CREATE USER myuser WITH PASSWORD 'mypassword';
GRANT ALL PRIVILEGES ON DATABASE result_management TO myuser;
\q
```

### 6. Run Migrations

```bash
python manage.py migrate
```

### 7. Create Superuser (Admin)

```bash
python manage.py createsuperuser
```

> **Note:** After creating the superuser, you must set the role to `ADMIN` in the Django admin panel (`/admin/`), or do it via shell:
> ```bash
> python manage.py shell -c "from accounts.models import User; u = User.objects.get(email='your@email.com'); u.role = 'ADMIN'; u.is_verified = True; u.must_change_password = False; u.save()"
> ```

### 8. Configure Grade Scales

After logging into Django Admin (`/admin/`), go to **Results → Grade Scales** and add your institution's grading policy, for example:

| Grade | Min % | Max % | Grade Points |
|-------|-------|-------|:---:|
| A+ | 90 | 100 | 4.00 |
| A  | 85 | 89  | 4.00 |
| A- | 80 | 84  | 3.70 |
| B+ | 75 | 79  | 3.30 |
| B  | 70 | 74  | 3.00 |
| B- | 65 | 69  | 2.70 |
| C+ | 60 | 64  | 2.30 |
| C  | 55 | 59  | 2.00 |
| D  | 50 | 54  | 1.00 |
| F  | 0  | 49  | 0.00 |

---

## 🔑 Environment Variables

| Variable | Description | Default |
|----------|-------------|---------|
| `SECRET_KEY` | Django secret key (**change in production!**) | `django-insecure-...` |
| `DEBUG` | Debug mode (`True`/`False`) | `False` |
| `ALLOWED_HOSTS` | Comma-separated allowed hostnames | `127.0.0.1,localhost` |
| `DB_NAME` | PostgreSQL database name | `result_management` |
| `DB_USER` | PostgreSQL username | `myuser` |
| `DB_PASSWORD` | PostgreSQL password | `mypassword` |
| `DB_HOST` | PostgreSQL host | `localhost` |
| `DB_PORT` | PostgreSQL port | `5432` |
| `JWT_ACCESS_LIFETIME_MINUTES` | JWT access token lifetime in minutes | `60` |
| `JWT_REFRESH_LIFETIME_DAYS` | JWT refresh token lifetime in days | `7` |
| `EMAIL_HOST_USER` | Gmail address for sending emails | _(empty)_ |
| `EMAIL_HOST_PASSWORD` | Gmail App Password | _(empty)_ |
| `CELERY_BROKER_URL` | Redis URL for Celery broker | `redis://localhost:6379/0` |
| `CELERY_RESULT_BACKEND` | Redis URL for Celery results | `redis://localhost:6379/0` |
| `CORS_ALLOWED_ORIGINS` | Comma-separated frontend origins | `http://localhost:3000` |

> **Gmail App Password:** Go to your Google Account → Security → 2-Step Verification → App Passwords → Generate one for "Mail".

---

## ▶️ Running the Project

### Development Server

```bash
python manage.py runserver
```

### Celery Worker (in a separate terminal)

```bash
# Make sure Redis is running first
redis-server

# Start Celery worker
celery -A config worker --loglevel=info
```

### Celery Beat (optional — for periodic tasks)

```bash
celery -A config beat --loglevel=info
```

---

## 📖 API Documentation

Once the server is running, visit:

| URL | Description |
|-----|-------------|
| `http://localhost:8000/api/docs/` | **Swagger UI** (interactive API explorer) |
| `http://localhost:8000/api/redoc/` | **ReDoc** (clean API reference) |
| `http://localhost:8000/api/schema/` | OpenAPI JSON schema |
| `http://localhost:8000/admin/` | Django Admin panel |

---

## 🔒 Role-Based Access Control

| Feature | Admin | Teacher | Student | Public |
|---------|:-----:|:-------:|:-------:|:------:|
| Register/Login/OTP | ✅ | ✅ | ✅ | ✅ |
| Create Student | ✅ | ❌ | ❌ | ❌ |
| Create Teacher | ✅ | ❌ | ❌ | ❌ |
| Manage Academics | ✅ | ❌ | ❌ | ❌ |
| Upload Results | ❌ | ✅ | ❌ | ❌ |
| Publish/Lock Results | ✅ | ❌ | ❌ | ❌ |
| View Own Transcript | ❌ | ❌ | ✅ | ❌ |
| Merit List | ✅ | ✅ | ✅ | ✅ |
| Search Results | ✅ | ✅ | ✅ | ✅ |

---

## 📊 Grade Scale Configuration

The system automatically calculates grades, GPA, and CGPA based on the `GradeScale` records you configure in the admin panel.

**GPA Formula:**
```
GPA = Σ(grade_points × credit_hours) / Σ(credit_hours)
```

**CGPA Formula:**
```
CGPA = Average GPA across all completed semesters
```

---

## 🌐 Deployment

### Using Gunicorn + Nginx

```bash
# Collect static files
python manage.py collectstatic --noinput

# Start Gunicorn
gunicorn config.wsgi:application \
    --bind 0.0.0.0:8000 \
    --workers 4 \
    --timeout 120
```

### Production Checklist

- [ ] Set `DEBUG=False` in `.env`
- [ ] Set a strong random `SECRET_KEY` in `.env`
- [ ] Set `ALLOWED_HOSTS` to your domain
- [ ] Run `python manage.py collectstatic`
- [ ] Configure Nginx to serve static/media files
- [ ] Set up SSL/HTTPS (Let's Encrypt / Certbot)
- [ ] Configure `SECURE_SSL_REDIRECT=True`, `SECURE_HSTS_SECONDS=31536000`
- [ ] Start Celery worker as a system service (e.g., `systemd`)
- [ ] Use a process manager like `Supervisor` or `systemd` for Gunicorn

### Docker Compose (Optional)

You can containerize this application using Docker Compose with services for `web`, `postgres`, `redis`, and `celery`. A `Dockerfile` and `docker-compose.yml` can be added on request.

---

## 🤝 Contributing

1. Fork the repository
2. Create your feature branch: `git checkout -b feature/your-feature`
3. Commit your changes: `git commit -m "feat: add your feature"`
4. Push to the branch: `git push origin feature/your-feature`
5. Open a Pull Request

---

## 📄 License

This project is licensed under the MIT License. See the [LICENSE](LICENSE) file for details.

---

<div align="center">
  Built with ❤️ using Django REST Framework
</div>
