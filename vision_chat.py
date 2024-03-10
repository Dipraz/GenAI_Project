from dotenv import load_dotenv
import streamlit as st
from PIL import Image
import google.generativeai as genai
import os

load_dotenv()  # Take environment variables from .env.
genai.configure(api_key=os.getenv("GOOGLE_API_KEY"))

def get_gemini_response(input, image):
    model = genai.GenerativeModel('gemini-pro-vision')
    if input != "":
        response = model.generate_content([input, image])
    else:
        response = model.generate_content(image)
    return response.text

def handle_button_click(prompt, image):
    model = genai.GenerativeModel('gemini-pro-vision')
    response = None  # Initialize response as None

    try:
        if prompt == "General Analysis":
            if image:  # Check if image is not empty
                response = model.generate_content(["Identify and describe everything and every words you see in this image.", image])
            else:
                return "Please upload an image for analysis."
        elif prompt == "Disease Identification":
            if image:  # Check if image is not empty
                response = model.generate_content(["Identify the disease or medical condition shown in the image, if any.", image])
            else:
                return "Please upload an image for analysis."
        elif prompt == "Personalized Diet Plans Based on Bangladeshi Foods":
            if image:  # Check if image is not empty
                response = model.generate_content(["Generate a personalized diet plan incorporating Bangladeshi foods based on the depicted health condition or dietary requirements in the image.", image])
            else:
                return "Please upload an image for analysis."
        elif prompt == "Health Tips and Lifestyle Recommendations":
            if image:  # Check if image is not empty
                response = model.generate_content(["Offer health tips and lifestyle recommendations suitable for the observed health scenario in the image.", image])
            else:
                return "Please upload an image for analysis."
        elif prompt == "Medicine Information":
            if image:  # Check if image is not empty
                response = model.generate_content(["Provide information about Medicine Information such as indication, dosages, side effects, and medications or treatments related to the health issue depicted in the image.", image])
            else:
                return "Please upload an image for analysis."
        else:
            return "Invalid prompt selected. Please choose a valid option."
    except Exception as e:
        return f"An error occurred: {str(e)}"  # Print out the exception message

    return response.text if response else "No response generated for this prompt."

def start_gemini_chat(history=[]):
    model = genai.GenerativeModel('gemini-pro')
    return model.start_chat(history=history)

def main():
    chat = None  # Initialize chat object
    
    st.set_page_config(page_title="Gemini Image Demo", layout="wide")
    st.title("AI Image Analysis")
    st.markdown("---")

    col1, col2 = st.columns([3, 1])

    with col1:
        st.header("Choose an Analysis Option")
        input_prompt = st.selectbox("Select Analysis:", ("General Analysis", "Disease Identification", "Personalized Diet Plans Based on Bangladeshi Foods", "Health Tips and Lifestyle Recommendations", "Medicine Information"))
        input_text = st.text_input("Input Custom Prompt:", key="input")
        
        upload_file = st.file_uploader("Upload Image:", type=["jpg", "Jpeg", "png"])
        
        if upload_file is not None:
            image = Image.open(upload_file)
            st.image(image, caption="Uploaded Image", use_column_width=True)
        else:
            image = ""

        submit = st.button("Analyze")

        if submit:
            if input_prompt:
                response = handle_button_click(input_prompt, image)
                if isinstance(response, str):
                    st.warning(response)
                else:
                    st.subheader("Analysis Result:")
                    st.write(response.text)  # Assuming .text attribute contains the generated text
            else:
                st.warning("Please select an analysis option.")

    with col2:
        st.markdown("---")
        st.header("Chat About the Results")
        if chat is None:
            chat = start_gemini_chat()  # Initialize chat if not done already

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

if __name__ == "__main__":
    main()
