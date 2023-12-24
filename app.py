# Q&A Chatbot
#from langchain.llms import OpenAI

from dotenv import load_dotenv

load_dotenv() # take environment variables from .env.

import streamlit as st
import os
import pathlib
import textwrap

import google.generativeai as genai

from IPython.display import display
from IPython.display import Markdown


def to_markdown(text):
  text = text.replace('•', '  *')
  return Markdown(textwrap.indent(text, '> ', predicate=lambda _: True))

os.getenv("GOOGLE_API_key")
genai.configure(api_key=os.getenv("GOOGLE_API_key"))

##Function to load OpenAI model and get responses..

def get_gemini_response(question):
    model = genai.GenerativeModel('gemini-pro')
    response = model.generate_content(question)
    return response.text

## Our Streamlit app initialization

st.set_page_config(page_title="Demo For Q & A")

st.header("Gemini Application")

input = st.text_input("Input: ",key="input")


submit = st.button("Ask your questions...")

if submit:
    
    response=get_gemini_response(input)
    st.subheader("The Response is...")
    st.write(response)



