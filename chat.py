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

# Define Scoring Functions
def calculate_image_quality_score(analysis_result, image_path):
    image = cv2.imread(image_path, cv2.IMREAD_GRAYSCALE)
    laplacian_var = cv2.Laplacian(image, cv2.CV_64F).var()
    if laplacian_var > 300:
        return 5
    elif laplacian_var > 100:
        return 3
    else:
        return 1

def calculate_accessibility_score(analysis_result, image_path):
    image = Image.open(image_path)
    stat = ImageStat.Stat(image)
    brightness = stat.mean[0]
    if brightness > 192:
        return 5
    elif brightness > 128:
        return 3
    else:
        return 1

def calculate_visual_hierarchy_score(analysis_result, image_path):
    return random.randint(1, 5)

def calculate_rating(analysis_result, image_path):
    quality_score = calculate_image_quality_score(analysis_result, image_path)
    accessibility_score = calculate_accessibility_score(analysis_result, image_path)
    hierarchy_score = calculate_visual_hierarchy_score(analysis_result, image_path)

    overall_rating = (quality_score + accessibility_score + hierarchy_score) / 3
    return round(overall_rating, 1)

# General analyze_images function
def analyze_images(images, prompt):
    results = []
    progress_bar = st.progress(0)
    progress_step = 100 // len(images)
    for i, image in enumerate(images):
        with st.spinner(f"Analyzing image {i+1}..."):
            temp_img_path = f"temp_image_{i}.png"
            image.save(temp_img_path)
            response = vision_model.generate_content([prompt, Image.open(temp_img_path)])
            results.append(response.text)
            rating = calculate_rating(response.text, temp_img_path)
            results.append(f"UX Design Rating: {rating}/5")
            progress_bar.progress(progress_step * (i + 1))
            os.remove(temp_img_path)
    return results

# Specific function for Image Headline Analysis
def analyze_headline_images(images, criteria):
    results = []
    progress_bar = st.progress(0)
    progress_step = 100 // len(images)
    for i, image in enumerate(images):
        with st.spinner(f"Analyzing image headline {i+1}..."):
            temp_img_path = f"temp_image_{i}.png"
            image.save(temp_img_path)
            prompts = [image_headline_analysis_options[crit] for crit in criteria]
            combined_prompt = " ".join(prompts)
            response = vision_model.generate_content([combined_prompt, Image.open(temp_img_path)])
            results.append(response.text)
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
    header_col1, header_col2 = st.columns([3, 1])

    with header_col1:
        st.title(":art: UX Design Assistant")
    with header_col2:
        st.image("robot.jpg", caption="UX Design Assistant", width=150)

    user_question = st.text_input("You:", placeholder="Ask me anything about UX design...",
                                  help="Start a conversation with your AI design assistant",
                                  key="user_input")
    submit_button = st.button("Send")

    if submit_button:
        with st.spinner("AI is thinking..."):
            response_text = get_gemini_response(user_question)
        st.write("AI:", response_text)

# Analysis Options and Headline Analysis Options
analysis_options = { 
    "Heuristic Evaluation": "Evaluate this design based on Nielsen's usability heuristics. Where does it succeed, and where might there be issues? providing a Score (1-5): and Explanation based on score:",
    "Accessibility Analysis": "Are there any elements in this design that might create accessibility barriers? Suggest improvements for inclusivity.providing a Score (1-5): and Explanation based on score:",
    "Visual Hierarchy Review": "Determine the visual hierarchy of this design. Does it effectively guide the user's attention to the most important aspects?providing a Score (1-5): and Explanation based on score:",
    "Comparative Analysis": "Compare these two design options. Which one is more successful based on clarity, intuitiveness, and why?providing a Score (1-5): and Explanation based on score:",
    "Design Ideation": "Brainstorm ideas to improve the visual appeal and overall user experience of this design. providing a Score (1-5): and Explanation based on score:",
    "Image Headline Analysis": """Image Headline Analysis
Headline for Evaluation: [Insert Headline Here]

Analyze the following aspects, providing a score and explanation for each point:

Clarity and Conciseness:
Is the headline immediately understandable? Can the core idea be grasped at a glance?
Does it avoid ambiguity and complex terminology?
Score (1-5):
Explanation:
Relevance and Accuracy:
Does the headline accurately reflect the dominant elements in the image (objects, actions, setting)?
Does it capture the overall theme or message conveyed by the visual?
Score (1-5):
Explanation:
Emotional Appeal:
Does the headline evoke an emotional response (excitement, curiosity, humor, surprise, etc.)?
Does it use sensory language or vivid descriptions?
Score (1-5):
Explanation:
Target Audience:
Is the language and tone appropriate for the intended audience (consider demographics, interests, etc.)?
Would the headline accurately draw the attention of the target viewer?
Score (1-5):
Explanation:
Benefit Driven:
Does the headline highlight a benefit or value for the reader/viewer?
Does it pique interest by promising insight or entertainment?
Score (1-5):
Explanation:
Keyword Optimization:
Are relevant keywords included for SEO (without keyword stuffing)?
Could additional keywords improve discoverability for the target audience?
Score (1-5):
Explanation:
Uniqueness:
Does the headline stand out as original or attention-grabbing?
Does it avoid cliches or overly generic phrasing?
Score (1-5):
Explanation:
Urgency and Curiosity:
Does the headline inspire a desire to click or learn more?
Does it utilize questions, hints at a story, or create a sense of intrigue?
Score (1-5):
Explanation:
Length and Format:
Is the length appropriate for the platform or medium?
Does the format enhance readability (capitalization, punctuation, etc.)?
Score (1-5):
Explanation:
Brand Consistency:
Does the headline align with the brand's voice and style (if applicable)?
Is it consistent with the branding in the image itself?
Score (1-5):
Explanation:
Power Words:
Are impactful verbs or adjectives used to create a stronger impression?
Score (1-5):
Explanation:
Total Score: [sum of scores/total applicable scores]

Overall Assessment:

Summarize the headline's major strengths and areas for improvement.
Provide actionable recommendations for greater impact and effectiveness.
Specific Recommendations:

Offer 2-3 alternative headline suggestions that address weaknesses and aim to increase engagement.
Key Improvements:

Visual Focus: Emphasizes analysis of the image itself, not just textual headlines
Actionable Feedback: Provides alternative headline suggestions.
SEO Awareness: Maintains focus on keywords for optimization.
**Note:** If a point is not applicable to the image, the model should respond with "Score (N/A): Not applicable for this headline" and still provide a short explanation as to why it's not applicable."""
}

