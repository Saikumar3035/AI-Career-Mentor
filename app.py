import json
import os
from pathlib import Path

import streamlit as st

from rag_star.config import APP_TITLE, APP_SUBTITLE, CAREER_PATHS, SAMPLE_JOBS, SAMPLE_STATUS_ITEMS
from rag_star.engine import CareerMentorEngine


@st.cache_resource
def get_mentor():
    return CareerMentorEngine()


def render_icon(name: str, color: str = "#ff8a65"):
    return f'<span style="display:inline-flex;align-items:center;justify-content:center;width:28px;height:28px;border-radius:10px;background:{color}22;color:{color};font-size:14px;font-weight:700;">{name}</span>'


def render_topbar():
    left, mid, right = st.columns([2.2, 3.4, 1.2])
    with left:
        st.markdown(
            """
            <div style="display:flex;align-items:center;gap:12px;">
                <div style="width:34px;height:34px;border-radius:12px;background:linear-gradient(135deg,#ff8a65,#ff4f7a);box-shadow:0 0 20px rgba(255,138,101,0.35);display:flex;align-items:center;justify-content:center;color:white;font-weight:700;">C</div>
                <div style="font-size:2.0rem;font-weight:700;color:#f5f7fb;">CareerTech.AI</div>
            </div>
            """,
            unsafe_allow_html=True,
        )
    with mid:
        st.markdown('<div style="text-align:center;font-size:2.3rem;font-weight:700;color:#f6f7fb; margin-top:8px;">Career Intelligence Command Center</div>', unsafe_allow_html=True)
    with right:
        st.markdown('<div style="display:flex;justify-content:flex-end;align-items:center;gap:12px; margin-top:12px;"> <div style="padding:8px 14px;border-radius:12px;border:1px solid rgba(255,159,125,0.35);background:rgba(15,23,42,0.28);color:#f0f5ff;">Your Dashboard</div> <div style="width:32px;height:32px;border-radius:50%;background:rgba(255,255,255,0.05);border:1px solid rgba(255,255,255,0.08);display:flex;align-items:center;justify-content:center;color:#fff;">🔔</div> </div>', unsafe_allow_html=True)


