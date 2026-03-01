from utils.supabase_utils import get_supabase_client

def initiate_disbursement(application_id: str, amount: float):
    try:
        client = get_supabase_client()
        # 1. Insert intent into shadow_ledger
        client.table("shadow_ledger").insert({
            "application_id": application_id,
            "intent_amount": amount,
            "status": "PENDING"
        }).execute()
        
        # 2. Mock external bank call (Simulating direct fund flow)
        # In a real scenario, this would be an API call to a Regulated Entity (Bank)
        print(f"DEBUG: Initiating mock disbursement of {amount} for app {application_id}")
        
        # Simulate a successful bank transaction
        bank_txn_id = f"BANK-TXN-{application_id[:8]}" 
        
        # 3. Update ledger on confirmation
        return client.table("shadow_ledger").update({
            "status": "SUCCESS",
            "bank_txn_id": bank_txn_id
        }).eq("application_id", application_id).execute()

    except Exception as e:
        print(f"Error in shadow ledger disbursement: {str(e)}")
        # In a real environment, send to Dead Letter Queue or trigger an alert
        return False
