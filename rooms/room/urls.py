from django.conf.urls import include, url
from django.contrib import admin

urlpatterns = [
    url(r'^login/', 'room.views.login'),
    url(r'^insertPerson/', 'room.views.insertPerson'),
    url(r'^success/', 'room.views.success'),
    url(r'^getRooms/', 'room.views.getRooms'),
]
