PS C:\Users\ashmi\OneDrive\Desktop\MinorSem6> .\venv\Scripts\activate; pip install kaggle
Collecting kaggle
  Downloading kaggle-2.0.0-py3-none-any.whl.metadata (15 kB)
Collecting bleach (from kaggle)
  Using cached bleach-6.3.0-py3-none-any.whl.metadata (31 kB)
Collecting kagglesdk<1.0,>=0.1.15 (from kaggle)
  Downloading kagglesdk-0.1.15-py3-none-any.whl.metadata (13 kB)
Requirement already satisfied: packaging in c:\users\ashmi\onedrive\desktop\minorsem6\venv\lib\site-packages (from kaggle) (26.0)
Collecting protobuf (from kaggle)
  Downloading protobuf-6.33.5-cp310-abi3-win_amd64.whl.metadata (593 bytes)
Requirement already satisfied: python-dateutil in c:\users\ashmi\onedrive\desktop\minorsem6\venv\lib\site-packages (from kaggle) (2.9.0.post0)
Collecting python-slugify (from kaggle)
  Using cached python_slugify-8.0.4-py2.py3-none-any.whl.metadata (8.5 kB)
Requirement already satisfied: requests in c:\users\ashmi\onedrive\desktop\minorsem6\venv\lib\site-packages (from kaggle) (2.32.5)
Requirement already satisfied: tqdm in c:\users\ashmi\onedrive\desktop\minorsem6\venv\lib\site-packages (from kaggle) (4.67.3)
Requirement already satisfied: urllib3>=1.15.1 in c:\users\ashmi\onedrive\desktop\minorsem6\venv\lib\site-packages (from kaggle) (2.6.3)   
Collecting webencodings (from bleach->kaggle)
  Using cached webencodings-0.5.1-py2.py3-none-any.whl.metadata (2.1 kB)
Requirement already satisfied: six>=1.5 in c:\users\ashmi\onedrive\desktop\minorsem6\venv\lib\site-packages (from python-dateutil->kaggle) (1.17.0)
Collecting text-unidecode>=1.3 (from python-slugify->kaggle)
  Using cached text_unidecode-1.3-py2.py3-none-any.whl.metadata (2.4 kB)
Requirement already satisfied: charset_normalizer<4,>=2 in c:\users\ashmi\onedrive\desktop\minorsem6\venv\lib\site-packages (from requests->kaggle) (3.4.4)
Requirement already satisfied: idna<4,>=2.5 in c:\users\ashmi\onedrive\desktop\minorsem6\venv\lib\site-packages (from requests->kaggle) (3.11)
Requirement already satisfied: certifi>=2017.4.17 in c:\users\ashmi\onedrive\desktop\minorsem6\venv\lib\site-packages (from requests->kaggle) (2026.1.4)
Requirement already satisfied: colorama in c:\users\ashmi\onedrive\desktop\minorsem6\venv\lib\site-packages (from tqdm->kaggle) (0.4.6)    
Downloading kaggle-2.0.0-py3-none-any.whl (75 kB)
Downloading kagglesdk-0.1.15-py3-none-any.whl (160 kB)
Using cached bleach-6.3.0-py3-none-any.whl (164 kB)
Downloading protobuf-6.33.5-cp310-abi3-win_amd64.whl (437 kB)
Using cached python_slugify-8.0.4-py2.py3-none-any.whl (10 kB)
Using cached text_unidecode-1.3-py2.py3-none-any.whl (78 kB)
Using cached webencodings-0.5.1-py2.py3-none-any.whl (11 kB)
Installing collected packages: webencodings, text-unidecode, python-slugify, protobuf, bleach, kagglesdk, kaggle
Successfully installed bleach-6.3.0 kaggle-2.0.0 kagglesdk-0.1.15 protobuf-6.33.5 python-slugify-8.0.4 text-unidecode-1.3 webencodings-0.5.1

[notice] A new release of pip is available: 25.3 -> 26.0.1
[notice] To update, run: python.exe -m pip install --upgrade pip
(venv) PS C:\Users\ashmi\OneDrive\Desktop\MinorSem6> cd 'c:\Users\ashmi\OneDrive\Desktop\MinorSem6'
(venv) PS C:\Users\ashmi\OneDrive\Desktop\MinorSem6> ^C
(venv) PS C:\Users\ashmi\OneDrive\Desktop\MinorSem6> mkdir -Force $env:USERPROFILE\.kaggle; Copy-Item "c:\Users\ashmi\OneDrive\Documents\College\Sem6\kaggle.json" "$env:USERPROFILE\.kaggle\kaggle.json"

    Directory: C:\Users\ashmi

