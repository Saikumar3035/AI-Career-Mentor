import streamlit as st
from pdfminer.high_level import extract_text
from docx import Document
import re
from sentence_transformers import SentenceTransformer
import faiss
import numpy as np
import openai
import os
from dotenv import load_dotenv
import json
import tempfile
from typing import List, Dict, Tuple, Optional
import logging
from datetime import datetime
import nltk
from collections import Counter
import plotly.express as px
import plotly.graph_objects as go
import pandas as pd

# Download required NLTK data
try:
    nltk.download('punkt', quiet=True)
    nltk.download('stopwords', quiet=True)
except:
    pass

# Configure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

# Load environment variables
load_dotenv()

# Configure Streamlit page
st.set_page_config(
    page_title="AI Career Mentor Pro", 
    layout="wide",
    initial_sidebar_state="expanded"
)

# Custom CSS for professional UI
st.markdown("""
<style>
    .main-header {
        text-align: center;
        color: #2E86AB;
        margin-bottom: 30px;
        font-size: 3rem;
        font-weight: bold;
    }
    .sub-header {
        color: #A23B72;
        border-bottom: 2px solid #F18F01;
        padding-bottom: 10px;
        margin-bottom: 20px;
    }
    .skill-match {
        background: linear-gradient(90deg, #d4edda 0%, #c3e6cb 100%);
        padding: 12px;
        border-radius: 8px;
        margin: 8px 0;
        border-left: 4px solid #28a745;
    }
    .skill-missing {
        background: linear-gradient(90deg, #f8d7da 0%, #f5c6cb 100%);
        padding: 12px;
        border-radius: 8px;
        margin: 8px 0;
        border-left: 4px solid #dc3545;
    }
    .skill-partial {
        background: linear-gradient(90deg, #fff3cd 0%, #ffeaa7 100%);
        padding: 12px;
        border-radius: 8px;
        margin: 8px 0;
        border-left: 4px solid #ffc107;
    }
    .recommendation-box {
        background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
        color: white;
        padding: 20px;
        border-radius: 15px;
        margin: 15px 0;
        box-shadow: 0 4px 15px rgba(0,0,0,0.1);
    }
    .metric-card {
        background: white;
        padding: 20px;
        border-radius: 10px;
        box-shadow: 0 2px 10px rgba(0,0,0,0.1);
        margin: 10px;
        text-align: center;
    }
    .experience-badge {
        background: #17a2b8;
        color: white;
        padding: 5px 10px;
        border-radius: 20px;
        font-size: 0.8rem;
        margin: 2px;
        display: inline-block;
    }
</style>
""", unsafe_allow_html=True)

