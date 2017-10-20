from django.contrib.auth.models import User
from rest_framework import generics
from rest_framework import mixins
from rest_framework import status
from rest_framework.response import Response

from comments_service.comment.models import Comment
from comments_service.comment.serializers import (
    CommentSerializer, CommentDeletedSerializer)
from comments_service.comment.utils import (
    get_inherited_comments, obtain_user_history, get_json_serializer,
    extract_date, get_history)
from comments_service.constants import *
from comments_service.page.models import Page
from comments_service.post.models import Post


class CommentList(generics.ListCreateAPIView):
    """
    List all comments, or create a new comment.
    """
    queryset = Comment.objects.exclude(is_deleted=True)
    serializer_class = CommentSerializer


class CommentDetail(generics.RetrieveUpdateDestroyAPIView):
    """
    Retrieve, update or delete comment instance.
    """
    queryset = Comment.objects.exclude(is_deleted=True)
    serializer_class = CommentSerializer

    def perform_destroy(self, instance):
        if not instance.has_inherited_comments():
            instance.is_deleted = True
        instance.save()


class TopCommentList(generics.ListAPIView):
    """
    List all comments, or create a new comment.
    """
    queryset = Comment.objects.filter(to__isnull=True)
    serializer_class = CommentSerializer


class InheritedComments(mixins.RetrieveModelMixin, generics.GenericAPIView):
    """
    Returns list of comments
    The list has the following view
    [A, [[[B,[C,[]]]],[D,[[E,[]],[F,[G]]]], [H,[]]]]
    which corresponds to the following tree
            A
          / |\
         /  | \
        /   \  \
        B   D  H
        \  / \
        C E  F
            /
           G

    """
    queryset = Comment.objects.all()
    serializer_class = CommentSerializer

    def get(self, request, *args, **kwargs):
        id_, type_ = self.kwargs['id'], self.kwargs['type']
        models_dict = {COMMENT: Comment,
                       POST: Post,
                       PAGE: Page}
        try:
            obj = models_dict.get(type_).objects.get(
                id=id_)
        except models_dict.get(type_).DoesNotExist:
            return Response(status=status.HTTP_500_INTERNAL_SERVER_ERROR)
        return Response(get_inherited_comments(obj, self.serializer_class))


class UserCommentHistory(mixins.ListModelMixin, generics.GenericAPIView):
    """
    Returns list of user comments
    """
    queryset = Comment.objects.all()
    serializer_class = CommentDeletedSerializer

    def list(self, request, *args, **kwargs):
        try:
            user_id = request.data['user_id']
        except KeyError:
            return Response(status=status.HTTP_500_INTERNAL_SERVER_ERROR,
                            exception='No User ID in request')
        try:
            user = User.objects.get(id=user_id)
        except User.DoesNotExist:
            return Response(status=status.HTTP_500_INTERNAL_SERVER_ERROR,
                            exception='Incorrect User ID')
        with_deleted = (request.data.get('with_deleted', 'False').lower() in
                        ['true', '1'])

        self.queryset = obtain_user_history(
            user,
            serializer=get_json_serializer(with_deleted),
            with_deleted=with_deleted)
        return super(UserCommentHistory, self).list(request, *args, **kwargs)

    def post(self, request, *args, **kwargs):
        """
        request should contain the following arguments
        :param user_id: ID of the user
        :param with_deleted: if equals to true or 1 then the response
        contains both deleted and not deleted comments and only not deleted
        comments otherwise
        """
        return self.list(request, *args, **kwargs)


class SaveHistory(mixins.ListModelMixin, generics.GenericAPIView):
    queryset = Comment.objects.all()
    serializer_class = CommentDeletedSerializer

    def list(self, request, *args, **kwargs):
        try:
            id_ = request.data['id']
        except KeyError:
            return Response(status=status.HTTP_500_INTERNAL_SERVER_ERROR,
                            exception='No object ID in request')
        with_deleted = (request.data.get('with_deleted', 'False').lower() in
                        ['true', '1'])
        date_from = extract_date(request, 'date_from')
        date_to = extract_date(request, 'date_to')
        model = request.data.get('model')
        ext = request.data.get('format')
        return get_history(model, id_, with_deleted, date_from, date_to, ext)

    def post(self, request, *args, **kwargs):
        """
        request should contain the following arguments
        :param id: ID of an object
        :param model: object model name [comment|post|page|user]
        :param date_from: look date_to
        :param date_to: not required param to filter results by creation dates
        :param with_deleted: if equals to true or 1 then the response
        contains both deleted and not deleted comments and only not deleted
        comments otherwise
        :param format: file format to store data to
        """
        return self.list(request, *args, **kwargs)


