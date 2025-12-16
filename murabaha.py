import streamlit as st
import pandas as pd
import hashlib
import datetime
from fpdf import FPDF

# --- 1. Page Configuration ---
st.set_page_config(
    page_title="ShariaChain | Audit System", 
    layout="wide", 
    page_icon="🏦",
    initial_sidebar_state="expanded"
)

# ==========================================
# 🎨 CUSTOM CSS (Professional Styling)
# ==========================================
st.markdown("""
    <style>
    /* 1. Global Background Settings */
    .stApp {
        background-color: #f8f9fa;
    }
    
    /* 2. Button Styling (Bank Blue) */
    .stButton>button {
        background-color: #004C99;
        color: white;
        border-radius: 8px;
        border: none;
        padding: 10px 24px;
        font-weight: bold;
        transition: 0.3s;
    }
    
    /* Button Hover Effect */
    .stButton>button:hover {
        background-color: #003366;
        color: #FFD700; /* Gold text */
    }

    /* 3. Clean UI: Hiding Watermarks but KEEPING Header visible */
    footer {visibility: hidden;}    /* Hides 'Made with Streamlit' */
    #MainMenu {visibility: hidden;} /* Hides the top-right menu (optional) */
    
    /* We DO NOT hide 'header' so you can see the sidebar arrow (>) */

    /* 4. Hide the Deploy Button */
    .stDeployButton {display:none;}
    
    /* 5. Card/Container Styling */
    div[data-testid="stVerticalBlock"] > div[style*="flex-direction: column;"] > div[data-testid="stVerticalBlock"] {
        background-color: white;
        padding: 20px;
        border-radius: 10px;
        box-shadow: 0 4px 6px rgba(0,0,0,0.1);
    }
    
    /* 6. Auditor Badge Styling */
    .auditor-badge {
        background-color: #28a745;
        color: white;
        padding: 5px 10px;
        border-radius: 15px;
        font-size: 12px;
        font-weight: bold;
    }
    </style>
""", unsafe_allow_html=True)

# ==========================================
# 🔐 SECURE LOGIN SYSTEM (MULTI-ROLE)
# ==========================================
if 'authentication_status' not in st.session_state:
    st.session_state['authentication_status'] = False
if 'user_role' not in st.session_state:
    st.session_state['user_role'] = None

def login_page():
    col1, col2, col3 = st.columns([1, 2, 1])
    with col2:
        st.markdown("<br><br>", unsafe_allow_html=True)
        st.title("🔒 System Access")
        st.write("Select your role and login.")
        
        with st.form("login_form"):
            username = st.text_input("Username")
            password = st.text_input("Password", type="password")
            submitted = st.form_submit_button("Login")
            
            if submitted:
                # ROLE 1: BANK OFFICER
                if username == "admin" and password == "1234":
                    st.session_state['authentication_status'] = True
                    st.session_state['user_role'] = "Officer"
                    st.rerun()
                # ROLE 2: SHARIA AUDITOR
                elif username == "auditor" and password == "5678":
                    st.session_state['authentication_status'] = True
                    st.session_state['user_role'] = "Auditor"
                    st.rerun()
                else:
                    st.error("❌ Invalid Credentials")
        
        st.info("Demo Accounts:\n\n👤 **Officer:** admin / 1234\n\n🛡️ **Auditor:** auditor / 5678")

if not st.session_state['authentication_status']:
    login_page()
    st.stop()

# ==========================================
# 🎨 SIDEBAR: DYNAMIC BASED ON ROLE
# ==========================================
with st.sidebar:
    # Use local 'logo.png' if available, else placeholder
    st.image("https://cdn-icons-png.flaticon.com/512/2438/2438078.png", width=90) 
    st.markdown("### **ShariaChain** \n *Digital Trust*")
    st.divider()
    
    # Show User Role Badge
    role_color = "blue" if st.session_state['user_role'] == "Officer" else "green"
    st.markdown(f"User Role: :{role_color}[**{st.session_state['user_role']}**]")
    
    st.header("⚙️ Configuration")
    
    # --- CURRENCY SELECTION IS HERE ---
    currency = st.selectbox("Operating Currency", ["MAD", "USD", "EUR"], index=0)
    
    # Only Officer can change financial parameters
    if st.session_state['user_role'] == "Officer":
        default_profit = st.slider("Profit Margin (%)", 5.0, 20.0, 10.0, 0.5)
        max_duration = st.number_input("Max Duration (Months)", value=60)
    else:
        # Auditor sees Read-Only values
        st.info("🔒 View-Only Mode")
        default_profit = 10.0
        max_duration = 60
    
    st.divider()
    if st.button("Logout", type="primary"):
        st.session_state['authentication_status'] = False
        st.session_state['user_role'] = None
        st.rerun()

