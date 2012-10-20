Get Started
===========
1. Clone the project
2. Create a virtual environment (`virtualenv venv`)
   * on debian you can `apt-get install python-virtualenv`
   * or get it on github [here](http://github.com/pypa/virtualenv)
3. Source into the venv (`source venv/bin/activate`)
4. Install the requirements (`pip install Django dj-database-url`)
5. Create the dev database (`python manage.py syncdb`)
   * create an admin account for yourself when it asks
6. Run the development server (`python manage.py runserver`)
