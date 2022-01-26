# Hustle

### This web app will help connect workers with people that need yard work done. This could include, lawn mowing, leaf raking, or snowblowing. 

## Work Space Layout

The app will be stored in this repository along with the documentation of the design process and the documentation of the app. The documentation for both can be found in the folder called "docs".

The actal app will be in the folder called "app"

## Version-Control Procedures

Every person on the team has a personal branch that they will use to develope on. When a change is needed to be merged with the main branch, the person that made the change will have to create a pull request. Then the rest of the team will look it over discuss and approve it. 

## Tool Stack Description and Setup

Django will be used to create and manage the web apps database. Django uses python and it's somthing that everyone on the team has some experience in making it a great choice.

## Build Instructions

Clone the project in gitbash. ``` bash $ git clone https://github.com/yodarocks1/3MusketeersAndARifleman ```

The next steps are basic Django setup instructions and are subject to change.

- Create and start a virtual environment ``` bash $ virtualenv --no-site-packages ```

- Install the project dependencies ``` bash $ pip install -r requirements.txt ```

- Create a file named "secret.sh" ``` bash touch secrets.sh ```

- Obtain a secret from MiniWebTool key and add to secret.sh ```bash export SECRET_KEY='<secret_key>'```

- Add secret.sh to .gitignore file Create a postgres db and add the credentials to settings.py
```

DATABASES = {
    'default':  {
        'ENGINE': 'django.db.backends.postgresql_psycopg2',
        'NAME': 'db_name',
        'USER': 'name',
        'PASSWORD': '',
        'HOST': 'localhost',
        'PORT': '', 
        }
    }

```
- Migrate in bash ``` bash $ python manage.py migrate ```

- Create an admin account ``` bash $ python manage.py createsuperuser ```

- Then complete migrations ``` bash $ python manage.py makemigrations group-7 ```

- Then migrate again ``` bash $ python manage.py migrate ```

- and finally ``` bash $ python manage.py runserver ```

- Type localhost:8000 in a browser to see the app running

## Unit Testing Instructions

Unit tests will cover all use cases laid out in the use case diagrams. Once they are implemented they will be in the "apps" folder under "unitTests"

## System Testing Instructions

Once the app is implemented this is what you will use to start up the project to start testing it.

Start by running an instance of the web app by first entering the correct repository and then by entering the following bash $ python manage.py runserver  Now
that the app is running, open an internet browser and enter the address localhost:8000. The testing username and pasword will be described later but will allow the user to test every system in the app.

## Other Development Notes


