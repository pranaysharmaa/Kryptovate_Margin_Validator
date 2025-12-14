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

All tests except one should pass. See discussions for more.

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




# Kryptovate Margin Validator – Design & Implementation Explanation

This document explains the architectural decisions, assumptions, and trade-offs made while implementing the Kryptovate Margin Validator.

The goal of the project is to simulate a **realistic exchange-style margin validation flow**, while remaining aligned with the assignment requirements.

---

## 1. High-Level Architecture

The system is split into two parts:

### Frontend (React + TypeScript)
- Provides a margin preview UI
- Performs non-authoritative margin calculation for UX
- Sends order parameters and claimed margin to backend

### Backend (FastAPI)
- Owns all economic and validation logic
- Recomputes margin independently
- Accepts or rejects the request based on risk rules

The backend is always the **final authority**.

---

## 2. Margin Calculation Model

Margin is calculated using the formula:

```
required_margin = (mark_price × order_size × contract_value) / leverage
```

This formula is applied:
- in the frontend for preview only
- in the backend for authoritative validation

---

## 3. Separation of Concerns

### Frontend
- Shows immediate feedback
- Warns users about invalid inputs
- Never enforces final rules

### Backend
- Validates all inputs
- Enforces economic constraints
- Prevents invalid or risky orders



---

## 4. Monetary Precision & Decimal Handling

### Key Decision
**All monetary values are handled as strings and converted to `Decimal` in the backend.**

#### Why not floats?
Binary floating-point numbers cannot represent many decimal values exactly, which leads to non-deterministic rounding behavior.

Example:
```
2.0145 → 2.0144999999999997
```

This causes incorrect rounding at `.005` boundaries.

---

## 5. Two-Decimal Normalization

### Design Choice
**All monetary values are normalized to exactly 2 decimal places (`0.01`) before comparison.**

This includes:
- backend-computed margin
- client-submitted margin

Both are quantized using:
```
ROUND_HALF_UP
```

### Why this matters
- Prevents scale mismatches (`19.2` vs `19.20`)
- Eliminates equality-boundary failures
- Matches how real exchanges store balances

---

## 6. Rounding Mode: ROUND_HALF_UP

`ROUND_HALF_UP` was chosen because:
- It matches human financial expectations
- It avoids under-collateralization
- It is deterministic and audit-safe

This rounding rule is standard in financial systems.

---

## 7. Margin Sufficiency Check

After computing the required margin, the backend checks:

```
client_margin >= required_margin
```

The client-submitted margin is treated as a **claim**, not a truth.

If the claim is insufficient, the request is rejected.

This prevents:
- tampered frontend submissions
- stale UI values
- malicious clients

---

## 8. Input Validation Rules

The backend enforces the following invariants:

- `order_size > 0`
- `leverage` must be allowed for the asset
- unsupported assets are rejected
- zero-margin orders are rejected

Frontend validation exists only for UX and warnings.

---

## 9. Handling React State Timing

The frontend originally calculated margin using derived state.

To avoid React race conditions:
- margin is recomputed synchronously during submission
- derived state is not relied upon for critical actions

This guarantees deterministic behavior.

---

## 10. Logging & Observability

The backend emits structured JSON logs for:
- margin computation
- validation success
- validation failure

Timestamps are logged in **IST (Asia/Kolkata)** using timezone-aware datetimes.

This makes logs readable and auditable.


---

## 12. Assumptions Made

- Margin validation is stateless
- Wallet balances are not modeled
- Orders are preview-only (no execution)
- Precision is limited to two decimal places

These assumptions are intentional and documented.

---

## 13. Discussion - Left open ended currently

- order size and margin client have type float which might lead to a lot of issues internally with the round half up function.
- appeared consistently in pytest
- should this be changed to str while or some other solution is possible.
