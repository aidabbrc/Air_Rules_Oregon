import streamlit as st
from query_data import main as query_data_main

st.title("Air Quality Rule Query App")
st.write("Ask questions related to Oregon Administrative Rules for Air Quality.")

query_text = st.text_input("Enter your query:")

if query_text:
    with st.spinner("Querying database..."):
        response = query_data_main(query_text)
    st.write(response)
