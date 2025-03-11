import os
import streamlit as st
import google.generativeai as genai
from dotenv import load_dotenv
from features.functions import *
# from features.auth import get_user_details

load_dotenv()

# Get user details
# user_data = get_user_details()
# name = user_data.get("name")
# preferred_lang = user_data.get("preferred_lang")

# Load environment variables
# GEMINI_API_KEY = os.getenv("GEMINI_API_KEY")
GEMINI_API_KEY = st.secrets["GOOGLE_API_KEY"]
genai.configure(api_key=GEMINI_API_KEY)

# Safety Settings
safety_settings = [
    {
        "category": "HARM_CATEGORY_HARASSMENT",
        "threshold": "BLOCK_MEDIUM_AND_ABOVE"
    },
    {
        "category": "HARM_CATEGORY_HATE_SPEECH",
        "threshold": "BLOCK_MEDIUM_AND_ABOVE"
    },
    {
        "category": "HARM_CATEGORY_SEXUALLY_EXPLICIT",
        "threshold": "BLOCK_MEDIUM_AND_ABOVE"
    },
    {
        "category": "HARM_CATEGORY_DANGEROUS_CONTENT",
        "threshold": "BLOCK_MEDIUM_AND_ABOVE"
    },
]

# Generation Configurations
generation_config = {
  "temperature": 0.4,
  "top_p": 0.95,
  "top_k": 30,
  "max_output_tokens": 1000,
  "response_mime_type": "text/plain",
  "frequency_penalty": 0.4,
  "presence_penalty":0.5
}

# System Instructions
system_instructions = {
    f"""
    You are CareerBot AI an AI based Mentor. You can provide career guidance, talk about trending skills, mentor students and more.
    Try to make the conversation more engaging and interactive. Try to use emojies and make the convo more fun.
    """
}

# Load model
model = genai.GenerativeModel(model_name="gemini-1.5-flash-latest",
                              safety_settings=safety_settings,
                              generation_config=generation_config,
                              system_instruction=system_instructions)

st.header('🧑🏻‍🏫AI Mentor', divider='rainbow')

# Initialize chat session in Streamlit if not already present
if "chat_session" not in st.session_state:
    st.session_state.chat_session = model.start_chat(history=[])

# Display the chat history
for msg in st.session_state.chat_session.history:
    with st.chat_message(map_role(msg["role"])):
        st.markdown(msg["content"])

# Input field for user's message
user_input = st.chat_input("Ask Me Anything...")
if user_input:
    # Add user's message to chat and display it
    st.chat_message("user").markdown(user_input)

    # Send user's message to Gemini and get the response
    gemini_response = fetch_gemini_response(user_input)

    # Display Gemini's response
    with st.chat_message("assistant"):
        st.markdown(gemini_response)

    # Add user and assistant messages to the chat history
    st.session_state.chat_session.history.append({"role": "user", "content": user_input})
    st.session_state.chat_session.history.append({"role": "model", "content": gemini_response})

# Clear current chat session
with st.sidebar:
    if st.button("Clear Chat"):
        st.session_state.chat_session = model.start_chat(history=[])