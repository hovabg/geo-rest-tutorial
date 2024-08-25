Idioma:  [ESP](ESP.md) | [EN](README.md)

# API REST geoespacial

En este tutorial, se explican los pasos iniciales para construir una API REST que maneje datos geográficos utilizando GeoDjango y Django REST Framework. A lo largo del proceso, se cubrirán desde la configuración básica hasta la implementación de funcionalidades clave para gestionar y consultar datos espaciales, ideal para quienes están comenzando a explorar el mundo de las aplicaciones geoespaciales.

## ¡Manos a la obra!

Antes de comenzar, asegúrate de tener un buen entendimiento de:

- Docker: Para agilizar nuestro entorno de desarrollo.
- Django: El marco web que será la base de nuestra API.
- Django REST framework: La herramienta ideal para crear APIs REST.

Con estos conocimientos, estaremos listos para sumergirnos en el mundo de GeoDjango y construir nuestra API geoespacial.

Paquetes a utilizar:
- Django
- Django REST framework
- Django REST framework GIS
- GDAL
- PROJ
- GEOS
- psycopg2

Estos paquetes ya están incluidos en la imagen de Docker que utilizaremos más adelante.

### Pre-requisitos

Para evitar complicaciones con la instalación de librerías como GDAL, utilizaremos Docker. Hemos creado una imagen de Docker con todo lo necesario para este proyecto.

