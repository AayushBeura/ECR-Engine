from utils.supabase_utils import get_supabase_client
from typing import Dict, Any, Optional
from datetime import datetime
import json

def get_client():
    try:
        return get_supabase_client()
    except Exception as e:
        print(f"Failed to get supabase client: {str(e)}")
        return None

def record_consent(user_id: str, purpose: str, purpose_details: str = '', metadata: Optional[Dict[str, Any]] = None) -> bool:
    """Record consent logically in a user's profile metadata or a dedicated consent table."""
    client = get_client()
    if not client:
        return False
        
    try:
        # Check if consent_ledger table exists, if we had one.
        # As per instructions, we integrate with supabase.
        # Assuming we might just add standard inserts into a consent_ledger table.
        # Supabase API format for insert
        consent_data = {
            "user_id": user_id,
            "purpose": purpose,
            "purpose_details": purpose_details,
            "status": "GRANTED",
            "metadata": json.dumps(metadata) if metadata else None,
            "recorded_at": datetime.utcnow().isoformat()
        }
        res = client.table("consent_ledger").insert(consent_data).execute()
        return len(res.data) > 0
    except Exception as e:
        print(f"Error recording consent: {str(e)}")
        # Fallback to local testing logic or error handling
        return False

def query_consent(user_id: str, purpose: Optional[str] = None) -> list:
    """Retrieve active consent records for a user."""
    client = get_client()
    if not client:
        return []
        
    try:
        query = client.table("consent_ledger").select("*").eq("user_id", user_id)
        if purpose:
            query = query.eq("purpose", purpose)
        res = query.execute()
        return res.data
    except Exception as e:
        print(f"Error querying consent: {str(e)}")
        return []

def revoke_consent(user_id: str, purpose: str) -> bool:
    """Revoke a previously granted consent."""
    client = get_client()
    if not client:
        return False
        
    try:
        consent_data = {
            "status": "REVOKED",
            "revoked_at": datetime.utcnow().isoformat()
        }
        res = client.table("consent_ledger").update(consent_data).eq("user_id", user_id).eq("purpose", purpose).execute()
        return len(res.data) > 0
    except Exception as e:
        print(f"Error revoking consent: {str(e)}")
        return False
