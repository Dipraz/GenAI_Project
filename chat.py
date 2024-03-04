from dotenv import load_dotenv
import streamlit as st
import os
import time
from PIL import Image
import google.generativeai as genai
import cv2
import random  # Remove if not needed elsewhere

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
import cv2  # Import OpenCV for image analysis

def calculate_image_quality_score(analysis_result, image):
    # Implement your own logic here based on analysis_result and image metrics
    score = random.randint(1, 5)  # Placeholder for your logic
    return score

def calculate_accessibility_score(analysis_result, image):
    # Implement your own logic here
    score = random.randint(1, 5)  # Placeholder for your logic
    return score

def calculate_visual_hierarchy_score(analysis_result, image):
    # Implement your own logic here
    score = random.randint(1, 5)  # Placeholder for your logic
    return score

def calculate_rating(analysis_result, image_path):  # Update to use image path
    # Convert image to an array for analysis
    image_array = cv2.imread(image_path)
    quality_score = calculate_image_quality_score(analysis_result, image_array)
    accessibility_score = calculate_accessibility_score(analysis_result, image_array)
    hierarchy_score = calculate_visual_hierarchy_score(analysis_result, image_array)

    overall_rating = (quality_score + accessibility_score + hierarchy_score) / 3
    return round(overall_rating, 1)  # Round to one decimal for display

# Enhanced analyze_images function to include scoring
def analyze_images(images, prompt):
    results = []
    progress_bar = st.progress(0)
    progress_step = 100 // len(images)
    for i, image in enumerate(images):
        with st.spinner(f"Analyzing image {i+1}..."):
            # Save temporary image and use as input for model and analysis
            temp_img_path = f"temp_image_{i}.png"
            image.save(temp_img_path)
            response = vision_model.generate_content([prompt, Image.open(temp_img_path)])
            results.append(response.text)
            rating = calculate_rating(response.text, temp_img_path)  # Pass the temporary image path here
            results.append(f"UX Design Rating: {rating}/5")
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
        st.image("robot.jpg", caption="UX design assistant", width=150)

    # Input Area
    user_question = st.text_input("You:", placeholder="Ask me anything about design...",
                                  help="Start a conversation with your AI design assistant",
                                  key="user_input")
    submit_button = st.button("Send")

    if submit_button:
        with st.spinner("AI is thinking..."):
            response_text = get_gemini_response(user_question)
        st.write("AI:", response_text)

# Expander Configuration
expander = st.expander("More options", expanded=True)
with expander:
    st.write("You can explore more features and options here.")

    # --- IMAGE ANALYSIS FEATURES ---
    st.header("Image Analysis")
    col1, col2 = st.columns(2)

    with col1:
        analysis_options = {
            # Define analysis options here
        }
        input_prompt = st.selectbox("Select Analysis Type:", list(analysis_options.keys()))
        upload_files = st.file_uploader("Upload UX Design Images:",
                                        type=["jpg", "jpeg", "png", "webp"],
                                        accept_multiple_files=True)
        if upload_files:
            images = []
            for uploaded_file in upload_files:
                image = Image.open(uploaded_file)
                images.append(image)
            image_container = st.container()
            if len(upload_files) > 1:
                st.write("Image Gallery:")
                cols = st.columns(len(upload_files))
                for idx, uploaded_file in enumerate(upload_files):
                    cols[idx].image(uploaded_file)
            else:
                image_container.image(upload_files, caption="Uploaded Image")

    with col2:
        input_text = st.text_input("Input Prompt:", key="input_prompt")
        analyze_button = st.button("Analyze Designs (Standard)")
        custom_analyze_button = st.button("Analyze Designs (Custom)")

        if analyze_button:
            selected_prompt = analysis_options.get(input_prompt, "")
            if input_text:
                prompt = selected_prompt + " " + input_text
            else:
                prompt = selected_prompt
            responses = analyze_images(images, prompt)
            st.subheader("Analysis Results:")
            for i, response in enumerate(responses, start=1):
                st.write(f"Design {i}:")
                st.write(response)

        if custom_analyze_button:
            if input_text:
                custom_prompt = input_text
                responses = analyze_images(images, custom_prompt)
                st.subheader("Analysis Results:")
                for i, response in enumerate(responses, start=1):
                    st.write(f"Design {i}:")
                    st.write(response)
            else:
                st.warning("Please enter a custom prompt for analysis.")

# Run the Streamlit app
if __name__ == "__main__":
    st.write()
