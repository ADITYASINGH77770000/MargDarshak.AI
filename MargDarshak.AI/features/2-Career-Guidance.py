#JOB TRACKER
import streamlit as st
import pandas as pd
import plotly.express as px
import requests
import os
import re
import google.generativeai as genai
from dotenv import load_dotenv

# Load API Keys
load_dotenv()
# RAPIDAPI_KEY = os.getenv("RAPIDAPI_KEY")
RAPIDAPI_KEY = st.secrets["RAPIDAPI_KEY"]
# GEMINI_API_KEY = os.getenv("GEMINI_API_KEY")
GEMINI_API_KEY = st.secrets["GOOGLE_API_KEY"]

# Configure Gemini AI
genai.configure(api_key=GEMINI_API_KEY)

# API Configuration
RAPIDAPI_HOST = "jsearch.p.rapidapi.com"

st.header("🚀 AI-Powered Career & Skill Trends", divider="rainbow")
st.write("🔍 Discover trending skills, salary insights & career recommendations")

career_domain = st.selectbox("Select Career Domain:", ["Data Science", "AI & ML", "Cybersecurity", "Web Development"])

# Fetch Job Listings
def fetch_jobs(domain):
    url = "https://jsearch.p.rapidapi.com/search"
    headers = {"X-RapidAPI-Key": RAPIDAPI_KEY, "X-RapidAPI-Host": RAPIDAPI_HOST}
    params = {"query": domain, "page": "1", "num_pages": "1"}

    response = requests.get(url, headers=headers, params=params)
    if response.status_code == 200:
        jobs = response.json().get("data", [])
        return pd.DataFrame(jobs)
    else:
        st.error("Failed to fetch job listings")
        return pd.DataFrame()

# Extract Skills Automatically
def extract_skills(job_desc):
    skills = re.findall(r"\b(Python|SQL|AWS|TensorFlow|Cloud Computing|Cybersecurity|JavaScript|React|AI|Docker)\b", job_desc, re.IGNORECASE)
    return skills

# Estimate Salary (if missing)
def estimate_salary(description):
    numbers = re.findall(r"\$\d{2,}", description)
    if numbers:
        min_salary = int(numbers[0].replace("$", "").replace(",", ""))  # First found salary
        max_salary = min_salary * 1.5  # Estimate max salary
    else:
        min_salary = 50000  # Default min salary
        max_salary = 100000  # Default max salary
    return min_salary, max_salary

# Gemini AI Insights
def get_gemini_insights(domain, top_skills):
    prompt = f"""
    The latest job market trends show high demand for {domain}.
    Top trending skills: {', '.join(top_skills)}.

    Predict:
    1. Average salary range
    2. Best certifications to learn these skills
    3. Top companies hiring
    """
    model = genai.GenerativeModel("gemini-1.5-flash")
    response = model.generate_content(prompt)
    return response.text

# Plotting Line Chart for Skills
def plot_skills_trend(skills_count):
    skills_df = pd.DataFrame({"Skill": skills_count.index, "Count": skills_count.values})
    fig = px.line(skills_df, x="Skill", y="Count", markers=True, title="📈 Skill Demand Over Time")
    st.plotly_chart(fig, use_container_width=True)

# Column Chart for Jobs vs Salary
def plot_jobs_vs_salary(jobs_df):
    fig = px.bar(jobs_df, x="job_title", y="estimated_max_salary", color="employer_name",
                 title="💰 Job Titles vs Estimated Salary", text_auto=True)
    st.plotly_chart(fig, use_container_width=True)

if st.button("Fetch Job Trends"):
    with st.spinner("Fetching Jobs..."):
        jobs_data = fetch_jobs(career_domain)
        if not jobs_data.empty:
            st.dataframe(jobs_data[["job_title", "employer_name", "job_description"]].head(10))

            # Extract skills from job descriptions
            all_skills = []
            min_salaries = []
            max_salaries = []
            salary_ranges = []

            for desc in jobs_data["job_description"]:
                all_skills.extend(extract_skills(desc))
                min_salary, max_salary = estimate_salary(desc)
                min_salaries.append(min_salary)
                max_salaries.append(max_salary)
                salary_ranges.append(f"${min_salary} - ${max_salary}")

            jobs_data["estimated_min_salary"] = min_salaries
            jobs_data["estimated_max_salary"] = max_salaries
            jobs_data["estimated_salary_range"] = salary_ranges

            skill_counts = pd.Series(all_skills).value_counts().head(5)

            st.subheader("📊 Skill Demand Over Time")
            plot_skills_trend(skill_counts)

            st.subheader("💰 Salary Insights (Estimated)")
            plot_jobs_vs_salary(jobs_data)

            st.subheader("🔮 AI Insights")
            ai_response = get_gemini_insights(career_domain, skill_counts.index.tolist())
            st.write(ai_response)
        else:
            st.error("No job data found")