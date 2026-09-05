import os
from datetime import date, timedelta

import streamlit as st
from google import genai

st.set_page_config(page_title="ByteVeda AI", page_icon="🎓", layout="wide")
MODEL = "gemini-2.5-flash"


@st.cache_resource
def get_client(key):
    return genai.Client(api_key=key)


def ask_ai(prompt, max_tokens=700):
    """Generate accurate, complete BCA-level answers."""
    quality_rules = """
You are ByteVeda AI, a careful and accurate BCA tutor.

Rules:
1. Give the direct answer first.
2. Explain the concept clearly using simple BCA-level language.
3. Prioritize correctness over speed.
4. Never invent facts, definitions, syntax, examples, or results.
5. If you are uncertain, clearly say so instead of guessing.
6. For programming questions, check the code logic before answering.
7. For exam questions, include the important points needed for a good answer.
8. Always finish the answer completely. Do not stop in the middle of a sentence.
9. Use headings, bullet points, and examples when useful.
10. Keep simple questions concise and give more detail when requested.
"""

    try:
        response = client.models.generate_content(
            model=MODEL,
            contents=f"{quality_rules}\n\n{prompt}",
            config={
                "temperature": 0.15,
                "max_output_tokens": max_tokens,
            },
        )

        text = response.text

        if not text:
            return "I could not create a complete answer. Please try asking the question again."

        return text

    except Exception as error:
        message = str(error)

        if "RESOURCE_EXHAUSTED" in message or "429" in message:
            return """### AI limit reached

Gemini has temporarily reached its request limit for this project.

Please try again later. You can still use the built-in study guides and practice sections."""

        return """### AI is temporarily unavailable

Please check your internet connection and Gemini API key, then try again."""


def read_uploaded_notes(uploaded_file):
    """Read text notes, with optional PDF support when pypdf is installed."""
    if uploaded_file.name.lower().endswith((".txt", ".md")):
        return uploaded_file.getvalue().decode("utf-8", errors="replace")

    try:
        from pypdf import PdfReader

        reader = PdfReader(uploaded_file)
        return "\n".join(page.extract_text() or "" for page in reader.pages)

    except ImportError:
        return "PDF reading needs the optional pypdf package. Please upload a .txt or .md file for now."

    except Exception:
        return "I could not read that PDF. Try a text-based PDF or upload a .txt/.md version."


api_key = os.environ.get("GEMINI_API_KEY")

if not api_key:
    st.error("GEMINI_API_KEY is not available.")
    st.info("Set your Gemini API key in the terminal, then restart Streamlit.")
    st.stop()

client = get_client(api_key)


for key, value in {
    "page": "Dashboard",
    "name": "",
    "saved_notes": "",
    "mock_question": "",
}.items():

    if key not in st.session_state:
        st.session_state[key] = value


st.markdown(
    """
<style>
.stApp {
    background:
        radial-gradient(circle at 12% 8%, rgba(99,102,241,.22), transparent 25%),
        radial-gradient(circle at 88% 18%, rgba(6,182,212,.18), transparent 22%),
        linear-gradient(135deg,#eef2ff 0%,#f8fafc 50%,#ecfeff 100%);
    background-attachment: fixed;
    color: #172554;
}

[data-testid="stSidebar"] {
    background: linear-gradient(180deg,#172554,#4338ca);
}

[data-testid="stSidebar"] .stMarkdown,
[data-testid="stSidebar"] p,
[data-testid="stSidebar"] span,
[data-testid="stSidebar"] label {
    color: #fff !important;
}

[data-testid="stSidebar"] button {
    background: rgba(255,255,255,.13);
    border: 1px solid rgba(255,255,255,.25);
    color: #fff !important;
}

[data-testid="stSidebar"] button:hover {
    background: rgba(255,255,255,.25);
}

h1,h2,h3,p,label,.stMarkdown {
    color: #172554;
}

.hero {
    padding: 1.4rem 1.8rem;
    border-radius: 20px;
    background: linear-gradient(120deg,#1e1b4b,#4338ca 55%,#0e7490);
    margin-bottom: 1rem;
    box-shadow: 0 14px 30px rgba(49,46,129,.22);
    border: 1px solid rgba(255,255,255,.18);
}

.hero h1 {
    color: #fff !important;
    margin: 0;
    font-size: 2.05rem;
}

.hero p {
    color: #e0f2fe !important;
    margin: .35rem 0 0;
    font-size: 1rem;
}

.card {
    min-height: 140px;
    padding: 1.2rem;
    border-radius: 18px;
    background: #fff;
    border: 1px solid #dbeafe;
    box-shadow: 0 8px 20px rgba(30,64,175,.08);
}

.card h3 {
    color: #1e3a8a !important;
    margin-top: 0;
}

.card p,
.muted {
    color: #475569 !important;
}

.resource {
    padding: 1rem;
    border-radius: 14px;
    background: #fff;
    border-left: 4px solid #4f46e5;
    margin-bottom: .7rem;
}
</style>
""",
    unsafe_allow_html=True,
)