def render_dashboard(mentor):
    st.markdown("### Dashboard")
    col_goal, col_score, col_gap = st.columns([1.15, 1.1, 1.1])

    with col_goal:
        st.markdown(
            """
            <div class="glass-panel" style="padding:20px;min-height:250px;">
                <div style="display:flex;justify-content:space-between;align-items:center;margin-bottom:12px;">
                    <div style="display:flex;align-items:center;gap:10px;color:#ffb399;font-weight:700;"> <span>👤</span> Career Goal </div>
                    <div style="color:#ffb399;font-size:20px;">⋯</div>
                </div>
                <div style="font-size:3rem; font-weight:700; line-height:1.1; color:#f6f7fb; margin-top:10px;">Product Operations<br>Manager</div>
                <div style="margin-top:18px;padding:8px 12px;display:inline-flex;align-items:center;gap:8px;border:1px solid rgba(255,166,120,0.4);border-radius:12px;color:#f7d7c4;background:rgba(255,136,95,0.05);">🎯 Target Role</div>
            </div>
            """,
            unsafe_allow_html=True,
        )

    with col_score:
        st.markdown(
            """
            <div class="glass-panel" style="padding:20px;min-height:250px;">
                <div style="display:flex;justify-content:space-between;align-items:center; margin-bottom:18px;">
                    <div style="color:#ffb399;font-weight:700; display:flex; align-items:center; gap:8px;"> <span>📊</span> Career Match Score </div>
                    <div style="color:#ffb399;font-size:20px;">⋯</div>
                </div>
                <div style="display:flex;justify-content:center;align-items:center;">
                    <div style="width:170px;height:170px;border-radius:50%;background:conic-gradient(#ff8a65 0 87%, rgba(255,255,255,0.08) 87% 100%);display:flex;justify-content:center;align-items:center;">
                        <div style="width:118px;height:118px;border-radius:50%;background:#0a1427;border:2px solid rgba(255,143,99,0.15);display:flex;align-items:center;justify-content:center;flex-direction:column;color:#f6f7fb;">
                            <div style="font-size:2.7rem;font-weight:700;line-height:1;">87%</div>
                            <div style="font-size:0.72rem; color:#ffb79d; margin-top:6px;">Strong Match</div>
                        </div>
                    </div>
                </div>
            </div>
            """,
            unsafe_allow_html=True,
        )

    with col_gap:
        st.markdown(
            """
            <div class="glass-panel" style="padding:20px;min-height:250px;">
                <div style="display:flex;justify-content:space-between;align-items:center; margin-bottom:18px;">
                    <div style="color:#ffb399;font-weight:700; display:flex; align-items:center; gap:8px;"> <span>🧭</span> Skill Gap Map </div>
                    <div style="color:#ffb399;font-size:20px;">⋯</div>
                </div>
                <div style="display:flex;flex-direction:column;gap:16px;">
                    <div>
                        <div style="display:flex;justify-content:space-between; font-size:0.8rem; color:#f4f5fa; margin-bottom:4px;"><span>Operations analytics</span><span>82%</span></div>
                        <div style="height:8px;border-radius:999px;background:rgba(255,255,255,0.08);overflow:hidden;"><div style="height:100%;width:82%;background:linear-gradient(90deg,#ff8a65,#ffb08f);border-radius:999px;"></div></div>
                    </div>
                    <div>
                        <div style="display:flex;justify-content:space-between; font-size:0.8rem; color:#f4f5fa; margin-bottom:4px;"><span>Workflow design</span><span>74%</span></div>
                        <div style="height:8px;border-radius:999px;background:rgba(255,255,255,0.08);overflow:hidden;"><div style="height:100%;width:74%;background:linear-gradient(90deg,#ff8a65,#ffb08f);border-radius:999px;"></div></div>
                    </div>
                    <div>
                        <div style="display:flex;justify-content:space-between; font-size:0.8rem; color:#f4f5fa; margin-bottom:4px;"><span>Stakeholder comms</span><span>68%</span></div>
                        <div style="height:8px;border-radius:999px;background:rgba(255,255,255,0.08);overflow:hidden;"><div style="height:100%;width:68%;background:linear-gradient(90deg,#ff8a65,#ffb08f);border-radius:999px;"></div></div>
                    </div>
                    <div>
                        <div style="display:flex;justify-content:space-between; font-size:0.8rem; color:#f4f5fa; margin-bottom:4px;"><span>AI product fluency</span><span>45%</span></div>
                        <div style="height:8px;border-radius:999px;background:rgba(255,255,255,0.08);overflow:hidden;"><div style="height:100%;width:45%;background:linear-gradient(90deg,#ff8a65,#ffb08f);border-radius:999px;"></div></div>
                    </div>
                </div>
            </div>
            """,
            unsafe_allow_html=True,
        )

    row2a, row2b, row2c = st.columns([1.25, 1.05, 1.05])
    with row2a:
        st.markdown(
            """
            <div class="glass-panel" style="padding:18px 20px;min-height:155px;">
                <div style="display:flex;justify-content:space-between;align-items:center; margin-bottom:18px;">
                    <div style="color:#ffb399;font-weight:700; display:flex; align-items:center; gap:10px;"> <span>🛤️</span> Career Path Timeline </div>
                    <div style="color:#ffb399;font-size:20px;">⋯</div>
                </div>
                <div style="display:flex;justify-content:space-between;align-items:center;">
                    <div style="text-align:center; flex:1;">
                        <div style="width:36px;height:36px;border-radius:50%;margin:0 auto 8px;background:rgba(255,255,255,0.05);border:1px solid rgba(255,255,255,0.12); display:flex;align-items:center;justify-content:center;">📊</div>
                        <div style="font-size:0.82rem;color:#f2f5fb;">Analyst</div>
                    </div>
                    <div style="flex:0.5; height:2px;background:linear-gradient(90deg,#ff8a65,#ffb3a0); margin-top:-12px;"></div>
                    <div style="text-align:center; flex:1;">
                        <div style="width:36px;height:36px;border-radius:50%;margin:0 auto 8px;background:rgba(255,140,110,0.18);border:1px solid rgba(255,140,110,0.35); display:flex;align-items:center;justify-content:center;">👥</div>
                        <div style="font-size:0.82rem;color:#f2f5fb;">Coordinator</div>
                    </div>
                    <div style="flex:0.5; height:2px;background:linear-gradient(90deg,#ff8a65,#ffb3a0); margin-top:-12px;"></div>
                    <div style="text-align:center; flex:1;">
                        <div style="width:36px;height:36px;border-radius:50%;margin:0 auto 8px;background:rgba(255,140,110,0.18);border:1px solid rgba(255,140,110,0.35); display:flex;align-items:center;justify-content:center;">💼</div>
                        <div style="font-size:0.82rem;color:#f2f5fb;">Manager</div>
                    </div>
                    <div style="flex:0.5; height:2px;background:linear-gradient(90deg,#ff8a65,#ffb3a0); margin-top:-12px;"></div>
                    <div style="text-align:center; flex:1;">
                        <div style="width:36px;height:36px;border-radius:50%;margin:0 auto 8px;background:rgba(255,140,110,0.18);border:1px solid rgba(255,140,110,0.35); display:flex;align-items:center;justify-content:center;">🏆</div>
                        <div style="font-size:0.82rem;color:#f2f5fb;">Director</div>
                    </div>
                </div>
            </div>
            """,
            unsafe_allow_html=True,
        )
    with row2b:
        st.markdown(
            """
            <div class="glass-panel" style="padding:18px 20px;min-height:155px;">
                <div style="display:flex;justify-content:space-between;align-items:center; margin-bottom:18px;">
                    <div style="color:#ffb399;font-weight:700; display:flex; align-items:center; gap:10px;"> <span>🧩</span> Job Match </div>
                    <div style="color:#ffb399;font-size:20px;">⋯</div>
                </div>
                <div style="font-size:2.2rem; font-weight:700; color:#f8f9fd; text-align:left; margin-top:8px;">High-fit role</div>
                <div style="display:flex;justify-content:space-between;align-items:center; margin-top:12px;">
                    <div style="color:#f5c3b2; font-size:0.82rem;">View opportunities</div>
                    <div style="color:#ffb399; font-size:1.2rem;">→</div>
                </div>
            </div>
            """,
            unsafe_allow_html=True,
        )
    with row2c:
        st.markdown(
            """
            <div class="glass-panel" style="padding:18px 20px;min-height:155px;">
                <div style="display:flex;justify-content:space-between;align-items:center; margin-bottom:18px;">
                    <div style="color:#ffb399;font-weight:700; display:flex; align-items:center; gap:10px;"> <span>🎤</span> Interview Prep </div>
                    <div style="color:#ffb399;font-size:20px;">⋯</div>
                </div>
                <div style="font-size:2.0rem; font-weight:700; color:#f8f9fd; margin-top:8px;">3 practice rounds<br>completed</div>
                <div style="display:flex;justify-content:space-between;align-items:center; margin-top:12px;">
                    <div style="color:#f5c3b2; font-size:0.82rem;">Continue prep</div>
                    <div style="color:#ffb399; font-size:1.2rem;">→</div>
                </div>
            </div>
            """,
            unsafe_allow_html=True,
        )

    row3a, row3b, row3c = st.columns([1.05, 1.05, 1.25])
    with row3a:
        st.markdown(
            """
            <div class="glass-panel" style="padding:18px 20px;min-height:160px;">
                <div style="display:flex;justify-content:space-between;align-items:center; margin-bottom:18px;">
                    <div style="color:#ffb399;font-weight:700; display:flex; align-items:center; gap:10px;"> <span>📝</span> Resume Optimization </div>
                    <div style="color:#ffb399;font-size:20px;">⋯</div>
                </div>
                <div style="font-size:1.7rem; color:#f8f9fd; font-weight:700; margin-top:8px;">ATS alignment<br>improved</div>
                <div style="display:flex;justify-content:space-between;align-items:center; margin-top:18px;">
                    <div style="color:#f5c3b2; font-size:0.82rem;">View my resume</div>
                    <div style="color:#ffb399; font-size:1.2rem;">→</div>
                </div>
            </div>
            """,
            unsafe_allow_html=True,
        )
    with row3b:
        st.markdown(
            """
            <div class="glass-panel" style="padding:18px 20px;min-height:160px;">
                <div style="display:flex;justify-content:space-between;align-items:center; margin-bottom:18px;">
                    <div style="color:#ffb399;font-weight:700; display:flex; align-items:center; gap:10px;"> <span>📚</span> Learning Path </div>
                    <div style="color:#ffb399;font-size:20px;">⋯</div>
                </div>
                <div style="font-size:1.7rem; color:#f8f9fd; font-weight:700; margin-top:8px;">4 modules<br>recommended</div>
                <div style="display:flex;justify-content:space-between;align-items:center; margin-top:18px;">
                    <div style="color:#f5c3b2; font-size:0.82rem;">Start learning</div>
                    <div style="color:#ffb399; font-size:1.2rem;">→</div>
                </div>
            </div>
            """,
            unsafe_allow_html=True,
        )
    with row3c:
        st.markdown(
            """
            <div class="glass-panel" style="padding:18px 20px;min-height:160px;">
                <div style="display:flex;justify-content:space-between;align-items:center; margin-bottom:18px;">
                    <div style="color:#ffb399;font-weight:700; display:flex; align-items:center; gap:10px;"> <span>🌍</span> Regional Adaptation Layer </div>
                    <div style="color:#ffb399;font-size:20px;">⋯</div>
                </div>
                <div style="font-size:1.75rem; color:#f8f9fd; font-weight:700; margin-top:8px;">Localized market fit</div>
                <div style="display:flex;justify-content:space-between;align-items:center; margin-top:18px;">
                    <div style="color:#f5c3b2; font-size:0.82rem;">View regional insights</div>
                    <div style="color:#ffb399; font-size:1.2rem;">→</div>
                </div>
            </div>
            """,
            unsafe_allow_html=True,
        )

    st.markdown(
        """
        <div class="footer-strip">
            <div>🔒 Secure. Private. Built for Your Success.</div>
            <div>🤖 AI-Powered Insights</div>
            <div>📈 Real-Time Market Data</div>
            <div>🎯 Personalized for You</div>
            <div style="margin-left:auto; color:#f6d4be; font-weight:700;">Built by InitiativeAI</div>
        </div>
        """,
        unsafe_allow_html=True,
    )


