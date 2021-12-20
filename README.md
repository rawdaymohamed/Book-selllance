## Book Selllance

## Introduction

Book Selllance is an ecommerce web application that allows the user to buy and sell books online.

## Attribution

All vectors in this website are from Freepik
[https://www.freepik.com/](Freepik)

## Dependencies

### 1. Backend Dependencies

The backend of the project includes:

- **virtualenv** as a tool to create isolated an Python environment
- **Postgres** as our database of choice
- **Python 3** and **Django** as our server language and server framework

You can download and install the dependencies mentioned above using these `pipenv`:

```
pip3 install pipenv
pipenv shell
pipenv install django
pipenv install psycopg2
```

### 2. Frontend Dependencies

We use HTML, CSS, jQuery, and Bootstrap for our front end

## Main Files: Project Structure

```sh
├── README.md
├── Book_selllance
│   ├── asgi.py
│   ├── settings.py
│   ├── urls.py
│   └──  wsgi.py
|
└── main
    ├── admin.py
    ├── apps.py
    ├── forms.py
    ├── middlewares.py
    ├── models.py
    ├── signals.py
    ├── urls.py
    ├── views.py
    └──  widgets.py
```

## Development Setup

```
git clone https://github.com/rawda-developer/Book-selllance
cd Book-sellance
```

**Run the development server:**

```
    cd Book_selllance
    ./manage.py makemigrations
    ./manage.py migrate
    ./manage.py createsuperuser
    ./manage.py test
    ./manage.py runserver
```

**Verify on the Browser**<br>
Navigate to project homepage [http://127.0.0.1:8000/](http://127.0.0.1:8000/) or [http://localhost:8000](http://localhost:8000)
