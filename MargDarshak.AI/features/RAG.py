import streamlit as st
import pandas as pd
import faiss
import numpy as np
import os
from dotenv import load_dotenv
from sentence_transformers import SentenceTransformer
import google.generativeai as genai

# Load environment variables
load_dotenv()
# GOOGLE_API_KEY = os.getenv("GOOGLE_API_KEY")
GOOGLE_API_KEY = st.secrets["GOOGLE_API_KEY"]

# Load the dataset
df = pd.read_csv("features/data/dataset.csv")

# Prepare the text corpus
corpus = (df["Course Name"] + " " + df["Course Difficulty"] + " " + df.get("Syllabus & Content Quality", "")).tolist()

# Load embedding model
model = SentenceTransformer("all-MiniLM-L6-v2")
embeddings = np.array(model.encode(corpus, convert_to_numpy=True))

# Create FAISS index
d = embeddings.shape[1]
index = faiss.IndexFlatL2(d)
index.add(embeddings)

# Configure Gemini API
genai.configure(api_key=GOOGLE_API_KEY)

def retrieve_courses(query, top_n=3):
    """Retrieve top N relevant courses using FAISS."""
    query_embedding = np.array(model.encode([query], convert_to_numpy=True))
    distances, indices = index.search(query_embedding, top_n)
    return df.iloc[indices[0]]

def safe_get(row, column_name, default="N/A"):
    """Safely get a column value, returning a default if the column is missing."""
    return row[column_name] if column_name in df.columns else default

def format_recommended_courses(courses):
    """Format recommended courses in a structured way."""
    return "\n\n".join([
        f"📌 *[{row['Course Name']}]({safe_get(row, 'Course URL')})*\n"
        f"- ⭐ *Rating:* {safe_get(row, 'Course Ratings')}\n"
        f"- ⏳ *Duration:* {safe_get(row, 'Course Duration')}"
        for _, row in courses.iterrows()
    ])

def generate_recommendation(query):
    """Use Gemini AI to generate a response with retrieved courses."""
    relevant_courses = retrieve_courses(query)
    course_info = format_recommended_courses(relevant_courses)
    
    prompt = f"""
    User Query: {query}
    
    Based on your preferences, here are some recommended courses:
    {course_info}
    
    Please provide a summary of these courses and suggest the best one based on user reviews and ratings.
    """
    
    model = genai.GenerativeModel("gemini-1.5-flash")
    response = model.generate_content(prompt)
    return response.text, course_info

# Streamlit UI
st.header("📚 Margdarshak.AI - Course Recommender", divider='rainbow')
query = st.text_input("Enter your learning preference:", placeholder="Data Science")
if st.button("Get Recommendations"):
    if query:
        with st.spinner("Fetching recommendations..."):
            recommendation, course_links = generate_recommendation(query)
            st.write("### Recommended Courses:")
            st.markdown(course_links, unsafe_allow_html=True)
            st.write("### AI Summary:")
            st.write(recommendation)
    else:
        st.warning("Please enter a query to get recommendations.")