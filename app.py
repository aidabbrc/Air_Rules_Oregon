import streamlit as st
import openai
from query_data import main as query_data_main

# Set the OpenAI API key from Streamlit secrets
openai.api_key = st.secrets["OPENAI_API_KEY"]

# Function to test OpenAI API connection
def test_openai_api():
    try:
        response = openai.Completion.create(
            model="text-davinci-003",
            prompt="This is a test prompt.",
            max_tokens=5
        )
        return f"API test successful: {response.choices[0].text.strip()}"
    except Exception as e:
        return f"API test failed: {e}"

# Run API test and display the result
api_test_result = test_openai_api()
st.write(api_test_result)  # Display the test result at the top of the app

# Main app interface
st.title("Air Quality Rule Query App")
st.write("Ask questions related to Oregon Administrative Rules for Air Quality.")

query_text = st.text_input("Enter your query:")

if query_text:
    with st.spinner("Querying database..."):
        response = query_data_main(query_text)
    st.write(response)
