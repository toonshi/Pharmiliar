# Pharmiliar

Django project that uses Googles APIs to auto populate fields, display maps and routes for multiple waypoints

1. cd to development directory
2. mkvirtualenv Pharmiliar
3. mkdir Pharmiliar
4. clone repository to new directory
5. pip install -r requirements.txt
6. Create and update settings.ini with your email API information

GOOGLE_API_KEY = ""

RECAPTCHA_PUBLIC_KEY = ""

RECAPTCHA_PRIVATE_KEY = ""

7. python manage.py makemigrations
8. python manage.py migrate
9. python manage.py runserver
10. https://localhost:8000 - Bob's your uncle!!

Note:

Don't forget to activate the following Google API's

reCAPTURE
Places API
Maps Javascript API
Directions API
Distance Matrix API
Geocoding API
