from rest_framework import generics

from comments_service.history.models import CommentHistory
from comments_service.history.serializers import CommentHistorySerializer


class CommentHistoryList(generics.ListAPIView):
    """
    List all comment historical records
    """
    queryset = CommentHistory.objects.all()
    serializer_class = CommentHistorySerializer


class CommentHistoryParticular(generics.ListAPIView):
    """
    Retrieve, update or delete comment instance.
    """
    queryset = CommentHistory.objects.all()
    serializer_class = CommentHistorySerializer

    def list(self, request, *args, **kwargs):
        comment_id = kwargs.get('comment_id')
        self.queryset = self.queryset.filter(comment_id=comment_id)

        return super(CommentHistoryParticular, self).list(
            request, *args, **kwargs)
