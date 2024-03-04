from dotenv import load_dotenv
import streamlit as st
import os
import time
from PIL import Image
import google.generativeai as genai
import cv2
import random  # Used only for placeholder logic

# Load environment variables from .env file
load_dotenv()

# Define and initialize the model variables
model = genai.GenerativeModel('gemini-pro')
vision_model = genai.GenerativeModel('gemini-pro-vision')

# Function to load OpenAI model and get responses
def get_gemini_response(question):
    full_input = f"{UX_DESIGN_PROMPT}\n{question}"
    with st.spinner("AI is typing..."):
        time.sleep(3)  # Simulate model response time
        response = model.generate_content(full_input)
    return response.text

# Define Scoring Functions based on the hypothetical outputs from vision_model
def calculate_rating(analysis_result):  # Placeholder for real logic
    # Example: Convert analysis_result into scores
    score = random.randint(1, 5)  # Replace with actual scoring logic based on vision_model output
    return score

# Enhanced analyze_images function to include scoring based on vision_model
def analyze_images(images, prompt):
    results = []
    progress_bar = st.progress(0)
    progress_step = 100 // len(images)
    for i, image in enumerate(images):
        with st.spinner(f"Analyzing image {i+1}..."):
            temp_img_path = f"temp_image_{i}.png"
            image.save(temp_img_path)

            # Assuming the vision model requires a dictionary with image path and prompt
            response = vision_model.generate_content({'image_path': temp_img_path, 'prompt': prompt})
            # Here you should parse the response from your vision_model
            # This example assumes the response includes some form of analysis
            analysis = response.get('analysis', {})  # Placeholder for actual response handling

            # Convert analysis into scores (this part is highly dependent on your model's output)
            score = calculate_rating(analysis)  # Convert the response into a UX score

            results.append({'analysis': analysis, 'score': score})
            progress_bar.progress(progress_step * (i + 1))
            os.remove(temp_img_path)  # Clean up temporary file

    return results

# Define UX design prompt
UX_DESIGN_PROMPT = """
You are a friendly, kind, helpful, and highly knowledgeable world-best UX design assistant, trained on a vast dataset of UX design articles, resources, and best practices to tackle any kind of design challenge. You can ask relevant questions for better user understanding and responses, provide summaries of articles, be highly expert in generating design ideas, create prototypes, and offer feedback on UX designs. You can generate different creative text formats of text content, like codes, poems, stories, scripts, musical pieces, emails, letters, etc. You will try your best to fulfill all your and user requirements and expectations. You do not respond as 'User' or pretend to be 'User'. You only respond once as 'Assistant'.
"""

# App Configuration
st.set_page_config(
    page_title="UX Design Assistant",
    page_icon=":art:",
    layout="wide"
)

# Theme customization
st.markdown("""
<style>
/* Main background */
.appview-container {
    background-color: #F8F8F8; 
}
/* Customize buttons */
.stButton > button {
    background-color: #4CAF50; /* Green */
    color: white;
}
.stButton > button:hover {
    background-color: #3e8e41; 
}
/* Section headers */
.st-ba { 
    background-color: #f0f2f6;
}
</style>
""", unsafe_allow_html=True)

# Main Container
main_container = st.container()

with main_container:
    header_col1, header_col2 = st.columns([3, 1])  # Adjusted header column ratio

    with header_col1:
        st.title(":art: UX Design Assistant")
    with header_col2:
        st.image("robot.jpg", caption="UX Design Assistant", width=150)  # Replace 'robot.jpg' with your image file

    user_question = st.text_input("You:", placeholder="Ask me anything about UX design...",
                                  help="Start a conversation with your AI design assistant",
                                  key="user_input")
    submit_button = st.button("Send")

    if submit_button:
        response_text = get_gemini_response(user_question)
        st.write("AI:", response_text)

# Image Analysis Features
st.header("Image Analysis")
col1, col2 = st.columns(2)

with col1:
    analysis_options = {
        "Heuristic Evaluation": "Analyze the image against established UX heuristics.",
        "Accessibility Analysis": "Assess the image for accessibility compliance.",
        "Visual Hierarchy Review": "Analyze the image's visual composition.",
        "Comparative Analysis": "Compare two or more design variations.",
        "Design Ideation": "Suggest alternative designs."
    }
    input_prompt = st.selectbox("Select Analysis Type:", list(analysis_options.keys()))
    upload_files = st.file_uploader("Upload UX Design Images:", type=["jpg", "jpeg", "png"], accept_multiple_files=True)
    images = [Image.open(uploaded_file) for uploaded_file in upload_files] if upload_files else []

with col2:
    input_text = st.text_area("Input Prompt:", help="Enter a custom analysis prompt or additional information.")
    analyze_button = st.button("Analyze Designs")

    if analyze_button and images:
        selected_prompt = analysis_options[input_prompt]
        prompt = f"{selected_prompt} {input_text}" if input_text else selected_prompt
        analysis_results = analyze_images(images, prompt)
        st.subheader("Analysis Results:")
        for result in analysis_results:
            st.markdown(f"**Analysis:** {result['analysis']}")
            st.markdown(f"**Score:** {result['score']}/5")

if __name__ == "__main__":
    st.write("Streamlit app is running...")
