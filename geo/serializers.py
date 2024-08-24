from rest_framework_gis.serializers import GeoFeatureModelSerializer
from .models import Restaurant


class RestaurantSerializer(GeoFeatureModelSerializer):
    class Meta:
        model = Restaurant
        fields = ['name', 'qualifications', 'owner', 'ppoly']
        # Field that is serialized as spatial geometry
        geo_field = 'ppoly'  # Campo que se serializa como geometría espacial

