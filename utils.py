import os
import re
import sys
import time
import random
import string
import tempfile

import zipfile
import pdfplumber
import unicodedata
import pandas as pd
from docx import Document
from datetime import datetime
from io import BytesIO, StringIO
import google.generativeai as genai
from google.api_core.exceptions import ResourceExhausted

original_stdout = sys.stdout
sys.stdout = StringIO()

def extract_info_details_name(candidate_details_raw):
    name_match = re.search(r"(?i)name[:\s]*([A-Za-z\s]+)", candidate_details_raw)
    return name_match.group(1).strip() if name_match else None

def extract_info_details_email(candidate_details_raw):
    email_match = re.search(r"(?i)email[:\s]*([\w\.-]+@[\w\.-]+)", candidate_details_raw)
    return email_match.group(1).strip() if email_match else None

def extract_info_details_phone(candidate_details_raw):
    phone_match = re.search(r"(?i)phone[:\s]*([\(\+\)\d\s-]+)", candidate_details_raw)
    return phone_match.group(1).strip() if phone_match else None

def get_model():
    genai.configure(api_key=os.getenv("GEMINI_API_KEY"))
    return genai.GenerativeModel('gemini-1.5-flash')

def get_prompt(text, description):
    return f"""
    You are a skilled ATS (Applicant Tracking System) scanner with a deep understanding of ATS functionality. 
    Evaluate the given resume against the provided job description and provide a match score. The output should be a single number representing the percentage match without the % symbol, based on the following criteria:

    - If the resume is empty or not valid, return 0.
    - If the resume does not fit the job description at all (i.e., no relevant skills or experience), return 0.
    - If the resume partially matches the job description, calculate a percentage match based on the overlap of required skills, experience, and qualifications.
    - If the resume fully matches the job description, return a percentage close to 100.

    Provide only a single number as the output. Do not include any additional text or explanations.

    Job Description:
    {description}

    Resume:
    {text}
    """

def get_candidate_info_prompt(text):
    return f"""
    Extract the candidate's name, email, and phone number from the following resume text.
    Anything happens the format should strictly be like this the format "Name: ..., Email: ..., Phone: ...

    Resume Text:
    {text}
    """

def make_text_plain(text):
    try:
        text = unicodedata.normalize('NFKD', text)
        text = text.lower().title()
        text = re.sub(r'\s+', ' ', text)
        text = re.sub(r'[^\w\s]', '', text)
        if text:
            return text.strip()
        return text
    except Exception as e:
        print(e)
        return ""

def pdf_to_text(pdf_path):
    text = ''
    try:
        with pdfplumber.open(pdf_path) as pdf:
            for page in pdf.pages:
                text += page.extract_text()
        return text
    except Exception as e:
        return text
    
def file_to_text(file):
    pdf_content = None
    if file.name.endswith(".pdf"):
        pdf_content = pdf_to_text(file)
    elif file.name.endswith(".docx"):
        pdf_content = docx_to_text(file)
    return pdf_content

def docx_to_text(docx_path):
    text = ''
    try:
        doc = Document(docx_path)
        for para in doc.paragraphs:
            text += para.text + '\n'
        return text
    except Exception as e:
        print(f"Error reading DOCX {docx_path.name}: {e}")
        return text

def get_candidate_info(resume):
    try:
        prompt = get_candidate_info_prompt(resume)
        response = get_model().generate_content(prompt)
        if response and response.text:
            return response.text.strip()
        return ""
    except Exception as e:
        print(e)
        return ""

def get_ats_score_deprecated(prompt):
    try:
        response = get_model().generate_content(prompt)
        return int(response.text.strip())
    except Exception as e:
        return 0
    
def rate_limit(delay=1):
    def decorator(func):
        def wrapper(*args, **kwargs):
            time.sleep(delay)
            return func(*args, **kwargs)
        return wrapper
    return decorator

@rate_limit(delay=1)
def get_ats_score(prompt, file_name, retries=10, delay=5):
    print(f"Processing {file_name}")
    attempt = 0
    while attempt < retries:
        try:
            response = get_model().generate_content(prompt)
            if response and response.text:
                return int(response.text.strip())
        except ResourceExhausted:
            print(f"API quota exhausted. Waiting for {delay} seconds before retrying...")
            time.sleep(delay)
            attempt += 1
        except Exception as e:
            print(f"An error occurred: {e}")
            return 0
    print(f"Exceeded maximum retries for {file_name}. Returning 0.")
    return 0

def get_day_month_year():
    return datetime.now().strftime("%d-%m-%Y")

def create_zip_file(resumes):
    try:
        zip_buffer = BytesIO()
        with zipfile.ZipFile(zip_buffer, "w", zipfile.ZIP_DEFLATED) as zip_file:
            for resume in resumes:
                resume_file = resume["ResumeFile"]
                resume_file.seek(0)  
                zip_file.writestr(resume["Resume"], resume_file.read())
        zip_buffer.seek(0)
        return zip_buffer
    except Exception as e:
        print("Error while zipping resumes", e)
        return None

def get_csv(results):
    csv_path = ""
    try:
        df = pd.DataFrame(results)
        with tempfile.NamedTemporaryFile(delete=False, suffix='.csv', mode='w', newline='') as tmp_file:
            df.to_csv(tmp_file.name, index=False)
            csv_path = tmp_file.name
        return csv_path
    except Exception as e:
        print(e)
        return csv_path

def generate_random_string(length=16):
    characters = string.ascii_letters + string.digits
    random_string = ''.join(random.choice(characters) for _ in range(length))
    return random_string