class AdvancedCareerMentor:
    def __init__(self):
        self.openai_client = None
        self.sentence_model = None
        self.knowledge_base = []
        self.career_paths = {}
        self.skill_categories = {}
        self.setup_models()
        self.load_knowledge_base()
        self.setup_career_paths()
    
    def setup_models(self):
        """Initialize AI models with caching"""
        try:
            # Setup OpenAI
            api_key = os.getenv("OPENAI_API_KEY")
            if api_key:
                openai.api_key = api_key
                self.openai_client = openai
            else:
                st.warning("⚠️ OpenAI API key not found. AI suggestions will be limited.")
            
            # Load sentence transformer with caching
            if 'sentence_model' not in st.session_state:
                with st.spinner("🤖 Loading AI models..."):
                    st.session_state.sentence_model = SentenceTransformer('all-mpnet-base-v2')
            self.sentence_model = st.session_state.sentence_model
            
        except Exception as e:
            logger.error(f"Error setting up models: {e}")
            st.error(f"Model initialization failed: {e}")
    
    def setup_career_paths(self):
        """Define career paths and required skills"""
        self.career_paths = {
            "Data Scientist": {
                "core_skills": ["Python", "SQL", "Machine Learning", "Statistics", "Pandas", "NumPy"],
                "advanced_skills": ["TensorFlow", "PyTorch", "Deep Learning", "NLP", "Computer Vision"],
                "tools": ["Jupyter", "Git", "Docker", "AWS", "Tableau"],
                "soft_skills": ["Problem Solving", "Communication", "Critical Thinking"]
            },
            "Software Engineer": {
                "core_skills": ["Python", "Java", "JavaScript", "Git", "Algorithms", "Data Structures"],
                "advanced_skills": ["System Design", "Microservices", "DevOps", "Cloud Computing"],
                "tools": ["Docker", "Kubernetes", "AWS", "Jenkins", "MongoDB"],
                "soft_skills": ["Teamwork", "Problem Solving", "Communication"]
            },
            "Frontend Developer": {
                "core_skills": ["JavaScript", "HTML", "CSS", "React", "Vue", "Angular"],
                "advanced_skills": ["TypeScript", "Node.js", "GraphQL", "Progressive Web Apps"],
                "tools": ["Git", "Webpack", "npm", "Chrome DevTools"],
                "soft_skills": ["Creativity", "Attention to Detail", "User Experience"]
            },
            "DevOps Engineer": {
                "core_skills": ["Linux", "Docker", "Kubernetes", "AWS", "Git", "CI/CD"],
                "advanced_skills": ["Infrastructure as Code", "Monitoring", "Security", "Automation"],
                "tools": ["Terraform", "Ansible", "Jenkins", "Prometheus", "Grafana"],
                "soft_skills": ["Problem Solving", "Automation Mindset", "Communication"]
            },
            "Machine Learning Engineer": {
                "core_skills": ["Python", "Machine Learning", "TensorFlow", "PyTorch", "SQL"],
                "advanced_skills": ["MLOps", "Model Deployment", "Deep Learning", "Distributed Computing"],
                "tools": ["Docker", "Kubernetes", "AWS", "MLflow", "Kubeflow"],
                "soft_skills": ["Analytical Thinking", "Research Skills", "Communication"]
            }
        }
    
    def load_knowledge_base(self):
        """Load comprehensive knowledge base"""
        kb_file = "advanced_knowledge_base.json"
        if os.path.exists(kb_file):
            try:
                with open(kb_file, "r") as f:
                    self.knowledge_base = json.load(f)
            except Exception as e:
                self.knowledge_base = self.create_comprehensive_knowledge_base()
                self.save_knowledge_base()
        else:
            self.knowledge_base = self.create_comprehensive_knowledge_base()
            self.save_knowledge_base()
    
    def create_comprehensive_knowledge_base(self) -> List[Dict]:
        """Create a comprehensive knowledge base with learning resources"""
        return [
            # Programming Languages
            {
                "text": "Python programming masterclass covering basics to advanced topics including OOP, decorators, generators, and async programming",
                "meta": {"category": "Programming", "level": "Beginner-Advanced", "skill": "Python", "duration": "40 hours", "platform": "Coursera"}
            },
            {
                "text": "Java complete developer course with Spring Boot, Hibernate, and microservices architecture patterns",
                "meta": {"category": "Programming", "level": "Intermediate", "skill": "Java", "duration": "60 hours", "platform": "Udemy"}
            },
            {
                "text": "Modern JavaScript ES6+ course covering promises, async/await, modules, and advanced concepts",
                "meta": {"category": "Programming", "level": "Intermediate", "skill": "JavaScript", "duration": "25 hours", "platform": "freeCodeCamp"}
            },
            
            # Data Science & ML
            {
                "text": "Machine Learning Specialization by Andrew Ng - comprehensive introduction to supervised and unsupervised learning",
                "meta": {"category": "Machine Learning", "level": "Beginner", "skill": "Machine Learning", "duration": "55 hours", "platform": "Coursera"}
            },
            {
                "text": "Deep Learning Specialization covering neural networks, CNNs, RNNs, and practical implementation with TensorFlow",
                "meta": {"category": "Deep Learning", "level": "Advanced", "skill": "TensorFlow", "duration": "90 hours", "platform": "Coursera"}
            },
            {
                "text": "Data Analysis with Pandas and NumPy - complete guide to data manipulation, cleaning, and analysis",
                "meta": {"category": "Data Science", "level": "Beginner", "skill": "Pandas", "duration": "20 hours", "platform": "DataCamp"}
            },
            
            # Web Development
            {
                "text": "React complete guide including hooks, context, Redux, testing, and performance optimization",
                "meta": {"category": "Frontend", "level": "Intermediate", "skill": "React", "duration": "45 hours", "platform": "Udemy"}
            },
            {
                "text": "Node.js and Express.js backend development with authentication, APIs, and database integration",
                "meta": {"category": "Backend", "level": "Intermediate", "skill": "Node.js", "duration": "35 hours", "platform": "Pluralsight"}
            },
            
            # Cloud & DevOps
            {
                "text": "AWS Solutions Architect certification path covering EC2, S3, RDS, Lambda, and cloud architecture",
                "meta": {"category": "Cloud", "level": "Intermediate", "skill": "AWS", "duration": "80 hours", "platform": "A Cloud Guru"}
            },
            {
                "text": "Docker and Kubernetes mastery course for containerization and orchestration",
                "meta": {"category": "DevOps", "level": "Intermediate", "skill": "Docker", "duration": "30 hours", "platform": "Linux Academy"}
            },
            
            # Databases
            {
                "text": "SQL masterclass covering complex queries, window functions, stored procedures, and database optimization",
                "meta": {"category": "Database", "level": "Beginner-Advanced", "skill": "SQL", "duration": "25 hours", "platform": "SQLBolt"}
            },
            
            # Practical Projects
            {
                "text": "Build 12 real-world Python projects including web scrapers, APIs, data analysis, and automation tools",
                "meta": {"category": "Projects", "level": "Intermediate", "skill": "Python", "duration": "50 hours", "platform": "GitHub"}
            },
            {
                "text": "Kaggle Learn micro-courses on data science competitions and practical machine learning implementation",
                "meta": {"category": "Practice", "level": "All Levels", "skill": "Data Science", "duration": "Flexible", "platform": "Kaggle"}
            }
        ]
    
    def save_knowledge_base(self):
        """Save knowledge base to file"""
        try:
            with open("advanced_knowledge_base.json", "w") as f:
                json.dump(self.knowledge_base, f, indent=2)
        except Exception as e:
            logger.error(f"Error saving knowledge base: {e}")
    
    def extract_text_from_file(self, file, file_type: str) -> str:
        """Enhanced file text extraction with better error handling"""
        try:
            if file_type == "pdf":
                with tempfile.NamedTemporaryFile(delete=False, suffix=".pdf") as tmp:
                    tmp.write(file.read())
                    tmp_path = tmp.name
                try:
                    text = extract_text(tmp_path)
                    if not text.strip():
                        st.warning("PDF appears to be empty or contains only images. Consider using OCR.")
                    return text
                finally:
                    os.unlink(tmp_path)
            
            elif file_type == "docx":
                with tempfile.NamedTemporaryFile(delete=False, suffix=".docx") as tmp:
                    tmp.write(file.read())
                    tmp_path = tmp.name
                try:
                    doc = Document(tmp_path)
                    text = "\n".join([p.text for p in doc.paragraphs])
                    # Also extract text from tables
                    for table in doc.tables:
                        for row in table.rows:
                            for cell in row.cells:
                                text += "\n" + cell.text
                    return text
                finally:
                    os.unlink(tmp_path)
            
            else:  # txt
                return file.read().decode("utf-8", errors="ignore")
        
        except Exception as e:
            logger.error(f"Error extracting text from {file_type}: {e}")
            st.error(f"Error processing {file_type} file: {e}")
            return ""
    
    def extract_comprehensive_info(self, text: str, is_resume: bool = True) -> Dict:
        """Extract comprehensive information from text"""
        info = {
            "skills": [],
            "experience_years": 0,
            "education": [],
            "certifications": [],
            "projects": [],
            "companies": [],
            "roles": [],
            "industries": []
        }
        
        # Enhanced skill extraction with categories
        technical_skills = self.extract_technical_skills(text)
        soft_skills = self.extract_soft_skills(text)
        
        info["skills"] = {
            "technical": technical_skills,
            "soft": soft_skills,
            "all": technical_skills + soft_skills
        }
        
        if is_resume:
            info["experience_years"] = self.extract_experience_years(text)
            info["education"] = self.extract_education(text)
            info["certifications"] = self.extract_certifications(text)
            info["projects"] = self.extract_projects(text)
            info["companies"] = self.extract_companies(text)
            info["roles"] = self.extract_roles(text)
        
        return info
    
    def extract_technical_skills(self, text: str) -> List[str]:
        """Extract technical skills with improved accuracy"""
        # Comprehensive technical skills database
        skill_database = {
            "programming": [
                "Python", "Java", "JavaScript", "TypeScript", "C++", "C#", "Go", "Rust", 
                "Ruby", "PHP", "Swift", "Kotlin", "Scala", "R", "MATLAB"
            ],
            "web": [
                "HTML", "CSS", "React", "Angular", "Vue", "Node.js", "Express", "Django", 
                "Flask", "Spring", "ASP.NET", "Laravel", "Ruby on Rails"
            ],
            "database": [
                "SQL", "MySQL", "PostgreSQL", "MongoDB", "Redis", "Cassandra", "Oracle", 
                "SQLite", "DynamoDB", "Neo4j"
            ],
            "cloud": [
                "AWS", "Azure", "GCP", "Docker", "Kubernetes", "Jenkins", "Terraform", 
                "Ansible", "CloudFormation"
            ],
            "data_science": [
                "Machine Learning", "Deep Learning", "TensorFlow", "PyTorch", "Pandas", 
                "NumPy", "Scikit-learn", "Matplotlib", "Seaborn", "Jupyter", "Apache Spark"
            ],
            "tools": [
                "Git", "GitHub", "GitLab", "Jira", "Confluence", "Slack", "Trello", 
                "Visual Studio Code", "IntelliJ", "Eclipse"
            ]
        }
        
        found_skills = []
        text_lower = text.lower()
        
        for category, skills in skill_database.items():
            for skill in skills:
                # Use word boundaries to avoid partial matches
                pattern = r'\b' + re.escape(skill.lower()) + r'\b'
                if re.search(pattern, text_lower):
                    found_skills.append(skill)
        
        return list(set(found_skills))
    
    def extract_soft_skills(self, text: str) -> List[str]:
        """Extract soft skills from text"""
        soft_skills_db = [
            "Leadership", "Communication", "Problem Solving", "Teamwork", "Critical Thinking",
            "Time Management", "Adaptability", "Creativity", "Attention to Detail",
            "Project Management", "Public Speaking", "Negotiation", "Mentoring"
        ]
        
        found_soft_skills = []
        text_lower = text.lower()
        
        for skill in soft_skills_db:
            if skill.lower() in text_lower:
                found_soft_skills.append(skill)
        
        return found_soft_skills
    
    def extract_experience_years(self, text: str) -> int:
        """Extract years of experience from resume"""
        patterns = [
            r'(\d+)\+?\s*years?\s*(?:of\s*)?experience',
            r'experience.*?(\d+)\+?\s*years?',
            r'(\d+)\+?\s*yrs?\s*(?:of\s*)?experience'
        ]
        
        years = []
        for pattern in patterns:
            matches = re.findall(pattern, text, re.I)
            years.extend([int(match) for match in matches])
        
        return max(years) if years else 0
    
    def extract_education(self, text: str) -> List[str]:
        """Extract education information"""
        education_patterns = [
            r'(?:Bachelor|Master|PhD|B\.?S\.?|M\.?S\.?|B\.?A\.?|M\.?A\.?|B\.?Tech|M\.?Tech).*?(?:in|of)\s*([^,\n]+)',
            r'(?:University|College|Institute).*?([^,\n]+)',
            r'(Computer Science|Engineering|Mathematics|Physics|Statistics|Business)'
        ]
        
        education = []
        for pattern in education_patterns:
            matches = re.findall(pattern, text, re.I)
            education.extend(matches)
        
        return list(set(education))[:3]  # Top 3 most relevant
    
    def extract_certifications(self, text: str) -> List[str]:
        """Extract certifications"""
        cert_keywords = [
            "AWS Certified", "Google Cloud", "Microsoft Azure", "Certified", "Certification",
            "PMP", "Scrum Master", "Six Sigma", "CISSP", "CompTIA"
        ]
        
        certifications = []
        for keyword in cert_keywords:
            if re.search(r'\b' + re.escape(keyword) + r'\b', text, re.I):
                # Extract surrounding context
                matches = re.findall(rf'.{{0,30}}{re.escape(keyword)}.{{0,30}}', text, re.I)
                certifications.extend(matches)
        
        return certifications[:5]
    
    def extract_projects(self, text: str) -> List[str]:
        """Extract project information"""
        project_patterns = [
            r'(?:Project|Built|Developed|Created|Implemented).*?([^.!?\n]+)',
            r'(?:Portfolio|GitHub|Git).*?([^.!?\n]+)'
        ]
        
        projects = []
        for pattern in project_patterns:
            matches = re.findall(pattern, text, re.I)
            projects.extend([match.strip() for match in matches])
        
        return projects[:5]
    
    def extract_companies(self, text: str) -> List[str]:
        """Extract company names"""
        # This is a simplified version - in practice, you'd use NER
        company_indicators = [
            r'(?:at|@)\s+([A-Z][a-zA-Z\s&]+?)(?:\s|,|\n|\.)',
            r'(?:Company|Corp|Inc|Ltd|LLC|Technologies|Systems|Solutions)\s*([^,\n]+)'
        ]
        
        companies = []
        for pattern in company_indicators:
            matches = re.findall(pattern, text)
            companies.extend(matches)
        
        return list(set(companies))[:5]
    
    def extract_roles(self, text: str) -> List[str]:
        """Extract job roles/titles"""
        role_patterns = [
            r'(?:Software|Data|Machine Learning|AI|Full Stack|Frontend|Backend|DevOps|Cloud)\s+(?:Engineer|Developer|Scientist|Analyst)',
            r'(?:Senior|Lead|Principal|Staff)\s+(?:Engineer|Developer|Scientist)',
            r'(?:Manager|Director|VP|CTO|Lead)\s+(?:Engineering|Technology|Data)'
        ]
        
        roles = []
        for pattern in role_patterns:
            matches = re.findall(pattern, text, re.I)
            roles.extend(matches)
        
        return list(set(roles))[:5]
    
    def calculate_match_score(self, resume_skills: List[str], job_skills: List[str]) -> Dict:
        """Calculate comprehensive match score"""
        resume_skills_lower = [skill.lower() for skill in resume_skills]
        job_skills_lower = [skill.lower() for skill in job_skills]
        
        matched_skills = [skill for skill in job_skills if skill.lower() in resume_skills_lower]
        missing_skills = [skill for skill in job_skills if skill.lower() not in resume_skills_lower]
        
        # Calculate different types of matches
        exact_matches = len(matched_skills)
        total_required = len(job_skills)
        
        match_percentage = (exact_matches / total_required * 100) if total_required > 0 else 0
        
        return {
            "match_percentage": round(match_percentage, 1),
            "matched_skills": matched_skills,
            "missing_skills": missing_skills,
            "total_resume_skills": len(resume_skills),
            "total_job_skills": total_required,
            "skill_gap": len(missing_skills)
        }
    
    def suggest_career_path(self, skills: List[str]) -> Dict:
        """Suggest career paths based on current skills"""
        path_scores = {}
        
        for path_name, path_info in self.career_paths.items():
            all_path_skills = (
                path_info["core_skills"] + 
                path_info["advanced_skills"] + 
                path_info["tools"]
            )
            
            matching_skills = len(set(skill.lower() for skill in skills) & 
                                 set(skill.lower() for skill in all_path_skills))
            
            score = matching_skills / len(all_path_skills) * 100
            path_scores[path_name] = {
                "score": round(score, 1),
                "matching_skills": matching_skills,
                "total_skills": len(all_path_skills),
                "missing_core": [skill for skill in path_info["core_skills"] 
                               if skill.lower() not in [s.lower() for s in skills]]
            }
        
        return dict(sorted(path_scores.items(), key=lambda x: x[1]["score"], reverse=True))
    
    def get_personalized_recommendations(self, resume_info: Dict, job_info: Dict, match_score: Dict) -> Dict:
        """Generate personalized recommendations"""
        recommendations = {
            "priority_skills": [],
            "learning_resources": [],
            "project_ideas": [],
            "certification_suggestions": [],
            "resume_improvements": [],
            "interview_prep": []
        }
        
        # Priority skills based on job requirements and current level
        missing_skills = match_score["missing_skills"]
        recommendations["priority_skills"] = missing_skills[:5]
        
        # Learning resources from RAG
        if missing_skills:
            query = " ".join(missing_skills)
            resources = self.get_learning_resources(query)
            recommendations["learning_resources"] = resources
        
        # Project ideas
        recommendations["project_ideas"] = self.generate_project_ideas(missing_skills, resume_info["skills"]["technical"])
        
        # Certification suggestions
        recommendations["certification_suggestions"] = self.suggest_certifications(missing_skills)
        
        # Resume improvements
        recommendations["resume_improvements"] = self.suggest_resume_improvements(resume_info, job_info)
        
        return recommendations
    
    def get_learning_resources(self, query: str, top_k: int = 5) -> List[Dict]:
        """Get relevant learning resources using RAG"""
        if not self.knowledge_base or not self.sentence_model:
            return []
        
        try:
            kb_texts = [item['text'] for item in self.knowledge_base]
            embeddings = self.sentence_model.encode(kb_texts, convert_to_numpy=True).astype('float32')
            
            index = faiss.IndexFlatL2(embeddings.shape[1])
            index.add(embeddings)
            
            query_vec = self.sentence_model.encode([query], convert_to_numpy=True).astype('float32')
            D, I = index.search(query_vec, k=top_k)
            
            resources = []
            for i, idx in enumerate(I[0]):
                resource = self.knowledge_base[idx].copy()
                resource['similarity_score'] = float(1 / (1 + D[0][i]))  # Convert distance to similarity
                resources.append(resource)
            
            return resources
        
        except Exception as e:
            logger.error(f"Error in RAG retrieval: {e}")
            return []
    
    def generate_project_ideas(self, missing_skills: List[str], current_skills: List[str]) -> List[str]:
        """Generate project ideas based on skills"""
        project_templates = {
            "Python": "Build a web scraper that collects and analyzes data from multiple sources",
            "Machine Learning": "Create a predictive model for a real-world problem using public datasets",
            "React": "Develop a responsive web application with modern UI/UX principles",
            "SQL": "Design and implement a database schema for a business scenario with complex queries",
            "Docker": "Containerize a multi-service application with proper orchestration",
            "AWS": "Deploy a scalable web application using AWS services with CI/CD pipeline",
            "Node.js": "Build a RESTful API with authentication and database integration",
            "TensorFlow": "Implement a deep learning model for image classification or NLP"
        }
        
        projects = []
        for skill in missing_skills[:3]:
            if skill in project_templates:
                projects.append(f"{skill}: {project_templates[skill]}")
        
        return projects
    
    def suggest_certifications(self, missing_skills: List[str]) -> List[str]:
        """Suggest relevant certifications"""
        cert_mapping = {
            "AWS": ["AWS Solutions Architect Associate", "AWS Developer Associate"],
            "Azure": ["Azure Fundamentals", "Azure Developer Associate"],
            "Google Cloud": ["Google Cloud Associate Engineer"],
            "Python": ["Python Institute PCAP", "Python Institute PCPP"],
            "Machine Learning": ["Google ML Engineer", "AWS ML Specialty"],
            "Project Management": ["PMP", "Scrum Master"],
            "Data Science": ["Microsoft Data Scientist Associate"],
            "Security": ["CompTIA Security+", "CISSP"]
        }
        
        suggestions = []
        for skill in missing_skills:
            for key, certs in cert_mapping.items():
                if key.lower() in skill.lower():
                    suggestions.extend(certs)
        
        return list(set(suggestions))[:3]
    
    def suggest_resume_improvements(self, resume_info: Dict, job_info: Dict) -> List[str]:
        """Suggest resume improvements"""
        improvements = []
        
        # Check if resume has quantified achievements
        if not re.search(r'\d+%|\$\d+|\d+\s*(?:users|customers|projects)', str(resume_info)):
            improvements.append("Add quantified achievements (e.g., 'Improved performance by 30%', 'Managed $50K budget')")
        
        # Check for action words
        action_words = ["developed", "implemented", "managed", "led", "created", "optimized"]
        resume_text = str(resume_info).lower()
        if not any(word in resume_text for word in action_words):
            improvements.append("Use strong action verbs to start bullet points (developed, implemented, led, etc.)")
        
        # Check skill relevance
        job_skills = job_info.get("skills", {}).get("all", [])
        resume_skills = resume_info.get("skills", {}).get("all", [])
        
        if len(set(s.lower() for s in resume_skills) & set(s.lower() for s in job_skills)) < len(job_skills) * 0.7:
            improvements.append("Tailor your skills section to better match the job requirements")
        
        improvements.append("Ensure your resume is ATS-friendly with clear section headers and standard formatting")
        improvements.append("Include relevant projects that demonstrate your technical skills")
        
        return improvements[:4]
    
    def generate_ai_insights(self, resume_info: Dict, job_info: Dict, match_score: Dict) -> str:
        """Generate AI-powered insights using OpenAI"""
        if not self.openai_client:
            return self.generate_fallback_insights(resume_info, job_info, match_score)
        
        prompt = f"""
        As an expert career mentor, analyze this career profile and provide personalized insights:
        
        RESUME PROFILE:
        - Technical Skills: {resume_info['skills']['technical']}
        - Experience: {resume_info.get('experience_years', 0)} years
        - Education: {resume_info.get('education', [])}
        - Projects: {resume_info.get('projects', [])[:2]}
        
        JOB REQUIREMENTS:
        - Required Skills: {job_info['skills']['all']}
        
        MATCH ANALYSIS:
        - Match Score: {match_score['match_percentage']}%
        - Missing Skills: {match_score['missing_skills']}
        - Matched Skills: {match_score['matched_skills']}
        
        Provide specific, actionable advice in these areas:
        1. Readiness Assessment (1-2 sentences)
        2. Top 3 Priority Actions
        3. Timeline Recommendation
        4. Confidence Builder (positive reinforcement)
        
        Keep it concise, encouraging, and practical.
        """
        
        try:
            response = self.openai_client.ChatCompletion.create(
                model="gpt-4o-mini",
                messages=[{"role": "user", "content": prompt}],
                max_tokens=400,
                temperature=0.7
            )
            return response['choices'][0]['message']['content']
        
        except Exception as e:
            logger.error(f"Error calling OpenAI API: {e}")
            return self.generate_fallback_insights(resume_info, job_info, match_score)
    
    def generate_fallback_insights(self, resume_info: Dict, job_info: Dict, match_score: Dict) -> str:
        """Generate insights without OpenAI API"""
        match_percentage = match_score['match_percentage']
        missing_count = len(match_score['missing_skills'])
        
        if match_percentage >= 80:
            readiness = "You're well-prepared for this role!"
        elif match_percentage >= 60:
            readiness = "You have a solid foundation with some areas to strengthen."
        else:
            readiness = "Focus on building key skills to become competitive."
        
        priority_actions = [
            f"Learn {match_score['missing_skills'][0]} - it's a key requirement" if missing_count > 0 else "Practice coding interviews",
            "Build a portfolio project showcasing your skills",
            "Network with professionals in your target companies"
        ]
        
        timeline = "2-3 months" if match_percentage >= 60 else "4-6 months"
        
        confidence = f"Your {len(match_score['matched_skills'])} matching skills show you're on the right track!"
        
        return f"""
        **Readiness Assessment:** {readiness}
        
        **Priority Actions:**
        1. {priority_actions[0]}
        2. {priority_actions[1]}
        3. {priority_actions[2]}
        
        **Timeline:** {timeline} with consistent effort
        
        **Confidence Builder:** {confidence}
        """

