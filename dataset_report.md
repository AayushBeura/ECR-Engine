# Synthetic Credit Dataset — Current State & Proposed Improvements

## 1. Overview

The **Explainable Credit Risk Engine** uses a synthetic dataset to train a LightGBM credit scoring model targeting India's 400M "thin-file" borrowers — gig workers and small vendors who lack formal credit histories (CIBIL scores). The model uses **alternative data signals** derived from UPI transaction behavior.

| Property | Value |
|---|---|
| **Rows** | 15,000 |
| **Total Columns** | 19 (8 model features + raw/derived + label) |
| **Model Features** | 8 |
| **Target Variable** | `default` (binary: 0 = No Default, 1 = Default) |
| **Default Rate** | 30.15% (4,522 defaults / 10,478 non-defaults) |
| **Generation Method** | Fully synthetic (`numpy` distributions) |
| **Random Seed** | 42 (reproducible) |

---

## 2. Feature Descriptions

### Model Features (used for training & prediction)

| Feature | Type | Range | Description | Monotonic Constraint |
|---|---|---|---|---|
| `income_stability` | Float | 0.04 – 1.00 | Coefficient of Variation (CV) of 6 months of UPI inflows. Higher = more volatile income = riskier. | ↑ increases default |
| `affordability_index` | Float | 0.00 – 0.85 | `(Income − Rent − Utilities − EMI) / Income`. Higher = more disposable income = safer. | ↑ decreases default |
| `nsf_frequency` | Int | 0 – 15 | Count of Non-Sufficient Funds (low balance) alerts over 6 months. Higher = riskier. | ↑ increases default |
| `bill_payment_latency` | Float | −10.0 – 21.5 | Average days late on bill payments. Negative = pays early. Higher = riskier. | ↑ increases default |
| `network_centrality` | Float | 0.02 – 0.52 | Normalized merchant diversity (`merchant_count / 50`). Higher = more UPI ecosystem engagement = safer. | ↑ decreases default |
| `time_to_zero_norm` | Float | 0.03 – 1.00 | Normalized days after income before balance nears zero. Higher = more financial buffer = safer. | ↑ decreases default |
| `debt_to_income` | Float | 0.00 – 0.35 | `existing_emi / monthly_income`. Higher = more leveraged = riskier. | ↑ increases default |
| `txn_freq_norm` | Float | 0.03 – 0.53 | Normalized monthly UPI transaction count (`txn_count / 100`). Higher = more active = safer. | ↑ decreases default |

### Raw / Intermediate Columns (not fed to model)

| Column | Description |
|---|---|
| `monthly_income` | Simulated monthly income (₹8K–₹80K, lognormal) |
| `rent`, `utilities`, `existing_emi` | Expense components |
| `time_to_zero` | Raw days-to-zero before normalization |
| `transaction_frequency` | Raw UPI transaction count before normalization |
| `merchant_diversity` | Raw unique merchant count (Poisson, λ=12) |
| `age` | Borrower age (21–54, uniform) |
| `loan_tenure_months` | Requested loan tenure (6/12/18/24 months) |
| `requested_amount` | Requested loan amount (INR) |

---

## 3. Current Model Performance

| Metric | Value |
|---|---|
| **AUC-ROC** | 0.9675 |
| **Accuracy** | 89% |
| **Default Precision** | 77% |
| **Default Recall** | 92% |
| **No-Default Precision** | 96% |
| **No-Default Recall** | 88% |

### Feature Importance (LightGBM split count)

| Rank | Feature | Importance | Correlation with Default |
|---|---|---|---|
| 1 | `income_stability` | 1197 | +0.497 |
| 2 | `affordability_index` | 1155 | −0.330 |
| 3 | `bill_payment_latency` | 995 | +0.184 |
| 4 | `time_to_zero_norm` | 990 | −0.159 |
| 5 | `nsf_frequency` | 981 | +0.476 |
| 6 | `debt_to_income` | 872 | +0.237 |
| 7 | `network_centrality` | 701 | −0.079 |
| 8 | `txn_freq_norm` | 483 | −0.015 |

---

## 4. How the Default Label Is Generated

The default label is created via a **logistic scoring function** with non-linear interactions:

```
default_score =
    + 3.5 × income_stability
    − 2.0 × affordability_index
    + 0.15 × nsf_frequency
    + 0.05 × bill_payment_latency
    − 1.5 × network_centrality
    − 1.0 × time_to_zero_norm
    + 1.2 × debt_to_income
    − 0.5 × txn_freq_norm

    # Interactions
    + 1.5 × (1 − affordability) × (nsf / 15)      ← broke + NSF = very bad
    + 0.8 × max(latency, 0) / 30 × (1 − centrality) ← late + isolated = bad
    + 0.6 × stability × debt_to_income                ← volatile + leveraged = bad

    + Normal(0, 0.4)                                   ← random noise
```

A sigmoid converts this to a probability, then a **72nd percentile threshold** creates the binary label (~28-30% default rate). Additionally, **~3% of rows are outlier edge cases** (high-income defaulters, early-payer defaulters) injected post-labeling.

