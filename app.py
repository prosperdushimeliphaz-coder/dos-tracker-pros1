import streamlit as st
import os
from openai import OpenAI
from io import BytesIO
from reportlab.pdfgen import canvas
from reportlab.lib.pagesizes import A4

# Connect to OpenAI API via environment variable
client = OpenAI(api_key=os.getenv("OPENAI_API_KEY"))

st.title("📘 Rwanda Teacher Lesson Plan AI Assistant")
st.markdown("Fill in basic details. AI will generate the rest of the lesson plan.")

# --- User Inputs ---
term = st.text_input("Term")
subject = st.text_input("Subject")
school_class = st.text_input("Class (e.g., S1, S2)")
unit_no = st.text_input("Unit Number")
lesson_no = st.text_input("Lesson Number")
num_learners = st.number_input("Number of learners", min_value=1, step=1)
unit_title = st.text_input("Unit Title")
key_competence = st.text_area("Key Unit Competence")
lesson_title = st.text_input("Lesson Title")
special_needs = st.text_area("Special Educational Needs")
self_eval = st.text_area("Teacher’s Self Evaluation")

if st.button("Generate Lesson Plan"):

    # Prepare AI prompt
    prompt = f"""
    Create a detailed lesson plan for Rwanda Competence-Based Curriculum.
    Inputs:
    Term: {term}
    Subject: {subject}
    Class: {school_class}
    Unit No.: {unit_no}
    Lesson No.: {lesson_no}
    Number of learners: {num_learners}
    Unit Title: {unit_title}
    Key Unit Competence: {key_competence}
    Lesson Title: {lesson_title}
    Special Needs: {special_needs}
    Teacher’s Self Evaluation: {self_eval}
    
    Output:
    - Learning Objectives (with measurable verbs + adverbs)
    - Teaching/Learning Activities
    - Teacher’s Activities (Intro, Body, Conclusion with sample questions)
    - Learner’s Activities (Intro, Body, Conclusion)
    - Teaching Aids
    - Assessment Methods
    Format as a clean lesson plan.
    """

    # Call OpenAI API
    response = client.chat.completions.create(
        model="gpt-4o-mini",
        messages=[{"role": "user", "content": prompt}],
        temperature=0.6
    )

    lesson_plan = response.choices[0].message.content

    st.subheader("Generated Lesson Plan")
    st.write(lesson_plan)

    # --- PDF Download ---
    buffer = BytesIO()
    p = canvas.Canvas(buffer, pagesize=A4)
    width, height = A4
    y = height - 50
    p.setFont("Helvetica-Bold", 14)
    p.drawString(180, y, "Lesson Plan")
    y -= 40

    p.setFont("Helvetica", 11)
    for line in lesson_plan.split("\n"):
        p.drawString(50, y, line)
        y -= 15
        if y < 50:  # new page
            p.showPage()
            y = height - 50
            p.setFont("Helvetica", 11)
    p.save()
    buffer.seek(0)

    st.download_button("Download Lesson Plan as PDF", buffer, file_name="lesson_plan.pdf")
