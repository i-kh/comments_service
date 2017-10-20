from django.db import models

from comments_service.entity.models import Entity


class Post(models.Model):
    entity = models.OneToOneField(Entity, verbose_name='to')
    caption = models.CharField(max_length=255, verbose_name='caption')

    def __str__(self):
        return self.caption