def render_application_center(mentor):
    st.markdown("### Application Command Center")
    status_data = [
        {"status": "Saved", "count": 14, "color": "#5eead4"},
        {"status": "Applied", "count": 9, "color": "#60a5fa"},
        {"status": "Assessment", "count": 4, "color": "#fbbf24"},
        {"status": "Interview", "count": 3, "color": "#f97316"},
        {"status": "Offer", "count": 1, "color": "#34d399"},
        {"status": "Rejected", "count": 2, "color": "#f87171"},
    ]
    cols = st.columns(len(status_data))
    for col, item in zip(cols, status_data):
        with col:
            st.markdown(
                f"""
                <div class="status-box">
                    <div style="font-size:0.8rem;color:#d4deff;">{item['status']}</div>
                    <div style="font-size:2rem;font-weight:700;color:{item['color']}; margin-top:8px;">{item['count']}</div>
                </div>
                """,
                unsafe_allow_html=True,
            )

    st.markdown("#### Active applications")
    for item in SAMPLE_STATUS_ITEMS:
        st.markdown(
            f"""
            <div class="list-row">
                <div style="display:flex;justify-content:space-between;align-items:center;gap:14px;">
                    <div>
                        <div style="font-weight:700;color:#f4f7ff;">{item['company']}</div>
                        <div style="font-size:0.8rem;color:#cddaf8;">{item['role']} • {item['location']}</div>
                    </div>
                    <div style="padding:6px 12px;border-radius:999px;background:rgba(255,255,255,0.05);border:1px solid rgba(255,255,255,0.08);color:{item['tag_color']};">{item['status']}</div>
                </div>
                <div style="margin-top:10px;color:#dfe9ff;font-size:0.82rem;">Link: {item['link']} • Deadline: {item['deadline']} • Follow-up: {item['followup']}</div>
            </div>
            """,
            unsafe_allow_html=True,
        )


