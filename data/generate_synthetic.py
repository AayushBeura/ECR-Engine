"""
Synthetic Dataset Generator for Explainable Credit Risk Engine
Generates 15,000 borrower profiles mimicking India's informal economy.
Features align with the project blueprint's specifications.

Improvements over v1:
- income_stability now correlated with default risk
- 3 new features: time_to_zero (normalized), debt_to_income_ratio, transaction_frequency
- Non-linear feature interactions in default scoring
- Realistic outliers & edge cases (~3%)
- Larger dataset (15,000 rows) for better minority-class learning
"""
import pandas as pd
import numpy as np
import os

np.random.seed(42)
N = 15000

def generate_dataset():
    # --- RAW SIMULATED DATA ---
    
    # Monthly income (INR) — gig workers / small vendors
    # Range: 8,000 to 80,000 per month
    monthly_income = np.random.lognormal(mean=10.0, sigma=0.6, size=N).clip(8000, 80000)
    
    # Monthly expenses (rent + utilities + existing EMI)
    rent = monthly_income * np.random.uniform(0.10, 0.55, size=N)
    utilities = monthly_income * np.random.uniform(0.03, 0.20, size=N)
    existing_emi = monthly_income * np.random.uniform(0.0, 0.35, size=N)
    
    # NSF (Non-Sufficient Funds) alert count over 6 months
    nsf_base = ((80000 - monthly_income) / 80000 * 8).clip(0, 10)
    nsf_frequency = np.random.poisson(lam=nsf_base).clip(0, 15).astype(int)
    
    # Bill payment latency (days late on average, negative = early)
    bill_payment_latency = np.random.normal(loc=3.0, scale=5.0, size=N).clip(-10, 30)
    
    # Number of unique merchants transacted with (UPI graph centrality proxy)
    merchant_diversity = np.random.poisson(lam=12, size=N).clip(1, 50)
    
    # Time-to-Zero: avg days after income until balance near zero
    # Lower = paycheck-to-paycheck = riskier
    time_to_zero = np.random.exponential(scale=10, size=N).clip(1, 30)
    
    # Age of borrower
    age = np.random.randint(21, 55, size=N)
    
    # Loan tenure requested (months)
    loan_tenure = np.random.choice([6, 12, 18, 24], size=N, p=[0.2, 0.4, 0.25, 0.15])
    
    # Requested loan amount (INR)
    requested_amount = (monthly_income * np.random.uniform(2, 8, size=N)).round(-2)
    
    # Transaction frequency: total UPI transactions per month (higher = more active)
    txn_frequency = np.random.poisson(lam=25, size=N).clip(1, 100)
    
    # --- STEP 1: Compute a preliminary risk score to condition income_stability ---
    # This ensures income_stability is correlated with default outcomes
    prelim_risk = (
        - 1.5 * ((monthly_income - 8000) / 72000)  # higher income = lower risk
        + 0.12 * nsf_frequency
        + 0.04 * bill_payment_latency
        - 0.8 * (merchant_diversity / 50.0)
    )
    prelim_risk_norm = (prelim_risk - prelim_risk.min()) / (prelim_risk.max() - prelim_risk.min())
    
    # --- STEP 2: Generate income inflows conditioned on risk ---
    # High-risk borrowers get WIDER income swings → higher CV → higher income_stability value
    volatility_scale = 0.15 + 0.45 * prelim_risk_norm  # range: 0.15 (stable) to 0.60 (volatile)
    monthly_inflows = np.column_stack([
        monthly_income * (1 + np.random.normal(0, volatility_scale)) for _ in range(6)
    ])
    monthly_inflows = np.maximum(monthly_inflows, 0)  # no negative inflows
    
    # --- ENGINEERED FEATURES ---
    
    # 1. Stability Index (CV of monthly inflows) — now risk-correlated
    income_stability = np.std(monthly_inflows, axis=1) / np.mean(monthly_inflows, axis=1)
    income_stability = np.nan_to_num(income_stability, nan=0.5).clip(0, 1)
    
    # 2. Affordability Index = (Income - Rent - Utilities - EMI) / Income
    affordability_index = (monthly_income - rent - utilities - existing_emi) / monthly_income
    affordability_index = affordability_index.clip(0, 1)
    
    # 3. Network Centrality (normalized merchant diversity)
    network_centrality = (merchant_diversity / 50.0).clip(0, 1)
    
    # 4. Normalized Time-to-Zero (higher = more buffer = better)
    time_to_zero_norm = (time_to_zero / 30.0).clip(0, 1)
    
    # 5. Debt-to-Income Ratio (higher = more leveraged = riskier)
    debt_to_income = (existing_emi / monthly_income).clip(0, 1)
    
    # 6. Transaction Frequency (normalized, higher = more active = better)
    txn_freq_norm = (txn_frequency / 100.0).clip(0, 1)
    
    # --- DEFAULT LABEL ---
    # Non-linear default scoring with feature interactions
    
    default_score = (
        # Main effects
        + 3.5 * income_stability          # Higher volatility → higher default
        - 2.0 * affordability_index       # Higher affordability → lower default
        + 0.15 * nsf_frequency            # More NSF alerts → higher default
        + 0.05 * bill_payment_latency     # Late payments → higher default
        - 1.5 * network_centrality        # More merchants → lower default
        - 1.0 * time_to_zero_norm         # Longer buffer → lower default
        + 1.2 * debt_to_income            # Higher leverage → higher default
        - 0.5 * txn_freq_norm             # More active → lower default
        
        # Interaction terms (non-linear relationships)
        + 1.5 * (1 - affordability_index) * (nsf_frequency / 15)   # broke + NSF = very bad
        + 0.8 * np.maximum(bill_payment_latency, 0) / 30 * (1 - network_centrality)  # late + isolated = bad
        + 0.6 * income_stability * debt_to_income                  # volatile + leveraged = bad
        
        # Random noise
        + np.random.normal(0, 0.4, size=N)
    )
    
    # Convert to probability via sigmoid
    default_prob = 1 / (1 + np.exp(-default_score))
    
    # Binary label: targeting ~28% default rate
    threshold = np.percentile(default_prob, 72)
    default_label = (default_prob >= threshold).astype(int)
    
    # --- INJECT EDGE CASES (~3% of data) ---
    n_outliers = int(N * 0.03)
    outlier_indices = np.random.choice(N, n_outliers, replace=False)
    
    for i, idx in enumerate(outlier_indices):
        if i % 2 == 0:
            # Type A: High income but defaults (lifestyle spending / gambling)
            monthly_income[idx] = np.random.uniform(50000, 80000)
            affordability_index[idx] = np.random.uniform(0.05, 0.15)  # very low despite high income
            nsf_frequency[idx] = np.random.randint(8, 15)
            default_label[idx] = 1
        else:
            # Type B: Low income, early bill payer, but still defaults (sudden shock)
            monthly_income[idx] = np.random.uniform(8000, 15000)
            bill_payment_latency[idx] = np.random.uniform(-10, -3)   # pays early
            income_stability[idx] = np.random.uniform(0.35, 0.55)    # but volatile
            default_label[idx] = 1
    
    # --- BUILD DATAFRAME ---
    df = pd.DataFrame({
        'monthly_income': monthly_income.round(0),
        'rent': rent.round(0),
        'utilities': utilities.round(0),
        'existing_emi': existing_emi.round(0),
        'income_stability': income_stability.round(4),
        'affordability_index': affordability_index.round(4),
        'nsf_frequency': nsf_frequency,
        'bill_payment_latency': bill_payment_latency.round(2),
        'network_centrality': network_centrality.round(4),
        'time_to_zero': time_to_zero.round(1),
        'time_to_zero_norm': time_to_zero_norm.round(4),
        'debt_to_income': debt_to_income.round(4),
        'transaction_frequency': txn_frequency,
        'txn_freq_norm': txn_freq_norm.round(4),
        'merchant_diversity': merchant_diversity,
        'age': age,
        'loan_tenure_months': loan_tenure,
        'requested_amount': requested_amount,
        'default': default_label
    })
    
    os.makedirs('data', exist_ok=True)
    df.to_csv('data/synthetic_credit_data.csv', index=False)
    
    # --- Summary ---
    feature_cols = [
        'income_stability', 'affordability_index', 'nsf_frequency',
        'bill_payment_latency', 'network_centrality', 'time_to_zero_norm',
        'debt_to_income', 'txn_freq_norm'
    ]
    
    print(f"Dataset generated: {len(df)} rows")
    print(f"Default rate: {df['default'].mean():.2%}")
    print(f"Outliers injected: {n_outliers} rows (~3%)")
    print(f"\nFeature summary:")
    print(df[feature_cols].describe().round(3))
    
    return df

if __name__ == "__main__":
    generate_dataset()
