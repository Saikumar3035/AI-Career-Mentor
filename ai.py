import os
from pathlib import Path

import streamlit as st

from rag_star.config import APP_TITLE, APP_SUBTITLE, CAREER_PATHS
from rag_star.engine import CareerMentorEngine


@st.cache_resource
def get_mentor():
    return CareerMentorEngine()


def render_resume_analysis(mentor: CareerMentorEngine):
    st.markdown("### Resume vs Job Match")
    col1, col2 = st.columns(2)

    with col1:
        st.markdown("#### Upload Resume")
        resume_file = st.file_uploader("Resume", type=["pdf", "docx", "txt"], key="resume_upload")

    with col2:
        st.markdown("#### Upload Job Description")
        job_file = st.file_uploader("Job description", type=["pdf", "docx", "txt"], key="job_upload")

    if resume_file and job_file:
        with st.spinner("Analyzing documents..."):
            resume_text = mentor.extract_text_from_file(resume_file, resume_file.name.lower().split(".")[-1])
            job_text = mentor.extract_text_from_file(job_file, job_file.name.lower().split(".")[-1])

            if not resume_text or not job_text:
                st.warning("Unable to read both documents. Please check file format and content.")
                return

            resume_info = mentor.extract_comprehensive_info(resume_text, is_resume=True)
            job_info = mentor.extract_comprehensive_info(job_text, is_resume=False)
            match_score = mentor.calculate_match_score(resume_info["skills"]["all"], job_info["skills"]["all"])

            st.markdown("#### Match summary")
            c1, c2, c3 = st.columns(3)
            c1.metric("Overall Match", f"{match_score['match_percentage']}%")
            c2.metric("Matched Skills", len(match_score["matched_skills"]))
            c3.metric("Skills to Learn", len(match_score["missing_skills"]))

            col3, col4 = st.columns(2)
            with col3:
                st.markdown("##### Matched skills")
                for skill in match_score["matched_skills"]:
                    st.success(f"✓ {skill}")
            with col4:
                st.markdown("##### Missing skills")
                for skill in match_score["missing_skills"]:
                    st.error(f"✗ {skill}")

            st.markdown("#### Best-fit career paths")
            path_suggestions = mentor.suggest_career_path(resume_info["skills"]["all"]) 
            for path, info in list(path_suggestions.items())[:3]:
                with st.expander(f"{path} — {info['score']}% match"):
                    st.write("Missing core skills:")
                    if info["missing_core"]:
                        for skill in info["missing_core"][:5]:
                            st.write(f"- {skill}")
                    else:
                        st.write("No major skill gaps for this path.")

            st.markdown("#### Personalized recommendations")
            recommendations = mentor.get_personalized_recommendations(resume_info, job_info, match_score)

            if recommendations["learning_resources"]:
                st.markdown("##### Learning resources")
                for resource in recommendations["learning_resources"][:3]:
                    meta = resource.get("meta", {})
                    st.markdown(f"**{meta.get('skill', 'Skill')}** — {meta.get('platform', 'Platform')}")
                    st.write(resource["text"])
                    st.caption(f"Duration: {meta.get('duration', 'Self-paced')} | Level: {meta.get('level', 'All')}" )

            if recommendations["project_ideas"]:
                st.markdown("##### Project ideas")
                for idea in recommendations["project_ideas"]:
                    st.write(f"• {idea}")

            st.markdown("#### AI insights")
            st.write(mentor.generate_ai_insights(resume_info, job_info, match_score))


def render_skill_gap(mentor: CareerMentorEngine):
    st.markdown("### Skill Gap Tracker")
    col1, col2 = st.columns(2)
    with col1:
        current_skills = st.text_area("Current skills (comma-separated)", placeholder="Python, SQL, MLOps, Docker")
    with col2:
        target_role = st.selectbox("Target role", list(CAREER_PATHS.keys()))

    if st.button("Analyze skill gap") and current_skills:
        skills = [s.strip() for s in current_skills.split(",") if s.strip()]
        required_skills = CAREER_PATHS[target_role]["core_skills"]
        score = mentor.calculate_match_score(skills, required_skills)

        st.metric("Readiness", f"{score['match_percentage']}%")

        col3, col4 = st.columns(2)
        with col3:
            st.markdown("##### Skills you have")
            for skill in score["matched_skills"]:
                st.success(f"✓ {skill}")
        with col4:
            st.markdown("##### Skills to acquire")
            for skill in score["missing_skills"]:
                st.error(f"✗ {skill}")


def render_roadmap(mentor: CareerMentorEngine):
    st.markdown("### Roadmap Builder")
    target_skills = st.multiselect(
        "Select skills you want to learn",
        ["Python", "Machine Learning", "SQL", "AWS", "Docker", "React", "LLMs", "TensorFlow", "Power BI"]
    )
    experience = st.selectbox("Current experience level", ["Beginner", "Intermediate", "Advanced"])

    if st.button("Generate roadmap") and target_skills:
        for index, skill in enumerate(target_skills, start=1):
            with st.expander(f"Step {index}: {skill}"):
                query = f"{skill} {experience} learning roadmap"
                resources = mentor.get_learning_resources(query, top_k=3)
                if resources:
                    for resource in resources:
                        meta = resource.get("meta", {})
                        st.write(f"**{meta.get('platform', 'Resource')}**")
                        st.write(resource["text"])
                        st.caption(f"Duration: {meta.get('duration', 'Self-paced')} | Level: {meta.get('level', 'All')}")
                else:
                    st.write(f"Learn {skill} through structured tutorials, hands-on projects, and guided labs.")


def main():
    st.set_page_config(page_title="Rag Star", page_icon="✨", layout="wide")
    st.markdown(
        """
        <style>
        .block-container { padding-top: 2rem; }
        h1 { color: #3b82f6; }
        .stApp { background: linear-gradient(180deg, #f8fbff 0%, #eef6ff 100%); }
        </style>
        """,
        unsafe_allow_html=True,
    )

    st.sidebar.title("Rag Star")
    st.sidebar.write(APP_SUBTITLE)
    page = st.sidebar.radio("Navigation", ["Resume Match", "Skill Gap", "Roadmap"])

    st.title("✨ Rag Star")
    st.caption("AI career mentor for smarter career growth")

    mentor = get_mentor()

    if page == "Resume Match":
        render_resume_analysis(mentor)
    elif page == "Skill Gap":
        render_skill_gap(mentor)
    else:
        render_roadmap(mentor)


if __name__ == "__main__":
    main()
