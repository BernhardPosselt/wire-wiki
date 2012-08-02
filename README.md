wire
====
Project base

Dependencies
============
* python2-markdown
* python-django

Before Deploying
================
settings.py:
* Change DEBUG to False
* Change PRODUCTION to True
* Insert your Database values
* Change the value of SECRET_KEY to a random, 50 characters long sequence
* HTTPS only: set SESSION_COOKIE_SECURE and CSRF_COOKIE_SECURE to True
* Adjust the django_apache.conf and double check to only allow serving of the static directory


Deploying
=========
Change into the same directory as the manage.py then run 
  
    python manage.py syncdb
    python manage.py collectstatic
    sudo /etc/init.d/apache2 restart
