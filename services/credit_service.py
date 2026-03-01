import joblib
import pandas as pd
import numpy as np
import shap
import json
from typing import Dict, List, Optional
from utils.supabase_utils import get_supabase_client

class CreditService:
    def __init__(self, model_path: str = "models/credit_model.pkl", 
                 calibrator_path: str = "models/calibrator.pkl",
                 training_data_path: str = "models/training_data.csv"):
        self.model = joblib.load(model_path)
        self.calibrator = joblib.load(calibrator_path)
        self.explainer = shap.TreeExplainer(self.model)
        self.training_data = pd.read_csv(training_data_path)
        
        self.feature_names = [
            'income_stability', 'affordability_index', 'nsf_frequency',
            'bill_payment_latency', 'network_centrality',
            'time_to_zero_norm', 'debt_to_income', 'txn_freq_norm'
        ]
        self.reason_mapping = {
            'income_stability': "Income sources appear irregular or highly volatile.",
            'affordability_index': "Limited disposable income relative to loan requirements.",
            'nsf_frequency': "Frequent low-balance alerts indicate potential cash flow stress.",
            'bill_payment_latency': "History of delayed bill payments suggests risk.",
            'network_centrality': "Low network engagement signals limited economic integration.",
            'time_to_zero_norm': "Funds deplete quickly after income receipt, indicating paycheck-to-paycheck living.",
            'debt_to_income': "Existing debt obligations consume a high share of income.",
            'txn_freq_norm': "Low transaction activity suggests limited financial engagement."
        }
        # Feature ranges for DiCE (realistic bounds)
        self.feature_ranges = {
            'income_stability': [0.0, 1.0],
            'affordability_index': [0.0, 1.0],
            'nsf_frequency': [0, 30],
            'bill_payment_latency': [-10, 60],
            'network_centrality': [0.0, 1.0],
            'time_to_zero_norm': [0.0, 1.0],
            'debt_to_income': [0.0, 1.0],
            'txn_freq_norm': [0.0, 1.0]
        }
        self.confidence_penalty = 0.0

    def process_transactions(self, transaction_data: List[Dict], requested_amount: float = 50000.0) -> Dict[str, float]:
        """Process transaction data into the 8 alternative data features.

        Uses Pandas aggregations (groupby month, std/mean, nunique, etc.)
        mirroring the methodology validated in the MODEL.ipynb notebook.
        """
        df = pd.DataFrame(transaction_data)

        if 'timestamp' in df.columns:
            df['timestamp'] = pd.to_datetime(df['timestamp'], errors='coerce')

        # Default baseline values (returned as-is if df is empty)
        features = {
            'income_stability': 0.3,
            'affordability_index': 0.4,
            'nsf_frequency': 0,
            'bill_payment_latency': 0.0,
            'network_centrality': 0.1,
            'time_to_zero_norm': 0.2,
            'debt_to_income': 0.3,
            'txn_freq_norm': 0.2,
        }

        if df.empty:
            return features

        try:
            if 'amount' in df.columns:
                df['amount'] = pd.to_numeric(df['amount'], errors='coerce').fillna(0)

            # ----------------------------------------------------------
            # 1. Income Stability  (CV = std / mean of monthly totals)
            # ----------------------------------------------------------
            if 'amount' in df.columns and 'timestamp' in df.columns:
                df['year_month'] = df['timestamp'].dt.to_period('M')
                monthly_totals = df.groupby('year_month')['amount'].sum()
                if len(monthly_totals) >= 2:
                    cv = monthly_totals.std() / monthly_totals.mean() if monthly_totals.mean() != 0 else 0.0
                    features['income_stability'] = float(cv)
                elif len(monthly_totals) == 1:
                    features['income_stability'] = 0.0   # single month → perfectly stable

            # ----------------------------------------------------------
            # 2. Transaction Frequency Norm  (total txns / 100)
            # ----------------------------------------------------------
            features['txn_freq_norm'] = min(len(df) / 100.0, 1.0)

            # ----------------------------------------------------------
            # 3. Network Centrality  (unique receivers / 50)
            # ----------------------------------------------------------
            if 'receiver_upi_id' in df.columns:
                unique_receivers = df['receiver_upi_id'].nunique()
                features['network_centrality'] = unique_receivers / 50.0
            elif 'receiver_name' in df.columns:
                unique_receivers = df['receiver_name'].nunique()
                features['network_centrality'] = unique_receivers / 50.0

            # ----------------------------------------------------------
            # 4. NSF Frequency
            #    Prefer transfer_ratio > 0.9 (notebook method).
            #    Fall back to status == 'failed' or 2% heuristic.
            # ----------------------------------------------------------
            if 'transfer_ratio' in df.columns:
                df['transfer_ratio'] = pd.to_numeric(df['transfer_ratio'], errors='coerce').fillna(0)
                features['nsf_frequency'] = int(len(df[df['transfer_ratio'] > 0.9]))
            elif 'status' in df.columns:
                features['nsf_frequency'] = int(len(df[df['status'].astype(str).str.lower() == 'failed']))
            else:
                features['nsf_frequency'] = min(max(int(len(df) * 0.02), 0), 10)

            # ----------------------------------------------------------
            # 5. Time-to-Zero Norm  (inverse of near-zero events)
            #    1 / (1 + count_of_events_with_transfer_ratio > 0.8)
            # ----------------------------------------------------------
            if 'transfer_ratio' in df.columns:
                near_zero_events = int(len(df[df['transfer_ratio'] > 0.8]))
                features['time_to_zero_norm'] = 1.0 / (1.0 + near_zero_events)
            else:
                # Proxy: derive from nsf_frequency and bill_payment_latency
                risk_factor = min(
                    (features['nsf_frequency'] / 10.0 + features.get('bill_payment_latency', 0) / 5.0) / 2.0,
                    1.0,
                )
                features['time_to_zero_norm'] = max(0.6 - (risk_factor * 0.5), 0.03)

            # ----------------------------------------------------------
            # 6. Bill Payment Latency
            #    No actual due-date info available; use merchant-category
            #    heuristic (same as before) or default to 3.0 days.
            # ----------------------------------------------------------
            if 'merchant_category' in df.columns:
                bill_txns = df[df['merchant_category'].astype(str).str.contains(
                    'bill|utility|telecom', case=False, na=False
                )]
                features['bill_payment_latency'] = max(5.0 - len(bill_txns), 0.0)
            else:
                features['bill_payment_latency'] = 3.0

            # ----------------------------------------------------------
            # 7. Affordability Index & Debt-to-Income
            #    Estimate monthly income from transaction volume, then
            #    compute EMI for the requested amount at 15% p.a. / 12 mo.
            # ----------------------------------------------------------
            estimated_monthly_income = 50000.0
            if 'amount' in df.columns and 'timestamp' in df.columns and len(df) > 1:
                date_range_days = (df['timestamp'].max() - df['timestamp'].min()).days
                months = max(date_range_days / 30.0, 1.0)
                total_volume = df['amount'].sum()
                estimated_monthly_income = max(total_volume / months, 10000.0)

            annual_rate = 0.15
            monthly_rate = annual_rate / 12
            monthly_emi = (
                requested_amount * monthly_rate * (1 + monthly_rate) ** 12
                / ((1 + monthly_rate) ** 12 - 1)
            )

            raw_affordability = (estimated_monthly_income - monthly_emi) / estimated_monthly_income
            features['affordability_index'] = max(0.01, min(raw_affordability, 0.99))

            raw_dti = monthly_emi / estimated_monthly_income
            features['debt_to_income'] = min(max(raw_dti, 0.0), 0.99)

            # If EMI exceeds income, force worst-case income_stability
            if monthly_emi > estimated_monthly_income:
                features['income_stability'] = 0.6

        except Exception as e:
            print(f"Error processing transactions: {e}")

        # ----------------------------------------------------------
        # Final: ensure every feature is within trained model bounds
        # ----------------------------------------------------------
        for feat in self.feature_names:
            min_val, max_val = self.feature_ranges[feat]
            features[feat] = float(np.clip(features[feat], min_val, max_val))

        return features

    def autotune_weights(self, transaction_count: int):
        """Autotune threshold/biases based on data density/confidence."""
        if transaction_count < 10:
            self.confidence_penalty = 0.10  # Penalize thin files
        elif transaction_count < 50:
            self.confidence_penalty = 0.05
        elif transaction_count > 150:
            self.confidence_penalty = -0.05 # Reward high visibility
        else:
            self.confidence_penalty = 0.0


    def predict(self, features: Dict[str, float]) -> Dict:
        input_df = pd.DataFrame([features])
        input_df = input_df[self.feature_names]
        
        # Raw probability from model
        raw_prob = float(self.model.predict_proba(input_df)[0][1])
        
        # Calibrated probability + autotuned penalty based on data richness
        calibrated_prob = float(self.calibrator.predict([raw_prob])[0])
        calibrated_prob = min(max(calibrated_prob + self.confidence_penalty, 0.0), 1.0)
        
        # Hard Business Policy Override (Practicality Check)
        # ML models fail on out-of-distribution extremes (e.g., trying to borrow 500 Crore).
        # We overlay a definitive rule baseline: Reject if DTI is too high or Affordability is structurally zero.
        policy_reject = False
        if features.get('debt_to_income', 0) > 0.60 or features.get('affordability_index', 1) < 0.10:
            policy_reject = True
            calibrated_prob = max(calibrated_prob, 0.85)  # Force a high default probability

        # Decision: APPROVED if default probability < 0.4 (i.e., 60%+ chance of NOT defaulting)
        decision = "APPROVED" if calibrated_prob < 0.4 and not policy_reject else "REJECTED"
        
        # SHAP explanations
        shap_values_raw = self.explainer.shap_values(input_df)
        # Handle both binary and multi-class SHAP output
        if isinstance(shap_values_raw, list):
            shap_values = shap_values_raw[1][0]  # Class 1 (default) SHAP values
        else:
            shap_values = shap_values_raw[0]
        
        # Top reasons for the decision
        reasons = []
        feature_impacts = sorted(
            zip(self.feature_names, shap_values), 
            key=lambda x: x[1], 
            reverse=True  # Highest positive SHAP = most pushing toward default
        )
        
        for feat, impact in feature_impacts[:3]:
            if impact > 0:  # Only include factors that increase default risk
                reasons.append(self.reason_mapping.get(feat, f"Issue with {feat}"))

        return {
            "decision": decision,
            "probability": round(1 - calibrated_prob, 4),  # Return approval probability
            "default_probability": round(calibrated_prob, 4),
            "shap_values": {feat: round(val, 4) for feat, val in zip(self.feature_names, shap_values)},
            "reason_codes": reasons if reasons else ["All financial indicators are within acceptable ranges."]
        }

    def generate_counterfactuals(self, features: Dict[str, float], num_cfs: int = 3) -> List[Dict]:
        """Generate 'Paths to Approval' using DiCE counterfactuals."""
        try:
            import dice_ml
            
            # Prepare training data for DiCE
            train_df = self.training_data[self.feature_names + ['default']].copy()
            
            d = dice_ml.Data(
                dataframe=train_df,
                continuous_features=self.feature_names,
                outcome_name='default'
            )
            m = dice_ml.Model(model=self.model, backend='sklearn', model_type='classifier')
            exp = dice_ml.Dice(d, m, method='random')
            
            # Create input instance
            input_df = pd.DataFrame([features])[self.feature_names]
            
            # Generate counterfactuals: find changes that flip to "no default" (class 0)
            cf = exp.generate_counterfactuals(
                input_df,
                total_CFs=num_cfs,
                desired_class=0,  # No default = approved
                features_to_vary=self.feature_names
            )
            
            # Parse results into readable paths
            paths = []
            cf_df = cf.cf_examples_list[0].final_cfs_df
            
            for _, row in cf_df.iterrows():
                changes = {}
                for feat in self.feature_names:
                    original = features.get(feat, 0)
                    new_val = row[feat]
                    if abs(new_val - original) > 0.001:
                        changes[feat] = {
                            "current": round(original, 4),
                            "target": round(new_val, 4),
                            "change": round(new_val - original, 4),
                            "advice": self._get_advice(feat, original, new_val)
                        }
                if changes:
                    paths.append(changes)
            
            return paths
            
        except Exception as e:
            import traceback
            traceback.print_exc()
            return [{"error": f"Could not generate counterfactuals: {str(e)}"}]

    def _get_advice(self, feature: str, current: float, target: float) -> str:
        """Convert feature changes to human-readable advice."""
        advice_map = {
            'income_stability': f"Maintain more consistent monthly income — reduce volatility from {current:.2f} to {target:.2f}.",
            'affordability_index': f"Reduce monthly expenses to increase disposable income ratio from {current:.0%} to {target:.0%}.",
            'nsf_frequency': f"Reduce low-balance alerts from {int(current)} to {int(target)} over the next 6 months.",
            'bill_payment_latency': f"Pay bills on time — reduce average delay from {current:.1f} to {target:.1f} days.",
            'network_centrality': "Diversify UPI transactions across more merchants to build economic footprint.",
            'time_to_zero_norm': f"Build a financial buffer — extend days before balance depletes from {current:.0%} to {target:.0%} of month.",
            'debt_to_income': f"Reduce existing EMI obligations from {current:.0%} to {target:.0%} of monthly income.",
            'txn_freq_norm': f"Increase regular transaction activity from {current:.0%} to {target:.0%} capacity."
        }
        return advice_map.get(feature, f"Adjust {feature} from {current} to {target}")

    def calculate_kfs(self, amount: float, default_probability: float) -> Dict:
        """Calculates Key Fact Statement (KFS) as per RBI guidelines."""
        approval_probability = 1.0 - default_probability
        risk_premium = default_probability * 14.0  # 0-14% based on risk
        interest_rate = 12.0 + risk_premium  # Base 12% + premium
        
        processing_fee = amount * 0.02
        
        # Monthly EMI calculation (simple for PoC)
        tenure_months = 12
        monthly_rate = interest_rate / 100 / 12
        emi = amount * monthly_rate * (1 + monthly_rate)**tenure_months / ((1 + monthly_rate)**tenure_months - 1)
        
        total_repayment = emi * tenure_months
        total_interest = total_repayment - amount
        apr = interest_rate + 2.0  # APR includes processing fee impact
        
        return {
            "requested_amount": amount,
            "interest_rate_pa": round(interest_rate, 2),
            "apr": round(apr, 2),
            "processing_fee": round(processing_fee, 2),
            "monthly_emi": round(emi, 2),
            "tenure_months": tenure_months,
            "total_repayment": round(total_repayment, 2),
            "total_interest": round(total_interest, 2),
            "repayment_frequency": "Monthly"
        }

    def save_audit_log(self, application_id: str, decision: str, probability: float, 
                       shap_values: Dict, reasons: List):
        client = get_supabase_client()
        return client.table("audit_log").insert({
            "application_id": application_id,
            "decision": decision,
            "approval_probability": probability,
            "shap_values": json.dumps(shap_values),
            "reason_codes": json.dumps(reasons),
            "model_version": "v3.0-improved-dataset"
        }).execute()
