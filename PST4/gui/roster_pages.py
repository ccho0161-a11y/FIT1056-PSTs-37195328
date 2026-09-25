# gui/roster_pages.py
import streamlit as st
import pandas as pd

def show_roster_page(manager):
    """Renders the daily roster and check-in functionality."""
    st.header("Daily Roster")

    # --- View Roster Section (remains the same) ---
    day = st.selectbox("Select a day", ["Monday", "Tuesday", "Wednesday", "Thursday", "Friday"])

    daily_lessons = manager.getting_daily_lessons(day)
    if daily_lessons:
        rows = [
            {
                "Course": course.name,
                "Instrument": course.instrument,
                "Start Time": lesson.get("start_time"),
                "Room": lesson.get("room"),
            }
            for course, lesson in daily_lessons
        ]
        st.dataframe(pd.DataFrame(rows))
    else:
        st.info(f"No lessons scheduled for {day}.")
    
    # --- Student Check-in Section (now works correctly) ---
    st.subheader("Student Check-in")
    with st.form("check_in_form"):
        student_list = {s.name: s.id for s in manager.students}
        course_list = {c.name: c.id for c in manager.courses}
        
        selected_student_name = st.selectbox("Select Student", student_list.keys())
        selected_course_name = st.selectbox("Select Course", course_list.keys())
        
        submitted = st.form_submit_button("Check-in Student")

        if submitted:
            student_id = student_list[selected_student_name]
            course_id = course_list[selected_course_name]

            success, message = manager.check_in(student_id, course_id)

            if success:
                st.success(message)
            else:
                st.error(message)

    st.divider()
    st.subheader("Schedule New Lesson")
    with st.form("schedule_lesson_form"):
        lesson_course_id = st.number_input("Course ID", min_value=1, step=1, key="lesson_course_id")
        lesson_day = st.selectbox("Day", ["Monday", "Tuesday", "Wednesday", "Thursday", "Friday"], key="lesson_day")
        lesson_time = st.text_input("Start Time (e.g. 16:00)", key="lesson_time")
        lesson_room = st.text_input("Room", key="lesson_room")
        lesson_submitted = st.form_submit_button("Schedule Lesson")

        if lesson_submitted:
            if lesson_time.strip() and lesson_room.strip():
                success, result = manager.schedule_lesson(
                    int(lesson_course_id), lesson_day, lesson_time.strip(), lesson_room.strip()
                )
                if success:
                    st.success(f"Lesson scheduled: {result['day']} at {result['start_time']} in {result['room']}.")
                else:
                    st.error(result)
            else:
                st.warning("Please enter a start time and room.")