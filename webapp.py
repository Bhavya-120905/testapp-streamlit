import streamlit as st

# Add a title to your web app
st.title("Welcome to My First Streamlit App")

# Add a text input
name = st.text_input("Enter your name:")

# Display the input when button is pressed
if st.button("Submit"):
    st.write(f"Hello, {name}!")
