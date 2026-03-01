# Gemini Chat Export

> Exported on: 2/21/2026, 8:55:14 PM

---

## 👤 You

EXPLAINABL...-FOR-INDIAPDF You said  explain this project, then explain the backend  add page number references to the explanation from the document

## 🤖 Gemini

This project, titled the **Explainable Credit Risk Engine for India**, is a technical blueprint for a digital lending platform specifically designed to bridge the credit gap for India's **informal economy**. It targets the 400 million "thin-file" borrowers—such as gig workers or small business owners—who have stable incomes but lack formal credit histories like CIBIL scores.

The core philosophy is to replace "black-box" lending models with an **explainability-first architecture** that complies with the **RBI Digital Lending Guidelines 2023** and the **DPDP Act 2023**.

### Project Overview

The system uses **alternative data**, primarily **UPI transaction history**, to assess creditworthiness through financial behavior rather than traditional documentation. Key innovations include:

* 
**Smart Data Analysis:** Extracts signals like income stability and merchant diversity from UPI and SMS logs.


* 
**Fair Machine Learning:** Uses LightGBM with **monotonic constraints** to ensure that better financial behavior (e.g., higher income) always results in a better or equal credit score, preventing algorithmic bias.


* 
**Transparent Decisions:** Every rejection is accompanied by **human-readable reason codes** (via SHAP values) and **counterfactual explanations** (via DiCE) that show borrowers specific paths to future approval.


* 
**Regulatory Compliance:** Features a "Direct Fund Flow" model where the fintech platform never touches borrower money, ensuring compliance with RBI mandates.



---

### Backend Architecture & Implementation

The backend is designed as a **Microservices architecture** using **FastAPI**, chosen to maintain a seamless "Python-native" environment for both machine learning and production services.

#### 1. Service Decomposition

The backend is split into four primary functional areas:

* 
**Gateway Service:** Handles JWT-based authentication, Pydantic-based input validation, and Redis-backed rate limiting (up to 1,000 requests/minute per IP).


* 
**Inference Service:** A CPU-intensive service isolated from the main I/O threads to prevent blocking . it manages the **LightGBM model**, **SHAP explainer**, and **DiCE engine** for generating predictions and explanations.


* 
**Loan Origination System (LOS):** Manages the application state machine (e.g., DRAFT → UNDERWRITING → APPROVED) and calculates the **Key Fact Statement (KFS)** and risk-based interest pricing in real-time.


* 
**Async External APIs:** Handles integrations for KYC verification (Aadhaar), SMS scraping, and payment mandates (e-NACH/UPI).



#### 2. Compliance-First Database Design

The system uses **PostgreSQL** with a schema specifically built for regulatory auditing and data sovereignty:

* 
**Data Localization:** All primary data and backups reside strictly within AWS Mumbai and Hyderabad regions to meet DPDP Act requirements.


* **Immutable Audit Log:** A dedicated table (`audit_log`) records every decision with its model version, SHAP values, and reason codes. It supports **INSERT only** operations to prevent tampering.


* 
**Time-Partitioned Retention:** The `sms_logs` table is partitioned by month, allowing the system to automatically drop (purge) data after 6 months to comply with "purpose limitation" laws.


* 
**Shadow Ledger:** A separate table records transaction intents and confirmations to reconcile against the bank's "legal ledger," ensuring funds are never at risk even if the app fails.



#### 3. Security

All **Personally Identifiable Information (PII)**, such as PAN and Aadhaar numbers, is encrypted at the application level using **AES-256** before being stored in the database.

Would you like me to dive deeper into how the SHAP values are converted into human-readable reason codes?

---

## 👤 You

You said  i want to build the backend for this. how do i proceed?

## 🤖 Gemini

Building the backend for an explainable credit risk engine requires a careful blend of traditional web development and machine learning operations (MLOps). Based on the technical specifications , you should follow a phased approach that prioritizes **regulatory compliance** and **model interpretability**.

---

### Step 1: Core Environment & Database Setup

Since the project mandates **Data Sovereignty**, your infrastructure must be hosted within India.

* **Framework Selection:** Use **FastAPI**. It is Python-native, which minimizes the "impedance mismatch" when integrating your ML models (LightGBM/SHAP).


* 
**Database (PostgreSQL):** Implement the "Compliance-First" schema.


* 
**User Table:** Must support AES-256 application-level encryption for PII like PAN and Aadhaar.


* 
**Audit Log:** Create an **immutable** table (INSERT only) to store every decision, its SHAP values, and model version.


* 
**Consent Ledger:** Track exactly when and for what purpose a user gave or revoked data access.




* 
**Data Retention:** Set up **Time-Partitioned tables** for SMS and UPI logs. This allows you to "drop" entire partitions after 6 months to comply with the DPDP Act’s purpose limitation.



