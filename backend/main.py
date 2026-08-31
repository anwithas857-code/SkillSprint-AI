
from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import FileResponse
from pydantic import BaseModel
from pathlib import Path
import sqlite3, json, math
from datetime import datetime, timedelta

BASE = Path(__file__).resolve().parent
DB = BASE / "skillsprint.db"
FRONTEND = BASE.parent / "frontend" / "index.html"

app.add_middleware(
    CORSMiddleware,
    allow_origins=[
        "https://anwithas857-code.github.io"
    ],
    allow_credentials=False,
    allow_methods=["*"],
    allow_headers=["*"]
)

ROLE_SKILLS = {
    "Data Analyst": ["Python", "SQL", "Data Visualisation", "Statistics", "Communication"],
    "Software Developer": ["Python", "JavaScript", "Problem Solving", "Git", "Communication"],
    "AI/ML Engineer": ["Python", "Math", "Machine Learning", "SQL", "Communication"],
    "UI/UX Designer": ["UX Research", "Figma", "Visual Design", "Prototyping", "Communication"],
    "Digital Marketer": ["Content", "Analytics", "SEO", "Social Media", "Communication"],
}

QUESTIONS = {
    "Data Analyst": [
        ("SQL", "Which SQL statement filters rows from a table?", ["SELECT ... WHERE", "GROUP BY only", "ORDER BY only", "JOIN only"], 0),
        ("SQL", "What is a JOIN mainly used for?", ["Combining related data from tables", "Deleting a database", "Formatting text", "Making charts"], 0),
        ("Data Visualisation", "Which chart is usually suitable for showing a trend over time?", ["Line chart", "Pie chart", "Scatter only", "Histogram only"], 0),
        ("Statistics", "What does the mean represent?", ["Average value", "Most frequent value", "Middle value only", "Largest value"], 0),
        ("Python", "Which Python structure stores key-value pairs?", ["Dictionary", "List only", "Tuple only", "String"], 0),
        ("Communication", "What is most useful when presenting an analytical insight?", ["Evidence and a clear explanation", "Only technical jargon", "No context", "More slides regardless of content"], 0),
    ],
    "Software Developer": [
        ("Python", "Which keyword defines a function in Python?", ["def", "func", "function", "define"], 0),
        ("JavaScript", "Which keyword declares a block-scoped variable?", ["let", "varname", "define", "newvar"], 0),
        ("Problem Solving", "What is a good first step when debugging?", ["Reproduce and isolate the problem", "Rewrite everything", "Ignore the error", "Delete the project"], 0),
        ("Git", "Which command records staged changes?", ["git commit", "git start", "git save", "git upload"], 0),
        ("Communication", "A good code review comment should be:", ["Specific and constructive", "Personal", "Vague", "Only negative"], 0),
    ],
    "AI/ML Engineer": [
        ("Python", "Which Python library is commonly used for numerical arrays?", ["NumPy", "Flask", "BeautifulSoup", "Requests only"], 0),
        ("Math", "What does a probability value range from?", ["0 to 1", "1 to 100 only", "-100 to 100", "0 to infinity only"], 0),
        ("Machine Learning", "What is a training set used for?", ["Learning model parameters", "Only displaying results", "Deleting features", "Formatting a report"], 0),
        ("SQL", "Why might ML engineers use SQL?", ["To retrieve and prepare data", "Only to draw UI", "To replace Python", "To create animations"], 0),
        ("Communication", "When explaining a model, you should include:", ["Assumptions, results and limitations", "Only accuracy", "Only code", "No context"], 0),
    ],
    "UI/UX Designer": [
        ("UX Research", "What is a user interview mainly for?", ["Understanding user needs and experiences", "Choosing database indexes", "Writing backend code", "Compressing images"], 0),
        ("Figma", "Figma is primarily used for:", ["Interface design and prototyping", "SQL queries", "Server hosting", "Data mining"], 0),
        ("Visual Design", "Contrast helps improve:", ["Readability and hierarchy", "Database speed", "API latency", "File compression"], 0),
        ("Prototyping", "A prototype is useful for:", ["Testing an interaction before full build", "Replacing all research", "Deploying a server", "Training an ML model"], 0),
        ("Communication", "A design rationale should explain:", ["Why a design decision supports the user", "Only personal preference", "Only colors", "Nothing"], 0),
    ],
    "Digital Marketer": [
        ("Content", "A strong piece of content should first provide:", ["Value to the target audience", "Random keywords", "Only promotion", "No clear purpose"], 0),
        ("Analytics", "A conversion rate measures:", ["The proportion completing a desired action", "Only page color", "Server uptime", "Number of employees"], 0),
        ("SEO", "SEO primarily aims to improve:", ["Search visibility", "Screen brightness", "Database storage", "Email encryption"], 0),
        ("Social Media", "Engagement can include:", ["Comments, shares and saves", "Only impressions", "Only page load time", "Server CPU"], 0),
        ("Communication", "A good campaign brief should define:", ["Audience, objective and message", "Only a logo", "Only a budget", "No measurable goal"], 0),
    ],
}

