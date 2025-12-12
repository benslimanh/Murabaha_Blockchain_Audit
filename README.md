# 🏦 Blockchain-Based Murabaha Audit System

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
