import streamlit as st
import pandas as pd
import os
import json
# import tkinter as tk
# from tkinter import filedialog
from streamlit_tree_select import tree_select
from pdf_extractor import extract_txt_list    # Daniel's script
# from extract_fields import main as extract    # Austin's script
from export_data import main as export_td
import pymupdf

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

    # # PDF Extraction Tool
    # if tool_option == "TDAR Export":
    #     st.title("TDAR Export")
    #         selected_files = select_folder()  # Use Streamlit file uploader
    #         if selected_files:
    #             if not needs_ocr(selected_files):
    #                 st.success("Files are ready for extraction!")
    #             else:
    #                 st.warning("OCR is needed for some files.")

    #     def file_tree(path):
    #         stack = [path]
    #         result = []
    #         parent_map = {path: result}

    #         while stack:
    #             current_path = stack.pop()
    #             current_nodes = parent_map[current_path]

    #             try:
    #                 for entry in os.scandir(current_path):
    #                     if entry.is_dir():
    #                         node = {
    #                             "label": entry.name,
    #                             "value": os.path.normpath(entry.path),
    #                             "children": []
    #                         }
    #                         current_nodes.append(node)
    #                         stack.append(entry.path)
    #                         parent_map[entry.path] = node["children"]
    #                     else:
    #                         if entry.path.endswith(".pdf") or entry.path.endswith(".docx"):
    #                             node = {
    #                                 "label": entry.name,
    #                                 "value": os.path.normpath(entry.path)
    #                             }
    #                             current_nodes.append(node)
    #             except:
    #                 pass

    #         nodes = result
    #         selected = tree_select(nodes, only_leaf_checkboxes=True)
    #         print(selected)
    #         return selected

    #     def show_td_table():
    #         output = {}

    #         # Opening JSON file
    #         f = open('./output.json')
            
    #         data = json.load(f)
            
    #         for i in range(len(data)):
    #             output[data[i]["column_name"]] = data[i]["answer"]
            
    #         f.close()

    #         subsection = list(output.keys())
    #         extracted_info = list(output.values())
    #         selection = []
    #         for i in enumerate(subsection):
    #             selection.append(False)
    #         file_location = ""
            
    #         d = {"Sub-Section": subsection, 
    #              "Extracted Data Points": extracted_info, 
    #              "Selection": selection, 
    #              "File Location": file_location}
    #         df = (pd.DataFrame(data=d)).explode("Extracted Data Points")

    #         return df

    #     def run_pdf_extraction():
    #         try:
    #             with open(r'./styles/style.css') as f:
    #                 css = f.read()
    #             st.markdown(f'<style>{css}</style>', unsafe_allow_html=True)

    #             col_file, col_table = st.columns([0.3, 0.7], gap="medium")

    #             with col_file:
    #                 with st.container():

    #                     selected_folder_path = st.session_state.get("folder_path", None)
    #                     if 'show' not in st.session_state:
    #                         st.session_state.show = False
    #                     if 'checked' not in st.session_state:
    #                         st.session_state.checked = False
    #                     if 'disable' not in st.session_state:
    #                         st.session_state.disable = True
    #                     if 'clicked' not in st.session_state:
    #                         st.session_state.clicked = False
    #                     if 'run' not in st.session_state:
    #                         st.session_state.run = 0

    #                     if selected_folder_path == None:
    #                         project_name = "New Project"
    #                     else:
    #                         project_name = os.path.basename(selected_folder_path)
                        
    #                     st.markdown(f'''
    #                                 <div class='margin-bottom bg_blue border'>
    #                                     <h4 class='margin-top margin-bottom bg_blue'>{project_name}</h4>
    #                                 </div>
    #                                 ''', unsafe_allow_html=True)

    #                     buttoncol1, buttoncol2, buttoncol3 = st.columns([0.5, 0.5, 0.5], gap="small")

    #                     with buttoncol1:    
    #                         folder_select_button = st.button(":heavy_plus_sign: Select folder")
                            
    #                         if folder_select_button:
    #                             selected_folder_path = select_folder()
    #                             st.session_state.folder_path = selected_folder_path
    #                             st.session_state.show = False
    #                             st.session_state.clicked = False
    #                             st.rerun()

    #                     if selected_folder_path != None:
    #                         selected_files = file_tree(selected_folder_path)

    #                         if selected_files["checked"]:
    #                             if not needs_ocr(selected_files["checked"]):
    #                                 st.session_state.checked = True
    #                                 st.session_state.disable = False

    #                                 if st.session_state.clicked == True:
    #                                     st.session_state.disable = True
                            
    #                         else:
    #                             st.session_state.checked = False
    #                             st.session_state.disable = True

    #                     with buttoncol2:
    #                         st.button(":arrow_down_small: Filter files")

    #                     with buttoncol3:
    #                         extract_details = st.button(":outbox_tray: Extract details", disabled=st.session_state.disable)
                            
    #                         if extract_details:
    #                             st.session_state.show = True
    #                             st.session_state.clicked = True
    #                             st.rerun()

    #             with col_table:
    #                 with st.container():
    #                     if st.session_state.show and st.session_state.checked:
    #                         extract_txt_list(selected_files["checked"])

    #                         header = "TD ASSESSMENT [Tool Ver.]"
    #                         st.markdown(f'''
    #                                     <div class='margin-bottom bg_blue border'>
    #                                         <h5>{header}</h5>
    #                                     </div>
    #                                     ''', unsafe_allow_html=True)
                            
    #                         with st.container():
    #                             df = show_td_table()
    #                             edited_df = st.data_editor(
    #                                             df, 
    #                                             column_config={
    #                                             "Selection": st.column_config.CheckboxColumn(
    #                                                 "Selection",
    #                                                 default=False
    #                                             )},
    #                                             hide_index=True, 
    #                                             disabled=["Sub-Section"], 
    #                                             use_container_width=True)

    #                         subcol1, subcol2, subcol3 = st.columns([0.3, 1, 0.2])
    #                         with subcol3:
    #                             filename = 'edited_data.json'
                                
    #                             if st.button("Export"):
    #                                 edited_df.to_json(filename, orient="records")
    #                                 export_td()

    #         except TypeError:
    #             pass

    #     run_pdf_extraction()

    # OCR Check Tool
    if tool_option == "OCR Check":
        st.title("OCR Check Tool")
        st.write("Select a folder to perform OCR checks on the files within it.")

        # Replace Tkinter's folder selector with Streamlit's file uploader
        def select_folder():
            uploaded_files = st.file_uploader("Upload PDF or DOCX Files", type=["pdf", "docx"], accept_multiple_files=True)
            if uploaded_files:
                return [file.name for file in uploaded_files]  # Return a list of file names

        # Modify file tree logic for uploaded files
        def file_tree(files):
            nodes = [{"label": file, "value": file} for file in files]
            selected = tree_select(nodes, only_leaf_checkboxes=True)
            return selected

        # PDF extraction logic using Streamlit's file_uploader
        def needs_ocr(file_list):
            for file in file_list:
                if file.name.endswith(".pdf"):
                    doc = pymupdf.open(file)
                    for page_num in range(len(doc)):
                        page = doc.load_page(page_num)
                        text = page.get_text()
                        if not text.strip():
                            return True
            return False

        # Initialize session state for folder path and file list
        if "ocr_folder_path" not in st.session_state:
            st.session_state.ocr_folder_path = ""
        if "ocr_files" not in st.session_state:
            st.session_state.ocr_files = []

        # Button to select a folder
        if st.button("Select Folder for OCR Check"):
            selected_folder_path = select_folder()
            st.session_state.ocr_folder_path = selected_folder_path  # Save folder path in session state

            # Retrieve and display all files in the folder
            file_list = [
                file.path for file in os.scandir(selected_folder_path)
                if file.is_file() and (file.path.endswith(".pdf") or file.path.endswith(".docx"))
            ]
            st.session_state.ocr_files = file_list

        # Display the selected folder path
        st.text_input("Selected Folder Path", value=st.session_state.ocr_folder_path, disabled=True)

        # Display files in the folder and OCR check status
        if st.session_state.ocr_files:
            st.write("Performing OCR check on the files in the selected folder:")
            for file_path in st.session_state.ocr_files:
                # Check if OCR is needed for each file
                ocr_needed = needs_ocr(file_path)
                status_message = "Failed" if ocr_needed else "Passed"
                status_color = "red" if ocr_needed else "green"

                # Display each file's path and OCR status
                st.markdown(f"- **{file_path}**: <span style='color:{status_color}'>{status_message}</span>", unsafe_allow_html=True)

    # CEAR Export Tool
    elif tool_option == "CEAR Export":
        st.title("CEAR Export Tool")
        st.write("Upload the completed TDAR document and CEAR template to proceed with the export.")

        # Initialize session state to store file paths
        if "word_file_path" not in st.session_state:
            st.session_state.word_file_path = ""
        if "cear_template_path" not in st.session_state:
            st.session_state.cear_template_path = ""

        # Button and text field for uploading the completed Word document
        uploaded_word_file = st.file_uploader("Upload Completed Word Document", type=["docx"])
        if uploaded_word_file is not None:
            # Update session state only if there's a new file upload
            if st.session_state.word_file_path != uploaded_word_file.name:
                st.session_state.word_file_path = f"/tmp/{uploaded_word_file.name}"
        st.text_input("Completed Word Document Directory", value=st.session_state.word_file_path, disabled=True)

        # Button and text field for uploading the CEAR template
        uploaded_cear_template = st.file_uploader("Upload CEAR Template", type=["docx"])
        if uploaded_cear_template is not None:
            # Update session state only if there's a new file upload
            if st.session_state.cear_template_path != uploaded_cear_template.name:
                st.session_state.cear_template_path = f"/tmp/{uploaded_cear_template.name}"
        st.text_input("CEAR Template Directory", value=st.session_state.cear_template_path, disabled=True)

        # Export Button at the bottom of the page with Progress Bar
        if st.button("Export"):
            # Initialize progress bar
            progress_bar = st.progress(0)
            
            # Simulate export steps with progress updates
            for i in range(1, 9):  # Example: 10 steps
                # Here you would add the actual logic for each export step
                # E.g., process file, save data, etc.
                
                progress_bar.progress(i * 10)  # Update progress (10%, 20%, ..., 100%)
                st.write(f"Step {i}/9: Processing...")  # Display step information
                time.sleep(0.5)  # Simulate time taken for each step

            st.success("Export complete!")

# Home Page
elif selected_page == "Home":
    # Display the TUV SUD logo
    st.image("./edited.png", width=300)  # Adjust the path and size as needed
    st.title("MHS TDA Tools")

# Settings Page
elif selected_page == "Settings":
    st.title("Settings")
    st.write("Configure your application settings here.")