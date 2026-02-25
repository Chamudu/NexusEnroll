# NexusEnroll
# NexusEnroll - Microservices Course Enrollment System

## Overview

NexusEnroll is a microservices-based course enrollment platform built to demonstrate modern software architecture principles. It replaces a legacy monolithic system with scalable, maintainable microservices, showcasing design patterns and best practices in distributed systems development.

## Architecture

- **Microservices Pattern:** Each major module (Student, Faculty, Administrator, Course, Enrollment, Notification, Auth, Reporting) runs as an independent service.
- **Communication:** Services interact via HTTP REST APIs over localhost.
- **Common Utilities:** Shared code for logging and database access.

## Directory Structure

```
NexusEnroll/
│── docs/
│   ├── architecture.pdf
│   └── diagrams/
│
│── services/
│   ├── student_service/
│   ├── course_service/
│   ├── enrollment_service/
│   ├── faculty_service/
│   ├── admin_service/
│   ├── notification_service/
│   ├── auth_service/
│   └── reporting_service/
│
│── common/
│   ├── database.py
│   └── logger.py
│
│── main.py
│── requirements.txt
│── README.md
```

## Getting Started

### Prerequisites

- Python 3.8+
- pip (Python package manager)

### Installation

1. Clone the repository:
    ```bash
    git clone https://github.com/your-org/NexusEnroll.git
    cd NexusEnroll
    ```

2. Install dependencies:
    ```bash
    pip install -r requirements.txt
    ```

### Running Services

Each microservice can be started independently. Example for Student Service:
```bash
python services/student_service/main.py
```
Repeat for other services (change the path each time).

### Testing APIs

Use [curl](https://curl.se/) or [Postman](https://www.postman.com/) to interact with each service.  
Example:
```bash
curl -X POST -H "Content-Type: application/json" -d '{"student_id":1, "course_id":"CS101"}' http://localhost:5000/enroll
```

## Contributing

- Use feature branches for development
- Write clear commit messages and document code
- Track tasks and issues using GitHub Issues

## License

---

> "You don't understand anything until you learn it more than one way" - Marvin Minsky

