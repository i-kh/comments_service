from django.conf.urls import url

from . import views

urlpatterns = [
    url(r'^$', views.CommentList.as_view()),
    url(r'^comment/(?P<pk>[0-9]+)/$', views.CommentDetail.as_view()),
    url(r'^top_comments/$', views.TopCommentList.as_view()),
    url(r'^inherited_comments/(?P<id>[0-9]+)/(?P<type>["comment", "post", "page"]+)/$', views.InheritedComments.as_view()),
    url(r'^user_history/$', views.UserCommentHistory.as_view()),
    url(r'^store_history/$', views.SaveHistory.as_view()),
]
