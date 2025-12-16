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
# 🎨 SIDEBAR: SETTINGS & BRANDING
# ==========================================
with st.sidebar:
    # 1. Logo Area (Placeholder image)
    st.image("https://cdn-icons-png.flaticon.com/512/2830/2830289.png", width=80)
    st.markdown("### **ShariaChain** \n *Islamic Finance Audit*")
    st.divider()
    
    # 2. Bank Configuration
    st.header("⚙️ System Configuration")
    
    # Currency Selection
    currency = st.selectbox("Operating Currency", ["MAD", "USD", "EUR"], index=0)
    
    # Default Bank Profit Margin
    default_profit = st.slider("Base Profit Margin (%)", 5.0, 20.0, 10.0, 0.5)
    
    # Max Financing Duration
    max_duration = st.number_input("Max Duration (Months)", value=60)
    
    st.divider()
    
    # 3. User Profile
    st.caption(f"👤 User: **Admin (Officer)**")
    if st.button("Logout", type="primary"):
        st.session_state['authentication_status'] = False
        st.rerun()

# ==========================================
# 🔐 SECURE LOGIN SYSTEM
# ==========================================
if 'authentication_status' not in st.session_state:
    st.session_state['authentication_status'] = False

def login_page():
    col1, col2, col3 = st.columns([1, 2, 1])
    with col2:
        st.markdown("<br><br>", unsafe_allow_html=True)
        st.title("🔒 Secure Staff Portal")
        st.write("Please log in to access the Audit Ledger.")
        with st.form("login_form"):
            username = st.text_input("Username")
            password = st.text_input("Password", type="password")
            if st.form_submit_button("Access System"):
                if username == "admin" and password == "1234":
                    st.session_state['authentication_status'] = True
                    st.rerun()
                else:
                    st.error("❌ Access Denied")

if not st.session_state['authentication_status']:
    login_page()
    st.stop()

# ==========================================
# 🏦 MAIN APPLICATION LOGIC
# ==========================================

st.title(f"🏦 Murabaha Audit Dashboard")
st.caption(f"Current System Currency: {currency} | AAOIFI Standard No.8 Compliance")
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
    # Header
    pdf.set_font("Arial", 'B', 16)
    pdf.cell(0, 10, txt="Islamic Murabaha Contract", ln=True, align='C')
    pdf.set_font("Arial", size=10)
    pdf.cell(0, 10, txt="Automated Sharia-Compliant Transaction", ln=True, align='C')
    pdf.ln(10)
    # Details
    pdf.set_font("Arial", 'B', 12)
    pdf.cell(0, 10, txt="Transaction Details:", ln=True)
    pdf.set_font("Arial", size=12)
    pdf.cell(0, 10, txt=f"Client Name: {client_name}", ln=True)
    pdf.cell(0, 10, txt=f"Asset: {asset}", ln=True)
    pdf.cell(0, 10, txt=f"Total Price: {price:,.2f} {curr}", ln=True)
    pdf.cell(0, 10, txt=f"Date: {datetime.date.today()}", ln=True)
    pdf.ln(10)
    # Hash
    pdf.set_font("Arial", 'B', 14)
    pdf.cell(0, 10, txt="Audit Trail (Blockchain Hashes)", ln=True)
    pdf.set_font("Courier", size=9)
    for log in logs:
        clean_line = f"[{log['Step']}] {log['Timestamp']}\nHash: {log['Block Hash']}\n"
        pdf.multi_cell(0, 8, txt=clean_line, border=1)
        pdf.ln(2)
    # Signature
    pdf.ln(20)
    pdf.cell(0, 10, txt="_" * 40, ln=True)
    pdf.cell(0, 10, txt="Authorized Signature", ln=True)
    return pdf.output(dest='S').encode('latin-1')

# --- Session State ---
if 'logs' not in st.session_state: st.session_state['logs'] = []
if 'step' not in st.session_state: st.session_state['step'] = 1 

# --- Layout ---
col1, col2 = st.columns([1, 1.5]) 

# LEFT COLUMN: Inputs & Actions
with col1:
    st.subheader("📝 New Transaction")
    with st.container(border=True):
        client_name = st.text_input("Client Name", "Hamza Bensliman")
        item_name = st.text_input("Asset Name", "Apartment Fes City")
        
        # Financial Inputs (Linked to Sidebar defaults)
        price = st.number_input(f"Cost Price ({currency})", min_value=0, value=250000)
        profit_margin = st.number_input("Profit Margin (%)", min_value=0.0, value=default_profit)
        duration_months = st.number_input("Duration (Months)", min_value=1, max_value=max_duration, value=12)
        
        final_price = price + (price * profit_margin / 100)
        monthly_installment = final_price / duration_months
        st.success(f"Final Price: {final_price:,.2f} {currency}")

    st.divider()
    
    # Workflow Steps
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

# RIGHT COLUMN: Dashboard
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