def render_market_intelligence(mentor):
    st.markdown("### Live Job Market Intelligence")
    st.markdown(
        """
        <div class="glass-panel" style="padding:22px;">
            <div style="display:flex;justify-content:space-between;">
                <div>
                    <div style="font-size:0.8rem;color:#ffb399;">Trending skills</div>
                    <div style="font-size:2rem;font-weight:700;color:#f8f9fd; margin-top:8px;">Python, AI Strategy, SQL, Cloud, Product Analytics</div>
                </div>
                <div style="padding:8px 12px;border-radius:12px;background:rgba(255,138,101,0.12);color:#ffb399;border:1px solid rgba(255,138,101,0.25);">Market Pulse</div>
            </div>
        </div>
        """,
        unsafe_allow_html=True,
    )
    for job in SAMPLE_JOBS:
        st.markdown(
            f"""
            <div class="list-row">
                <div style="display:flex;justify-content:space-between; align-items:center;">
                    <div>
                        <div style="font-weight:700;color:#f7f9ff;">{job['title']}</div>
                        <div style="font-size:0.8rem;color:#d7def7;">{job['company']} • {job['salary']} • {job['experience']}</div>
                    </div>
                    <div style="padding:6px 12px;border-radius:99px;border:1px solid rgba(255,255,255,0.08);background:rgba(255,255,255,0.04);color:#f9c7af;">{job['demand']}</div>
                </div>
            </div>
            """,
            unsafe_allow_html=True,
        )


