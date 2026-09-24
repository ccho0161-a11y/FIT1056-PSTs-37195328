import json
from app.student import StudentUser
# Corrected Import: TeacherUser and Course now come from the same file.
from app.teacher import TeacherUser, Course

class ScheduleManager:
    """The main controller for all business logic and data handling."""
    def __init__(self, data_path="data/msms.json"):
        self.data_path = data_path
        self.students = []
        self.teachers = []
        self.courses = []
        self.next_lesson_id = 1
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

    """Finding stuff"""
    def find_student_by_id(self, student_id):
        """Finds a student by their ID."""
        for student in self.students:
            if student.id == student_id:
                return student
        return None

    def find_course_by_id(self, course_id):
        """Finds a course by its ID."""
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

    def find_course_by_instrument(self, instrument):
        """
        Finds an available (not full) course matching the given instrument.
        Returns None if no matching course has space.
        NOTE: adjust MAX_CLASS_SIZE / matching logic to your team's actual rules.
        """
        for course in self.courses:
            if course.instrument.lower() == instrument.lower():
                if len(course.enrolled_student_ids) < MAX_CLASS_SIZE:
                    return course
        return None

    def getting_daily_lessons(self, day):
        """Returns a list of (course, lesson) pairs scheduled for the given day."""
        daily_lessons = []
        for course in self.courses:
            for lesson in course.lessons:
                if lesson['day'].lower() == day.lower():
                    daily_lessons.append((course, lesson))
        return daily_lessons
    
    """Student related stuff"""
    def register_new_student(self, name, instrument):
            """Enrols a student via the GUI (Streamlit) with instrument-based matching"""
            if self.students:
                student_id = self.students[-1].id + 1
            else:
                student_id = 1
            new_student = StudentUser(student_id, name)
            self.students.append(new_student)
    
            course = self.find_course_by_instrument(instrument)
            if course:
                new_student.enrolled_course_ids.append(course.id)
                course.enrolled_student_ids.append(student_id)
            else:
                self.students.remove(new_student)
                return None
    
            self._save_data()
            return new_student
    
    def find_course_by_instrument(self, instrument):
        """Finds a course matching the given instrument. Returns None if no matching course exists."""
        for course in self.courses:
            if course.instrument.lower() == instrument.lower():
                return course
        return None

    def update_student(self, student_id, new_name):
        """Updates a student's name. Returns (True, student) on success,
        or (False, error_message) on failure."""
        student = self.find_student_by_id(student_id)
        if not student:
            return False, f"Student with ID {student_id} not found."

        if new_name and new_name.strip():
            student.name = new_name.strip()

        self._save_data()
        return True, student

    def remove_student(self, student_id):
        """Removes a student and cleans up their course enrolments.
        Returns (True, message) or (False, message)."""
        student = self.find_student_by_id(student_id)
        if not student:
            return False, f"Student with ID {student_id} not found."

        for course_id in student.enrolled_course_ids:
            course = self.find_course_by_id(course_id)
            if course and student_id in course.enrolled_student_ids:
                course.enrolled_student_ids.remove(student_id)

        self.students.remove(student)
        self._save_data()
        return True, f"Student '{student.name}' has been removed."

    def enrol_student_in_course(self, student_id, course_id):
        """Enrols an existing student into a course. Returns (True, message) or (False, message)."""
        student = self.find_student_by_id(student_id)
        course = self.find_course_by_id(course_id)

        if not student or not course:
            return False, "Enrolment failed. Invalid student or course ID."

        if course_id in student.enrolled_course_ids:
            return False, f"{student.name} is already enrolled in {course.name}."

        student.enrolled_course_ids.append(course_id)
        course.enrolled_student_ids.append(student_id)

        self._save_data()
        return True, f"{student.name} enrolled in {course.name}."

    def switch_student_course(self, student_id, from_course_id, to_course_id):
        """Moves a student from one course to another. Returns (True, message) or (False, message)."""
        student = self.find_student_by_id(student_id)
        from_course = self.find_course_by_id(from_course_id)
        to_course = self.find_course_by_id(to_course_id)

        if not student:
            return False, "Switch failed: invalid student ID."

        if not from_course or not to_course:
            return False, "Switch failed: invalid course ID."

        if from_course_id not in student.enrolled_course_ids:
            return False, f"{student.name} is not enrolled in {from_course.name}."

        student.enrolled_course_ids.remove(from_course_id)
        student.enrolled_course_ids.append(to_course_id)

        from_course.enrolled_student_ids.remove(student_id)
        to_course.enrolled_student_ids.append(student_id)

        self._save_data()
        return True, f"{student.name} has been switched from {from_course.name} to {to_course.name}."

    def list_students(self):
        """Returns a list of dicts describing each student (for GUI tables)."""
        result = []
        for student in self.students:
            course_names = [
                c.name for cid in student.enrolled_course_ids
                if (c := self.find_course_by_id(cid))
            ]
            result.append({
                "id": student.id,
                "name": student.name,
                "enrolled_in": course_names,
            })
        return result

    def print_student_card(self, student_id):
        """Creates a text file badge for a student.
        Returns (True, filename) on success, or (False, error_message)."""
        student = self.find_student_by_id(student_id)
        if not student:
            return False, f"Could not print card, student {student_id} not found."

        course_names = [
            c.name for cid in student.enrolled_course_ids
            if (c := self.find_course_by_id(cid))
        ]

        filename = f"{student_id}_card.txt"
        with open(filename, 'w') as f:
            f.write("========================\n")
            f.write("  MUSIC SCHOOL ID BADGE\n")
            f.write("========================\n")
            f.write(f"ID: {student.id}\n")
            f.write(f"Name: {student.name}\n")
            f.write(f"Enrolled In: {', '.join(course_names)}\n")

        return True, filename

    """Teacher stuff"""
    def register_new_teacher(self, name, speciality):
        """Adds a new teacher to the system. Returns the new TeacherUser."""
        if self.teachers:
            teacher_id = self.teachers[-1].id + 1
        else:
            teacher_id = 1

        new_teacher = TeacherUser(teacher_id, name, speciality)
        self.teachers.append(new_teacher)

        self._save_data()
        return new_teacher

    def update_teacher(self, teacher_id, new_name=None, new_speciality=None):
        """Updates a teacher's name and/or speciality.
        Returns (True, teacher) on success, or (False, error_message)."""
        teacher = self.find_teacher_by_id(teacher_id)
        if not teacher:
            return False, f"Teacher with ID {teacher_id} not found."

        if new_name and new_name.strip():
            teacher.name = new_name.strip()
        if new_speciality and new_speciality.strip():
            teacher.speciality = new_speciality.strip()

        self._save_data()
        return True, teacher

    def remove_teacher(self, teacher_id):
        """Removes a teacher, blocked if they still have courses assigned.
        Returns (True, message) or (False, message)."""
        teacher = self.find_teacher_by_id(teacher_id)
        if not teacher:
            return False, f"Teacher with ID {teacher_id} not found."

        assigned_courses = [c for c in self.courses if c.teacher_id == teacher_id]
        if assigned_courses:
            course_names = [c.name for c in assigned_courses]
            return False, (
                f"Cannot remove '{teacher.name}' — still assigned to course(s): "
                f"{course_names}. Reassign or remove these courses first."
            )

        self.teachers.remove(teacher)
        self._save_data()
        return True, f"Teacher '{teacher.name}' has been removed."

    def list_teachers(self):
        """Returns a list of dicts describing each teacher (for GUI tables)."""
        return [
            {"id": t.id, "name": t.name, "speciality": t.speciality}
            for t in self.teachers
        ]

    def search_database(self, search_type, term):
        """Searches students/teachers by name, ID, or course.
        Returns a list of result strings (empty list if no matches)."""
        results = []

        if search_type == 'Name':
            for student in self.students:
                if term.lower() in student.name.lower():
                    course_names = [
                        c.name for cid in student.enrolled_course_ids
                        if (c := self.find_course_by_id(cid))
                    ]
                    results.append(
                        f"Student - ID: {student.id}, Name: {student.name}, Enrolled in: {course_names}"
                    )
            for teacher in self.teachers:
                if term.lower() in teacher.name.lower():
                    results.append(
                        f"Teacher - ID: {teacher.id}, Name: {teacher.name}, Speciality: {teacher.speciality}"
                    )

        elif search_type == 'ID':
            try:
                search_id = int(term)
            except ValueError:
                return []

            student = self.find_student_by_id(search_id)
            if student:
                course_names = [
                    c.name for cid in student.enrolled_course_ids
                    if (c := self.find_course_by_id(cid))
                ]
                results.append(
                    f"Student - ID: {student.id}, Name: {student.name}, Enrolled in: {course_names}"
                )

            teacher = self.find_teacher_by_id(search_id)
            if teacher:
                results.append(
                    f"Teacher - ID: {teacher.id}, Name: {teacher.name}, Speciality: {teacher.speciality}"
                )

        elif search_type == 'Course':
            matched_course = None
            for c in self.courses:
                if term.lower() in c.name.lower():
                    matched_course = c
                    break

            if not matched_course:
                return []

            for student_id in matched_course.enrolled_student_ids:
                student = self.find_student_by_id(student_id)
                if student:
                    course_names = [
                        c.name for cid in student.enrolled_course_ids
                        if (c := self.find_course_by_id(cid))
                    ]
                    results.append(
                        f"Student - ID: {student.id}, Name: {student.name}, Enrolled in: {course_names}"
                    )

            teacher = self.find_teacher_by_id(matched_course.teacher_id)
            if teacher:
                results.append(
                    f"Teacher - ID: {teacher.id}, Name: {teacher.name}, Speciality: {teacher.speciality}"
                )

        return results

    def add_course(self, name, instrument, teacher_id):
        """Creates a new course taught by an existing teacher.
        Returns (True, course) on success, or (False, error_message)."""
        teacher = self.find_teacher_by_id(teacher_id)
        if not teacher:
            return False, f"No teacher found with ID {teacher_id}."

        if self.courses:
            course_id = self.courses[-1].id + 1
        else:
            course_id = 1

        new_course = Course(course_id, name, instrument, teacher_id)
        new_course.enrolled_student_ids = []
        new_course.lessons = []
        self.courses.append(new_course)

        self._save_data()
        return True, new_course