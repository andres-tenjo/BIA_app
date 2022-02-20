from django.db import models
from django.db.models import Model
from django.conf import settings

class BaseModel(models.Model):
    user_creation = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE,
                                        null=True, blank=True, related_name='%(app_label)s_%(class)s_creation')
    creation_date = models.DateTimeField(auto_now_add=True, null=True, blank=True)
    user_update = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE,
                                        null=True, blank=True, related_name='%(app_label)s_%(class)s_updated')
    update_date = models.DateTimeField(auto_now=True, null=True, blank=True)

    class Meta:
        abstract = True