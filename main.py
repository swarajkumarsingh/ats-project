import sys
import utils
import streamlit as st
from io import StringIO
from dotenv import load_dotenv

load_dotenv()

sys.stdout = StringIO() 
st.set_page_config(page_title="Plus Gold ∙ ATS")

def main():
    st.title("Plus Gold | ATS Tracking System")
    st.markdown("---")

    st.subheader("Job Description and ATS Criteria")
    st.write("Please provide the job description and set the ATS criteria for filtering resumes.")

    description = st.text_area("Job Description:", key="input", height=150)
    ats_criteria = st.number_input("Enter ATS Score Criteria (Percentage):", min_value=0, max_value=100, value=75, step=1)

    st.markdown("---")

    st.subheader("Upload Resumes")
    upload_option = st.radio("Choose how to upload resumes:", ("Upload from Computer", "Provide Google Drive Link"), index=0)
    
    st.write("")  

    uploaded_files = []

    if upload_option == "Upload from Computer":
        uploaded_files = st.file_uploader("Upload your resumes (PDF)...", type=["pdf"], accept_multiple_files=True)
        if uploaded_files:
            st.success(f"{len(uploaded_files)} PDF(s) Uploaded Successfully.")
    
    elif upload_option == "Provide Google Drive Link":
        google_drive_link = st.text_input("Enter Google Drive Link:")
        if google_drive_link:
            st.info("Fetching resumes from Google Drive...")
            uploaded_files = utils.fetch_resumes_from_drive(google_drive_link)
            st.success(f"{len(uploaded_files)} PDF(s) Fetched Successfully.")

    st.markdown("---")

    submit = st.button("Process Resumes")

    if submit:
        if not description:
            st.error("Please provide a job description before processing resumes.")
        
        elif not uploaded_files:
            if upload_option == "Upload from Computer":
                st.error("Please upload at least one resume to proceed.")
            else:
                st.error("Please provide a valid Google Drive link to fetch resumes.")
                
        proceed_resumes = []    
        for uploaded_file in uploaded_files:
            pdf_content = utils.pdf_to_text(uploaded_file)
            if not pdf_content:
                st.write(f"Rejected {uploaded_file.name}")
                continue

            prompt = utils.get_prompt(pdf_content, description)

            ats_score = utils.get_ats_score(prompt=prompt, file_name=uploaded_file.name)
            if ats_score < int(ats_criteria):
                st.write(f"Rejected {uploaded_file.name}, ats_score: {ats_score}")
                continue

            st.write(f'{uploaded_file.name}: Passed the ATS percentage criteria with {ats_score}%')

            candidate_details_raw = utils.get_candidate_info(pdf_content)
            if candidate_details_raw == "":
                st.write(f"Rejected {uploaded_file.name} with ats_score: {ats_score} because no name/email found")
                continue
            
            name = utils.extract_info_details_name(candidate_details_raw)   
            email = utils.extract_info_details_email(candidate_details_raw)   
            phone = utils.extract_info_details_phone(candidate_details_raw)

            if not name or not email:
                st.write(f"Rejected {uploaded_file.name} with ats_score: {ats_score} because no name/email found")
                continue

            name = utils.make_text_plain(name)

            proceed_resumes.append({
                "Name": name,
                "Email": email,
                "Phone": phone,
                "Score": ats_score,
                "Resume": uploaded_file.name,
                "ResumeFile": uploaded_file
            })

        if len(proceed_resumes) != 0:
            for result in proceed_resumes: st.write(result["Name"], result["Score"])

            csv_path = utils.get_csv(proceed_resumes)
            # email_service.send_email_to(to_email="aniket@getplus.in", subject="ATS Passed Candidates",body_html=email_service.hr_body_html, attachment_path=csv_path)

            for candidate in proceed_resumes:
                pass
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
            
    with st.expander("Show Debug Logs"):
        captured_output = sys.stdout.getvalue()
        st.text_area("Debug Logs", captured_output, height=150)


if __name__ == "__main__":
    main()
