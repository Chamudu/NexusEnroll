from flask import Flask, request, jsonify
from student import Student

app = Flask(__name__)

students = {
    1: Student(1, "Alice"),
    2: Student(2, "Bob")
}

@app.route('/enroll', methods=['POST'])
def enroll():
    data = request.json
    student_id = data.get('student_id')
    course_id = data.get('course_id')
    student = students.get(student_id)
    if not student:
        return jsonify({"error": "Student not found"}), 404
    success = student.enroll(course_id)
    if success:
        return jsonify({"message": f"{student.name} enrolled in {course_id}"})
    else:
        return jsonify({"message": f"{student.name} already enrolled in {course_id}"}), 400

if __name__ == '__main__':
    app.run(port=5000)