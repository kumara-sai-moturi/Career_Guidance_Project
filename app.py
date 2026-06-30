import streamlit as st
from groq import Groq
from dotenv import load_dotenv
import os

# ==========================
# API
# ==========================
load_dotenv()
API_KEY = os.getenv("GROQ_API_KEY")
client = Groq(api_key=API_KEY)

# ==========================
# PAGE
# ==========================
st.set_page_config(
    page_title="Learning Dashboard",
    page_icon="🎓",
    layout="wide"
)

# ==========================
# CSS
# ==========================
st.markdown("""
<style>

label{
    color:white !important;
    font-size:18px !important;
    font-weight:bold !important;
}

input{
    color:white !important;
    background-color:#1E293B !important;
}

[data-testid="stWidgetLabel"]{
    color:#FFFFFF !important;
    font-size:18px !important;
    font-weight:bold !important;
}

.stApp{
    background:linear-gradient(135deg,#0f172a,#1e3a8a,#312e81);
    color:white;
}

.main-title{
    text-align:center;
    font-size:42px;
    font-weight:bold;
    color:white;
    margin-top:20px;
    margin-bottom:40px;
}

.card{
    background-color:#1E293B;
    padding:25px;
    border-radius:15px;
    margin-bottom:20px;
    box-shadow:0px 0px 12px rgba(255,255,255,0.15);
    color:#FFFFFF;
}

.card h3{
    color:#60A5FA;
    font-size:24px;
    font-weight:bold;
}

.card p{
    color:#F8FAFC;
    font-size:17px;
    line-height:1.6;
}

div.stButton > button{
    background:linear-gradient(90deg,#2563EB,#3B82F6);
    box-shadow:0px 0px 15px rgba(59,130,246,0.5);
    color:white;
    width:100%;
    height:50px;
    border:none;
    border-radius:10px;
    font-size:18px;
    font-weight:bold;
}

div.stButton > button:hover{
    background-color:#1D4ED8;
    color:white;
}

/* FLOWCHART CARD */
.flow-card{
    background:#1E293B;
    padding:18px;
    border-radius:12px;
    text-align:center;
    font-size:22px;
    font-weight:bold;
    margin-bottom:10px;
    border:1px solid #3B82F6;
    box-shadow:0px 0px 10px rgba(59,130,246,0.4);
}

.arrow{
    text-align:center;
    font-size:32px;
    margin-bottom:10px;
}

[data-testid="metric-container"]{
    background-color:#1E293B !important;
    border:1px solid #3B82F6;
    padding:20px;
    border-radius:12px;
}

</style>
""", unsafe_allow_html=True)

# ==========================
# SESSION
# ==========================
if "logged_in" not in st.session_state:
    st.session_state.logged_in = False

if "username" not in st.session_state:
    st.session_state.username = ""

if "career_data" not in st.session_state:
    st.session_state.career_data = ""

if "roadmap" not in st.session_state:
    st.session_state.roadmap = ""

if "flowchart" not in st.session_state:
    st.session_state.flowchart = []

if "skill" not in st.session_state:
    st.session_state.skill = ""

if "job" not in st.session_state:
    st.session_state.job = ""

if "show_login" not in st.session_state:
    st.session_state.show_login = False

if "show_signup" not in st.session_state:
    st.session_state.show_signup = False

if "show_forgot" not in st.session_state:
    st.session_state.show_forgot = False

if "users" not in st.session_state:
    st.session_state.users = {}

# ==========================
# AUTH FUNCTIONS
# ==========================
def login(username,password):

    if username=="" or password=="":
        return False

    if username in st.session_state.users:
        if st.session_state.users[username]==password:
            st.session_state.logged_in=True
            st.session_state.username=username
            return True

    return False


def signup(username,password):

    if "@" not in username:
        return "invalid_email"

    if "." not in username.split("@")[-1]:
        return "invalid_email"

    if password=="":
        return "empty_password"

    if username in st.session_state.users:
        return "exists"

    st.session_state.users[username]=password
    return "success"


# ==========================
# AI FUNCTIONS
# ==========================
def generate_ai(skill,job):

    prompt=f"""
You are an expert AI Career Guidance Assistant.

Current skills:
{skill}

Target job:
{job}

Generate personalized roadmap.

Explain:
- skills to learn
- projects to build
- certifications
- career path

Give answer in bullet points.
"""

    try:
        response=client.chat.completions.create(
            model="llama-3.1-8b-instant",
            messages=[
                {"role":"user","content":prompt}
            ]
        )

        return response.choices[0].message.content

    except Exception as e:
        return f"Error: {str(e)}"


