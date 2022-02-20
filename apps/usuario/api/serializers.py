from rest_framework import serializers
from django.contrib.auth.models import Permission

class PermissionsSerializer(serializers.ModelSerializer):
    
    class Meta:
        model = Permission
        fields = ('__all__')