# Initialize the mentor
@st.cache_resource
def get_mentor():
    return AdvancedCareerMentor()

def main():
    """Main Streamlit application"""
    mentor = get_mentor()
    
    # Sidebar
    st.sidebar.markdown("## 🚀 Navigation")
    page = st.sidebar.selectbox(
        "Choose Analysis Type",
        ["Resume vs Job Match", "Career Path Analysis", "Skill Gap Analysis", "Learning Roadmap"]
    )
    
    if page == "Resume vs Job Match":
        resume_job_analysis(mentor)
    elif page == "Career Path Analysis":
        career_path_analysis(mentor)
    elif page == "Skill Gap Analysis":
        skill_gap_analysis(mentor)
    else:
        learning_roadmap(mentor)

def resume_job_analysis(mentor):
    """Resume vs Job Description Analysis"""
    st.markdown("<h1 class='main-header'>📋 Resume vs Job Analysis</h1>", unsafe_allow_html=True)
    
    col1, col2 = st.columns(2)
    
    with col1:
        st.markdown("### 📄 Upload Your Resume")
        resume_file = st.file_uploader(
            "Choose your resume file",
            type=["pdf", "docx", "txt"],
            help="Upload your resume in PDF, DOCX, or TXT format"
        )
    
    with col2:
        st.markdown("### 📋 Upload Job Description")
        job_file = st.file_uploader(
            "Choose job description file",
            type=["pdf", "docx", "txt"],
            help="Upload the job description you're targeting"
        )
    
    if resume_file and job_file:
        with st.spinner("🔍 Analyzing your documents..."):
            # Extract text
            resume_text = mentor.extract_text_from_file(
                resume_file, 
                resume_file.name.split('.')[-1]
            )
            job_text = mentor.extract_text_from_file(
                job_file, 
                job_file.name.split('.')[-1]
            )
            
            if resume_text and job_text:
                # Analyze both documents
                resume_info = mentor.extract_comprehensive_info(resume_text, is_resume=True)
                job_info = mentor.extract_comprehensive_info(job_text, is_resume=False)
                
                # Calculate match score
                match_score = mentor.calculate_match_score(
                    resume_info["skills"]["all"],
                    job_info["skills"]["all"]
                )
                
                # Display results
                display_analysis_results(mentor, resume_info, job_info, match_score)

