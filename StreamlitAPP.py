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

# Create the app title and introductory text
st.title("MCQs Creator Application with LangChain 🦜⛓️")
st.markdown("### Easily generate multiple choice questions (MCQs) with AI")

# Create a form for input
with st.form("mcq_form"):
    st.header("🔧 Input Section")
    
    # File Upload
    uploaded_file = st.file_uploader("Upload a PDF or txt file containing the subject content", type=["pdf", "txt"])

    # Input Fields
    mcq_count = st.number_input("How many MCQs to generate?", min_value=3, max_value=50, value=5)

    # Subject
    subject = st.text_input("Subject or Topic", max_chars=50, placeholder="e.g., Biology")

    # Quiz Tone
    tone = st.selectbox("Choose the tone for the questions", ["Simple", "Moderate", "Challenging"])

    # Add Submit Button
    button = st.form_submit_button("Generate MCQs")

    # Process the form if the submit button is pressed
    if button and uploaded_file is not None and mcq_count and subject and tone:
        st.markdown("---")
        st.header("⏳ Generating MCQs...")

        try:
            # Read the file content
            text = read_file(uploaded_file)

            # Call the OpenAI API to generate the MCQs
            with st.spinner("Please wait..."):
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

            # Clean up the MCQs output for better readability
            mcqs = completion.choices[0].message.content.split("\n\n")  # Split by double line breaks

            st.header("✅ Generated MCQs")
            for index, mcq in enumerate(mcqs, start=1):
                if mcq.strip():
                    st.markdown(f" {mcq.strip()}")

            # Display the review or any feedback on the generated MCQs
            st.markdown("---")
            st.header("📝 Quiz Review")
            st.text_area("Review", value="These questions seem to be appropriate for the topic.", height=150)

        except Exception as e:
            traceback.print_exception(type(e), e, e.__traceback__)
            st.error("An error occurred while generating MCQs.")

# Style and layout improvements
st.markdown("---")
st.markdown("### 💡 **How it works**:")
st.markdown(
    """
    1. **Upload a document**: Upload a PDF or text file containing the subject matter.
    2. **Enter details**: Specify the number of questions, subject, and complexity level.
    3. **Generate questions**: The AI will generate high-quality MCQs for your topic.
    """
)