Mode                 LastWriteTime         Length Name
----                 -------------         ------ ----
d----          07-01-2026    21:09                .kaggle
                                                                                                                        
(venv) PS C:\Users\ashmi\OneDrive\Desktop\MinorSem6> ^C
(venv) PS C:\Users\ashmi\OneDrive\Desktop\MinorSem6> cd 'c:\Users\ashmi\OneDrive\Desktop\MinorSem6'
(venv) PS C:\Users\ashmi\OneDrive\Desktop\MinorSem6> ^C
(venv) PS C:\Users\ashmi\OneDrive\Desktop\MinorSem6> mkdir -Force data                                                                     

    Directory: C:\Users\ashmi\OneDrive\Desktop\MinorSem6

Mode                 LastWriteTime         Length Name
----                 -------------         ------ ----
d----          21-02-2026    21:38                data

(venv) PS C:\Users\ashmi\OneDrive\Desktop\MinorSem6> cd 'c:\Users\ashmi\OneDrive\Desktop\MinorSem6'
(venv) PS C:\Users\ashmi\OneDrive\Desktop\MinorSem6> ^C
(venv) PS C:\Users\ashmi\OneDrive\Desktop\MinorSem6> .\venv\Scripts\activate; kaggle datasets download -d laotse/credit-risk-dataset -p data/credit-risk --unzip
HTTPSConnectionPool(host='api.kaggle.com', port=443): Max retries exceeded with url: /v1/datasets.DatasetApiService/GetDatasetMetadata (Caused by NameResolutionError("HTTPSConnection(host='api.kaggle.com', port=443): Failed to resolve 'api.kaggle.com' ([Errno 11002] getaddrinfo failed)"))
(venv) PS C:\Users\ashmi\OneDrive\Desktop\MinorSem6> cd 'c:\Users\ashmi\OneDrive\Desktop\MinorSem6'
(venv) PS C:\Users\ashmi\OneDrive\Desktop\MinorSem6> .\venv\Scripts\activate; python data/generate_synthetic.py                            
Dataset generated: 5000 rows
Default rate: 25.00%

Feature summary:
       income_stability  affordability_index  nsf_frequency  bill_payment_latency  network_centrality
count          5000.000             5000.000       5000.000              5000.000            5000.000
mean              0.154                0.499          5.412                 3.076               0.241
std               0.038                0.105          2.794                 4.963               0.069
min               0.031                0.211          0.000               -10.000               0.020
25%               0.130                0.423          3.000                -0.330               0.200
50%               0.156                0.500          5.000                 3.055               0.240
75%               0.181                0.573          7.000                 6.490               0.280
max               0.268                0.789         15.000                22.580               0.520
(venv) PS C:\Users\ashmi\OneDrive\Desktop\MinorSem6> cd 'c:\Users\ashmi\OneDrive\Desktop\MinorSem6'
(venv) PS C:\Users\ashmi\OneDrive\Desktop\MinorSem6> .\venv\Scripts\activate; python training/train_model.py   
============================================================
EXPLAINABLE CREDIT RISK ENGINE — MODEL TRAINING
============================================================

Dataset: 5000 rows, Default rate: 25.00%
Train: 4000, Test: 1000

Monotonic constraints: {'income_stability': -1, 'affordability_index': -1, 'nsf_frequency': 1, 'bill_payment_latency': 1, 'network_centrality': -1}

--- Raw Model Performance ---
              precision    recall  f1-score   support

  No Default       0.83      0.93      0.87       750
     Default       0.65      0.41      0.50       250

    accuracy                           0.80      1000
   macro avg       0.74      0.67      0.69      1000
weighted avg       0.78      0.80      0.78      1000

AUC-ROC: 0.8307

Calibrated AUC-ROC: 0.8301
Calibrated mean probability: 0.2408 (actual default rate: 0.2500)

--- Feature Importance ---
  bill_payment_latency: 904
  affordability_index: 854
  nsf_frequency: 741
  network_centrality: 703
  income_stability: 0

