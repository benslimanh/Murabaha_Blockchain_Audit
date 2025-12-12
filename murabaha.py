import streamlit as st
import pandas as pd
import hashlib
import datetime
from io import BytesIO  # مكتبة للتعامل مع الملفات في الذاكرة

# --- 1. Page Configuration ---
st.set_page_config(page_title="Islamic Murabaha System", layout="wide")
st.title("🏦 Blockchain Murabaha Audit System")
st.markdown("### AAOIFI-Compliant Audit Engine")
st.caption("A Prototype for enforcing sequential compliance in Islamic Finance using Blockchain Logic.")

# --- 2. Blockchain Functions ---
def generate_hash(data):
    sha = hashlib.sha256()
    sha.update(data.encode('utf-8'))
    return sha.hexdigest()

# --- 3. Session State ---
if 'logs' not in st.session_state:
    st.session_state['logs'] = []
if 'step' not in st.session_state:
    st.session_state['step'] = 1 

# --- 4. Application UI ---
col1, col2 = st.columns([1, 2])

with col1:
    st.header("📝 Contract Workflow")
    item_name = st.text_input("Asset Name", "Toyota Camry 2025")
    price = st.number_input("Cost Price (Bank's Cost)", min_value=0, value=25000)
    profit_margin = st.number_input("Profit Margin (%)", min_value=0, value=10)
    final_price = price + (price * profit_margin / 100)
    st.info(f"Final Selling Price to Client: ${final_price:,.2f}")
    st.divider()

    # Step 1
    if st.session_state['step'] == 1:
        st.markdown("#### Phase 1: Purchase Order")
        if st.button("1. Submit Promise to Purchase (Wa'd)"):
            timestamp = str(datetime.datetime.now())
            data_to_hash = f"REQUEST-{item_name}-{timestamp}"
            block_hash = generate_hash(data_to_hash)
            st.session_state['logs'].append({
                "Step": "1. Promise (Wa'd)", "Description": f"Client requested: {item_name}",
                "Timestamp": timestamp, "Block Hash": block_hash, "Sharia Status": "Valid (Promise)"
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
                "Step": "2. Bank Possession", "Description": "Bank acquired ownership",
                "Timestamp": timestamp, "Block Hash": block_hash, "Sharia Status": "Valid (Ownership)"
            })
            st.session_state['step'] = 3
            st.rerun()

    # Step 3
    elif st.session_state['step'] == 3:
        st.markdown("#### Phase 3: Murabaha Sale")
        if st.button("3. Execute Murabaha Sale"):
            timestamp = str(datetime.datetime.now())
            prev_hash = st.session_state['logs'][-1]['Block Hash']
            data_to_hash = f"SALE-{item_name}-{final_price}-{timestamp}-{prev_hash}"
            block_hash = generate_hash(data_to_hash)
            st.session_state['logs'].append({
                "Step": "3. Murabaha Sale", "Description": f"Sold to Client for ${final_price}",
                "Timestamp": timestamp, "Block Hash": block_hash, "Sharia Status": "Transaction Complete"
            })
            st.session_state['step'] = 4
            st.rerun()
            
    elif st.session_state['step'] == 4:
        st.success("🎉 Transaction Completed.")
        if st.button("Start New Transaction"):
            st.session_state['logs'] = []
            st.session_state['step'] = 1
            st.rerun()

with col2:
    st.header("⛓️ Immutable Audit Ledger")
    
    if len(st.session_state['logs']) > 0:
        df = pd.DataFrame(st.session_state['logs'])
        df = df[["Step", "Description", "Timestamp", "Sharia Status", "Block Hash"]]
        st.table(df)

        st.divider()
        st.markdown("### 📥 Export Professional Report")

        # --- بداية السحر: تحويل الملف إلى Excel منسق ---
        buffer = BytesIO()
        with pd.ExcelWriter(buffer, engine='xlsxwriter') as writer:
            # 1. كتابة البيانات
            df.to_excel(writer, index=False, sheet_name='Audit Log')
            
            # 2. الحصول على كائنات التنسيق
            workbook = writer.book
            worksheet = writer.sheets['Audit Log']
            
            # 3. تعريف الأنماط (Styles)
            header_format = workbook.add_format({
                'bold': True,
                'text_wrap': True,
                'valign': 'top',
                'fg_color': '#004C99',
                'font_color': '#FFFFFF',
                'border': 1
            })
            
            # --- التعديل هنا: أضفنا text_wrap: True ---
            cell_format = workbook.add_format({
                'border': 1,
                'valign': 'vcenter',
                'text_wrap': True  # هذا الأمر يجبر النص على البقاء داخل العمود
            })

            # 4. تطبيق التنسيق على الأعمدة
            worksheet.set_column('A:A', 20, cell_format) # Step
            worksheet.set_column('B:B', 30, cell_format) # Description
            worksheet.set_column('C:C', 20, cell_format) # Timestamp
            worksheet.set_column('D:D', 20, cell_format) # Status
            worksheet.set_column('E:E', 50, cell_format) # Hash (سيصبح النص الآن مرتباً داخله)

            # 5. تطبيق تنسيق العناوين
            for col_num, value in enumerate(df.columns.values):
                worksheet.write(0, col_num, value, header_format)

        # تجهيز الملف للتحميل
        st.download_button(
            label="Download Excel Report (.xlsx)",
            data=buffer,
            file_name='Murabaha_Audit_Report.xlsx',
            mime='application/vnd.ms-excel'
        )
