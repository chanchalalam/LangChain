from dotenv import load_dotenv
load_dotenv()

import streamlit as st
import os
from PIL import Image
import google.generativeai as genai

genai.configure(api_key=os.getenv("GOOGLE_API_KEY"))

model= genai.GenerativeModel('gemini-pro-vision')

def get_gemini_response(input,image,prompt):
    response = model.generate_content([input,image[0],prompt])
    return response.text

def input_image_details(uploaded_file):
    if uploaded_file is not None:
        byte_data = uploaded_file.getvalue()

        image_parts =[
            {
                "mimi_type": uploaded_file.type,
                "data": byte_data
            }
        ]
        return image_parts
    else:
        raise FileNotFoundError("No file uploaded")

st.set_page_config(page_title="Multi Language Invoive Extraction")

st.header("Multi Language Invoive Extraction")
input=st.text_input("Input Prompt: ",key="Input")
uploaded_file = st.file_uploader("Choose an image of the invoice....", type=["jpeg","png","jpg",])
Image=""
if uploaded_file is not None:
    image = Image.open(uploaded_file)  

    st.image(image, caption="Uploaded Image",use_column_width=True)

submit = st.button("Tell me about the invoice")

input_prompt = ""

if submit:
    image_data= input_image_details(uploaded_file)
    response = get_gemini_response(input_prompt,image_data,input)
    st.subheader("The response is")
    st.write(response)