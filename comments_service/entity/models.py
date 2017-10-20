from django.conf import settings
from django.db import models


class Entity(models.Model):
    user = models.ForeignKey(settings.AUTH_USER_MODEL, verbose_name='user')
    date = models.DateTimeField(verbose_name='date')

    def __str__(self):
        return 'Entity {id}'.format(id=self.id)

