import streamlit as st
import pandas as pd
import hashlib
import datetime
from io import BytesIO
from fpdf import FPDF

# --- 1. Page Configuration (Must be the very first command) ---
st.set_page_config(page_title="Islamic Murabaha System", layout="wide", page_icon="🏦")

# ==========================================
# 🔐 SECURE LOGIN SYSTEM ()
# ==========================================

# Login status configuration
if 'authentication_status' not in st.session_state:
    st.session_state['authentication_status'] = False

def login_page():
    # Design an elegant login page in the middle
    col1, col2, col3 = st.columns([1, 2, 1])
    
    with col2:
        st.markdown("<br><br>", unsafe_allow_html=True)
        st.image("https://cdn-icons-png.flaticon.com/512/2480/2480421.png", width=100) # أيقونة بنك
        st.title("🔒 Bank Staff Portal")
        st.markdown("Please sign in to access the Murabaha Audit System.")
        
        with st.form("login_form"):
            username = st.text_input("Username")
            password = st.text_input("Password", type="password")
            submit_button = st.form_submit_button("Sign In")
            
            if submit_button:
                if username == "admin" and password == "1234":
                    st.session_state['authentication_status'] = True
                    st.success("Login Successful!")
                    st.rerun() # Refresh the page to go to the app
                else:
                    st.error("❌ Incorrect Username or Password")

# If the user is not logged in, display the login page and stop.
if st.session_state['authentication_status'] == False:
    login_page()
    st.stop() # 🛑 This prevents the rest of the application from appearing.



# Logout button in the side menu
with st.sidebar:
    st.write(f"👤 User: **Admin**")
    if st.button("Log Out"):
        st.session_state['authentication_status'] = False
        st.rerun()
    st.divider()

# --- Debut R ---

st.title("🏦 Blockchain Murabaha Audit System")
st.markdown("### AAOIFI-Compliant Audit Engine & Financial Simulator")

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

def create_contract_pdf(client_name, asset, price, logs):
    pdf = FPDF()
    pdf.add_page()
    pdf.set_font("Arial", size=12)
    # Header
    pdf.set_font("Arial", 'B', 16)
    pdf.cell(0, 10, txt="Islamic Murabaha Contract", ln=True, align='C')
    pdf.set_font("Arial", size=10)
    pdf.cell(0, 10, txt="Automated Sharia-Compliant Transaction (AAOIFI No.8)", ln=True, align='C')
    pdf.ln(10)
    # Details
    pdf.set_font("Arial", 'B', 12)
    pdf.cell(0, 10, txt="Transaction Details:", ln=True)
    pdf.set_font("Arial", size=12)
    pdf.cell(0, 10, txt=f"Client Name: {client_name}", ln=True)
    pdf.cell(0, 10, txt=f"Asset Description: {asset}", ln=True)
    pdf.cell(0, 10, txt=f"Total Murabaha Price: ${price:,.2f}", ln=True)
    pdf.cell(0, 10, txt=f"Contract Date: {datetime.date.today()}", ln=True)
    pdf.ln(10)
    # Hash
    pdf.set_font("Arial", 'B', 14)
    pdf.cell(0, 10, txt="Digital Audit Trail (Immutable Ledger)", ln=True)
    pdf.set_font("Courier", size=9)
    pdf.multi_cell(0, 8, txt="The following cryptographic hashes verify the sequence integrity:")
    pdf.ln(2)
    for log in logs:
        clean_line = f"[{log['Step']}] {log['Timestamp']}\nHash: {log['Block Hash']}\n"
        pdf.multi_cell(0, 8, txt=clean_line, border=1)
        pdf.ln(2)
    # Signature
    pdf.ln(20)
    pdf.cell(0, 10, txt="_" * 40, ln=True)
    pdf.cell(0, 10, txt="Authorized Digital Signature", ln=True)
    return pdf.output(dest='S').encode('latin-1')

# --- Session State ---
if 'logs' not in st.session_state:
    st.session_state['logs'] = []
