import streamlit as st
import pandas as pd
import hashlib
import datetime

# --- 1. Page Configuration ---
st.set_page_config(page_title="Islamic Murabaha System", layout="wide")
st.title("🏦 Blockchain Murabaha Audit System")
st.markdown("### AAOIFI-Compliant Audit Engine")
st.caption("A Prototype for enforcing sequential compliance in Islamic Finance using Blockchain Logic.")

# --- 2. Blockchain Functions (Cryptography) ---
def generate_hash(data):
    # Create a SHA-256 digital fingerprint
    sha = hashlib.sha256()
    sha.update(data.encode('utf-8'))
    return sha.hexdigest()

# --- 3. Session State (Memory) ---
if 'logs' not in st.session_state:
    st.session_state['logs'] = []
if 'step' not in st.session_state:
    st.session_state['step'] = 1  # 1: Request, 2: Bank Buy, 3: Murabaha Sale

# --- 4. Application UI ---

col1, col2 = st.columns([1, 2])

with col1:
    st.header("📝 Contract Workflow")
    
    # Asset Details
    item_name = st.text_input("Asset Name", "Toyota Camry 2025")
    price = st.number_input("Cost Price (Bank's Cost)", min_value=0, value=25000)
    profit_margin = st.number_input("Profit Margin (%)", min_value=0, value=10)
    
    final_price = price + (price * profit_margin / 100)
    st.info(f"Final Selling Price to Client: ${final_price:,.2f}")

    st.divider()

    # STEP 1: Client Request
    if st.session_state['step'] == 1:
        st.markdown("#### Phase 1: Purchase Order")
        if st.button("1. Submit Promise to Purchase (Wa'd)"):
            timestamp = str(datetime.datetime.now())
            # Create Genesis Block Hash
            data_to_hash = f"REQUEST-{item_name}-{timestamp}"
            block_hash = generate_hash(data_to_hash)
            
            # Record Transaction
            st.session_state['logs'].append({
                "Step": "1. Promise (Wa'd)",
                "Description": f"Client requested: {item_name}",
                "Timestamp": timestamp,
                "Block Hash": block_hash,
                "Sharia Status": "✅ Valid (Non-binding Promise)"
            })
            st.session_state['step'] = 2
            st.rerun()

    # STEP 2: Bank Purchase (Ownership)
    elif st.session_state['step'] == 2:
        st.markdown("#### Phase 2: Bank Ownership")
        st.warning("⚠️ Compliance Rule: Bank must own and possess the asset BEFORE selling it.")
        
        if st.button("2. Execute Purchase & Possession (Bank)"):
            timestamp = str(datetime.datetime.now())
            # Link to previous block (Blockchain Logic)
            prev_hash = st.session_state['logs'][-1]['Block Hash']
            data_to_hash = f"BUY-{item_name}-{timestamp}-{prev_hash}"
            block_hash = generate_hash(data_to_hash)
            
            st.session_state['logs'].append({
                "Step": "2. Bank Possession",
                "Description": "Bank acquired ownership & possession",
                "Timestamp": timestamp,
                "Block Hash": block_hash,
                "Sharia Status": "✅ Valid (Ownership Established)"
            })
            st.session_state['step'] = 3
            st.rerun()

    # STEP 3: Murabaha Sale
    elif st.session_state['step'] == 3:
        st.markdown("#### Phase 3: Murabaha Contract")
        if st.button("3. Execute Murabaha Sale (To Client)"):
            timestamp = str(datetime.datetime.now())
            prev_hash = st.session_state['logs'][-1]['Block Hash']
            data_to_hash = f"SALE-{item_name}-{final_price}-{timestamp}-{prev_hash}"
            block_hash = generate_hash(data_to_hash)
            
            st.session_state['logs'].append({
                "Step": "3. Murabaha Sale",
                "Description": f"Sold to Client for ${final_price}",
                "Timestamp": timestamp,
                "Block Hash": block_hash,
                "Sharia Status": "✅ Transaction Complete"
            })
            st.session_state['step'] = 4
            st.rerun()
            
    elif st.session_state['step'] == 4:
        st.success("🎉 Murabaha Cycle Completed Successfully.")
        if st.button("Start New Transaction"):
            st.session_state['logs'] = []
            st.session_state['step'] = 1
            st.rerun()

with col2:
    st.header("⛓️ Immutable Audit Ledger")
    st.caption("This ledger demonstrates the blockchain sequence. Backdating is mathematically impossible.")
    
    if len(st.session_state['logs']) > 0:
        df = pd.DataFrame(st.session_state['logs'])
        # Reorder columns for better view
        df = df[["Step", "Description", "Timestamp", "Sharia Status", "Block Hash"]]
        st.table(df)
    else:
        st.info("Waiting for transactions...")