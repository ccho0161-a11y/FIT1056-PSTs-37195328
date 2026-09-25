# gui/student_pages.py
import streamlit as st

def show_student_management_page(manager):
    """Renders all components for the student management page."""
    st.header("Student Management")

    # --- Registration Section (now works correctly) ---
    st.subheader("Register New Student")
    with st.form("registration_form"):
        reg_name = st.text_input("New Student Name")
        reg_instrument = st.text_input("First Instrument")
        submitted = st.form_submit_button("Register Student")
        
        if submitted:
            if reg_name.strip() and reg_instrument.strip():
                new_student = manager.register_new_student(reg_name.strip(), reg_instrument.strip())
                if new_student:
                    st.success(f"Successfully registered {reg_name.strip()}!")
                    st.balloons()
                else:
                    st.error(f"Could not register student. A teacher for {reg_instrument} might not be available.")
            else:
                st.warning("Please enter both a name and an instrument.")
     # --- Update Section ---
    st.subheader("Update Student")
    with st.form("update_form"):
        update_id = st.number_input("Student ID", min_value=1, step=1)
        new_name = st.text_input("New Name (leave blank to skip)")
        update_submitted = st.form_submit_button("Update Student")
 
        if update_submitted:
            success, result = manager.update_student(int(update_id), new_name)
            if success:
                st.success(f"Student {result.id} updated to '{result.name}'.")
            else:
                st.error(result)
 
    st.divider()
 
    # --- Remove Section ---
    st.subheader("Remove Student")
    with st.form("remove_form"):
        remove_id = st.number_input("Student ID to remove", min_value=1, step=1, key="remove_id")
        remove_submitted = st.form_submit_button("Remove Student")
 
        if remove_submitted:
            success, message = manager.remove_student(int(remove_id))
            if success:
                st.success(message)
            else:
                st.error(message)
 
    st.divider()
 
    # --- Enrol in Course Section ---
    st.subheader("Enrol Student in Course")
    with st.form("enrol_form"):
        enrol_student_id = st.number_input("Student ID", min_value=1, step=1, key="enrol_student_id")
        enrol_course_id = st.number_input("Course ID", min_value=1, step=1, key="enrol_course_id")
        enrol_submitted = st.form_submit_button("Enrol")
 
        if enrol_submitted:
            success, message = manager.enrol_student_in_course(int(enrol_student_id), int(enrol_course_id))
            if success:
                st.success(message)
            else:
                st.error(message)
 
    st.divider()
 
    # --- Switch Course Section ---
    st.subheader("Switch Student's Course")
    with st.form("switch_form"):
        switch_student_id = st.number_input("Student ID", min_value=1, step=1, key="switch_student_id")
        from_course_id = st.number_input("From Course ID", min_value=1, step=1, key="from_course_id")
        to_course_id = st.number_input("To Course ID", min_value=1, step=1, key="to_course_id")
        switch_submitted = st.form_submit_button("Switch Course")
 
        if switch_submitted:
            success, message = manager.switch_student_course(
                int(switch_student_id), int(from_course_id), int(to_course_id)
            )
            if success:
                st.success(message)
            else:
                st.error(message)
 
    st.divider()
 
    # --- Student Card Section ---
    st.subheader("Print Student Card")
    with st.form("card_form"):
        card_student_id = st.number_input("Student ID", min_value=1, step=1, key="card_student_id")
        card_submitted = st.form_submit_button("Generate Card")

        if card_submitted:
            success, result = manager.print_student_card(int(card_student_id))
            if success:
                st.success(f"Card generated: {result}")
                st.session_state.last_card_file = result
            else:
                st.error(result)
                st.session_state.last_card_file = None

    # Download button lives OUTSIDE the form
    if st.session_state.get("last_card_file"):
        with open(st.session_state.last_card_file, "r") as f:
            st.download_button("Download Card", f.read(), file_name=st.session_state.last_card_file)
 
    st.divider()
 
    # --- List All Students ---
    st.subheader("All Students")
    students = manager.list_students()
    if students:
        students = sorted(students, key=lambda s: s['id'])
        for s in students:
            st.write(f"**ID {s['id']}** — {s['name']} — Enrolled in: {', '.join(s['enrolled_in']) or 'None'}")
    else:
        st.info("No students registered yet.")