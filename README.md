# NotesApp v2 - Advanced Note-Taking Application

![NotesApp Logo](https://img.shields.io/badge/NotesApp-v2-informational?style=flat&logo=note&logoColor=white&color=blue)

**NotesApp v2** is a modern, user-friendly, and open-source application designed to help users efficiently manage their thoughts, ideas, and tasks. This is a revamped version of the original ["Simple Note Application"](https://github.com/IdkBemja/SimpleNoteApp), now featuring **JWT-based authentication**, **dynamic JavaScript-driven pages**, and a more robust architecture.

---

## ✨ Features

- 🔒 **Login and Register System**: Secure user authentication using JWT.
- 📌 **Note Management**: Add, edit, delete, and tag notes for easy organization.
- 🕒 **Last Note Display**: Quickly access the most recent note.
- 📋 **Categorization**: Organize notes using tags and categories (planned).
- 🛠️ **Admin Panel** *(In Progress)*: Manage users, permissions, and content.
- 🌐 **Responsive Design**: Optimized for desktop and mobile devices.

---

## 🔐 Security

- **JWT (JSON Web Tokens)**:
  - Secure token-based authentication for user sessions.
  - Automatic token refresh and validation to ensure seamless user experience.
- **Data Privacy**:
  - User data is encrypted before being stored in the database.
- **Role-Based Access Control** *(Planned)*:
  - Admin vs User-level permissions for enhanced security.

---

## 🛠️ Tech Stack

This note-taking application leverages the following technologies:

### **Backend**
- ![Python](https://img.shields.io/badge/Python_3.11-blue?logo=python&logoColor=white)
  - Backend logic and APIs built with Flask.
- ![Flask](https://img.shields.io/badge/Flask-Framework-orange?logo=flask&logoColor=white)
  - Lightweight, scalable web framework.

### **Frontend**
- ![JavaScript](https://img.shields.io/badge/JavaScript-ES6+-yellow?logo=javascript&logoColor=white)
  - Dynamic UI and interactivity.
- ![Bootstrap](https://img.shields.io/badge/Bootstrap-Styling-purple?logo=bootstrap&logoColor=white)
  - Responsive design and components.

### **Database**
- ![SQLAlchemy + Postgresql](https://img.shields.io/badge/SQLAlchemyORM-PostgreSQL-blue?logo=database&logoColor=white)
  - ORM for managing database operations.

### **Authentication**
- ![JWT](https://img.shields.io/badge/Authentication-JWT-yellow?logo=jsonwebtokens&logoColor=white)
  - Token-based secure authentication.

### **Upcoming Integration**
- ![Laravel](https://img.shields.io/badge/Laravel-PHP_Framework-red?logo=laravel&logoColor=white)
  - Planned integration for hybrid backend functionality.

---

## 🌍 Live Test

Try the live version of the application here:

[**NotesApp Live Demo**](https://notesapp.idkbemja.me)

---

## ⚙️ Installation

Follow these steps to install and run the application locally:

### Prerequisites
Make sure you have Python installed on your system.

### Steps
```bash
# Step 1: Create a directory for the project
mkdir noteapp

# Step 2: Clone the repository
git clone https://github.com/IdkBemja/NotesApp-v2.git

# Step 3: Navigate to the project directory
cd NotesApp-v2

# Step 4: Install dependencies using pipenv
python -m pipenv install -r requirements.txt

# Step 5: Activate the virtual environment
python -m pipenv shell

# Step 6: Run the application
python main.py