### Step 2: Develop the Machine Learning Microservice

To keep your API responsive, isolate the CPU-intensive inference logic into its own service.

* **Model Pipeline:**
1. 
**Feature Engineering:** Build scripts to transform raw UPI/SMS data into features like "Stability Index" (Coefficient of Variation) and "Time-to-Zero".


2. 
**LightGBM Training:** Apply **monotonic constraints** during training (e.g., higher income must always lead to a higher score) to ensure fairness and auditability.


3. 
**Probability Calibration:** Use **Isotonic Regression** so the model output reflects a true default probability.




* **Explainability Engine:**
* Integrate **SHAP (TreeExplainer)** to calculate feature contributions for every application.


* Implement a **Semantic Mapping Pipeline** to convert raw SHAP values into human-readable reason codes (e.g., "Frequent low balance alerts indicate cash flow stress").


* Use **DiCE** to generate counterfactuals—showing the borrower 3 realistic "Paths to Approval".





### Step 3: Implement Regulatory Logic

The backend must enforce the **Direct Fund Flow** and **KFS** mandates from the RBI.

* 
**Nodal Bypass Logic:** Your system should not hold borrower funds. Instead:


* The backend sends a signal to the Regulated Entity (Bank), which disburses funds directly to the borrower.


* Maintain a **Shadow Ledger** to track transaction intents and reconcile them daily with the bank's actual statement.




* 
**Key Fact Statement (KFS) Engine:** Build a module that calculates the **All-inclusive APR** (Annual Percentage Rate). It must include the base rate, risk premium, processing fees, and third-party charges.



### Step 4: Security & MLOps Integration

* 
**API Security:** Enforce HTTPS, JWT-based authentication, and Redis-backed rate limiting (e.g., 1000 req/min).


* 
**Monitoring:** Implement **Drift Detection** using the Population Stability Index (PSI). If the PSI exceeds 0.25, the system should trigger an automated retraining alert.


* 
**Fairness Audits:** Build a monthly reporting task to check for "Adverse Impact". If the approval rate for a protected group (e.g., women) is less than 80% of the reference group, flag it for a manual audit.



### Summary of Deliverables for Phase 1

| Component | Action | Reference |
| --- | --- | --- |
| **Data Extraction** | UPI, SMS, and BBPS parsing logic

 |  |
| **Core API** | <br>`/predict`, `/explain`, and `/counterfactual` endpoints |  |
| **Compliance** | Immutable audit log and DPDP consent tracking

 |  |
| **Inference** | LightGBM model with Isotonic calibration

 |  |

**Would you like me to provide a Python code template for the FastAPI `/explain` endpoint using the SHAP mapping logic?**

---

## 👤 You

You said  since this is just a minor project poc, i want to use supabase for the database

## 🤖 Gemini

Using **Supabase** is a smart move for a 14-day PoC. It provides an instant PostgreSQL database, built-in Auth, and an "Edge Functions" environment that can handle your FastAPI-like logic while significantly reducing boilerplate.

Here is how you can adapt the project's **Compliance-First Design** to the Supabase ecosystem:

### 1. Database Schema (SQL Editor)

You can run the DDL (Data Definition Language) provided in the blueprint directly in the Supabase SQL Editor. Ensure you implement the specific tables required for RBI and DPDP compliance:

* 
**Users Table:** Use Supabase Auth for the `user_id`, but create a separate `profiles` table to store PII (PAN/Aadhaar). Note: For a PoC, you can use Supabase's built-in column-level encryption or PGvault to handle the AES-256 requirement.


* 
**Immutable Audit Log:** Create the `audit_log` table and use **PostgreSQL Policies (RLS)** to ensure it is "Insert Only" for the application service role.


* 
**Time-Partitioned Logs:** Use the `pg_partman` extension (available in Supabase) to handle the 6-month auto-deletion of `sms_logs`.



### 2. Backend Logic: FastAPI vs. Supabase Edge Functions

You have two architectural options:

* 
**Option A (Hybrid):** Keep **FastAPI** hosted on a platform like Render or Railway for the heavy ML lifting (LightGBM, SHAP, DiCE) and connect it to Supabase as your primary DB. This is best because SHAP and DiCE are CPU-intensive and might exceed Edge Function limits.


* 
**Option B (Pure Supabase):** Use **Supabase Edge Functions** for the Gateway and LOS logic (KFS calculation, application state). You would then call an external "Inference API" (like an AWS Lambda or a small Python container) specifically for the model's predictions.



### 3. Implementing the "Shadow Ledger" in Supabase

Since the project relies on a **Direct Fund Flow Mechanism**, you must use Supabase **Realtime** or **Database Webhooks**:

1. When a loan status in `loan_applications` changes to `APPROVED`, trigger a Supabase Webhook.


