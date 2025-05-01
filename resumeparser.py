from dotenv import load_dotenv
load_dotenv()
import os
import json
import pdfplumber
import re
from docx import Document

from sharpapi import SharpApiService
sharp_key = os.getenv("SHARP_API_KEY");

sharp_api = SharpApiService(api_key=sharp_key)

file_to_parse = 'your_resume_file.ext'

def extract_text_from_pdf(pdf_path):
    text = ""
    with pdfplumber.open(pdf_path) as pdf:
        for page in pdf.pages:
            text += page.extract_text() + "\n"
    return text

def extract_text_from_docx(docx_path):
    text = ""
    doc = Document(docx_path)
    for para in doc.paragraphs:
        text += para.text + "\n"
    return text

def extract_text_from_file(file_path):
    ext = os.path.splitext(file_path)[1].lower()
    if ext == ".pdf":
        return extract_text_from_pdf(file_path)
    elif ext == ".docx":
        return extract_text_from_docx(file_path)
    else:
        raise ValueError("Unsupported file format: only .pdf and .docx are supported")

def extract_linkedin(text):
    match = re.search(r'(https?://)?(www\.)?linkedin\.com/in/[A-Za-z0-9\-_/]+', text)
    return match.group(0)

def get_confidence(data):
    return 0.99 if data else 0.0

try:
    status_url = sharp_api.parse_resume(
        file_path=file_to_parse,
        language='English'  # Optional
    )
    # SharpAPI doesn't parse everything, we will use regex where possible
    parsed_document = extract_text_from_file(file_to_parse)

    parsed_resume = sharp_api.fetch_results(status_url)
    raw_json_string = parsed_resume.get_result_json()

    # parsed_resume.get_result_json() returns a string that is a double-encoded JSON string. 
    # We have to parse it twice; first to turn the escaped string into a JSON string,
    # then to turn it into a Python dict

    intermediate_string = json.loads(raw_json_string)
    parsed_dict = json.loads(intermediate_string)

    name = parsed_dict.get("candidate_name", "")
    email = parsed_dict.get("candidate_email", "")
    phone = parsed_dict.get("candidate_phone", "")
    linkedin = extract_linkedin(parsed_document)
    skills = list({skill for pos in parsed_dict.get("positions", []) for skill in pos.get("skills", [])})
    certifications = parsed_dict.get("candidate_courses_and_certifications", [])
    projects = [] 

    # Collect info about the education and experience
    education = [
        {
            "school": edu.get("school_name", ""),
            "degree": edu.get("degree_type", ""),
            "specialization": edu.get("specialization_subjects", ""),
            "start_date": edu.get("start_date", ""),
            "end_date": edu.get("end_date", ""),
            "learning_mode": edu.get("learning_mode", "")
        }
        for edu in parsed_dict.get("education_qualifications", [])
    ]

    experience = [
        {
            "title": pos.get("position_name", ""),
            "company": pos.get("company_name", ""),
            "start_date": pos.get("start_date", ""),
            "end_date": pos.get("end_date", ""),
            "skills": pos.get("skills", []),
            "details": pos.get("job_details", "")
        }
        for pos in parsed_dict.get("positions", [])
    ]

    output = {
        "data": {
            "name": name,
            "email": email,
            "phone": phone,
            "linkedin": linkedin,
            "skills": skills,
            "education": education,
            "experience": experience,
            "certifications": certifications,
            "projects": projects
        },
        "confidence": {
            "name": get_confidence(name),
            "email": get_confidence(email),
            "phone": get_confidence(phone),
            "linkedin": get_confidence(linkedin),
            "skills": get_confidence(skills),
            "education": get_confidence(education),
            "experience": get_confidence(experience)
        }
    }

    print("Final output:", json.dumps(output, indent=4))



    # print(json.dumps(parsed_resume.get_result_json(), indent=2))
except Exception as e:
    print(f"An error occurred: {e}")