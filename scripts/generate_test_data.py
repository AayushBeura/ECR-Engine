import pandas as pd
import numpy as np
import random
from datetime import datetime, timedelta

def generate_test_transactions(filename, num_transactions=60):
    start_date = datetime.now() - timedelta(days=90)
    
    transactions = []
    
    categories = ['grocery', 'food', 'utility', 'telecom', 'bill', 'entertainment', 'transfer']
    statuses = ['SUCCESS', 'SUCCESS', 'SUCCESS', 'SUCCESS', 'FAILED'] # 20% failure rate
    
    receivers = [f'user{i}@upi' for i in range(1, 15)]
    receivers += [f'merchant{i}@upi' for i in range(1, 10)]
    
    for i in range(num_transactions):
        txn_date = start_date + timedelta(days=random.randint(0, 90), hours=random.randint(0, 23))
        category = random.choice(categories)
        status = random.choice(statuses)
        amount = round(random.uniform(50, 5000), 2)
        receiver = random.choice(receivers)
        
        transactions.append({
            'transaction_id': f'TXN{random.randint(100000, 999999)}',
            'timestamp': txn_date.strftime('%Y-%m-%d %H:%M:%S'),
            'amount': amount,
            'status': status,
            'merchant_category': category,
            'receiver_upi_id': receiver,
            'sender_upi_id': 'testuser@upi'
        })
        
    df = pd.DataFrame(transactions)
    # Sort by timestamp
    df = df.sort_values(by='timestamp')
    df.to_csv(filename, index=False)
    print(f"Generated {filename} with {num_transactions} transactions.")

def generate_rejection_test_set(filename, num_transactions=20):
    start_date = datetime.now() - timedelta(days=90)
    
    transactions = []
    
    # We want to trigger a rejection:
    # 1. High NSF frequency (lots of FAILED transactions)
    # 2. No bill payments (increases latency penalty)
    # 3. Low network centrality (only sending to 1 or 2 receivers)
    
    categories = ['grocery', 'food', 'entertainment'] # No bills or utilities
    statuses = ['FAILED', 'FAILED', 'FAILED', 'SUCCESS'] # 75% failure rate (NSF)
    
    receivers = [f'user{i}@upi' for i in range(1, 3)] # Very low network centrality
    
    for i in range(num_transactions):
        txn_date = start_date + timedelta(days=random.randint(0, 90), hours=random.randint(0, 23))
        category = random.choice(categories)
        status = random.choice(statuses)
        amount = round(random.uniform(500, 2000), 2)
        receiver = random.choice(receivers)
        
        transactions.append({
            'transaction_id': f'TXN{random.randint(100000, 999999)}',
            'timestamp': txn_date.strftime('%Y-%m-%d %H:%M:%S'),
            'amount': amount,
            'status': status,
            'merchant_category': category,
            'receiver_upi_id': receiver,
            'sender_upi_id': 'testuser@upi'
        })
        
    df = pd.DataFrame(transactions)
    df = df.sort_values(by='timestamp')
    df.to_csv(filename, index=False)
    print(f"Generated {filename} with {num_transactions} transactions (High Risk).")

if __name__ == "__main__":
    generate_test_transactions("datasets/test_transactions_rich.csv", 160)
    generate_test_transactions("datasets/test_transactions_medium.csv", 60)
    generate_test_transactions("datasets/test_transactions_thin.csv", 5)
    generate_rejection_test_set("datasets/test_transactions_rejection.csv", 30)