if 'step' not in st.session_state:
    st.session_state['step'] = 1 

# --- Layout ---
col1, col2 = st.columns([1, 1.5]) 

# COLUMN 1: INPUTS
with col1:
    st.header("📝 Transaction Details")
    with st.container(border=True):
        client_name = st.text_input("Client Name", "Hamza Bensliman")
        item_name = st.text_input("Asset Name", "Toyota Camry 2025")
        price = st.number_input("Cost Price (Bank's Cost)", min_value=0, value=25000)
        profit_margin = st.number_input("Profit Margin (%)", min_value=0, value=10)
        duration_months = st.number_input("Financing Duration (Months)", min_value=1, value=12)
        
        final_price = price + (price * profit_margin / 100)
        monthly_installment = final_price / duration_months
        st.info(f"Final Selling Price: ${final_price:,.2f}")

    st.divider()
    st.subheader("⚙️ Execution Workflow")
    
    # Step 1
    if st.session_state['step'] == 1:
        st.markdown("#### Phase 1: Purchase Order")
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

    # Step 2
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

    # Step 3
    elif st.session_state['step'] == 3:
        st.markdown("#### Phase 3: Murabaha Sale")
        if st.button("3. Execute Murabaha Sale", type="primary"):
            timestamp = str(datetime.datetime.now())
            prev_hash = st.session_state['logs'][-1]['Block Hash']
            data_to_hash = f"SALE-{item_name}-{final_price}-{timestamp}-{prev_hash}"
            block_hash = generate_hash(data_to_hash)
            st.session_state['logs'].append({
                "Step": "3. Murabaha Sale", "Description": f"Contract concluded.",
                "Timestamp": timestamp, "Block Hash": block_hash, "Sharia Status": "Transaction Complete"
            })
            st.session_state['step'] = 4
            st.rerun()
            
    # Completion
    elif st.session_state['step'] == 4:
        st.success("✅ Transaction Successfully Audited.")
        st.write("### 📄 Contract Generation")
        pdf_data = create_contract_pdf(client_name, item_name, final_price, st.session_state['logs'])
        st.download_button(
            label="⬇️ Download Smart Contract (PDF)",
            data=pdf_data,
            file_name=f"Smart_Contract_{datetime.date.today()}.pdf",
            mime="application/pdf",
            type="primary"
        )
        st.divider()
        if st.button("Start New Transaction"):
            st.session_state['logs'] = []
            st.session_state['step'] = 1
            st.rerun()

# COLUMN 2: DASHBOARD
with col2:
    st.header("💰 Financial Dashboard")
    m1, m2, m3 = st.columns(3)
    m1.metric("Total Payable", f"${final_price:,.2f}")
    m2.metric("Monthly Installment", f"${monthly_installment:,.2f}")
    m3.metric("Duration", f"{duration_months} Months")
    
    tab1, tab2 = st.tabs(["📈 Chart", "📋 Schedule Table"])
    schedule_df = calculate_schedule(final_price, duration_months)
    with tab1:
        st.line_chart(schedule_df, x="Month", y="Remaining Balance", color="#004C99")
    with tab2:
        st.dataframe(schedule_df, hide_index=True, use_container_width=True)

    st.divider()
    st.header("⛓️ Immutable Audit Ledger")
    if len(st.session_state['logs']) > 0:
        audit_df = pd.DataFrame(st.session_state['logs'])
        st.dataframe(audit_df[["Step", "Description", "Sharia Status"]], use_container_width=True, hide_index=True)
        buffer = BytesIO()
        with pd.ExcelWriter(buffer, engine='xlsxwriter') as writer:
            audit_df.to_excel(writer, index=False, sheet_name='Audit Log')
            schedule_df.to_excel(writer, index=False, sheet_name='Payment Schedule')
        st.download_button(
            label="📥 Download Excel Report",
            data=buffer,
            file_name='Murabaha_Report.xlsx',
            mime='application/vnd.ms-excel'
        )
    else:
        st.info("Waiting for transaction steps...")