# ==========================================
# 🏦 MAIN LOGIC
# ==========================================

st.title(f"🏦 Murabaha Audit Dashboard")
st.caption(f"Role: {st.session_state['user_role']} | Compliance: AAOIFI No.8")
st.markdown("---")

# --- Helper Functions ---
def generate_hash(data):
    sha = hashlib.sha256()
    sha.update(data.encode('utf-8'))
    return sha.hexdigest()

def calculate_schedule(total_amount, months):
    monthly_payment = total_amount / months
    schedule = []
    remaining_balance = total_amount
    for i in range(1, months + 1):
        payment = monthly_payment
        remaining_balance -= payment
        schedule.append({
            "Month": i,
            "Installment": round(payment, 2),
            "Remaining Balance": round(max(0, remaining_balance), 2),
            "Status": "Pending"
        })
    return pd.DataFrame(schedule)

def create_contract_pdf(client_name, asset, price, logs, curr):
    pdf = FPDF()
    pdf.add_page()
    pdf.set_font("Arial", size=12)
    pdf.set_font("Arial", 'B', 16)
    pdf.cell(0, 10, txt="Islamic Murabaha Contract", ln=True, align='C')
    pdf.set_font("Arial", size=10)
    pdf.cell(0, 10, txt="Automated Sharia-Compliant Transaction", ln=True, align='C')
    pdf.ln(10)
    pdf.set_font("Arial", 'B', 12)
    pdf.cell(0, 10, txt="Transaction Details:", ln=True)
    pdf.set_font("Arial", size=12)
    pdf.cell(0, 10, txt=f"Client Name: {client_name}", ln=True)
    pdf.cell(0, 10, txt=f"Asset: {asset}", ln=True)
    pdf.cell(0, 10, txt=f"Total Price: {price:,.2f} {curr}", ln=True)
    pdf.cell(0, 10, txt=f"Date: {datetime.date.today()}", ln=True)
    pdf.ln(10)
    pdf.set_font("Arial", 'B', 14)
    pdf.cell(0, 10, txt="Audit Trail (Blockchain Hashes)", ln=True)
    pdf.set_font("Courier", size=9)
    for log in logs:
        clean_line = f"[{log['Step']}] {log['Timestamp']}\nHash: {log['Block Hash']}\n"
        pdf.multi_cell(0, 8, txt=clean_line, border=1)
        pdf.ln(2)
    pdf.ln(20)
    pdf.cell(0, 10, txt="_" * 40, ln=True)
    pdf.cell(0, 10, txt="Authorized Signature", ln=True)
    return pdf.output(dest='S').encode('latin-1')

# --- Session State ---
if 'logs' not in st.session_state: st.session_state['logs'] = []
if 'step' not in st.session_state: st.session_state['step'] = 1 

# --- DYNAMIC LAYOUT BASED ON ROLE ---

# SCENARIO 1: AUDITOR (READ ONLY)
if st.session_state['user_role'] == "Auditor":
    st.info("🛡️ You are logged in as a Sharia Auditor. You have Read-Only access to the Blockchain Ledger.")
    
    st.subheader("⛓️ Immutable Audit Ledger")
    
    if len(st.session_state['logs']) > 0:
        # 1. Show the Ledger Table
        audit_df = pd.DataFrame(st.session_state['logs'])
        st.table(audit_df[['Step', 'Timestamp', 'Status', 'Block Hash']])
        
        st.markdown("---")
        st.subheader("🧐 Compliance Analysis")
        
        # 2. AUTOMATED CHECKS (التحقق الذكي)
        last_step = st.session_state['logs'][-1]['Step']
        
        # Check A: Is the sequence complete? (Must end with '3. Bay'')
        if "3. Bay'" in last_step:
            st.success("✅ STATUS: COMPLETE. The transaction fully complies with AAOIFI sequence (Wa'd -> Qabd -> Bay').")
            # Show download button only if complete
            if st.button("📥 Download Final Audit Report"):
                st.toast("Audit Report Generated Successfully!")
        else:
            # If incomplete, show specific warning based on where it stopped
            st.warning("⚠️ STATUS: INCOMPLETE. The transaction is still in progress.")
            
            if "1. Wa'd" in last_step:
                st.error("❌ ISSUE: Bank possesses only the 'Promise'. Asset NOT yet purchased.")
            elif "2. Qabd" in last_step:
                st.error("❌ ISSUE: Bank holds the Asset (Qabd), but has NOT sold it to the client yet.")
                
    else:
        st.warning("No transactions found in the current session ledger.")