image_headline_analysis_options = {
    "Clarity and Conciseness": "Does the headline clearly and concisely convey the main point of the blog? Score (1-5) ",
    "Relevance and Accuracy": "How accurately does the headline reflect the content of the blog? Score (1-5)",
    "Use of Keywords": "Are relevant keywords included in the headline for SEO purposes? Do these keywords fit naturally? Score (1-5)",
    "Emotional Appeal": "Does the headline evoke an emotional response or curiosity? Score (1-5)",
    "Uniqueness": "How unique or original is the headline? Score (1-5)",
    "Urgency and Curiosity": "Does the headline create a sense of urgency or curiosity? Score (1-5)",
    "Benefit Driven": "Does the headline convey a clear benefit or value to the reader? Score (1-5)",
    "Target Audience": "Is the headline tailored to resonate with the specific target audience? Score (1-5)",
    "Length and Format": "Is the headline of an appropriate length (6-12 words)? Score (1-5)",
    "Use of Numbers and Lists": "Does the headline use numbers or indicate a list effectively, if applicable? Score (1-5)",
    "Brand Consistency": "Does the headline align with the overall brand tone and style? Score (1-5)",
    "Use of Power Words": "Does the headline include power words or action verbs? Score (1-5)"
}

# Image Analysis Features
st.header("Image Analysis")
analysis_choice = st.selectbox("Select Analysis Type:", list(analysis_options.keys()))
col1, col2 = st.columns(2)

with col1:
    upload_files = st.file_uploader("Upload UX Design Images:", type=["jpg", "jpeg", "png", "webp"], accept_multiple_files=True)
    images = []
    if upload_files:
        for uploaded_file in upload_files:
            image = Image.open(uploaded_file)
            images.append(image)
        if len(upload_files) > 1:
            st.write("Image Gallery:")
            cols = st.columns(len(upload_files))
            for idx, uploaded_file in enumerate(upload_files):
                cols[idx].image(uploaded_file, width=150)
        else:
            st.image(upload_files[0], caption="Uploaded Image", width=300)

with col2:
    if analysis_choice == "Image Headline Analysis":
        image_headline_options = st.multiselect("Select Criteria:", list(image_headline_analysis_options.keys()))
        input_text = st.text_area("Input Prompt:", height=150, help="Enter additional information.")
        analyze_headline_button = st.button("Analyze Headline")
        default_analyze_button = st.button("Default Headline Analysis")
        if analyze_headline_button and images and image_headline_options:
            selected_prompt = [image_headline_analysis_options[crit] for crit in image_headline_options]
            prompt = " ".join(selected_prompt) + " " + input_text if input_text else " ".join(selected_prompt)
            responses = analyze_headline_images(images, image_headline_options)
            st.subheader("Analysis Results:")
            for response in responses:
                st.write(response)
        elif default_analyze_button and images:
            prompt = "Analyze this image and its accompanying headline. Evaluate the following aspects of the headline, providing a score (1-5) for each:* **Clarity and Conciseness:** Is the headline easy to understand and get the main point at a glance?* **Relevance and Accuracy:** Does the headline accurately reflect the content or message conveyed by the image?* **Emotional Appeal:** Does the headline evoke any emotion or curiosity? * **Target Audience:**  Does the language and tone of the headline seem appropriate for the intended audience (consider demographics, interests, etc., if you have that information)?* **Benefit-Driven:** Does the headline clearly highlight a benefit or value proposition for the reader?Provide a brief explanation for each score and suggest any specific changes to make the headline stronger.**Total Score:** [sum of scores/total applicable scores]"
            responses = analyze_images(images, prompt)
            st.subheader("Default Analysis Results:")
            for response in responses:
                st.write(response)
    else:
        input_text = st.text_area("Input Prompt:", height=150, help="Enter a custom analysis prompt or additional information.")
        analyze_button = st.button("Analyze Designs (Standard)")
        custom_analyze_button = st.button("Analyze Designs (Custom)")

        if analyze_button and images:
            selected_prompt = analysis_options.get(analysis_choice, "")
            prompt = selected_prompt + " " + input_text if input_text else selected_prompt
            responses = analyze_images(images, prompt)
            st.subheader("Analysis Results:")
            for response in responses:
                st.write(response)

        if custom_analyze_button and images:
            if input_text:  # Ensure there's a custom prompt
                custom_prompt = input_text
                responses = analyze_images(images, custom_prompt)
                st.subheader("Analysis Results:")
                for response in responses:
                    st.write(response)
            else:
                st.warning("Please enter a custom prompt for analysis.")

# Run the Streamlit app
if __name__ == "__main__":
    st.write("Streamlit app is running...")
