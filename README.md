# Explainable Credit Risk Engine for India

An **explainability-first** lending platform backend built for India's informal economy. It replaces black-box credit scoring with **transparent, fair, and RBI-compliant** decisions using alternative data (UPI/SMS) instead of traditional CIBIL scores.

Built with **FastAPI**, **Supabase (PostgreSQL)**, **LightGBM**, **SHAP**, and **DiCE**.

---

## Table of Contents

- [Architecture Overview](#architecture-overview)
- [What Has Been Implemented](#what-has-been-implemented)
- [What Is Left to Implement](#what-is-left-to-implement)
- [Project Structure](#project-structure)
- [Setup & Installation](#setup--installation)
- [API Reference](#api-reference)
- [Model Training](#model-training)
- [Tech Stack](#tech-stack)

---

## Architecture Overview

```
┌──────────────┐     ┌──────────────────────┐     ┌──────────────┐
│   Frontend   │────▶│   FastAPI Backend     │────▶│   Supabase   │
│  (Next.js)   │◀────│                      │◀────│  (PostgreSQL)│
└──────────────┘     │  ┌────────────────┐  │     └──────────────┘
                     │  │  LightGBM      │  │
                     │  │  + SHAP        │  │     ┌──────────────┐
                     │  │  + DiCE        │  │────▶│  Audit Log   │
                     │  │  + Calibrator  │  │     │  (Immutable) │
                     │  └────────────────┘  │     └──────────────┘
                     └──────────────────────┘
```

---

## What Has Been Implemented

### 1. Compliance-First Database Schema (Supabase)
- **`profiles`** — Stores user PII (PAN, Aadhaar) encrypted at application level
- **`loan_applications`** — Tracks application lifecycle (`DRAFT → UNDERWRITING → APPROVED/REJECTED`)
- **`audit_log`** — Immutable ledger (INSERT only via RLS) recording every decision with SHAP values, reason codes, and model version
- **`shadow_ledger`** — Tracks fund flow intents and bank confirmations (Direct Fund Flow per RBI)
- **`consent_ledger`** — Logs user consent grants/revocations per DPDP Act 2023
- **Row Level Security (RLS)** — Borrowers can only view their own data

### 2. PII Encryption
- AES-256 encryption using **Fernet** (`cryptography` library)
- PAN, Aadhaar, and phone numbers are encrypted **before** touching the database
- Encryption key stored in `.env`, never hardcoded

### 3. Synthetic Dataset
- **5,000 borrower profiles** mimicking India's informal economy (gig workers, small vendors)
- Features: monthly income (₹8K–₹80K), 6-month UPI inflow history, NSF alerts, bill payments, merchant diversity
- Realistic **25% default rate** with labeled ground truth
- Script: `data/generate_synthetic.py`

### 4. ML Model (LightGBM with Monotonic Constraints)
- **Monotonic constraints** enforce fairness:
  - Higher affordability → never increases default risk
  - More NSF alerts → never decreases default risk
  - Better bill payment history → never increases default risk
- **AUC-ROC: 0.83** on test set
- **Isotonic Regression** calibration ensures predicted probabilities are true default rates (0.24 predicted vs 0.25 actual)
- Script: `training/train_model.py`

### 5. SHAP Explainability (Reason Codes)
- Every decision includes **feature-level SHAP values**
- Negative factors are mapped to **human-readable reason codes**, e.g.:
  - *"Frequent low-balance alerts indicate potential cash flow stress"*
  - *"History of delayed bill payments suggests risk"*
  - *"Limited disposable income relative to loan requirements"*

### 6. DiCE Counterfactuals (Paths to Approval)
- Rejected applicants receive **3 actionable paths** showing the smallest behavioral changes needed for approval
- Example output:
  - *"Reduce low-balance alerts from 12 to 1 over the next 6 months"*
  - *"Pay bills on time — reduce average delay from 15.0 to 7.6 days"*
  - *"Diversify UPI transactions across more merchants"*

### 7. Key Fact Statement (KFS) Engine
- Calculates **risk-based interest rate** (Base 12% + up to 14% risk premium)
- Computes **monthly EMI**, total repayment, total interest, and **all-inclusive APR**
- Compliant with RBI mandate for transparent loan terms before signing

### 8. Shadow Ledger (Direct Fund Flow)
- Implements the **RBI Nodal Bypass** architecture
- Records disbursement `PENDING` intent → updates to `SUCCESS` on bank confirmation
- Ensures the fintech platform never touches borrower funds
- *Hardened: Wrapped with fallback handlers for network disconnects.*

### 9. Privacy & Consent Ledger (DPDP Act)
- Integration with Supabase to record, query, and revoke digital consent.
- Enforces data minimization via active `pg_cron` jobs scheduling the deletion of unneeded SMS/UPI transaction logs older than 6 months.

### 10. API Endpoints
| Method | Endpoint | Description |
|--------|----------|-------------|
| `GET` | `/` | Health check |
| `POST` | `/predict` | Quick credit decision (no Supabase, just ML) |
| `POST` | `/apply` | Full loan application with encryption, audit, KFS |
| `POST` | `/counterfactuals` | Generate "Paths to Approval" for any feature set |
| `GET` | `/config/generate-key` | Generate a new Fernet encryption key |
| `POST` | `/consent/record` | Record user DPDP consent |
| `GET` | `/consent/{user_id}` | Query active consent records |
| `POST` | `/consent/revoke` | Revoke active consent |

---

## What Is Left to Implement

Per the project blueprint document, the following components are not yet built:

### Backend
| Component | Description | Priority |
|-----------|-------------|----------|
| **Supabase Auth (JWT)** | Protect endpoints with Supabase JWT tokens instead of open access | Medium |
| **Drift Detection (PSI)** | Monitor Population Stability Index; alert if PSI > 0.25 for retraining | Medium |
| **Fairness Audit** | Monthly adverse impact check (approval rate for protected groups < 80% of reference → flag) | Low |
| **Rate Limiting** | Redis-backed rate limiting (1,000 req/min per IP) on gateway | Low |

### Frontend
| Component | Description |
|-----------|-------------|
| **Next.js PWA** | Loan application form, decision display, "Paths to Approval" visualization, KFS display |

---

## Project Structure

```
MinorSem6/
├── .env                          # Supabase credentials + encryption key
├── .env.template                 # Template for .env (safe to commit)
├── requirements.txt              # Python dependencies
├── main.py                       # FastAPI entry point (all endpoints)
│
├── services/
│   └── credit_service.py         # CreditService: ML inference, SHAP, DiCE, KFS
│
├── utils/
│   ├── encryption.py             # AES-256 Fernet encrypt/decrypt
│   ├── supabase_utils.py         # Supabase client, profile & application insertion
│   └── shadow_ledger.py          # Direct fund flow tracking
│
├── data/
│   ├── generate_synthetic.py     # Synthetic dataset generator (5,000 rows)
│   └── synthetic_credit_data.csv # Generated dataset
│
├── training/
│   └── train_model.py            # Full training pipeline (LightGBM + Isotonic)
│
├── models/
│   ├── credit_model.pkl          # Trained LightGBM model
│   ├── calibrator.pkl            # Isotonic Regression calibrator
│   └── training_data.csv         # Training data snapshot (for DiCE)
│
└── EXPLAINABLE-CREDIT-RISK-ENGINE-FOR-INDIA.pdf  # Project blueprint
```

---

## Setup & Installation

### Prerequisites
- **Python 3.10+**
- **Supabase project** (region: Mumbai `ap-south-1` for DPDP compliance)

### 1. Clone & Create Virtual Environment

```bash
git clone <your-repo-url>
cd MinorSem6

python -m venv venv

# Windows
.\venv\Scripts\activate

# macOS / Linux
source venv/bin/activate
```

### 2. Install Dependencies

```bash
pip install -r requirements.txt
```

### 3. Configure Environment Variables

Copy the template and fill in your credentials:

```bash
cp .env.template .env
```

Edit `.env`:
```env
SUPABASE_URL=https://your-project.supabase.co
SUPABASE_KEY=your-anon-or-service-role-key
ENCRYPTION_KEY=your-fernet-key
```

To generate a new encryption key:
```bash
python -c "from cryptography.fernet import Fernet; print(Fernet.generate_key().decode())"
```

### 4. Set Up Supabase Database

Run the following SQL in your **Supabase SQL Editor** to create all required tables:

```sql
-- 1. PROFILES (PII encrypted at app level)
CREATE TABLE profiles (
  id UUID REFERENCES auth.users ON DELETE CASCADE PRIMARY KEY,
  pan_encrypted TEXT,
  aadhaar_encrypted TEXT,
  full_name TEXT,
  phone_encrypted TEXT,
  created_at TIMESTAMP WITH TIME ZONE DEFAULT NOW()
);

-- 2. LOAN APPLICATIONS
CREATE TABLE loan_applications (
  id UUID DEFAULT gen_random_uuid() PRIMARY KEY,
  user_id UUID REFERENCES auth.users NOT NULL,
  income_stability FLOAT,
  affordability_index FLOAT,
  nsf_frequency INT,
  bill_payment_latency FLOAT,
  network_centrality FLOAT,
  status TEXT DEFAULT 'DRAFT' CHECK (status IN ('DRAFT', 'SUBMITTED', 'UNDERWRITING', 'APPROVED', 'REJECTED')),
  requested_amount FLOAT NOT NULL,
  approved_rate FLOAT,
  kfs_json JSONB,
  created_at TIMESTAMP WITH TIME ZONE DEFAULT NOW(),
  decision_at TIMESTAMP WITH TIME ZONE
);

-- 3. IMMUTABLE AUDIT LOG
CREATE TABLE audit_log (
  id BIGINT GENERATED BY DEFAULT AS IDENTITY PRIMARY KEY,
  application_id UUID REFERENCES loan_applications(id) NOT NULL,
  decision TEXT NOT NULL,
  approval_probability FLOAT NOT NULL,
  shap_values JSONB NOT NULL,
  reason_codes JSONB NOT NULL,
  model_version TEXT NOT NULL,
  timestamp TIMESTAMP WITH TIME ZONE DEFAULT NOW()
);

-- 4. SHADOW LEDGER (Direct Fund Flow)
CREATE TABLE shadow_ledger (
  id BIGINT GENERATED BY DEFAULT AS IDENTITY PRIMARY KEY,
  application_id UUID REFERENCES loan_applications(id),
  intent_amount FLOAT NOT NULL,
  status TEXT DEFAULT 'PENDING' CHECK (status IN ('PENDING', 'SUCCESS', 'FAILURE')),
  bank_txn_id TEXT,
  created_at TIMESTAMP WITH TIME ZONE DEFAULT NOW()
);

-- 5. CONSENT LEDGER (DPDP Act)
CREATE TABLE consent_ledger (
  id BIGINT GENERATED BY DEFAULT AS IDENTITY PRIMARY KEY,
  user_id UUID REFERENCES auth.users NOT NULL,
  purpose TEXT NOT NULL,
  consent_given BOOLEAN DEFAULT FALSE,
  granted_at TIMESTAMP WITH TIME ZONE DEFAULT NOW(),
  revoked_at TIMESTAMP WITH TIME ZONE
);

-- 6. ROW LEVEL SECURITY
ALTER TABLE profiles ENABLE ROW LEVEL SECURITY;
ALTER TABLE loan_applications ENABLE ROW LEVEL SECURITY;
ALTER TABLE audit_log ENABLE ROW LEVEL SECURITY;

CREATE POLICY "Users can view own profile" ON profiles FOR SELECT USING (auth.uid() = id);
CREATE POLICY "Users can view own applications" ON loan_applications FOR SELECT USING (auth.uid() = user_id);
CREATE POLICY "Users view own audit trail" ON audit_log FOR SELECT
  USING (application_id IN (SELECT id FROM loan_applications WHERE user_id = auth.uid()));
```

### 5. Generate Dataset & Train Model

```bash
python data/generate_synthetic.py
python training/train_model.py
```

Expected output:
- `data/synthetic_credit_data.csv` — 5,000 rows, 25% default rate
- `models/credit_model.pkl` — LightGBM model (AUC-ROC ~0.83)
- `models/calibrator.pkl` — Isotonic Regression calibrator
- `models/training_data.csv` — Training data snapshot for DiCE

### 6. Run the Server

```bash
uvicorn main:app --reload
```

### 7. Start the frontend server

```bash
cd project_format_fresh
npm install
npm run build
npm start
```

The API will be available at **http://127.0.0.1:8000**  
Swagger docs at **http://127.0.0.1:8000/docs**

---

## API Reference

### `POST /predict` — Quick Credit Decision

```json
// Request
{
  "features": {
    "income_stability": 0.15,
    "affordability_index": 0.5,
    "nsf_frequency": 3,
    "bill_payment_latency": 2.0,
    "network_centrality": 0.3
  }
}

// Response
{
  "decision": "APPROVED",
  "probability": 0.9504,
  "default_probability": 0.0496,
  "shap_values": { ... },
  "reason_codes": ["Limited disposable income relative to loan requirements."]
}
```

### `POST /apply` — Full Loan Application

```json
// Request
{
  "user_id": "uuid-from-supabase-auth",
  "pan": "ABCDE1234F",
  "aadhaar": "123456789012",
  "full_name": "Rajesh Kumar",
  "amount": 50000,
  "features": {
    "income_stability": 0.15,
    "affordability_index": 0.5,
    "nsf_frequency": 3,
    "bill_payment_latency": 2.0,
    "network_centrality": 0.3
  }
}

// Response (Approved)
{
  "application_id": "uuid",
  "decision": "APPROVED",
  "approval_probability": 0.95,
  "default_probability": 0.05,
  "shap_values": { ... },
  "reasons": [ ... ],
  "kfs": {
    "interest_rate_pa": 12.70,
    "apr": 14.70,
    "monthly_emi": 4450.32,
    "total_repayment": 53403.84,
    ...
  },
  "paths_to_approval": null
}

// Response (Rejected) — includes Paths to Approval
{
  "application_id": "uuid",
  "decision": "REJECTED",
  "reasons": ["Frequent low-balance alerts...", "History of delayed bill payments..."],
  "paths_to_approval": [
    {
      "nsf_frequency": {
        "current": 12, "target": 1,
        "advice": "Reduce low-balance alerts from 12 to 1 over the next 6 months."
      }
    }
  ]
}
```

### `POST /counterfactuals` — Paths to Approval

```json
// Request
{
  "features": { ... },
  "num_paths": 3
}

// Response
{
  "paths_to_approval": [
    { "feature": { "current": ..., "target": ..., "advice": "..." } },
    ...
  ]
}
```

---

## Model Training

### Feature Definitions

| Feature | Formula | Monotonic Constraint |
|---------|---------|---------------------|
| `income_stability` | CV of 6-month UPI inflows (σ/μ) | ↓ Lower = better |
| `affordability_index` | (Income − Rent − Utils − EMI) / Income | ↑ Higher = better |
| `nsf_frequency` | Count of low-balance alerts in 6 months | ↓ Lower = better |
| `bill_payment_latency` | Avg days late on bill payments | ↓ Lower = better |
| `network_centrality` | Unique merchant count / 50 (normalized) | ↑ Higher = better |

### Retraining

```bash
# Regenerate data (optional, uses seed=42 for reproducibility)
python data/generate_synthetic.py

# Retrain model
python training/train_model.py
```

The server will auto-reload and pick up the new `credit_model.pkl` on next restart.

---

## Tech Stack

| Layer | Technology |
|-------|-----------|
| **API Framework** | FastAPI + Uvicorn |
| **Database** | Supabase (PostgreSQL) |
| **ML Model** | LightGBM |
| **Explainability** | SHAP (TreeExplainer) |
| **Counterfactuals** | DiCE |
| **Calibration** | Isotonic Regression (scikit-learn) |
| **Encryption** | Fernet (AES-256) |
| **Data Generation** | NumPy + Pandas |

---

## Regulatory Compliance

| Regulation | Implementation |
|-----------|---------------|
| **RBI Digital Lending 2023** | KFS engine, Shadow Ledger, Direct Fund Flow |
| **DPDP Act 2023** | PII encryption, Consent Ledger, Data localization (Mumbai region) |
| **Explainability Mandate** | SHAP reason codes, DiCE counterfactuals |
| **Fairness** | Monotonic constraints, Isotonic calibration |
| **Audit Trail** | Immutable audit log with model versioning |
