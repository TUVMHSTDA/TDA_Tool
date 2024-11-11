import streamlit as st
import pandas as pd
import json
from streamlit_tree_select import tree_select
from pdf_extractor import extract_txt_list  # Daniel's script
from export_data import main as export_td
import fitz  # pymupdf
import time  # Required for simulating progres

class OCRCheckTool:
    def __init__(self):
        pass

    def needs_ocr(self, uploaded_file):
        if uploaded_file.name.endswith(".pdf"):
            doc = fitz.open(stream=uploaded_file.read(), filetype="pdf")
            for page_num in range(len(doc)):
                page = doc.load_page(page_num)
                text = page.get_text()
                if not text.strip():  # If no text is detected
                    return True
            return False
        else:
            st.warning(f"Skipping unsupported file: {uploaded_file.name}")
            return None

    def run(self):
        st.title("OCR Check Tool")
        st.write("Upload files to perform OCR checks on them.")

        uploaded_files = st.file_uploader(
            "Upload PDF or DOCX Files", type=["pdf", "docx"], accept_multiple_files=True
        )

        if uploaded_files:
            st.write("Performing OCR check on uploaded files:")
            for uploaded_file in uploaded_files:
                ocr_needed = self.needs_ocr(uploaded_file)
                if ocr_needed is None:
                    continue  # Skip unsupported files
                status_message = "Failed" if ocr_needed else "Passed"
                status_color = "red" if ocr_needed else "green"
                st.markdown(
                    f"- **{uploaded_file.name}**: <span style='color:{status_color}'>{status_message}</span>",
                    unsafe_allow_html=True
                )
