# Rag Star

Rag Star is a modern, AI-powered career mentor platform designed to help students and professionals compare their strengths with target job roles, discover missing skills, and build a roadmap for growth.

This project is a full redesign of the original AI Career Mentor idea into a more polished, AIML-focused portfolio application.

## Why this version is better

- Modular Python project structure
- Better AI and RAG workflow
- Career analytics with clear skill-gap scoring
- Resume and job description analysis
- Personalized learning recommendations
- Stronger portfolio value for AI/ML career preparation

## Core features

- Resume vs job description matching
- Skill gap detection
- Career path suggestions
- RAG-powered learning recommendations
- Roadmap builder for target skill acquisition
- AI summary insights using OpenAI when available
- Demo-friendly fallback logic without API keys

## Project structure

```text
AI-Career-Mentor/
├── app.py
├── ai.py
├── requirements.txt
├── .env.example
├── .gitignore
├── README.md
├── rag_star/
│   ├── __init__.py
│   ├── config.py
│   ├── engine.py
│   ├── data/
│   │   └── knowledge_base.json
│   └── ui/
│       └── __init__.py
└── .streamlit/
    └── config.toml
```

## Setup

1. Clone the repository.
2. Create a virtual environment:

```bash
python -m venv venv
source venv/bin/activate
```

3. Install dependencies:

```bash
pip install -r requirements.txt
```

4. Add your API key (optional):

```bash
cp .env.example .env
```

Then update `.env`:

```env
OPENAI_API_KEY=your_api_key_here
```

## Run the app

```bash
streamlit run app.py
```

## Demo usage

- Upload a resume and target job description
- See the match percentage and missing skills
- Review the best-fit career path
- Get learning resources and roadmap suggestions
- Explore skill-gap analytics

## Tech stack

- Python
- Streamlit
- SentenceTransformers
- FAISS
- OpenAI API
- pdfminer.six
- python-docx
- Plotly
- pandas

## AIML career vision

Rag Star is built to reflect a real-world AI career project: combining NLP, information retrieval, personalization, and career intelligence into one polished experience.

This makes it suitable for:

- AI portfolio work
- Internship/college project showcase
- Capstone demonstration
- Career preparation dashboard

## License

This project is for personal and learning use.
