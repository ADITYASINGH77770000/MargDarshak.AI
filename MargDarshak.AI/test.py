import streamlit as st
import pandas as pd

# Page Title
st.title("📊 User Progress Dashboard")

# Initialize session state for progress tracking
if "completed_tasks" not in st.session_state:
    st.session_state.completed_tasks = {}

# User Inputs
st.sidebar.header("📝 User Details")
user_name = st.sidebar.text_input("Enter your name", placeholder="John Doe")
career_goal = st.sidebar.text_input("Career Goal", placeholder="e.g., Data Scientist")
learning_duration = st.sidebar.slider("Expected Completion Time (Months)", 1, 12, 6)

st.sidebar.markdown("---")

# Sample Learning Roadmap
st.subheader(f"📌 {user_name}'s Learning Roadmap")
roadmap_data = {
    "Task": ["Learn Python", "Complete SQL Basics", "Build a Data Science Project", "Learn Machine Learning", "Apply for Internships"],
    "Status": ["Not Started", "In Progress", "Completed", "Not Started", "Not Started"]
}

df = pd.DataFrame(roadmap_data)

# Checkbox for task completion tracking
st.subheader("✅ Task Completion Tracker")
for task in roadmap_data["Task"]:
    checked = st.checkbox(task, value=st.session_state.completed_tasks.get(task, False))
    st.session_state.completed_tasks[task] = checked

# Calculate progress percentage
completed_count = sum(st.session_state.completed_tasks.values())
total_tasks = len(roadmap_data["Task"])
progress_percentage = int((completed_count / total_tasks) * 100)

# Display Progress Bar
st.subheader("📊 Progress Overview")
st.progress(progress_percentage / 100)
st.write(f"**{progress_percentage}% completed**")

# Learning Insights
st.subheader("📈 Learning Insights")
col1, col2 = st.columns(2)
col1.metric("Total Tasks", total_tasks)
col2.metric("Completed Tasks", completed_count)

# Encouragement Message
if progress_percentage == 100:
    st.success("🎉 Congratulations! You've completed your learning roadmap!")
elif progress_percentage > 50:
    st.info("🚀 Keep going! You're more than halfway there!")
else:
    st.warning("📚 Keep learning! Every step counts.")

# Data Persistence (Optional: Save Progress)
if st.button("Save Progress"):
    st.success("✅ Your progress has been saved!")

