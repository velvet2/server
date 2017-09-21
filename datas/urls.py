from django.conf.urls import url
from datas import views

urlpatterns = [
    url(r'^datas/(?P<dataset_id>[0-9]+)$', views.DataList.as_view()),
    # url(r'^datas/(?P<pk>[0-9]+)/$', views.DatasetDetail.as_view()),
]
