from openai import OpenAI
import os
import json
import traceback
import pandas as pd
import streamlit as st
from dotenv import load_dotenv
from src.mcqgenerator.utils import read_file, get_table_data
from src.mcqgenerator.MCQGenerator import generate_evaluate_chain
from src.mcqgenerator.logger import logging

# Load environment variables
load_dotenv()

# Instantiate the OpenAI client
client = OpenAI(api_key=os.getenv("OPENAI_API_KEY"))

# Load the JSON response file
try:
    with open('Response.json', 'r') as file:
        RESPONSE_JSON = json.load(file)
except json.JSONDecodeError:
    st.error("Error: The JSON file is empty or contains invalid data.")

# Create a title for the app
st.title("MCQs Creator Application with LangChain 🦜⛓️")

# Create a form using st.form with a unique key to avoid duplicates
with st.form("mcq_form"):
    # File Upload
    uploaded_file = st.file_uploader("Upload a PDF or txt file")

    # Input Fields
    mcq_count = st.number_input("No. of MCQs", min_value=3, max_value=50)

    # Subject
    subject = st.text_input("Insert Subject", max_chars=20)

    # Quiz Tone
    tone = st.text_input("Complexity Level Of Questions", max_chars=20, placeholder="Simple")

    # Add Submit Button
    button = st.form_submit_button("Create MCQs")

    # Check if the button is clicked and all fields have input
    if button and uploaded_file is not None and mcq_count and subject and tone:
        with st.spinner("Loading..."):
            try:
                # Read the file content
                text = read_file(uploaded_file)

                # OpenAI API call without token tracking for now
                try:
                    # New API method for chat completions
                    completion = client.chat.completions.create(
                        model="gpt-3.5-turbo",
                        messages=[{
                            "role": "system",
                            "content": "You are an expert MCQ maker."
                        }, {
                            "role": "user",
                            "content": f"Generate {mcq_count} MCQs for {subject}. Text: {text}"
                        }],
                        max_tokens=1024,
                        temperature=0.3
                    )

                    # Properly access the response
                    st.write(completion.choices[0].message.content)

                except Exception as e:
                    st.error(f"OpenAI API Error: {e}")
                    completion = None  # Ensure response is None on failure

            except Exception as e:
                traceback.print_exception(type(e), e, e.__traceback__)
                st.error("An error occurred while generating MCQs.")
                completion = None  # Ensure response is None on failure

            # Validate the completion response without checking for dictionary type
            if completion:
                # Here, use the completion object directly or convert it to a dict if needed
                if isinstance(completion, dict):
                    quiz = completion.get("quiz", None)

                    if quiz is not None:
                        table_data = get_table_data(quiz)

                        # If quiz data is available, display it in a table
                        if table_data is not None:
                            df = pd.DataFrame(table_data)
                            df.index = df.index + 1
                            st.table(df)

                            # Display the review in a text area
                            st.text_area(label="Review", value=completion.get("review", ""))

                        else:
                            st.error("Error in the table data.")
                    else:
                        st.error("Quiz data is missing from the response.")
            else:
                st.error("No valid response received from OpenAI.")
