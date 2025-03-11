# Speaker
import os
import streamlit as st
import pyttsx3
import speech_recognition as sr
import google.generativeai as genai

GEMINI_API_KEY = st.secrets["GOOGLE_API_KEY"]
genai.configure(api_key=GEMINI_API_KEY)

# Initialize Text-to-Speech Engine
def speak_text(text):
    engine = pyttsx3.init()
    engine.say(text)
    engine.runAndWait()

# Speech Recognition Function (30s Limit)
def transcribe_speech():
    recognizer = sr.Recognizer()
    with sr.Microphone() as source:
        recognizer.adjust_for_ambient_noise(source, duration=2)
        st.info("Listening... Speak now!")
        try:
            audio = recognizer.listen(source, timeout=30)
            text = recognizer.recognize_google(audio)
            return text
        except sr.WaitTimeoutError:
            return "Timeout: No speech detected. Please try again."
        except sr.UnknownValueError:
            return "Sorry, I couldn't understand your speech."
        except sr.RequestError:
            return "Speech recognition service is unavailable."

# Generate Interview Questions
def generate_questions(domain, level):
    prompt = f"""
    You are an expert interviewer. Generate exactly 4 technical interview questions for a {level} level candidate applying for {domain}.
    Each question should be concise and within 200 words.
    Format:
    Q1: <question>
    Q2: <question>
    Q3: <question>
    Q4: <question>
    """
    model = genai.GenerativeModel('gemini-1.5-flash')
    response = model.generate_content(prompt)

    if response and response.text:
        lines = response.text.strip().split("\n")
        questions = [line.split(": ")[1] for line in lines if ": " in line]
        return ["Introduce yourself"] + questions[:4] if len(questions) >= 4 else None
    return None

# AI-Powered Answer Evaluation
def evaluate_answers(answers):
    combined_answers = "\n".join(answers)
    prompt = f"""
    You are an AI interview coach. Analyze the candidate's responses:
    {combined_answers}
    - Identify strengths and weaknesses.
    - Highlight missing skills.
    - Assess confidence and tone (e.g., nervous, confident, hesitant).
    - Provide 3 improvement suggestions.
    Keep the response concise and within 1000 words.
    """
    model = genai.GenerativeModel('gemini-1.5-flash')
    response = model.generate_content(prompt)
    return response.text[:1000] if response and response.text else "AI evaluation failed."

# Streamlit UI Setup
st.header("🎙️ AI-Powered Mock Interview", divider='rainbow')
st.write("Practice your interview skills with AI-powered real-time feedback!")

domain = st.selectbox("Choose Your Domain:", ["Data Science", "AI Engineer", "Software Development", "Finance", "Marketing"])
level = st.selectbox("Select Interview Level:", ["Beginner", "Intermediate", "Advanced"])

stop_interview = False  # Flag to stop interview
if st.button("Start Mock Interview"):
    questions = generate_questions(domain, level)
    if not questions:
        st.error("Failed to generate questions. Try again!")
    else:
        st.subheader("📌 AI Interview Questions")
        answers = []
        stop_button = st.button("Stop Interview")  # Stop button

        for i, question in enumerate(questions, 1):
            if stop_button:
                st.warning("Interview stopped by user.")
                break  # Exit loop

            st.write(f"**Q{i}:** {question}")
            speak_text(question)

            st.subheader("🗣️ Speak your answer (30 sec max)...")
            answer = transcribe_speech()

            if "stop interview" in answer.lower():
                st.warning("Interview stopped by user.")
                break  # Exit loop

            st.write(f"💬 Your Answer: {answer}")
            answers.append(answer)

        if answers:
            st.subheader("📊 AI Feedback on Your Performance")
            feedback = evaluate_answers(answers)
            st.write(feedback)
            speak_text(feedback)