Get Started
===========
1. Clone the project
2. `git checkout moreforums`
3. Create a virtual environment (`virtualenv venv`)
   * on debian you can `apt-get install python-virtualenv`
   * or get it on github [here](http://github.com/pypa/virtualenv)
4. Source into the venv (`source venv/bin/activate`)
5. Install the requirements (`pip install -r requirements.txt`)
6. Create the dev database (`python manage.py syncdb`)
   * create an admin account for yourself when it asks
7. Load some test data (`python manage.py loaddata test`)
8. Run the development server (`python manage.py runserver`)