def go_to(page):
    st.session_state.page = page
    st.rerun()


def page_header(title, subtitle):
    st.markdown(
        f"<div class='hero'><h1>{title}</h1><p>{subtitle}</p></div>",
        unsafe_allow_html=True,
    )


with st.sidebar:
    st.markdown("# 🎓 ByteVeda AI")
    st.caption("Learn BCA • Build skills • Shape your career")
    st.markdown("---")

    st.toggle("🌙 Night mode", key="night_mode")

    pages = [
        ("🏠 Dashboard", "Dashboard"),
        ("📚 Subjects", "Subjects"),
        ("🤖 AI Tutor", "AI Tutor"),
        ("💻 Programs", "Programs"),
        ("📝 BCA Notes", "Notes"),
        ("🎯 Interview Questions", "Interviews"),
        ("🗓️ Study Plans", "Study Plans"),
        ("🧑‍💼 Mock Interview", "Mock Interview"),
        ("📄 Career Kit", "Career Kit"),
        ("💼 Jobs & Internships", "Careers"),
    ]

    for label, page in pages:
        if st.button(
            label,
            use_container_width=True,
            key=f"nav_{page}",
        ):
            go_to(page)

    st.markdown("---")
    st.caption("Your BCA learning & career companion")


if st.session_state.get("night_mode"):
    st.markdown(
        """
<style>
.stApp {
    background: linear-gradient(135deg,#0f172a,#172554 55%,#083344) !important;
    color: #e2e8f0 !important;
}

h1,h2,h3,p,label,.stMarkdown {
    color: #e2e8f0 !important;
}

.card,.resource {
    background: #172554 !important;
    border-color: #334155 !important;
    box-shadow: none !important;
}

.card h3 {
    color: #bfdbfe !important;
}

.card p,.muted {
    color: #cbd5e1 !important;
}

[data-testid="stTextInput"] input,
[data-testid="stTextArea"] textarea,
[data-baseweb="select"] > div {
    background: #0f172a !important;
    color: #f8fafc !important;
    border-color: #475569 !important;
}

[data-testid="stFileUploader"] {
    background: #172554;
    border-radius: 12px;
    padding: 8px;
}
</style>
""",
        unsafe_allow_html=True,
    )


if st.session_state.page == "Dashboard":

    page_header(
        "ByteVeda AI",
        "A simple BCA workspace for learning, practice, and career progress.",
    )

    if not st.session_state.name:
        name = st.text_input(
            "What should we call you?",
            placeholder="Enter your name",
            label_visibility="collapsed",
        )

        if st.button("Save name") and name.strip():
            st.session_state.name = name.strip()
            st.rerun()

    else:
        st.caption(f"Welcome back, {st.session_state.name}.")

  st.markdown("### 🚀 What do you want to do today?")
st.caption("Choose a section below and start learning.")

    cards = [
        ("📚 Study", "Subjects & notes", "Subjects"),
        ("💻 Build", "Programs & projects", "Programs"),
        ("🎯 Practice", "Interview & study plan", "Mock Interview"),
        ("💼 Career", "Jobs & resources", "Careers"),
    ]

    for column, (title, text, destination) in zip(
        st.columns(4), cards
    ):

        with column:

            if st.button(
                title,
                key=f"home_{destination}",
                use_container_width=True,
            ):
                go_to(destination)

            st.caption(text)

    st.info(
        "Use **AI Tutor** for questions. Use the other sections for notes, "
        "code practice, interview skills, and careers."
    )


