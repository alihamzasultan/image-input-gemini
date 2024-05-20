### Health Management APP
from dotenv import load_dotenv

load_dotenv() ## load all the environment variables

import streamlit as st
import os
import google.generativeai as genai
from PIL import Image
from io import BytesIO
import base64
import cv2


genai.configure(api_key=os.getenv("GOOGLE_API_KEY"))

## Function to load Google Gemini Pro Vision API And get response

def get_gemini_repsonse(input,image,prompt):
    model=genai.GenerativeModel('gemini-pro-vision')
    response=model.generate_content([input,image[0],prompt])
    return response.text

def input_image_setup(uploaded_file):
    # Check if a file has been uploaded
    if uploaded_file is not None:
        # Read the file into bytes
        bytes_data = uploaded_file.getvalue()

        image_parts = [
            {
                "mime_type": uploaded_file.type,  # Get the mime type of the uploaded file
                "data": bytes_data
            }
        ]
        return image_parts
    else:
        raise FileNotFoundError("No file uploaded")
    
def get_image_from_camera():
    st.write("Click below to take a picture:")
    if st.button("Open Camera"):
        cap = cv2.VideoCapture(0)
        ret, frame = cap.read()
        cap.release()
        if ret:
            # Convert the image to bytes
            img = Image.fromarray(frame)
            buffer = BytesIO()
            img.save(buffer, format="JPEG")
            data = base64.b64encode(buffer.getvalue()).decode()
            st.image(img, caption="Captured Image", use_column_width=True)
            return data
        else:
            st.write("Failed to open camera. Please try again.")
    
##initialize our streamlit app

st.set_page_config(page_title="Gemini Health App")

st.header("Gemini")
input=st.text_input("Input Prompt: ",key="input")
uploaded_file = st.file_uploader("Choose an image...", type=["jpg", "jpeg", "png"])
image=""   
if uploaded_file is not None:
    image = Image.open(uploaded_file)
    st.image(image, caption="Uploaded Image.", use_column_width=True)

camera_data = get_image_from_camera()

submit=st.button("do EDA")

input_prompt="""

Instructions:

analyse the dataset
"""

## If submit button is clicked

if submit:
    if camera_data is None and uploaded_file is None:
        st.write("Please upload an image or capture one from the camera.")
    elif uploaded_file is not None:
        image_data=input_image_setup(uploaded_file)
        response=get_gemini_repsonse(input_prompt,image_data,input)
        st.subheader("The Response is")
        st.write(response)
    else:
        response=get_gemini_repsonse(input_prompt,[{"mime_type": "image/jpeg", "data": camera_data}],input)
        st.subheader("The Response is")
        st.write(response)
