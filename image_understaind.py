from dotenv import load_dotenv
import streamlit as st
import os
from PIL import Image
import google.generativeai as genai

# Load environment variables
load_dotenv()

# Configure Google Generative AI with the API key
genai.configure(api_key=os.getenv("GOOGLE_API_KEY"))

# Define a function to get a response from the Gemini model
def get_gemini_response(input, image):
    model = genai.GenerativeModel('gemini-1.5-pro')
    if input != "":
        response = model.generate_content([input, image])
    else:
        response = model.generate_content(image)
    return response.text

# Set page config with a custom title and layout
st.set_page_config(page_title="Gemini Image Demo", page_icon="📷", layout="wide")

# Sidebar for additional navigation or options
st.sidebar.title("Q&A Chatbot")
st.sidebar.markdown("Upload an image and ask Gemini for details!")

# Main header
st.header("Gemini Image and Q&A Chatbot")

# Input section
st.subheader("Enter your prompt:")
input = st.text_input("Input Prompt:", key="input", placeholder="Describe the image or ask a question...")

# Image upload section
st.subheader("Upload an image:")
uploaded_file = st.file_uploader("Choose an image...", type=["jpg", "jpeg", "png"])

# Display the uploaded image
image = ""
if uploaded_file is not None:
    image = Image.open(uploaded_file)
    st.image(image, caption="Uploaded Image", use_column_width=True)

# Submit button
submit = st.button("Analyze Image & Prompt")

# If submit button is clicked, generate the response
if submit:
    if uploaded_file or input:
        with st.spinner("Processing..."):
            response = get_gemini_response(input, image)
            st.subheader("Gemini's Response")
            st.write(response)
    else:
        st.warning("Please provide either an image or a text prompt.")

# Custom CSS for better styling
st.markdown("""
    <style>
        .stButton>button {
            background-color: #ff4b4b;
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
            color: #4CAF50;
        }
        .stImage img {
            border-radius: 15px;
            box-shadow: 2px 2px 10px rgba(0, 0, 0, 0.1);
        }
    </style>
""", unsafe_allow_html=True)
