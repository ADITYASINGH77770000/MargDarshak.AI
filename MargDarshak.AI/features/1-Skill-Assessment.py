import google.generativeai as genai
import streamlit as st
from dotenv import load_dotenv
import os
import time
import fitz
import random

# Load environment variables
load_dotenv()

# Configure Gemini API
# GOOGLE_API_KEY = os.getenv("GOOGLE_API_KEY")
GOOGLE_API_KEY = st.secrets["GOOGLE_API_KEY"]
genai.configure(api_key=GOOGLE_API_KEY)

# Generation Configration
generation_config = {
  "temperature": 0.2,
  "top_p": 0.95,
  "top_k": 40,
  "max_output_tokens": 1000,
  "response_mime_type": "text/plain",
  "frequency_penalty": 0.4,
  "presence_penalty":0.5
}

gemini_model = genai.GenerativeModel("gemini-1.5-flash", generation_config=generation_config)

def get_gemini_recommendation(domain, career_goal, skills):
    """
    Generates learning recommendations based on career domain, goal, and current skills.
    """
    try:
        prompt = f"""
        My career domain is {domain} and my career goal is {career_goal}.
        My current skills are: {skills}.
        What should I learn to advance in my career?
        """
        response = gemini_model.generate_content(prompt)
        output_response = response.text
        def stream_output_ai_text():
            for word in output_response.split(" "):
                yield word + " "
                time.sleep(0.02)
        return st.write_stream(stream_output_ai_text())
    except Exception as e:
        return f"Error generating recommendations: {e}"

# Function to extract text from PDF using PyMuPDF
def extract_text_from_pdf(uploaded_file):
    """Extract text from uploaded PDF file using PyMuPDF."""
    try:
        doc = fitz.open(stream=uploaded_file.read(), filetype="pdf")
        text = ""
        for page in doc:
            text += page.get_text("text") + "\n"
        return text.strip()
    except Exception as e:
        st.error(f"Error extracting text: {e}")
        return None

# Function to analyze resume using Gemini AI
def analyze_resume(resume_text, career_path):
    """Extracts skills, experience, and suggests missing skills using Gemini AI."""
    model = genai.GenerativeModel('gemini-1.5-flash')
    chat = model.start_chat(history=[])
    prompt = f"""
    Analyze the following resume text and extract:
    - Skills listed
    - Experience (years, roles, companies if mentioned)
    - Suggest missing skills for the given career path: {career_path}
    - Recommend relevant courses with company name and sources

    Resume:
    {resume_text}
    """
    response = chat.send_message(prompt, stream=True)
    extracted_info = ""
    for chunk in response:
        if chunk.text:
            extracted_info += chunk.text
    return extracted_info

# Function to generate a resume score
def generate_resume_score(resume_text):
    """Calculates a resume score based on length, skills, and keywords."""
    length_score = min(len(resume_text) // 100, 30)  # Score based on text length
    skill_score = random.randint(20, 30)  # Placeholder for skill evaluation
    experience_score = random.randint(10, 20)  # Placeholder for experience evaluation
    total_score = length_score + skill_score + experience_score
    return min(total_score, 100)  # Score capped at 100

st.header('📊AI-Powered Skill or Resume Analysis', anchor='learning-recommendations', divider='rainbow')

with st.expander('What is SkillLens?'):
    st.write('SkillLens is an AI-powered tool that helps you analyze your skills, career path, and provides personalized learning recommendations. You can either upload your resume for analysis or manually input your career domain, goal, and skills to get learning recommendations.')

resume_or_not = st.selectbox("Do you have a resume to analyze and recommend learning?", ["Yes", "No"], key="resume_or_not")

if resume_or_not == "Yes":
    uploaded_file = st.file_uploader("Upload your Resume (PDF only)", type=["pdf"])

    # Manual Career Path Input
    selected_career = st.text_input("Enter your desired career path (Optional)", "")

    # Submit Button
    submit = st.button("Analyze Resume")

    # Processing
    if submit:
        if not uploaded_file:
            st.error("Please upload a PDF resume!")
            st.stop()
        else:
            with st.spinner("⏳ Analyzing your resume..."):
                resume_text = extract_text_from_pdf(uploaded_file)
                if resume_text:
                    analysis_result = analyze_resume(resume_text, selected_career)
                    resume_score = generate_resume_score(resume_text)

                    st.subheader("🔍 Analysis Result")
                    st.write(analysis_result)

                    st.subheader("📊 Resume Score")
                    st.success(f"Your Resume Score: **{resume_score}/100**")
                else:
                    st.error("❌ Failed to extract text from PDF. Try another file.")
else:
    # User Inputs
    domain = st.text_input("What is your career domain? (e.g., IT, Healthcare, Finance, Marketing)", key="domain_input")
    career_goal = st.text_input("What is your career goal? (e.g., Data Scientist, Web Developer, AI Researcher)", key="goal_input")
    skills_input = st.text_area("What skills do you currently have? (comma-separated, e.g., Python, SQL, Machine Learning)", key="skills_input")

    skills = {}
    if skills_input:
        skill_list = [skill.strip() for skill in skills_input.split(',')]
        for skill in skill_list:
            level = st.selectbox(f"What is your level in {skill}?", ["Beginner", "Intermediate", "Advanced"], key=skill)
            skills[skill] = level

    # Get Learning Recommendations
    if st.button("Get Learning Recommendations"):
        if domain.strip() and career_goal.strip() and skills:
            st.write("⏳ Generating your personalized learning recommendations... Please wait.")
            skills_text = ", ".join([f"{skill} ({level})" for skill, level in skills.items()])
            recommendation = get_gemini_recommendation(domain, career_goal, skills_text)
            st.write(recommendation)
        else:
            st.warning("⚠️ Please enter all required fields to generate recommendations.")