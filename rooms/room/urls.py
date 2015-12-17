from django.conf.urls import include, url
from django.contrib import admin

urlpatterns = [
    url(r'^$', 'room.views.login'),
    url(r'^login/$', 'room.views.login'),
    url(r'^insertPerson/$', 'room.views.insertPerson'),
    url(r'^success/$', 'room.views.success'),
    url(r'^getRooms/$', 'room.views.getRooms'),
    url(r'^login/retry/$', 'room.views.retrylogin'),
    url(r'^logout/$', 'room.views.logout'),
    url(r'^profile/(?P<rollno>\w+)/$', 'room.views.profile'),
    url(r'^getMatches/$', 'room.views.getMatches'),
    url(r'^about/$', 'room.views.about'),
]
