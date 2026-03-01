"""
Model Training Pipeline for Explainable Credit Risk Engine
- LightGBM with Monotonic Constraints (fairness)
- 3-way split: Train / Calibration / Test (prevents calibrator overfitting)
- Isotonic Regression for Probability Calibration
- scale_pos_weight for class imbalance
- Saves model, calibrator, and training data reference for DiCE
"""
import pandas as pd
import numpy as np
import lightgbm as lgb
from sklearn.model_selection import train_test_split
from sklearn.isotonic import IsotonicRegression
from sklearn.metrics import classification_report, roc_auc_score, brier_score_loss
import joblib
import os

# --- Feature configuration ---
FEATURE_COLS = [
    'income_stability',
    'affordability_index', 
    'nsf_frequency',
    'bill_payment_latency',
    'network_centrality',
    'time_to_zero_norm',
    'debt_to_income',
    'txn_freq_norm'
]

# Monotonic constraints as per project blueprint:
# income_stability:     -1 (lower CV = more stable = better → increasing value should increase default)
#                        Wait — income_stability IS the CV, higher CV = more volatile = RISKIER
#                        so constraint = 1 (increasing stability value → increasing default risk)
#                        BUT the blueprint says "lower CV = better" and the model constraint format is:
#                        1 = feature increase → prediction increase (default prob increase)
#                       -1 = feature increase → prediction decrease
# income_stability:      1 (higher CV → higher default probability)
# affordability_index:  -1 (higher affordability → lower default risk)
# nsf_frequency:         1 (more NSF alerts → higher default risk)
# bill_payment_latency:  1 (late payments → higher default risk)
# network_centrality:   -1 (more merchant diversity → lower default risk)
# time_to_zero_norm:    -1 (longer buffer → lower default risk)
# debt_to_income:        1 (higher leverage → higher default risk)
# txn_freq_norm:        -1 (more transactions → lower default risk)
MONOTONIC_CONSTRAINTS = [1, -1, 1, 1, -1, -1, 1, -1]

TARGET_COL = 'default'

