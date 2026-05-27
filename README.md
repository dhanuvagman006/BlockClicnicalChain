# Novel ML-Integrated Private Blockchain for Securing Clinical Trials Data

[![Python](https://img.shields.io/badge/Python-3.14-blue)](https://python.org)
[![FastAPI](https://img.shields.io/badge/FastAPI-0.111-green)](https://fastapi.tiangolo.com)
[![React](https://img.shields.io/badge/React-18-61dafb)](https://reactjs.org)
[![Solidity](https://img.shields.io/badge/Solidity-0.8.19-purple)](https://soliditylang.org)
[![XGBoost](https://img.shields.io/badge/XGBoost-2.0-orange)](https://xgboost.readthedocs.io)

A complete, end-to-end private blockchain system that secures clinical trial data using SHA-256 cryptographic hashing, role-based node participation, 8 ML fraud-detection models, Ethereum smart contracts, IPFS off-chain storage, and AI-driven governance.

---

## Architecture Overview

```
[Drug Inventor UI] ──CSV Upload──► [Step 1: Data Ingestion]
                                          │
                                          ▼
                               [Step 2: SHA-256 Hashing]
                                  (Avalanche Effect Demo)
                                          │
                                          ▼
                               [Step 3: Transaction Creation]
                                  TX = {Trial_ID, Hash, Node, CID}
                                          │
                                          ▼
                        ┌─────────────────┴──────────────────┐
                        │      Step 4: Role-Based Nodes       │
                        │  PROTOCOL_VALIDATOR │ CONSENT_VERIFIER │ COMPLIANCE_AUDITOR
                        └─────────────────┬──────────────────┘
                                          │
                                          ▼
                        ┌─────────────────┴──────────────────┐
                        │    Step 5: ML Verification Gate     │
                        │  LR │ SVM │ DT │ RF │ KNN │ NB    │
                        │           XGBoost (best) │ ANN    │
                        └──────────VALID────────MANIPULATED──┘
                                          │                 │
                                     (Accept)          (Reject & Flag)
                                          │
                                          ▼
                        [Step 6: Smart Contract Protocol Check]
                         Phase sequence │ Dropout rate │ Consent
                                          │
                                          ▼
                        [Step 7/8: PoA/DPoS Consensus]
                         Reputation-weighted voting (NODE-01: 97%)
                                          │
                                          ▼
                        [Step 9: Append to Blockchain]
                         {PrevHash │ MerkleRoot │ Timestamp │ ValidatorSig}
                                          │
                                 ┌────────┴────────┐
                          [Step 10: IPFS]      [On-chain: CID + Hash]
                           Raw data off-chain   Metadata on-chain
                                          │
                                          ▼
                        [Step 11: Compliance Audit Node]
                         HIPAA │ GDPR │ GCP (read-only)
                                          │
                                          ▼
                        [Step 12: AI Governance Engine]
                         Monitor drift → adjust scores → update consensus
```

---

## Project Structure

```
Blockchain/
├── backend/                  # FastAPI server (Steps 1–4, 7–12)
│   ├── main.py              # All REST API endpoints
│   ├── hashing.py           # SHA-256, avalanche, tamper detection
│   ├── transaction.py       # Transaction model & mempool
│   └── nodes.py             # RBAC node registry
├── blockchain/              # Private chain implementation
│   ├── chain.py             # Block structure, append, verify, tamper demo
│   ├── consensus.py         # PoA / DPoS consensus engine
│   └── governance.py        # AI governance feedback loop
├── contracts/               # Solidity smart contracts
│   ├── ClinicalTrialRegistry.sol  # RBAC + protocol enforcement
│   ├── scripts/deploy.js    # Hardhat deployment
│   └── package.json         # Hardhat config
├── ml/                      # ML training pipeline
│   ├── train_models.py      # All 8 models + evaluation + plots
│   ├── saved_models/        # Serialized models (post-training)
│   └── plots/               # ROC curves, comparison charts
├── ipfs/                    # IPFS integration
│   └── ipfs_client.py       # Upload/retrieve, on-chain linking
├── frontend-app/            # React.js dashboard
│   └── src/
│       ├── pages/           # Dashboard, InventorPortal, TxExplorer,
│       │                    # MLPanel, RoleManagement, AuditLog
│       ├── components/      # Sidebar
│       └── api.js           # Axios API client
├── dataset/
│   ├── generate_dataset.py  # Synthetic clinical trial data generator
│   └── clinical_trials.csv  # Generated 2000-record dataset
├── docs/                    # Architecture docs
└── requirements.txt         # Python dependencies
```

---

## Quick Start

### Prerequisites
- Python 3.10+
- Node.js 18+
- (Optional) IPFS daemon for real IPFS storage
- (Optional) Ganache / Hardhat node for on-chain smart contracts

### 1. Install Python Dependencies
```bash
pip3 install --break-system-packages -r requirements.txt
# or with venv:
python3 -m venv venv && source venv/bin/activate && pip install -r requirements.txt
```

### 2. Generate Dataset
```bash
python3 dataset/generate_dataset.py
# → clinical_trials.csv (2000 records, ~23% manipulated)
```

### 3. Train ML Models (Step 5)
```bash
cd ml && python3 train_models.py
# Trains all 8 models, saves to ml/saved_models/
# Generates plots in ml/plots/
# Expected: XGBoost F1≈94%, AUC≈0.97
```

### 4. Start Backend API
```bash
python3 -m uvicorn backend.main:app --host 0.0.0.0 --port 8000 --reload
# → http://localhost:8000
# → http://localhost:8000/docs (Swagger UI)
```

### 5. Start Frontend Dashboard
```bash
cd frontend-app && npm start
# → http://localhost:3000
```

### 6. Deploy Smart Contracts (Optional)
```bash
# Start Ganache first, then:
cd contracts && npm install && npm run compile && npm run deploy
```

---

## Deployment

### Render backend

Deploy the repository root as a Render web service using the included [render.yaml](render.yaml). The backend listens on Render's `$PORT` automatically.

Set this environment variable in Render:

- `CORS_ORIGINS` to your Vercel frontend origin, for example `https://your-app.vercel.app`

### Vercel frontend

Deploy [frontend-app](frontend-app) as the Vercel project root. Set this environment variable in Vercel:

- `REACT_APP_API_URL` to your Render backend URL, for example `https://your-backend.onrender.com`

The frontend uses [frontend-app/src/api.js](frontend-app/src/api.js) to read that value at build time.

---

## All 12 Steps — Implementation Summary

| Step | Feature | Module |
|------|---------|--------|
| 1 | Dataset ingestion & schema validation | `backend/main.py /api/dataset/upload` |
| 2 | SHA-256 hashing, avalanche demo, tamper detection | `backend/hashing.py` |
| 3 | Transaction creation & mempool | `backend/transaction.py` |
| 4 | RBAC nodes: Protocol Validator, Consent Verifier, Compliance Auditor | `backend/nodes.py` |
| 5 | 8 ML models: LR, SVM, DT, RF, KNN, NB, XGBoost, ANN | `ml/train_models.py` |
| 6 | Solidity smart contracts: phase enforcement, consent, RBAC | `contracts/ClinicalTrialRegistry.sol` |
| 7 | PoA consensus with reputation-weighted voting | `blockchain/consensus.py` |
| 8 | DPoS delegate election | `blockchain/consensus.py::DPoSElection` |
| 9 | Append blocks with Merkle root + tamper-proof demo | `blockchain/chain.py` |
| 10 | IPFS upload + on-chain CID linking | `ipfs/ipfs_client.py` |
| 11 | Compliance audit log (HIPAA/GDPR/GCP) | `backend/main.py /api/governance/actions` |
| 12 | AI governance: drift detection, score updates | `blockchain/governance.py` |

---

## ML Models — Expected Performance

| Model | F1 | AUC-ROC |
|-------|----|----|
| XGBoost 🏆 | 94.1% | 0.97 |
| Random Forest | 93.4% | 0.96 |
| ANN (MLP) | 91.2% | 0.95 |
| SVM (RBF) | 89.5% | 0.93 |
| Gradient Boosting | 90.1% | 0.94 |
| Decision Tree | 84.7% | 0.88 |
| Logistic Regression | 82.3% | 0.87 |
| KNN (K=5) | 81.6% | 0.86 |
| Naive Bayes | 79.4% | 0.85 |

---

## API Endpoints

| Method | Endpoint | Description |
|--------|----------|-------------|
| GET | `/` | Service info + node/chain stats |
| POST | `/api/dataset/upload` | CSV upload & schema validation |
| POST | `/api/hash/compute` | SHA-256 of any data |
| POST | `/api/hash/avalanche` | Avalanche effect demo |
| POST | `/api/hash/verify` | VALID/TAMPERED detection |
| POST | `/api/transactions/submit` | Add TX to mempool |
| GET | `/api/transactions/pending` | List pending TXs |
| POST | `/api/blockchain/mine` | Mine pending TXs into block |
| GET | `/api/blockchain/chain` | Full chain summary |
| GET | `/api/blockchain/verify` | Chain integrity check |
| POST | `/api/consensus/propose` | Propose block for consensus |
| POST | `/api/consensus/vote` | Cast consensus vote |
| POST | `/api/ml/predict` | XGBoost fraud prediction |
| GET | `/api/ml/summary` | All model evaluation results |
| GET | `/api/nodes` | List network nodes |
| POST | `/api/nodes/register` | Register new node with role |
| POST | `/api/ipfs/upload` | Upload to IPFS + link on-chain |
| GET | `/api/governance/health` | AI governance health report |
| GET | `/api/metrics` | API performance metrics |

Full interactive docs: **http://localhost:8000/docs**

---

## Smart Contract Functions (Solidity)

- `registerNode(address, role, org)` — Admin registers a node
- `submitTrial(trialId, dataHash, ipfsCid, dropoutRate, mlApproved, compliance)` — Submit trial
- `verifyConsent(trialId, consentHash)` — Consent Verifier signs off
- `approveAndActivate(trialId)` — Protocol Validator activates trial
- `advancePhase(trialId)` — Enforce Phase I→II→III→IV sequence
- `haltTrial(trialId, reason)` — Emergency halt with event emission
- `appendBlock(merkleRoot, txIds)` — On-chain block record
- `auditTrial(trialId, action)` — Compliance Auditor read-only log
- `consensusWeight(nodeAddr)` — Returns reputation-weighted vote power

---

## Dataset Fields

| Field | Type | Description |
|-------|------|-------------|
| trial_id | string | NCT-format trial identifier |
| patient_id | string | Hashed before going on-chain |
| age_group | enum | `<18`, `18-35`, `36-50`, `51-65`, `65+` |
| drug_name | string | Drug under study (hashed on-chain) |
| dosage_level_mg | float | Dosage in mg (hashed on-chain) |
| phase | enum | Clinical phase `I`–`IV` |
| response_time_days | int | Trial duration |
| adverse_event | enum | None/Mild/Moderate/Severe/Life-threatening |
| adverse_event_flag | 0/1 | Binary adverse event indicator |
| consent_hash | string | SHA-256 of patient consent |
| timestamp | ISO8601 | Record creation time |
| node_id | string | Submitting network node |
| manipulated | 0/1 | **Target**: 0=Valid, 1=Manipulated |

---

## References

- [ClinicalTrials.gov](https://clinicaltrials.gov/)
- [HIPAA](https://www.hhs.gov/hipaa/index.html)
- [Clinical Trial Phases](https://www.zeclinics.com/blog/clinical-trial-phases-fda-approval/)
- [Original GitHub Reference](https://github.com/PrathamPShetty/medicine-trial.git)
