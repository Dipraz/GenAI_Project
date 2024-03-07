import google.generativeai as genai
from dotenv import load_dotenv
import streamlit as st
import os
import time
from PIL import Image, ImageStat
import numpy as np
import cv2
import random
import re
import base64
from io import BytesIO

# Load environment variables from .env file
load_dotenv()

# Define and initialize the model variable
model = genai.GenerativeModel('gemini-pro')
vision_model = genai.GenerativeModel('gemini-pro-vision')

# Function to load OpenAI model and get responses
def get_gemini_response(question):
    full_input = f"{UX_DESIGN_PROMPT}\n{question}"
    with st.spinner("AI is typing..."):
        time.sleep(3)  # Simulate model response time
        response = model.generate_content(full_input)
    return response.text

# Define Scoring Functions
def calculate_image_quality_score(analysis_result, image_path):
    # Implement your image quality scoring logic here
    pass

def calculate_accessibility_score(analysis_result, image_path):
    # Implement your accessibility scoring logic here
    pass

def calculate_visual_hierarchy_score(analysis_result, image_path):
    # Implement your visual hierarchy scoring logic here
    pass

def calculate_rating(analysis_result, image_path):
    # Combine quality, accessibility, and hierarchy scores to calculate overall rating
    pass

# Image Conversion Helper
def image_to_base64(image):
    buffered = BytesIO()
    image.save(buffered, format="JPEG") 
    img_str = base64.b64encode(buffered.getvalue()).decode()
    return img_str

