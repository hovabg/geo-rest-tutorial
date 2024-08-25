Language: [ESP](ESP.md) | [EN](README.md)

# Geospatial REST API

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

To avoid complications with installing libraries like GDAL, we'll be using Docker. We've created a Docker image with everything you need for this project.

All you need is Docker installed. Download and install Docker from [Docker](https://www.docker.com/products/docker-desktop/)


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

###  I: Let's configure our project settings.

#### INSTALLED_APPS

To enable GeoDjango and Django REST framework functionalities, we need to add the following apps to the ```INSTALLED_APPS``` list in our ```settings.py``` file:

```
INSTALLED_APPS = [
    # ... other apps ...
    'django.contrib.gis',  # For geospatial functionalities
    'rest_framework',
    'rest_framework_gis',  # For geospatial REST APIs
    'geo',  # Your app
]
```

#### Database 
For optimal performance and a wide range of geospatial functionalities, we recommend using PostgreSQL with the ```PostGIS``` extension. This combination provides a robust and scalable solution for storing and querying geographic data.

To configure your Django project to use PostgreSQL and PostGIS, update your ```settings.py``` file as follows:

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

- ENGINE: Specifies the database engine to use. In this case, ```django.contrib.gis.db.backends.postgis``` indicates that we will be using PostgreSQL with PostGIS.

Note: Make sure that your PostgreSQL database is running and that the PostGIS extension is enabled. If you're using Docker, consult your ```docker-compose.yml``` file for the specific database configuration.

### II: Model creation

To handle geographic data within our Django models, we'll leverage the spatial capabilities provided by ```django.contrib.gis```. This allows us to define fields that can store various geometric types, such as points, lines, and polygons.

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

Other available geographic field types:

- PointField: Represents a point feature, such as a hospital.
- LineStringField: Represents a linear feature, such as a road or river.
- PolygonField: Represents a polygonal area, such as a country or a building footprint.
- MultiPointField: Represents multiple points in a single geometry.
- MultiLineStringField: Represents multiple lines.
- MultiPolygonField: Represents multiple polygons.

### III: Serializers

When serializing Django models containing geographic fields, ```GeoFeatureModelSerializer``` from ```rest_framework_gis``` is the ideal choice. It simplifies the process of converting our Django objects into GeoJSON, a widely-used format for representing geographic data. This allows for easy consumption of our spatial data by various GIS applications and mapping platforms.

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

- GeoFeatureModelSerializer: This class is a subclass of ModelSerializer that adds support for geographic fields.
- model: Specifies the Django model to be serialized.
- fields: Indicates the model fields to be included in the JSON representation.
- geo_field: Defines the field containing the geographic geometry. This field will be serialized as a GeoJSON object.


### IV: Views

With our model (Restaurant) and its corresponding Serializer (RestaurantSerializer) in place, we're ready to integrate these components into a view for our REST API.

We'll use a ```ModelViewSet```, provided by Django REST Framework, which will handle the CRUD operations on restaurants automatically. This way, we can create a functional REST API with minimal code.

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

To efficiently manage our API's URLs, we'll use the ```router``` method provided by Django REST Framework. This approach significantly simplifies URL configuration, especially when dealing with multiple resources.

Example: 

In our app's ```urls.py``` file (for example, geo/urls.py), we'll configure the routes as follows:

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

In our project's main ```urls.py``` file (for example, proyect/urls.py), we'll include the URLs of our app:

```
from django.urls import path, include

urlpatterns = [
    path('', include('geo.urls')),
]
```

###  Optional, VI: Admin

To have a visual and geographic control over the data uploaded and managed through our API, GeoDjango provides us with a simple way to integrate a map into the admin panel. This will allow us to visualize the geographic location of each record.

To enable this functionality, we just need to make a small modification in our app's ```admin.py``` file:

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