def render_project_matching(mentor):
    st.markdown("### Project-to-Job Matching Engine")
    st.write("Connect projects or GitHub repos to target roles and see which ones best demonstrate hiring-relevant skills.")
    sample = [
        ("AI Resume Evaluator", "Python, NLP, RAG, Product Thinking", "88% fit for AI Product Analyst"),
        ("Demand Forecast Dashboard", "SQL, Analytics, Visualization, Forecasting", "91% fit for Data Analyst"),
        ("MLOps Deployment Pipeline", "Docker, CI/CD, AWS, ML", "90% fit for ML Engineer"),
    ]
    for name, tech, fit in sample:
        st.markdown(
            f"""
            <div class="list-row">
                <div style="font-weight:700;color:#f7f9ff;">{name}</div>
                <div style="font-size:0.82rem;color:#dfe8ff;margin-top:4px;">Skills: {tech}</div>
                <div style="margin-top:8px;color:#ffb399;font-size:0.9rem;">{fit}</div>
            </div>
            """,
            unsafe_allow_html=True,
        )


def render_talent_commons(mentor):
    st.markdown("### Talent Commons")
    st.write("Match people to unclaimed work using skills, projects, and role readiness. This helps discover hidden matching opportunities across teams.")
    talent = [
        ("Product AI Builder", "NLP, experimentation, analytics", "Strong match"),
        ("Career Coach for Data Roles", "Mentoring, SQL, learning design", "High alignment"),
        ("AI Workflow Analyst", "Automation, business analysis, Python", "Good pair"),
    ]
    for person, skills, match in talent:
        st.markdown(
            f"""
            <div class="list-row">
                <div style="display:flex;justify-content:space-between;align-items:center;">
                    <div style="font-weight:700;color:#f7f9ff;">{person}</div>
                    <div style="padding:6px 12px;border-radius:999px;border:1px solid rgba(255,255,255,0.08);background:rgba(255,255,255,0.04);color:#ffb399;">{match}</div>
                </div>
                <div style="font-size:0.82rem;color:#dfe8ff;margin-top:6px;">Skills: {skills}</div>
            </div>
            """,
            unsafe_allow_html=True,
        )