✅ Saved: models/credit_model.pkl
✅ Saved: models/calibrator.pkl
✅ Saved: models/training_data.csv
✅ Saved: credit_model.pkl (root, backward compat)
(venv) PS C:\Users\ashmi\OneDrive\Desktop\MinorSem6> cd 'c:\Users\ashmi\OneDrive\Desktop\MinorSem6'
(venv) PS C:\Users\ashmi\OneDrive\Desktop\MinorSem6> $body = @{features = @{income_stability = 0.15; affordability_index = 0.5; nsf_frequency = 3; bill_payment_latency = 2.0; network_centrality = 0.3}} | ConvertTo-Json; Invoke-RestMethod -Uri http://127.0.0.1:8000/predict -Method Post -Body $body -ContentType 'application/json' | ConvertTo-Json -Depth 5
{
  "decision": "APPROVED",
  "probability": 0.9504,
  "default_probability": 0.0496,
  "shap_values": {
    "income_stability": 0.0,
    "affordability_index": 0.0991,
    "nsf_frequency": -1.0322,
    "bill_payment_latency": -0.0493,
    "network_centrality": -0.1729
  },
  "reason_codes": [
    "Limited disposable income relative to loan requirements."
  ]
}
(venv) PS C:\Users\ashmi\OneDrive\Desktop\MinorSem6> cd 'c:\Users\ashmi\OneDrive\Desktop\MinorSem6'
(venv) PS C:\Users\ashmi\OneDrive\Desktop\MinorSem6> $body = @{features = @{income_stability = 0.25; affordability_index = 0.22; nsf_frequency = 12; bill_payment_latency = 15.0; network_centrality = 0.05}} | ConvertTo-Json; Invoke-RestMethod -Uri http://127.0.0.1:8000/predict -Method Post -Body $body -ContentType 'application/json' | ConvertTo-Json -Depth 5
{
  "decision": "REJECTED",
  "probability": 0.0,
  "default_probability": 1.0,
  "shap_values": {
    "income_stability": 0.0,
    "affordability_index": 1.642,
    "nsf_frequency": 3.606,
    "bill_payment_latency": 1.8507,
    "network_centrality": 1.1945
  },
  "reason_codes": [
    "Frequent low-balance alerts indicate potential cash flow stress.",
    "History of delayed bill payments suggests risk.",
    "Limited disposable income relative to loan requirements."
  ]
}
(venv) PS C:\Users\ashmi\OneDrive\Desktop\MinorSem6> cd 'c:\Users\ashmi\OneDrive\Desktop\MinorSem6'
(venv) PS C:\Users\ashmi\OneDrive\Desktop\MinorSem6> $body = @{features = @{income_stability = 0.25; affordability_index = 0.22; nsf_frequency = 12; bill_payment_latency = 15.0; network_centrality = 0.05}; num_paths = 3} | ConvertTo-Json; Invoke-RestMethod -Uri http://127.0.0.1:8000/counterfactuals -Method Post -Body $body -ContentType 'application/json' | ConvertTo-Json -Depth 5
{
  "paths_to_approval": [
    {
      "affordability_index": {
        "current": 0.22,
        "target": 0.6881,
        "change": 0.4681,
        "advice": "Reduce monthly expenses to increase disposable income ratio from 22% to 69%."
      },
      "network_centrality": {
        "current": 0.05,
        "target": 0.39,
        "change": 0.34,
        "advice": "Diversify UPI transactions across more merchants to build economic footprint."
      }
    },
    {
      "nsf_frequency": {
        "current": 12.0,
        "target": 1.0,
        "change": -11.0,
        "advice": "Reduce low-balance alerts from 12 to 1 over the next 6 months."
      },
      "bill_payment_latency": {
        "current": 15.0,
        "target": 7.6,
        "change": -7.4,
        "advice": "Pay bills on time — reduce average delay from 15.0 to 7.6 days."
      }
    },
    {
      "nsf_frequency": {
        "current": 12.0,
        "target": 1.0,
        "change": -11.0,
        "advice": "Reduce low-balance alerts from 12 to 1 over the next 6 months."
      },
      "bill_payment_latency": {
        "current": 15.0,
        "target": 8.6,
        "change": -6.4,
        "advice": "Pay bills on time — reduce average delay from 15.0 to 8.6 days."
      }
    }
  ]
}