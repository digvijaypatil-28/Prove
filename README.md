# PROVE — Proof Builder & Evidence Intelligence

PROVE is a full-stack, evidence-based skill verification and intelligence system. It takes a user's claimed skills, background experience, project details, outcomes, and evidence links, parses them using a Large Language Model (LLM) for Natural Language Understanding (NLU), and then applies deterministic Python logic to verify, score, and map those claims to verifiable proof artifacts.

---

##  Selected Project

**PROVE — Proof Builder & Evidence Intelligence** was selected as the project for this assignment because it demonstrates:
*   **Full-Stack Engineering:** Combines a responsive, animated React + TypeScript frontend with a high-performance FastAPI backend.
*   **Hybrid AI Architecture:** Integrates LLM-based NLU for unstructured text parsing with deterministic Python business logic for assessments, scoring, and workflow controls.
*   **Relational Persistence:** Implements structured SQLAlchemy mapping to a local SQLite database for historical logging and retrieval.
*   **Quality & Gap Verification:** Calculates quality metrics across seven dimensions and produces actionable, targeted development plans to resolve evidence gaps.
*   **Production Readiness & Reliability:** Employs schema validation (Pydantic), error boundary retry states, and offline mock fallbacks for resilient operation.

---

##  Live Deployment

The application is deployed on the Render cloud platform:

