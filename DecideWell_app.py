import streamlit as st 
import os
import json
from openai import OpenAI
from dotenv import load_dotenv
import sqlite3
import pandas as pd


#SAVE_DIR = os.path.join(os.getcwd(), "./decidewell")
#os.makedirs(SAVE_DIR, exist_ok=True)
#HISTORY = os.path.join(SAVE_DIR, "history.json")

load_dotenv(override=True)

# ── Page config ────────────────────────────────────────────────────────────────
st.set_page_config(
    page_title="Making decision with AI",
    page_icon="🌿",
    layout="wide",
    initial_sidebar_state="auto",
)

# Custom CSS for stunning visual design
custom_css = """
<style>
    /* Root color variables - bold, intentional palette */
    :root {
        --primary: #0f172a;
        --accent: #06b6d4;
        --accent-secondary: #ec4899;
        --accent-tertiary: #8b5cf6;
        --surface: #1e293b;
        --surface-light: #334155;
        --text-primary: #f1f5f9;
        --text-secondary: #cbd5e1;
    }

    /* Global styling */
    * {
        margin: 0;
        padding: 0;
        box-sizing: border-box;
    }

    body {
        background: linear-gradient(135deg, #3a57a3 0%, #3a57a3 50%, #3a57a3 100%);
        color: var(--text-primary);
        font-family: 'Segoe UI', Tahoma, Geneva, Verdana, sans-serif;
        overflow-x: hidden;
    }

    /* Main container */
    .main {
        background: transparent !important;
    }

    .stApp {
        background: linear-gradient(135deg, #3a57a3 0%, #3a57a3 50%, #3a57a3 100%);
    }

    /* Remove default Streamlit styling */
    [data-testid="stAppViewContainer"] {
        background: transparent !important;
    }

    [data-testid="stHeader"] {
        background: transparent !important;
    }

    /* Sidebar styling */
    [data-testid="stSidebar"] {
        background: linear-gradient(180deg, #0f172a 0%, #1e293b 100%) !important;
        border-right: 2px solid rgba(6, 182, 212, 0.2) !important;
    }

    [data-testid="stSidebarContent"] {
        padding: 2rem 1rem !important;
    }

    /* Typography - distinctive and bold */
    h1 {
        font-size: 3.5rem;
        font-weight: 800;
        background: linear-gradient(120deg, #06b6d4 0%, #8b5cf6 50%, #ec4899 100%);
        -webkit-background-clip: text;
        -webkit-text-fill-color: transparent;
        background-clip: text;
        letter-spacing: -1px;
        margin-bottom: 0.5rem;
        animation: gradientShift 6s ease infinite;
    }

    h2 {
        font-size: 2rem;
        font-weight: 700;
        color: var(--text-primary);
        margin-top: 2rem;
        margin-bottom: 1rem;
        border-bottom: 3px solid var(--accent);
        padding-bottom: 0.5rem;
        display: inline-block;
    }

    h3 {
        font-size: 1.3rem;
        font-weight: 600;
        color: var(--accent);
        margin-top: 1.5rem;
        margin-bottom: 0.75rem;
    }

    p {
        color: var(--text-secondary);
        line-height: 1.6;
        margin-bottom: 1rem;
    }

    /* Gradient animation */
    @keyframes gradientShift {
        0% { filter: hue-rotate(0deg); }
        50% { filter: hue-rotate(10deg); }
        100% { filter: hue-rotate(0deg); }
    }

    /* Cards/Containers */
    [data-testid="stMetricValue"],
    [data-testid="stMetricLabel"] {
        color: var(--text-primary) !important;
    }

    .metric-card {
        background: linear-gradient(135deg, rgba(6, 182, 212, 0.1) 0%, rgba(139, 92, 246, 0.1) 100%) !important;
        border: 1px solid rgba(6, 182, 212, 0.3) !important;
        border-radius: 12px !important;
        padding: 1.5rem !important;
        backdrop-filter: blur(10px) !important;
        transition: all 0.3s ease !important;
    }

    .metric-card:hover {
        border-color: var(--accent) !important;
        background: linear-gradient(135deg, rgba(6, 182, 212, 0.2) 0%, rgba(139, 92, 246, 0.2) 100%) !important;
        transform: translateY(-4px) !important;
        box-shadow: 0 20px 40px rgba(6, 182, 212, 0.2) !important;
    }

    /* Buttons */
    button {
        background: linear-gradient(120deg, #06b6d4 0%, #8b5cf6 100%) !important;
        color: white !important;
        border: none !important;
        border-radius: 8px !important;
        font-weight: 600 !important;
        padding: 0.75rem 1.5rem !important;
        cursor: pointer !important;
        transition: all 0.3s ease !important;
        box-shadow: 0 10px 25px rgba(6, 182, 212, 0.3) !important;
    }

    button:hover {
        transform: translateY(-2px) !important;
        box-shadow: 0 15px 35px rgba(6, 182, 212, 0.5) !important;
    }

    /* Input fields */
    input, textarea, select {
        background: rgba(30, 41, 59, 0.8) !important;
        color: var(--text-primary) !important;
        border: 2px solid rgba(6, 182, 212, 0.3) !important;
        border-radius: 8px !important;
        padding: 0.75rem !important;
        transition: all 0.3s ease !important;
    }

    input:focus, textarea:focus, select:focus {
        border-color: var(--accent) !important;
        box-shadow: 0 0 0 3px rgba(6, 182, 212, 0.1) !important;
        background: rgba(30, 41, 59, 1) !important;
    }

    /* Tabs */
    [data-testid="stTabs"] [role="tablist"] {
        background: transparent !important;
        border-bottom: 2px solid rgba(6, 182, 212, 0.2) !important;
    }

    [data-testid="stTabs"] [role="tab"] {
        color: var(--text-secondary) !important;
        border: none !important;
        border-bottom: 3px solid transparent !important;
        font-weight: 600 !important;
        transition: all 0.3s ease !important;
    }

    [data-testid="stTabs"] [role="tab"][aria-selected="true"] {
        color: var(--accent) !important;
        border-bottom-color: var(--accent) !important;
    }

    [data-testid="stTabs"] [role="tab"]:hover {
        color: var(--accent) !important;
    }

    /* Expander */
    [data-testid="stExpander"] {
        border: 1px solid rgba(6, 182, 212, 0.2) !important;
        border-radius: 8px !important;
        background: rgba(30, 41, 59, 0.5) !important;
    }

    [data-testid="stExpander"] > div > button {
        background: transparent !important;
        box-shadow: none !important;
    }

    /* Slider */
    [role="slider"] {
        accent-color: var(--accent) !important;
    }

    /* Code blocks */
    pre {
        background: rgba(30, 41, 59, 0.9) !important;
        border: 1px solid rgba(6, 182, 212, 0.2) !important;
        border-radius: 8px !important;
        padding: 1rem !important;
    }

    code {
        color: var(--accent) !important;
        background: transparent !important;
    }

    /* Animations */
    @keyframes fadeInUp {
        from {
            opacity: 0;
            transform: translateY(20px);
        }
        to {
            opacity: 1;
            transform: translateY(0);
        }
    }

    @keyframes slideInRight {
        from {
            opacity: 0;
            transform: translateX(-30px);
        }
        to {
            opacity: 1;
            transform: translateX(0);
        }
    }

    .fade-in-up {
        animation: fadeInUp 0.6s ease-out;
    }

    .slide-in-right {
        animation: slideInRight 0.6s ease-out;
    }

    /* Glass morphism effect */
    .glass {
        background: rgba(30, 41, 59, 0.3);
        backdrop-filter: blur(10px);
        border: 1px solid rgba(6, 182, 212, 0.1);
        border-radius: 12px;
        padding: 1.5rem;
    }

    /* Gradient text */
    .gradient-text {
        background: linear-gradient(120deg, #06b6d4 0%, #8b5cf6 50%, #ec4899 100%);
        -webkit-background-clip: text;
        -webkit-text-fill-color: transparent;
        background-clip: text;
    }

    /* Loading animation */
    @keyframes pulse {
        0%, 100% { opacity: 1; }
        50% { opacity: 0.5; }
    }

    .pulse {
        animation: pulse 2s cubic-bezier(0.4, 0, 0.6, 1) infinite;
    }
</style>
"""