def train():
    print("=" * 60)
    print("EXPLAINABLE CREDIT RISK ENGINE — MODEL TRAINING")
    print("=" * 60)
    
    # 1. Load data (borrower behavior dataset derived from UPI transactions)
    df = pd.read_csv('data/borrower_behavior_dataset.csv')
    # Drop non-feature columns if present
    if 'sender_upi_id' in df.columns:
        df = df.drop(columns=['sender_upi_id'])
    print(f"\nDataset: {len(df)} rows, Default rate: {df[TARGET_COL].mean():.2%}")
    
    X = df[FEATURE_COLS]
    y = df[TARGET_COL]
    
    # 2. Three-way split: Train (60%) / Calibration (20%) / Test (20%)
    #    Calibration split prevents isotonic regression from overfitting to training data
    X_dev, X_test, y_dev, y_test = train_test_split(
        X, y, test_size=0.2, random_state=42, stratify=y
    )
    X_train, X_calib, y_train, y_calib = train_test_split(
        X_dev, y_dev, test_size=0.25, random_state=42, stratify=y_dev  # 0.25 of 80% = 20%
    )
    print(f"Train: {len(X_train)}, Calibration: {len(X_calib)}, Test: {len(X_test)}")
    
    # 3. Calculate class imbalance ratio for scale_pos_weight
    neg_count = (y_train == 0).sum()
    pos_count = (y_train == 1).sum()
    scale_weight = neg_count / pos_count
    print(f"\nClass balance — No Default: {neg_count}, Default: {pos_count}")
    print(f"scale_pos_weight: {scale_weight:.2f}")
    
    # 4. Train LightGBM with Monotonic Constraints + Class Imbalance Handling
    print(f"\nMonotonic constraints: {dict(zip(FEATURE_COLS, MONOTONIC_CONSTRAINTS))}")
    
    model = lgb.LGBMClassifier(
        monotone_constraints=MONOTONIC_CONSTRAINTS,
        scale_pos_weight=scale_weight,
        n_estimators=300,
        learning_rate=0.05,
        max_depth=6,
        num_leaves=31,
        min_child_samples=30,
        subsample=0.8,
        colsample_bytree=0.8,
        random_state=42,
        verbose=-1
    )
    model.fit(X_train, y_train)
    
    # 5. Evaluate raw model
    y_pred = model.predict(X_test)
    y_prob = model.predict_proba(X_test)[:, 1]
    
    print("\n--- Raw Model Performance ---")
    print(classification_report(y_test, y_pred, target_names=['No Default', 'Default']))
    print(f"AUC-ROC: {roc_auc_score(y_test, y_prob):.4f}")
    
    # 6. Probability Calibration on SEPARATE calibration set (3-way split)
    #    This prevents the calibrator from overfitting to the training data
    calibrator = IsotonicRegression(y_min=0, y_max=1, out_of_bounds='clip')
    y_prob_calib = model.predict_proba(X_calib)[:, 1]
    calibrator.fit(y_prob_calib, y_calib)
    
    # Verify calibration on test set
    y_prob_calibrated = calibrator.predict(y_prob)
    raw_brier = brier_score_loss(y_test, y_prob)
    calibrated_brier = brier_score_loss(y_test, y_prob_calibrated)
    print(f"\nRaw Brier Score: {raw_brier:.4f}")
    print(f"Calibrated Brier Score: {calibrated_brier:.4f}")
    print(f"Calibrated AUC-ROC: {roc_auc_score(y_test, y_prob_calibrated):.4f}")
    print(f"Calibrated mean probability: {y_prob_calibrated.mean():.4f} (actual default rate: {y_test.mean():.4f})")
    
    # 7a. Retrain final model on train + calibration data for production
    print("\n--- Retraining Final Model on Train + Calibration Data ---")
    X_final = pd.concat([X_train, X_calib])
    y_final = pd.concat([y_train, y_calib])
    
    model_final = lgb.LGBMClassifier(
        monotone_constraints=MONOTONIC_CONSTRAINTS,
        scale_pos_weight=scale_weight,
        n_estimators=300,
        learning_rate=0.05,
        max_depth=6,
        num_leaves=31,
        min_child_samples=30,
        subsample=0.8,
        colsample_bytree=0.8,
        random_state=42,
        verbose=-1
    )
    model_final.fit(X_final, y_final)
    
    # Recalibrate on the same calibration set with the final model
    y_prob_calib_final = model_final.predict_proba(X_calib)[:, 1]
    calibrator_final = IsotonicRegression(y_min=0, y_max=1, out_of_bounds='clip')
    calibrator_final.fit(y_prob_calib_final, y_calib)
    
    # Verify final model on test set
    y_prob_final = model_final.predict_proba(X_test)[:, 1]
    y_pred_final = model_final.predict(X_test)
    y_prob_calibrated_final = calibrator_final.predict(y_prob_final)
    print(f"\n--- Final Model Performance (on Test Set) ---")
    print(classification_report(y_test, y_pred_final, target_names=['No Default', 'Default']))
    print(f"AUC-ROC: {roc_auc_score(y_test, y_prob_final):.4f}")
    print(f"Calibrated Brier: {brier_score_loss(y_test, y_prob_calibrated_final):.4f}")
    
    # 8. Feature importance (final model)
    print("\n--- Feature Importance (Final Model) ---")
    importance = dict(zip(FEATURE_COLS, model_final.feature_importances_))
    for feat, imp in sorted(importance.items(), key=lambda x: -x[1]):
        print(f"  {feat}: {imp}")
    
    # 9. Verify all features have non-zero importance
    zero_importance = [f for f, i in importance.items() if i == 0]
    if zero_importance:
        print(f"\n[!] WARNING: Zero-importance features: {zero_importance}")
    else:
        print("\n[OK] All features have non-zero importance")
    
    # 10. Save artifacts (using final model trained on train+calib)
    os.makedirs('models', exist_ok=True)
    joblib.dump(model_final, 'models/credit_model.pkl')
    joblib.dump(calibrator_final, 'models/calibrator.pkl')
    
    # Save training data for DiCE counterfactuals (train+calib combined)
    train_data = X_final.copy()
    train_data[TARGET_COL] = y_final.values
    train_data.to_csv('models/training_data.csv', index=False)
    
    # Also overwrite root credit_model.pkl for backward compatibility
    joblib.dump(model_final, 'credit_model.pkl')
    
    print("\n[OK] Saved: models/credit_model.pkl")
    print("[OK] Saved: models/calibrator.pkl")
    print("[OK] Saved: models/training_data.csv")
    print("[OK] Saved: credit_model.pkl (root, backward compat)")
    
    return model_final, calibrator_final

if __name__ == "__main__":
    train()
