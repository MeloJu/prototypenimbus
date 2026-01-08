
# Music Generator Company – Minimal Prototype

## Overview

This repository contains a **small proof of concept** created for CloudWalk’s **Level 2.3 – Music Generator Company** challenge.

The goal of this prototype is to **validate the proposed architecture**, focusing on agent separation, orchestration, and context-aware decision making. It is intentionally minimal and not intended to be production-ready.

---

## Scope and Intent

This prototype focuses on:

* Multi-agent coordination
* Clear separation of responsibilities
* Selective use of Retrieval-Augmented Generation (RAG)
* Pragmatic engineering choices

External services are mocked on purpose to keep the focus on system design rather than integration complexity.

---

## Architecture Decisions

### Mocked External Services

* **Music generation** is simulated through genre and mood selection.
* **Billing** is simulated with a simple $1/month subscription flow.
* **Marketing** is simulated through post generation logic.

Real APIs would not change the architectural reasoning demonstrated here.

---

### Selective Use of RAG

RAG is applied only where contextual memory adds value:

**Music Agent**

* Avoids repeating recently used genres.
* Varies mood and style based on recent history and time of day.

**Marketing Agent**

* Reuses high-performing post templates.
* Selects hashtags based on genre.

**Billing Agent**

* Uses deterministic logic only.
* No AI is involved, as billing does not benefit from LLM-based reasoning.

---

### Knowledge Base

The system uses a simple local JSON file as a lightweight knowledge store, holding:

* Recently generated genres
* Mood mappings
* Marketing templates and engagement data

For a prototype of this size, in-memory state is sufficient to demonstrate RAG concepts.

---

### No LLM API Calls

LLM behavior is simulated using predefined logic.
This keeps the prototype runnable without credentials and shifts attention to **architecture and decision flow** rather than model performance.

---

## System Diagram

```
┌─────────────────────────────────────┐
│     Autonomous Music Company        │
└─────────────────────────────────────┘
              │
    ┌─────────┼─────────┐
    │         │         │
┌───▼───┐ ┌──▼──┐ ┌────▼─────┐
│ Music │ │Bill │ │Marketing │
│ Agent │ │Agent│ │  Agent   │
└───┬───┘ └──┬──┘ └────┬─────┘
    │        │         │
    └────────┼─────────┘
             │
    ┌────────▼────────┐
    │   Knowledge     │
    │      Base       │
    └─────────────────┘
```

---

## Running the Prototype

```bash
python prototype.py
```

Example output:

```
Generated: "Morning Light" (Pop, Uplifting)
Processed 5 subscriptions: $5.00
Posted: "🎵 New Pop track: Morning Light! #Pop #Music"
```

---

## Notes

This prototype demonstrates how a small autonomous system can:

* Use context to improve decisions
* Avoid unnecessary AI usage
* Remain simple and explainable

It is meant to validate architectural choices rather than implementation scale.

---

## Repository Contents

* `prototype.py` – Minimal multi-agent orchestration
* `knowledge_base.json` – Lightweight RAG store
* `README.md` – This document

---

**Author:** Juan
**Challenge:** CloudWalk AI Wizard – Level 2.3


