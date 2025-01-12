# KU-CMS (Kathmandu University Classroom Management System)


This is the backend server for KU-CMS


## Prerequisites


- Python 3.8+
- Git
- MYSQL/MariaDB


## Getting Started


### Clone the Repository


```bash
git clone https://github.com/notashwinii/kucms.git
cd kucms
```


### Set Up Virtual Environment


#### For Windows
```bash
python -m venv venv
venv\Scripts\activate
```


#### For macOS/Linux
```bash
python3 -m venv venv
source venv/bin/activate
```


### Create Environment File


Create a new file named `.env` in the root directory and add the following configurations:


```plaintext
DEBUG=True
SECRET_KEY=your-secret-key-here
ALLOWED_HOSTS=*


# Database Configuration
DB_NAME=kucms
DB_USER=your_db_user
DB_PASSWORD=your_db_password
DB_HOST=localhost
DB_PORT=5432
```

### Install Dependencies


```bash
pip install -r requirements.txt
```


### Database Setup


Run migrations to create database tables:


```bash
python manage.py makemigrations
python manage.py migrate
```


### Create Superuser (Admin)


```bash
python manage.py createsuperuser
```
Access the admin panel at:
`http://127.0.0.1:8000/admin/`

### Run Development Server


```bash
python manage.py runserver
```


The application will be available at `http://127.0.0.1:8000/`


## API Documentation


### Swagger Documentation


Access the API documentation at:
- Swagger UI: `http://127.0.0.1:8000/swagger/`






