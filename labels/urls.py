from django.conf.urls import url
from labels import views

urlpatterns = [
    url(r'^labels', views.LabelList.as_view()),
    url(r'^datas/labels', views.DataLabel.as_view()),
]
