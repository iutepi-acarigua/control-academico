# Context: University Application (Odoo 19)

## 1. Project Overview
This project is an Odoo 19 module named `university_application`. It serves as an enrollment system for a university, allowing prospective students to submit applications and upload required documents (PDFs), while providing administrators a backend interface to review and manage these applications.

## 2. Architecture (MVT / MVC)
The system relies heavily on Odoo's native server-side rendering and avoids complex JavaScript frameworks.
* **Models (Database/Business Logic):** Defined in Python using the Odoo ORM. They handle data storage for careers and applications, and manage document attachments using `ir.attachment` via `Binary` fields with `attachment=True`.
* **Controllers (Routing/HTTP):** Python HTTP controllers (`odoo.http.Controller`) intercept form submissions (POST requests) from the public web, process binary files (converting PDFs to Base64), and interact with the Models using `.sudo()` where appropriate for public/portal users.
* **Views (Frontend/QWeb):** QWeb templates render standard HTML forms. Forms use `enctype="multipart/form-data"` for file uploads.
* **Views (Backend/XML):** Traditional Odoo XML views (Kanban, Form, Tree) are used strictly for internal users (administrators) to manage the lifecycle of applications.
* **Authentication & Routing:** A unified login (`/web/login`) is used. Portal Users (students) are routed to the QWeb frontend, while Internal Users (administrators) access the standard Odoo backend.

## 3. Directory Structure
The module follows this strict structure:

university_application/
├── __init__.py
├── __manifest__.py
├── controllers/
│   ├── __init__.py
│   └── main.py
├── models/
│   ├── __init__.py
│   ├── university_career.py
│   └── university_application.py
├── security/
│   ├── ir.model.access.csv
│   └── rules.xml
├── static/
│   └── src/
│       ├── img/
│       └── scss/
│           └── styles.scss
└── views/
    ├── backend/
    │   ├── university_career_views.xml
    │   ├── university_application_views.xml
    │   └── menu_views.xml
    └── frontend/
        ├── templates.xml
        └── pages/
            ├── landing_page.xml
            ├── enrollment_form.xml
            └── success_page.xml

## 4. Odoo 19 Coding Guidelines & Naming Conventions

* Always adhere to the official Odoo coding guidelines:

* Language: All code (variables, classes, model names, IDs) MUST be in English.

* Models: Singular, lowercase, dot-separated (e.g., _name = 'university.career').

* Classes (Python): CamelCase (e.g., class UniversityCareer(models.Model):).

* Files/Directories: Lowercase, underscore-separated (e.g., university_career.py).

* XML IDs: Meaningful and snake_case (e.g., id="view_university_application_kanban").

* String Attributes: Use title case for UI strings (e.g., string="Student Name").

## 5. Best Practices for this Project
* Zero/Low JS Policy: Rely on standard HTML5 validations (required, accept="application/pdf") and server-side QWeb rendering. Do not introduce Vue, React, or custom heavy JS scripts unless explicitly requested.

* Security First: Always include <input type="hidden" name="csrf_token" t-att-value="request.csrf_token()"/> in QWeb forms. Apply strict ir.model.access.csv and Record Rules to prevent portal users from seeing other students' data.

* File Handling: In the controller, read the file object from kwargs, encode it to base64, and save both the binary data and the original filename.

## 6. Official Documentation
Always refer to the Odoo 19 documentation for API references and framework features: https://www.odoo.com/documentation/19.0
