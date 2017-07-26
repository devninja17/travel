from django.conf.urls import url
from . import views

urlpatterns = [
    url('^$', views.index),
    url('^travelbuddy$', views.index),
    url('^main$', views.index),
    url('^travels$', views.travels),
    url('^travels/add$', views.addplan),
    url(r'^login$', views.login),
    url(r'^logout$', views.logout),
    url('^travels/destination/(?P<trip_id>\d+)$', views.destination),
    url('^travels/join/(?P<trip_id>\d+)$', views.join_trip),
]