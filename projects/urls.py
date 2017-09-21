from django.conf.urls import url
from projects import views

urlpatterns = [
    url(r'^projects$', views.ProjectList.as_view()),
    url(r'^projects/(?P<pk>[0-9]+)$', views.ProjectDetail.as_view()),
    url(r'^projects/exports/(?P<pk>[0-9]+)$', views.ProjectExport.as_view()),

]
