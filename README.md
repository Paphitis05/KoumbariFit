# KoumbariFit

A fitness-oriented web application built with Python (Django), HTML/HTMX, and SQLite for local database storage.

## Features:
- User registration and authentication
- Image upload with description as post
- Post deletion
- Partial refresh with HTMX for dynamic content updates
- SQLite as the local database
- Query search for users registered in database
## Repository:
[https://github.com/Paphitis05/KoumbariFit](https://github.com/Paphitis05/KoumbariFit)

## Installation & Setup:

Before running the project, make sure to install the required libraries:

```bash
pip install django
pip install pillow    # For handling image uploads
pip install django-htmx    # For partial refresh with HTMX
```
Running the surver : 
```bash
python manage.py runserver
The server will be running locally at:
http://127.0.0.1:8000/
```
If needed run these commands to make sure all the migrations have been completed succesfuly:
```bash
python manage.py makemigrations
python manage.py migrate
