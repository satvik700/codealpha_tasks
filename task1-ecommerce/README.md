# Task 1 – Simple E-commerce Store (Django)
Features: product listing + search, product details, session shopping cart, user registration/login, checkout and order history, admin panel. Database: SQLite (products, users, orders).

## Run
```
cd task1-ecommerce
pip install -r requirements.txt
python manage.py makemigrations store
python manage.py migrate
python manage.py seed
python manage.py createsuperuser   # optional, for /admin
python manage.py runserver
```
Open http://127.0.0.1:8000
