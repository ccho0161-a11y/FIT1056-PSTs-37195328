import json
from app.student import StudentUser
from app.teacher import TeacherUser, Course

class ScheduleManager:
    """The main controller for all business logic and data handling."""
    def __init__(self, data_path="data/msms.json"):
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