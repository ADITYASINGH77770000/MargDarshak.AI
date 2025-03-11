import streamlit as st
import pymongo
# from collections.abc import MutableMapping

# MongoDB Atlas Connection String 
MONGO_URI = "mongodb+srv://anubhavyadav77ff:anubhav123@cluster0.wimg7.mongodb.net/?retryWrites=true&w=majority&appName=Cluster0"
DATABASE_NAME = "user_feedback"
COLLECTION_NAME = "feedback"

# Connect to MongoDB
client = pymongo.MongoClient(MONGO_URI)
db = client[DATABASE_NAME]
collection = db[COLLECTION_NAME]

st.header("📝Feedback", divider='rainbow')

with st.form("feedback_form"):
    name = st.text_input("Full Name*", value=None, placeholder="John Doe")
    email = st.text_input("Email*", value=None, placeholder="johndoe@gmail.com")
    rating = st.slider("Rating*", min_value=1, max_value=5, value=3)
    easy_to_use = st.selectbox("Easy to Use*", options=["Yes", "No", "Somewhat"], help="Select if the application is easy to use")
    challenges = st.text_area("Challenges Faced*", help="Enter the challenges faced by you", value=None, placeholder=None)
    general_feedback = st.text_area("Any other feedback", help="Enter any other feedback", value=None)
    st.markdown("**Required*")
    submit = st.form_submit_button("Submit")

if submit:
    if not name or not email or not rating or not easy_to_use or not challenges:
        st.error("Please fill all the required fields.")
        st.stop()
    else:
        feedback_document = {
            "Name": name,
            "Email": email,
            "Rating": rating,
            "Easy to Use": easy_to_use,
            "Challenges": challenges,
            "General Feedback": general_feedback
        }
        collection.insert_one(feedback_document)
        st.success("Thank you for your feedback! Your response has been recorded in MongoDB.") 