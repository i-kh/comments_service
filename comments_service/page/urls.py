from django.conf.urls import url

from . import views

urlpatterns = [
    url(r'^$', views.PageList.as_view()),
    url(r'^page/(?P<pk>[0-9]+)/$', views.PageDetail.as_view())
]
