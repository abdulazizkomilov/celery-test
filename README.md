README = """
# 🛰️ Celery-Enabled Django Project

This is a Django-based project with powerful asynchronous task processing using **Celery**, **Redis**, and **Celery Beat**. It includes a role-based user system with support for manager onboarding, task queues, scheduled tasks, and task monitoring with **Flower**.

## 🚀 Tech Stack

- **Django** – Backend web framework
- **Celery** – Distributed task queue
- **Redis** – Celery message broker
- **Celery Beat** – Periodic task scheduler
- **Flower** – Celery monitoring tool
- **PostgreSQL** – Default database (configurable)
- **DRF (Django Rest Framework)** – API development
- **Makefile** – Easy command execution

## 📦 Project Features

### 🔐 User Management
- Custom `User` model with roles: `admin`, `manager`, `user`
- API endpoint to create `manager` accounts with one-time passwords
- CSV export functionality for manager users with reset URLs

### ⏱️ Task Scheduling
- Queue-based task execution (`default`, `sms_queue`)
- Scheduled processing of tasks using `Celery Beat`
- Persistent JSON-based mock SMS output simulation

### 📊 Monitoring
- Celery task monitoring with Flower on port `5555`
- Basic HTTP authentication for Flower

## 🧪 Setup & Usage

### 1. Clone and Install

```bash
git clone git@github.com:<your_username>/celery-test.git
cd celery-test
python3 -m venv venv
source venv/bin/activate
pip install -r requirements.txt
```

### 2. Environment Configuration

Ensure you have the following `.env` or config variables set (example):

```bash
DJANGO_SECRET_KEY=your-secret
DEBUG=True
ALLOWED_HOSTS=*
REDIS_URL=redis://localhost:6379/0
```

### 3. Database Setup

```bash
make make     # runs makemigrations
make migrate  # applies migrations
make create   # creates superuser
```

### 4. Running the Application

```bash
make run
```

## 🎯 Celery Workers & Tasks

### Start Default Worker

```bash
make worker
```

### Start SMS Worker

```bash
make worker-sms
```

### Start Celery Beat Scheduler

```bash
make beat
```

### Start Flower Monitor

```bash
make flower
```

Access Flower UI at: http://localhost:5555/flower

Login with:
Username: login
Password: password

## 🧪 API Endpoints

### ➕ Create Manager (Admin only)

POST /api/manager/create/

```json
{
  "username": "testmanager",
  "email": "manager@example.com"
}
```


Response:
```json
{
  "username": "testmanager",
  "one_time_password": "zXQ8s3Fa9kL2",
  "role": "manager"
}
```

### 📤 Export Manager Users as CSV

GET /api/manager/export/
Optional query param: ?username=testmanager
Returns a downloadable CSV file.

## 📋 Task Overview

### 1. send_sms
- Queue: sms_queue
- Simulates sending SMS and logs to sms_responses.json

### 2. task_1
- Queue: default
- Logs a given number

### 3. process_schedule
- Queue: default
- Updates the status and description of Schedule instance

### 4. auto_task_runner
- Queue: default
- Runs periodically to process all due/incomplete Schedules

## ⚙️ Makefile Commands

| Command          | Description                          |
|------------------|--------------------------------------|
| make run         | Start Django development server      |
| make make        | Make migrations                      |
| make migrate     | Apply migrations                     |
| make create      | Create superuser                     |
| make shell       | Open Django shell                    |
| make worker      | Start default Celery worker          |
| make worker-sms  | Start SMS queue worker               |
| make beat        | Start Celery Beat                    |
| make flower      | Start Flower monitoring UI           |

## 📂 Project Structure

celery-test/
├── core/                   # Django settings and celery init
├── app/                    # Django app: models, views, tasks
├── templates/
├── static/
├── requirements.txt
├── manage.py
├── Makefile

## 🧠 Notes

- Ensure Redis server is running before launching workers.
- You can customize task frequency in Celery Beat and add more queues as needed.
- Consider using Docker or supervisor for production deployment.

## 📬 Contributions

Feel free to fork and submit PRs. If you find bugs or want a feature, open an issue.

## 📝 License

This project is licensed under the MIT License.
"""
