import unittest
from app.schedule import ScheduleManager as manager
students = []
class TestMSMS(unittest.TestCase):
    def setUp(self):
        self.m = manager()
    def test_find_student_twice(self):
        students = self.m.find_student_by_id(1)
        return students

if __name__ == "__main__":
    unittest.main()