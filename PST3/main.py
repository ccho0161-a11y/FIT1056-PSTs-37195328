# main.py - The View Layer
from app.schedule import ScheduleManager

def front_desk_daily_roster(manager, day):
    """Displays a pretty table of all lessons on a given day."""
    print(f"\n--- Daily Roster for {day} ---")
    day_lessons = manager.getting_daily_lessons(day)

    if not day_lessons:
        print(f"No lessons scheduled for {day}.")
        return

    for course, lesson in day_lessons:
        teacher = manager.find_teacher_by_id(course.teacher_id)
        teacher_name = teacher.name if teacher else "Unknown"
        print(f"{lesson['start_time']} - {course.name} with {teacher_name} in {lesson['room']}")
    

def switch_course(manager, student_id, from_course_id, to_course_id):
    """Handles switching a student between two courses"""
    manager.switch_student_course(student_id, from_course_id, to_course_id)

def main():
    """Main function to run the MSMS application."""
    manager = ScheduleManager() # Create ONE instance of the application brain.
    print(f"DEBUG: Loaded {len(manager.courses)} courses, {len(manager.students)} students.")
    
    while True:
        print("\n===== MSMS v3 (Object-Oriented) =====")
        # TODO: Create a menu for the new PST3 functions.
        # Get user input and call the appropriate view function, passing 'manager' to it.
        print("1. Daily lessons")
        print("2. Switch a class")
        print("3. Add a student")
        print("4. View all existing students")
        print("5. View all existing teachers")
        print("6. Update student information")
        print("7. Update teacher information")
        print("8. Check in a student")
        print("9. Add a student to a class")
        print("q. Quit")
        choice = input("Enter choice: ")
        if choice == '1':
            day = input("Enter day (e.g., Monday): ")
            front_desk_daily_roster(manager, day)

        elif choice == '2':
            try:
                student_id = int(input("Enter a student ID: "))
                from_course_id = int(input("Enter current course ID: "))
                to_course_id = int(input("Enter new course ID: "))
                switch_course(manager, student_id, from_course_id, to_course_id)
            except ValueError:
                print("Invalid ID. Please enter a number.")
        elif choice == '3':
            manager.add_student()

        elif choice == '4':
            manager.list_students()

        elif choice == '5':
            manager.list_teachers()

        elif choice == '6':
            manager.update_student()

        elif choice == '7':
            manager.update_teacher()

        elif choice == '8':
            try:
                student_id = int(input("Enter student ID: "))
                course_id = int(input("Enter course ID: "))
                manager.check_in(student_id, course_id)
            except ValueError:
                print("Invalid ID. Please enter a number.")
        elif choice == '9':
            try:
                student_id = int(input("Enter student ID: "))
                course_id = int(input("Enter course ID: "))
                manager.enrol_student_in_course(student_id, course_id)
            except ValueError:
                print("Invalid ID. Please enter a number.")
        elif choice.lower() == 'q':
            break
        else:
            print("Invalid choice")
        
if __name__ == "__main__":
    main()