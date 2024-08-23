from dotenv import load_dotenv
import streamlit as st
import os
from PIL import Image
import google.generativeai as genai

# Load environment variables
load_dotenv()

# Configure Google Generative AI with the API key
genai.configure(api_key=os.getenv("GOOGLE_API_KEY"))
model = genai.GenerativeModel("gemini-1.5-pro")

# Function to get a response from the Gemini model, incorporating history
def get_gemini_response(input, image, prompt, history):
    # Combine the history with the new input and prompt
    conversation = history + [input, prompt]
    response = model.generate_content([*conversation, image[0]])
    return response.text

# Function to prepare image data
def input_image_setup(uploaded_file):
    if uploaded_file is not None:
        bytes_data = uploaded_file.getvalue()  # Extract image bytes
        image_type = uploaded_file.type  # Extract MIME type
        image_parts = [
            {
                "mime_type": image_type,
                "data": bytes_data
            }
        ]
        return image_parts
    else:
        raise FileNotFoundError("No file uploaded")

# Set up Streamlit app configuration
st.set_page_config(page_title="Gemini Invoice App", page_icon="📄", layout="wide")

# Initialize session state for chat history
if "chat_history" not in st.session_state:
    st.session_state.chat_history = []

# Header
st.title("Gemini Invoice App")
st.markdown("### Upload an invoice image and ask questions!")

# Input section
input_prompt = st.text_input("Input Prompt:", key="input", placeholder="Describe the invoice or ask a question...")

# Image upload section
uploaded_file = st.file_uploader("Choose the invoice to upload", type=["jpg", "jpeg", "png"])
image = ""   
if uploaded_file is not None:
    image = Image.open(uploaded_file)
    st.image(image, caption="Uploaded Image", use_column_width=True)

# Submit button
submit = st.button("Tell me the details of the invoice")

# Predefined prompt for invoice analysis
input_prompts = """
You are not an expert in understanding invoices. We will upload an image of an invoice, 
and you need to answer questions based on that.
"""

# If submit button is clicked, generate the response
if submit:
    if uploaded_file:
        try:
            # Prepare image data
            image_data = input_image_setup(uploaded_file)
            # Append the current prompt to the chat history
            st.session_state.chat_history.append(input_prompt)
            with st.spinner("Analyzing invoice..."):
                # Generate a response considering the full chat history
                response = get_gemini_response(input_prompt, image_data, input_prompts, st.session_state.chat_history)
                # Save the model's response in chat history
                st.session_state.chat_history.append(response)
                st.subheader("Invoice Analysis")
                st.write(response)
        except Exception as e:
            st.error(f"Error: {e}")
    else:
        st.warning("Please upload an image!")

# Display chat history
st.subheader("Chat History")
for i, message in enumerate(st.session_state.chat_history):
    if i % 2 == 0:  # User's input
        st.markdown(f"**You:** {message}")
    else:  # Model's response
        st.markdown(f"**Gemini:** {message}")

# Custom CSS for improved styling
st.markdown("""
    <style>
        .stButton>button {
            background-color: #4CAF50;
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
