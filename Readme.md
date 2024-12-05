
# Advanced ATS System

Welcome to the **Advanced ATS System**, a personal project designed to streamline the resume screening process. This tool evaluates resumes against predefined job descriptions and ATS criteria, offering an intuitive and feature-rich interface for recruiters. Also supports both Gemeini & ChatGPT for it's calculations and saves the scheduled interview to google calender

![ats](https://github.com/user-attachments/assets/85b094e1-1dd6-4773-a117-7e317adcd761)
![ATS SS 2](https://github.com/user-attachments/assets/664e9086-6ea6-4844-b67b-5de468b162b9)


## Features

### 1. **Job Description and Criteria Input**
   - **Text Area for Job Descriptions**: Input detailed job descriptions to define the requirements for the position.
   - **Set Experience Requirements**:  
      - Minimum Years of Experience: Define the least experience required for the role.  
      - Maximum Years of Experience: Set the upper limit of experience suitable for the role.
   - **ATS Score Criteria**: Set a difficulty level for filtering resumes based on ATS scores (0 to 100).

---

### 2. **Resume Uploads**
   - **Upload Multiple Resumes**: Drag and drop or select multiple resumes in **PDF** or **DOCX** format.
   - **Validation and Feedback**: Each resume is validated and categorized as *Accepted* or *Rejected* based on ATS criteria.

---

### 3. **Resume Processing**
   - **Score Resumes**: Automatically calculate the ATS score for each resume using the provided job description and criteria.
   - **Rejection Feedback**: Clear reasons for rejection (e.g., score below criteria, missing key information like name or email).
   - **Approval Notifications**: Resumes that meet the ATS criteria are marked as *Passed*.

---

### 4. **Candidate Information Extraction**
   - Extract **Name**, **Email**, and **Phone Number** from the resume for successful candidates.
   - Validation for missing critical details like name or email, ensuring quality processing.

---

### 5. **AI-Powered ATS Scoring**
   - **Supports Gemini and ChatGPT Models**:  
     Leverage the power of **Gemini** and **ChatGPT** for enhanced AI-driven resume analysis and ATS scoring. You can easily switch between these models based on your preference or use case.

---

### 6. **Email Notifications**
   - **HR Notification**: 
     - Receive a CSV file with details of all shortlisted candidates via email.  
     - Email includes key candidate details and their ATS scores.
   - **Candidate Notifications**:
     - Shortlisted candidates receive an email informing them of their selection.

---

### 7. **Export and Download**
   - **ZIP File of Shortlisted Resumes**: Download all shortlisted resumes in a single ZIP file for easy access.
   - **CSV Export**: Export detailed candidate information (name, email, phone, ATS score) in CSV format.

---

### 8. **Debug Logs**
   - **Debugging Made Easy**: Expandable debug logs display key details of the resume processing pipeline for transparency.

---

## How to Use

1. **Set Job Criteria**:  
   - Enter the job description, minimum and maximum experience, and ATS score criteria.
2. **Upload Resumes**:  
   - Drag and drop resumes in PDF or DOCX format into the upload section.
3. **Process Resumes**:  
   - Click "Process Resumes" to evaluate uploaded resumes.
4. **Download Results**:  
   - Download a ZIP of shortlisted resumes or a CSV with candidate details.
5. **Email Notifications**:  
   - Receive a compiled CSV of successful candidates.
   - Shortlisted candidates receive personalized email notifications.

---

## Project Structure

```
project/
│
├── main.py               # Core application logic
├── utils.py              # Utility functions for processing resumes and files
├── email_service.py      # Email handling for notifications
├── .env                  # Environment variables (API keys, email config)
└── README.md             # Project documentation
```

---

## Dependencies

Make sure you have the following libraries installed:

- **Python 3.9+**
- **Streamlit** (for the web interface)
- **dotenv** (for environment variable management)
- **io** (for handling string inputs/outputs)
- **Custom modules** (`utils`, `email_service`)

Install all dependencies using:

```bash
pip install -r requirements.txt
```

---

## Configuration

1. Create a `.env` file with the following variables:
   ```
   SMTP_SERVER=smtp.example.com
   SMTP_PORT=587
   SMTP_USER=your_email@example.com
   SMTP_PASSWORD=your_email_password
   
   GEMINI_API_KEY=your_key
   OPENAI_API_KEY=your_key
   
   AWS_BUCKET_NAME=your_aws_bucket_name
   AWS_SES_FROM_EMAIL_ID=your_aws_ses_from_email
   ```
2. Adjust any custom configurations in `email_service.py` and `utils.py` as needed.

---

## Run the Application

Start the application using Streamlit:

```bash
streamlit run main.py
```

Visit the app in your browser at `http://localhost:8501`.

---

## Future Enhancements

- **AI-Based Resume Scoring**: Use ML models to improve the scoring process.
- **Integration with Job Boards**: Automate resume collection directly from platforms like LinkedIn or Naukri.
- **Admin Dashboard**: Add analytics for processed resumes and ATS performance.

---

## **Application Workflow**

## **Overview**
This document details the automated workflow for processing candidate resumes through the ATS (Applicant Tracking System). The system is engineered to efficiently extract and evaluate candidate data, executing a series of sophisticated actions when the candidate's ATS score surpasses 75%.

---

## Workflow Steps

1. **Initial Scoring:**
   - The ATS application processes each candidate's resume.
   - Calculate the candidate's ATS score based on the match between the resume, job description and ats score.

2. **Conditional Check:**
   - **If Candidate's ATS Score > 75%:**
     - Proceed with the following steps.
   - **Else:**
     - No further action is taken for this candidate.

3. **Data Extraction:**
   - Extract the following details from the candidate's resume:
     - **Candidate's ATS Score**: The calculated score indicating how well the resume matches the job description.
     - **Candidate's Email**: The email address provided by the candidate.
     - **Candidate's Name**: The full name of the candidate.
     - **Candidate's Phone Number**: The contact phone number listed on the resume.

4. **Email Notifications:**
   - **To HR:**
     - Send an email containing the candidate's ATS score, name, email, and phone number.
   - **To Candidate:**
     - Send an email informing the candidate about the outcome and next steps.

5. **Google Calendar Event:**
   - Set up a Google Calendar event for the candidate.
   - Send the event invitation to both the candidate and HR.


6. **Download processed resumes button:**
   - Download the list of passed candidates in zip format.

### Contact

For queries, suggestions, or contributions, feel free to reach out:

- **Email**: sswaraj169@gmail.com
- **Linkedin**: https://in.linkedin.com/in/swarajkumarsingh

### Happy Recruiting!