2. The Webhook notifies the Regulated Entity (or a mock bank API for your PoC).


3. On receiving the `DISBURSEMENT_SUCCESS` webhook back, update your `shadow_ledger` table to record the intent and confirmation.



### 4. DPDP Compliance with Supabase

Supabase makes **Consent Management** and the **Right to Deletion** easier:

* 
**Consent Tracking:** Use a `consent_ledger` table as specified.


* 
**Automated Purging:** Write a **Supabase Cron Job** (pg_cron) to search for users who have revoked consent or for data that has exceeded the 6-month retention period and trigger the `DELETE` operations.



### 5. API Configuration (The Gateway)

Replace the manual FastAPI rate-limiting with Supabase's built-in **Kong Gateway** settings:

* 
**Authentication:** Use Supabase JWTs to protect your `/predict` and `/explain` endpoints.


* 
**Row Level Security (RLS):** Ensure that a borrower can only see their own `reason_codes` and `paths_to_approval`.



**Would you like the SQL script to set up the DPDP-compliant `consent_ledger` and `audit_log` tables specifically for Supabase?**

---

## 👤 You

You said  explain the flow to me  what am i supposed to do and how

## 🤖 Gemini

To build this PoC using Supabase and FastAPI, you need to follow a specific "Lending Lifecycle" that moves from data ingestion to regulatory-compliant disbursement.

Here is the step-by-step flow of what happens in the system and how you should implement it:

### 1. The Application & Data Inflow

When a user (like a gig worker) applies, the system must collect "Alternative Data" because they likely lack a CIBIL history.

* 
**What you do:** Create a frontend form (Next.js PWA) to collect basic PII (PAN, Aadhaar) and request consent to read UPI/SMS logs.


* **How to implement:** Use **Supabase Auth** for the user account and store the encrypted PII in a `profiles` table. Use a `consent_ledger` table to log the timestamp and purpose of data access.



### 2. Feature Engineering & Inference

The raw data (SMS/UPI) is useless to an ML model until it is transformed into "features".

* 
**What you do:** Build a Python script (FastAPI) that parses the raw UPI strings to calculate the **Stability Index** (income volatility) and **Affordability Index** (disposable income).


* 
**How to implement:** * **Parsing:** Use Regex to extract transaction types and amounts from SMS logs.


* **Inference:** Pass these features to your **LightGBM model**. The model must use **monotonic constraints** so that "Better behavior = Higher score".


* 
**Calibration:** Pass the raw score through an **Isotonic Regression** layer to get a true probability of default.





### 3. The Explainability Layer (Crucial for RBI Compliance)

The RBI mandates that you cannot just say "Rejected"; you must explain *why*.

* 
**What you do:** Generate **SHAP values** for the specific application to identify the top three negative factors.


* **How to implement:**
* 
**Reason Codes:** Map the SHAP values to human language (e.g., "Frequent low balance alerts").


* 
**Counterfactuals (DiCE):** Generate "Paths to Approval" (e.g., "If you maintain a 5,000 balance for 3 months, you will be approved").





### 4. Regulatory Disbursement (The "Shadow Ledger")

Per RBI rules, the Fintech (your app) cannot touch the money.

* 
**What you do:** Implement a "Nodal Bypass" where the funds flow directly from the Bank (Regulated Entity) to the User.


* **How to implement:**
1. 
**Approval:** Your FastAPI service sends an approval signal to the Bank’s API.


2. 
**Shadow Ledger:** Simultaneously, insert a record into a `shadow_ledger` table in Supabase marked as `PENDING`.


3. 
**Confirmation:** Once the Bank confirms disbursement via webhook, update the `shadow_ledger` to `SUCCESS`.





### 5. Data Purging (DPDP Compliance)

You cannot store "Alternative Data" (SMS/UPI) forever.

* 
**What you do:** Set up an automated process to delete raw transaction data after the credit decision is made or after 6 months.


* 
**How to implement:** Use **Supabase `pg_cron**` or a scheduled Edge Function to "Drop" the old monthly partitions of your `sms_logs` table.



---

### Summary Table: Your Build Order

| Step | Action | Tool |
| --- | --- | --- |
| **1** | Setup Schema (Audit Log, Profiles, Consent Ledger) | Supabase SQL Editor |
| **2** | Deploy Inference API (LightGBM + SHAP + FastAPI) | Render / Docker |
| **3** | Create Feature Engineering Logic (Regex + Math) | Python Service |
| **4** | Build "Paths to Approval" UI | Next.js PWA |
| **5** | Schedule Auto-Purge Cron Jobs | Supabase pg_cron |

**Would you like me to provide the specific SQL code for the Supabase schema mentioned in Step 1?**

---

## 👤 You

You said  guide me through all the steps with code

## 🤖 Gemini

