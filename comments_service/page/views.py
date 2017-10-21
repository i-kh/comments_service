from rest_framework import generics

from comments_service.page.models import Page
from comments_service.page.serializers import PageSerializer


class PageList(generics.ListCreateAPIView):
    """
    List all comments, or create a new comment.
    """
    queryset = Page.objects.all()
    serializer_class = PageSerializer


class PageDetail(generics.RetrieveUpdateDestroyAPIView):
    """
    Retrieve, update or delete comment instance.
    """
    queryset = Page.objects.all()
    serializer_class = PageSerializer