# Inject custom CSS
st.markdown(custom_css, unsafe_allow_html=True)

# st.header("Making well informed decision with AI", text_alignment="center")
# Hero Section
st.markdown("""
<div style="text-align: center; padding: 3rem 0;">
    <h1>✨ Decide Well</h1>
    <p style="font-size: 1.3rem; color: #cbd5e1; margin-top: 1rem;">
        Making well informed decision with AI
    </p>
</div>
""", unsafe_allow_html=True)

def save_db(values: dict) -> str:
    ins_sql = """INSERT INTO HISTORY_TBL(user_question,pros_list,cons_lis, ai_analysis)
values(?,?,?,?)
    """
    ins_values = (values["question"],values["pros"],values["cons"], values["ai_analysis"])
    
    try:
        with sqlite3.connect("decision_history.db") as conn:
            con = conn.cursor()
            con.execute(ins_sql,ins_values)
            return_value = "Values are saved in table"
    except sqlite3.OperationalError as err:
        return_value = "Issue with saving record:" + err
    
    return return_value

def show_history():
    try:
        with sqlite3.connect("decision_history.db") as conn:
            con = conn.cursor()
            con.execute("SELECT user_question, pros_list, cons_lis, ai_analysis FROM HISTORY_TBL")
            rows = con.fetchall()
    except sqlite3.OperationalError as err:
        print("error getting the details, error:", err)
    
    df = pd.DataFrame(rows, columns=["Question","Pros_list","Cons_list","Ai_analysis"])
    return df
            

