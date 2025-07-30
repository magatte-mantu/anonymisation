import streamlit as st
import tempfile
import os
from anonymisation import anonymize_sql_procedure
from desanonymisation import desanonymize_sql

st.set_page_config(page_title="SQL Anonymizer", layout="wide")
st.title("🔐 SQL Query Anonymizer & Deanonymizer")

st.markdown("""
This tool lets you anonymize sensitive SQL queries before sharing them with an AI tool (like ChatGPT), and then restore the original names afterward.
""")

# --- Input Method Selection ---
st.header("1️⃣ SQL Input")
input_method = st.radio("Select input method:", ["Paste manually", "Upload .sql file"])

if "last_mapping_path" not in st.session_state:
    st.session_state.last_mapping_path = None

if "last_input_path" not in st.session_state:
    st.session_state.last_input_path = None

if input_method == "Paste manually":
    col1, col2 = st.columns(2)

    with col1:
        sql_input_text = st.text_area("✍️ Paste your SQL code here:", height=400, key="manual_input")
        btn_anonymize = st.button("🔄 Anonymize", key="btn_anonymize")
        btn_deanonymize = st.button("♻️ Deanonymize", key="btn_deanonymize")

        output_text = ""

        if btn_anonymize:
            with tempfile.NamedTemporaryFile(delete=False, suffix=".sql", mode="w", encoding="utf-8") as tmp_in:
                tmp_in.write(sql_input_text)
                st.session_state.last_input_path = tmp_in.name

            output_path = tempfile.NamedTemporaryFile(delete=False, suffix=".sql").name
            st.session_state.last_mapping_path = tempfile.NamedTemporaryFile(delete=False, suffix=".txt").name

            anonymize_sql_procedure(
                st.session_state.last_input_path,
                output_path,
                st.session_state.last_mapping_path
            )

            with open(output_path, encoding="utf-8") as f:
                output_text = f.read()

        elif btn_deanonymize:
            if st.session_state.last_input_path and st.session_state.last_mapping_path:
                deanonymized_path = tempfile.NamedTemporaryFile(delete=False, suffix=".sql").name
                desanonymize_sql(
                    st.session_state.last_input_path,
                    st.session_state.last_mapping_path,
                    deanonymized_path
                )

                with open(deanonymized_path, encoding="utf-8") as f:
                    output_text = f.read()
            else:
                st.warning("⚠️ No previous anonymization mapping found.")

    with col2:
        st.text_area("📄 Output SQL:", value=output_text, height=400)

        if output_text:
            st.download_button(
                label="⬇️ Download output as .sql",
                data=output_text,
                file_name="result.sql",
                mime="text/plain"
            )


        if st.session_state.last_mapping_path:
            with open(st.session_state.last_mapping_path, encoding="utf-8") as f:
                mapping_preview = f.read()

            with st.expander("📋 View Mapping File"):
                st.code(mapping_preview, language="text")

else:
    uploaded_file = st.file_uploader("📄 Upload your SQL file", type="sql")
    if uploaded_file is not None:
        with tempfile.NamedTemporaryFile(delete=False, suffix=".sql") as tmp_file:
            tmp_file.write(uploaded_file.read())
            input_path = tmp_file.name

        output_path = tempfile.NamedTemporaryFile(delete=False, suffix=".sql").name
        mapping_path = tempfile.NamedTemporaryFile(delete=False, suffix=".txt").name

        if st.button("🔄 Anonymize uploaded file"):
            anonymize_sql_procedure(input_path, output_path, mapping_path)
            st.success("Anonymized successfully!")
            st.download_button("⬇️ Download anonymized SQL", open(output_path).read(), file_name="output.sql")
            st.download_button("⬇️ Download mapping file", open(mapping_path).read(), file_name="mapping.txt")


