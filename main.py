import streamlit as st
import pandas as pd
import json
from streamlit_tree_select import tree_select
from pdf_extractor import extract_txt_list  # Daniel's script
from export_data import main as export_td
import fitz  # pymupdf
import time  # Required for simulating progress

from ocr_check_tool import OCRCheckTool
from cear_export_tool import CEARExportTool

class TDAApp:
    def __init__(self):
        self.selected_page = None

    def setup_sidebar(self):
        with st.sidebar:
            st.image("./edited.png", width=150)
        self.selected_page = st.sidebar.selectbox(
            "Navigation",
            ("Home", "Tools", "Settings")
        )

    def display_home(self):
        col1, col2, col3 = st.columns([1, 1.5, 1])
        with col2:
            st.image("./edited.png", width=300)
            st.title("MHS TDA Tool")
            st.write("by TÜV SÜD")

    def display_settings(self):
        st.title("Settings")
        st.write("Configure your application settings here.")

    def run(self):
        self.setup_sidebar()
        if self.selected_page == "Home":
            self.display_home()
        elif self.selected_page == "Tools":
            tools_page = Tools()
            tools_page.run()
        elif self.selected_page == "Settings":
            self.display_settings()

class Tools:
    def __init__(self):
        self.tool_option = None

    def setup_tools_sidebar(self):
        self.tool_option = st.sidebar.selectbox(
            "Select Tool",
            ("OCR Check", "CEAR Export")
        )

    def run(self):
        self.setup_tools_sidebar()
        if self.tool_option == "OCR Check":
            ocr_tool = OCRCheckTool()
            ocr_tool.run()
        elif self.tool_option == "CEAR Export":
            cear_export_tool = CEARExportTool()
            cear_export_tool.run()

if __name__ == "__main__":
    app = TDAApp()
    app.run()
