# gui/teacher_pages.py
import streamlit as st
import pandas as pd


def show_teacher_management_page(manager):
    """Renders all components for the teacher management page."""
    st.header("Teacher Management")

    # --- Registration Section ---
    st.subheader("Register New Teacher")
    with st.form("teacher_registration_form"):
        reg_name = st.text_input("New Teacher Name")
        reg_speciality = st.text_input("Speciality (e.g. Piano, Guitar)")
        submitted = st.form_submit_button("Register Teacher")

        if submitted:
            if reg_name.strip() and reg_speciality.strip():
                new_teacher = manager.register_new_teacher(reg_name.strip(), reg_speciality.strip())
                st.success(f"Successfully registered {new_teacher.name} (ID {new_teacher.id}).")
            else:
                st.warning("Please enter both a name and a speciality.")

    st.divider()

    # --- Update Section ---
    st.subheader("Update Teacher")
    with st.form("teacher_update_form"):
        update_id = st.number_input("Teacher ID", min_value=1, step=1)
        new_name = st.text_input("New Name (leave blank to skip)", key="teacher_new_name")
        new_speciality = st.text_input("New Speciality (leave blank to skip)", key="teacher_new_speciality")
        update_submitted = st.form_submit_button("Update Teacher")

        if update_submitted:
            success, result = manager.update_teacher(int(update_id), new_name, new_speciality)
            if success:
                st.success(f"Teacher {result.id} updated: {result.name}, {result.speciality}.")
            else:
                st.error(result)

    st.divider()

    # --- Remove Section ---
    st.subheader("Remove Teacher")
    with st.form("teacher_remove_form"):
        remove_id = st.number_input("Teacher ID to remove", min_value=1, step=1, key="teacher_remove_id")
        remove_submitted = st.form_submit_button("Remove Teacher")

        if remove_submitted:
            success, message = manager.remove_teacher(int(remove_id))
            if success:
                st.success(message)
            else:
                st.error(message)

    st.divider()

    # --- List All Teachers ---
    st.subheader("All Teachers")
    teachers = manager.list_teachers()
    for t in teachers:
        st.write(f"**ID {t['id']}** — {t['name']} — Speciality: {t['speciality']}")
    else:
        st.info("No teachers registered yet.")

    st.divider()

    # --- Add Course Section ---
    st.subheader("Add New Course")
    with st.form("add_course_form"):
        course_name = st.text_input("Course Name")
        course_instrument = st.text_input("Instrument")
        course_teacher_id = st.number_input("Teacher ID", min_value=1, step=1, key="course_teacher_id")
        course_submitted = st.form_submit_button("Add Course")

        if course_submitted:
            if course_name.strip() and course_instrument.strip():
                success, result = manager.add_course(
                    course_name.strip(), course_instrument.strip(), int(course_teacher_id)
                )
                if success:
                    st.success(f"Course '{result.name}' added with ID {result.id}.")
                else:
                    st.error(result)
            else:
                st.warning("Please enter both a course name and instrument.")