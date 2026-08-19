# PROVE — Architectural Documentation

## Overview

PROVE separates **Natural Language Understanding (LLM)** from **Business Logic & Scoring (Deterministic Python)**.

```
React Frontend (TypeScript + Vite)
       │
       │ HTTP JSON API
       ▼
FastAPI Backend (/api/proof/analyze)
       │
       ├─► 1. Pydantic Request Validation (ProofAnalysisRequest)
       │
       ├─► 2. LLM Service Layer (LLMService -> GeminiProvider / MockProvider)
       │      └─► Natural Language Fact Extraction (Actions, Tools, Outputs, Outcomes)
       │
       ├─► 3. Pydantic Schema Validation & Retry (ExtractedEvidence)
       │
       ├─► 4. Deterministic Skill Mapping Engine (PROVEN | IMPLIED | CLAIMED | UNPROVEN)
       │
       ├─► 5. L0–L5 Proficiency Evaluation (L0: No Evidence → L5: Deep Ownership)
       │
       ├─► 6. 7-Dimension Evidence Quality Engine (Relevance, Depth, Ownership, Outcome, Verifiability, Recency, Transferability)
       │
       ├─► 7. Proof Gap & Proof Builder Engine (Constructs concrete project blueprints)
       │
       ├─► 8. SQLite Relational Persistence (SQLAlchemy: proof_records, claimed_skills, evidence, assessments, proof_plans)
       │
       ▼
Structured Proof Artifact & JSON Response
```

---

## Why Deterministic Scoring & Classification?

### The Problem with Pure LLM Scoring
Large Language Models excel at understanding unstructured natural language, but are prone to:
1. **Scoring Hallucinations**: Giving different numerical scores for identical inputs across runs.
2. **Unsupported Inferences**: Falsely elevating unverified user claims (e.g. "I grew revenue 50%") to verified proof.
3. **Inconsistent Skill Mapping**: Marking a skill as proven in one query and merely claimed in another.

### PROVE's Hybrid Separation
- **LLM Responsibility**: Extracts natural language facts into structured primitive arrays (actions, tools, outputs, outcomes) and generates concrete text for project deliverables.
- **Python Deterministic Engine Responsibility**:
  - Validates that user claims match extracted tools and personal actions.
  - Computes exact L0–L5 proficiency levels based on verifiable outputs and evidence links.
  - Calculates 7-dimension evidence quality scores using fixed mathematical weights:
    - Relevance (20%)
    - Depth (15%)
    - Ownership (15%)
    - Outcome (15%)
    - Verifiability (15%)
    - Recency (10%)
    - Transferability (10%)
  - Ensures factual guardrails: Claims without evidence links receive capped verifiability scores and remain unverified.

---

## Database Architecture

SQLite with SQLAlchemy ORM provides lightweight, fast, local relational storage:

- `users`: User identity table.
- `proof_records`: Primary record metadata, target role, domain, raw experience, project name, outcome, links, and AI usage declaration.
- `claimed_skills`: Skills explicitly claimed by user in submission.
- `evidence`: JSON-serialized lists of extracted actions, tools, outputs, outcomes, plus all 7 dimension scores and overall quality label.
- `skill_assessments`: Individual skill evaluations storing status (`PROVEN`, `IMPLIED`, `CLAIMED`, `UNPROVEN`), proficiency (`L0`–`L5`), justification text, and proof gap description.
- `proof_plans`: Recommended project blueprints storing activity, deliverables list, evidence venue, effort, and difficulty.

---

## LLM Abstraction Layer

The application implements a clean provider abstraction:

- `BaseLLMProvider`: Abstract Base Class defining standard interface methods for extraction and proof plan generation.
- `GeminiProvider`: Primary production implementation using the free-tier Gemini API (`gemini-2.5-flash`) via `google-genai` SDK with automatic JSON parsing retries.
- `MockProvider`: Production-ready rule-based fallback provider. Allows full unit testing, CI execution, and offline usage without requiring API keys.