def display_analysis_results(mentor, resume_info, job_info, match_score):
    """Display comprehensive analysis results"""
    
    # Match Score Header
    col1, col2, col3 = st.columns(3)
    
    with col1:
        st.markdown(f"""
        <div class='metric-card'>
            <h3 style='color: #2E86AB;'>{match_score['match_percentage']}%</h3>
            <p>Overall Match</p>
        </div>
        """, unsafe_allow_html=True)
    
    with col2:
        st.markdown(f"""
        <div class='metric-card'>
            <h3 style='color: #28a745;'>{len(match_score['matched_skills'])}</h3>
            <p>Skills Matched</p>
        </div>
        """, unsafe_allow_html=True)
    
    with col3:
        st.markdown(f"""
        <div class='metric-card'>
            <h3 style='color: #dc3545;'>{len(match_score['missing_skills'])}</h3>
            <p>Skills to Learn</p>
        </div>
        """, unsafe_allow_html=True)
    
    # Skills Analysis
    st.markdown("<h2 class='sub-header'>🔍 Skills Analysis</h2>", unsafe_allow_html=True)
    
    col1, col2 = st.columns(2)
    
    with col1:
        st.markdown("#### ✅ Matched Skills")
        for skill in match_score['matched_skills']:
            st.markdown(f"<div class='skill-match'>✓ {skill}</div>", unsafe_allow_html=True)
    
    with col2:
        st.markdown("#### ❌ Missing Skills")
        for skill in match_score['missing_skills']:
            st.markdown(f"<div class='skill-missing'>✗ {skill}</div>", unsafe_allow_html=True)
    
    # Career Path Suggestions
    st.markdown("<h2 class='sub-header'>🎯 Career Path Fit</h2>", unsafe_allow_html=True)
    path_suggestions = mentor.suggest_career_path(resume_info["skills"]["all"])
    
    for i, (path, info) in enumerate(list(path_suggestions.items())[:3]):
        if i == 0:
            color = "#28a745"
        elif i == 1:
            color = "#ffc107"
        else:
            color = "#17a2b8"
        
        st.markdown(f"""
        <div style='background: linear-gradient(90deg, {color}22 0%, {color}11 100%); 
                    padding: 15px; border-radius: 10px; margin: 10px 0; 
                    border-left: 4px solid {color};'>
            <h4 style='color: {color}; margin: 0;'>{path} - {info['score']}% Match</h4>
            <p style='margin: 5px 0;'>Missing core skills: {', '.join(info['missing_core'][:3])}</p>
        </div>
        """, unsafe_allow_html=True)
    
    # Personalized Recommendations
    st.markdown("<h2 class='sub-header'>🎓 Personalized Recommendations</h2>", unsafe_allow_html=True)
    recommendations = mentor.get_personalized_recommendations(resume_info, job_info, match_score)
    
    # Learning Resources
    if recommendations["learning_resources"]:
        st.markdown("#### 📚 Recommended Learning Resources")
        for resource in recommendations["learning_resources"][:3]:
            meta = resource.get('meta', {})
            st.markdown(f"""
            <div class='recommendation-box'>
                <h5>{meta.get('skill', 'General')} - {meta.get('level', 'All Levels')}</h5>
                <p>{resource['text']}</p>
                <small>📍 {meta.get('platform', 'Online')} | ⏱️ {meta.get('duration', 'Self-paced')}</small>
            </div>
            """, unsafe_allow_html=True)
    
    # Project Ideas
    if recommendations["project_ideas"]:
        st.markdown("#### 🛠️ Project Ideas")
        for project in recommendations["project_ideas"]:
            st.markdown(f"• {project}")
    
    # AI Insights
    st.markdown("<h2 class='sub-header'>🤖 AI Career Mentor Insights</h2>", unsafe_allow_html=True)
    ai_insights = mentor.generate_ai_insights(resume_info, job_info, match_score)
    st.markdown(ai_insights)
    
    # Resume Improvements
    if recommendations["resume_improvements"]:
        st.markdown("<h2 class='sub-header'>📝 Resume Improvement Tips</h2>", unsafe_allow_html=True)
        for tip in recommendations["resume_improvements"]:
            st.markdown(f"• {tip}")

