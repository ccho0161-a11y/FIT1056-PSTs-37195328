# pst2_main.py - The Persistent Application

import json
import datetime

DATA_FILE = "msms.json"
app_data = {} # This global dictionary will hold ALL our data.

# --- Core Persistence Engine ---
def load_data(path=DATA_FILE):
    """Loads all application data from a JSON file."""
    global app_data
    try:
        with open(path, 'r') as f:
            app_data = json.load(f)
            print("Data loaded successfully.")
    except FileNotFoundError:
        print("Data file not found. Initializing with default structure.")
        app_data = {
            "students": [],
            "teachers": [],
            "attendance": [],
            "next_student_id": 1,
            "next_teacher_id": 1
        }

def save_data(path=DATA_FILE):
    """Saves all application data to a JSON file."""
    with open(path, 'w') as f:
        json.dump(app_data, f, indent=4)
    print("Data saved successfully.")


# --- Full CRUD for Core Data ---
# Note: We are now working with lists of dictionaries, not lists of objects.

def add_teacher(name, speciality):
    """Adds a teacher dictionary to the data store."""
    teacher_id = app_data['next_teacher_id']
    new_teacher = {"id": teacher_id, "name": name, "speciality": speciality}
    app_data['teachers'].append(new_teacher)
    app_data['next_teacher_id'] += 1
    print(f"Core: Teacher '{name}' added.")

def update_teacher(teacher_id, **fields):
    """Finds a teacher by ID and updates their data with provided fields."""
    for teacher in app_data['teachers']:
        if teacher['id'] == teacher_id:
            teacher.update(fields)
            print(f"Teacher {teacher_id} updated.")
            return
    print(f"Error: Teacher with ID {teacher_id} not found.")

def remove_student(student_id):
    """Removes a student from the data store."""
    matches = [s for s in app_data['students'] if s['id'] == student_id] #searches the database
    
    if matches:
        app_data['students'].remove(matches[0])
        print(f"Student {student_id} removed.")
    else:
        print(f"Error: Student with ID {student_id} not found.")

def remove_teacher(teacher_id):
    """Removes a teacher from the data store."""
    matches = [s for s in app_data['teachers'] if s['id'] == teacher_id]
    
    if matches:
        app_data['teachers'].remove(matches[0])
        print(f"Teacher {teacher_id} removed.")
    else:
        print(f"Error: Teacher with ID {teacher_id} not found.")

def update_student(student_id, **fields):
    """Finds a student by ID and updates their data with provided fields."""
    for student in app_data['students']:
        if student['id'] == student_id:
            student.update(fields)
            print(f"Student {student_id} updated.")
            return
    print(f"Error: Student with ID {student_id} not found.")

def add_student(name, enrolled_in):
    """Adds a student dictionary to the data store."""
    student_id = app_data['next_student_id']
    new_student = {"id": student_id, "name": name, "enrolled_in": enrolled_in}
    app_data['students'].append(new_student)
    app_data['next_student_id'] += 1
    print(f"Core: Student '{name}' added.")


# --- New Receptionist Features ---
def check_in(student_id, course_id, timestamp=None):
    """Records a student's attendance for a course."""
    student_exists = any(s['id'] == student_id for s in app_data['students'])
    
    if not student_exists:
        print(f"Error: Student with ID {student_id} not found.")
        return
    
    if timestamp is None:
        timestamp = datetime.datetime.now().isoformat()
    
    check_in_record = {
        "student_id": student_id,
        "course_id": course_id,
        "timestamp": timestamp
    }
    app_data['attendance'].append(check_in_record)
    print(f"Receptionist: Student {student_id} checked into {course_id}.")

def print_student_card(student_id):
    """Creates a text file badge for a student."""
    student_to_print = None
    for s in app_data['students']:
        if s['id'] == student_id:
            student_to_print = s
            break
    
    if student_to_print:
        filename = f"{student_id}_card.txt"
        with open(filename, 'w') as f:
            f.write("========================\n")
            f.write(f"  MUSIC SCHOOL ID BADGE\n")
            f.write("========================\n")
            f.write(f"ID: {student_to_print['id']}\n")
            f.write(f"Name: {student_to_print['name']}\n")
            f.write(f"Enrolled In: {', '.join(student_to_print.get('enrolled_in', []))}\n")
        print(f"Printed student card to {filename}.")
    else:
        print(f"Error: Could not print card, student {student_id} not found.")

# --- Main Application Loop ---
def main():
    """Main function to run the MSMS application."""
    load_data() # Load all data from file at startup.

    while True:
        print("\n===== MSMS v2 (Persistent) =====")
        print("1. Check-in Student")
        print("2. Print Student Card")
        print("3. Update Teacher Info")
        print("4. Remove Student")
        print("5. Register New Student")
        print("6. Add A Teacher")
        print("7. Update Student Info")
        print("q. Quit and Save")
        
        choice = input("Enter your choice: ")
        
        made_change = False # A flag to track if we need to save
        if choice == '1':
            try:
                student_id = int(input("Enter student ID: "))
                course_id = input("Enter course or instrument: ")
                check_in(student_id, course_id)
                made_change = True
            except ValueError:
                print("Invalid ID, please enter a number")
        elif choice == '2':
            try:
                student_id = int(input("Enter student ID: "))
                print_student_card(student_id)
            except ValueError:
                print("Invalid ID, please enter a number")
        elif choice == '3':
            try:
                teacher_id = int(input("Enter teacher ID: "))
                new_speciality = input("Enter new speciality (leave blank and press enter to skip): ")
                new_name = input("Enter new name (leave blank and press enter to skip): ")
                fields = {}
                if new_name:
                    fields["name"] = new_name
                if new_speciality:
                    fields["speciality"] = new_speciality
                if fields:
                    update_teacher(teacher_id, **fields)
                    made_change = True
                else:
                    print("No changes made.")
                    made_change = False
            except ValueError:
                print("Invalid ID, please enter a number")

        elif choice == '4':
            try:
                student_id = int(input("Enter student ID: "))
                remove_student(student_id)
                made_change = True
            except ValueError:
                print("Invalid ID, please enter a number")

        elif choice == '5':
            #get studnet id and add student
            name = input("Enter student name: ")
            instrument = input("Enter instrument to enrol in: ")
            add_student(name, [instrument])
            made_change = True

        elif choice == '6':
            #get teacheer and add teacher
            name = input("Enter teacher name: ")
            speciality = input("Enter speciality: ")
            add_teacher(name, speciality)
            made_change = True

        elif choice == '7':
            try:
                student_id = int(input("Enter student ID: "))
                new_name = input("Enter new name (leave blank and press enter to skip): ")
                new_instrument = input("Enter new instrument to add (leave blank to skip): ")
                fields = {}
                if new_name:
                    fields["name"] = new_name
                if new_instrument:
                    fields["enrolled_in"] = [new_instrument]
                if fields:
                    update_student(student_id, **fields)
                    made_change = True
                else:
                    print("No changes made.")
            except ValueError:
                print("Invalid ID, please enter a number")

        elif choice.lower() == 'q':
            print("Saving final changes and exiting.")
            break
        else:
            print("Invalid choice.")
            
        if made_change:
            save_data() # Save the data immediately after any change.

    save_data() # One final save on exit.

# --- Program Start ---
if __name__ == "__main__":
    main()