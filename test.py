import streamlit as st
import supabase
from datetime import datetime

# Replace with your Supabase project URL and API key
supabase_url = "https://nyglkiudiuejsjtuvkdk.supabase.co"
supabase_key = "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJpc3MiOiJzdXBhYmFzZSIsInJlZiI6Im55Z2xraXVkaXVlanNqdHV2a2RrIiwicm9sZSI6ImFub24iLCJpYXQiOjE3MDY0NTMwOTAsImV4cCI6MjAyMjAyOTA5MH0.wrXwCZR2eqeEch-ZK0ZKWzaCgp2tbQIMMQzJckraxXU"

# Connect to Supabase
supabase_client = supabase.create_client(supabase_url, supabase_key)

# Specify the table name (replace 'Streamlit_base' with your actual table name)
table_name = 'Streamlit'

# Streamlit App
st.title('Welcome to :black[USD/KES Analysis App]')
choice = st.selectbox('Login/Sign_Up', ['Login', 'Sign_Up'])

if choice == 'Login':
    email = st.text_input('Enter Email Address')
    password = st.text_input('Password', type='password')
    
    if st.button('Login'):
        # Perform login logic with Supabase
        # Check if the user exists in the specified table
        user_query = supabase_client.table(table_name).select().eq('email', email).execute()
        
        # Display the result
        st.write('User Query Result:', user_query)

else:
    email = st.text_input('Enter Email Address')
    password = st.text_input('Password', type='password')
    username = st.text_input('Enter your unique Username')
    
    if st.button("Create My Account"):
        # Perform user registration logic with Supabase
        # Insert a new user into the specified table
        new_user = {
            'email': email,
            'password': password,
            'username': username,
            'created_at': datetime.utcnow()
        }
        
        try:
            # Attempt to insert the new user
            user_insert = supabase_client.table(table_name).upsert([new_user])
            st.write('User Insert Result:', user_insert)
        except Exception as e:
            # Handle any exceptions (you can print or log the exception for debugging)
            st.write(f'Error: {e}')
            st.write('User already exists. Please log in or use a different email.')
