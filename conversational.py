from dotenv import load_dotenv
import streamlit as st
import google.generativeai as genai
import os

# Load environment variables
load_dotenv()

# Configure Google Generative AI with the API key
genai.configure(api_key=os.getenv("GOOGLE_API_KEY"))

# Initialize the chat model
model = genai.GenerativeModel("gemini-1.0-pro")
chat = model.start_chat(history=[])

# Define a function to get a response from the Gemini model
def get_gemini_response(question):
    response = chat.send_message(question, stream=True)
    return response

# Streamlit app layout
st.set_page_config(page_title="Gemini AI Chat", page_icon="🤖", layout="wide")

st.title("Gemini AI Chat")

# Initialize chat history in session state if not already done
if 'chat_history' not in st.session_state:
    st.session_state['chat_history'] = []

# Input box for the user to enter a question
st.text_input("Enter your question:", key="input")

# Ask Gemini button and response handling
if st.button("Ask Gemini"):
    question = st.session_state.get("input")
    if question:
        with st.spinner("Thinking..."):
            response = get_gemini_response(question)
            # Add user question to chat history
            st.session_state['chat_history'].append(("You", question))
            # Display and store bot's response in chunks
            bot_response = ""
            for chunk in response:
                bot_response += chunk.text
            st.session_state['chat_history'].append(("Gemini", bot_response))
        st.subheader("Gemini Response")
        st.write(bot_response)
    else:
        st.warning("Please enter a question!")

# Display chat history
st.subheader("Chat History")

chat_container = st.container()
with chat_container:
    for role, text in st.session_state['chat_history']:
        if role == "You":
            st.markdown(f"**{role}:** {text}")
        else:
            st.markdown(f"<span style='color: blue;'>{role}:</span> {text}", unsafe_allow_html=True)

# CSS for better visuals
st.markdown("""
    <style>
        .stButton>button {
            background-color: #4CAF50;
            color: white;
            border-radius: 8px;
            padding: 10px 24px;
            font-size: 16px;
            margin-top: 10px;
        }
        .stTextInput input {
            border-radius: 8px;
            padding: 10px;
            font-size: 16px;
        }
        .stMarkdown p {
            font-size: 18px;
            line-height: 1.6;
        }
    </style>
""", unsafe_allow_html=True)
