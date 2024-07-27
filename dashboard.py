import toml
import streamlit as st
import firebase_admin
from firebase_admin import credentials, db
import pandas as pd
import matplotlib.pyplot as plt

# Initialize Firebase only if it has not been initialized
def initialize_firebase():
    if not firebase_admin._apps:
        fb_credentials = st.secrets["firebase"]['my_project_settings']
        cred = credentials.Certificate(fb_credentials)
        firebase_admin.initialize_app(cred, {
            'databaseURL': 'https://nitsgms-default-rtdb.firebaseio.com/'
        })

# Streamlit app
st.title("NIT Silchar Grievance Management System - Admin Dashboard")

# Initialize Firebase
initialize_firebase()

# Fetch complaints from Firebase
def fetch_complaints():
    ref = db.reference('complaints')
    return ref.get()

# Display complaints in a table
def display_complaints(complaints):
    if complaints:
        df = pd.DataFrame.from_dict(complaints, orient='index')
        st.dataframe(df)
    else:
        st.write("No complaints found.")

# Display analytics
def display_analytics(complaints):
    if complaints:
        df = pd.DataFrame.from_dict(complaints, orient='index')
        status_counts = df['status'].value_counts()
        
        st.subheader("Complaints Status Distribution")
        st.bar_chart(status_counts)
        
        st.subheader("Complaints Over Time")
        df['timestamp'] = pd.to_datetime(df['timestamp'])
        df.set_index('timestamp', inplace=True)
        complaints_over_time = df.resample('M').size()
        st.line_chart(complaints_over_time)
    else:
        st.write("No complaints to analyze.")

# Main function
def main():
    st.sidebar.title("Dashboard")
    page = st.sidebar.selectbox("Select a page", ["Complaints", "Analytics","Document Uploader"])
    
    complaints = fetch_complaints()
    
    if page == "Complaints":
        st.header("Complaints Management")
        display_complaints(complaints)
    elif page == "Analytics":
        st.header("Complaints Analytics")
        display_analytics(complaints)
    elif page == "Document Uploader":
        st.header("Document Uploader")
        st.write('Document Upload for RAG pipeline of chatbot')
        uploaded_file = st.file_uploader("Choose a PDF file", type="pdf")

        if uploaded_file is not None:
            st.success("Uploaded successfully!")


if __name__ == "__main__":
    main()
