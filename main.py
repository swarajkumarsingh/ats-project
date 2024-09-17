import sys
import utils
import streamlit as st
from io import StringIO
from dotenv import load_dotenv

load_dotenv()

sys.stdout = StringIO() 
st.set_page_config(page_title="Plus Gold ∙ ATS")

def main():
    st.title("Plus Gold | ATS")
    st.markdown("---")

    st.subheader("Job Description and ATS Criteria")
    st.write("Please provide the job description and set the ATS criteria for filtering resumes.")

    description = st.text_area("Job Description:", key="input", height=150)
    min_experience = st.number_input("Minimum Years of Experience:", min_value=0, max_value=50, value=1, step=1)
    max_experience = st.number_input("Maximum Years of Experience:", min_value=0, max_value=50, value=3, step=1)
    ats_criteria = st.number_input("Enter ATS Score Criteria (difficulty level):", min_value=0, max_value=100, value=75, step=1)

    st.markdown("---")
    st.subheader("Upload Resumes")
    st.write("")  

    uploaded_files = st.file_uploader("Upload your resumes (PDF or DOCX)...", type=["pdf", "docx"], accept_multiple_files=True)

    if uploaded_files:
        st.success(f"{len(uploaded_files)} PDF(s) Uploaded Successfully.")

    submit = st.button("Process Resumes")
    st.markdown("---")
    if submit:
        if not description:
            st.error("Please provide a job description before processing resumes.")

        elif not uploaded_files:
            st.error("Please upload at least one resume to proceed.")
        else:
            process_resumes(description, ats_criteria, uploaded_files, min_experience, max_experience)
            
    with st.expander("Show Debug Logs"):
        captured_output = sys.stdout.getvalue()
        st.text_area("Debug Logs", captured_output, height=150)

def process_resumes(description, ats_criteria, uploaded_files, min_experience, max_experience):
    proceed_resumes = []
    for uploaded_file in uploaded_files:
        pdf_content = utils.file_to_text(uploaded_file)
        if not pdf_content:
            st.write(f"Rejected: {uploaded_file.name}")
            continue

        prompt = utils.get_prompt(pdf_content, description, min_experience, max_experience)
        ats_score = utils.get_ats_score(prompt=prompt, file_name=uploaded_file.name)

        if ats_score < int(ats_criteria):
            st.write(f"Rejected: {uploaded_file.name}, ats_score: {ats_score}")
            continue
        st.write(f'Passed: {uploaded_file.name} the ATS percentage criteria with {ats_score}')

        # candidate_details_raw = utils.get_candidate_info(pdf_content)
        # if candidate_details_raw == "":
        #     st.write(f"Rejected {uploaded_file.name} with ats_score: {ats_score} because no name/email found")
        #     continue

        # name = utils.extract_info_details_name(candidate_details_raw)   
        # email = utils.extract_info_details_email(candidate_details_raw)   
        # phone = utils.extract_info_details_phone(candidate_details_raw)
        # if not name or not email:
        #     st.write(f"Rejected {uploaded_file.name} with ats_score: {ats_score} because no name/email found")
        #     continue

        # name = utils.make_text_plain(name)

        proceed_resumes.append({
            "Name": uploaded_file.name,
            # "Name": name,
            # "Email": email,
            # "Phone": phone,
            "Score": ats_score,
            "Resume": uploaded_file.name,
            "ResumeFile": uploaded_file
        })

    if len(proceed_resumes) != 0:
        # csv_path = utils.get_csv(proceed_resumes)
        # email_service.send_email_to(to_email="aniket@getplus.in", subject="ATS Passed Candidates",body_html=email_service.hr_body_html, attachment_path=csv_path)

        # for candidate in proceed_resumes:
        #     pass
            # email_service.send_email_to(to_email=candidate["Email"], subject="ATS Score Cleared!", body_html=email_service.candidate_email_body(candidate["Name"]))
        
        zip_buffer = utils.create_zip_file(proceed_resumes)
        current_date_str = utils.get_day_month_year()
        if zip_buffer: 
            st.download_button(
                label="Download Shortlisted Resumes as ZIP",
                data=zip_buffer,
                file_name=f"shortlisted-resumes-{current_date_str}.zip",
                mime="application/zip"
            )

if __name__ == "__main__":
    main()
