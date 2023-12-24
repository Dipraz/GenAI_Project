from dotenv import load_dotenv
import streamlit as st
from PIL import Image
import google.generativeai as genai
import os

load_dotenv()  # Take environment variables from .env.
genai.configure(api_key=os.getenv("GOOGLE_API_KEY"))

chat = None  # Initialize chat object

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

    if prompt == "General Analysis":
        response = model.generate_content(["Identify and describe everything you see in this image.", image])
    elif prompt == "Disease Identification":
        response = model.generate_content(["Identify the disease or medical condition shown in the image, if any.", image])
    elif prompt == "Personalized Diet Plans Based on Bangladeshi Foods":
        response = model.generate_content(["Generate a personalized diet plan incorporating Bangladeshi foods based on the depicted health condition or dietary requirements in the image.", image])
    elif prompt == "Health Tips and Lifestyle Recommendations":
        response = model.generate_content(["Offer health tips and lifestyle recommendations suitable for the observed health scenario in the image.", image])
    elif prompt == "Medicine Information":
        response = model.generate_content(["Provide information about Medicine Information such as indication, dosages, side effects, and medications or treatments related to the health issue depicted in the image.", image])
    else:
        return "Invalid prompt selected. Please choose a valid option."

    return response if response else "No response generated for this prompt."

def start_gemini_chat(history=[]):
    model = genai.GenerativeModel('gemini-pro')
    return model.start_chat(history=history)

def main():
    global chat  # Access the global chat object
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
                    # Initialize or continue the chat after displaying the result
                    chat = start_gemini_chat([response.text])
            else:
                st.warning("Please select an analysis option.")

    with col2:
        st.markdown("---")
        st.header("Chat About the Results")
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
            st.warning("Please analyze an image to start the chat.")

if __name__ == "__main__":
    main()
