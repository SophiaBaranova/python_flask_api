# 🗓️ Python Web App for Event Scheduling

This is a simple Python web application built with Flask web framework that allows user to view upcoming events and their schedules. 
It uses a SQLite database for data persistence, provides REST API endpoints with Swagger documentation, and includes unit tests with Pytest.

---

## 👀 Demo

The home page contains the list of all upcoming events.

![home page](https://github.com/user-attachments/assets/485c9ca8-9b8d-49d8-8c86-d64de02c59d9)

By clicking on the particular row in the table user navigates to the schedule page, where the details of the event can be seen.

![schedule page](https://github.com/user-attachments/assets/dc729398-54d0-4fbc-85fa-e87a28da9046)

Swagger UI provides a clear API documentation and serves for interaction with endpoints.

![swagger for events](https://github.com/user-attachments/assets/26e01a6f-aaaa-4593-b99c-b519bdac2a92)

![post for events](https://github.com/user-attachments/assets/ea27e18b-8069-4c20-8dd1-d559c9ac609d)

![swagger for subevents](https://github.com/user-attachments/assets/ade61b78-0f7d-418e-a3d3-dee7ecf3dc1f)

---

## 🚀 Getting Started

### 1. Clone the repository

```bash
git clone https://github.com/SophiaBaranova/python_flask_api.git
cd python_flask_api
```

### 2. Install dependencies

```bash
pip install -r requirements.txt
```

> [!TIP]
> To avoid conflicts with Python and packages versions it's better to create and activate a virtual environment
> before installing dependencies.
> 
> ```bash
> python -m venv venv
> venv\Scripts\activate
> ```

### 3. Run the app

```bash
python -m rp_flask_api.app
```

The app will be available at `http://127.0.0.1:8000`

### 4. Explore documentation

Visit `http://localhost:8000/api/ui/` to access an interactive interface for all available REST API endpoints.

### 5. Run the tests

```bash
pytest
```

## 🙏 Acknowledgments

This project is based on the excellent three-part tutorial series by [Real Python](https://realpython.com/flask-connexion-rest-api/)

Parts of the structure and implementation are adapted from it. Full credit to the authors.

I do not claim original authorship over the parts derived from the tutorial and have used them for educational purposes.
