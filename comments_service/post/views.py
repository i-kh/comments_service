from rest_framework import generics
from comments_service.post.models import Post
from comments_service.post.serializers import PostSerializer


class PostList(generics.ListCreateAPIView):
    """
    List all comments, or create a new comment.
    """
    queryset = Post.objects.all()
    serializer_class = PostSerializer


class PostDetail(generics.RetrieveUpdateDestroyAPIView):
    """
    Retrieve, update or delete comment instance.
    """
    queryset = Post.objects.all()
    serializer_class = PostSerializer
