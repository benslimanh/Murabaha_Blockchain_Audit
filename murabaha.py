import streamlit as st
import pandas as pd
import hashlib
import datetime
from io import BytesIO  # Library for in-memory file handling

# --- 1. Page Configuration ---
st.set_page_config(page_title="Islamic Murabaha System", layout="wide", page_icon="🏦")
st.title("🏦 Blockchain Murabaha Audit System")
st.markdown("### AAOIFI-Compliant Audit Engine & Financial Simulator")
st.caption("A Prototype for enforcing sequential compliance in Islamic Finance using Blockchain Logic.")

# --- 2. Helper Functions ---

def generate_hash(data):
    """Generates SHA-256 Hash for the blockchain ledger."""
    sha = hashlib.sha256()
    sha.update(data.encode('utf-8'))
    return sha.hexdigest()

def calculate_schedule(total_amount, months):
    """Generates the amortization schedule (Monthly Payments)."""
    monthly_payment = total_amount / months
    schedule = []
    remaining_balance = total_amount
    
    for i in range(1, months + 1):
        payment = monthly_payment
        remaining_balance -= payment
        # Determine status based on current month (Simulation)
        status = "Pending"
        schedule.append({
            "Month": i,
            "Installment": round(payment, 2),
            "Remaining Balance": round(max(0, remaining_balance), 2),
            "Status": status
        })
    return pd.DataFrame(schedule)

# --- 3. Session State Initialization ---
if 'logs' not in st.session_state:
    st.session_state['logs'] = []
if 'step' not in st.session_state:
    st.session_state['step'] = 1 

# --- 4. Application Layout ---
col1, col2 = st.columns([1, 1.5]) # Adjusted ratio for better visualization

# ================= COLUMN 1: INPUTS & WORKFLOW =================
with col1:
    st.header("📝 Transaction Details")
    
    with st.container(border=True): # New container for better grouping
        item_name = st.text_input("Asset Name", "Toyota Camry 2025")
        price = st.number_input("Cost Price (Bank's Cost)", min_value=0, value=25000)
        profit_margin = st.number_input("Profit Margin (%)", min_value=0, value=10)
        duration_months = st.number_input("Financing Duration (Months)", min_value=1, value=12) # NEW INPUT
        
        # Calculation
        final_price = price + (price * profit_margin / 100)
        monthly_installment = final_price / duration_months
        
        st.info(f"Final Selling Price: ${final_price:,.2f}")

    st.divider()

    # --- Murabaha Workflow Logic ---
    st.subheader("⚙️ Execution Workflow")
    
    # Step 1: Wa'd
    if st.session_state['step'] == 1:
        st.markdown("#### Phase 1: Purchase Order")
        st.markdown("*Client promises to buy the asset.*")
        if st.button("1. Submit Promise (Wa'd)", type="primary"):
            timestamp = str(datetime.datetime.now())
            data_to_hash = f"REQUEST-{item_name}-{timestamp}"
            block_hash = generate_hash(data_to_hash)
            st.session_state['logs'].append({
                "Step": "1. Promise (Wa'd)", "Description": f"Client requested: {item_name}",
                "Timestamp": timestamp, "Block Hash": block_hash, "Sharia Status": "Valid Promise"
            })
            st.session_state['step'] = 2
            st.rerun()

    # Step 2: Qabd
    elif st.session_state['step'] == 2:
        st.markdown("#### Phase 2: Bank Ownership")
        st.warning("⚠️ Compliance Rule: Bank must own asset BEFORE selling.")
        if st.button("2. Execute Purchase & Possession"):
            timestamp = str(datetime.datetime.now())
            prev_hash = st.session_state['logs'][-1]['Block Hash']
            data_to_hash = f"BUY-{item_name}-{timestamp}-{prev_hash}"
            block_hash = generate_hash(data_to_hash)
            st.session_state['logs'].append({
                "Step": "2. Bank Possession", "Description": "Bank acquired ownership (Qabd)",
                "Timestamp": timestamp, "Block Hash": block_hash, "Sharia Status": "Valid Ownership"
            })
            st.session_state['step'] = 3
            st.rerun()

    # Step 3: Bay'
    elif st.session_state['step'] == 3:
        st.markdown("#### Phase 3: Murabaha Sale")
        st.markdown(f"*Selling to client for ${final_price:,.2f}*")
        if st.button("3. Execute Murabaha Sale", type="primary"):
            timestamp = str(datetime.datetime.now())
            prev_hash = st.session_state['logs'][-1]['Block Hash']
            data_to_hash = f"SALE-{item_name}-{final_price}-{timestamp}-{prev_hash}"
            block_hash = generate_hash(data_to_hash)
            st.session_state['logs'].append({
                "Step": "3. Murabaha Sale", "Description": f"Contract concluded. Profit: {profit_margin}%",
                "Timestamp": timestamp, "Block Hash": block_hash, "Sharia Status": "Transaction Complete"
            })
            st.session_state['step'] = 4
            st.rerun()
            
    # Completion
    elif st.session_state['step'] == 4:
        st.success("✅ Transaction Successfully Audited.")
        if st.button("Start New Transaction"):
            st.session_state['logs'] = []
            st.session_state['step'] = 1
            st.rerun()

