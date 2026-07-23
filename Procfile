web: python manage.py migrate && python manage.py collectstatic --noinput && python manage.py runbot & gunicorn config.wsgi:application --bind 0.0.0.0:$PORT
