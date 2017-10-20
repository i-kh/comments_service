from django.apps import AppConfig


class CommentConfig(AppConfig):
    name = 'comments_service.comment'
    verbose_name = 'Comment'

    def ready(self):
        import comments_service.comment.signals.handlers
