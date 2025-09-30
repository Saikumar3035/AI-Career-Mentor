🌟 AI Career Mentor

AI Career Mentor is an intelligent career guidance platform that leverages Generative AI and Retrieval-Augmented Generation (RAG) to help job seekers bridge the gap between their current skills and industry requirements. By analyzing resumes and job descriptions, it provides ATS-optimized resume suggestions, skill gap analysis, learning resources, career roadmaps, and mock interview preparation—all in one place.

✨ Key Features

🔐 Secure Login & Personalized Dashboard

📄 Resume & Job Description Parsing (PDF & DOCX supported)

🔎 RAG-Powered Retrieval with FAISS for fetching relevant learning resources

🤖 AI-Powered Insights

ATS-optimized resume suggestions

Missing skill detection with resource links

3–6 month personalized career roadmap

Mock interview Q&A tailored to the role

📊 User Dashboard for storing history and exporting reports

🛠️ Tech Stack

Frontend: Streamlit

Backend: Python

AI Models: OpenAI API, HuggingFace, SentenceTransformers

Vector Database: FAISS

Parsing Tools: pdfminer, python-docx

Other Libraries: NumPy, dotenv

📂 Project Structure
AI-Career-Mentor/
│── ai.py                # Main Streamlit application
│── requirements.txt      # Project dependencies
│── README.md             # Project documentation
│── data/                 # Sample resumes & job descriptions
│── outputs/              # Generated reports & recommendations

⚡ Installation & Setup

Clone the repository

git clone https://github.com/your-username/AI-Career-Mentor.git
cd AI-Career-Mentor


Create a virtual environment

python -m venv venv
source venv/bin/activate   # Mac/Linux
venv\Scripts\activate      # Windows


Install dependencies

pip install -r requirements.txt


Configure API keys
Create a .env file in the project root:

OPENAI_API_KEY=your_api_key_here


Run the application

streamlit run app.py

📖 Usage Guide

Sign up or log in to access the dashboard.

Upload your resume and job description.

Get instant insights:

✅ Resume enhancement suggestions

✅ Skill gap analysis with curated learning resources

✅ Career roadmap with upskilling strategy

✅ Mock interview Q&A

🚀 Future Roadmap

🔗 Integration with LinkedIn Jobs API for live job recommendations

🌍 Multi-language support

☁️ Cloud-based persistent user profiles

📬 Automated job application tracker

🤝 Contributing

We welcome contributions!

Fork this repository

Create your feature branch (git checkout -b feature/YourFeature)

Commit your changes (git commit -m 'Add new feature')

Push to the branch (git push origin feature/YourFeature)

Create a Pull Request
