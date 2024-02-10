from dotenv import load_dotenv

load_dotenv()  # Take environment variables from .env.

import streamlit as st
import os
import textwrap
import time

import google.generativeai as genai

from IPython.display import display
from IPython.display import Markdown

# Initialize Streamlit app and set page configuration
st.set_page_config(
    page_title="UX Design Assistant",
    page_icon=":art:",
    layout="wide"  # Use wide layout for better display
)

# Function to load OpenAI model and get responses
def get_gemini_response(question):
    model = genai.GenerativeModel('gemini-pro')

    # Combine the prompt and question into a single string
    full_input = f"{UX_DESIGN_PROMPT}\n{question}"

    # Simulate model response time with loading indicator
    with st.spinner("AI is typing..."):
        time.sleep(3)  # Simulate model response time
        response = model.generate_content(full_input)  # Pass the combined input

    return response.text

# Add a header with title and icon
st.title(":robot.jpg: UX Design Assistant")

# Define UX design prompt
UX_DESIGN_PROMPT = f"""You are a friendly, kind, helpful, and highly knowledgeable world-best UX design assistant, trained on a vast dataset of UX design articles, resources, and best practices to tackle any kind of design challenge. You can ask relevant questions for better user understanding and responses, provide summaries of articles, be highly expert in generating design ideas, create prototypes, and offer feedback on UX designs. You can generate different creative text formats of text content, like codes, poems, stories, scripts, musical pieces, emails, letters, etc. You will try your best to fulfill all your and user requirements and expectations. You do not respond as 'User' or pretend to be 'User'. You only respond once as 'Assistant'."""

# Add text input for user to ask a question
input_question = st.text_input("You: ")

# Add button to submit question
submit_button = st.button("Send")

# If the submit button is clicked
if submit_button:
    # Get response from Gemini model
    response_text = get_gemini_response(input_question)
    
    # Display response
    st.write("AI:", response_text)

# Add dynamic loading button for interactive experience
with st.expander("More options"):
    st.write("You can explore more features and options here.")
