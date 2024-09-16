import streamlit as st
import pandas as pd

# Possible column names that could represent the "Instrument Name"
INSTRUMENT_NAME_COLUMNS = ['SEM_INSTRUMENT_NAME','Name','Names', 'Instrument', 'Instrument Name', 'Stock Name']

# Function to upload and cache the file
@st.cache_data
def load_file(uploaded_file):
    if uploaded_file.name.endswith('.csv'):
        return pd.read_csv(uploaded_file)
    elif uploaded_file.name.endswith('.xlsx'):
        return pd.read_excel(uploaded_file)
    else:
        return None

# Function to find the correct "Instrument Name" column
def find_instrument_column(df):
    for col in INSTRUMENT_NAME_COLUMNS:
        if col in df.columns:
            return col
    return None

# Page for uploading the main file
def upload_page():
    st.title("Upload CSV or Excel")

    # File uploader for the first CSV or Excel file
    uploaded_file = st.file_uploader("Choose a CSV or Excel file for main data", type=["csv", "xlsx"])
    
    if uploaded_file is not None:
        try:
            # Load the file using the cached function
            data = load_file(uploaded_file)
            st.session_state['uploaded_data'] = data  # Store main data in session_state

            # Display the data in a table
            st.dataframe(data)

        except Exception as e:
            st.error(f"Error: {e}")

# Page for filtering settings with a separate CSV file
def filtering_page():
    st.title("Upload a Separate CSV for Filtering")

    # File uploader for a separate CSV file for filtering
    filter_file = st.file_uploader("Choose a CSV file for filtering", type=["csv"])
    
    if filter_file is not None:
        try:
            # Load the filtering file using the cached function
            filter_data = load_file(filter_file)
            st.session_state['filter_data'] = filter_data  # Store filter data in session_state

            # Display the filter data
            st.dataframe(filter_data)
        except Exception as e:
            st.error(f"Error: {e}")

    # Proceed with filtering if the file is uploaded
    if 'filter_data' in st.session_state:
        data = st.session_state['filter_data']

        # Find the correct instrument column
        instrument_column = find_instrument_column(data)

        if instrument_column:
            # Populate the instrument names from the filtering file
            instrument_names = data[instrument_column].unique()

            # Create a selectbox for Instrument Name
            selected_instrument = st.selectbox(f"Select Instrument ({instrument_column})", instrument_names)

            # Filter the data based on selected instrument
            filtered_data = data[data[instrument_column] == selected_instrument]

            # Display the filtered data
            st.write(f"Filtered data for: {selected_instrument}")
            st.dataframe(filtered_data)
        else:
            st.error(f"Could not find an 'Instrument Name' column in the filtering file. Please check your file's column headers.")
    else:
        st.write("Please upload a separate CSV file for filtering.")

# Main function to create the sidebar and navigation
def main():
    st.sidebar.title("Navigation")
    page = st.sidebar.selectbox("Select a page", ["Upload", "Settings"])

    if page == "Upload":
        upload_page()
    elif page == "Settings":
        filtering_page()

if __name__ == "__main__":
    main()