COURSES = {
    "SQL": ["SQL for Data Analysis", "Beginner", "Queries, filtering, joins and real datasets"],
    "Data Visualisation": ["Data Visualisation Fundamentals", "Beginner", "Charts, dashboards and data storytelling"],
    "Statistics": ["Statistics for Data Analytics", "Beginner", "Descriptive statistics, probability and interpretation"],
    "Python": ["Python for Problem Solving", "Beginner", "Core Python, functions and practical exercises"],
    "Communication": ["Professional Communication", "Beginner", "Explain ideas clearly with evidence"],
    "JavaScript": ["JavaScript Foundations", "Beginner", "Modern JavaScript and browser fundamentals"],
    "Problem Solving": ["Problem Solving Patterns", "Intermediate", "Decomposition, debugging and algorithms"],
    "Git": ["Git & GitHub Essentials", "Beginner", "Version control and collaboration"],
    "Math": ["Math Foundations for AI", "Beginner", "Probability, linear algebra and model intuition"],
    "Machine Learning": ["Machine Learning Foundations", "Beginner", "Supervised learning and evaluation"],
    "UX Research": ["UX Research Essentials", "Beginner", "Interviews, personas and usability testing"],
    "Figma": ["Figma UI Foundations", "Beginner", "Components, layouts and prototypes"],
    "Visual Design": ["Visual Design Fundamentals", "Beginner", "Hierarchy, contrast and typography"],
    "Prototyping": ["Rapid Prototyping", "Beginner", "Wireframes, flows and interactive prototypes"],
    "Content": ["Content Strategy Basics", "Beginner", "Audience, messaging and content planning"],
    "Analytics": ["Marketing Analytics", "Beginner", "KPIs, funnels and campaign measurement"],
    "SEO": ["SEO Foundations", "Beginner", "Search intent, on-page SEO and measurement"],
    "Social Media": ["Social Media Strategy", "Beginner", "Content calendars, engagement and measurement"],
}

def conn():
    c = sqlite3.connect(DB)
    c.row_factory = sqlite3.Row
    return c

def init_db():
    c = conn()
    c.executescript("""
    CREATE TABLE IF NOT EXISTS students(
      id INTEGER PRIMARY KEY AUTOINCREMENT, name TEXT NOT NULL, role TEXT NOT NULL,
      hours INTEGER DEFAULT 8, created_at TEXT NOT NULL
    );
    CREATE TABLE IF NOT EXISTS answers(
      id INTEGER PRIMARY KEY AUTOINCREMENT, student_id INTEGER, skill TEXT,
      question TEXT, selected INTEGER, correct INTEGER, created_at TEXT
    );
    CREATE TABLE IF NOT EXISTS progress(
      id INTEGER PRIMARY KEY AUTOINCREMENT, student_id INTEGER, skill TEXT,
      course TEXT, done INTEGER DEFAULT 0, due_date TEXT, updated_at TEXT
    );
    CREATE TABLE IF NOT EXISTS reminders(
      id INTEGER PRIMARY KEY AUTOINCREMENT, student_id INTEGER, text TEXT,
      due_date TEXT, done INTEGER DEFAULT 0
    );
    """)
    c.commit(); c.close()

