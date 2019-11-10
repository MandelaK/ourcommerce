web: cd server/ && gunicorn ecommerce.wsgi

release: python server/manage.py makemigrations
release: python server/manage.py migrate