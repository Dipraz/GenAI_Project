import streamlit as st
from PIL import Image
import os
import google.generativeai as genai
from google.generativeai import GenerativeModel
import os

# Load the API key from environment variables
os.getenv("GOOGLE_API_key")
genai.configure(api_key=os.getenv("GOOGLE_API_key"))

# Function to perform image analysis
def analyze_image(image, prompt):
    model = genai.GenerativeModel('gemini-pro-vision')
    response = model.generate_content([prompt, image])
    return response.text

# Function to handle chat messages
def send_chat_message(model, history, user_message):
    history.append({"text": user_message, "sender": "user"})
    response = model.generate_content(history=history)
    if response:
        history.append({"text": response.text, "sender": "ai"})
    return history, response.text

# Main function to run the Streamlit app
def main():
    st.set_page_config(page_title="PowerPoint Slide Analysis", layout="wide")
    st.title("PowerPoint Slide Analysis with AI")
    st.markdown("---")

    # Layout: two columns for image analysis and chat
    col1, col2 = st.columns([3, 1])

    with col1:
        st.header("Image Analysis")
        analysis_options = {
            "Content Analysis": "Identify topics, themes, or keywords from the slides.",
            "Visual Analysis": "Group slides based on layout, color palettes, chart types, or image presence.",
            "Presentation Type": "Differentiate between introductory slides, data visualizations, analysis reports, or storytelling narratives.",
            "Emotional Tone": "Gauge the overall emotional sentiment conveyed by the slides.",
            "Time-Based Organization": "Cluster slides based on creation date or presentation sequence."
        }
        input_prompt = st.selectbox("Select Analysis Type:", list(analysis_options.keys()))
        upload_file = st.file_uploader("Upload Slide Image:", type=["jpg", "jpeg", "png"])

        if upload_file:
            image = Image.open(upload_file)
            st.image(image, caption="Uploaded Slide", use_column_width=True)

        submit = st.button("Analyze Slide")

        if submit and upload_file:
            selected_prompt = analysis_options[input_prompt]
            response = analyze_image(image, selected_prompt)
            st.subheader("Analysis Result:")
            st.write(response)
        elif submit and not upload_file:
            st.error("Please upload an image to analyze.")

    with col2:
        st.header("Chat About the Results")
        # Initialize the chat model
        chat_model = genai.GenerativeModel('gemini-pro')

        # Session state to keep track of chat history
        if 'chat_history' not in st.session_state:
            st.session_state['chat_history'] = []

        chat_input = st.text_input("Your message:", key="chat_input")
        send_message = st.button("Send", key="send_message")

        if send_message and chat_input:
            # Update chat history with the user message and the model's response
            st.session_state['chat_history'], response = send_chat_message(
                chat_model,
                st.session_state['chat_history'],
                chat_input
            )
            # Display the conversation
            for chat in st.session_state['chat_history']:
                if chat["sender"] == "user":
                    st.text_area("", chat["text"], key=str(chat), height=40, disabled=True)
                else:
                    st.text_area("", chat["text"], key=str(chat), height=80, disabled=True, background_color="#E8E8E8")
            # Clear the chat input box after sending the message
            st.session_state.chat_input = ""

        # Displaying the chat history
        for chat in st.session_state['chat_history']:
            st.write(f"{chat['sender'].title()}: {chat['text']}")

if __name__ == "__main__":
    main()
