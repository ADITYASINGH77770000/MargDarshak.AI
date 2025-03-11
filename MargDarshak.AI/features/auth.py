import streamlit as st
import yaml
from yaml.loader import SafeLoader
from streamlit_authenticator.utilities import Hasher, LoginError
import streamlit_authenticator as stauth
import pandas as pd
import os
import pymongo
# from collections.abc import MutableMapping

# MongoDB Atlas Connection String 
MONGO_URI = "mongodb+srv://anubhavyadav77ff:anubhav123@cluster0.wimg7.mongodb.net/?retryWrites=true&w=majority&appName=Cluster0"
DATABASE_NAME = "user_data"
COLLECTION_NAME = "users"
CSV_FILE = "user_data.csv"

# Connect to MongoDB
client = pymongo.MongoClient(MONGO_URI)
db = client[DATABASE_NAME]
collection = db[COLLECTION_NAME]

# Loading config file
with open('config.yaml', 'r', encoding='utf-8') as file:
    config = yaml.load(file, Loader=SafeLoader)

# Initialize session state for register page
if 'register' not in st.session_state:
    st.session_state['register'] = False
if 'authentication_status' not in st.session_state:
    st.session_state['authentication_status'] = None
if 'user_data' not in st.session_state:
    st.session_state['user_data'] = {}

def show_login_form():
    # Creating the authenticator object
    authenticator = stauth.Authenticate(
        config['credentials'],
        config['cookie']['name'],
        config['cookie']['key'],
        config['cookie']['expiry_days'],
    )
    
    # Creating a login widget
    try:
        authenticator.login()
    except LoginError as e:
        st.error(e)
    
    if st.session_state["authentication_status"]:
        authenticator.logout('Logout', "sidebar")
        st.sidebar.write(f'Welcome **{st.session_state["name"]}**👋')
        # Extract user data
        username = st.session_state["username"]
        user_data = config['credentials']['usernames'].get(username, {})
        st.session_state["user_data"] = user_data
    elif st.session_state["authentication_status"] is False:
        st.error('Username/password is incorrect')
    elif st.session_state["authentication_status"] is None:
        st.warning('Please enter your username and password')

    # Only show the "Register" button if the user is NOT logged in
    if st.session_state["authentication_status"] is None or st.session_state["authentication_status"] == False:
        st.write("---")
        if st.button("Register"):
            st.session_state['register'] = True  # Switch to register page

# Define function to show the register form
def show_register_form():
    with st.container():
        st.write("## Register")
        st.divider()
        new_username = st.text_input("Enter Username")
        new_name = st.text_input("Enter Your Full Name")
        new_password = st.text_input("Enter Password", type="password")
        new_email = st.text_input("Enter your email")
        preferred_lang = st.selectbox("Preferred Language",  ["English","Japanese","Korean","Arabic","Bahasa Indonesia","Bengali","Bulgarian","Chinese (Simplified)","Chinese (Traditional)",
                                                            "Croatian","Czech","Danish","Dutch","Estonian","Farsi","Finnish","French","German","Gujarati","Greek","Hebrew","Hindi","Hungarian","Italian","Kannada","Latvian",
                                                            "Lithuanian","Malayalam","Marathi","Norwegian","Polish","Portuguese","Romanian","Russian","Serbian","Slovak","Slovenian","Spanish","Swahili","Swedish","Tamil",
                                                            "Telugu","Thai","Turkish","Ukrainian","Urdu","Vietnamese"])

        if st.button("Submit Registration"):
            if new_username and new_password and new_email:
                # Hash the new password
                hashed_password = Hasher([new_password]).hash(new_password)
                if 'credentials' not in config:
                    config['credentials'] = {}
                if 'usernames' not in config['credentials']:
                    config['credentials']['usernames'] = {}
                    
                # Update the config dictionary
                config['credentials']['usernames'][new_username] = {
                    'name': new_name,
                    'password': hashed_password,
                    'email': new_email,
                    'preferred_lang': preferred_lang,
                }
            
                # Save the updated credentials to the config.yaml file
                with open('config.yaml', 'w') as file:
                    yaml.dump(config, file)
                
                new_data = pd.DataFrame([[new_username, new_name, new_email, preferred_lang]], columns=["Username", "Name", "Email", "Language"])
                if os.path.exists(CSV_FILE):
                    existing_data = pd.read_csv(CSV_FILE)
                    updated_data = pd.concat([existing_data, new_data], ignore_index=True)
                else:
                    updated_data = new_data
                updated_data.to_csv(CSV_FILE, index=False)
                
                user_document = {"Username":new_username, "Name": new_name, "Email": new_email, "Language": preferred_lang}
                collection.insert_one(user_document)
                
                st.success("User registered successfully! You can now log in.")
            
            # Add a "Back to Login" button to return to the login page
    if st.button("Back to Login"):
        st.session_state['register'] = False  # Return to login page

# Main section: Show either login or register form based on state
def authentication():
    if st.session_state['register']:
        show_register_form()  # Show register form
    else:
        show_login_form()  # Show login form

# Get user details
def get_user_details():
    return st.session_state.get("user_data", {})