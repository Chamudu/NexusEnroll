"""
Integration test runner for NexusEnroll microservices.
You can use this to simulate end-to-end scenarios or orchestrate startup.
"""

print("Welcome to NexusEnroll Microservices Test Runner!")
print("Please run each service independently using their main.py script in the respective service directory.")

# pip install -r requirements.txt
# Start the student service with python services/student_service/main.py.
# Test with curl or Postman:
    # curl -X POST -H "Content-Type: application/json" -d '{"student_id":1, "course_id":"CS101"}' http://localhost:5000/enroll