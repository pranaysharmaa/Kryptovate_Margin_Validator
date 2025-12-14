# Kryptovate Margin Validator – Setup Instructions

This document explains how to run the Kryptovate Margin Validator project locally on different systems.

The project consists of:
- a **FastAPI backend** (Python)
- a **React + TypeScript frontend**

No environment variables or secrets are required.

---

## 1. Prerequisites

### Backend
- Python **3.9+**
- pip
- virtualenv (recommended)

### Frontend
- Node.js **18+**
- npm

---

## 2. Backend Setup (FastAPI)

### Step 1: Navigate to backend
```bash
cd backend
```

### Step 2: Create and activate virtual environment (recommended)

**macOS / Linux**
```bash
python3 -m venv venv
source venv/bin/activate
```

**Windows**
```bash
python -m venv venv
venv\Scripts\activate
```

### Step 3: Install dependencies
```bash
pip install -r requirements.txt
```

### Step 4: Run the backend server
```bash
uvicorn main:app --reload --port 8000
```

The backend will be available at:
```
http://localhost:8000
```

---

## 3. Frontend Setup (React)

### Step 1: Navigate to frontend
```bash
cd frontend
```

### Step 2: Install dependencies
```bash
npm install
```

### Step 3: Start the development server
```bash
npm start
```

The frontend will be available at:
```
http://localhost:3000
```

---

## 4. Running Tests (Backend)

To run backend unit tests:
```bash
cd backend
pytest -v
```

All tests should pass.

---

## 5. Notes

- No `.env` file is required
- API base URL is hardcoded to `http://localhost:8000` for simplicity
- Backend is the authoritative source of truth for margin validation

---

## 6. Stopping the Project

Press `CTRL + C` in the terminal running:
- `uvicorn` to stop backend
- `npm start` to stop frontend

