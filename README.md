# PROVE — Proof Builder & Evidence Intelligence

**PROVE** is a full-stack, evidence-based skill verification and intelligence system. It takes claimed skills, background experience, project details, and evidence links; extracts structured facts using LLM natural language understanding; deterministically maps evidence to skills (`PROVEN`, `IMPLIED`, `CLAIMED`, `UNPROVEN`); evaluates proficiency on an explicit **L0–L5 model**; scores evidence quality across **7 distinct dimensions**; pinpoints proof gaps; constructs actionable project-based proof plans; and generates structured, persistent **Proof Artifacts** stored in SQLite.

---

## 🚀 Features

- **LLM Fact Extraction**: Uses Gemini API (or a deterministic offline Mock Provider) to extract structured **Actions, Tools, Outputs, and Outcomes** without blindly trusting user claims.
- **Deterministic Skill Classification**: Classifies claimed skills into:
  - `PROVEN`: Direct personal evidence supporting meaningful skill usage.
  - `IMPLIED`: Indirect evidence suggesting skill usage in environment context.
  - `CLAIMED`: Skill claimed by user without supporting evidence in text.
  - `UNPROVEN`: Insufficient claim or evidence.
- **L0–L5 Proficiency Model**:
  - `L0`: No evidence
  - `L1`: Awareness / basic exposure
  - `L2`: Basic practical usage
  - `L3`: Independent practical usage
  - `L4`: Advanced / complex application
  - `L5`: Expert / deep ownership
- **7-Dimension Evidence Quality Engine**:
  - Relevance (20%)
  - Depth (15%)
  - Ownership (15%)
  - Outcome (15%)
  - Verifiability (15%)
  - Recency (10%)
  - Transferability (10%)
  - Overall Quality Labels: `Weak` (0–39), `Moderate` (40–69), `Strong` (70–84), `Very Strong` (85–100).
- **Proof Gap Intelligence & Proof Builder**: Identifies exact skill deficits and builds concrete, project-based proof blueprints with deliverables, difficulty, effort estimates, and evidence venues.
- **Persistent Proof Artifacts**: Saves structured records to SQLite with unique IDs and exportable markdown artifacts with one-click clipboard copying.
- **Zero-Cost / Dual Provider**: Runs out-of-the-box using the built-in `MockProvider` without requiring paid or external API keys, while supporting the free-tier Gemini API (`gemini-2.5-flash`).

---

## 🛠️ Tech Stack

- **Frontend**: React 18, TypeScript, Vite, Tailwind CSS, Lucide Icons.
- **Backend**: Python 3.12, FastAPI, Pydantic V2, SQLAlchemy.
- **Database**: SQLite.
- **LLM Layer**: Abstracted LLM Provider (`GeminiProvider` via `google-genai` free tier & fallback `MockProvider`).
- **Testing**: pytest & evaluation suite (`tests/evaluation_cases.json`).

---

## 📁 Directory Structure

```
prove/
├── README.md
├── architecture.md
├── .gitignore
├── .env.example
├── backend/
│   ├── app/
│   │   ├── api/routes/proof.py
│   │   ├── core/config.py
│   │   ├── db/database.py & models.py
│   │   ├── schemas/proof.py, evidence.py, assessment.py
│   │   ├── services/
│   │   │   ├── llm_service.py
│   │   │   ├── gemini_provider.py
│   │   │   ├── mock_provider.py
│   │   │   ├── evidence_extractor.py
│   │   │   ├── skill_mapper.py
│   │   │   ├── evidence_scorer.py
│   │   │   ├── proof_gap.py
│   │   │   └── proof_builder.py
│   │   └── prompts/
│   │       ├── extraction_prompt.txt
│   │       └── proof_builder_prompt.txt
│   ├── tests/
│   │   ├── test_extraction.py
│   │   ├── test_skill_mapping.py
│   │   ├── test_evidence_scoring.py
│   │   ├── test_proof_gap.py
│   │   ├── test_proof_builder.py
│   │   ├── test_api.py
│   │   └── test_evaluation_cases.py
│   ├── requirements.txt
│   └── .env
├── frontend/
│   ├── src/
│   │   ├── components/
│   │   │   ├── Header.tsx
│   │   │   ├── ProofInputForm.tsx
│   │   │   ├── LoadingProgress.tsx
│   │   │   ├── AnalysisResults.tsx
│   │   │   ├── SkillAssessmentCards.tsx
│   │   │   ├── EvidenceQualityBreakdown.tsx
│   │   │   ├── ProofGapSection.tsx
│   │   │   ├── ProofBuilderSection.tsx
│   │   │   └── ProofArtifactView.tsx
│   │   ├── services/api.ts
│   │   ├── types/proof.ts
│   │   ├── App.tsx
│   │   ├── main.tsx
│   │   └── index.css
│   ├── package.json
│   ├── tsconfig.json
│   └── vite.config.ts
└── tests/
    └── evaluation_cases.json
```

---

## ⚡ Quick Start

### 1. Environment Setup

Copy `.env.example` to `backend/.env`:

```bash
# Set LLM_PROVIDER to 'mock' (default) or 'gemini'
LLM_PROVIDER=mock

# Gemini API Key (Only needed if LLM_PROVIDER=gemini)
GEMINI_API_KEY=your_gemini_api_key_here

DATABASE_URL=sqlite:///./prove.db
PORT=8000
HOST=0.0.0.0
```

### 2. Backend Setup & Server Execution

```bash
cd backend
python -m pip install -r requirements.txt
python -m uvicorn app.main:app --reload --port 8000
```
Backend API interactive documentation is available at `http://localhost:8000/docs`.

### 3. Frontend Setup & Dev Server

```bash
cd frontend
npm install
npm run dev
```
Open `http://localhost:3000` in your browser.

---

## 🧪 Running Tests

To run the complete test suite (unit tests, API integration tests, and 8 evaluation cases):

```bash
cd backend
python -m pytest -v
```

---

## 🔌 API Endpoints

| Method | Endpoint | Description |
| shadow | --- | --- |
| `POST` | `/api/proof/analyze` | Executes extraction, skill mapping, scoring, gap analysis, persists in SQLite, and returns Proof Artifact |
| `POST` | `/api/proof/build` | Generates a targeted Proof Plan for a specific skill gap |
| `GET` | `/api/proof/{id}` | Retrieves a persisted Proof Record and constructs its full Proof Artifact |
| `GET` | `/api/proof` | Lists recent proof records |
| `GET` | `/api/health` | Returns backend health and active LLM provider configuration |

---

## 🎯 Scoring & Guardrails

- **No Scoring Hallucination**: The LLM is used strictly for natural language parsing and concrete proof plan text generation. Skill classification, proficiency calculation, and 7-dimension scoring are executed in deterministic Python logic.
- **Factual Guardrails**: Unverified user statements (e.g., "I increased sales by 40%") remain unverified claims and receive low verifiability scores unless accompanied by public links or verified proof sources.