def llm_call(question :str, pros :str, cons :str)-> str:
    client = OpenAI()
    model = "gpt-4o-mini"
    system_msg = [{"role":"system","content":"You are an excellent decision maker, you will proide rational explanasion behind your decisions."}]
    user_msg = f"""You are suppose to provide a decision based on the pros and cons given for the specific question:
    {question} with the given Pros: {pros} and given cons: {cons}. You can add more pros and cons based on your judgement.
    
    Please reply with a decision with clear explanation. Reply in markdown.
    """
    message = [{"role":"user", "content":user_msg}]+ system_msg
    response = client.chat.completions.create(
        model=model,
        messages=message
    )
    return response.choices[0].message.content
    
def clear_fields():
    input_values["question"] = ""
    input_values["pros"] = ""
    input_values["cons"] = ""


input_values : dict = {
    "question":None,
    "pros": None,
    "cons": None,
    "ai_analysis": None,
    "ai_recomnd": None
}

if "input_values" not in st.session_state:
    st.session_state.input_values  = {
        "question":None,
        "pros": None,
        "cons": None,
        "ai_analysis": None,
        "ai_recomnd": None
    }
    
tab1, tab2 = st.tabs(["📊 Your Question", "📈 History"])

with tab1:
    st.subheader("Which life decision will you like to take?")
    with st.form(key="Input_details"):
        #st.subheader("Decision Area")
        input_values["question"] = st.text_input("What's the question in your mind?")
        input_values["pros"] = st.text_area("List down your pros")
        input_values["cons"] = st.text_area("List down your cons")
    
        submit_button = st.form_submit_button("click for AI Analysis", type="primary")
    
    st.divider()
    if submit_button:
        #st.write(input_values.values())
        st.session_state.input_values["question"] = input_values["question"]
        st.session_state.input_values["pros"] = input_values["pros"]
        st.session_state.input_values["cons"] = input_values["cons"]
        with st.status("Communicating with LLM model...", expanded=True,) as status:
            st.session_state.input_values["ai_analysis"] = llm_call(input_values["question"],input_values["pros"],input_values["cons"])
            status.update(label="LLM model responded",state="complete", expanded=False)
        with st.container():
            st.subheader("Details of AI analysis:")
            #st.write("Here is the LLM analysis:")
            st.markdown(st.session_state.input_values["ai_analysis"])
            #recomend_button = st.button("Click for AI recommendations", type="secondary", on_click=ai_recomnd)
    col1, col2 = st.columns(2, gap="medium")
    with col1:
        save_record = st.button("Save Record", type="secondary")
    with col2:
        clear_records = st.button("Clear all the fields", type="primary", on_click=clear_fields)

    if save_record:
        if len(st.session_state.input_values["ai_analysis"]) >0:
            comments = save_db(st.session_state.input_values)
            st.warning(comments)
        else:
            st.warning("Please submit your question for Ai anlysis before saving!")

with tab2:
    st.subheader("Showing you all the previous communications")
    history_button = st.button("Click to Show History")
    if history_button:
        hist = show_history()
        st.dataframe(hist)


    

    