def career_path_analysis(mentor):
    """Career Path Analysis Page"""
    st.markdown("<h1 class='main-header'>🎯 Career Path Analysis</h1>", unsafe_allow_html=True)
    
    st.markdown("### Enter Your Current Skills")
    skills_input = st.text_area(
        "List your skills (comma-separated)",
        placeholder="Python, SQL, Machine Learning, React, AWS...",
        height=100
    )
    
    if st.button("Analyze Career Paths") and skills_input:
        skills = [skill.strip() for skill in skills_input.split(',')]
        path_suggestions = mentor.suggest_career_path(skills)
        
        st.markdown("### 🚀 Best Career Matches")
        
        for path, info in path_suggestions.items():
            with st.expander(f"{path} - {info['score']}% Match"):
                col1, col2 = st.columns(2)
                
                with col1:
                    st.markdown("**Your Matching Skills:**")
                    core_skills = mentor.career_paths[path]["core_skills"]
                    matching = [s for s in skills if s in core_skills]
                    for skill in matching:
                        st.markdown(f"✓ {skill}")
                
                with col2:
                    st.markdown("**Skills to Develop:**")
                    for skill in info["missing_core"][:5]:
                        st.markdown(f"• {skill}")

def skill_gap_analysis(mentor):
    """Skill Gap Analysis Page"""
    st.markdown("<h1 class='main-header'>📊 Skill Gap Analysis</h1>", unsafe_allow_html=True)
    
    col1, col2 = st.columns(2)
    
    with col1:
        current_skills = st.text_area("Current Skills", height=150)
    
    with col2:
        target_role = st.selectbox("Target Role", list(mentor.career_paths.keys()))
    
    if st.button("Analyze Gap") and current_skills:
        skills = [skill.strip() for skill in current_skills.split(',')]
        required_skills = mentor.career_paths[target_role]["core_skills"]
        
        match_score = mentor.calculate_match_score(skills, required_skills)
        
        # Create visualization
        fig = go.Figure(go.Bar(
            x=['Current Skills', 'Required Skills', 'Missing Skills'],
            y=[len(skills), len(required_skills), len(match_score['missing_skills'])],
            marker_color=['#28a745', '#2E86AB', '#dc3545']
        ))
        
        fig.update_layout(title=f"Skill Gap Analysis for {target_role}")
        st.plotly_chart(fig, use_container_width=True)
        
        st.markdown("### 📈 Gap Analysis")
        col1, col2 = st.columns(2)
        
        with col1:
            st.markdown("**Skills You Have:**")
            for skill in match_score['matched_skills']:
                st.success(f"✓ {skill}")
        
        with col2:
            st.markdown("**Skills to Acquire:**")
            for skill in match_score['missing_skills']:
                st.error(f"• {skill}")

