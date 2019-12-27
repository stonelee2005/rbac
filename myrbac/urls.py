from django.conf.urls import url
from django.urls import re_path

from myrbac import views

app_name='[rbac]'
urlpatterns = [
    re_path(r'^role/list/$',views.role_list, name='role_list'),
]
