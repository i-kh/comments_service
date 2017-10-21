from django.conf.urls import url

from . import views

urlpatterns = [
    url(r'^$', views.PostList.as_view()),
    url(r'^post/(?P<pk>[0-9]+)/$', views.PostDetail.as_view())
]
