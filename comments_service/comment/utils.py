import datetime

from django.contrib.auth.models import User
from django.db.models import Q

from rest_framework import status
from rest_framework.response import Response

from comments_service.comment.models import Comment
from comments_service.comment.serializers import (
    CommentDeletedSerializer, CommentSerializer)
from comments_service.comment.tasks import save_history_to_file, \
    obtain_result_and_notify
from comments_service.constants import *
from comments_service.page.models import Page
from comments_service.post.models import Post


def get_json_serializer(with_deleted):
    return CommentDeletedSerializer if with_deleted else CommentSerializer


def get_history(model, id_, with_deleted=None, date_from=None, date_to=None,
                ext=None):
    models_dict = {COMMENT: Comment,
                   POST: Post,
                   PAGE: Page,
                   USER: User
                   }
    ext_serializer_dict = {JSON: (get_json_serializer, (with_deleted,))}
    ext = ext or JSON
    if ext not in ext_serializer_dict.keys():
        return Response(
            status=status.HTTP_500_INTERNAL_SERVER_ERROR,
            data={('Extension {ext} is incorrect. '
                   'Allowed extensions are [{extensions}]').format(
                ext=ext, extensions="|".join(ext_serializer_dict.keys()))})
    try:
        obj = models_dict.get(model).objects.get(
            id=id_)
    except models_dict.get(model).DoesNotExist:
        return Response(
            status=status.HTTP_500_INTERNAL_SERVER_ERROR,
            data={'error_message': '{model} with id={id} is not found'.format(
                model=model, id=id_)})
    serializer = ext_serializer_dict[ext][0](*ext_serializer_dict[ext][1])
    if model == USER:
        history = obtain_user_history(
            obj, serializer, with_deleted, date_from, date_to, True)
    else:
        history = get_inherited_comments(obj, serializer, with_deleted,
                                         date_from, date_to)
    save_to_file_task = save_history_to_file.delay(history, ext)
    obtain_result_and_notify.delay(save_to_file_task.id, 'file_url')
    data = dict(task_id=save_to_file_task.id)
    return Response(status=status.HTTP_200_OK, data=data)


def obtain_user_history(user, serializer=None, with_deleted=False,
                        date_from=None, date_to=None,
                        as_list=False):
    filter_params = dict(entity__user=user)
    if date_from:
        filter_params.update(datetime__gte=date_from)
    if date_to:
        filter_params.update(datetime__lte=date_to)
    comments = Comment.objects.filter(**filter_params)
    if not with_deleted:
        comments = comments.exclude(is_deleted=True)
    if as_list:
        comments = [serializer(comment).data if serializer else comment
                    for comment in comments]
    return comments


def get_inherited_comments(obj, serializer_class=None, with_deleted=False,
                           date_from=None, date_to=None):
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

    :param obj: Object to retrieve comments tree for
    :param serializer_class: response serializer
    :param with_deleted: if this parameter is True deleted comments are
           also included into the response
    :param date_from: if this parameter is passed then only comments older than
                      date_from is returned
    :param date_to: if this parameter is passed then only comments made earlier
                    than date_to is returned
    :param plain: If plain is False than objects in list are
                    serialized for Http response using serializer_class
    :return: list of comments
            Example: [A, [[[B,[C,[]]]],[D,[[E,[]],[F,[G]]]], [H,[]]]]
    """
    response_list = list()
    operation_stack = list()
    operation_stack.append([obj, response_list])
    date_filter = Q()
    exclude_filter = Q()
    if date_from:
        date_filter &= Q(entity__date__gte=date_from)
    if date_to:
        date_filter &= Q(entity___date_lte=date_to)
    if not with_deleted:
        exclude_filter &= Q(is_deleted=True)

    while operation_stack:
        comment, comment_list = operation_stack.pop(0)
        sub_list = [[comment, list()] for comment in
                    comment.entity.to.filter(date_filter).exclude(
                        exclude_filter)]
        if sub_list:
            comment_list.extend(
                [[serializer_class(comment).data if
                  serializer_class else comment, lst]
                 for (comment, lst) in sub_list])
            operation_stack.extend(sub_list)
    return response_list


def extract_date(request, key, format_=None):
    format_ = format_ or '%Y-%m-%dT%H:%M:%SZ'
    try:
        return datetime.datetime.strptime(request.data.get(key), format_)
    except TypeError: # No key in request.data is found
        return None


############################################################################
def get_entity_obj(_id, _type):
    # TODO: придумать как красиво использовать только эту ф-ю во всех вьюхах
    # success, obj = get_entity_obj(id, type)
    # if not success:
    #     return Response(**obj)# success, obj = get_entity_obj(id, type)

    models_dict = {COMMENT: Comment,
                   POST: Post,
                   PAGE: Page}
    try:
        obj = models_dict.get(_type).objects.get(
            id=_id)
    except models_dict.get(_type).DoesNotExist:
        return False, dict(
            status=status.HTTP_500_INTERNAL_SERVER_ERROR,
            data={'error_message': '{model} with id={id} is not found'.format(
                model=_type, id=_id)})
    return True, obj

############################################################################