*   **Frontend UI:** [https://prove-frontend.onrender.com/](https://prove-frontend.onrender.com/)
*   **Backend API Service:** [https://prove-backend.onrender.com/](https://prove-backend.onrender.com/)
*   **API Health Check:** [https://prove-backend.onrender.com/api/health](https://prove-backend.onrender.com/api/health)
*   **API Interactive Documentation (Swagger UI):** [https://prove-backend.onrender.com/docs](https://prove-backend.onrender.com/docs)

> [!NOTE]
> The backend health check endpoint (`/api/health`) provides status confirmation of backend availability. The API is hosted entirely under the `/api/...` prefix; visiting the root `/` URL may return an expected `404 Not Found` response.

---

##  What Problem Does PROVE Solve?

Traditional resumes, job applications, and professional profiles rely on self-reported, ungrounded claims (e.g., *"I have 5 years of Python experience"* or *"I built scalable dashboards using React"*). Without verification, these claims introduce subjectivity and risk exaggeration.

PROVE solves this by translating unstructured human experience into structured facts (Actions, Tools, Outputs, and Outcomes) and validating them. The system assesses claimed skills against these verified facts to classify skill statuses, evaluate proficiency levels, score evidence quality, identify proof gaps, and suggest targeted projects to close those gaps.

---

##  Main Features

1.  **LLM-Based Fact Extraction:** Extracts structured entities (Actions, Tools, Outputs, Outcomes) from natural-language experience texts.
2.  **Deterministic Skill Classification:** Maps extracted evidence to claimed skills, classifying them into `PROVEN`, `IMPLIED`, `CLAIMED`, or `UNPROVEN` statuses.
3.  **L0–L5 Proficiency Model:** Dynamically evaluates proficiency levels based on concrete indicators (outcomes, outputs, links).
4.  **7-Dimension Evidence Scoring:** Evaluates evidence quality across Relevance, Depth, Ownership, Outcome, Verifiability, Recency, and Transferability.
5.  **Proof Gap Analysis:** Identifies specific missing evidence components for claimed skills.
6.  **Proof Builder Plan Generator:** Recommends targeted projects, deliverables, hosting platforms, and efforts to close gaps.
7.  **SQLite Persistence:** Stores raw experience input, scores, assessments, and proof plans as a permanent `ProofArtifact` database record.
8.  **Resilient Offline Fallback:** Automatically falls back to local regular expression parsing (`MockProvider`) if the Gemini API key is missing or encounters `429 RESOURCE_EXHAUSTED` rate limits.

---

##  System Architecture

PROVE decouples unstructured text processing from final business decisions. For a comprehensive description, see the full [architecture.md](file:///d:/Coding/Prove/architecture.md) documentation.

```text
       [React Frontend Form]  ◄───────────────────────────┐
                 │                                        │
                 ▼ (POST /api/proof/analyze)              │
       [FastAPI Main Router]                              │
                 │                                        │
                 ▼                                        │
       [Pydantic Schema Validation]                       │
                 │                                        │
                 ▼                                        │
       [LLM Abstraction Layer]                            │
                 │                                        │
      ┌──────────┴──────────┐                             │
      ▼ (LLM_PROVIDER=gemini) ▼ (LLM_PROVIDER=mock)       │
[Gemini Provider]     [Mock Regex Provider]               │
      └──────────┬──────────┘                             │
                 │                                        │
                 ▼ (Extracted Evidence JSON)              │
       [Skill Mapper (synonym/ownership rules)]           │
                 │                                        │
                 ▼                                        │
       [Evidence Scorer (weighted formulas)]              │
                 │                                        │
                 ▼                                        │
       [Proof Gap Engine (gap mapping)]                   │
                 │                                        │
                 ▼                                        │
       [Proof Plan Service (activity building)]           │
                 │                                        │
                 ▼                                        │
       [SQLAlchemy ORM Transaction]                       │
                 │                                        │
                 ▼                                        │
       [SQLite Database Persistence]                      │
                 │                                        │
                 ▼ (ProofArtifact Response)               │
       [JSON API Output] ─────────────────────────────────┘
```

### Deterministic vs. LLM Responsibilities
*   **LLM Role:** Responsible for NLU entity extraction (identifying tools/actions/outcomes from unstructured paragraphs) and generating descriptions for proof projects. The LLM is **not** allowed to assign scores, verify skills, or determine proficiency.
*   **Deterministic Python Role:** Executes all scoring formulas, synonym checks, personal ownership filters, database queries, and route handling. This ensures 100% reproducible results.

---

##  Technology Stack

*   **Frontend:** React 18, TypeScript, Vite, Tailwind CSS, Lucide Icons.
*   **Backend:** Python 3.12, FastAPI, Pydantic v2 (validation), Pydantic Settings.
*   **Database & ORM:** SQLite, SQLAlchemy ORM.
*   **AI Service SDK:** Google GenAI SDK (targeting the active model **`gemini-3.6-flash`**).
*   **Testing:** pytest.

---

##  Deterministic Logic Details

### 1. Skill Mapping Statuses
Claimed skills are cross-referenced with extracted tools and actions using a synonyms directory (e.g., `python` matches pandas, pytest, fastapi, django, etc.):
*   **`PROVEN`:** Directly supported by personal actions and tools.
*   **`IMPLIED`:** Mentioned in context (e.g., in tools), but personal execution is ambiguous or matches team-only patterns.
*   **`CLAIMED`:** Declared by the user, but unsupported by any tools or actions in the text.
*   **`UNPROVEN`:** Insufficient details or evidence present.

### 2. Personal vs. Team pronouns Guardrail
If action statements contain team pronouns (`"we"`, `"our"`, `"the team"`, `"company"`) and lack personal pronouns (`"I"`, `"my"`, `"me"`), the skill status is set to **IMPLIED** instead of **PROVEN**, and a proof gap is flagged.

### 3. L0–L5 Proficiency Evaluation
*   **`L0 — No Evidence`:** Unclaimed / unprovided skills.
*   **`L1 — Awareness`:** Assigned to **CLAIMED** skills.
*   **`L2 — Basic Practical`:** Assigned to **IMPLIED** skills, or proven skills without outcomes/outputs.
*   **`L3 — Independent`:** Proven skills with outputs, outcomes, or links.
*   **`L4 — Advanced`:** Proven skills with valid external links AND quantitative outcomes.
*   **`L5 — Expert`:** Conceptual level representing architectural ownership.

### 4. 7-Dimension Quality Scoring
Scores are computed using weighted averages:
$$\text{Overall Score} = (Relevance \times 0.20) + (Depth \times 0.15) + (Ownership \times 0.15) + (Outcome \times 0.15) + (Verifiability \times 0.15) + (Recency \times 0.10) + (Transferability \times 0.10)$$

*   **Weak:** Score $< 40.0$
*   **Moderate:** $40.0 \le \text{Score} < 70.0$
*   **Strong:** $70.0 \le \text{Score} < 85.0$
*   **Very Strong:** Score $\ge 85.0$
*   **Penalty Guardrail:** Brief text inputs (less than 60 characters) containing no tools are penalized (scoring parameters capped) to prevent false inflation.

---

##  Database Architecture

PROVE persists records to a local SQLite database (`prove.db`) using SQLAlchemy models:

*   **`User`** (`users` table): User profile identity information.
*   **`ProofRecord`** (`proof_records` table): Transactional metadata representing target roles, domains, raw experience descriptions, and links.
*   **`ClaimedSkill`** (`claimed_skills` table): List of skills claimed by the user.
*   **`EvidenceItem`** (`evidence` table): Extracted actions/tools/outputs/outcomes JSON and the 7-dimension scoring values.
*   **`SkillAssessmentModel`** (`skill_assessments` table): The verification status, proficiency level, justification text, and gap description for each skill.
*   **`ProofPlanModel`** (`proof_plans` table): Actions, deliverables, hosting venues, and difficulty levels generated for skill gaps.

---

##  API Endpoints

| Method | Endpoint | Purpose |
| :--- | :--- | :--- |
| `GET` | `/api/health` | Verifies service health, active LLM provider, and database state. |
| `POST` | `/api/proof/analyze` | Executes the complete evidence analysis pipeline and saves results. |
| `POST` | `/api/proof/build` | Generates a targeted project plan to close a specific skill proof gap. |
| `GET` | `/api/proof/{id}` | Retrieves a previously saved proof analysis record by ID. |
| `GET` | `/api/proof` | Lists metadata for the 50 most recent saved analysis records. |

---

##  Repository Structure

```text
prove/
├── README.md
├── architecture.md
├── render.yaml
├── backend/
│   ├── app/
│   │   ├── api/routes/proof.py
│   │   ├── core/config.py
│   │   ├── db/database.py & models.py
│   │   ├── schemas/ (proof.py, evidence.py, assessment.py)
│   │   ├── services/ (llm_service.py, gemini_provider.py, mock_provider.py, evidence_extractor.py, etc.)
│   │   └── prompts/ (extraction_prompt.txt, proof_builder_prompt.txt)
│   ├── tests/ (test_api.py, test_evaluation_cases.py, test_evidence_scoring.py, etc.)
│   ├── requirements.txt
│   └── prove.db
├── frontend/
│   ├── src/
│   │   ├── components/ (ProofInputForm, LoadingProgress, SkillAssessmentCards, etc.)
│   │   ├── services/api.ts
│   │   ├── types/proof.ts
│   │   └── App.tsx
│   ├── package.json
│   └── tailwind.config.js
└── tests/
    └── evaluation_cases.json
```

---

##  Local Installation & Setup

Follow these steps to run PROVE locally on Windows.

### 1. Clone the Repository
```powershell
git clone <repository_url>
cd prove
```

### 2. Backend Installation
Open a terminal in the `backend/` directory:
```powershell
cd backend
python -m venv .venv
.\.venv\Scripts\Activate.ps1
pip install -r requirements.txt
```

### 3. Configure Environment Variables
Create a file named `.env` in the `backend/` directory (you can copy `.env.example` as a template):
```env
LLM_PROVIDER=gemini
GEMINI_API_KEY=YOUR_GEMINI_API_KEY_HERE
DATABASE_URL=sqlite:///./prove.db
PORT=8000
HOST=0.0.0.0
```
> [!NOTE]
> If `GEMINI_API_KEY` is left blank or `LLM_PROVIDER` is set to `mock`, the application will automatically run offline using the `MockProvider`.

### 4. Start the Backend API Server
```powershell
uvicorn app.main:app --reload --port 8000
```
The API documentation will be available at [http://127.0.0.1:8000/docs](http://127.0.0.1:8000/docs).

### 5. Frontend Installation and Launch
Open a separate terminal in the `frontend/` directory:
```powershell
cd frontend
npm install
npm run dev
```
The user interface will be available at [http://localhost:5173](http://localhost:5173).

---

##  Testing & Validation Suite

The backend test suite is located in `backend/tests/` and uses `pytest` for validation.

### Golden Dataset Scenarios
The file `tests/evaluation_cases.json` holds 8 scenario cases verifying key evidence intelligence rules:
*   `CASE_1`: Strong Evidence - Senior Data Engineer (Proven Python/SQL, Strong/Very Strong quality).
*   `CASE_2`: Claimed Skill Without Evidence (Claimed Python with proof gap, Proven Excel/SQL).
*   `CASE_3`: Weak Evidence (Weak quality, score $\le 45.0$).
*   `CASE_4`: Unsupported Numerical Claim (Claimed Python, verifiability capped).
*   `CASE_5`: Mixed Evidence (Proven React/Python/FastAPI, Claimed Kubernetes).
*   `CASE_6`: AI-Assisted Project (Proven Python, metadata flag check).
*   `CASE_7`: Insufficient Experience Text (Validation checks).
*   `CASE_8`: Conflicting or Ambiguous Evidence (Proven Python, Implied Rust, Claimed Go).

### Run the Tests Locally
Ensure the backend virtual environment is activated, then run the test suite offline:
```powershell
$env:LLM_PROVIDER="mock"
python -m pytest -v
```
All **20 automated tests** should pass:
```text
tests/test_api.py::test_health_check PASSED
tests/test_api.py::test_analyze_proof_success PASSED
...
tests/test_skill_mapping.py::test_skill_mapping_proven_and_claimed PASSED
tests/test_skill_mapping.py::test_skill_mapping_implied PASSED
======================= 20 passed in 1.02s =======================
```

---

##  AI-Assisted Development Disclosure

During the development of PROVE, AI coding assistants (specifically Gemini models) were utilized as support tools for:
*   Exploring code and reviewing FastAPI framework layout.
*   Debugging syntax errors, Pydantic type conversions, and database transaction queries.
*   Generating initial unit test skeletons and test-case parameter structures.
*   Structuring and proofreading documentation (such as `architecture.md` and this `README.md`).
*   Troubleshooting the dynamic client initialization within the Gemini API provider.

The developer manually reviewed, modified, and validated all final implementation details, database relationships, deterministic scoring logic, and integration tests to ensure correctness and alignment with assignment specifications.

---

##  Conclusion

PROVE demonstrates how LLMs can be integrated with deterministic rules to build reliable, audit-ready AI systems. By restricting the LLM to language parsing and delegating scoring and validation to Python, PROVE provides objective, reproducible skill verifications suitable for professional evaluation workflows.
