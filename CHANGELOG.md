# Changelog

All notable changes to the Explainable Credit Risk Engine project will be documented in this file.

## [Unreleased] - 2026-03-26

### Fixed

#### Backend
- **CORS Configuration** - Added proper CORS middleware to allow frontend requests from `http://localhost:3000`
- **Debug Endpoint** - Added `/debug` endpoint for troubleshooting and testing
- **credit_service.py Validation** - Fixed validation errors in credit service logic
- **credit_service.py DiCE Errors** - Resolved DiCE counterfactual generation errors
- **requirements.txt** - Pinned all dependency versions for reproducible builds:
  - fastapi==0.115.6
  - uvicorn==0.34.0
  - supabase==2.11.0
  - cryptography==44.0.0
  - lightgbm==4.5.0
  - shap==0.46.0
  - joblib==1.4.2
  - pandas==2.2.3
  - numpy==1.26.4
  - python-dotenv==1.0.1
  - dice-ml==0.10.0
  - scikit-learn==1.6.0

#### Frontend
- **Frontend URL** - Fixed API base URL configuration to correctly point to backend
- **Clock AM/PM Display** - Fixed time formatting to properly show AM/PM indicators

#### Data Generation
- **generate_synthetic.py Broadcasting** - Fixed NumPy broadcasting errors in synthetic data generation

### Added
- **.env.example** - Created example environment file template for easier setup
- **GSD-STYLE.md** - Added GSD style guide documentation
- **PROJECT_RULES.md** - Added project rules and guidelines
- **scripts/** - Added validation and search scripts for project maintenance
- **adapters/** - Added adapters directory for future integrations
- **docs/** - Added documentation directory

### Changed
- **.env.template** - Updated template with improved comments and structure

---

## [1.0.0] - 2026-03-25

### Initial Release

#### Core Features
- **FastAPI Backend** - RESTful API with Swagger documentation
- **Supabase Integration** - PostgreSQL database with Row Level Security (RLS)
- **LightGBM ML Model** - Credit scoring with monotonic constraints for fairness
- **SHAP Explainability** - Reason codes for every credit decision
- **DiCE Counterfactuals** - Paths to approval for rejected applicants
- **KFS Engine** - Key Fact Statement calculator (RBI compliant)
- **Shadow Ledger** - Direct Fund Flow tracking
- **Consent Ledger** - DPDP Act 2023 compliance
- **PII Encryption** - AES-256 Fernet encryption for sensitive data

#### Database Schema
- `profiles` - User PII storage with encryption
- `loan_applications` - Application lifecycle tracking
- `audit_log` - Immutable decision ledger
- `shadow_ledger` - Fund flow intents
- `consent_ledger` - Consent grants/revocations

#### API Endpoints
- `GET /` - Health check
- `POST /predict` - Quick credit decision
- `POST /apply` - Full loan application
- `POST /counterfactuals` - Generate paths to approval
- `GET /config/generate-key` - Generate Fernet key
- `POST /consent/record` - Record DPDP consent
- `GET /consent/{user_id}` - Query consent records
- `POST /consent/revoke` - Revoke consent

#### Synthetic Dataset
- 5,000 borrower profiles mimicking India's informal economy
- 25% default rate with labeled ground truth
- Features: income stability, affordability index, NSF frequency, bill payment latency, network centrality

#### Model Performance
- AUC-ROC: 0.83
- Isotonic Regression calibration for true probability estimates

---

## Version History

| Version | Date | Description |
|---------|------|-------------|
| Unreleased | 2026-03-26 | Bug fixes and improvements |
| 1.0.0 | 2026-03-25 | Initial release |
