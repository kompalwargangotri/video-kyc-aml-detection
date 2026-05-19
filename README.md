# YOLO-Based Real-Time Identity Verification and Financial Fraud Detection System

SecureFin is a production-grade identity verification (KYC) and transaction monitoring (AML) compliance framework. It combines deep learning computer vision, optical character recognition (OCR), and machine learning anomaly detection to prevent identity spoofing and financial fraud.

## Key Features

- **Advanced Identity Verification Pipeline**:
  - Optical Character Recognition (OCR) for document validation (Aadhaar, PAN).
  - Face matching between ID document and real-time capture.
  - YOLO-based multi-person detection to prevent spoofing.
  - Guided liveness challenge with text-to-action prompts.
- **Financial Anomaly Detection (AML Engine)**:
  - Isolation Forest model combined with customizable business rules.
  - Real-time decisioning: `ALLOW`, `REVIEW`, or `BLOCK`.
- **Advanced Security & Hardening**:
  - Automated plaintext-to-bcrypt hashing migration routine for user passwords.
  - Dynamic cryptographically secure JWT and encryption key generation in `.env`.
  - Advanced AES/Fernet encryption for all uploaded PII documents.
  - Multi-threaded SQLite handling (`check_same_thread=False`).
- **Research Analytics & Metrics Suite**:
  - Live performance, distribution, and confidence charts are directly generated to the `research_graphs/` folder for use in research papers.

## Project Structure

```text
securefin_project/
├── backend/
│   ├── main.py
│   ├── aml.py
│   ├── kyc.py
│   ├── liveness.py
│   ├── ocr.py
│   ├── train_aml_model.py
│   ├── evaluate_aml_model.py
│   ├── evaluate_kyc_metrics.py
│   ├── aml_model.pkl
│   └── uploads/
├── frontend/
│   ├── index.html
│   ├── script.js
│   └── styles.css
├── database/
│   └── securefin.db
├── research_graphs/
│   ├── aml_scatter.png
│   ├── aml_distribution.png
│   ├── kyc_confidence.png
│   ├── kyc_status_distribution.png
│   ├── kyc_validation_parameters.png
│   └── aml_confusion_matrix.png
├── frontend_server.py
├── generate_graphs.py
├── run_project.ps1
└── README.md
```

## Tech Stack

- **Backend**: FastAPI, Uvicorn
- **Frontend**: HTML, CSS (Inter Typography + Responsive Glassmorphism), JavaScript
- **AML Engine**: scikit-learn (IsolationForest)
- **Computer Vision & OCR**: YOLOv8, Tesseract OCR via `pytesseract`
- **Database**: SQLite (SQLAlchemy & direct cursor handling)

## Setup & Running the Project

### 1. Prerequisite Checklist

- Python 3.10+
- Tesseract OCR installed on your system PATH (`C:\Program Files\Tesseract-OCR\tesseract.exe`)

### 2. Launching the Application

Execute the following one-click PowerShell script from the inner project folder to launch both frontend and backend:

```powershell
.\run_project.ps1
```

If script execution is disabled on your system, run:

```powershell
Set-ExecutionPolicy -Scope Process Bypass
.\run_project.ps1
```

Once running:

- **Backend**: `http://127.0.0.1:8000`
- **Frontend**: `http://127.0.0.1:5500`

## System Default Login Accounts

- **Agent**: `agent01` | Password: `agent123`
- **Reviewer**: `reviewer01` | Password: `review123`

## Performance Evaluation & Research Graphs

The platform is designed to instantly compute evaluation metrics. All outputs are automatically stored in the **`research_graphs/`** directory.

To update the graphs from live database records:

```powershell
# Updates ML evaluation metrics
python backend/evaluate_aml_model.py

# Updates KYC performance metrics
python backend/evaluate_kyc_metrics.py

# Generates real-time live database charts
python generate_graphs.py
```

## Authors

- **Gangotri Kompalwar** (Dept. of E&Tc, Pune, India)
- **Prathamesh Gavhane** (Dept. of E&Tc, Pune, India)
- **Sudarshan Khatal** (Dept. of E&Tc, Pune, India)
- **Suraj Konda** (Dept. of E&Tc, Pune, India)