To build this backend with **Supabase** and **FastAPI**, you need to bridge the gap between a high-performance database and a specialized Machine Learning environment.

The following steps guide you through the implementation, focusing on the core innovations of the project: the **Compliance-First Schema**, **Fair ML Inference**, and the **Explainability Engine**.

---

### Step 1: Database Setup (Supabase)

Run this SQL in your Supabase SQL Editor. This schema implements the **DPDP-compliant data localization** and the **immutable audit log** required for regulatory transparency.

```sql
-- 1. Profiles with encrypted PII (conceptual - use Supabase Vault for real encryption)
CREATE TABLE profiles (
  id UUID REFERENCES auth.users ON DELETE CASCADE PRIMARY KEY,
  pan_encrypted TEXT, -- 
  aadhaar_encrypted TEXT,
  phone_encrypted TEXT,
  created_at TIMESTAMP WITH TIME ZONE DEFAULT NOW()
);

-- 2. The Immutable Audit Log 
CREATE TABLE audit_log (
  id BIGINT GENERATED BY DEFAULT AS IDENTITY PRIMARY KEY,
  application_id UUID NOT NULL,
  decision TEXT NOT NULL, -- APPROVED or REJECTED 
  approval_probability FLOAT NOT NULL, 
  shap_values JSONB NOT NULL, -- Raw SHAP values for auditing 
  reason_codes JSONB NOT NULL, -- Human-readable reasons 
  model_version TEXT NOT NULL, 
  timestamp TIMESTAMP WITH TIME ZONE DEFAULT NOW()
);

-- 3. Consent Ledger for DPDP 2023 
CREATE TABLE consent_ledger (
  id BIGINT GENERATED BY DEFAULT AS IDENTITY PRIMARY KEY,
  user_id UUID REFERENCES auth.users NOT NULL,
  purpose TEXT NOT NULL, -- e.g., 'credit_assessment' 
  consent_given BOOLEAN DEFAULT FALSE,
  granted_at TIMESTAMP WITH TIME ZONE DEFAULT NOW(),
  revoked_at TIMESTAMP WITH TIME ZONE -- 
);

```

---

### Step 2: Feature Engineering (FastAPI)

This Python logic transforms raw UPI strings into the **Stability Index** (Coefficient of Variation) and **Affordability Index** described in the blueprint.

```python
import numpy as np
import pandas as pd

def calculate_stability_index(monthly_inflows):
    """Calculates CV: Standard Deviation / Mean """
    mean_income = np.mean(monthly_inflows)
    if mean_income == 0: return 1.0
    sd_income = np.std(monthly_inflows)
    cv = sd_income / mean_income # 
    return cv

def calculate_affordability(income, rent, utilities, existing_emi):
    """Derived Affordability Index """
    disposable_income = income - rent - utilities - existing_emi # 
    return disposable_income / income if income > 0 else 0

```

---

### Step 3: Fair ML & Explainability Engine

This is the core "Inference Service". You must use **LightGBM with Monotonic Constraints** to ensure fairness—for example, ensuring that a higher stability index (lower volatility) never decreases an approval score.

```python
import lightgbm as lgb
import shap
from dice_ml import Data, Model, Dice

# 1. Enforce Monotonic Constraints 
# 1 = Increase, -1 = Decrease, 0 = No constraint
constraints = [1, -1, -1, 0, 1] # Income (+), Volatility (-), NSF (-), Age (0), Tenure (+) 

model = lgb.LGBMClassifier(
    monotone_constraints=constraints, # 
    n_estimators=200
)

# 2. Explainability: SHAP to Reason Codes 
def get_reason_codes(model, input_data):
    explainer = shap.TreeExplainer(model) # 
    shap_values = explainer.shap_values(input_data)
    
    # Mapping raw SHAP to human language 
    mapping = {
        'nsf_frequency': "Frequent low balance alerts indicate cash flow stress", # 
        'stability_index': "Income sources appear irregular", # 
        'affordability_index': "Limited disposable income for new loan" # 
    }
    
    # Sort by magnitude of negative impact 
    # (Simplified for demonstration)
    return [mapping[feat] for feat in top_negative_features]

```

---

### Step 4: The Counterfactual Engine (DiCE)

To empower borrowers, use **DiCE** to generate "Paths to Approval". This tells the rejected user exactly what to change to get a "Yes" next time.

```python
def generate_paths_to_approval(model, applicant_data, training_df):
    d = Data(dataframe=training_df, continuous_features=['income', 'stability'], outcome_name='default') # 
    m = Model(model=model, backend='sklearn') # 
    exp = Dice(d, m)
    
    # Generate 3 realistic paths 
    counterfactuals = exp.generate_counterfactuals(
        applicant_data, 
        total_CFs=3, 
        desired_class="opposite", # REJECTED -> APPROVED 
        features_to_vary=['affordability_index', 'nsf_frequency'] # 
    )
    return counterfactuals

```