elif st.session_state.page == "Subjects":

    page_header(
        "BCA Subjects",
        "Choose a topic and get a focused explanation—not an unnecessarily long answer.",
    )

    subjects = {
        "Programming": [
            "C Programming",
            "Python",
            "Java",
            "C++",
        ],
        "Data Structures": [
            "Arrays",
            "Linked Lists",
            "Stack",
            "Queue",
            "Trees",
            "Graphs",
            "Searching",
            "Sorting",
        ],
        "Database": [
            "DBMS",
            "SQL",
            "Normalization",
            "Transactions",
        ],
        "Computer Science": [
            "Operating Systems",
            "Computer Networks",
            "Computer Architecture",
        ],
        "Web Development": [
            "HTML",
            "CSS",
            "JavaScript",
        ],
        "Emerging Technology": [
            "Artificial Intelligence",
            "Machine Learning",
            "Data Science",
            "Cybersecurity",
            "Cloud Computing",
        ],
    }

    category = st.selectbox(
        "Category",
        list(subjects),
    )

    topic = st.selectbox(
        "Topic",
        subjects[category],
    )

    st.markdown(
        f"""
<div class='resource'>
<b>Quick study focus: {topic}</b><br>
Start with the definition, learn its purpose, see one example,
then practise explaining it in your own words.
Use the AI explanation below when available for deeper learning.
</div>
""",
        unsafe_allow_html=True,
    )

    if st.button("Explain topic"):

        with st.spinner("Preparing explanation..."):

            st.markdown(
                ask_ai(
                    f"""
Question: What is {topic}?

Give a reliable BCA study answer of 300–450 words with these exact headings:
Direct answer, Why it matters, How it works, Example, Key points,
and Common mistake.

Explain unfamiliar words simply.
""",
                    900,
                )
            )


elif st.session_state.page == "AI Tutor":

    page_header(
        "AI Tutor",
        "Ask a question the way you would in ChatGPT—then choose how deeply you want to learn it.",
    )

    question = st.text_area(
        "Your question",
        placeholder="Example: Explain inheritance in Java.",
    )

    answer_type = st.selectbox(
        "Answer style",
        [
            "Short answer",
            "Detailed explanation",
            "Exam answer",
            "Practical example",
            "Code explanation",
        ],
    )

    if st.button("Get answer", type="primary"):

        if question.strip():

            with st.spinner("Thinking..."):

                instructions = {

                    "Short answer":
                        "STRICT FORMAT: Answer in a maximum of 3 short lines. "
                        "Give only the direct answer. If an example is useful, "
                        "include it in the same 3 lines. Never give a long "
                        "paragraph, headings, or extra explanation.",

                    "Detailed explanation":
                        "Give a clear explanation of about 300–450 words. "
                        "Use headings when useful. Explain the concept simply, "
                        "include an example, and avoid unnecessary repetition.",

                    "Exam answer":
                        "Give a focused, exam-ready answer of about 180–300 words. "
                        "Include a brief introduction, important key points, "
                        "an example when useful, and a short conclusion. "
                        "Use proper headings and avoid unnecessary detail.",

                    "Practical example":
                        "STRICT FORMAT: Start with a realistic practical situation "
                        "where this concept is actually used. Explain the situation "
                        "step by step, show exactly how the concept is applied, "
                        "and then explain the concept behind the example. "
                        "The response MUST contain a genuine practical example, "
                        "not only a definition.",

                    "Code explanation":
                        "STRICT FORMAT: If the question is related to programming, "
                        "first explain the concept briefly, then provide a small "
                        "complete code example in the correct programming language. "
                        "Explain the code step by step and include expected output "
                        "when useful. The response MUST contain actual code when "
                        "code is applicable. Do not give only theory.",
                }

                limit = (
                    1700
                    if answer_type == "Detailed explanation"
                    else 1100
                    if answer_type == "Exam answer"
                    else 500
                    if answer_type == "Short answer"
                    else 900
                )

                st.markdown(
                    ask_ai(
                        f"""
You are ByteVeda AI, a BCA study tutor.

Be accurate, helpful, and easy to understand.

Student question:
{question}

Required response style:
{answer_type}

IMPORTANT:
Follow the selected response style exactly.

{instructions[answer_type]}

Use simple BCA-level language.
Do not invent facts or pretend a concept is simpler than it is.
""",
                        limit,
                    )
                )

        else:
            st.warning("Please enter a question.")