init_db()

class Profile(BaseModel):
    name: str
    role: str
    hours: int = 8

class Answer(BaseModel):
    student_id: int
    skill: str
    question: str
    selected: int
    correct: int

class Complete(BaseModel):
    student_id: int
    progress_id: int

@app.get("/")
def home():
    return FileResponse(FRONTEND)

@app.get("/api/health")
def health():
    return {"status":"ok","message":"SkillSprint AI backend is running"}

@app.post("/api/students")
def create_student(p: Profile):
    if p.role not in ROLE_SKILLS: raise HTTPException(400, "Invalid career")
    c=conn(); cur=c.execute(
        "INSERT INTO students(name,role,hours,created_at) VALUES(?,?,?,?)",
        (p.name.strip() or "Student",p.role,max(2,min(40,p.hours)),datetime.now().isoformat())
    )
    sid=cur.lastrowid
    c.commit(); c.close()
    return {"id":sid,"name":p.name.strip() or "Student","role":p.role,"hours":p.hours}

@app.get("/api/questions/{student_id}")
def get_questions(student_id:int):
    c=conn(); s=c.execute("SELECT * FROM students WHERE id=?",(student_id,)).fetchone(); c.close()
    if not s: raise HTTPException(404,"Student not found")
    return [{"id":i,"skill":q[0],"question":q[1],"options":q[2]} for i,q in enumerate(QUESTIONS[s["role"]])]

@app.post("/api/answers")
def save_answer(a: Answer):
    c=conn()
    c.execute("""INSERT INTO answers(student_id,skill,question,selected,correct,created_at)
                VALUES(?,?,?,?,?,?)""",(a.student_id,a.skill,a.question,a.selected,a.correct,datetime.now().isoformat()))
    c.commit(); c.close()
    return {"ok":True}

def scores(student_id):
    c=conn(); s=c.execute("SELECT * FROM students WHERE id=?",(student_id,)).fetchone()
    if not s: raise HTTPException(404,"Student not found")
    rows=c.execute("SELECT skill, correct FROM answers WHERE student_id=?",(student_id,)).fetchall()
    c.close()
    base={k:50 for k in ROLE_SKILLS[s["role"]]}
    grouped={k:[] for k in base}
    for r in rows:
        if r["skill"] in grouped: grouped[r["skill"]].append(r["correct"])
    for skill in base:
        vals=grouped[skill]
        if vals: base[skill]=round(30+70*(sum(vals)/len(vals)))
    # Keep unassessed skills visible but clearly provisional.
    overall=round(sum(base.values())/len(base))
    return s,base,overall

@app.get("/api/analysis/{student_id}")
def analysis(student_id:int):
    s,sk,overall=scores(student_id)
    weakest=min(sk,key=sk.get); strongest=max(sk,key=sk.get)
    gap=max(0,100-overall)
    return {
        "student":{"id":s["id"],"name":s["name"],"role":s["role"],"hours":s["hours"]},
        "skills":sk,"overall":overall,"gap":gap,"weakest":weakest,"strongest":strongest,
        "insight":f"Your strongest current area is {strongest} ({sk[strongest]}%). Your biggest opportunity is {weakest} ({sk[weakest]}%). Focus there first, then prove it with a small project.",
        "capability": f"At {overall}% current readiness, you are building toward an entry-level {s['role']} path. Reaching about 80% with consistent practice and portfolio evidence would put you in a much stronger position.",
    }

