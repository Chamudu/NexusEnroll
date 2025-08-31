class Student:
    def __init__(self, student_id, name):
        self.student_id = student_id
        self.name = name
        self.courses = []

    def enroll(self, course_id):
        if course_id not in self.courses:
            self.courses.append(course_id)
            return True
        return False