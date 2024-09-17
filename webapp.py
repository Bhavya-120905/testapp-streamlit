import streamlit as st
import pandas as pd
from datetime import datetime
import os

# Hardcoded admin credentials
ADMIN_USER = "admin"
ADMIN_PASS = "password123"

# File paths
SCRIP_MASTER_PATH = "latest_scrip_master.csv"
TRADE_HISTORY_DIR = "trade_histories/"

# Create the directory if it doesn't exist for trade histories
if not os.path.exists(TRADE_HISTORY_DIR):
    os.makedirs(TRADE_HISTORY_DIR)

# Function to load the file (cached)
@st.cache_data
def load_file(file_path_or_uploaded_file):
    if isinstance(file_path_or_uploaded_file, str):  # If it's a file path (string)
        if file_path_or_uploaded_file.endswith('.csv'):
            return pd.read_csv(file_path_or_uploaded_file)
        elif file_path_or_uploaded_file.endswith('.xlsx'):
            return pd.read_excel(file_path_or_uploaded_file)
    else:  # If it's an uploaded file
        if file_path_or_uploaded_file.name.endswith('.csv'):
            return pd.read_csv(file_path_or_uploaded_file)
        elif file_path_or_uploaded_file.name.endswith('.xlsx'):
            return pd.read_excel(file_path_or_uploaded_file)
    return None

# Admin authentication check
def authenticate():
    st.sidebar.header("Admin Login")
    username = st.sidebar.text_input("Username")
    password = st.sidebar.text_input("Password", type="password")
    if username == ADMIN_USER and password == ADMIN_PASS:
        st.session_state['authenticated'] = True
        return True
    else:
        st.session_state['authenticated'] = False
        st.sidebar.warning("Invalid credentials")
        return False

# Admin page for managing Scrip Master file
def admin_page():
    st.title("Admin - Manage Scrip Master File")

    # Check if a Scrip Master file already exists
    if os.path.exists(SCRIP_MASTER_PATH):
        st.write("Current Scrip Master File:")
        scrip_master = load_file(SCRIP_MASTER_PATH)
        st.dataframe(scrip_master)

        # Option to delete the current Scrip Master file
        if st.button("Delete Current Scrip Master File"):
            try:
                os.remove(SCRIP_MASTER_PATH)
                st.success("Scrip Master file has been deleted.")
            except Exception as e:
                st.error(f"Error deleting file: {e}")
    else:
        st.warning("No Scrip Master file currently exists.")

    # Option to upload a new Scrip Master file (update)
    uploaded_file = st.file_uploader("Upload a new Scrip Master file", type=["csv", "xlsx"])

    if uploaded_file is not None:
        try:
            # Save the uploaded file as the latest scrip master
            file_data = load_file(uploaded_file)
            file_data.to_csv(SCRIP_MASTER_PATH, index=False)
            st.success(f"New Scrip Master file successfully uploaded and saved as {SCRIP_MASTER_PATH}.")
        except Exception as e:
            st.error(f"Error: {e}")

# Viewer page for viewing and filtering Scrip Master
def viewer_page():
    st.title("Viewer - Scrip Master")

    # Check if the latest Scrip Master file exists
    if os.path.exists(SCRIP_MASTER_PATH):
        try:
            # Load the Scrip Master file
            scrip_master = load_file(SCRIP_MASTER_PATH)

            # Apply filters for Scrip Master
            # Filter by "SEM_EXM_EXCH_ID"
            if "SEM_EXM_EXCH_ID" in scrip_master.columns:
                exch_ids = scrip_master['SEM_EXM_EXCH_ID'].unique()
                selected_exch_id = st.selectbox("Filter by Exchange ID (SEM_EXM_EXCH_ID)", exch_ids)
                scrip_master = scrip_master[scrip_master['SEM_EXM_EXCH_ID'] == selected_exch_id]


            if "SEM_INSTRUMENT_NAME" in scrip_master.columns:
                inst_name = scrip_master['SEM_INSTRUMENT_NAME'].unique()
                selected_inst_name = st.selectbox("Filter by Instrument Name (SEM_INSTRUMENT_NAME)", inst_name)
                scrip_master = scrip_master[scrip_master['SEM_INSTRUMENT_NAME'] == selected_inst_name]

            # Add more filters (example with SEM_STRIKE_PRICE)
            if "SEM_STRIKE_PRICE" in scrip_master.columns:
                strike_min = scrip_master['SEM_STRIKE_PRICE'].min()
                strike_max = scrip_master['SEM_STRIKE_PRICE'].max()
                if strike_min != strike_max:
                    selected_strike = st.slider("Filter by Strike Price (SEM_STRIKE_PRICE)",
                                                min_value=strike_min, max_value=strike_max)
                    scrip_master = scrip_master[scrip_master['SEM_STRIKE_PRICE'] == selected_strike]
                else:
                    st.write(f"Only one unique Strike Price value: {strike_min}")

            # Display filtered data
            st.write("Filtered Data:")
            st.dataframe(scrip_master)

        except Exception as e:
            st.error(f"Error loading Scrip Master: {e}")
    else:
        st.warning("Scrip Master file not available. Please check with the admin.")

# Viewer page for uploading and viewing their trade history
def trade_history_page():
    st.title("Viewer - Trade History")

    # Trade history file upload
    uploaded_trade_file = st.file_uploader("Upload your trade history file", type=["csv", "xlsx"])

    if uploaded_trade_file is not None:
        try:
            # Save the user's trade history with a timestamp
            timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
            trade_file_path = os.path.join(TRADE_HISTORY_DIR, f"trade_history_{timestamp}.csv")
            file_data = load_file(uploaded_trade_file)
            file_data.to_csv(trade_file_path, index=False)
            st.success(f"Trade history successfully uploaded and saved as {trade_file_path}.")
        except Exception as e:
            st.error(f"Error: {e}")

    # Viewing previously uploaded trade history
    st.write("Your uploaded trade history files:")
    trade_files = [f for f in os.listdir(TRADE_HISTORY_DIR) if f.endswith('.csv')]

    if trade_files:
        selected_file = st.selectbox("Select a trade history file to view", trade_files)
        if selected_file:
            try:
                # Load and display the selected trade history file
                trade_history = load_file(os.path.join(TRADE_HISTORY_DIR, selected_file))
                st.write(f"Trade History: {selected_file}")
                st.dataframe(trade_history)
            except Exception as e:
                st.error(f"Error loading trade history: {e}")
    else:
        st.warning("No trade history files uploaded yet.")

    # Button to delete all trade history files
    if st.button("Delete All Trade History Files"):
        try:
            for f in trade_files:
                os.remove(os.path.join(TRADE_HISTORY_DIR, f))
            st.success("All trade history files have been deleted.")
        except Exception as e:
            st.error(f"Error deleting files: {e}")

# Main function with sidebar navigation
def main():
    st.sidebar.title("Navigation")
    option = st.sidebar.radio("Select a page", ["Viewer", "Admin"])

    if option == "Viewer":
        viewer_action = st.sidebar.radio("Choose an action", ["View Scrip Master", "Manage Trade History"])
        
        if viewer_action == "View Scrip Master":
            viewer_page()
        elif viewer_action == "Manage Trade History":
            trade_history_page()
    
    elif option == "Admin":
        if 'authenticated' not in st.session_state:
            st.session_state['authenticated'] = False

        if not st.session_state['authenticated']:
            st.sidebar.write("---")
            if authenticate():
                admin_page()
        else:
            admin_page()

if __name__ == "__main__":
    main()
