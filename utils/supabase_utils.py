from supabase import create_client, Client
import os
from dotenv import load_dotenv

load_dotenv()

def get_supabase_client() -> Client:
    url = os.getenv("SUPABASE_URL")
    key = os.getenv("SUPABASE_KEY")
    if not url or not key:
        raise ValueError("SUPABASE_URL and SUPABASE_KEY must be set in .env")
    return create_client(url, key)

def insert_profile(client: Client, user_id: str, pan_encrypted: str, aadhaar_encrypted: str = None, full_name: str = None):
    data = {
        "id": user_id,
        "pan_encrypted": pan_encrypted,
        "aadhaar_encrypted": aadhaar_encrypted,
        "full_name": full_name
    }
    return client.table("profiles").upsert(data).execute()

def create_application(client: Client, user_id: str, amount: float, status: str = "DRAFT", features: dict = None):
    data = {
        "user_id": user_id,
        "requested_amount": amount,
        "status": status
    }
    if features:
        for key in ['income_stability', 'affordability_index', 'nsf_frequency',
                     'bill_payment_latency', 'network_centrality']:
            if key in features:
                data[key] = features[key]
    return client.table("loan_applications").insert(data).execute()
