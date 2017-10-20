import datetime

from django.contrib.postgres.fields import JSONField
from django.db import models
from comments_service.constants import CREATED, CHANGED, DELETED


class CommentHistory(models.Model):
    date = models.DateTimeField(default=datetime.datetime.now,
                                verbose_name='when')
    #  The user field does not present here, because it is already contained
    # in changes field (entity__user)
    # user = models.ForeignKey(settings.AUTH_USER_MODEL, verbose_name='Who')
    changes = JSONField(verbose_name='what')
    comment = models.ForeignKey('comment.Comment', verbose_name='Comment')
    type = models.CharField(max_length=1, choices=(
        (CREATED, 'Created'),
        (CHANGED, 'Changed'),
        (DELETED, 'Deleted'),
    ))

    def __str__(self):
        return 'History record [ {date}|Comment {id}]'.format(
            date=self.date.strftime('%d.%m.%Y %H:%M:%S'),
            id=self.id)
