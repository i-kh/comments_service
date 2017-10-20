from django.conf.urls import url

from . import views

urlpatterns = [
    url(r'^$', views.CommentHistoryList.as_view()),
    url(r'^(?P<comment_id>[0-9]+)/$',
        views.CommentHistoryParticular.as_view()),
]
