from pathlib import Path

APP_TITLE = "Rag Star"
APP_SUBTITLE = "AI Career Mentor for smarter career growth and interview readiness"
BASE_DIR = Path(__file__).resolve().parent
KNOWLEDGE_BASE_FILE = BASE_DIR / "data" / "knowledge_base.json"

CAREER_PATHS = {
    "AI Engineer": {
        "core_skills": ["Python", "Machine Learning", "Deep Learning", "SQL", "MLOps"],
        "advanced_skills": ["PyTorch", "TensorFlow", "LLMs", "Computer Vision", "Model Deployment"],
        "tools": ["Docker", "Git", "AWS", "Kubernetes", "Jupyter"],
        "soft_skills": ["Problem Solving", "Communication", "Analytical Thinking"],
    },
    "Data Scientist": {
        "core_skills": ["Python", "SQL", "Statistics", "Machine Learning", "Data Analysis"],
        "advanced_skills": ["Pandas", "NumPy", "EDA", "Feature Engineering", "A/B Testing"],
        "tools": ["Jupyter", "Tableau", "Power BI", "Git", "AWS"],
        "soft_skills": ["Storytelling", "Critical Thinking", "Communication"],
    },
    "Software Engineer": {
        "core_skills": ["Python", "JavaScript", "Data Structures", "Algorithms", "Git"],
        "advanced_skills": ["System Design", "Microservices", "REST APIs", "Testing", "DevOps"],
        "tools": ["Docker", "AWS", "Linux", "CI/CD", "GitHub"],
        "soft_skills": ["Teamwork", "Problem Solving", "Ownership"],
    },
    "Frontend Developer": {
        "core_skills": ["HTML", "CSS", "JavaScript", "React", "UI Design"],
        "advanced_skills": ["TypeScript", "Node.js", "Next.js", "Accessibility", "State Management"],
        "tools": ["Git", "Figma", "Webpack", "npm", "Chrome DevTools"],
        "soft_skills": ["Creativity", "User Experience", "Communication"],
    },
    "Cloud Engineer": {
        "core_skills": ["Linux", "Networking", "AWS", "Docker", "Terraform"],
        "advanced_skills": ["Kubernetes", "Security", "Infrastructure as Code", "Monitoring", "CI/CD"],
        "tools": ["Git", "Docker", "Kubernetes", "CloudFormation", "Prometheus"],
        "soft_skills": ["Automation", "Problem Solving", "Collaboration"],
    },
}

SKILL_DATABASE = {
    "programming": [
        "Python", "Java", "JavaScript", "TypeScript", "C++", "C#", "Go", "Rust", "PHP", "SQL", "R"
    ],
    "web": [
        "HTML", "CSS", "React", "Node.js", "Express", "Django", "Flask", "Next.js", "REST APIs", "GraphQL"
    ],
    "ml_ai": [
        "Machine Learning", "Deep Learning", "TensorFlow", "PyTorch", "LLMs", "Computer Vision", "NLP", "Data Analysis", "Pandas", "NumPy", "Scikit-learn", "OpenCV"
    ],
    "cloud": [
        "AWS", "Azure", "GCP", "Docker", "Kubernetes", "Linux", "Terraform", "CI/CD", "Git", "Jenkins"
    ],
    "data": [
        "SQL", "Statistics", "Tableau", "Power BI", "Excel", "Spark", "Data Visualization", "ETL"
    ],
}

SOFT_SKILLS = [
    "Leadership", "Communication", "Problem Solving", "Teamwork", "Critical Thinking",
    "Time Management", "Adaptability", "Creativity", "Attention to Detail",
    "Project Management", "Public Speaking", "Mentoring", "Analytical Thinking"
]

ROLE_PATTERNS = [
    r"(?:AI|Data|Machine Learning|Software|Frontend|Cloud|Full Stack|Backend|DevOps)\s+(?:Engineer|Developer|Scientist|Analyst)",
    r"(?:Senior|Lead|Principal|Staff)\s+(?:Engineer|Developer|Scientist|Analyst)",
    r"(?:Manager|Director|VP|CTO|Lead)\s+(?:Engineering|Technology|Data)"
]

CERTIFICATE_MAP = {
    "AWS": ["AWS Solutions Architect Associate", "AWS Certified Developer"],
    "Python": ["Python Institute PCAP", "Python Institute PCPP"],
    "Machine Learning": ["Google ML Engineer", "AWS ML Specialty"],
    "Azure": ["Azure Fundamentals", "Azure Developer Associate"],
    "Data": ["Microsoft Power BI Data Analyst", "Databricks Lakehouse Fundamentals"],
    "Cloud": ["Google Associate Cloud Engineer", "CompTIA Cloud+"],
    "Security": ["CompTIA Security+", "AWS Security Specialty"],
}

PROJECT_TEMPLATES = {
    "Python": "Build a data processing app that ingests CSV/JSON and produces insights and visual dashboards.",
    "Machine Learning": "Create a predictive model using a public dataset and deploy a small API for inference.",
    "SQL": "Design a retail analytics database and write advanced queries for trends, retention, and segmentation.",
    "React": "Build a responsive product dashboard with filters, charts, and real-time state updates.",
    "AWS": "Deploy a full-stack app with EC2, S3, and CI/CD automation for a real business workflow.",
    "Docker": "Containerize a microservice app and document deployment steps and health checks.",
    "LLMs": "Build an RAG chatbot for a domain-specific knowledge base with retrieval and evaluation.",
    "TensorFlow": "Train a small deep learning model for image classification or text classification and share results.",
}

SAMPLE_STATUS_ITEMS = [
    {
        "company": "Google",
        "role": "Product Analyst",
        "location": "Remote",
        "status": "Interview",
        "tag_color": "#fbbf24",
        "link": "https://careers.google.com",
        "deadline": "2026-11-05",
        "followup": "2026-11-02",
    },
    {
        "company": "Microsoft",
        "role": "Senior Data Analyst",
        "location": "Bengaluru",
        "status": "Applied",
        "tag_color": "#60a5fa",
        "link": "https://jobs.microsoft.com",
        "deadline": "2026-11-09",
        "followup": "2026-11-01",
    },
    {
        "company": "Amazon",
        "role": "Business Analyst",
        "location": "Hyderabad",
        "status": "Assessment",
        "tag_color": "#f97316",
        "link": "https://amazon.jobs",
        "deadline": "2026-11-08",
        "followup": "2026-11-03",
    },
]

SAMPLE_JOBS = [
    {
        "title": "AI Product Analyst",
        "company": "DataForge",
        "experience": "2-4 years",
        "salary": "$120k - $145k",
        "demand": "High demand",
    },
    {
        "title": "ML Engineer",
        "company": "CloudNest",
        "experience": "3-5 years",
        "salary": "$130k - $160k",
        "demand": "Strong hiring",
    },
    {
        "title": "Data Analyst",
        "company": "Insight Labs",
        "experience": "1-3 years",
        "salary": "$95k - $120k",
        "demand": "Fast growth",
    },
]
