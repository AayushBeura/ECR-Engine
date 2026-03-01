from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel, Field
from typing import Dict, Optional
import os
from dotenv import load_dotenv

from utils.encryption import encrypt_data, generate_key
from utils.supabase_utils import get_supabase_client, insert_profile, create_application
from utils.shadow_ledger import initiate_disbursement
from services.credit_service import CreditService

load_dotenv()

app = FastAPI(title="Explainable Credit Risk Engine API")

# --------------------------------------------------
# CORS
# --------------------------------------------------
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=False,
    allow_methods=["*"],
    allow_headers=["*"],
)

credit_service = CreditService()

# --------------------------------------------------
# REQUEST MODELS
# --------------------------------------------------

class Features(BaseModel):
    income_stability: float
    affordability_index: float
    nsf_frequency: int = Field(..., description="Must be integer")
    bill_payment_latency: float
    network_centrality: float

    # optional / engineered
    time_to_zero_norm: Optional[float] = None
    debt_to_income: Optional[float] = None
    txn_freq_norm: Optional[float] = None


class ApplicationRequest(BaseModel):
    user_id: str
    pan: str
    aadhaar: Optional[str] = None
    full_name: str
    amount: float
    features: Features


class PredictRequest(BaseModel):
    features: Dict[str, float]


class CounterfactualRequest(BaseModel):
    features: Dict[str, float]
    num_paths: Optional[int] = 3


# --------------------------------------------------
# ROUTES
# --------------------------------------------------

@app.get("/")
def read_root():
    return {
        "message": "Explainable Credit Risk Engine API",
        "version": "2.0"
    }


@app.post("/predict")
async def predict_only(request: PredictRequest):
    try:
        return credit_service.predict(request.features)
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


@app.post("/apply")
async def apply_for_loan(request: ApplicationRequest):
    try:
        client = get_supabase_client()

        encryption_key = os.getenv("ENCRYPTION_KEY")
        if not encryption_key:
            encryption_key = generate_key()

        # Encrypt PII
        pan_enc = encrypt_data(request.pan, encryption_key)
        aadhaar_enc = encrypt_data(request.aadhaar, encryption_key) if request.aadhaar else None

        # Store Profile
        insert_profile(
            client,
            request.user_id,
            pan_enc,
            aadhaar_enc,
            request.full_name
        )

        # Normalize Features
        features_dict = request.features.dict()
        features_dict["nsf_frequency"] = int(features_dict["nsf_frequency"])

        # Create Application
        app_resp = create_application(
            client=client,
            user_id=request.user_id,
            amount=request.amount,
            status="UNDERWRITING",
            features=features_dict
        )

        application_id = app_resp.data[0]["id"]

        # ML Prediction
        result = credit_service.predict(features_dict)

        # ✅ FIXED: removed reason_codes parameter
        credit_service.save_audit_log(
            application_id,
            result["decision"],
            result["probability"],
            result["shap_values"],
            result["reason_codes"]
        )

        # Decision Handling
        kfs = None
        paths_to_approval = None

        if result["decision"] == "APPROVED":
            kfs = credit_service.calculate_kfs(
                request.amount,
                result["default_probability"]
            )

            client.table("loan_applications").update({
                "status": "APPROVED",
                "approved_rate": kfs["interest_rate_pa"],
                "kfs_json": kfs
            }).eq("id", application_id).execute()

            initiate_disbursement(application_id, request.amount)

        else:
            client.table("loan_applications").update({
                "status": "REJECTED"
            }).eq("id", application_id).execute()

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
    try:
        return {
            "paths_to_approval": credit_service.generate_counterfactuals(
                request.features,
                request.num_paths
            )
        }
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


@app.get("/config/generate-key")
def get_new_key():
    return {"encryption_key": generate_key()}