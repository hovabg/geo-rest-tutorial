from django.db import models
from django.contrib.gis.db import models


# Create your models here.

class Restaurant(models.Model):

    name = models.CharField(max_length=50)
    qualifications = models.IntegerField()
    owner = models.CharField(max_length=50)
    # Use MultiPoint Field for have access to different geom  options like geojson.
    # Usar el campo MultiPoint para tener acceso a diferentes opciones de geom como  geojson.
    ppoly = models.MultiPointField(srid=4326)  # Utilizando SRID 4326 para WGS84

    def __str__(self):
        return self.name
