# 🏦 Blockchain-Based Murabaha Audit System

[![Streamlit App](https://static.streamlit.io/badges/streamlit_badge_black_white.svg)](https://murabaha-blockchain-audit.streamlit.app/)
### 📜 Project Overview
This represents an educational FinTech prototype designed to simulate an **Automated Sharia Audit Trail**. The system addresses the operational risk of non-compliance in *Murabaha* transactions (specifically sequence violations) by enforcing strict chronological execution using cryptographic hashing.

### 🎯 Key Features
* **State Machine Logic:** Enforces the sequence: *Promise (Wa'd) → Bank Possession (Qabd) → Sale (Bay')*.
* **Immutable Ledger:** Uses SHA-256 hashing to link transaction steps, making backdating mathematically impossible.
* **AAOIFI Compliance:** Designed according to Sharia Standard No. 8 (Murabaha).

### 🛠️ Technologies Used
* **Language:** Python 3.12
* **Framework:** Streamlit
* **Logic:** Pandas (Dataframe), Hashlib (Cryptography)

### 🚀 How to Run locally
1. Install requirements: `pip install streamlit pandas`
2. Run the app: `streamlit run murabaha.py`

---
*Developed by: Bensliman Hamza - Management & Finance Student*


### 📊 System Architecture & Workflow
Here is the strict chronological sequence enforced by the algorithm:

```mermaid
sequenceDiagram
    participant C as Client
    participant B as Bank
    participant L as Blockchain Ledger (Audit)

    Note over C, B: Phase 1: Promise (Wa'd)
    C->>B: 1. Request Asset (e.g. Toyota Camry)
    B->>L: Generate Hash #1 (Request + Timestamp)
    L-->>B: Log Transaction (Step 1 Locked)

    Note over B: Phase 2: Ownership (Qabd)
    B->>B: 2. Buy Asset from Supplier
    B->>L: Generate Hash #2 (Ownership + Hash #1)
    Note right of L: Chaining prevents backdating
    L-->>B: Log Transaction (Step 2 Locked)

    Note over C, B: Phase 3: Murabaha Sale (Bay')
    B->>C: 3. Sell Asset (Cost + Profit)
    B->>L: Generate Hash #3 (Sale + Hash #2)
    L-->>B: Transaction Complete ✅
