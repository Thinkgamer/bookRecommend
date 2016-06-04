from django.conf.urls import include, url
from django.contrib import admin

urlpatterns = [
    # url(r"^index/(\w+)/$",'index.views.index'),
    url(r"^index/(.+)/$",'index.views.index'),
    url(r"^index/$",'login.views.login'),
    url(r"^more/(.+)/$",'index.views.more'),
    url(r"^new/(.+)/$",'index.views.new'),
    url(r"^hot/(.+)/$",'index.views.hot'),
    url(r"^details/(.+)/(.+)/$",'index.views.details'),
    url(r"change/(.+)/$","index.views.change")
]
