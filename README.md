# 🚀 Course Tracker API

A robust backend service built with Django, Python, and MySQL to power the Course Tracker application. This API handles user data, course records, grade analysis, and career suggestions.

## ✨ Features

- 🔐 **User Authentication** - Secure user authentication and session management
- 📊 **Grade Tracking** - Store and analyze student grades with career path recommendations
- 🗂️ **Course Management** - Comprehensive course and subject data management
- 🧾 **RESTful API** - Clean endpoints for seamless frontend integration
- 🛡️ **Secure Architecture** - Scalable and secure backend infrastructure
- 🎯 **Career Suggestions** - AI-powered career recommendations based on academic performance

## 🛠️ Tech Stack

### Backend
![Python](https://img.shields.io/badge/Python-3776AB?style=for-the-badge&logo=python&logoColor=white)
![Django](https://img.shields.io/badge/Django-092E20?style=for-the-badge&logo=django&logoColor=white)
![MySQL](https://img.shields.io/badge/MySQL-4479A1?style=for-the-badge&logo=mysql&logoColor=white)
![Django REST Framework](https://img.shields.io/badge/DRF-ff1709?style=for-the-badge&logo=django&logoColor=white)

### Frontend Integration
![TypeScript](https://img.shields.io/badge/TypeScript-007ACC?style=for-the-badge&logo=typescript&logoColor=white)
![React](https://img.shields.io/badge/React-20232A?style=for-the-badge&logo=react&logoColor=61DAFB)
![Tailwind CSS](https://img.shields.io/badge/Tailwind_CSS-38B2AC?style=for-the-badge&logo=tailwind-css&logoColor=white)


## 📡 API Endpoints

### Authentication
| Endpoint | Method | Description |
|----------|--------|-------------|
| `/api/login/` | POST | User login |
| `/api/register/` | POST | User registration |
| `/api/logout/` | POST | User logout |

### Courses
| Endpoint | Method | Description |
|----------|--------|-------------|
| `/api/courses/` | GET | Retrieve all courses |
| `/api/courses/` | POST | Create a new course |
| `/api/courses/{id}/` | GET | Get course details |
| `/api/courses/{id}/` | PUT | Update course |
| `/api/courses/{id}/` | DELETE | Delete course |

### Grades
| Endpoint | Method | Description |
|----------|--------|-------------|
| `/api/grades/` | GET | Retrieve all grades |
| `/api/grades/` | POST | Submit grade data |
| `/api/grades/{id}/` | PUT | Update grade |
| `/api/grades/{id}/` | DELETE | Delete grade |

### Career Suggestions
| Endpoint | Method | Description |
|----------|--------|-------------|
| `/api/career-suggestions/` | GET | Get career recommendations |
| `/api/career-paths/` | GET | List available career paths |


## 🔒 Security Features

- CSRF protection enabled
- SQL injection prevention through Django ORM
- Password hashing with PBKDF2
- Session management with secure cookies
- Input validation and sanitization
- CORS configuration for frontend integration

## 📊 Database Schema

The API uses the following main models:
- **User** - User authentication and profile data
- **Course** - Course information and details
- **Grade** - Student grades and performance data
- **Subject** - Subject categories and metadata
- **CareerPath** - Career recommendations and requirements

