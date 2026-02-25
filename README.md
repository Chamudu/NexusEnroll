# NexusEnroll
# NexusEnroll - Microservices Course Enrollment System

[![Python](https://img.shields.io/badge/Python-3.8+-blue.svg)](https://python.org)
[![Architecture](https://img.shields.io/badge/Architecture-Microservices-orange.svg)](https://microservices.io/)
[![Design Patterns](https://img.shields.io/badge/Design%20Patterns-6%20Implemented-green.svg)](README.md)
[![License](https://img.shields.io/badge/License-Academic-yellow.svg)](LICENSE)

NexusEnroll is a microservices-based course enrollment platform built to demonstrate modern software architecture principles. It replaces a legacy monolithic system with scalable, maintainable microservices, showcasing design patterns and best practices in distributed systems development.

## 🎯 Overview

NexusEnroll is a sophisticated microservices-based university course enrollment platform designed for the **SCS 2303 Software Architecture Assignment (2025)**. It replaces legacy monolithic systems with modern, scalable, and maintainable microservices architecture, demonstrating professional-grade software engineering practices.

### 🏆 Key Achievements

- **✅ Production-Ready Authentication Service** - Complete with web interface and security features
- **✅ 6 Design Patterns Implemented** - Singleton, Factory, Observer, Strategy, Repository, Facade
- **✅ Comprehensive Documentation** - Complete API docs and testing guides
- **✅ Interactive Testing** - Built-in web interface for real-time API testing
- **✅ Security Implementation** - RBAC, session management, account lockout protection

## 🏗️ Architecture Overview

### Microservices Pattern
Each major module runs as an independent, loosely-coupled service:

```
┌─────────────────────────────────────────────────────────────┐
│                    NexusEnroll Architecture                 │
├─────────────────────────────────────────────────────────────┤
│  🌐 Web Interface & API Gateway                            │
├─────────────────────────────────────────────────────────────┤
│  🔐 Authentication Service (Port 5001) ✅ IMPLEMENTED      │
│  👥 Student Service (Port 5000) 🔄 BASIC                   │
│  📚 Course Service (Port 5002) ⏳ PLANNED                  │
│  🎓 Faculty Service (Port 5003) ⏳ PLANNED                 │
│  📋 Enrollment Service (Port 5004) ⏳ PLANNED              │
│  📧 Notification Service (Port 5005) ⏳ PLANNED            │
│  👨‍💼 Admin Service (Port 5006) ⏳ PLANNED                   │
│  📊 Reporting Service (Port 5007) ⏳ PLANNED               │
├─────────────────────────────────────────────────────────────┤
│  🗄️ Common Utilities (Database, Logging)                   │
└─────────────────────────────────────────────────────────────┘
```

### Design Patterns Implemented

Our system demonstrates **6 key design patterns**:

1. **🔄 Singleton Pattern** - Database connections, logging systems
2. **🏭 Factory Pattern** - User and service object creation
3. **👁️ Observer Pattern** - Event-driven notifications
4. **🎯 Strategy Pattern** - Authentication and validation strategies
5. **📚 Repository Pattern** - Data access layer abstraction
6. **🎭 Facade Pattern** - Simplified interfaces for complex operations

### Communication Architecture
- **Protocol**: HTTP REST APIs
- **Format**: JSON data exchange
- **Security**: Token-based authentication
- **Cross-Origin**: CORS support for web interfaces

## 📁 Project Structure

```
NexusEnroll/
├── 📋 README.md                    # Main project documentation
├── 📋 requirements.txt             # Python dependencies
├── 🚀 main.py                      # Project orchestrator
│
├── 📊 Diagrams/                    # Architecture & UML diagrams
│   └── NexusEnroll_Class_Diagram/
│       ├── NexusEnroll_Class_Diagram.puml
│       └── NexusEnroll_Class_Diagram_Fixed.png
│
├── 🔧 common/                      # Shared utilities
│   ├── database.py                # Database connection management
│   └── logger.py                  # Centralized logging system
│
└── 🏗️ services/                    # Microservices
    ├── 🔐 auth_service/           ✅ FULLY IMPLEMENTED
    │   ├── main.py                # Flask REST API (11 endpoints)
    │   ├── auth_service.py        # Business logic
    │   ├── user.py               # User entity & authentication
    │   ├── test_auth.py          # Automated test suite (8 scenarios)
    │   ├── api_examples.py       # API usage examples
    │   ├── web_test.html         # Interactive web testing interface
    │   └── README.md             # Complete service documentation
    │
    └── 👥 student_service/        🔄 BASIC IMPLEMENTATION
        ├── main.py               # Basic Flask server
        └── student.py           # Student entity
```

## 🚀 Quick Start Guide

### Prerequisites
- **Python 3.8+** - Required runtime
- **Flask & Flask-CORS** - Web framework and CORS support
- **Web Browser** - For testing the web interface

### 1. Install Dependencies
```powershell
# Navigate to project root
cd "NexusEnroll"

# Install required packages
pip install flask flask-cors
```

### 2. Start the Authentication Service
```powershell
# Navigate to auth service
cd "services\auth_service"

# Start the service
python main.py
```

The service will start on `http://127.0.0.1:5001`

### 3. Test with Web Interface 🌐
- **Open browser**: Navigate to `http://127.0.0.1:5001/`
- **Login**: Use admin credentials (`admin` / `admin123`)
- **Test all features**: Interactive UI for complete testing

### 4. Verify Installation
```powershell
# Check service status
Invoke-RestMethod -Uri "http://127.0.0.1:5001/auth/status"
```

## 🌐 Web Testing Interface

The authentication service includes a **comprehensive web testing interface** accessible at:
**`http://127.0.0.1:5001/`**

### Features:
- 📊 **Real-time Service Status** - Live health monitoring
- 🔑 **Interactive Authentication** - Login/logout testing  
- 👤 **User Management** - Create and manage users
- 🛡️ **Authorization Testing** - Test role-based permissions
- ✅ **Session Validation** - Token management and validation
- 📋 **JSON Response Viewer** - Formatted API responses

## 🔐 Authentication Service (Fully Implemented)

The **crown jewel** of our implementation - a production-ready authentication microservice:

### Features
- **🔑 Complete Authentication** - Login/logout with secure session management
- **👤 User Management** - Create, list, deactivate users with role-based access
- **🛡️ Authorization System** - Hierarchical permissions (Admin > Faculty > Student)
- **🔒 Security Features** - Account lockout, session expiry, audit logging
- **🌐 Web Interface** - Interactive testing at `http://127.0.0.1:5001/`
- **📡 REST API** - 11 fully documented endpoints
- **🧪 Testing Suite** - 8/8 automated test scenarios passing

### Default Test Accounts
| Username | Password | Role | Access Level |
|----------|----------|------|-------------|
| `admin` | `admin123` | Administrator | Full system access |
| `prof_smith` | `faculty123` | Faculty | Course management |
| `alice_student` | `student123` | Student | Course enrollment |

## 🎯 Implementation Status

### ✅ Completed Components

1. **🔐 Authentication Service** - **PRODUCTION READY**
   - Complete REST API with 11 endpoints
   - Web testing interface
   - Comprehensive security features
   - Full documentation and testing

2. **📊 Class Diagram** - **COMPLETE**
   - 6 design patterns visualized
   - PlantUML with colored relationships
   - Comprehensive component mapping

3. **🔧 Common Utilities** - **IMPLEMENTED**
   - Centralized logging system
   - Database connection management
   - Shared across all services

### 🔄 In Progress

4. **👥 Student Service** - **BASIC IMPLEMENTATION**
   - Basic Flask server structure
   - Ready for integration with auth service

### ⏳ Planned Services

5. **📚 Course Service** - Course catalog management
6. **🎓 Faculty Service** - Grade and course management
7. **📋 Enrollment Service** - Student course enrollment
8. **📧 Notification Service** - Email and alert system
9. **👨‍💼 Admin Service** - System administration
10. **📊 Reporting Service** - Analytics and reporting

## 🛠️ Development & Testing

### Service-by-Service Testing

Each service can be tested independently:

```powershell
# Authentication Service (Port 5001)
cd "services\auth_service"
python main.py
# Test at: http://127.0.0.1:5001/

# Student Service (Port 5000)
cd "services\student_service"
python main.py
# Test at: http://127.0.0.1:5000/
```

## Contributing

- Use feature branches for development
- Write clear commit messages and document code
- Track tasks and issues using GitHub Issues

1. **🌐 Start with Web Interface**
   - Show the interactive testing at `http://127.0.0.1:5001/`
   - Demonstrate all authentication features live

2. **📊 Architecture Overview** 
   - Present the class diagram with design patterns
   - Explain microservices communication

3. **🔐 Security Features**
   - Show account lockout protection
   - Demonstrate role-based access control

4. **📋 Code Quality**
   - Review design patterns implementation
   - Show comprehensive testing suite

### Quick Demo Script
```powershell
# 1. Start the service
python services\auth_service\main.py

# 2. Open browser to http://127.0.0.1:5001/
# 3. Show live authentication testing
# 4. Run automated tests
python services\auth_service\test_auth.py

# 5. Show API examples
python services\auth_service\api_examples.py
```

## 📞 Project Information

- **Course**: SCS 2303 Software Architecture (2025)
- **Assignment**: Assignment 03 - Microservices Architecture
- **Implementation**: Production-ready authentication with design patterns
- **Documentation**: Comprehensive guides and API documentation
- **Testing**: Multiple testing approaches with web interface

## 📚 Additional Resources

- **📖 Auth Service Documentation** - Complete guide in `services/auth_service/README.md`
- **📊 Class Diagram** - Visual design patterns in `Diagrams/NexusEnroll_Class_Diagram/`
- **💻 API Examples** - Interactive examples in `services/auth_service/api_examples.py`
- **🧪 Test Suite** - Automated testing in `services/auth_service/test_auth.py`
- **🌐 Web Interface** - Live testing at `http://127.0.0.1:5001/`

---

<div align="center">

**🎓 Built for Educational Excellence**

*NexusEnroll - Modern Microservices Architecture for University Systems*

[![Authentication](https://img.shields.io/badge/Auth%20Service-Production%20Ready-brightgreen)](services/auth_service/)
[![Design Patterns](https://img.shields.io/badge/Design%20Patterns-6%20Implemented-blue)](README.md)
[![Documentation](https://img.shields.io/badge/Documentation-Complete-success)](README.md)

</div>

