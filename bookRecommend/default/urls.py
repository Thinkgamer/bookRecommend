from django.conf.urls import include, url
from django.contrib import admin

urlpatterns = [
    url(r"^admin/(.+)/$",'default.views.admin'),
    url(r"^login/$",'default.views.login'),
    url(r"^umanago/(.+)/(\d+)/$",'default.views.umanago'),
    url(r"^umanage/(.+)/(\d+)/$",'default.views.umanage'),
    url(r"^deluser/(.+)/(.+)/$",'default.views.deluser'),
    url(r"^adduser/(.+)/$",'default.views.adduser'),


    url(r"^amanage/(.+)/$",'default.views.amanage'),
    url(r"^adel/(.+)/(.+)/$",'default.views.adel'),
    url(r"^aadd/(.+)/$",'default.views.aadd'),

    url(r"^bmanage/(.+)/(\d+)/$",'default.views.bmanage'),
    url(r"^changebook/(.+)/(.+)/$",'default.views.changebook'),
    url(r"^show/(.+)/(.+)/$",'default.views.show'),
    url(r"^bookdel/(.+)/(.+)/$",'default.views.bookdel'),
    url(r"^addbook/(.+)/$",'default.views.addbook'),
]