elif st.session_state.page == "Programs":

    # Intentionally keeps the original program-generator workflow.
    page_header(
        "Programming Assistant",
        "Write a program, understand code, or paste code to find errors.",
    )

    language = st.selectbox(
        "Programming language",
        ["C", "C++", "Java", "Python"],
    )

    program_question = st.text_area(
        "What do you want to do?",
        placeholder="Example: Write a Java program to find the largest of three numbers.",
    )

    code = st.text_area(
        "Optional: paste your code",
        placeholder="Paste your program here if you want it explained or fixed.",
    )

    if st.button("Generate / explain program", type="primary"):

        if program_question.strip() or code.strip():

            with st.spinner("Working on your program..."):

                st.markdown(
                    ask_ai(
                        f"""
You are a programming assistant for a BCA student.

Language: {language}

Request:
{program_question}

Code:
{code}

If asked for a program, give correct runnable code,
a brief explanation, and expected output.

If code is supplied, identify errors, give corrected code,
and explain the correction.

Keep it clear.
""",
                        850,
                    )
                )

        else:
            st.warning(
                "Please enter a programming question or paste code."
            )


elif st.session_state.page == "Notes":

    page_header(
        "BCA Notes",
        "Upload your class notes, then turn them into easier revision material.",
    )

    uploaded = st.file_uploader(
        "Upload notes",
        type=["txt", "md", "pdf"],
        help="Your notes stay in this browser session and are not stored by the app.",
    )

    if uploaded:

        st.session_state.saved_notes = read_uploaded_notes(uploaded)

        st.success(f"Loaded: {uploaded.name}")

    notes = st.session_state.saved_notes

    if notes:

        with st.expander("Preview uploaded notes"):
            st.write(notes[:4000])

        if st.button("Remove uploaded notes"):
            st.session_state.saved_notes = ""
            st.rerun()

    else:
        st.info(
            "Upload a note to unlock summaries, revision questions, "
            "and note-based answers."
        )

    left, middle, right = st.columns(3)

    with left:

        if st.button("Summarise my notes", type="primary"):

            if notes.strip():

                with st.spinner("Creating revision notes..."):

                    st.markdown(
                        ask_ai(
                            f"""
Turn these BCA notes into a concise revision sheet
with headings, key definitions, and five quick recall points.

Do not add facts that are not in the notes.

NOTES:
{notes[:12000]}
""",
                            650,
                        )
                    )

            else:
                st.warning("Add or upload notes first.")

    with middle:

        if st.button("Create revision questions"):

            if notes.strip():

                with st.spinner("Creating revision questions..."):

                    st.markdown(
                        ask_ai(
                            f"""
Use only these BCA notes.

Create 10 useful revision questions:
6 short-answer and 4 longer-answer questions.

Put answers after a divider.

Do not add facts absent from the notes.

NOTES:
{notes[:12000]}
""",
                            800,
                        )
                    )

            else:
                st.warning("Upload notes first.")

    with right:

        note_question = st.text_input(
            "Ask about these notes",
            placeholder="What is the most important definition?",
        )

        if st.button("Ask from notes"):

            if notes.strip() and note_question.strip():

                with st.spinner("Reading your notes..."):

                    st.markdown(
                        ask_ai(
                            f"""
Answer only from these notes.

If the answer is absent, say so clearly.

Question:
{note_question}

NOTES:
{notes[:12000]}
""",
                            400,
                        )
                    )

            else:
                st.warning("Add notes and a question first.")

    st.caption(
        "Notes stay only in this browser session; they are not saved permanently by this app."
    )


