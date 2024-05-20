import streamlit as st
from model import generate_summary

st.title("Text Summarizer")

file = st.file_uploader("Upload file", type=['txt'])

if file is not None:
    st.write("File uploaded successfully!")
    st.write("Generating Summary...")

    summary = generate_summary(file.name, 2)
    
    st.subheader("Summary:")
    st.write(summary)
