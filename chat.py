from dotenv import load_dotenv
import streamlit as st
import os
import time
from PIL import Image
import google.generativeai as genai

load_dotenv()  # Take environment variables from .env.

# Initialize Streamlit app and set page configuration
st.set_page_config(
    page_title="UX Design Assistant",
    page_icon=":art:",
    layout="wide"  # Use wide layout for better display
)

# Function to load OpenAI model and get responses
def get_gemini_response(question):
    model = genai.GenerativeModel('gemini-pro')
    full_input = f"{UX_DESIGN_PROMPT}\n{question}"
    with st.spinner("AI is typing..."):
        time.sleep(3)  # Simulate model response time
        response = model.generate_content(full_input)
    return response.text

# Function to perform image analysis
def analyze_image(image, prompt):
    model = genai.GenerativeModel('gemini-pro-vision')
    response = model.generate_content([prompt, image])
    return response.text

# Define UX design prompt
UX_DESIGN_PROMPT = """
You are a friendly, kind, helpful, and highly knowledgeable world-best UX design assistant, trained on a vast dataset of UX design articles, resources, and best practices to tackle any kind of design challenge. You can ask relevant questions for better user understanding and responses, provide summaries of articles, be highly expert in generating design ideas, create prototypes, and offer feedback on UX designs. You can generate different creative text formats of text content, like codes, poems, stories, scripts, musical pieces, emails, letters, etc. You will try your best to fulfill all your and user requirements and expectations. You do not respond as 'User' or pretend to be 'User'. You only respond once as 'Assistant'.
"""

# Add a header with title and icon
st.title(":art: UX Design Assistant")
st.image("robot.jpg", caption="UX design assistant", width=600)

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
    
    # Image Analysis Section
    st.header("Image Analysis")
    analysis_options = {
        "Heuristic Evaluation": "Analyze the image against established UX heuristics (e.g., Nielsen's 10 Usability Heuristics). Highlight potential areas for improvement.Example Prompt: Evaluate this design based on Nielsen's usability heuristics. Where does it succeed, and where might there be issues? ",
        "Accessibility Analysis": "Assess the image for accessibility compliance (color contrast, alt-text, readability). Provide recommendations.Example Prompt:Are there any elements in this design that might create accessibility barriers? Suggest improvements for inclusivity. ",
        "Visual Hierarchy Review": " Analyze the image's visual composition. Focus on the importance of design elements, guiding the user's eye.Example Prompt: Determine the visual hierarchy of this design. Does it effectively guide the user's attention to the most important aspects? ",
        "Comparative Analysis": " Let the user upload two (or more) design variations. Analyze strengths/weaknesses, suggesting the superior version.Example Prompt: Compare these two design options. Which one is more successful based on [state a guiding principle, e.g., clarity, intuitiveness], and why?",
        "Design Ideation": "Use the image as a starting point. Suggest alternative layouts, color palettes, typography, or interactions that could enhance the design.Example Prompt: Brainstorm ideas to improve the visual appeal and overall user experience of this design."
    }

    input_prompt = st.selectbox("Select Analysis Type:", list(analysis_options.keys()))
    upload_file = st.file_uploader("Upload UX_Design Image:", type=["jpg", "jpeg", "png"])

    if upload_file:
        image = Image.open(upload_file)
        st.image(image, caption="Uploaded image", use_column_width=True)
        submit = st.button("Analyze Design")

        if submit:
            selected_prompt = analysis_options[input_prompt]
            # Combine the selected prompt with a custom prompt if provided
            if input:
                prompt = selected_prompt + " " + input
            else:
                prompt = selected_prompt + " " + input
            response = analyze_image(image, prompt)
            st.subheader("Analysis Result:")
            st.write(response)
    else:
        st.write("Please upload an image to analyze")