elif st.session_state.page == "Interviews":

    page_header(
        "Interview Questions",
        "Practice technical and HR questions for your first internship or job.",
    )

    role = st.selectbox(
        "Target role",
        [
            "Software Developer",
            "Web Developer",
            "Data Analyst",
            "AI / ML Intern",
            "Cybersecurity Intern",
            "General IT Support",
        ],
    )

    difficulty = st.selectbox(
        "Level",
        ["Beginner", "Intermediate"],
    )

    starter_questions = {

        "Software Developer": [
            (
                "What is OOP?",
                "A programming approach that organizes code using objects and classes.",
            ),
            (
                "What is the difference between an array and a linked list?",
                "Arrays store items in contiguous positions; linked lists connect items through links.",
            ),
            (
                "Describe a project you built.",
                "Explain the problem, tools used, your contribution, and what you learned.",
            ),
        ],

        "Web Developer": [
            (
                "What is the difference between HTML, CSS, and JavaScript?",
                "HTML gives structure, CSS controls appearance, and JavaScript adds behaviour.",
            ),
            (
                "What is responsive design?",
                "Designing a site so it works well on phones, tablets, and desktops.",
            ),
            (
                "Show one web project.",
                "Explain its purpose, stack, key feature, and a challenge you solved.",
            ),
        ],

        "Data Analyst": [
            (
                "What is SQL used for?",
                "SQL is used to query, organise, and analyse data in databases.",
            ),
            (
                "What is the difference between a primary key and foreign key?",
                "A primary key uniquely identifies a row; a foreign key links tables.",
            ),
            (
                "How would you clean messy data?",
                "Check missing values, duplicates, inconsistent formats, and incorrect entries.",
            ),
        ],

        "AI / ML Intern": [
            (
                "What is machine learning?",
                "It is a method where systems learn patterns from data to make predictions or decisions.",
            ),
            (
                "What is overfitting?",
                "When a model learns training data too closely and performs poorly on new data.",
            ),
            (
                "Why split data into training and testing sets?",
                "To check whether a model works on data it did not learn from.",
            ),
        ],

        "Cybersecurity Intern": [
            (
                "What is phishing?",
                "A fake message or site designed to steal information.",
            ),
            (
                "What makes a strong password?",
                "A long, unique password plus multi-factor authentication.",
            ),
            (
                "What is the principle of least privilege?",
                "Giving users only the access they need to do their work.",
            ),
        ],

        "General IT Support": [
            (
                "How do you troubleshoot a slow computer?",
                "Check running programs, storage, updates, malware, and network connection.",
            ),
            (
                "What is an IP address?",
                "A number that identifies a device on a network.",
            ),
            (
                "How would you help a non-technical user?",
                "Listen calmly, explain in simple steps, and confirm the problem is solved.",
            ),
        ],
    }

    st.markdown("### Starter questions you can practise now")

    for question, answer in starter_questions[role]:

        with st.expander(question):
            st.write(answer)

    if st.button("Generate practice questions", type="primary"):

        with st.spinner("Preparing your practice set..."):

            st.markdown(
                ask_ai(
                    f"""
Create 8 {difficulty.lower()} interview questions
for a BCA student applying for a {role} role.

Include 6 technical and 2 HR/project questions.

For each, give a short model answer or what the interviewer looks for.

Keep it practical and concise.
""",
                    850,
                )
            )

    st.info(
        "Tip: say your answer aloud first, then use AI Tutor to improve it. "
        "Real interviews vary by company and role."
    )


elif st.session_state.page == "Study Plans":

    page_header(
        "Study Plans",
        "Make a realistic plan, finish small tasks, and learn without feeling overloaded.",
    )

    subject = st.selectbox(
        "What do you want to study?",
        [
            "Python",
            "Java",
            "DBMS / SQL",
            "Data Structures",
            "Web Development",
            "Computer Networks",
            "Operating Systems",
            "AI Basics",
        ],
    )

    available_time = st.selectbox(
        "Study time each day",
        ["30 minutes", "1 hour", "2 hours"],
    )

    goal = st.selectbox(
        "Your goal",
        [
            "Understand the basics",
            "Prepare for an exam",
            "Build a project",
            "Prepare for interviews",
        ],
    )

    if st.button("Create my 7-day plan", type="primary"):

        with st.spinner("Making a realistic plan..."):

            st.markdown(
                ask_ai(
                    f"""
Create a seven-day study plan for a BCA student
learning {subject}.

They have {available_time} daily and want to {goal.lower()}.

Each day needs one focused topic,
one small practice task,
and an approximate time split.

Make it beginner-friendly and realistic.
""",
                    800,
                )
            )

    st.markdown("### Today’s focus checklist")

    checklist = [
        "Read or watch one focused lesson",
        "Write notes in my own words",
        "Practice one problem or program",
        "Review yesterday's key point",
    ]

    completed = sum(
        st.checkbox(
            task,
            key=f"check_{index}",
        )
        for index, task in enumerate(checklist)
    )

    st.progress(
        completed / len(checklist),
        text=f"{completed} of {len(checklist)} small tasks complete",
    )

    st.caption(
        f"Small daily steps matter. Today is "
        f"{date.today().strftime('%d %b %Y')}; your next seven days run to "
        f"{(date.today() + timedelta(days=6)).strftime('%d %b %Y')}."
    )


