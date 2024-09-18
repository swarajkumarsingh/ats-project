import os
import shutil
import pdfplumber
import google.generativeai as genai
import time
from google.api_core.exceptions import ResourceExhausted

resume_dir = './resumes'
shortlist_dir = './short-listed-resumes'
genai.configure(api_key=os.getenv("GEMINI_API_KEY"))
model = genai.GenerativeModel('gemini-1.5-flash')

os.makedirs(shortlist_dir, exist_ok=True)

def pdf_to_text(pdf_path):
    text = ''
    with pdfplumber.open(pdf_path) as pdf:
        for page in pdf.pages:
            text += page.extract_text()
    return text

def get_description():
    return """
    Job Title: Technical Tester
    Salary: Up to 6 LPA

    Responsibilities:
    Execute manual and automated test cases
    Identify, report, and track software defects
    Collaborate with developers to resolve issues
    Create and maintain test documentation
    Participate in test planning and strategy development
    Analyse requirements for testability

    Requirements:
    Bachelor's degree in Computer Science or related field
    1-3 years of software testing experience
    Knowledge of testing methodologies and tools
    Basic programming skills (e.g., Python, Java)
    Familiarity with test automation frameworks
    Strong analytical and problem-solving abilities
    Excellent communication skills

    Preferred:
    Experience with Agile development methodologies
    Knowledge of database testing and SQL
    """

def get_pdf_path(resume_dir, resume_file):
    return os.path.join(resume_dir, resume_file)

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

def get_ats_percentage(prompt, retries=5, delay=5):
    attempt = 0
    while attempt < retries:
        try:
            response = model.generate_content(prompt)
            return response.text.strip()
        except ResourceExhausted:
            print(f"API quota exhausted. Waiting for {delay} seconds before retrying...")
            time.sleep(delay)
            attempt += 1
    print("Exceeded maximum retries. Skipping this resume.")
    return None

def get_resume_dir():
    try:
        return os.listdir(resume_dir)
    except Exception as e:
        return None

def main():
    resume_files = get_resume_dir()
    if not resume_files or len(resume_files) == 0:
        print("No resumes found :(")
        return

    for resume_file in resume_files:
        if resume_file.lower().endswith('.pdf'):
            pdf_path = get_pdf_path(resume_dir, resume_file)
            print(f'Processing {pdf_path}...')

            text = pdf_to_text(pdf_path)
            description = get_description()
            prompt = get_prompt(text, description)
            response = get_ats_percentage(prompt)
            
            if response is None:
                continue

            try:
                ats_percentage = int(response)
                if not ats_percentage > 90:
                    print(f'{pdf_path}: Did not meet the ATS percentage criteria')
                else:
                    shutil.move(pdf_path, shortlist_dir)
                    print(f'{pdf_path}: Passed the ATS percentage criteria with {ats_percentage}%')
            except Exception as _:
                print(f'{pdf_path}: Invalid ATS response from model')

if __name__ == "__main__":
    main()