def main():
    st.set_page_config(page_title=APP_TITLE, page_icon="✨", layout="wide")
    st.markdown(
        """
        <style>
        :root {
            --bg: #060d1b;
            --bg-2: #0d162c;
            --panel: rgba(13, 20, 35, 0.82);
            --panel-soft: rgba(20, 30, 48, 0.9);
            --line: rgba(255, 152, 114, 0.30);
            --text: #edf3ff;
            --muted: #c7d4f0;
            --accent: #ff8a65;
            --accent-2: #ffb08b;
            --subtle: rgba(255,255,255,0.06);
        }
        html, body, [data-testid="stApp"] {
            background:
                radial-gradient(circle at 30% 100%, rgba(255,118,74,0.18), transparent 26%),
                linear-gradient(180deg, #030b16 0%, #061522 38%, #0c1626 100%);
            color: var(--text);
        }
        .block-container {
            padding-top: 1.6rem;
            padding-bottom: 1rem;
        }
        .glass-panel {
            background: linear-gradient(180deg, rgba(12,22,35,0.92), rgba(9,17,28,0.96));
            border: 1px solid var(--line);
            border-radius: 22px;
            box-shadow: 0 0 0 1px rgba(255,255,255,0.04), 0 18px 50px rgba(0,0,0,0.28);
        }
        .status-box, .list-row {
            background: linear-gradient(180deg, rgba(17,28,44,0.82), rgba(9,17,28,0.9));
            border: 1px solid rgba(255,255,255,0.08);
            border-radius: 16px;
            padding: 16px 18px;
            margin-bottom: 12px;
            box-shadow: inset 0 1px 0 rgba(255,255,255,0.04);
        }
        .footer-strip {
            margin-top: 18px;
            display: flex;
            gap: 18px;
            align-items: center;
            padding: 14px 18px;
            border-radius: 18px;
            border: 1px solid rgba(255,255,255,0.08);
            background: rgba(255,255,255,0.02);
            color: #f4f7ff;
            font-size: 0.8rem;
            flex-wrap: wrap;
        }
        .stSidebar {
            background: rgba(4, 9, 18, 0.72);
            border-right: 1px solid rgba(255,255,255,0.06);
        }
        .stRadio > div {
            gap: 12px;
        }
        .stRadio label {
            color: #edf3ff !important;
            font-weight: 600;
        }
        .stRadio [role="radio"] {
            border-color: #ff8a65 !important;
        }
        .stRadio [role="radio"]::before {
            background: #ff8a65 !important;
        }
        </style>
        """,
        unsafe_allow_html=True,
    )

    st.sidebar.title("Rag Star")
    st.sidebar.caption(APP_SUBTITLE)
    page = st.sidebar.radio("Navigation", ["Dashboard", "Application Center", "Market Intelligence", "Project Matching", "Talent Commons"])

    render_topbar()

    mentor = get_mentor()

    if page == "Dashboard":
        render_dashboard(mentor)
    elif page == "Application Center":
        render_application_center(mentor)
    elif page == "Market Intelligence":
        render_market_intelligence(mentor)
    elif page == "Project Matching":
        render_project_matching(mentor)
    elif page == "Talent Commons":
        render_talent_commons(mentor)


if __name__ == "__main__":
    main()