Solo necesitas tener Docker instalado. Descarga e instala Docker desde [enlace para descargar Docker](https://www.docker.com/products/docker-desktop/).


### Instalacion

Navega al directorio del proyecto: Abre una terminal o línea de comandos en la carpeta donde se encuentra este archivo ```README.md``` (o donde esté ubicado tu archivo de configuración).

Construye e inicia el contenedor Docker: Ejecuta los siguientes comandos para construir la imagen de Docker y luego iniciar un contenedor a partir de ella:

```
docker-compose build
docker-compose up -d
```

Accede al contenedor: Para interactuar con el contenedor en ejecución, utiliza el siguiente comando:

```
docker exec -it geoapp bash
```

Inicia el servidor de desarrollo de Django: Una vez dentro del contenedor, inicia el servidor de desarrollo de Django, para darle una mirada a la api de ejemplo:

```
python manage.py runserver 
```

## Tutorial

Empecemos a constuir nuestro proyecto, partiendo de que tanto el proyecto como la  app de django estan ya creados.

### I: Configuración del Proyecto

#### INSTALLED_APPS

Para habilitar las funcionalidades de GeoDjango y Django REST framework, debemos agregar las siguientes aplicaciones a la lista ```INSTALLED_APPS``` en nuestro archivo ```settings.py```:

```
INSTALLED_APPS = [
    # ... otras aplicaciones ...
    'django.contrib.gis',  # Para funcionalidades geoespaciales
    'rest_framework',
    'rest_framework_gis',  # Para APIs REST geoespaciales
    'geo',  # Tu aplicación
]
```
- django.contrib.gis: Proporciona las herramientas necesarias para trabajar con datos geográficos en Django (GeoDjango).
- rest_framework: El framework para crear APIs REST.
- rest_framework_gis: Una extensión de rest_framework para trabajar con datos geoespaciales en las APIs.


#### Database

Para aprovechar al máximo las capacidades de GeoDjango, recomendamos utilizar PostgreSQL con la extensión ```PostGIS```. Configura la base de datos en tu archivo ```settings.py``` de la siguiente manera:

Ejemplo:

```
DATABASES = {
    'default': {
        'ENGINE': 'django.contrib.gis.db.backends.postgis',
        'NAME': 'gis',
        'USER': 'tu_usuario',
        'PASSWORD': 'tu_contraseña',
        'HOST': 'tu_host',
        'PORT': '5432',
    }
}
```
- ENGINE: Especifica el motor de base de datos a utilizar. En este caso, ```django.contrib.gis.db.backends.postgis``` indica que usaremos PostgreSQL con PostGIS.

Nota: Asegúrate de que la base de datos y la extensión PostGIS estén creadas y configuradas correctamente en tu sistema o en tu entorno Docker. Si estás utilizando Docker, las credenciales y configuración de la base de datos suelen estar definidas en el archivo ```docker-compose.yml```.

### II: Creacion de modelos

Para trabajar con datos geográficos en Django, utilizaremos los modelos espaciales proporcionados por ```django.contrib.gis```. Estos modelos nos permiten definir campos geográficos como puntos, líneas y polígonos.

Ejemplo:

```
from django.contrib.gis.db import models

class Restaurant(models.Model):

    name = models.CharField(max_length=50)
    qualifications = models.IntegerField()
    owner = models.CharField(max_length=50)
 
    ppoly = models.MultiPointField(srid=4326)  

    def __str__(self):
        return self.name
```

- models.MultiPointField: Este campo permite almacenar múltiples puntos en una sola geometría.
- srid: Especifica el sistema de referencia espacial (CRS) de la geometría. 

Otros tipos de campos geográficos:

- PointField: Para representar un solo punto, como un hospital.
- LineStringField: Para representar una línea, como rios o carreteras.
- PolygonField: Para representar un polígono, como un pais o construir footprint's.
- MultiPointField: Para represnetar multiples puntos en una sola geometria.
- MultiLineStringField: Para represnetar multiples lineas.
- MultiPolygonField: Para represnetar multiples poligonos.


### III: Creacion de Serializers

Hay varias opciones a la hora de crear serializadores pero en el caso de datos geográficos, uno de los serializador  más adecuado es ```GeoFeatureModelSerializer```, proporcionado por el paquete ```rest_framework_gis```. Este serializador permite transformar nuestros objetos Django en objetos GeoJSON, un formato estándar para representar datos geográficos.

Ejemplo:

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

- GeoFeatureModelSerializer: Esta clase es una subclase de ModelSerializer que agrega soporte para campos geográficos.
- model: Especifica el modelo Django que se va a serializar.
- fields: Indica los campos del modelo que queremos incluir en la representación JSON.
- geo_field: Define el campo que contiene la geometría geográfica. Este campo será serializado como un objeto GeoJSON.


### IV: Creacion de vistas

Con nuestro modelo (Restaurant) y su serializador (RestaurantSerializer) estamos preparados para integrar estos componentes en una vista de nuestra API REST.

Emplearemos un ```ModelViewSet```, proporcionado por Django REST Framework, que se encargará de gestionar las operaciones CRUD sobre los restaurantes de manera automática. De esta forma, podremos crear una API REST funcional con un mínimo de código.

Para este ejemplo, crearemos una vista basica de la siguiente forma:

```
from rest_framework import viewsets
from .models import Restaurant
from .serializers import RestaurantSerializer


class RestaurantViewSet(viewsets.ModelViewSet):
    queryset = Restaurant.objects.all()
    serializer_class = RestaurantSerializer

```

### V: Urls

Para gestionar las URL de nuestra API de manera eficiente, utilizaremos el método ```router``` proporcionado por Django REST Framework. Este enfoque simplifica significativamente la configuración de las rutas, especialmente cuando trabajamos con múltiples recursos.

Ejemplo:

En el archivo ```urls.py``` de nuestra aplicación (por ejemplo, geo/urls.py), configuraremos las rutas de la siguiente manera:

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

En el archivo ```urls.py``` de nuestro proyecto principal (por ejemplo, proyect/urls.py), incluiremos las URL de nuestra aplicación

```
from django.urls import path, include

urlpatterns = [
    path('', include('geo.urls')),
]
```

### Opcional, VI: Admin

Para tener un control visual y geográfico de los datos cargados a través de nuestra API, GeoDjango nos ofrece una forma sencilla de integrar un mapa en el panel de administración. Esto nos permitirá visualizar la ubicación geográfica de cada registro.

Para habilitar esta funcionalidad, solo necesitamos realizar una pequeña modificación en el archivo ```admin.py``` de nuestra aplicación:

```
from django.contrib import admin
from django.contrib.gis.admin import GISModelAdmin
from .models import Restaurant

# Register your models here, using Gis model admin.

admin.site.register(Restaurant, GISModelAdmin)
```

## Descubre más en la documentacion!

* [GeoDjango](https://docs.djangoproject.com/en/4.2/ref/contrib/gis/) 
* [Django-rest-framework-gis](https://github.com/openwisp/django-rest-framework-gis) 
* [Django-rest-framework](https://www.django-rest-framework.org/) 

## Contribución

¿Quieres colaborar en este tutorial? Escribeme

¡Ayúdame a mejorar este tutorial! Si encuentras algún error, falta de claridad o quieres sugerir una mejora, ¡no dudes en compartir tu opinión! Tu feedback simepre es bienvenido.

## Autor

* **Hovannes Borras Gurlekian** - [HovaBg](https://github.com/hovabg)

## Licencia 

Este proyecto está bajo la licencia MIT - Consulta el archivo [LICENSE.md](LICENSE.md)  para más detalles.
