elif st.session_state.page == "Mock Interview":

    page_header(
        "Mock Interview",
        "Practise one question at a time and get constructive feedback before the real interview.",
    )

    role = st.selectbox(
        "Interview role",
        [
            "Software Developer Intern",
            "Web Developer Intern",
            "Data Analyst Intern",
            "AI / ML Intern",
            "Cybersecurity Intern",
        ],
    )

    if st.button("Give me an interview question", type="primary"):

        with st.spinner("Choosing a realistic question..."):

            st.session_state.mock_question = ask_ai(
                f"""
Give one realistic beginner interview question
for a BCA student applying for a {role} role.

Ask only the question, followed by one short hint.

Do not provide the answer yet.
""",
                180,
            )

    if st.session_state.mock_question:

        st.markdown("### Your question")

        st.info(st.session_state.mock_question)

        answer = st.text_area(
            "Type your answer",
            placeholder="Answer as if you are in the interview...",
        )

        if st.button("Review my answer"):

            if answer.strip():

                with st.spinner("Reviewing your answer..."):

                    st.markdown(
                        ask_ai(
                            f"""
You are a supportive interviewer for a BCA student
applying for {role}.

Question:
{st.session_state.mock_question}

Student answer:
{answer}

Give:
1) a score out of 10,
2) two strong points,
3) two specific improvements,
4) an improved short sample answer.

Be honest, kind, and concise.
""",
                            650,
                        )
                    )

            else:
                st.warning("Type your answer first.")


elif st.session_state.page == "Career Kit":

    page_header(
        "Career Kit",
        "Build the basic proof recruiters look for: skills, projects, a clear resume, and interview readiness.",
    )

    st.markdown("### Fresher readiness checklist")

    readiness = [
        "One-page resume with contact details",
        "LinkedIn profile with a clear headline",
        "GitHub profile with 2–3 finished projects",
        "Projects have a README, screenshots, and setup steps",
        "Basic SQL, Git, and communication practice",
        "A tailored application for each role",
    ]

    score = sum(
        st.checkbox(
            item,
            key=f"ready_{number}",
        )
        for number, item in enumerate(readiness)
    )

    st.progress(
        score / len(readiness),
        text=f"Career readiness: {score}/{len(readiness)} essentials complete",
    )

    st.markdown("### Improve a project description")

    description = st.text_area(
        "Paste your project description",
        placeholder="Example: I made a student attendance app using Python...",
    )

    if st.button("Make my project description stronger"):

        if description.strip():

            with st.spinner("Improving your portfolio wording..."):

                st.markdown(
                    ask_ai(
                        f"""
Rewrite this BCA student's project description
for a resume or LinkedIn.

Keep it truthful, specific, simple, and under 80 words.

Add measurable results only if they appear
in the original text.

{description}
""",
                        250,
                    )
                )

        else:
            st.warning("Paste a project description first.")

    st.caption(
        "Do not paste passwords, ID numbers, financial details, "
        "or other sensitive information into any AI tool."
    )


