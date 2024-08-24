# GIS REST API

A brief tutorial on how to create and configure a REST API using GeoDjango and Django REST framework with geospatial components. This guide aims to provide a quick and basic introduction to building a geospatial REST API.

## Getting Started

Before we dive in, make sure you're familiar with Django and Django REST framework. We'll be using these frameworks, along with GeoDjango, to build our geospatial REST API.

To get started, install the following packages:
- Django
- Django REST framework
- Django REST framework GIS
- GDAL
- PROJ
- GEOS
- psycopg2

### Prerequisites

Installing libraries like GDAL on Windows can be complex. To simplify the process, we recommend using Docker. If you have Docker installed, you can find the necessary Dockerfile and build instructions in the repository.

### Installing

Navigate to the project directory: Open your terminal or command prompt and navigate to the directory where your project files are located.

Start the container: Run the following command to build and start the Docker container (this may take a while):

```
docker-compose build
docker-compose up -d
```
Enter the container: Once the container is running, use the following command to enter a bash shell within the container:

```
docker exec -it geoapp bash
```

Run the Django server: Inside the container, execute the following command to start the Django development server in order to take a look the example:

```
python manage.py runserver 
```

## Tutorial

Let's begin building our project from the ground up. We'll assume you have a Django project and app already set up.

###  I: Let's configure our project settings, specifically INSTALLED_APPS and DATABASES.

#### INSTALLED_APPS

1) Add django.contrib.gis for using GeoDjango.
2) Add rest_framework and rest_framework_gis in that order for using Geo serializers.

```
INSTALLED_APPS = [
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',
    # Add contrib gis for use geodjango.
    'django.contrib.gis',
    # Add rest and rest_gis for create a geo api's
    'rest_framework',
    'rest_framework_gis',
    # Your app
    'geo',
]
```

#### Database 
Add your PostgreSQL/PostGIS database credentials. Remember to set the ENGINE to django.contrib.gis.db.backends.postgis.

Example:

```
DATABASES = {
    'default': {
        'ENGINE': 'django.contrib.gis.db.backends.postgis',
        'NAME': 'gis',
        'USER': 'your_username',
        'PASSWORD': 'your_password',
        'HOST': 'your_host',
        'PORT': '5432',
    }
}
```
Note: Replace your_username, your_password, your_host with your actual database credentials.

### II: Model creation

To create models, we'll use contrib.gis to import spatial models. This allows us to add geospatial fields like models.MultiPointField() to our database.

Example:

```
from django.contrib.gis.db import models

class Restaurant(models.Model):

    name = models.CharField(max_length=50)
    qualifications = models.IntegerField()
    owner = models.CharField(max_length=50)
    # Use MultiPoint Field for have access to different geom  options like geojson.
    ppoly = models.MultiPointField(srid=4326)  
    def __str__(self):
        return self.name
```

### III: Serializers

We have multiple options for creating serializers, but we'll use GeoFeatureModelSerializer from rest_framework_gis. This serializer provides a concise way to implement the basic methods of an API and also supports GeoJSON, which is our target format.

Example:

```
from rest_framework_gis.serializers import GeoFeatureModelSerializer
from .models import Restaurant

class RestaurantSerializer(GeoFeatureModelSerializer):
    class Meta:
        model = Restaurant
        fields = ['name', 'qualifications', 'owner', 'ppoly']
        # Field that is serialized as spatial geometry
        geo_field = 'ppoly'

```

### IV: Urls

To manage our API's URLs, we'll use the router method provided by rest_framework.routers. This will simplify the URL configuration process.

Example: 

'name-app'/urls.py

```
from django.urls import path, include
from rest_framework.routers import DefaultRouter
from .views import RestaurantViewSet


router = DefaultRouter()
router.register(r'restaurant', RestaurantViewSet)

urlpatterns = [
    path('', include(router.urls)),
]
```

'proyect'/urls.py

```
from django.urls import path, include

urlpatterns = [
    path('', include('geo.urls')),
]
```

###  Optional, V: Admin

If you want to have geospatial control over the data uploaded through your API, GeoDjango provides a convenient way to achieve this. Simply add the following configuration to your app's admin.py file.

```
from django.contrib import admin
from django.contrib.gis.admin import GISModelAdmin
from .models import Restaurant

# Register your models here, using Gis model admin.

admin.site.register(Restaurant, GISModelAdmin)
```

This will allow us to see uploaded fields and their locations on a map within the server's admin panel.


## Discover more in the documentation!

* [GeoDjango](https://docs.djangoproject.com/en/4.2/ref/contrib/gis/) 
* [Django-rest-framework-gis](https://github.com/openwisp/django-rest-framework-gis) 
* [Django-rest-framework](https://www.django-rest-framework.org/) 

## Contributing

Want to help improve the tutorial? Let me know!

If something doesn't make sense or is wrong, please let me know! Constructive feedback is always appreciated.

## Authors

* **Hovannes Borras Gurlekian** - [HovaBg](https://github.com/hovabg)


## License

This project is licensed under the MIT License - see the [LICENSE.md](LICENSE.md) file for details


