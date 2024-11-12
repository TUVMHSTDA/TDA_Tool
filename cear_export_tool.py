import streamlit as st
import docx
import pandas as pd
import time  # Required for simulating progress
from streamlit_tree_select import tree_select
from pdf_extractor import extract_txt_list  # Daniel's script
from export_data import main as export_td
import fitz  # pymupdf

# Functions from auto_populator.py

def replace_content_control(element, namespaces=None):
    """Replaces xml w:sdt tags with the elements found under w:sdtContent"""
    kwargs = {} if not namespaces else {"namespaces": namespaces}  # xpath args can vary for docx objects vs lxml.etree
    sdt_elements = element.xpath(".//w:sdt", **kwargs)  # Get all w:sdt elements
    for e in sdt_elements:
        inner_elements = e.xpath(".//w:sdt", namespaces=e.nsmap)
        for inner_element in inner_elements:
            replace_content_control(inner_element, namespaces=e.nsmap)
        content_elements = e.xpath(".//w:sdtContent/*", namespaces=e.nsmap)  # Get all elements under sdtContent
        for c in content_elements:
            e.addprevious(c)  # Add content outside of sdt tag
        parent = e.getparent()
        if parent is not None:
            parent.remove(e)  # Remove sdt tag


def remove_hidden_text(element, namespaces=None):
    """Removes any XML elements with the hidden text property (w:vanish)."""
    # Setting up namespaces for the search
    kwargs = {} if not namespaces else {"namespaces": namespaces}
    
    hidden_element1 = element.xpath(".//w:p[w:pPr/w:pStyle[@w:val='Informationinvisibelblau']]", **kwargs)
    hidden_element2 = element.xpath(".//w:p[w:pPr/w:pStyle[@w:val='Informationinvisibelgrn']]", **kwargs)
    
    style_elements = hidden_element1 + hidden_element2

    # Remove each element from its parent
    for e in style_elements:
        parent = e.getparent()
        if parent is not None:
            parent.remove(e)  # Remove the element


def extract_text_between_markers(text, start_marker, end_marker):
    try:
        start_index = text.index(start_marker) + len(start_marker)
        end_index = text.index(end_marker)
        return "\n" + text[start_index:end_index].strip() + "\n"
    except ValueError:
        return "Markers not found in the provided text."


def fill_placeholder(template_doc, placeholder, full_text, start_marker, end_marker):
    extracted_text = extract_text_between_markers(full_text, start_marker, end_marker)
    
    # Replace in paragraphs
    for para in template_doc.paragraphs:
        if placeholder in para.text:
            para.text = para.text.replace(placeholder, extracted_text)

    # Replace in tables
    for table in template_doc.tables:
        for row in table.rows:
            for cell in row.cells:
                for para in cell.paragraphs:
                    if placeholder in para.text:
                        para.text = para.text.replace(placeholder, extracted_text)


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
            # Save uploaded file to a temporary location
            temp_word_path = os.path.join(tempfile.gettempdir(), uploaded_word_file.name)
            with open(temp_word_path, "wb") as f:
                f.write(uploaded_word_file.getbuffer())
            st.session_state.word_file_path = temp_word_path

        uploaded_cear_template = st.file_uploader("Upload CEAR Template", type=["docx"])
        if uploaded_cear_template is not None:
            # Save uploaded file to a temporary location
            temp_template_path = os.path.join(tempfile.gettempdir(), uploaded_cear_template.name)
            with open(temp_template_path, "wb") as f:
                f.write(uploaded_cear_template.getbuffer())
            st.session_state.cear_template_path = temp_template_path

        if st.button("Export"):
            self.export_with_progress()

    def export_with_progress(self):
        progress_bar = st.progress(0)
        for i in range(1, 10):
            progress_bar.progress(i * 10)
            st.write(f"Step {i}/9: Processing...")
            time.sleep(0.5)
        
        # Check if files are correctly saved in session state
        if st.session_state.get("word_file_path") and st.session_state.get("cear_template_path"):
            self.auto_populate()
            st.success("Export complete!")
        else:
            st.error("Please upload both documents before exporting.")

    def auto_populate(self):
        source_doc_path = st.session_state.word_file_path
        template_doc_path = st.session_state.cear_template_path
        output_doc_path = source_doc_path.replace(".docx", "_Filled.docx")
        
        # Load documents
        source_doc = docx.Document(source_doc_path)
        template_doc = docx.Document(template_doc_path)
        
        # Remove hidden text and content controls
        remove_hidden_text(source_doc.element)
        for p in source_doc.paragraphs:
            replace_content_control(p._element)
        for t in source_doc.tables:
            replace_content_control(t._element)
        
        # Extract all text from source document
        full_text = "\n".join([para.text for para in source_doc.paragraphs])

        # Define placeholders and markers within template document
        sections = [
            ('%productname%', "Product or trade name:", "Reference list of applicable or corresponding UDI-DIs assigned: "),
            ('%basicudi%', "Basic UDI device identifier(s)", "Test specifications"),
            ('%mdan%', "MDN / MDA and MDS code(s)", "Basic UDI device identifier(s)"),
            ('%manufacturer%', "Legal manufacturer", "Single registration number"),
            ('%srn%', "Single registration number", "Authorised representative"),
            ('%authorep%', "Authorised representative", "Production location(s)"),
            ('%devicedescription%', "General description of the device:", 
             "Intended purpose of the device in accordance with the current instructions for use:"),
            ('%intendedpurpose%', "Intended purpose of the device in accordance with the current instructions for use: ", 
             "Intended user of the device:"),
            ('%intendeduser%', "Intended user of the device:", 
             "Intended patient population, patient selection criteria, indications, contraindications, warnings (MDR Annex II Section 1.1(c))"),
            ('%populationcontra%', "Intended patient population, patient selection criteria, indications, contraindications, warnings (MDR Annex II Section 1.1(c))", 
             "Warning:"),
            ('%contraindications%', "Contraindication:", "Warning:"),
            ('%warnings%', "Warning:", "Principles of operation of the device and its mode of action (MDR Annex II, Section 1.1(d))"),
            ('%deviceconfig%', "List of all configurations and variants of the device intended to be made available on the market:", 
             "Accessories and device combinations (MDR Annex II Sections 1.1(h), 1.1(i))"),
            ('%accessories%', "List of accessories provided with the device:", "Combined devices"),
            ('%previousgen%', "Overview of a previous generation or generations of the device: ", "INFORMATION SUPPLIED BY THE MANUFACTURER ")
        ]

        # Replace placeholders in the template document
        for placeholder, start_marker, end_marker in sections:
            fill_placeholder(template_doc, placeholder, full_text, start_marker, end_marker)

        template_doc.save(output_doc_path)
        st.write(f"Populated document saved to: {output_doc_path}")

# Run the tool
if __name__ == "__main__":
    tool = CEARExportTool()
    tool.run()
