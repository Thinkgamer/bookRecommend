from django.conf.urls import include, url
from django.contrib import admin

urlpatterns = [
    url(r"^login/$",'login.views.login'),
    url(r"^see/$",'login.views.see'),
]
