from django.conf.urls import url
from datasets import views

urlpatterns = [
    url(r'^datasets$', views.DatasetList.as_view()),
    url(r'^datasets/(?P<pk>[0-9]+)$', views.DatasetDetail.as_view()),
    url(r'^datasets/exports/(?P<pk>[0-9]+)/$', views.DatasetExport.as_view())
]
