import streamlit as st
import pandas as pd
import json
from streamlit_tree_select import tree_select
from pdf_extractor import extract_txt_list  # Daniel's script
from export_data import main as export_td
import fitz  # pymupdf

# Page configuration
st.set_page_config(
    page_title="TDA",
    page_icon="🧊",
    layout="wide"
)

# Add icon to the sidebar
with st.sidebar:
    st.image("./edited.png", width=150)  # Adjust size as needed

# Define navigation options
selected_page = st.sidebar.selectbox(
    "Navigation",
    ("Home", "Tools", "Settings")
)

# Define Tools sub-options when "Tools" is selected
if selected_page == "Tools":
    tool_option = st.sidebar.selectbox(
        "Select Tool",
        ("OCR Check", "CEAR Export")
    )

    # OCR Check Tool
    if tool_option == "OCR Check":
        st.title("OCR Check Tool")
        st.write("Upload files to perform OCR checks on them.")

        # Function to perform OCR check on each file
        def needs_ocr(uploaded_file):
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

        # File uploader for multiple PDFs and DOCX files
        uploaded_files = st.file_uploader(
            "Upload PDF or DOCX Files", type=["pdf", "docx"], accept_multiple_files=True
        )

        # Display OCR check results if files are uploaded
        if uploaded_files:
            st.write("Performing OCR check on uploaded files:")
            for uploaded_file in uploaded_files:
                ocr_needed = needs_ocr(uploaded_file)
                if ocr_needed is None:
                    continue  # Skip unsupported files
                status_message = "Failed" if ocr_needed else "Passed"
                status_color = "red" if ocr_needed else "green"

                # Display file name and OCR status
                st.markdown(
                    f"- **{uploaded_file.name}**: <span style='color:{status_color}'>{status_message}</span>",
                    unsafe_allow_html=True
                )

    # CEAR Export Tool
    elif tool_option == "CEAR Export":
        st.title("CEAR Export Tool")
        st.write("Upload the completed TDAR document and CEAR template to proceed with the export.")

        # Initialize session state to store file paths
        if "word_file_path" not in st.session_state:
            st.session_state.word_file_path = ""
        if "cear_template_path" not in st.session_state:
            st.session_state.cear_template_path = ""

        # File uploader for Word document
        uploaded_word_file = st.file_uploader("Upload Completed Word Document", type=["docx"])
        if uploaded_word_file is not None:
            if st.session_state.word_file_path != uploaded_word_file.name:
                st.session_state.word_file_path = f"/tmp/{uploaded_word_file.name}"
        st.text_input("Completed Word Document Directory", value=st.session_state.word_file_path, disabled=True)

        # File uploader for CEAR template
        uploaded_cear_template = st.file_uploader("Upload CEAR Template", type=["docx"])
        if uploaded_cear_template is not None:
            if st.session_state.cear_template_path != uploaded_cear_template.name:
                st.session_state.cear_template_path = f"/tmp/{uploaded_cear_template.name}"
        st.text_input("CEAR Template Directory", value=st.session_state.cear_template_path, disabled=True)

        # Export Button with Progress Bar
        if st.button("Export"):
            progress_bar = st.progress(0)

            # Simulate export process
            for i in range(1, 10):
                progress_bar.progress(i * 10)
                st.write(f"Step {i}/9: Processing...")
                time.sleep(0.5)

            st.success("Export complete!")

# Home Page
elif selected_page == "Home":
    col1, col2, col3, col4 = st.columns([1, 1, 2, 1])

    with col3:
        st.image("./edited.png", width=300)
        st.title("MHS TDA Tools")

# Settings Page
elif selected_page == "Settings":
    st.title("Settings")
    st.write("Configure your application settings here.")
