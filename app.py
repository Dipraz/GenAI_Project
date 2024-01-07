from dotenv import load_dotenv
import streamlit as st
from PIL import Image, UnidentifiedImageError
import google.generativeai as genai
import os
import logging

# Configure logging
logging.basicConfig(filename='app.log', level=logging.ERROR)

# Load environment variables
load_dotenv()

# Configure Google Generative AI API
genai.configure(api_key=os.getenv("GOOGLE_API_KEY"))

def get_gemini_response(input, images):
    try:
        model = genai.GenerativeModel('gemini-pro-vision')
        responses = []
        for image in images:
            if input != "":
                response = model.generate_content([input, image])
            else:
                response = model.generate_content(image)
            responses.append(response.text)
        return responses
    except Exception as e:
        logging.error(f"An error occurred: {str(e)}")
        return [f"An error occurred: {str(e)}"]

# Define analysis options dictionary
analysis_options = {
        "general analysis": "Identify and describe everything and every word you see in this image.",
        "Focus on Template-Specific Considerations": "Imagine you are tasked with creating slide templates based on the provided folder of slides. Analyze each slide and identify potential groupings that could represent distinct templates. Consider these factors:Reusability of layout: Can the overall structure, color scheme, and element arrangement be easily adapted to different content?Modular design: Are there distinct sections or components within the layout that can be easily replaced or swapped?Brand consistency: Does the layout align with any existing brand guidelines or visual identity?Scalability: Can the template accommodate different content lengths and variations without losing its visual integrity?",
        "content understanding and summarization": "For this presentation slide, identify the key topics, ideas, and arguments presented. Generate a concise summary capturing the essential points, highlighting any noteworthy statistics or trends.",
        "Focus on Visual Features and Layout Similarities": "Analyze the visual features and layout of each slide in the provided folder, identifying slides that share significant similarities in terms of:Overall layout structure: Grids, columns, sections, placement of elements.Color palettes and font styles: Dominating colors, font families, font sizes, and their arrangement.Object arrangement and relationships: Position of text boxes, images, charts, and other elements relative to each other.Spacing and margins: White space distribution, padding between elements, and overall visual balance.Group the slides with the most similar layout features together, highlighting potential templates and suggesting common design patterns within each group.Provide detailed descriptions of the identified similarities for each group, explaining why these slides might be considered part of the same template family.",
        "semantic relationships and knowledge extraction": "Extract the underlying concepts and ideas presented on this slide and explain their connections. Identify any potential contradictions or inconsistencies in the information presented.",
        "presentation style and effectiveness analysis": "Analyze the effectiveness of the slide transitions and pacing in maintaining audience engagement. Suggest improvements to the presentation style and delivery for better audience understanding and retention.",
        "decoding success": "Analyze the presentation style in comparison to similar high-performing presentations within the same field. Identify specific elements (e.g., visuals, engagement, flow) that contribute to their effectiveness and suggest how you can incorporate these best practices to elevate your own presentation delivery."
    }

def handle_button_click(input, images):
    if input in analysis_options:
        prompt = analysis_options[input]
        responses = get_gemini_response(prompt, images)
    else:
        return ["Invalid prompt selected. Please choose a valid option."]

    return responses

def start_gemini_chat(history=[]):
    model = genai.GenerativeModel('gemini-pro')
    return model.start_chat(history=history)

def main():
    chat = None
    images = []
    st.set_page_config(page_title="Gemini Image Demo", page_icon="🦄", layout="wide")
    st.title("AI Image Analysis")
    st.markdown("---")

    col1, col2 = st.columns([3, 1])

    with col1:
        st.header("Choose an Analysis Option")
        input_prompt = st.selectbox("Select Analysis:", list(analysis_options.keys()))

        st.subheader("Upload Image(s)")
        upload_files = st.file_uploader("Upload Image(s):", type=["jpg", "jpeg", "png"], accept_multiple_files=True)

        if upload_files:
            images.clear()  # Clear existing images
            for uploaded_file in upload_files:
                try:
                    image = Image.open(uploaded_file)
                    images.append(image)
                    st.image(image, caption="Uploaded Image", use_column_width=True)
                except UnidentifiedImageError:
                    st.error(f"The file {uploaded_file.name} is not a valid image.")

        submit = st.button("Analyze Image(s)")

        if submit:
            if input_prompt and images:
                responses = handle_button_click(input_prompt, images)
                for idx, response in enumerate(responses):
                    st.subheader(f"Analysis Result for Image {idx + 1}:")
                    st.write(response)
            else:
                st.warning("Please select an analysis option and upload image(s).")

    with col2:
        st.markdown("---")
        st.header("Chat About the Results")

        if chat is None:
            st.info("Initializing the chat... Please wait.")
            chat = start_gemini_chat()
            st.info("Chat initialized. You can now start chatting with Gemini.")

        if chat is not None:
            chat_input = st.text_input("Chat Input:", key="chat_input")
            send_message = st.button("Send")

            if send_message:
                if chat_input:
                    response = chat.send_message(chat_input, stream=True)
                    st.subheader("Gemini's Response:")
                    for chunk in response:
                        st.write(chunk.text)
                else:
                    st.warning("Please input a message to chat.")
        else:
            st.warning("Please wait... Initializing the chat.")

    st.markdown("---")
    st.markdown("©2024 @Hotmailer. All rights reserved.")

if __name__ == "__main__":
    main()
