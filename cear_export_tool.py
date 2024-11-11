import streamlit as st
import pandas as pd
import json
from streamlit_tree_select import tree_select
from pdf_extractor import extract_txt_list  # Daniel's script
from export_data import main as export_td
import fitz  # pymupdf
import time  # Required for simulating progress

class CEARExportTool:
    def __init__(self):
        if "word_file_path" not in st.session_state:
            st.session_state.word_file_path = ""
        if "cear_template_path" not in st.session_state:
            st.session_state.cear_template_path = ""

    def run(self):
        st.title("CEAR Export Tool")
        st.write("Upload the completed TDAR document and CEAR template to proceed with the export.")

        uploaded_word_file = st.file_uploader("Upload Completed Word Document", type=["docx"])
        if uploaded_word_file is not None:
            if st.session_state.word_file_path != uploaded_word_file.name:
                st.session_state.word_file_path = f"/tmp/{uploaded_word_file.name}"
        st.text_input("Completed Word Document Directory", value=st.session_state.word_file_path, disabled=True)

        uploaded_cear_template = st.file_uploader("Upload CEAR Template", type=["docx"])
        if uploaded_cear_template is not None:
            if st.session_state.cear_template_path != uploaded_cear_template.name:
                st.session_state.cear_template_path = f"/tmp/{uploaded_cear_template.name}"
        st.text_input("CEAR Template Directory", value=st.session_state.cear_template_path, disabled=True)

        if st.button("Export"):
            self.export_with_progress()

    def export_with_progress(self):
        progress_bar = st.progress(0)
        for i in range(1, 10):
            progress_bar.progress(i * 10)
            st.write(f"Step {i}/9: Processing...")
            time.sleep(0.5)
        st.success("Export complete!")
