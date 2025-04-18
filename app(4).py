import streamlit as st
from pdfminer.high_level import extract_text
import re
import pandas as pd

# Function to extract information from the resume
def extract_resume_info(text):
    name = extract_name(text)
    email = extract_email_addresses(text)
    phone = extract_phone_number(text)
    education = extract_qualification(text)
    skills = extract_skills(text)
    return {
        'Name': name,
        'Email': email,
        'Phone': phone,
        'Education': education,
        'Skills': skills,
    }

# Function to extract name from text
def extract_name(text):
    pattern = r'Name\s*:\s*(\w+)\s*'
    match = re.search(pattern, text)
    return match.group(1) if match else None

# Function to extract email addresses from text
def extract_email_addresses(text):
    r = re.compile(r'[\w\.-]+@[\w\.-]+')
    emails = r.findall(text)
    cleaned_emails = [re.sub(r'[^\w\s@.-]', '', email) for email in emails]
    return cleaned_emails

# Function to extract phone number from text
def extract_phone_number(text):
    r = re.compile(r'(?:(?:\+?([1-9]|[0-9][0-9]|[0-9][0-9][0-9])\s*(?:[.-]\s*)?)?(?:\(\s*([2-9]1[02-9]|[2-9][02-8]1|[2-9][02-8][02-9])\s*\)|([0-9][1-9]|[0-9]1[02-9]|[2-9][02-8]1|[2-9][02-8][02-9]))\s*(?:[.-]\s*)?)?([2-9]1[02-9]|[2-9][02-9]1|[2-9][02-9]{2})\s*(?:[.-]\s*)?([0-9]{4})(?:\s*(?:#|x\.?|ext\.?|extension)\s*(\d+))?')
    match = r.findall(text)
    if match:
        cleaned_numbers = []
        for m in match[0]:
            if m:
                cleaned_numbers.append(''.join([c for c in m if c.isdigit()]))
        return '-'.join(cleaned_numbers)
    else:
        return None

# Function to extract qualification from text
def extract_qualification(text):
    pattern = r'Qualification:\s*(.*?)Skills\s*:'
    match = re.search(pattern, text, re.DOTALL)
    return match.group(1).strip() if match else None

# Function to extract skills from text
def extract_skills(text):
    pattern = r'Skills\s*:\s*(.*?)Personal details\s*:'
    match = re.search(pattern, text, re.DOTALL)
    return [skill.strip() for skill in match.group(1).split('\n') if skill.strip()] if match else None

# Main function to run the Streamlit app
def main():
    st.title("Resume Parser")

    # Upload a file
    uploaded_file = st.file_uploader("Upload a resume", type=["pdf"])

    if uploaded_file is not None:
        # Extract text from the uploaded PDF
        text = extract_text(uploaded_file)
        if text:
            # Extract information from the resume
            resume_info = extract_resume_info(text)

            # Display the extracted information
            st.subheader("Extracted Information")
            st.write(resume_info)

            # Save the information to a CSV file
            st.subheader("Save Extracted Information")
            if st.button("Save as CSV"):
                df = pd.DataFrame([resume_info])
                df.to_csv('extracted_resume_info.csv', index=False)
                st.success("Information saved to extracted_resume_info.csv")

if __name__ == "__main__":
    main()
