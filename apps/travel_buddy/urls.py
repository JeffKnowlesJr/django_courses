from django.conf.urls import url
from django.urls import path
from . import views

urlpatterns = [
    path('', views.index),
    path('create', views.create),
    path('dash', views.dash),
    path('join/<int:id>', views.join),
    path('login', views.login),
    path('logout', views.logout),
    path('add_travel', views.add_travel),
    path('process_travel', views.process_travel),
    path('plan/<int:id>', views.plan),
]