elif st.session_state.page == "Careers":

    page_header(
        "Jobs & Internships",
        "Start with a skill path, build proof through projects, then apply through trusted portals and company career pages.",
    )

    st.markdown("### A beginner-friendly starting plan")

    items = [
        (
            "1. Pick a direction",
            "Choose web, software, data, AI, cybersecurity, or cloud.",
        ),
        (
            "2. Learn foundations",
            "Learn programming, Git/GitHub, SQL, and communication.",
        ),
        (
            "3. Build proof",
            "Finish 2–3 small projects and write a clear README.",
        ),
        (
            "4. Apply consistently",
            "Tailor your resume, apply, track, and practise interviews.",
        ),
    ]

    for column, (title, body) in zip(
        st.columns(4),
        items,
    ):

        with column:

            st.markdown(
                f"""
<div class='card'>
<h3>{title}</h3>
<p>{body}</p>
</div>
""",
                unsafe_allow_html=True,
            )

    st.markdown("### Choose a roadmap")

    path = st.selectbox(
        "Career direction",
        [
            "Software / Web Development",
            "Data Analytics",
            "AI / Machine Learning",
            "Cybersecurity",
            "Cloud / IT Support",
        ],
    )

    if st.button("Create my roadmap", type="primary"):

        with st.spinner("Building a practical roadmap..."):

            st.markdown(
                ask_ai(
                    f"""
Create a practical 12-week beginner roadmap
for a BCA student targeting {path}.

Include:
- skills in order,
- free tools,
- 2 portfolio projects,
- GitHub steps,
- internship interview preparation.

Be realistic: do not guarantee a job.

Use short weekly sections.
""",
                    850,
                )
            )

    st.markdown("### Essential skills for every BCA fresher")

    skill_columns = st.columns(3)

    for column, title, detail in zip(
        skill_columns,
        ["Technical", "Proof of skill", "Career skills"],
        [
            "One programming language, SQL, Git/GitHub, and basic problem-solving.",
            "Two finished projects, clear READMEs, and a one-page resume.",
            "Communication, a LinkedIn profile, interview practice, and safe applications.",
        ],
    ):

        with column:

            st.markdown(
                f"""
<div class='card'>
<h3>{title}</h3>
<p>{detail}</p>
</div>
""",
                unsafe_allow_html=True,
            )

    st.markdown("### Apply through trusted places")

    st.markdown(
        """
<div class='resource'>
<b>India job & internship portals</b><br>
<a href='https://www.linkedin.com/jobs/' target='_blank'>LinkedIn Jobs</a> ·
<a href='https://internshala.com/internships/' target='_blank'>Internshala</a> ·
<a href='https://www.ncs.gov.in/' target='_blank'>National Career Service (India)</a> ·
<a href='https://www.naukri.com/' target='_blank'>Naukri</a>
</div>

<div class='resource'>
<b>Company career pages</b> — search roles by city/country and set alerts.<br>
<a href='https://www.tcs.com/careers' target='_blank'>TCS</a> ·
<a href='https://www.infosys.com/careers.html' target='_blank'>Infosys</a> ·
<a href='https://www.accenture.com/in-en/careers' target='_blank'>Accenture</a> ·
<a href='https://www.google.com/about/careers/applications/jobs/results/' target='_blank'>Google Careers</a> ·
<a href='https://jobs.careers.microsoft.com/global/en/search' target='_blank'>Microsoft Careers</a>
</div>
""",
        unsafe_allow_html=True,
    )

    st.caption(
        "Opportunities change frequently. Apply only through official company pages "
        "or established portals; never pay a fee for a job or internship."
    )

    st.markdown("### Free learning and credential resources")

    resources = [
        (
            "freeCodeCamp",
            "Free programming certifications and project-based practice.",
            "https://www.freecodecamp.org/learn/",
        ),
        (
            "Microsoft Learn",
            "Free self-paced technical training and learning paths.",
            "https://learn.microsoft.com/training/",
        ),
        (
            "IBM SkillsBuild",
            "Free career-focused courses and digital credentials.",
            "https://skillsbuild.org/",
        ),
        (
            "Cisco Skills for All",
            "Free networking, cybersecurity, and Python learning.",
            "https://www.skillsforall.com/",
        ),
        (
            "Google Skillshop",
            "Free Google product training and certifications.",
            "https://skillshop.withgoogle.com/",
        ),
    ]

    for name, description, url in resources:

        st.markdown(
            f"""
<div class='resource'>
<a href='{url}' target='_blank'><b>{name}</b></a><br>
<span class='muted'>{description}</span>
</div>
""",
            unsafe_allow_html=True,
        )

    career_question = st.text_area(
        "Ask a career question",
        placeholder="Example: Which cities and companies should a web-development fresher target in India?",
    )

    if st.button("Get career guidance"):

        if career_question.strip():

            with st.spinner("Preparing practical guidance..."):

                st.markdown(
                    ask_ai(
                        f"""
You are a careful BCA career advisor.

Answer:
{career_question}

Give practical next steps, skills, project ideas,
and application advice.

You may mention common Indian tech hubs such as
Bengaluru, Hyderabad, Pune, Chennai, Gurugram,
and Mumbai when relevant, but do not claim a vacancy exists.

Tell the student to verify openings through official career pages.

Keep it concise.
""",
                        600,
                    )
                )

        else:
            st.warning("Please enter a career question.")


st.markdown("---")

st.caption(
    "🎓 ByteVeda AI • Learn BCA • Build skills • Shape your career"
)