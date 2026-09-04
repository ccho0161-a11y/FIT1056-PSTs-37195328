# main.py - The View Layer
from app.schedule import ScheduleManager

def front_desk_daily_roster(manager, day):
    """Displays a pretty table of all lessons on a given day."""
    valid_days = ["monday", "tuesday", "wednesday", "thursday", "friday", "saturday", "sunday"]
    if day.lower() not in valid_days:
        print(f"Error: '{day}' is not a valid day. Valid days are: Monday, Tuesday, Wednesday, Thursday and Friday.")
        return
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
    manager = ScheduleManager() 
    print(f"DEBUG: Loaded {len(manager.courses)} courses, {len(manager.students)} students.")
    
    while True:
        print("\n===== MSMS v3 (Object-Oriented) =====")
        print("1. Daily lessons")
        print("2. Switch a class")
        print("3. Add a student")
        print("4. View all existing students")
        print("5. View all existing teachers")
        print("6. Update student information")
        print("7. Update teacher information")
        print("8. Check in a student")
        print("9. Add a student to a class")
        print("10. Search for student or teacher")
        print("11. Add a teacher")
        print("12. Remove a student")
        print("13. Remove a teacher")
        print("14. Print student card")
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
        elif choice == '10':
            search_type = input("Search by (name/id/course): ").strip().lower()
            if search_type not in ('name', 'id', 'course'):
                print("Invalid search type.")
            else:
                term = input(f"Enter {search_type} to search for: ")
                manager.search_database(search_type, term)
        elif choice == '11':
            manager.add_teacher()
        elif choice == '12':
            manager.remove_student()
        elif choice == '13':
            manager.remove_teacher()
        elif choice == '14':
            manager.print_student_card()
        elif choice.lower() == 'q':
            break
        else:
            print("Invalid choice")
        
if __name__ == "__main__":
    main()