def generate_career(job):

    prompt=f"""
A student wants career in {job}.

Tell:

1 Entry roles
2 Mid roles
3 Advanced roles
4 Future demand
5 Salary range

Short bullet points.
"""

    try:
        response=client.chat.completions.create(
            model="llama-3.1-8b-instant",
            messages=[
                {"role":"user","content":prompt}
            ]
        )

        return response.choices[0].message.content

    except Exception as e:
        return f"Error: {str(e)}"


def generate_flowchart(skill,job):

    prompt=f"""
Student knows:
{skill}

Target:
{job}

Generate learning steps only.

Rules:
- 8 steps maximum
- one step per line
- no explanation
- start beginner
- end with target job

Example:

Python Basics
Statistics
NumPy
Pandas
Machine Learning
Projects
Internship
Data Scientist
"""

    try:
        response=client.chat.completions.create(
            model="llama-3.1-8b-instant",
            messages=[
                {"role":"user","content":prompt}
            ]
        )

        result=response.choices[0].message.content

        steps=result.split("\n")
        clean=[x.strip("- ").strip()
               for x in steps if x.strip()]

        return clean

    except Exception as e:
        return [f"Error: {str(e)}"]
# ==========================
# HOME PAGE
# ==========================

if not st.session_state.logged_in:

    st.markdown(
        '<div class="main-title">🎓 Learning Path Dashboard for Enhancing Skills</div>',
        unsafe_allow_html=True
    )

    col1, col2, col3 = st.columns([1,3,1])

    with col2:

        st.markdown("""
        <div class="card">
        <h3>Career Guidance</h3>
        <p>
        This platform helps students identify their interests and career goals.<br>
        It provides guidance based on selected skills and job roles.<br>
        Students can explore personalized learning paths.
        </p>
        </div>
        """, unsafe_allow_html=True)

        st.markdown("""
        <div class="card">
        <h3>Skill Development</h3>
        <p>
        AI helps students understand what skills must be learned.<br>
        It creates personalized learning plans.<br>
        It guides students step by step.
        </p>
        </div>
        """, unsafe_allow_html=True)

        st.markdown("""
        <div class="card">
        <h3>AI Roadmap Generator</h3>
        <p>
        Using Generative AI, students get personalized career guidance.<br>
        AI generates roadmap, flowchart and opportunities.<br>
        It improves employability.
        </p>
        </div>
        """, unsafe_allow_html=True)

        # BUTTONS
        c1,c2,c3=st.columns(3)

        with c1:
            if st.button("Login"):
                st.session_state.show_login=True
                st.session_state.show_signup=False
                st.session_state.show_forgot=False

        with c2:
            if st.button("Create Account"):
                st.session_state.show_signup=True
                st.session_state.show_login=False
                st.session_state.show_forgot=False

        with c3:
            if st.button("Forgot Password"):
                st.session_state.show_forgot=True
                st.session_state.show_login=False
                st.session_state.show_signup=False

        # LOGIN
        if st.session_state.show_login:

            st.subheader("Login")

            username=st.text_input("Username")
            password=st.text_input("Password",type="password")

            if st.button("Submit Login"):

                result=login(username,password)

                if result:
                    st.success("Login Successful ✅")
                    st.rerun()
                else:
                    st.error("Invalid Login Credentials ❌")

        # SIGNUP
        if st.session_state.show_signup:

            st.subheader("Create Account")

            new_user=st.text_input("Enter Email")
            new_pass=st.text_input("Create Password",type="password")

            if st.button("Create Account Now"):

                result=signup(new_user,new_pass)

                if result=="success":
                    st.success("Account Created Successfully ✅")

                elif result=="invalid_email":
                    st.error("Invalid Email ❌")

                elif result=="empty_password":
                    st.error("Password Cannot Be Empty ❌")

                else:
                    st.error("User Already Exists ⚠️")

        # FORGOT PASSWORD
        if st.session_state.show_forgot:

            st.subheader("Forgot Password")

            forgot_email=st.text_input("Enter Registered Email")

            if st.button("Recover Password"):

                if forgot_email=="":
                    st.error("Please Enter Email ❌")

                elif forgot_email in st.session_state.users:
                    st.success("Password Reset Link Sent Successfully ✅")

                else:
                    st.error("Email Not Found ❌")


# ==========================
# DASHBOARD
# ==========================

