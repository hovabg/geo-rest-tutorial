Language:[ESP](ESP.md)|[EN](README.md)

# GIS REST API

A brief tutorial on how to create and configure a REST API using GeoDjango and Django REST framework with geospatial components. This guide aims to provide a quick and basic introduction to building a geospatial REST API.

## Getting Started

Before we dive in, make sure you're familiar with Docker, Django and Django REST framework. We'll be using these frameworks, along with GeoDjango, to build our geospatial REST API.

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
    # ... ...
    'django.contrib.gis',  
    'resrt_framework',
    'rest_framework_gis',  
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
### IV: Views

With our model (Restaurant) and its corresponding Serializer (RestaurantSerializer) in place, we're ready to integrate these components into a view for our REST API.

We'll use a ModelViewSet, provided by Django REST Framework, which will handle the CRUD operations on restaurants automatically. This way, we can create a functional REST API with minimal code.

Example:

```
from rest_framework import viewsets
from .models import Restaurant
from .serializers import RestaurantSerializer


# Create your views here.
class RestaurantViewSet(viewsets.ModelViewSet):
    queryset = Restaurant.objects.all()
    serializer_class = RestaurantSerializer


```

### V: Urls

To efficiently manage our API's URLs, we'll use the router method provided by Django REST Framework. This approach significantly simplifies URL configuration, especially when dealing with multiple resources.

Example: 

In our app's urls.py file (for example, geo/urls.py), we'll configure the routes as follows:

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

In our project's main urls.py file (for example, proyect/urls.py), we'll include the URLs of our app:

```
from django.urls import path, include

urlpatterns = [
    path('', include('geo.urls')),
]
```

###  Optional, VI: Admin

To have a visual and geographic control over the data uploaded and managed through our API, GeoDjango provides us with a simple way to integrate a map into the admin panel. This will allow us to visualize the geographic location of each record.

To enable this functionality, we just need to make a small modification in our app's admin.py file:

```
from django.contrib import admin
from django.contrib.gis.admin import GISModelAdmin
from .models import Restaurant

# Register your models here, using Gis model admin.

admin.site.register(Restaurant, GISModelAdmin)
```



## Discover more in the documentation!

* [GeoDjango](https://docs.djangoproject.com/en/4.2/ref/contrib/gis/) 
* [Django-rest-framework-gis](https://github.com/openwisp/django-rest-framework-gis) 
* [Django-rest-framework](https://www.django-rest-framework.org/) 

## Contributing

Want to help improve the tutorial? Let me know!

Do you think something is missing from this tutorial? Is there any concept that's not clear? Let me know! Your feedback will help to create an even better and more comprehensive tutorial.

## Authors

* **Hovannes Borras Gurlekian** - [HovaBg](https://github.com/hovabg)


## License

This project is licensed under the MIT License - see the [LICENSE.md](LICENSE.md) file for details


