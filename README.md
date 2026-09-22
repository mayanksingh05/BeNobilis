# BeNobilis

BeNobilis is an AI-powered ATS resume analyzer built using React and FastAPI.

## Features

* Hybrid ML ATS resume scoring (TF-IDF Cosine Similarity + Skill Match + Structure)
* Resume vs Job Description comparison
* 17-Domain Skill Category Breakdown & Visualizations
* Dynamic suggestions and tailored recommendations
* PDF and DOCX resume upload (1 KB to 30 MB)
* Modern responsive UI with Recharts and Framer Motion

## Tech Stack

### Frontend

* React
* Vite
* Tailwind CSS
* Recharts
* Framer Motion

### Backend

* FastAPI
* Python
* pdfplumber & python-docx
* scikit-learn
* spaCy

## Project Structure

frontend/ → React frontend
backend/ → FastAPI backend

## Local Setup

### 1. Backend

```bash
cd backend
pip install -r requirements.txt
python -m spacy download en_core_web_sm
uvicorn app.main:app --reload
```
API runs on `http://localhost:8000`.

### 2. Frontend

```bash
cd frontend
npm install
npm run dev
```
Frontend runs on `http://localhost:5173`.

## Future Improvements

* OCR support for scanned/image resumes
* Authentication & user profiles
* Resume version history
* Downloadable PDF reports

## Author

Mayank Singh

