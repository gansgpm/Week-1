import streamlit as st


# ---------------------------------------------------------------
# Day 2 grading logic (brought over unchanged)
# ---------------------------------------------------------------
def get_grade(mark):
    if mark >= 90:
        return "A"
    elif mark >= 80:
        return "B"
    elif mark >= 70:
        return "C"
    elif mark >= 60:
        return "D"
    else:
        return "F"


# ---------------------------------------------------------------
# Page setup
# ---------------------------------------------------------------
st.set_page_config(page_title="Student Grade Manager", page_icon="🎓")
st.title("🎓 Student Grade Manager")

# Streamlit reruns this whole file on every interaction.
# session_state is the only place data survives between reruns,
# so the student list is created once and then reused.
if "students" not in st.session_state:
    st.session_state.students = []

# ---------------------------------------------------------------
# Form to add a student
# ---------------------------------------------------------------
with st.form("add", clear_on_submit=True):
    col1, col2 = st.columns([2, 1])
    name = col1.text_input("Name")
    mark = col2.number_input("Mark", min_value=0, max_value=100, step=1, value=0)

    if st.form_submit_button("Add"):
        clean_name = name.strip()
        if not clean_name:
            st.error("Please enter a student name.")
        elif not 0 <= mark <= 100:
            st.error("Mark must be between 0 and 100.")
        else:
            st.session_state.students.append(
                {"Name": clean_name, "Mark": int(mark), "Grade": get_grade(mark)}
            )
            st.success(f"Added {clean_name} ({int(mark)}, grade {get_grade(mark)})")

# ---------------------------------------------------------------
# Results table and class metrics
# ---------------------------------------------------------------
if st.session_state.students:
    students = st.session_state.students
    marks = [s["Mark"] for s in students]

    st.subheader("Class Results")
    st.table(students)

    m1, m2, m3 = st.columns(3)
    m1.metric("Average", f"{sum(marks) / len(marks):.1f}")
    m2.metric("Highest", max(marks))
    m3.metric("Lowest", min(marks))

    if st.button("Clear all students"):
        st.session_state.students = []
        st.rerun()
else:
    st.info("No students yet. Add one using the form above.")
