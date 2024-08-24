from django.contrib import admin
from django.contrib.gis.admin import GISModelAdmin
from .models import Restaurant

# Register your models here, using Gis model admin.
# Registra los modelos aqui, usando Gis model admin.
admin.site.register(Restaurant, GISModelAdmin)