def learning_roadmap(mentor):
    """Learning Roadmap Page"""
    st.markdown("<h1 class='main-header'>🗺️ Learning Roadmap</h1>", unsafe_allow_html=True)
    
    target_skills = st.multiselect(
        "Select skills you want to learn:",
        ["Python", "JavaScript", "React", "Machine Learning", "AWS", "Docker", "SQL", "TensorFlow"]
    )
    
    experience_level = st.selectbox("Your Experience Level", ["Beginner", "Intermediate", "Advanced"])
    
    if st.button("Generate Roadmap") and target_skills:
        st.markdown("### 🎓 Your Personalized Learning Roadmap")
        
        for i, skill in enumerate(target_skills, 1):
            query = f"{skill} {experience_level}"
            resources = mentor.get_learning_resources(query, top_k=2)
            
            with st.expander(f"Step {i}: Master {skill}"):
                if resources:
                    for resource in resources:
                        meta = resource.get('meta', {})
                        st.markdown(f"""
                        **{meta.get('platform', 'Resource')}**: {resource['text']}
                        
                        *Duration: {meta.get('duration', 'Self-paced')} | Level: {meta.get('level', 'All')}*
                        """)
                else:
                    st.markdown(f"Search for {skill} courses on platforms like Coursera, Udemy, or YouTube")

if __name__ == "__main__":
    main()