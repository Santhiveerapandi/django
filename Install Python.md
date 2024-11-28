# Install Python 3
sudo apt install python3

# Verify the Installation
python3 --version

# Install pip (Python Package Installer)
sudo apt install python3-pip

# Verify the pip installation:
pip3 --version

# Install Virtual Environment (Optional)
sudo apt install python3-venv


# 1. Navigate to Your Project Directory
cd /var/www/html/backup/

# To activate it, follow these steps:
python3 -m venv myenv
cd myenv
pip install django djangorestframework
pip install psycopg2-binary

# 2. Activate the Virtual Environment
. myenv/bin/activate

cd python-projects

# Create a Django Project:
django-admin startproject firstapp

cd firstapp

# Change database connection in settings.py
DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.postgresql',
        'NAME': 'mydatabase', #change it databasename
        'USER': 'postgres', #change it database user name
        'PASSWORD': 'root', # change user database password
        'HOST': 'localhost',  
        'PORT': '5432',           
    }
}
# Create a Django App:
python manage.py startapp movie

python manage.py migrate    


# Define Models Task Model
. We’ll create a `Movie` model in `movie/models.py`. 

from django.db import models

class Movie(models.Model):
    name = models.CharField(max_length=100)
    director = models.TextField()
    completed = models.BooleanField(default=True)

    def __str__(self):
        return self.name

# Migrations and Database Setup:
This is where we tell Django to create our database tables based on our app’s models.
Run these commands:

python manage.py makemigrations
python manage.py migrate


python manage.py makemigrations firstapp
python manage.py migrate

python manage.py runserver

python manage.py runserver 192.168.2.142:8000

# Method 1: Using python manage.py show_urls with django-extensions

## 1. Install django-extensions if you haven't already:
pip install django-extensions

## 2. Add django_extensions to your INSTALLED_APPS in settings.py:
INSTALLED_APPS = [
    # other apps
    'django_extensions',
]

## 3.Run the following command to list all URLs:
python manage.py show_urls

## 4. Create admin user
python manage.py createsuperuser

References: https://medium.com/@learncodeguide/creating-a-crud-api-with-django-rest-framework-and-postgresql-3ead7ffb140f

## ref: https://www.geeksforgeeks.org/django-rest-api-crud-with-drf/

## 5. GraphQL support with django-extensions
1.pip install graphene-django
2.Update your settings.py file:

INSTALLED_APPS = [
    # other apps
    "graphene_django",
]

3. Set Up the GraphQL Endpoint
In your settings.py, define the GRAPHENE configuration:

GRAPHENE = {
    "SCHEMA": "myapp.schema.schema",  # Replace 'myapp' with your app name
}

4. Create a Schema File
In your app folder (e.g., myapp), create a file called schema.py to define your GraphQL schema.

Example schema.py:

import graphene
from graphene_django.types import DjangoObjectType
from myapp.models import Department

# Define a GraphQL type for the Department model
class DepartmentType(DjangoObjectType):
    class Meta:
        model = Department

# Define Query class
class Query(graphene.ObjectType):
    departments = graphene.List(DepartmentType)

    def resolve_departments(root, info, **kwargs):
        return Department.objects.all()

# Define the schema
schema = graphene.Schema(query=Query)


5. Define a URL Route for GraphQL
In your project's urls.py:

from django.urls import path
from graphene_django.views import GraphQLView

urlpatterns = [
    # Other routes
    path("graphql/", GraphQLView.as_view(graphiql=True)),  # Enable the GraphiQL interface
]


