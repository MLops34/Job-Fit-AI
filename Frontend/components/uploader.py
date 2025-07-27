import streamlit as st

def upload_resume():
    st.file_uploader("📤 Upload your resume", type=["pdf", "docx", "txt"])
