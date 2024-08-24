# Rest GIS api

Small tutorial on how to configure and create a rest api with django rest framework with geometry fields

## Getting Started

The first thing to keep in mind is that we will be using geodjango and django rest framework, therefore it is necessary to know how to use django and django rest framework

To start you need to install:
 -django
 -djangorestframework
 -djangorestframework-gis
 -gdal
 -proj
 -geos
 -psycopg2

### Prerequisites

Using libraries like gdal, which are complicated to install on Windows, is the use of docker which makes it much easier. So if you have docker installed, in the repository you will find what you need to build the container.


### Installing

First step: Use cmd for create a docker container in the yml path you have to execute this command

```
docker-compose up -d
```

that take a time, so after finish the process, enter  next command for use the container

```
docker exec -it geoapp bash
```

Now you only have to run the django server in order to take a look the example:

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

* **Hovannes Borras Gurlekian** - *Initial work* - [PurpleBooth](https://github.com/PurpleBooth)


## License

This project is licensed under the MIT License - see the [LICENSE.md](LICENSE.md) file for details

## Acknowledgments

* Hat tip to anyone whose code was used
* Inspiration
* etc

