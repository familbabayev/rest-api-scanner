# Web-based REST API Security Scanner

Open-source REST API Security Scanner with Web Interface

## Tech Stack
- Python 3.10.10
- Django 4.1.7
- PostgreSQL 14.1


## Installation

1. Clone this repo
2. Create a virtual environment and activate it
3. Install the requirements in the virtual environment 

    ```pip install -r requirements.txt```
4. Run the server
    
    ```python manage.py runserver```


## Environment Variables

To run this project, you will need to add the following environment variables to your .env file in the config folder

`DEBUG` - True or False

`SECRET_KEY` - Strong Random Key of Characters

`DATABASE_NAME` - Database Name

`DATABASE_USER` - Database User

`DATABASE_PASSWORD` - Database Password

`DATABASE_HOST` - Database Host

`DATABASE_PORT` - Database Port
