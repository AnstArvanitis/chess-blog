# The Grandmaster's Log ♟️

A robust, multi-user blog application built with **Python** and **Flask**, deployed on **Render**.
This project serves as the Capstone for the "100 Days of Code" Bootcamp, demonstrating Full-Stack development skills, relational database management, and secure authentication flows.

🔗 **Live Demo:** (https://chess-blog.onrender.com/)

![Project Screenshot](https://via.placeholder.com/800x400?text=App+Screenshot+Coming+Soon)

## 🛠️ Tech Stack

* **Backend:** Python 3.11, Flask 2.3
* **Database:** PostgreSQL (Production), SQLite (Development), SQLAlchemy ORM
* **Frontend:** Jinja2 Templating, Bootstrap 5, CKEditor (Rich Text)
* **Authentication:** Flask-Login, Werkzeug Security (Hashing & Salting)
* **DevOps:** Git, GitHub, Render (PaaS), Gunicorn

## 🚀 Key Features

* **Role-Based Access Control (RBAC):**
    * **Admin:** Full CRUD capabilities (Create, Read, Update, Delete posts).
    * **Users:** Can read posts and leave comments.
    * **Guests:** Read-only access.
* **Secure Authentication:** User registration and login system with password hashing.
* **Relational Data Structure:** Implemented **One-to-Many** relationships linking Users to Posts and Comments.
* **Dynamic Content:** Rich text editing for posts and comments using CKEditor.
* **Profile Avatars:** Automated avatar generation based on user email (Gravatar).
* **Production Grade:** Configured with `gunicorn` for WSGI serving and Environment Variables for security.

## 🔒 Security & Configuration

This project implements industry-standard security practices:
* **Environment Variables:** Sensitive data (API Keys, DB URIs) are hidden using `python-dotenv` locally and Environment Config on Render.
* **Database Switching:** Automatically switches between SQLite (Local) and PostgreSQL (Live) based on the environment.
* **Safe SMTP Handling:** The contact form includes a fail-safe mechanism. It attempts to send emails via SMTP but gracefully falls back to logging if the connection is blocked by provider security policies, preventing server crashes (Error 500).

## ⚙️ Local Installation

If you want to run this locally:

1.  **Clone the repository**
    ```bash
    git clone https://github.com/AnstArvanitis/chess-blog.git
    cd chess-blog
    ```

2.  **Install Dependencies**
    ```bash
    pip install -r requirements.txt
    ```

3.  **Setup Environment Variables**
    Create a `.env` file in the root directory and add:
    ```text
    FLASK_KEY=your_secret_key
    DB_URI=sqlite:///posts.db
    MY_EMAIL=your_email@gmail.com
    MY_EMAIL_PASSWORD=your_app_password
    ```

4.  **Run the App**
    ```bash
    python main.py
    ```

## 👨‍💻 Author

**Anastasis** *Junior Python Developer & AUEB Graduate (Information Systems)* Building tools that bridge business logic with technical execution.

---
*Developed as part of the 100 Days of Code Challenge.*