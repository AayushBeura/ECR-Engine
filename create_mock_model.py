import pandas as pd
import numpy as np
import lightgbm as lgb
import joblib
import os

def create_mock_model():
    # Synthetic data for mock training
    X = pd.DataFrame({
        'income_stability': np.random.rand(100),
        'affordability_index': np.random.rand(100),
        'nsf_frequency': np.random.randint(0, 5, 100),
        'bill_payment_latency': np.random.rand(100),
        'network_centrality': np.random.rand(100)
    })
    y = np.random.randint(0, 2, 100)

    # Monotonic constraints: Income (+), Volatility (-), NSF (-), Latency (-), Centrality (+)
    constraints = [1, 1, -1, -1, 1]
    
    model = lgb.LGBMClassifier(monotone_constraints=constraints)
    model.fit(X, y)
    
    joblib.dump(model, "credit_model.pkl")
    print("Mock model created and saved as credit_model.pkl")

if __name__ == "__main__":
    create_mock_model()
