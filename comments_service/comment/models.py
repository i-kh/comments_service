from django.db import models

from comments_service.entity.models import Entity


class Comment(models.Model):
    entity = models.OneToOneField(Entity, verbose_name='entity')
    to = models.ForeignKey(Entity, verbose_name='comment_to', related_name='to',
                           null=True)
    text = models.TextField(verbose_name='comment_text')
    is_deleted = models.BooleanField(verbose_name='is_deleted', default=False)

    def __str__(self):
        return 'Comment {id}'.format(id=self.id)

    def has_inherited_comments(self):
        return self.entity.to.exists()
