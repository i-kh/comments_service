from django.db.models.signals import pre_save, post_save
from django.dispatch import receiver

from comments_service.comment.models import Comment
from comments_service.comment.notify import send_notification
from comments_service.constants import CHANGED, CREATED, DELETED
from comments_service.history.models import CommentHistory
from comments_service.history.serializers import CommentHistorySerializer


@receiver(pre_save, sender=Comment)
def pre_save(sender, instance, **kwargs):
    _id = getattr(instance, 'id', None)
    _type = CREATED if not _id else CHANGED
    if _id and _type == CHANGED:
        old_instance = Comment.objects.get(pk=_id)
        if old_instance.is_deleted != instance.is_deleted and instance.is_deleted:
            _type = DELETED

        create_historical_record(instance, old_instance, _type)


@receiver(post_save, sender=Comment)
def post_delete(instance, created,  **kwargs):
    if created:
        create_historical_record(instance, None, CREATED)


def create_historical_record(new_instance, old_instance, _type):
    changes = {}
    for field in new_instance._meta.fields:
        #  Assume that entity fields are never changes
        changes[field.attname] = (
            getattr(old_instance, field.attname, None),
            getattr(new_instance, field.attname, None)
        )

    history_obj = CommentHistory.objects.create(
        comment=new_instance,
        type=_type,
        changes=changes
    )
    send_notification(CommentHistorySerializer(history_obj).data)
