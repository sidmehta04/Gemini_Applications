import streamlit as st
import google.generativeai as genai
from dotenv import load_dotenv
import os
from PIL import Image

# Load environment variables
load_dotenv()

# Configure Google Generative AI with the API key
genai.configure(api_key=os.getenv("GOOGLE_API_KEY"))

# Function to get a response from the Gemini model
def get_gemini_response(input, image, prompt):
    model = genai.GenerativeModel("gemini-1.5-pro")
    response = model.generate_content([input, image[0], prompt])
    return response.text

# Function to prepare image data
def input_image_setup(uploaded_file):
    if uploaded_file is not None:
        bytes_data = uploaded_file.getvalue()
        image_parts = [
            {
                "mime_type": uploaded_file.type,
                "data": bytes_data
            }
        ]
        return image_parts
    else:
        raise FileNotFoundError("No file uploaded")

# Set up Streamlit app configuration
st.set_page_config(page_title="Gemini Health App", page_icon="🍎", layout="wide")

# Header
st.title("Gemini Health App")
st.markdown("### Upload a food image and get calorie information!")

# Input section
input = st.text_input("Input Prompt:", key="input", placeholder="Describe the image or ask a question...")

# Image upload section
uploaded_file = st.file_uploader("Choose an image...", type=["jpg", "jpeg", "png"])
image = ""   
if uploaded_file is not None:
    image = Image.open(uploaded_file)
    st.image(image, caption="Uploaded Image.", use_column_width=True)

# Submit button
submit = st.button("Tell me the total calories")

# Predefined prompt for calorie estimation
input_prompt = """
You are an expert nutritionist. Look at the food items in the image and calculate the total calories. 
Also, provide details of each food item with its calorie intake in the following format:

1. Item 1 - number of calories
2. Item 2 - number of calories
----
----
"""

# If submit button is clicked, generate the response
if submit:
    if uploaded_file:
        try:
            image_data = input_image_setup(uploaded_file)
            with st.spinner("Analyzing image..."):
                response = get_gemini_response(input_prompt, image_data, input)
                st.subheader("Calorie Analysis")
                st.write(response)
        except Exception as e:
            st.error(f"Error: {e}")
    else:
        st.warning("Please upload an image!")

# Custom CSS for improved styling
st.markdown("""
    <style>
        .stButton>button {
            background-color: #FF6347;
            color: white;
            font-size: 16px;
            padding: 10px 20px;
            border-radius: 8px;
            margin-top: 20px;
        }
        .stTextInput input {
            padding: 10px;
            border-radius: 8px;
            font-size: 16px;
        }
        .stFileUploader {
            margin-top: 20px;
        }
        .stMarkdown h2, h3 {
            color: #2E8B57;
        }
        .stImage img {
            border-radius: 15px;
            box-shadow: 2px 2px 10px rgba(0, 0, 0, 0.1);
        }
    </style>
""", unsafe_allow_html=True)
