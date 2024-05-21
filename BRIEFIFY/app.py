import streamlit as st
from model import generate_summary, extract_keywords

# Set page title and background color
st.set_page_config(page_title="BRIEFIFY", page_icon=":bulb:", layout="wide")

# Set title and subtitle
st.title("BRIEFIFY")
st.subheader("AI Based Text Summarizer and Keyword Extractor")

# Upload file and process
file = st.file_uploader("Upload file", type=['txt'])

if file is not None:
    st.write("File uploaded successfully!")
    st.write("Generating Summary and Extracting Keywords...")

    # Read file content
    text = file.read().decode("utf-8")

    # Extract keywords
    keywords = extract_keywords(text, top_n=10)

    # Display keywords in a box
    st.subheader("Keywords Highlighted")
    with st.expander("Keywords"):
        for keyword in keywords:
            st.markdown(f"- **{keyword}**")

    # Generate summary
    summary = generate_summary(text, 2)

    # Display number of words in the input file and summarized text
    col1, col2 = st.columns(2)
    with col1:
        st.info("Word Count in Input File")
        st.write(len(text.split()))
    with col2:
        st.success("Word Count in Summarized Text")
        st.write(len(summary.split()))

    # Display summary
    st.warning("Summary")
    st.write(summary)