# SCENARIO 2: BANK OFFICER (FULL ACCESS)
else:
    col1, col2 = st.columns([1, 1.5]) 
    
    with col1:
        st.subheader("📝 New Transaction")
        with st.container(border=True):
            client_name = st.text_input("Client Name", "Hamza Bensliman")
            item_name = st.text_input("Asset Name", "Apartment Fes City")
            
            # Inputs
            price = st.number_input(f"Cost Price ({currency})", min_value=0, value=250000)
            profit_margin = st.number_input("Profit Margin (%)", min_value=0.0, value=default_profit)
            duration_months = st.number_input("Duration (Months)", min_value=1, max_value=max_duration, value=12)
            
            # Calculations
            final_price = price + (price * profit_margin / 100)
            monthly_installment = final_price / duration_months
            st.success(f"Final Price: {final_price:,.2f} {currency}")

        st.divider()
        
        # Workflow Logic
        if st.session_state['step'] == 1:
            st.info("Step 1: Initiate Promise to Purchase")
            if st.button("1. Submit Promise (Wa'd)", type="primary"):
                timestamp = str(datetime.datetime.now())
                data_to_hash = f"REQUEST-{item_name}-{timestamp}"
                block_hash = generate_hash(data_to_hash)
                st.session_state['logs'].append({
                    "Step": "1. Wa'd", "Description": "Promise to Purchase",
                    "Timestamp": timestamp, "Block Hash": block_hash, "Status": "Valid"
                })
                st.session_state['step'] = 2
                st.rerun()

        elif st.session_state['step'] == 2:
            st.warning("⚠️ Action Required: Bank must acquire possession.")
            if st.button("2. Execute Purchase (Qabd)"):
                timestamp = str(datetime.datetime.now())
                prev_hash = st.session_state['logs'][-1]['Block Hash']
                data_to_hash = f"BUY-{item_name}-{prev_hash}"
                block_hash = generate_hash(data_to_hash)
                st.session_state['logs'].append({
                    "Step": "2. Qabd", "Description": "Bank Ownership Verified",
                    "Timestamp": timestamp, "Block Hash": block_hash, "Status": "Valid"
                })
                st.session_state['step'] = 3
                st.rerun()

        elif st.session_state['step'] == 3:
            st.info("Ready for Final Sale Contract")
            if st.button("3. Execute Sale (Murabaha)", type="primary"):
                timestamp = str(datetime.datetime.now())
                prev_hash = st.session_state['logs'][-1]['Block Hash']
                data_to_hash = f"SALE-{final_price}-{prev_hash}"
                block_hash = generate_hash(data_to_hash)
                st.session_state['logs'].append({
                    "Step": "3. Bay'", "Description": "Murabaha Contract Signed",
                    "Timestamp": timestamp, "Block Hash": block_hash, "Status": "Complete"
                })
                st.session_state['step'] = 4
                st.rerun()

        elif st.session_state['step'] == 4:
            st.success("✅ Transaction Audited & Closed")
            pdf_data = create_contract_pdf(client_name, item_name, final_price, st.session_state['logs'], currency)
            st.download_button("⬇️ Download Contract (PDF)", pdf_data, "Smart_Contract.pdf", "application/pdf")
            if st.button("Start New Transaction"):
                st.session_state['logs'] = []
                st.session_state['step'] = 1
                st.rerun()

    with col2:
        st.subheader("📊 Financial Overview")
        m1, m2, m3 = st.columns(3)
        m1.metric("Total Payable", f"{final_price:,.2f} {currency}")
        m2.metric("Monthly", f"{monthly_installment:,.2f} {currency}")
        m3.metric("Profit", f"{(final_price - price):,.2f} {currency}")
        
        tab1, tab2 = st.tabs(["📉 Amortization", "⛓️ Audit Chain"])
        with tab1:
            schedule_df = calculate_schedule(final_price, duration_months)
            st.line_chart(schedule_df, x="Month", y="Remaining Balance", color="#004C99")
            st.dataframe(schedule_df, use_container_width=True, hide_index=True)
        with tab2:
            if len(st.session_state['logs']) > 0:
                st.dataframe(pd.DataFrame(st.session_state['logs']), use_container_width=True)
            else:
                st.info("Waiting for transaction data...")



