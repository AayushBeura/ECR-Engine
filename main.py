from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel, Field
from typing import Dict, Optional, List
import os
import uuid
from dotenv import load_dotenv

from utils.encryption import encrypt_data, generate_key
from utils.supabase_utils import get_supabase_client, insert_profile, create_application
from utils.shadow_ledger import initiate_disbursement
from services.credit_service import CreditService

load_dotenv()

app = FastAPI(title="Explainable Credit Risk Engine API")

# Flag to bypass the Supabase database for initial PoC testing
MOCK_DB = False

# CORS — allow all origins for standalone HTML frontend
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=False,
    allow_methods=["*"],
    allow_headers=["*"],
)

credit_service = CreditService()

# --- Request Models ---

class Features(BaseModel):
    """Typed features model with validation."""
    income_stability: float
    affordability_index: float
    nsf_frequency: int = Field(..., description="Must be integer")
    bill_payment_latency: float
    network_centrality: float
    # Optional / engineered features
    time_to_zero_norm: Optional[float] = None
    debt_to_income: Optional[float] = None
    txn_freq_norm: Optional[float] = None


class ApplicationRequest(BaseModel):
    user_id: str
    pan: str
    aadhaar: Optional[str] = None
    full_name: str
    amount: float
    features: Optional[Features] = None
    transaction_data: Optional[List[Dict]] = None

class CounterfactualRequest(BaseModel):
    features: Dict[str, float]
    num_paths: Optional[int] = 3

class PredictRequest(BaseModel):
    features: Dict[str, float]

# --- Endpoints ---

@app.get("/")
def read_root():
    return {"message": "Explainable Credit Risk Engine API", "version": "2.0"}

@app.post("/predict")
async def predict_only(request: PredictRequest):
    """Get a credit decision without creating a full application."""
    try:
        result = credit_service.predict(request.features)
        return result
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@app.post("/apply")
async def apply_for_loan(request: ApplicationRequest):
    """Full loan application: encrypts PII, runs ML, logs audit, calculates KFS."""
    try:
        try:
            client = get_supabase_client() if not MOCK_DB else None
        except Exception as e:
            print(f"Warning: Supabase connection failed or bypassed. using mock DB mode. {e}")
            client = None

        encryption_key = os.getenv("ENCRYPTION_KEY")
        
        if not encryption_key:
            encryption_key = generate_key()
            print(f"WARNING: ENCRYPTION_KEY not set. Using temporary key.")

        # 1. Encrypt PII
        pan_enc = encrypt_data(request.pan, encryption_key)
        aadhaar_enc = encrypt_data(request.aadhaar, encryption_key) if request.aadhaar else None
        
        # 2. Store Profile
        if client:
            insert_profile(client, request.user_id, pan_enc, aadhaar_enc, request.full_name)
        
        # 3. Create Application
        if request.transaction_data:
            from services.credit_service import CreditService
            features_dict = credit_service.process_transactions(request.transaction_data, request.amount)
            credit_service.autotune_weights(len(request.transaction_data))
        elif request.features:
            features_dict = request.features.model_dump()
            # Default None optional features to 0.0 for ML model compatibility
            for key in features_dict:
                if features_dict[key] is None:
                    features_dict[key] = 0.0
        else:
            raise HTTPException(status_code=400, detail="Must provide either features or transaction_data")

        features_dict["nsf_frequency"] = int(features_dict.get("nsf_frequency", 0))

        if client:
            app_resp = create_application(client, request.user_id, request.amount, status="UNDERWRITING", features=features_dict)
            application_id = app_resp.data[0]["id"]
        else:
            application_id = str(uuid.uuid4())
        
        # 4. Get Credit Decision
        result = credit_service.predict(features_dict)
        
        # 5. Save Audit Log
        if client:
            credit_service.save_audit_log(
                application_id, 
                result["decision"], 
                result["probability"], 
                result["shap_values"], 
                result["reason_codes"]
            )
        
        # 6. Generate KFS if approved, counterfactuals if rejected
        kfs = None
        paths_to_approval = None
        
        if result["decision"] == "APPROVED":
            kfs = credit_service.calculate_kfs(request.amount, result["default_probability"])
            if client:
                client.table("loan_applications").update({
                    "status": "APPROVED",
                    "kfs_json": kfs,
                    "approved_rate": kfs["interest_rate_pa"]
                }).eq("id", application_id).execute()

                # Initiate Disbursement (Shadow Ledger)
                initiate_disbursement(application_id, request.amount)
        else:
            if client:
                client.table("loan_applications").update({
                    "status": "REJECTED"
                }).eq("id", application_id).execute()
            
            # Generate Paths to Approval for rejected applicants
            paths_to_approval = credit_service.generate_counterfactuals(features_dict)

        return {
            "application_id": application_id,
            "decision": result["decision"],
            "approval_probability": result["probability"],
            "default_probability": result["default_probability"],
            "shap_values": result["shap_values"],
            "reasons": result["reason_codes"],
            "kfs": kfs,
            "paths_to_approval": paths_to_approval
        }

    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@app.post("/counterfactuals")
async def get_counterfactuals(request: CounterfactualRequest):
    """Generate 'Paths to Approval' for a given feature set."""
    try:
        paths = credit_service.generate_counterfactuals(request.features, request.num_paths)
        return {"paths_to_approval": paths}
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@app.get("/config/generate-key")
def get_new_key():
    """Generate a new encryption key for .env setup."""
    return {"encryption_key": generate_key()}
