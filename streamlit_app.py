from dotenv import load_dotenv

load_dotenv()

import base64 
import io
import streamlit
import os
from PIL import Image
import pdf2image
import google.generativeai as genai



genai.configure(api_key = os.getenv("GOOGLE_API_KEY"))

def get_gemini_response(input,pdf_content, prompt):
    model = genai.GenerativeModel('models/gemini-pro-vision')
    response = model.generate_content([input, pdf_content[0], prompt])
    return response.text

def input_pdf_setup(upload_file):
    """
        covert the pdf to image
    """
    if upload_file is not None:
        image = pdf2image.convert_from_bytes(upload_file.read())
        
        first_page = image[0]
        
        #convert image to bytes
        img_byte_arr = io.BytesIO()
        first_page.save(img_byte_arr, format="JPEG")
        img_byte_arr = img_byte_arr.getvalue()
        
        pdf_parts = [
            {
                "mime_type" : "image/jpeg",
                "data" : base64.b64encode(img_byte_arr).decode()
            }  
        ]
        
        return pdf_parts
    
    else:
        raise FileNotFoundError("No file uploaded")
    

### ---------------- streamLit Frontend APP Start -------------- #####

streamlit.set_page_config(page_title =  "ATS Resume Expert") 
streamlit.header("ATS Tracking System")
job_description_text = streamlit.text_area ("Job Description:", key = "input")
upload_file = streamlit.file_uploader("Upload Your Resume(PDF)...")

if upload_file is not None :
    streamlit.write("Resume Uploaded Succesfully!!")
    
Resume_summerise_button = streamlit.button("Tell me About the Resume")
#Improve_Skills_button   = st.button("How can I Improve My skills")
#Match_Score_button      = st.button("Tell me about percentage Match")

resume_summerise_prompt = """
 You are an experienced Technical Human Resource Manager,your task is to review the provided resume against the job description. 
  Please share your professional evaluation on whether the candidate's profile aligns with the role. 
 Highlight the strengths and weaknesses of the applicant in relation to the specified job requirements.
"""

match_Score_prompt = """
You are an skilled ATS (Applicant Tracking System) scanner with a deep understanding of data science and ATS functionality, 
your task is to evaluate the resume against the provided job description. give me the percentage of match if the resume matches
the job description. First the output should come as percentage and then keywords missing and last final thoughts.
"""

if Resume_summerise_button:
    if upload_file is not None:
        pdf_content = input_pdf_setup(upload_file)
        response = get_gemini_response(resume_summerise_prompt,pdf_content,job_description_text)
        streamlit.subheader("The Response is")
        streamlit.write(response)
    else:
        streamlit.write("Please upload the resume")
