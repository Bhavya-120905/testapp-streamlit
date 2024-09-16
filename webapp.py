import streamlit as st
import pandas as pd

# Sidebar for navigation
st.sidebar.title("Navigation")
page = st.sidebar.selectbox("Choose a page", ["Home", "Upload CSV/Excel"])

if page == "Home":
    # Home page content
    st.title("Welcome to the Home Page!")
    st.write("Use the sidebar to navigate to the file upload page.")
    
elif page == "Upload CSV/Excel":
    # Upload page content
    st.title("Upload CSV or Excel File")

    # File uploader widget
    uploaded_file = st.file_uploader("Choose a file", type=["csv", "xlsx"])

    if uploaded_file is not None:
        # Check file type
        if uploaded_file.name.endswith('.csv'):
            df = pd.read_csv(uploaded_file)
        elif uploaded_file.name.endswith('.xlsx'):
            df = pd.read_excel(uploaded_file)

        # Display the file as a table
        st.write("Here is your data:")
        st.dataframe(df)
    else:
        st.write("Please upload a CSV or Excel file.")
