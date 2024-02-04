import streamlit as st
from datetime import datetime
import firebase_admin
from firebase_admin import credentials
from firebase_admin import auth

# Check if Firebase app is already initialized
if not firebase_admin._apps:
    # Initialize Firebase app
    cred = credentials.Certificate('streamlit-database-ed78d-89b53795efa6.json')
    firebase_admin.initialize_app(cred)

st.title('Welcome to :black[USD/KES Analysis App]')
choice = st.selectbox('Login/Sign_Up', ['Login', 'Sign_Up'])
if choice == 'Login':
    email = st.text_input('Enter Email Address')
    password = st.text_input('Password', type='password')
    st.button('Login')

else:
    email = st.text_input('Enter Email Address')
    password = st.text_input('Password', type='password')
    username = st.text_input('Enter your unique Username')
    
    if st.button("Create My Account"):
        user = auth.create_user(email=email, password=password, uid=username)
        st.success('Account created successfully!')
        st.markdown('Please Login using your Email and Password')
