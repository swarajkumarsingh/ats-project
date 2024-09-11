# 🎯 **ATS Application Workflow**

## ✨ **Overview**
This document details the automated workflow for processing candidate resumes through the ATS (Applicant Tracking System). The system is engineered to efficiently extract and evaluate candidate data, executing a series of sophisticated actions when the candidate's ATS score surpasses 75%.

---

## Workflow Steps

1. **Initial Scoring:**
   - The ATS application processes each candidate's resume.
   - Calculate the candidate's ATS score based on the match between the resume and job description.

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
   - **To Aniket:**
     - Send an email containing the candidate's ATS score, name, email, and phone number.
   - **To Candidate:**
     - Send an email informing the candidate about the outcome and next steps.

5. **Google Calendar Event:**
   - Set up a Google Calendar event for the candidate.
   - Send the event invitation to both the candidate and Aniket.