---

### Step 5: Implementation Timeline

As this is a **14-day PoC**, proceed in this order:

1. 
**Days 1-3:** Set up the Supabase schema and Auth.


2. 
**Days 4-7:** Build the FastAPI inference service with LightGBM and SHAP.


3. 
**Days 8-10:** Integrate the **KFS (Key Fact Statement)** engine to calculate the 26% APR as per the regulatory formula.


4. 
**Days 11-14:** Connect the Next.js PWA frontend to visualize the "Paths to Approval".



Would you like the specific **Key Fact Statement (KFS)** calculation code to ensure your APR math matches the RBI formula?

---

## 👤 You

You said  how to train the ml model, and on which datasets? find required datasets online and list them out

## 🤖 Gemini

To train this model for a production-aware PoC, you need data that mirrors the financial behavior of India’s informal sector. Since real UPI and SMS banking data are private and protected by the DPDP Act 2023, you must use a combination of **open-source behavioral datasets** and **synthetically generated data** to simulate thin-file borrowers.

### 1. Recommended Datasets

You can find these datasets on platforms like Kaggle or through public financial reports to bootstrap your model.

| Dataset Name | Source | Description | Use Case in Project |
| --- | --- | --- | --- |
| **SMS-Data for Riders** | [Kaggle](https://www.kaggle.com/datasets/ramniwashkumar/sms-data) | Contains transactional SMS logs for delivery agents (Swiggy/Zomato). | Use to build the **SMS Parsing** and **NSF Alert Frequency** features. |
| **UPI Transactions 2024** | [Kaggle](https://www.kaggle.com/datasets/skullagos5246/upi-transactions-2024-dataset) | Simulated P2P and P2M UPI transactions across Indian merchant categories. | Use for **Income Proxy** and **Stability Index** calculations. |
| **Thin-File Synthetic Data** | [Kaggle](https://www.kaggle.com/datasets/deepashukla/synthetic-credit-score-of-thin-file-consumers) | Specifically designed to simulate borrowers with no credit history. | Use for training the core **LightGBM** model for "New-to-Credit" labels. |
| **Credit Risk Benchmark** | [Kaggle](https://www.kaggle.com/datasets/laotse/credit-risk-dataset) | Traditional credit bureau data including income, age, and loan status. | Use as a **Baseline** to compare alternative data performance. |

---

### 2. Training Workflow

The training process must prioritize **fairness** and **explainability** to meet RBI guidelines.

#### Step 1: Feature Engineering (The Informal Lens)

Instead of relying on credit scores, transform raw logs into these behavioral indicators:

* **Stability Index:** Calculate the **Coefficient of Variation (CV)** of 6 months of UPI inflows to quantify income volatility.
* **Time-to-Zero (TTZ):** Measure the average days from income receipt until the balance hits near-zero (detects paycheck-to-paycheck living).
* **Bill Latency:** Average delay between a bill being generated on BBPS and the user paying it.

#### Step 2: Training with Monotonic Constraints

Use **LightGBM** and explicitly define monotonic constraints to ensure the model follows logical financial rules (e.g., higher income should never decrease approval probability).

```python
# Define constraints: 1 for increasing, -1 for decreasing
constraints = {
    'income_proxy': 1, 
    'stability_index': -1,  # Lower CV (volatility) is better
    'bill_latency': -1, 
    'nsf_frequency': -1
}

model = lgb.LGBMClassifier(monotone_constraints=list(constraints.values()))
model.fit(X_train, y_train)

```

#### Step 3: Probability Calibration

Raw model outputs are often "log-odds" and not true probabilities. Use **Isotonic Regression** to calibrate the scores so that an output of 0.10 literally means a 10% chance of default. This is essential for accurate financial forecasting and risk pricing.

#### Step 4: Explainability Integration (SHAP & DiCE)

Once the model is trained, wrap it in an explainability layer:

* **SHAP:** Generate "Reason Codes" for every decision to show which features had the most negative impact.
* **DiCE:** Generate three "Paths to Approval" by identifying the smallest changes a user can make to their behavior (e.g., "Reduce late bill payments to zero") to get approved.

### 3. Monitoring for Drift

Once deployed, monitor the **Population Stability Index (PSI)**. If the distribution of your applicants changes (e.g., a sudden influx of younger borrowers), the PSI will exceed 0.25, signaling an urgent need to retrain the model on the latest 90 days of data.

Would you like me to provide a **Python script** to generate a synthetic UPI transaction dataset tailored to the delivery agent profiles (like the "Rajesh" example) mentioned in the doc?

---

## 👤 You

You said  explain the supabase part to me

## 🤖 Gemini

Supabase serves as the **Compliance-First Data Layer** for this project. While FastAPI handles the heavy machine learning (LightGBM and SHAP), Supabase manages the "Source of Truth," ensuring the system meets the **RBI Digital Lending Guidelines** and **DPDP Act 2023** requirements for data sovereignty, immutability, and privacy.

Here is the breakdown of how to implement the specific "Supabase parts" of this architecture.

---

### 1. Compliance-First Schema Implementation

In your Supabase SQL Editor, you will create the core tables designed for regulatory auditing.

#### **The Immutable Audit Log**

Per the blueprint, every decision must be tied to a model version and timestamp to be auditable 5 years later.

```sql
CREATE TABLE audit_log (
  id BIGINT GENERATED BY DEFAULT AS IDENTITY PRIMARY KEY,
  application_id UUID NOT NULL,
  decision TEXT NOT NULL CHECK (decision IN ('APPROVED', 'REJECTED')), 
  approval_probability FLOAT NOT NULL,
  shap_values JSONB NOT NULL, -- Stores the "Why" for regulators 
  reason_codes JSONB NOT NULL, -- The human-readable explanation 
  model_version TEXT NOT NULL, 
  created_at TIMESTAMP WITH TIME ZONE DEFAULT NOW()
);

-- SECURITY: Make this table "Insert Only" using RLS
ALTER TABLE audit_log ENABLE ROW LEVEL SECURITY;
CREATE POLICY "Enable insert for authenticated services only" ON audit_log FOR INSERT TO service_role WITH CHECK (true);
-- (No UPDATE or DELETE policies should be created, making it immutable) 

```

#### **The Shadow Ledger**

Because fintechs cannot hold borrower funds, you use a **Shadow Ledger** to track the intent and confirmation of money flowing between the Bank and the Borrower.

```sql
CREATE TABLE shadow_ledger (
  id BIGINT GENERATED BY DEFAULT AS IDENTITY PRIMARY KEY,
  application_id UUID REFERENCES loan_applications(id),
  intent_amount FLOAT NOT NULL, 
  status TEXT DEFAULT 'PENDING' CHECK (status IN ('PENDING', 'SUCCESS', 'FAILURE')), 
  txn_id TEXT, -- The ID received from the Bank's webhook 
  created_at TIMESTAMP WITH TIME ZONE DEFAULT NOW()
);

```

---

### 2. Data Sovereignty & Hosting

The **DPDP Act 2023** mandates that all personal data must physically reside in India.

* **What you do:** When creating your Supabase project, you **MUST** select the **Mumbai (ap-south-1)** region.
* 
**Why:** This ensures your primary database, backups, and logs never leave Indian borders, avoiding potential 50 crore fines.



---

### 3. Data Retention & The "Right to Deletion"

The DPDP Act requires a "Purpose Limitation" strategy, meaning data like SMS logs must be purged after the credit decision is made or after 6 months.

#### **Automated Purging with pg_cron**

Supabase supports the `pg_cron` extension. You can schedule a job to automatically delete old "Alternative Data".

```sql
-- Enable the extension
CREATE EXTENSION IF NOT EXISTS pg_cron;

-- Schedule a job to delete SMS logs older than 180 days every night at midnight
SELECT cron.schedule('0 0 * * *', $$
  DELETE FROM sms_logs 
  WHERE created_at < NOW() - INTERVAL '6 months'; 
$$);

```

---

### 4. Direct Fund Flow (Webhooks)

To comply with the **Nodal Bypass Architecture**, your Supabase instance should act as a listener.

1. **FastAPI** approves a loan and inserts a `PENDING` record in the `shadow_ledger`.
2. **The Bank** processes the transfer and hits a **Supabase Edge Function** URL with the result.
3. 
**Supabase Edge Function** updates the `shadow_ledger` to `SUCCESS` and triggers a **Realtime** notification to the borrower's mobile app.



---

### 5. Security & PII Protection

The blueprint mandates that **Personally Identifiable Information (PII)** like PAN and Aadhaar be encrypted at the application level.

* **The Supabase Way:** Use the **Supabase Vault** or the `pgsodium` extension for transparent column-level encryption. This ensures that even if someone gains access to the database, the raw PAN numbers remain unreadable without the specific decryption key.



### Next Step for You

I recommend starting with the **Database Schema**. Would you like me to provide a complete **SQL migration file** that sets up all five tables (Users, Applications, Audit, Consent, and Shadow Ledger) in one go?

---

## 👤 You

You said  yes please

## 🤖 Gemini

This SQL script establishes the **Compliance-First Design**  required for the 14-day PoC. It incorporates the **DPDP Act 2023** mandates for data localization and purpose limitation , along with the **RBI's Direct Fund Flow** requirement.

Copy and run this in your **Supabase SQL Editor** (ensure your project region is set to **Mumbai** or **Hyderabad** ).

```sql
-- ==========================================
-- 1. PII & PROFILE MANAGEMENT (DPDP COMPLIANCE)
-- ==========================================
CREATE TABLE profiles (
  id UUID REFERENCES auth.users ON DELETE CASCADE PRIMARY KEY,
  pan_encrypted TEXT,          -- PII: Encrypted at app level 
  aadhaar_encrypted TEXT,      -- PII: Encrypted at app level 
  full_name TEXT,
  phone_encrypted TEXT,
  created_at TIMESTAMP WITH TIME ZONE DEFAULT NOW()
);

-- ==========================================
-- 2. LOAN APPLICATIONS & ALTERNATIVE DATA
-- ==========================================
CREATE TABLE loan_applications (
  id UUID DEFAULT gen_random_uuid() PRIMARY KEY,
  user_id UUID REFERENCES auth.users NOT NULL,
  
  -- Features for Informal Sector 
  income_stability FLOAT,      -- Stability Index (CV) 
  affordability_index FLOAT,   -- (Inc-Rent-Utils-EMI)/Inc 
  nsf_frequency INT,           -- Low balance alert count 
  bill_payment_latency FLOAT,  -- Avg payment vs due date 
  network_centrality FLOAT,    -- Social proof from UPI graph 
  
  status TEXT DEFAULT 'DRAFT' CHECK (status IN ('DRAFT', 'SUBMITTED', 'UNDERWRITING', 'APPROVED', 'REJECTED')),
  requested_amount FLOAT NOT NULL,
  approved_rate FLOAT,         -- Interest rate based on ML score 
  kfs_json JSONB,              -- Key Fact Statement snapshot 
  
  created_at TIMESTAMP WITH TIME ZONE DEFAULT NOW(),
  decision_at TIMESTAMP WITH TIME ZONE
);

-- ==========================================
-- 3. IMMUTABLE AUDIT LOG (RBI COMPLIANCE)
-- ==========================================
-- This table records the "Why" behind every decision.
CREATE TABLE audit_log (
  id BIGINT GENERATED BY DEFAULT AS IDENTITY PRIMARY KEY,
  application_id UUID REFERENCES loan_applications(id) NOT NULL,
  decision TEXT NOT NULL,
  approval_probability FLOAT NOT NULL, -- Calibrated probability 
  shap_values JSONB NOT NULL,         -- Feature attribution 
  reason_codes JSONB NOT NULL,        -- Human-readable explanations 
  model_version TEXT NOT NULL,        -- For version tracking 
  timestamp TIMESTAMP WITH TIME ZONE DEFAULT NOW()
);

-- ==========================================
-- 4. SHADOW LEDGER (DIRECT FUND FLOW)
-- ==========================================
-- Records intent vs confirmation to ensure no pass-through accounts.
CREATE TABLE shadow_ledger (
  id BIGINT GENERATED BY DEFAULT AS IDENTITY PRIMARY KEY,
  application_id UUID REFERENCES loan_applications(id),
  intent_amount FLOAT NOT NULL,
  status TEXT DEFAULT 'PENDING' CHECK (status IN ('PENDING', 'SUCCESS', 'FAILURE')),
  bank_txn_id TEXT, -- RE's bank statement reference 
  created_at TIMESTAMP WITH TIME ZONE DEFAULT NOW()
);

-- ==========================================
-- 5. CONSENT LEDGER (PURPOSE LIMITATION)
-- ==========================================
-- Tracks explicit user consent as per DPDP Act.
CREATE TABLE consent_ledger (
  id BIGINT GENERATED BY DEFAULT AS IDENTITY PRIMARY KEY,
  user_id UUID REFERENCES auth.users NOT NULL,
  purpose TEXT NOT NULL, -- e.g., 'credit_assessment', 'fraud_detection' 
  consent_given BOOLEAN DEFAULT FALSE,
  granted_at TIMESTAMP WITH TIME ZONE DEFAULT NOW(),
  revoked_at TIMESTAMP WITH TIME ZONE -- For "Right to Deletion" 
);

-- ==========================================
-- 6. SECURITY & ACCESS CONTROL (RLS)
-- ==========================================
ALTER TABLE profiles ENABLE ROW LEVEL SECURITY;
ALTER TABLE loan_applications ENABLE ROW LEVEL SECURITY;
ALTER TABLE audit_log ENABLE ROW LEVEL SECURITY;

-- Borrowers can only see their own data
CREATE POLICY "Users can view own profile" ON profiles FOR SELECT USING (auth.uid() = id);
CREATE POLICY "Users can view own applications" ON loan_applications FOR SELECT USING (auth.uid() = user_id);

-- Audit log is only viewable by the user it belongs to
CREATE POLICY "Users view own audit trail" ON audit_log FOR SELECT 
USING (application_id IN (SELECT id FROM loan_applications WHERE user_id = auth.uid()));

```

---

### Implementation Notes for Your PoC

* 
**Encrypted PII:** For this PoC, perform the encryption in your FastAPI logic using the `cryptography` library before sending it to Supabase.


* 
**Shadow Ledger Sync:** When your bank mock API returns a success message, update the `shadow_ledger` status via a Supabase service role key to ensure the data is locked and consistent.


* 
**Auto-Deletion:** You can now go to the "Database" -> "Extensions" tab in Supabase, enable `pg_cron`, and set up the deletion job for `consent_ledger` revocations.



Would you like the **FastAPI Python code** to handle the PII encryption and the initial Supabase data insertion?

---

## 👤 You

You said  made the tables, what to do next

## 🤖 Gemini

Now that your database tables are ready in Supabase, the next phase is to build the **Inference Service** using FastAPI. This service acts as the "brain" of the project, handling the logic for PII encryption, feature engineering, and the explainable ML predictions.

Here is the step-by-step guide to setting up your backend logic.

---

### Step 1: Environment Configuration

Create a `.env` file in your Python project directory to securely store your Supabase credentials and encryption keys.

```bash
SUPABASE_URL="your-project-url"
SUPABASE_KEY="your-anon-or-service-role-key"
ENCRYPTION_KEY="your-32-byte-base64-key" # Generate using: Fernet.generate_key()

```

### Step 2: PII Encryption & Data Insertion (FastAPI)

Per the **DPDP Act 2023** compliance requirement in the blueprint, you must encrypt PII at the application level before it ever touches the database.

```python
from cryptography.fernet import Fernet
from supabase import create_client
import os

# Initialize Supabase and Encryption
supabase = create_client(os.getenv("SUPABASE_URL"), os.getenv("SUPABASE_KEY"))
cipher = Fernet(os.getenv("ENCRYPTION_KEY"))

def encrypt_data(plain_text: str):
    return cipher.encrypt(plain_text.encode()).decode()

async def create_user_application(user_id: str, pan: str, amount: float):
    # 1. Encrypt PII immediately 
    encrypted_pan = encrypt_data(pan)
    
    # 2. Insert into Supabase Profiles
    supabase.table("profiles").upsert({
        "id": user_id,
        "pan_encrypted": encrypted_pan
    }).execute()
    
    # 3. Create Loan Application Entry
    response = supabase.table("loan_applications").insert({
        "user_id": user_id,
        "requested_amount": amount,
        "status": "UNDERWRITING"
    }).execute()
    
    return response.data[0]["id"]

```

### Step 3: Implement the Prediction & Explanation Flow

This is where you integrate the **LightGBM model with monotonic constraints** and the **SHAP engine**.

```python
import shap
import joblib

# Load your pre-trained model and data
model = joblib.load("credit_model.pkl")

@app.post("/predict/{application_id}")
async def get_credit_decision(application_id: str, features: dict):
    # 1. Run Inference
    # Model uses monotonic constraints for fairness 
    probability = model.predict_proba([list(features.values())])[0][1]
    decision = "APPROVED" if probability >= 0.50 else "REJECTED" 
    
    # 2. Generate SHAP Explanations 
    explainer = shap.TreeExplainer(model)
    shap_vals = explainer.shap_values(list(features.values()))
    
    # 3. Map SHAP to Reason Codes 
    # Example logic: Get feature names for the most negative SHAP values
    reasons = ["Frequent low balance alerts", "Irregular income sources"] 
    
    # 4. Save to Immutable Audit Log 
    supabase.table("audit_log").insert({
        "application_id": application_id,
        "decision": decision,
        "approval_probability": probability,
        "shap_values": str(shap_vals),
        "reason_codes": reasons,
        "model_version": "v1.0-poc"
    }).execute()
    
    return {"decision": decision, "reasons": reasons}

```

### Step 4: The Key Fact Statement (KFS) Engine

If approved, the RBI mandates that the borrower receives an all-inclusive **APR calculation** before signing.

* 
**Formula:** .


* 
**Implementation:** Build a utility function that sums the **Base Rate**, **Risk Premium** (derived from the ML score), and **Processing Fees** to generate this JSON and save it to the `loan_applications` table.



### Step 5: Setup the Shadow Ledger for Disbursement

Once the decision is made, you must initiate the **Direct Fund Flow**.

1. 
**Insert Intent:** Create a record in `shadow_ledger` with the amount and a `PENDING` status.


2. **Mock Disbursement:** Call your simulated Bank API.
3. 
**Update Ledger:** Upon success, update the Supabase record with the `bank_txn_id`.



---

### What to do next?

Your immediate focus should be **Step 2 and 3**. Do you have a pre-trained `.pkl` model file ready, or should I show you how to write the **Model Training Script** using the LightGBM constraints specifically for this project?

---

