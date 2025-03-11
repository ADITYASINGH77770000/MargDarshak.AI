import streamlit as st
import pandas as pd
import os
import pymongo

# MongoDB Atlas Connection String 
MONGO_URI = "mongodb+srv://anubhavyadav77ff:anubhav123@cluster0.wimg7.mongodb.net/?retryWrites=true&w=majority&appName=Cluster0"
DATABASE_NAME = "user_data"
COLLECTION_NAME = "users"

# CSV file path
CSV_FILE = "user_data.csv"

# Connect to MongoDB
client = pymongo.MongoClient(MONGO_URI)
db = client[DATABASE_NAME]
collection = db[COLLECTION_NAME]

# Streamlit UI
st.title("User Registration Form")

# User Input Fields
name = st.text_input("Enter your Name")
email = st.text_input("Enter your Email")
age = st.number_input("Enter your Age", min_value=1, max_value=120, step=1)

# Submit Button
if st.button("Submit"):
    if name and email and age:
        # Create a DataFrame
        new_data = pd.DataFrame([[name, email, age]], columns=["Name", "Email", "Age"])

        # Check if CSV file exists
        if os.path.exists(CSV_FILE):
            existing_data = pd.read_csv(CSV_FILE)
            updated_data = pd.concat([existing_data, new_data], ignore_index=True)
        else:
            updated_data = new_data

        # Save to CSV
        updated_data.to_csv(CSV_FILE, index=False)

        # Store Data in MongoDB Atlas
        user_document = {"Name": name, "Email": email, "Age": age}
        collection.insert_one(user_document)

        # Success Message
        st.success(f"Registration successful for {name}! Data saved in CSV & MongoDB.")

    else:
        st.warning("Please fill in all fields.")