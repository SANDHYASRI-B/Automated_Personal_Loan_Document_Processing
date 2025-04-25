!pip install streamlit 
!pip install pytesseract
import pytesseract
import cv2
import numpy as np
import re
import streamlit as st

from PIL import Image

# Function to preprocess the image
def preprocess_image(image):
    gray = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)
    blurred = cv2.GaussianBlur(gray, (5, 5), 0)
    _, thresh = cv2.threshold(blurred, 0, 255, cv2.THRESH_BINARY + cv2.THRESH_OTSU)
    return thresh

# Function to extract text using OCR
def extract_text(image):
    text = pytesseract.image_to_string(image)
    return text

# Function to extract key fields from the text
def extract_key_fields(text):
    name = re.search(r'Name:\s*(.*)', text)
    address = re.search(r'Address:\s*(.*)', text)
    income = re.search(r'Income:\s*\$?(\d+)', text)
    loan_amount = re.search(r'Loan Amount:\s*\$?(\d+)', text)
    
    return {
        'name': name.group(1) if name else None,
        'address': address.group(1) if address else None,
        'income': income.group(1) if income else None,
        'loan_amount': loan_amount.group(1) if loan_amount else None
    }

# Function to validate extracted data
def validate_data(data):
    if not data['name'] or not data['address']:
        return False
    if not data['income'].isdigit() or not data['loan_amount'].isdigit():
        return False
    return True

# Streamlit UI
st.title("Automated Personal Loan Document Processing")

# Upload Document
uploaded_file = st.file_uploader("Upload a personal loan document (image format)", type=["jpg", "jpeg", "png"])

if uploaded_file is not None:
    # Load the image
    image = Image.open(uploaded_file)
    image_cv = cv2.cvtColor(np.array(image), cv2.COLOR_RGB2BGR)
    
    # Preprocess the image
    preprocessed_image = preprocess_image(image_cv)
    
    # Extract text from the image
    text = extract_text(preprocessed_image)
    
    # Extract key fields
    key_fields = extract_key_fields(text)
    
    # Display extracted data
    st.subheader("Extracted Data:")
    st.write(key_fields)
    
    # Validate data
    if validate_data(key_fields):
        st.success("Data is valid!")
    else:
        st.error("Data validation failed. Please check the extracted fields.")

    # Option for manual correction
    st.subheader("Manual Correction")
    name = st.text_input("Name", value=key_fields['name'])
    address = st.text_input("Address", value=key_fields['address'])
    income = st.text_input("Income", value=key_fields['income'])
    loan_amount = st.text_input("Loan Amount", value=key_fields['loan_amount'])

    if st.button("Submit"):
        corrected_data = {
            'name': name,
            'address': address,
            'income': income,
            'loan_amount': loan_amount
        }
        if validate_data(corrected_data):
            st.success("Corrected data is valid!")
            # Here you can add code to integrate with the bank's loan processing system
        else:
            st.error("Corrected data validation failed. Please check the fields.")
