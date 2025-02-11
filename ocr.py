import pytesseract
from PIL import Image
import json
import psycopg2
import os

# Set Tesseract path if needed
pytesseract.pytesseract.tesseract_cmd = r'C:\Program Files\Tesseract-OCR\tesseract.exe'

def ocr_extract_text(image_path):
    """Extract text from an image using Tesseract OCR."""
    image = Image.open(image_path)
    text = pytesseract.image_to_string(image)
    return text

def parse_text_to_json(text):
    """Parse extracted text into structured JSON format."""
    lines = text.split('\n')
    data = {}
    
    for line in lines:
        if "Patient Name" in line:
            data["patient_name"] = line.split(":")[-1].strip()
        elif "DOB" in line:
            data["dob"] = line.split(":")[-1].strip()
        elif "INJECTION" in line:
            data["injection"] = "YES" if "YES" in line else "NO"
        elif "Exercise Therapy" in line:
            data["exercise_therapy"] = "YES" if "YES" in line else "NO"
        elif "Pain" in line and "Numbness" in line:
            values = [int(s) for s in line.split() if s.isdigit()]
            if len(values) == 5:
                data["pain_symptoms"] = {
                    "pain": values[0],
                    "numbness": values[1],
                    "tingling": values[2],
                    "burning": values[3],
                    "tightness": values[4]
                }
    
    return json.dumps(data, indent=4)

def save_to_database(json_data):
    """Save JSON data into PostgreSQL database."""
    try:
        conn = psycopg2.connect(
            dbname="ocr_db", user="user", password="password", host="localhost", port="5432"
        )
        cursor = conn.cursor()
        
        cursor.execute("""
            INSERT INTO forms_data (form_json) VALUES (%s)
        """, (json_data,))
        
        conn.commit()
        cursor.close()
        conn.close()
        print("Data saved successfully.")
    except Exception as e:
        print("Database error:", e)

if __name__ == "__main__":
    image_path = "sample_form.jpg"  # Change this to the actual image path
    extracted_text = ocr_extract_text(image_path)
    json_data = parse_text_to_json(extracted_text)
    print(json_data)
    save_to_database(json_data)
