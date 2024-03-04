from dotenv import load_dotenv
import streamlit as st
import os
import time
from PIL import Image
import google.generativeai as genai
import cv2
import random  # Used only for placeholder logic
import base64

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

# Function to convert image to base64-encoded text
def image_to_base64(image_path):
    with open(image_path, "rb") as image_file:
        return base64.b64encode(image_file.read()).decode('utf-8')

# Placeholder for real logic to convert analysis_result into scores
def calculate_rating(analysis_result):
    score = random.randint(1, 5)  # Replace with actual scoring logic based on vision_model output
    return score

# Function to analyze images without the prompt in the request content
def analyze_images(images):
    results = []
    progress_bar = st.progress(0)
    progress_step = 100 // len(images)
    for i, image in enumerate(images):
        with st.spinner(f"Analyzing image {i+1}..."):
            temp_img_path = f"temp_image_{i}.png"
            image.save(temp_img_path)

            image_base64 = image_to_base64(temp_img_path)
            request_content = {
                'parts': [{
                    'mime_type': 'image/png',
                    'data': image_base64
                }]
            }

            response = vision_model.generate_content(request_content)
            
            # Placeholder for actual response parsing and score calculation
            analysis = {}  # This should be replaced with actual analysis data extraction logic
            score = calculate_rating(analysis)  # Convert the response into a UX score

            results.append({'analysis': 'Placeholder analysis', 'score': score})
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

# Main Container
main_container = st.container()
with main_container:
    header_col1, header_col2 = st.columns([3, 1])
    with header_col1:
        st.title(":art: UX Design Assistant")
    with header_col2:
        st.image("robot.jpg", caption="UX Design Assistant", width=150)  # Placeholder image

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
    upload_files = st.file_uploader("Upload UX Design Images:", type=["jpg", "jpeg", "png"], accept_multiple_files=True
# Continued from the previous code snippet

# Define Scoring Functions
def calculate_image_quality_score(analysis_result, image_path):
    # Placeholder logic: Calculate image quality score based on analysis result
    # Replace this with actual logic based on the analysis_result
    score = random.randint(1, 5)  # Placeholder score
    return score

def calculate_accessibility_score(analysis_result, image_path):
    # Placeholder logic: Calculate accessibility score based on analysis result
    # Replace this with actual logic based on the analysis_result
    score = random.randint(1, 5)  # Placeholder score
    return score

def calculate_visual_hierarchy_score(analysis_result, image_path):
    # Placeholder logic: Calculate visual hierarchy score based on analysis result
    # Replace this with actual logic based on the analysis_result
    score = random.randint(1, 5)  # Placeholder score
    return score

# Enhanced analyze_images function to include scoring
def analyze_images(images):
    results = []
    progress_bar = st.progress(0)
    progress_step = 100 // len(images)
    for i, image in enumerate(images):
        with st.spinner(f"Analyzing image {i+1}..."):
            temp_img_path = f"temp_image_{i}.png"
            image.save(temp_img_path)

            # Placeholder logic: Perform analysis with the vision model
            analysis_result = {}  # Placeholder analysis result

            # Calculate scores based on analysis result
            quality_score = calculate_image_quality_score(analysis_result, temp_img_path)
            accessibility_score = calculate_accessibility_score(analysis_result, temp_img_path)
            hierarchy_score = calculate_visual_hierarchy_score(analysis_result, temp_img_path)

            overall_rating = (quality_score + accessibility_score + hierarchy_score) / 3

            results.append({
                'image': image,
                'quality_score': quality_score,
                'accessibility_score': accessibility_score,
                'hierarchy_score': hierarchy_score,
                'overall_rating': overall_rating
            })

            progress_bar.progress(progress_step * (i + 1))
            os.remove(temp_img_path)  # Clean up temporary file

    return results

# Main function to run the app
def main():
    # App Configuration
    st.set_page_config(
        page_title="UX Design Assistant",
        page_icon=":art:",
        layout="wide"
    )

    # Main Container
    main_container = st.container()
    with main_container:
        header_col1, header_col2 = st.columns([3, 1])
        with header_col1:
            st.title(":art: UX Design Assistant")
        with header_col2:
            st.image("robot.jpg", caption="UX Design Assistant", width=150)  # Placeholder image

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
        analyze_button = st.button("Analyze Designs")
        if analyze_button and images:
            analysis_results = analyze_images(images)
            st.subheader("Analysis Results:")
            for result in analysis_results:
                st.image(result['image'], caption="Uploaded Image", use_column_width=True)
                st.write("Quality Score:", result['quality_score'])
                st.write("Accessibility Score:", result['accessibility_score'])
                st.write("Visual Hierarchy Score:", result['hierarchy_score'])
                st.write("Overall Rating:", result['overall_rating'])

if __name__ == "__main__":
    main()
