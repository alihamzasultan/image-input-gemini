### Health Management APP
from dotenv import load_dotenv

load_dotenv() ## load all the environment variables

import streamlit as st
import os
import google.generativeai as genai
from PIL import Image

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
    
##initialize our streamlit app

st.set_page_config(page_title="Gemini Health App")

st.header("Gemini Health App")
input=st.text_input("Input Prompt: ",key="input")
uploaded_file = st.file_uploader("Choose an image...", type=["jpg", "jpeg", "png"])
image=""   
if uploaded_file is not None:
    image = Image.open(uploaded_file)
    st.image(image, caption="Uploaded Image.", use_column_width=True)


submit=st.button("Tell me the total calories")

input_prompt="""

Task: As an expert in FrontEnd Development, your task is to examine an image representing the design of a website's frontend and produce the corresponding HTML and CSS code to replicate the design. Additionally, you are required to provide details of the elements used in the design and suggest GitHub repositories that contain similar design elements in their repository name.

Instructions:

Inspect the Design: Begin by carefully examining the provided image, which represents the visual layout and design elements of a website.
Generate HTML and CSS Code: Based on your analysis of the design, write HTML and CSS code to recreate the layout, styling, and functionality of the website. Ensure that the generated code closely matches the visual representation in the image.
HTML Code: Write the HTML markup for the structure of the webpage, including elements such as headers, navigation menus, sections, divs, and footer.
CSS Code: Define the styling rules using CSS to achieve the visual appearance, positioning, colors, fonts, and responsiveness observed in the design.
Provide Element Details: Document the details of each element used in the design, including their purpose, functionality, and styling attributes. This will help in understanding the role of each component within the webpage.
GitHub Repositories: Identify GitHub repositories that contain similar frontend design elements or templates. Search for repositories with descriptive names or keywords that match the design features. Provide links to these repositories for further exploration and reference.
Example Output Format:

HTML Code:
html
Copy code
<!-- Insert HTML code generated based on the design -->
<header>
    <nav>
        <ul>
            <li><a href="#">Home</a></li>
            <li><a href="#">About</a></li>
            <li><a href="#">Services</a></li>
            <li><a href="#">Contact</a></li>
        </ul>
    </nav>
</header>
<section>
    <h1>Welcome to our Website</h1>
    <p>Lorem ipsum dolor sit amet, consectetur adipiscing elit.</p>
</section>
<!-- More HTML code for other sections -->
CSS Code:
css
Copy code
/* Insert CSS code generated based on the design */
body {
    font-family: Arial, sans-serif;
    background-color: #f0f0f0;
}
header {
    background-color: #333;
    color: #fff;
    padding: 10px;
}
nav ul {
    list-style-type: none;
    margin: 0;
    padding: 0;
}
/* More CSS rules for styling */
Element Details:
Header: Contains the navigation menu and branding/logo.
Navigation Menu: Consists of links to various sections of the website.
Section: Divided content areas with descriptive headings and text.
GitHub Repositories:
example-repo1
example-repo2
example-repo3
Note: Ensure that the generated code is well-structured, semantic, and adheres to best practices in web development to ensure maintainability and accessibility
"""

## If submit button is clicked

if submit:
    image_data=input_image_setup(uploaded_file)
    response=get_gemini_repsonse(input_prompt,image_data,input)
    st.subheader("The Response is")
    st.write(response)