else:

    st.sidebar.markdown("## 🎯 Navigation Panel")
    st.sidebar.write("Choose your section")

    menu=st.sidebar.radio(
        "Menu",
        [
            "Home",
            "Roadmaps",
            "AI Flowchart",
            "Career Opportunities",
            "Time Duration",
            "Prediction",
            "Logout"
        ]
    )


    # HOME
    if menu=="Home":

        st.title("Dashboard")

        st.markdown(f"""
<div style="
background:#1E293B;
padding:20px;
border-radius:15px;
text-align:center;
font-size:22px;
font-weight:bold;
margin-bottom:20px;">
👋 Welcome, {st.session_state.username}
</div>
""", unsafe_allow_html=True)

        skill=st.text_input("What skill are you interested in?")
        job=st.text_input("What kind of job are you interested in?")

        st.session_state.skill=skill
        st.session_state.job=job

        if st.button("Generate Roadmap"):

            if skill=="" or job=="":
                st.error("Please Enter Skill and Job Role ❌")

            else:

                with st.spinner("AI is generating roadmap..."):

                    roadmap=generate_ai(skill,job)

                    career_data=generate_career(job)

                    flowchart=generate_flowchart(skill,job)

                    st.session_state.roadmap=roadmap
                    st.session_state.career_data=career_data
                    st.session_state.flowchart=flowchart

                st.success("Generated Successfully ✅")

        if st.session_state.roadmap:
            st.write(st.session_state.roadmap)


    # ROADMAP
    elif menu=="Roadmaps":

        st.header("Generated Roadmap")

        if st.session_state.roadmap:
            st.write(st.session_state.roadmap)

        else:
            st.info("Generate roadmap first")
    # ==========================
    # AI FLOWCHART
    # ==========================
    elif menu=="AI Flowchart":

        st.header("🤖 AI Generated Learning Flowchart")

        if st.session_state.flowchart:

            for i, step in enumerate(st.session_state.flowchart):

                st.markdown(f"""
                <div class="flow-card">
                    {step}
                </div>
                """, unsafe_allow_html=True)

                # show arrow except last item
                if i != len(st.session_state.flowchart)-1:
                    st.markdown("""
                    <div class="arrow">
                        ⬇️
                    </div>
                    """, unsafe_allow_html=True)

        else:
            st.info("Generate roadmap first")


    # ==========================
    # CAREER OPPORTUNITIES
    # ==========================
    elif menu=="Career Opportunities":

        st.header("Career Opportunities")

        if st.session_state.career_data:

            st.markdown(f"""
            <div class="card">
            <h3>Career Growth Opportunities</h3>
            <p>{st.session_state.career_data}</p>
            </div>
            """, unsafe_allow_html=True)

        else:
            st.info("Generate roadmap first")


    # ==========================
    # TIME DURATION
    # ==========================
    elif menu=="Time Duration":

        st.header("Estimated Learning Duration")

        st.markdown("""
        <div class="card">
        <h3>Learning Timeline</h3>
        <p>
        Beginner Level : 2 Months <br><br>
        Intermediate Level : 4 Months <br><br>
        Advanced Level : 6 Months <br><br>
        Total Estimated Duration : 12 Months
        </p>
        </div>
        """, unsafe_allow_html=True)


    # ==========================
    # PREDICTION
    # ==========================
    elif menu=="Prediction":

        st.header("Career Prediction")

        skill = st.session_state.skill.lower()
        job = st.session_state.job.lower()

        score = 40

        high_demand_skills = [
            "python",
            "java",
            "ai",
            "machine learning",
            "data science",
            "cloud",
            "cyber security"
        ]

        if any(x in skill for x in high_demand_skills):
            score += 30

        if "developer" in job:
            score += 20

        if "analyst" in job:
            score += 15

        if score >= 80:
            growth = "High"
            demand = "High"

        elif score >= 60:
            growth = "Medium"
            demand = "Medium"

        else:
            growth = "Low"
            demand = "Low"

        col1,col2,col3 = st.columns(3)

        with col1:
            st.metric("📈 Career Growth", growth)

        with col2:
            st.metric("🔥 Demand Level", demand)

        with col3:
            st.metric("⭐ Score", f"{score}/100")


    # ==========================
    # LOGOUT
    # ==========================
    elif menu=="Logout":

        st.session_state.logged_in=False
        st.session_state.username=""
        st.session_state.roadmap=""
        st.session_state.career_data=""
        st.session_state.flowchart=[]
        st.session_state.skill=""
        st.session_state.job=""

        st.session_state.show_login=False
        st.session_state.show_signup=False
        st.session_state.show_forgot=False

        st.rerun()