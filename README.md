# The Grandmaster's Log ♟️

A multi-user blog application built with Python and Flask.
This project was developed as the **Capstone Project** for the "100 Days of Code" Python Bootcamp (Day 69). It features a full authentication system, role-based access control (Admin vs. Users), and a relational database structure.

![Project Screenshot](https://via.placeholder.com/800x400?text=App+Screenshot+Placeholder) 
*(Note: Replace this line with a real screenshot of your app)*

## 🚀 Features

* **User Authentication:** Secure Login/Register system using `Werkzeug` for password hashing and `Flask-Login` for session management.
* **Role-Based Access:**
    * **Admin (ID=1):** Can Create, Edit, and Delete posts.
    * **Registered Users:** Can read posts and leave comments.
    * **Guests:** Can only read posts.
* **Database Relationships (SQLAlchemy 2.0):**
    * Implemented **One-to-Many** relationships connecting Users, Blog Posts, and Comments.
* **Rich Text Editor:** Integrated `Flask-CKEditor` for writing styled blog posts and comments.
* **Profile Avatars:** Users automatically get profile pictures via `Flask-Gravatar`.
* **Styling:** Responsive design using Bootstrap 5 (`Flask-Bootstrap`).

## 🛠️ Tech Stack & Requirements

* **Python 3.x**
* **Flask 2.3.2** (Core Framework)
* **SQLAlchemy 2.0.25** (ORM & Database Management)
* **SQLite** (Database)
* **WTForms** (Form Validation)

## ⚙️ Installation & Setup

1.  **Clone the repository**
    ```bash
    git clone [https://github.com/YOUR_USERNAME/chess-blog.git](https://github.com/YOUR_USERNAME/chess-blog.git)
    cd chess-blog
    ```

2.  **Create a Virtual Environment** (Optional but recommended)
    ```bash
    python -m venv venv
    source venv/bin/activate  # On Windows use: venv\Scripts\activate
    ```

3.  **Install Dependencies**
    ```bash
    pip install -r requirements.txt
    ```

4.  **Run the Application**
    ```bash
    python main.py
    ```
    The app will run at `http://127.0.0.1:5002/`.

## 💡 Key Learnings

Building this project helped me understand:
* How to structure a **Relational Database** properly (handling Foreign Keys and `back_populates`).
* The importance of **Route Protection** using custom decorators (`@admin_only`).
* How to bridge the Frontend (Jinja2 templates) with Backend logic effectively.
* Handling "Breaking Changes" in database schemas during development.

## 📝 License

This project is for educational purposes. Design template by [Start Bootstrap](https://startbootstrap.com/).