# Enhanced analyze_images function to include scoring
def analyze_images(images, prompt):
    results = []
    progress_bar = st.progress(0)
    progress_step = 100 // len(images)

    for i, image in enumerate(images):
        with st.spinner(f"Analyzing image {i+1}..."):
            temp_img_path = f"temp_image_{i}.png"
            image.save(temp_img_path)
            
            # Convert image to base64 for model input
            image_base64 = image_to_base64(image) 

            response = vision_model.generate_content(image_base64)  # Remove the prompt from here
            rating = calculate_rating(response.text, temp_img_path)
            results.append(f"{response.text}\nUX Design Rating: {rating}/5")
            progress_bar.progress(progress_step * (i + 1))
            os.remove(temp_img_path)
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
.appview-container {
    background-color: #F8F8F8; 
}
.stButton > button {
    background-color: #4CAF50; 
    color: white;
}
.stButton > button:hover {
    background-color: #3e8e41; 
}
.st-ba { 
    background-color: #f0f2f6;
}
</style>
""", unsafe_allow_html=True)

# Main Container
main_container = st.container()

with main_container:
    st.title(":art: UX Design Assistant")
    user_question = st.text_input("You:", placeholder="Ask me anything about UX design...",
                                  help="Start a conversation with your AI design assistant",
                                  key="user_input")
    submit_button = st.button("Send")

    if submit_button:
        with st.spinner("AI is thinking..."):
            response_text = get_gemini_response(user_question)
        st.write("AI:", response_text)

# Analysis Options
analysis_options = { 
    "Heuristic Evaluation": "Evaluate this design based on Nielsen's usability heuristics. Where does it succeed, and where might there be issues?",
    "Accessibility Analysis": "Are there any elements in this design that might create accessibility barriers? Suggest improvements for inclusivity.",
    "Visual Hierarchy Review": "Determine the visual hierarchy of this design. Does it effectively guide the user's attention to the most important aspects?",
    "Comparative Analysis": "Compare these two design options. Which one is more successful based on clarity, intuitiveness, and why?",
    "Design Ideation": "Brainstorm ideas to improve the visual appeal and overall user experience of this design."
}

# Define Headline Analysis Options
headline_analysis_options = {
    "Clarity and Conciseness": "Does the headline clearly and concisely convey the main point of the blog? Score (1-5): ",
    "Relevance and Accuracy": "How accurately does the headline reflect the content of the blog? Score (1-5): ",
    "Use of Keywords": "Are relevant keywords included in the headline for SEO purposes? Do these keywords fit naturally? Score (1-5): ",
    "Emotional Appeal": "Does the headline evoke an emotional response or curiosity? Score (1-5): ",
    "Uniqueness": "How unique or original is the headline? Score (1-5): ",
    "Urgency and Curiosity": "Does the headline create a sense of urgency or curiosity? Score (1-5): ",
    "Benefit Driven": "Does the headline convey a clear benefit or value to the reader? Score (1-5): ",
    "Target Audience": "Is the headline tailored to resonate with the specific target audience? Score (1-5): ",
    "Length and Format": "Is the headline of an appropriate length (6-12 words)? Score (1-5): ",
    "Use of Numbers and Lists": "Does the headline use numbers or indicate a list effectively, if applicable? Score (1-5):",
    "Brand Consistency": "Does the headline align with the overall brand tone and style? Score (1-5):",
    "Use of Power Words": "Does the headline include power words or action verbs? Score (1-5):"
}

# Analyze headline function (with error handling)
def analyze_headline(headline_option, input_text):
    try:
        if input_text:
            headline_response = vision_model.generate_content(
                [headline_analysis_options[headline_option]]
            )
            return f"{headline_option}: {headline_response.text}"
        else:
            return "Please enter a custom prompt for headline analysis."            
    except google.api_core.exceptions.InvalidArgument as e:
        return f"Error: Invalid input format for headline analysis. Details: {e}"

# Image Analysis Features
st.header("Image Analysis")
col1, col2 = st.columns(2)

with col1:
    analysis_choice = st.selectbox("Select Analysis Type:", list(analysis_options.keys()) + ["Headline Analysis"])
    upload_files = st.file_uploader("Upload UX Design Images:", type=["jpg", "jpeg", "png", "webp"], accept_multiple_files=True)
    images = [] 
    if upload_files:
        # Display uploaded images
        for uploaded_file in upload_files:
            image = Image.open(uploaded_file)
            images.append(image)
            st.image(image, caption="Uploaded Image", use_column_width=True)

    if analysis_choice == "Headline Analysis":
        headline_option = st.selectbox("Select Headline Analysis Criterion:", list(headline_analysis_options.keys()))

with col2:
    input_text = st.text_area("Input Prompt:", height=150, help="Enter a custom analysis prompt or additional information.")
    analyze_button = st.button("Analyze Designs (Standard)")
    custom_analyze_button = st.button("Analyze Designs (Custom)")

    if analyze_button:
        if analysis_choice != "Headline Analysis":
            if images:  # Ensure there are images to analyze
                selected_prompt = analysis_options.get(analysis_choice, "")
                prompt = selected_prompt + " " + input_text if input_text else selected_prompt
                responses = analyze_images(images, prompt)
                st.subheader("Analysis Results:")
                for response in responses:
                    st.write(response)
        else:
            if images:  # Ensure there are images to analyze for headline analysis
                headline_response = analyze_headline(headline_option, input_text)
                st.subheader("Headline Analysis Results:")
                st.write(headline_response)  # Display headline analysis result
            else:
                st.warning("Please upload images for headline analysis.")

    if custom_analyze_button:
        if analysis_choice != "Headline Analysis":
            if images and input_text:  # Ensure there are images and a custom prompt
                custom_prompt = input_text
                responses = analyze_images(images, custom_prompt)
                st.subheader("Analysis Results:")
                for response in responses:
                    st.write(response)
            else:
                st.warning("Please upload images and enter a custom prompt for analysis.")
        else:
            if input_text:  # Ensure there's a custom prompt for headline analysis
                headline_response = analyze_headline(headline_option, input_text)
                st.subheader("Custom Headline Analysis Results:")
                st.write(headline_response)  # Display custom headline analysis result
            else:
                st.warning("Please enter a custom prompt for headline analysis.")

# Run the Streamlit app
if __name__ == "__main__":
    st.write("Streamlit app is running...")
