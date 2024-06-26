import streamlit as st
from twilio.rest import Client
import firebase_admin
from firebase_admin import credentials, firestore, db
from datetime import datetime


st.set_page_config(page_title="Fire Detection")

# Twilio credentials
account_sid = 'AC9d3be93a105dd809ee11e2d2f32f0571'
auth_token = 'e5040c862d33b765acf68a2a5df4e330'
twilio_number = '+14149397542'


current_datetime = datetime.now()
# Function to send SMS
def send_sms(to, message):
    client = Client(account_sid, auth_token)
    try:
        message = client.messages.create(
            body=message,
            from_=twilio_number,
            to=to
        )
        return True, message.sid
    except Exception as e:
        return False, str(e)

# Check if Firebase app is already initialized
if not firebase_admin._apps:
    # Initialize Firebase Admin SDK
    cred = credentials.Certificate("firedetectionsettings.json")
    firebase_admin.initialize_app(cred, {
    'databaseURL': 'https://projectdesignprototype-855f8-default-rtdb.asia-southeast1.firebasedatabase.app/'
})


# Get Firestore client
db = firestore.client()


# Title of the main page0
st.title("Phone Number Storage App")

tab1, tab2 = st.tabs(["Add Contact", "SMS"])

with tab1:
    # Sidebar section for adding a phone number
    st.title("Add phone number")
    phone_number = st.text_input("Enter phone number:")
    if st.button("Add Contact"):
        # Add data to an existing document in Firestore
        data = {"Contact": phone_number}
        # Specify the document ID ("Detection") where you want to append the data
        detection_ref = db.collection("Fire").document("Contacts")
        detection_ref.update(data)
        st.success("Data appended successfully to the specific document!")

with tab2:
    # Display Firestore data for Fire/Detection document
    st.subheader("SMS notification")

    # Specify the document ID ("Contacts") from which you want to retrieve data
    contact_ref = db.collection("Fire").document("Contacts")
    # Get the document snapshot
    contact_snapshot = contact_ref.get()
    
    # Check if the document exists
    if contact_snapshot.exists:
        # Retrieve data from the document
        contact_data = contact_snapshot.to_dict()
        st.success("Data retrieved successfully!")
        # Display the retrieved data
        st.write("Contact:", contact_data.get("Contact", "No contact found"))
    else:
        st.warning("Document does not exist!")
        
    if st.button("Send SMS Notification"):
        message = "Fire Detected! "
        success, sid = send_sms(contact_data.get("Contact", "No contact found"), message)
        if success:
            st.success("SMS sent successfully! SID: {}".format(sid))
        else:
            st.error("Failed to send SMS. Error: {}".format(sid))
       


