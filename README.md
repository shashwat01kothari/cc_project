# Student Admission Admin Dashboard

This project is a **Student Admission Admin Dashboard** built with **Next.js (frontend)** and **FastAPI (backend)**. The dashboard allows administrators to:

- View seat availability across departments.
- Fetch and review student applications.
- Verify submitted student documents.

---

## 🛠️ Tech Stack

- **Frontend:** Next.js, Tailwind CSS
- **Backend:** FastAPI, PostgresQL
- **Database:** SQLite (with raw SQL or SQLAlchemy)

---

## 🚀 Features

### 🎓 Student Applications
- View list of student applications
- Each application shows:
  - ID
  - Exam type
  - Verification status (`unverified`, `verified`)
- Button to mark an application as "Verified"

### 📊 Department Seat Info
- Displays:
  - Department name
  - Total seats
  - Available seats
- Real-time fetch from backend

---


## 🧪 Setup Instructions

### 1. Clone the repository

```bash
git clone https://github.com/shashwat01kothari/cc_project.git
cd cc_proj
```

### 2. Setup the Backend (FastAPI)

```bash
cd backend/logic
python -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate
pip install -r requirements.txt

uvicorn app:app --reload
```

> Server will run on `http://127.0.0.1:8000`

### 3. Setup the Frontend (Next.js)

```bash
cd frontend/cc
npm install
npm run dev
```

> Frontend will run on `http://localhost:3000`

---

## 🔗 API Endpoints

### GET `/api/seatInfo`
Returns a list of departments with seat availability.

### GET `/api/studentApplications`
Returns a list of student applications.

### PUT `/api/studentApplications/{id}/verify`
Marks a student application as "verified".

### GET `/api/getData`
Return application status for a particular ID 

### POST `/api/confirmSeat`
Confirm/Block your seat for the year 2025

---

## 🙌 Acknowledgements

Special thanks to everyone who contributed to this project — whether through code, testing, or feedback.

---

## 📃 License

This project is licensed under the MIT License.