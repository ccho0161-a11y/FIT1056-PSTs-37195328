import json
import datetime
from app.student import StudentUser
from app.teacher import TeacherUser, Course
import os

class ScheduleManager:
    """The main controller for all business logic and data handling."""
    def __init__(self, data_path=None):
        if data_path is None:
            base_dir = os.path.dirname(os.path.abspath(__file__))
            data_path = os.path.join(base_dir, "..", "data", "msms.json")
        self.data_path = data_path
        self.students = []
        self.teachers = []
        self.courses = []
        self.attendance_log = []
        self._load_data()

    def _load_data(self):
        """Loads data from the JSON file and populates the object lists."""
        try:
            with open(self.data_path, 'r') as f:
                data = json.load(f)
                self.students = []
                for s in data.get("students", []):
                    student = StudentUser(s['id'], s['name'])
                    student.enrolled_course_ids = s.get('enrolled_course_ids', [])
                    self.students.append(student)

                self.courses = []
                for c in data.get("courses", []):
                    course = Course(c['id'], c['name'], c['instrument'], c['teacher_id'])
                    course.enrolled_student_ids = c.get('enrolled_student_ids', [])
                    course.lessons = c.get('lessons', [])
                    self.courses.append(course)
                self.teachers = [
                    TeacherUser(t['id'], t['name'], t['speciality']) for t in data.get("teachers", [])
                ]
                self.attendance_log = data.get("attendance", [])
        except FileNotFoundError:
            print("Data file not found. Starting with a clean state.")
    
    def _save_data(self):
        """Converts object lists back to dictionaries and saves to JSON."""
        data_to_save = {
            "students": [s.__dict__ for s in self.students],
            "teachers": [t.__dict__ for t in self.teachers],
            "courses": [c.__dict__ for c in self.courses],
            "attendance": self.attendance_log,
        }
        with open(self.data_path, 'w') as f:
            json.dump(data_to_save, f, indent=4)
    
    def check_in(self, student_id, course_id):
        """Records a student's attendance for a course after validation."""
        if not isinstance(student_id, int) or not isinstance(course_id, int):
            print("Error: Check-in failed. Student and Course IDs must be numbers.")
            return False
        
        student = self.find_student_by_id(student_id)
        course = self.find_course_by_id(course_id)
        
        if not student or not course:
            print("Error: Check-in failed. Invalid Student or Course ID.")
            return False
            
        timestamp = datetime.datetime.now().isoformat()
        check_in_record = {"student_id": student_id, "course_id": course_id, "timestamp": timestamp}
        
        self.attendance_log.append(check_in_record)
        self._save_data()
        print(f"Success: Student {student.name} checked into {course.name}.")
        return True

    def find_student_by_id(self, student_id):
        """Finds a student by their ID"""
        for student in self.students:
            if student.id == student_id:
                return student
        return None

    def find_course_by_id(self, course_id):
        """Finds a course by its ID"""
        for course in self.courses:
            if course.id == course_id:
                return course
        return None
    
    def find_teacher_by_id(self, teacher_id):
        """Finds a teacher by their ID."""
        for teacher in self.teachers:
            if teacher.id == teacher_id:
                return teacher
        return None

    def getting_daily_lessons(self, day):
        """Returns a list of course and lesson pairs if they are scheduled for the day"""
        daily_lessons = []
        for course in self.courses:
            for lesson in course.lessons:
                if lesson['day'].lower() == day.lower():
                    daily_lessons.append((course, lesson))
        return daily_lessons

    def switch_student_course(self, student_id, from_course_id, to_course_id):
        """Moves a student from one course to another"""
        student = self.find_student_by_id(student_id)
        from_course = self.find_course_by_id(from_course_id)
        to_course = self.find_course_by_id(to_course_id)
    
        if not student:
            print("Error: Switch failed, reason: invalid student ID.")
            return False
            
        if not from_course or not to_course:
            print("Error: Switch failed, reason: invalid course ID.")
            return False
        
        if from_course_id not in student.enrolled_course_ids:
            print(f"Error: Student{student.name} is not enrolled in {from_course.name}.")
            return False
        
        student.enrolled_course_ids.remove(from_course_id)
        student.enrolled_course_ids.append(to_course_id)
        
        from_course.enrolled_student_ids.remove(student_id)
        to_course.enrolled_student_ids.append(student_id)
        
        self._save_data()
        print(F"{student.name} has been successfully switched from {from_course.name} to {to_course.name}.")
        return True

    def add_student(self):
        """Enrols a student with optional course enrollment"""
        if self.students:
            student_id = self.students[-1].id + 1
        else:
            student_id = 1
        
        student_name = input("Enter student name: ")
        while student_name == "":
            print("Student name cannot be blank")
            student_name = input("Enter student name: ")

        new_student = StudentUser(student_id, student_name)
        self.students.append(new_student)
        
        course_input = input("Enter course ID to enrol in now (press enter to skip): ")
        if course_input != "":
            try:
                course_id = int(course_input)
                course = self.find_course_by_id(course_id)
                if course:
                    new_student.enrolled_course_ids.append(course_id)
                    course.enrolled_student_ids.append(student_id)
                    print(f"Enrolled in {course.name}.")
                else:
                    print(f"No course found with ID {course_id}. Student added with no courses.")
            except ValueError:
                print("Invalid course ID entered. Student added with no courses.")

        self._save_data()
        print(f"The student '{student_name}' has been added with ID {student_id}.")
        return new_student

    def list_students(self):
        """Prints all students and their enrolled courses."""
        if not self.students:
            print("No students found")
            return
        for student in self.students:
            print(f"ID: {student.id}, Name: {student.name}, Enrolled in: {student.enrolled_course_ids}")

    def list_teachers(self):
        """Prints all teachers and their speciality."""
        if not self.teachers:
            print("No teachers found")
            return
        for teacher in self.teachers:
            print(f"ID: {teacher.id}, Name: {teacher.name}, Speciailitie(s) : {teacher.speciality}")

    def update_student(self):
        """Updates an existing student's details"""
        try:
            student_id = int(input("Enter student ID: "))
        except ValueError:
            print("Invalid ID. Please enter a number.")
            return

        student = self.find_student_by_id(student_id)
        if not student:
            print("Error: student with that ID is not found.")
            return
        
        new_name = input("Enter new name (leave blank to skip): ")
        if new_name != "":
            student.name = new_name

        self._save_data()
        print(f"Success: Student {student_id} updated.")

    def update_teacher(self):
        """Updates an existing teacher's details."""
        try:
            teacher_id = int(input("Enter teacher ID: "))
        except ValueError:
            print("Invalid ID. Please enter a number.")
            return

        teacher = self.find_teacher_by_id(teacher_id)
        if not teacher:
            print(f"Error: Teacher with ID {teacher_id} not found.")
            return

        new_name = input("Enter new name (leave blank to skip): ")
        if new_name != "":
            teacher.name = new_name

        new_speciality = input("Enter new speciality (leave blank to skip): ")
        if new_speciality != "":
            teacher.speciality = new_speciality

        self._save_data()
        print(f"Success: Teacher {teacher_id} updated.")

    def enrol_student_in_course(self, student_id, course_id):
        """Enrols an existing student into a course."""
        student = self.find_student_by_id(student_id)
        course = self.find_course_by_id(course_id)

        if not student or not course:
            print("Error: Enrolment failed. Invalid student or course ID.")
            return False

        if course_id in student.enrolled_course_ids:
            print(f"Error: {student.name} is already enrolled in {course.name}.")
            return False

        student.enrolled_course_ids.append(course_id)
        course.enrolled_student_ids.append(student_id)

        self._save_data()
        print(f"Success: {student.name} enrolled in {course.name}.")
        return True

    def search_database(self, search_type, term):
        """Searches database universally (for student or teacher) by name, ID or enrolled course/speciality"""
        results = []

        if search_type == 'name':
            for student in self.students:
                if term.lower() in student.name.lower():
                    course_names = [self.find_course_by_id(cid).name for cid in student.enrolled_course_ids if self.find_course_by_id(cid)]
                    results.append(f"Student - ID: {student.id}, Name: {student.name}, Enrolled in: {course_names}")
            for teacher in self.teachers:
                if term.lower() in teacher.name.lower():
                    results.append(f"Teacher - ID: {teacher.id}, Name: {teacher.name}, Speciality: {teacher.speciality}")
        elif search_type == 'id':
            try:
                search_id = int(term)
            except ValueError:
                print("Invalid ID. Please enter a number.")
                return
            student = self.find_student_by_id(search_id)
            if student:
                course_names = [self.find_course_by_id(cid).name for cid in student.enrolled_course_ids if self.find_course_by_id(cid)]
                results.append(f"Student - ID: {student.id}, Name: {student.name}, Enrolled in: {course_names}")
            teacher = self.find_teacher_by_id(search_id)
            if teacher:
                results.append(f"Teacher - ID: {teacher.id}, Name: {teacher.name}, Speciality: {teacher.speciality}")
        elif search_type == 'course':
            course = None
            for c in self.courses:
                if term.lower() in c.name.lower():
                    course = c
                    break
                if not course:
                    print(f"No course matches {term}")
                    return
                for student_id in course.enrolled_student_ids:
                    student = self.find_student_by_id(student_id)
                    if student:
                        course_names = [self.find_course_by_id(cid).name for cid in student.enrolled_course_ids if self.find_course_by_id(cid)]
                    results.append(f"Student - ID: {student.id}, Name: {student.name}, Enrolled in: {course_names}")
                teacher = self.find_teacher_by_id(course.teacher_id)
                if teacher:
                    results.append(f"Teacher - ID: {teacher.id}, Name: {teacher.name}, Speciality: {teacher.speciality}")

        if not results:
            print("No matches found.")
        else:
            print(f"\n--- Search results ---")
            for r in results:
                print(f"  {r}")

    def add_teacher(self):
        """Adds a new teacher to the system."""
        if self.teachers:
            teacher_id = self.teachers[-1].id + 1
        else:
            teacher_id = 1

        teacher_name = input("Enter teacher name: ")
        while teacher_name == "":
            print("Teacher name cannot be blank")
            teacher_name = input("Enter teacher name: ")

        speciality = input("Enter teacher's speciality: ")
        while speciality == "":
            print("Speciality cannot be blank")
            speciality = input("Enter teacher's speciality: ")

        new_teacher = TeacherUser(teacher_id, teacher_name, speciality)
        self.teachers.append(new_teacher)

        self._save_data()
        print(f"The teacher '{teacher_name}' has been added with ID {teacher_id}.")
        return new_teacher

    def remove_student(self):
        """Removes a student and cleans up their course enrollments."""
        try:
            student_id = int(input("Enter student ID: "))
        except ValueError:
            print("Invalid ID. Please enter a number.")
            return

        student = self.find_student_by_id(student_id)
        if not student:
            print(f"Error: Student with ID {student_id} not found.")
            return

        for course_id in student.enrolled_course_ids:
            course = self.find_course_by_id(course_id)
            if course and student_id in course.enrolled_student_ids:
                course.enrolled_student_ids.remove(student_id)

        self.students.remove(student)
        self._save_data()
        print(f"Success: Student '{student.name}' has been removed.")
    def remove_teacher(self):
        """Removes a teacher, blocked if they still have courses assigned."""
        try:
            teacher_id = int(input("Enter teacher ID: "))
        except ValueError:
            print("Invalid ID. Please enter a number.")
            return

        teacher = self.find_teacher_by_id(teacher_id)
        if not teacher:
            print(f"Error: Teacher with ID {teacher_id} not found.")
            return

        assigned_courses = [course for course in self.courses if course.teacher_id == teacher_id]
        if assigned_courses:
            course_names = [course.name for course in assigned_courses]
            print(f"Error: Cannot remove '{teacher.name}' — they are still assigned course(s): {course_names}. Reassign or remove these courses first.")
            return

        self.teachers.remove(teacher)
        self._save_data()
        print(f"Success: Teacher '{teacher.name}' has been removed.")

    def print_student_card(self):
        """Creates a text file badge for a student."""
        try:
            student_id = int(input("Enter student ID: "))
        except ValueError:
            print("Invalid ID. Please enter a number.")
            return

        student = self.find_student_by_id(student_id)
        if not student:
            print(f"Error: Could not print card, student {student_id} not found.")
            return

        course_names = [self.find_course_by_id(cid).name for cid in student.enrolled_course_ids if self.find_course_by_id(cid)]

        filename = f"{student_id}_card.txt"
        with open(filename, 'w') as f:
            f.write("========================\n")  
            f.write(f"  MUSIC SCHOOL ID BADGE\n")
            f.write("========================\n")
            f.write(f"ID: {student.id}\n")
            f.write(f"Name: {student.name}\n")
            f.write(f"Enrolled In: {', '.join(course_names)}\n")
        print(f"Printed student card to {filename}.")