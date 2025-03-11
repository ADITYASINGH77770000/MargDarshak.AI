import os
import streamlit as st
import google.generativeai as genai
from dotenv import load_dotenv
import time

load_dotenv()

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

# Generation Configration
generation_config = {
  "temperature": 0.2,
  "top_p": 0.95,
  "top_k": 40,
  "max_output_tokens": 2000,
  "response_mime_type": "text/plain",
  "frequency_penalty": 0.4,
  "presence_penalty":0.5
}

# System Instruction
system_instructions = {"""
    You are Margdarshak.AI an AI based Roadmap Generator. You can generate roadmap for Students based on data provided by them.
"""}

# Model
model = genai.GenerativeModel(model_name="gemini-2.0-flash",
                              generation_config=generation_config,
                              safety_settings=safety_settings,
                              system_instruction=system_instructions)

st.header("📚AI Roadmap Generator", divider="rainbow")
with st.expander('What is Roadmap Generator?'):
    st.write("Margdarshak.AI is an AI-based Roadmap Generator that helps students to create a roadmap for their academic journey. And provide course recommendations, study material generation and more.")

with st.form("my_form"):
    target_career = st.text_input("Enter your target career*", help="Enter your target career for which you want to create roadmap.", placeholder="Data Scientist")
    skill_already_have = st.text_input("Enter the skills you already have*", help="Enter the skills you already have for the target career.", placeholder="Python, Machine Learning")
    skill_want_to_learn = st.text_input("Enter the skills you want to learn*", help="Enter the skills you want to learn for the target career.", placeholder="Deep Learning, NLP")
    preferred_learning_mode = st.selectbox("Preferred Learning Mode*", ["Self-Paced", "Online Courses", "Mentorship"])
    time_commitment = st.number_input("Time Commitment (in hours)*", help="Enter the time commitment in hours per day.", min_value=1, max_value=10, value=5)
    career_goal_timeline = st.selectbox("Career Goal Timeline*", ["0-6 Months", "6-12 Months", "1+ Years"])
    experience_level = st.selectbox("Experience Level*", ["Beginner", "Intermediate", "Advanced"])
    st.markdown("**Required*")
    submit_button = st.form_submit_button(label="Generate Roadmap")

if submit_button:
    if not target_career or not skill_already_have or not skill_want_to_learn or not preferred_learning_mode or not time_commitment or not career_goal_timeline or not experience_level:
        st.error("Please fill all the required fields.")
        st.stop()
    else:
        st.success("Your Entries are submitted successfully.")
st.divider()
with st.spinner("Processing..."):
    if target_career and skill_already_have and skill_want_to_learn and preferred_learning_mode and time_commitment and career_goal_timeline:
        prompt = f"""
            Generate the Roadmap for a student who wants to become a {target_career}. The student already has skills like {skill_already_have} and wants to learn skills like {skill_want_to_learn}. The student prefers {preferred_learning_mode} learning mode and can commit {time_commitment} hours per day. The student wants to achieve the career goal in {career_goal_timeline}. The student has {experience_level} experience level.
    """
        response = model.generate_content(prompt)
        st.subheader("Hi, Here is the Roadmap for you:")
        output_ai_text = response.text
        def stream_output_ai_text():
            for word in output_ai_text.split(" "):
                yield word + " "
                time.sleep(0.02)
        st.write_stream(stream_output_ai_text())
    else:
        st.warning("Please fill all the required fields.")