# ================= COLUMN 2: FINANCIAL & AUDIT DASHBOARD =================
with col2:
    # --- Part A: Financial Dashboard (The New Feature) ---
    st.header("💰 Financial Dashboard")
    
    # Metrics Row
    m1, m2, m3 = st.columns(3)
    m1.metric("Total Payable", f"${final_price:,.2f}")
    m2.metric("Monthly Installment", f"${monthly_installment:,.2f}")
    m3.metric("Duration", f"{duration_months} Months")
    
    # Amortization Schedule & Chart
    tab1, tab2 = st.tabs(["📈 Chart", "📋 Schedule Table"])
    
    schedule_df = calculate_schedule(final_price, duration_months)
    
    with tab1:
        st.caption("Balance Depletion Over Time")
        st.line_chart(schedule_df, x="Month", y="Remaining Balance", color="#004C99")
        
    with tab2:
        st.dataframe(schedule_df, hide_index=True, use_container_width=True)

    st.divider()

    # --- Part B: Audit Ledger (Existing Logic) ---
    st.header("⛓️ Immutable Audit Ledger")
    
    if len(st.session_state['logs']) > 0:
        audit_df = pd.DataFrame(st.session_state['logs'])
        
        # Display simplified table for UI
        st.dataframe(
            audit_df[["Step", "Description", "Timestamp", "Sharia Status"]], 
            use_container_width=True,
            hide_index=True
        )

        st.caption("Note: Cryptographic hashes are hidden in view but included in export.")

        # --- Excel Export Logic ---
        buffer = BytesIO()
        with pd.ExcelWriter(buffer, engine='xlsxwriter') as writer:
            # Sheet 1: Audit Log
            audit_df.to_excel(writer, index=False, sheet_name='Audit Log')
            
            # Sheet 2: Payment Schedule (NEW)
            schedule_df.to_excel(writer, index=False, sheet_name='Payment Schedule')
            
            # Formatting (Optional but recommended)
            workbook = writer.book
            worksheet = writer.sheets['Audit Log']
            cell_format = workbook.add_format({'text_wrap': True, 'valign': 'vcenter', 'border': 1})
            worksheet.set_column('A:E', 25, cell_format)
            worksheet.set_column('E:E', 50, cell_format) # Wider for Hash

        st.download_button(
            label="📥 Download Full Audit Report (.xlsx)",
            data=buffer,
            file_name='Murabaha_Full_Report.xlsx',
            mime='application/vnd.ms-excel'
        )
    else:
        st.info("Waiting for transaction steps to be recorded on the blockchain...")