@app.get("/api/courses/{student_id}")
def courses(student_id:int):
    _,sk,_=scores(student_id)
    weak=sorted(sk.items(),key=lambda x:x[1])
    c=conn()
    out=[]
    for skill,score in weak[:3]:
        item=COURSES.get(skill,[f"{skill} Skill Builder","Beginner","Focused practice and a mini project"])
        existing=c.execute("SELECT id,done FROM progress WHERE student_id=? AND skill=? ORDER BY id DESC LIMIT 1",(student_id,skill)).fetchone()
        out.append({"skill":skill,"score":score,"title":item[0],"level":item[1],"description":item[2],
                    "progress_id": existing["id"] if existing else None,"done":bool(existing["done"]) if existing else False})
    c.close(); return out

@app.post("/api/progress")
def create_progress(a: Complete):
    c=conn()
    r=c.execute("SELECT * FROM progress WHERE id=? AND student_id=?",(a.progress_id,a.student_id)).fetchone()
    if not r: raise HTTPException(404,"Progress item not found")
    c.execute("UPDATE progress SET done=1,updated_at=? WHERE id=?",(datetime.now().isoformat(),a.progress_id))
    c.commit(); c.close()
    return {"ok":True}

@app.post("/api/progress/start/{student_id}/{skill}")
def start_course(student_id:int,skill:str):
    item=COURSES.get(skill,[f"{skill} Skill Builder","Beginner","Focused practice"])
    due=(datetime.now()+timedelta(days=7)).date().isoformat()
    c=conn()
    cur=c.execute("INSERT INTO progress(student_id,skill,course,done,due_date,updated_at) VALUES(?,?,?,?,?,?)",
                  (student_id,skill,item[0],0,due,datetime.now().isoformat()))
    c.commit(); pid=cur.lastrowid; c.close()
    return {"id":pid,"due_date":due}

@app.get("/api/dashboard/{student_id}")
def dashboard(student_id:int):
    s,sk,overall=scores(student_id)
    c=conn()
    prog=c.execute("SELECT * FROM progress WHERE student_id=? ORDER BY id DESC",(student_id,)).fetchall()
    reminders=c.execute("SELECT * FROM reminders WHERE student_id=? ORDER BY done,due_date",(student_id,)).fetchall()
    c.close()
    done=sum(1 for p in prog if p["done"])
    progress_pct=round(done/max(1,len(prog))*100)
    return {"student":dict(s),"skills":sk,"overall":overall,"gap":max(0,100-overall),
            "progress_pct":progress_pct,"progress":[dict(p) for p in prog],
            "reminders":[dict(r) for r in reminders]}

@app.post("/api/reminders/{student_id}")
def make_reminder(student_id:int):
    c=conn()
    s=c.execute("SELECT * FROM students WHERE id=?",(student_id,)).fetchone()
    if not s: raise HTTPException(404,"Student not found")
    _,sk,_=scores(student_id); weak=min(sk,key=sk.get)
    due=(datetime.now()+timedelta(days=2)).date().isoformat()
    text=f"Practice {weak} for 30 minutes"
    c.execute("INSERT INTO reminders(student_id,text,due_date) VALUES(?,?,?)",(student_id,text,due))
    c.commit(); c.close()
    return {"ok":True,"text":text,"due_date":due}

@app.get("/api/career/{student_id}")
def career(student_id:int):
    s,sk,overall=scores(student_id)
    if overall>=80: stage="Strong entry-level readiness"
    elif overall>=65: stage="Developing — close the most important gaps"
    else: stage="Early foundation — build core skills first"
    return {"role":s["role"],"overall":overall,"improve_to_80":max(0,80-overall),
            "stage":stage,"skills":sk,
            "actions":[f"Raise {min(sk,key=sk.get)} through focused practice",
                        "Complete one portfolio project",
                        "Update your resume with evidence",
                        "Re-assess after 2–4 weeks"]}
