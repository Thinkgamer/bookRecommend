from django.conf.urls import include, url
from django.contrib import admin

urlpatterns = [
    url(r"^index/(\w+)/$",'index.views.index'),
    url(r"^hot/(\w+)/$",'index.views.hot')
]
