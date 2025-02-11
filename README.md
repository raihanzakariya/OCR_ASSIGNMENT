# OCR-Based Patient Data Extraction

## Overview
This project automates the extraction of data from patient assessment forms using Optical Character Recognition (OCR). The extracted data is stored in a PostgreSQL database in JSON format.

## Features
- Extracts text from patient assessment forms (both handwritten and printed).
- Converts extracted data into structured JSON format.
- Stores JSON data in a PostgreSQL database.
- Uses Tesseract OCR for text recognition.

## Technologies Used
- **Python** (Primary language)
- **Tesseract OCR** (Text extraction)
- **PostgreSQL** (Database storage)
- **Pillow** (Image processing)
- **psycopg2** (PostgreSQL connection)

## Installation

### Prerequisites
1. Install Python (>=3.7) if not already installed.
2. Install Tesseract OCR:
   - Windows: Download from [Tesseract OCR GitHub](https://github.com/tesseract-ocr/tesseract)
   - Linux: `sudo apt install tesseract-ocr`
3. Install PostgreSQL and create a database.

### Setup
1. Clone this repository:
   ```sh
   git clone https://github.com/your-repo/ocr-patient-data.git
   cd ocr-patient-data
   ```
2. Install required Python libraries:
   ```sh
   pip install -r requirements.txt
   ```
3. Set up the database:
   ```sql
   CREATE DATABASE ocr_db;
   
   CREATE TABLE patients (
       id SERIAL PRIMARY KEY,
       name VARCHAR(255),
       dob DATE
   );
   
   CREATE TABLE forms_data (
       id SERIAL PRIMARY KEY,
       patient_id INT REFERENCES patients(id),
       form_json JSONB,
       created_at TIMESTAMP DEFAULT NOW()
   );
   ```

## Usage

### Running the OCR Script
1. Place patient form images (JPEG or PNG) in the project folder.
2. Run the script:
   ```sh
   python ocr_script.py
   ```
3. The extracted data will be displayed in the console and stored in the PostgreSQL database.

## Example Output
```json
{
  "patient_name": "John Doe",
  "dob": "01/05/1988",
  "injection": "Yes",
  "exercise_therapy": "No",
  "pain_symptoms": {
    "pain": 2,
    "numbness": 5,
    "tingling": 6,
    "burning": 7,
    "tightness": 5
  }
}
```

## Database Integration
1. The extracted patient details are stored in the `patients` table.
2. The JSON-formatted assessment data is stored in the `forms_data` table.
3. The `patient_id` links each form entry to a patient record.

## Contributing
Feel free to submit issues and pull requests to improve this project!

## License
This project is licensed under the MIT License.