---

## 5. Known Limitations & Proposed Improvements

### 🔴 Critical: AUC-ROC Is Unrealistically High (0.97)

**Problem:** Real-world credit models achieve 0.70–0.85 AUC-ROC. A score of 0.97 signals that synthetic patterns are too clean and predictable. Evaluators may question the PoC's credibility, and the model won't generalize to real data.

**Proposed Fix:** Increase noise variance from `Normal(0, 0.4)` to `Normal(0, 0.8)`, reduce feature coefficient magnitudes by ~40%, and add label noise (randomly flip ~3-5% of labels to simulate real-world mislabeling / edge cases the model can't capture).

---

### 🔴 Critical: 100% Synthetic Data

**Problem:** The data is entirely generated from numpy distributions. The feature distributions (income, expenses, NSF counts) may not match real Indian borrower profiles. This weakens claims about the model's applicability to the informal economy.

**Proposed Fix:** Download real credit datasets from Kaggle (the project already lists 4 candidate datasets) and use their distributions as the *seed* for the synthetic generator. For example, fit the `monthly_income` distribution from the "Credit Risk Benchmark" dataset and sample from that instead of a hardcoded lognormal.

---

### 🟡 Important: Calibrator Fitted on Training Data

**Problem:** The Isotonic Regression calibrator is currently fitted on `model.predict_proba(X_train)` — the same data the model was trained on. This introduces optimistic bias in the calibrated probabilities.

**Proposed Fix:** Use a **3-way split** (train / calibration / test) or **5-fold cross-validation** with a held-out calibration fold. The calibrator should never see data the model was trained on.

---

### 🟡 Important: Single Train/Test Split

**Problem:** Performance metrics are computed from a single 80/20 split. Results vary with the random seed and don't provide confidence intervals.

**Proposed Fix:** Implement **5-fold Stratified Cross-Validation** and report mean ± std for AUC-ROC, precision, and recall across folds.

---

### 🟡 Important: Hand-Picked Hyperparameters

**Problem:** LightGBM hyperparameters (`n_estimators=300`, `max_depth=7`, `num_leaves=42`, etc.) are manually chosen. These may not be optimal for the data distribution.

**Proposed Fix:** Use **Optuna** for Bayesian hyperparameter optimization with the search space:
- `learning_rate`: [0.01, 0.2]
- `num_leaves`: [15, 63]
- `max_depth`: [4, 10]
- `min_child_samples`: [10, 50]
- `subsample`: [0.6, 1.0]
- `colsample_bytree`: [0.6, 1.0]
- `scale_pos_weight`: [1.5, 4.0]

---

### 🟢 Nice-to-Have: Additional Derived Features

**Problem:** Some meaningful credit signals can be derived from existing raw data but aren't being used.

**Proposed Features:**

| Feature | Formula | Rationale |
|---|---|---|
| `income_trend` | Slope of 6-month inflows | Is income growing or shrinking? |
| `nsf_per_txn` | `nsf_frequency / transaction_frequency` | NSF relative to activity level |
| `savings_rate` | `1 − (rent + utilities + emi) / income` | How much is saved (similar to affordability but distinct) |
| `expense_volatility` | CV of monthly expenses | Spending consistency |

---

### 🟢 Nice-to-Have: Categorical Features

**Problem:** All features are continuous. Real credit applicants have categorical attributes that affect risk.

**Proposed Features:**

| Feature | Values | Rationale |
|---|---|---|
| `employment_type` | `gig_worker`, `salaried`, `self_employed`, `seasonal` | Gig workers have different risk profiles |
| `city_tier` | `tier_1`, `tier_2`, `tier_3`, `rural` | Urban vs rural lending dynamics |
| `loan_purpose` | `working_capital`, `personal`, `education`, `medical` | Purpose affects repayment behavior |

LightGBM handles categoricals natively — no one-hot encoding needed.

---

### 🟢 Nice-to-Have: Fairness Auditing

**Problem:** The RBI blueprint requires checking for **adverse impact** across demographic groups, but no such analysis is currently performed.

**Proposed Fix:** After training, stratify test set predictions by `age` buckets (21-30, 31-40, 41-54) and verify that:
- Approval rate for each group ≥ 80% of the reference group (4/5ths rule)
- Average predicted probability doesn't deviate by more than 5% across groups

---

## 6. Improvement Priority Matrix

| Priority | Improvement | Effort | Impact on Credibility |
|---|---|---|---|
| 🔴 P0 | Reduce AUC to realistic range | Low | Very High |
| 🔴 P0 | Blend real Kaggle data distributions | Medium | Very High |
| 🟡 P1 | Cross-validation | Low | High |
| 🟡 P1 | Calibrator on held-out set | Low | Medium |
| 🟡 P1 | Optuna hyperparameter tuning | Medium | Medium |
| 🟢 P2 | Add derived features | Low | Medium |
| 🟢 P2 | Add categorical features | Medium | Medium |
| 🟢 P2 | Fairness auditing | Low | High (for RBI compliance) |
