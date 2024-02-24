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

Step 1: Install django-crontab
First, you need to install django-crontab using pip:

bash
Copy code
pip install django-crontab
Step 2: Configure django-crontab in Your Django Project's Settings
Add django_crontab to your INSTALLED_APPS in your Django project's settings file (settings.py):

python
Copy code
INSTALLED_APPS = [
# Other installed apps
'django_crontab',
]
Step 3: Define Your Periodic Task
In your Django app, define a function that represents the task you want to run every two weeks. For example:

python
Copy code

# myapp/utils.py

def my_periodic_task(): # Your task logic here
pass
Step 4: Configure django-crontab to Run Your Task
In your Django project's settings file (settings.py), configure django-crontab to run your task every two weeks. Add the following lines at the end of the file:

python
Copy code
CRONJOBS = [
('0 0 */2 * *', 'myapp.utils.my_periodic_task'), # Run every two weeks
]
Step 5: Apply the Crontab Configuration
Run the following command in your terminal to apply the crontab configuration:

bash
Copy code
python manage.py crontab add
This will schedule your periodic task to run every two weeks.

Note:
Remember that django-crontab relies on cron to execute the scheduled tasks. While django-crontab simplifies the process of scheduling tasks within a Django project, it ultimately relies on the underlying system's cron scheduler to execute those tasks. Therefore, cron must still be installed and properly configured on your system for django-crontab to work.

Using django-crontab provides a Django-native solution for scheduling periodic tasks, eliminating the need for manual cron configuration and making it easier to manage scheduled tasks within your Django project.
