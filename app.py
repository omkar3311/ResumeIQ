import streamlit as st
from ATS_checker import ATS
from JD_checker import JD

st.markdown(
    """
    <style>
    .css-18e3th9 { 
        padding-top: 0rem;
        padding-bottom: 0rem;
        padding-left: 0rem;
        padding-right: 0rem;
        margin: 0;
    }
    body {
        background: linear-gradient(to bottom, #6a0dad 0%,#7a1fbd 100%);
        background-attachment: fixed;
        margin: 0;
        height: 100vh;
        width: 100%;
    }
    .stApp, .css-1d391kg {
        background-color: transparent;
    }
    </style>
    """,
    unsafe_allow_html=True
)

st.set_page_config(page_title="ResumeIQ",page_icon="📊")

if "page" not in st.session_state :
    st.session_state["page"] = "home"


def top_nav():
    col1, col2, col3 = st.columns([1, 1, 6])

    with col1:
        if st.button("🏠 Home"):
            st.session_state["page"] = "home"
            st.rerun()

    with col2:
        if st.button("📄 JD"):
            st.session_state["page"] = "jd"
            st.rerun()

    with col3:
        if st.button("🤖 ATS"):
            st.session_state["page"] = "ats"
            st.rerun()

def home_page():
    st.markdown(
        """
        <div style='display: flex; flex-direction: column; justify-content: center; align-items: center; height: 40vh;'>
            <h1 style='font-size: 80px; font-weight: bold; margin: 0;'>🤖 ResumeIQ</h1>
            <p style='font-size: 24px; color: black; margin-top: 0px;'>
                AI-Powered Resume Analysis for Smarter Hiring
            </p>
        </div>
        """,
        unsafe_allow_html=True )
    col1,col2 = st.columns(2)
    with col1:
        st.markdown(
            f"""
                    <div style="
                        border: 2px solid black;
                        border-radius: 8px;
                        padding: 15px;
                        margin-bottom: 15px;
                        background-color: transparent;
                        text-align: center;
                        box-shadow: 0 2px 5px rgba(0, 0, 0, 0.1);
                    ">
                    <h2 style="margin: 0; color: #333;">JD checker</h2>
                    </div>
                    """,unsafe_allow_html=True)
        if st.button("➡️ Get started"):
            st.session_state["page"] = "jd"
            st.rerun()
            
    with col2:
        st.markdown(
            f"""
                    <div style="
                        border: 2px solid black;
                        border-radius: 8px;
                        padding: 15px;
                        margin-bottom: 15px;
                        background-color: transparent;
                        text-align: center;
                        box-shadow: 0 2px 5px rgba(0, 0, 0, 0.1);
                    ">
                    <h2 style="margin: 0; color: #333;">ATS checker</h2>
                    </div>
                    """,unsafe_allow_html=True)
        if st.button("➡️ Get started", key="ats"):
            st.session_state["page"] = "ats"
            st.rerun()

if st.session_state["page"] == "home":
    home_page()

elif st.session_state["page"] == "jd":
    JD()

elif st.session_state["page"] == "ats":
    ATS()