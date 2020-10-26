from django.conf.urls import url

from affiliation import views

urlpatterns = [
    url(r'^tableaudebord$', views.tableaudebord, name="tableaudebord"),
    url(r'^poste$', views.poste, name="poste"),
    url(r'^createposte$', views.createposte, name="createposte"),
    url(r'^(?P<id>\d+)/deleteposte$', views.deleteposte, name="deleteposte"),
    url(r'^(?P<id>\d+)/updateposte$', views.updateposte, name="updateposte"),
    url(r'^ajouter$', views.ajouter, name="ajouter"),
    url(r'^liste$', views.liste, name="liste"),
    url(r'^parcours$', views.parcours, name="parcours"),
    url(r'^codepays$', views.codepays, name="codepays"),
    url(r'^createcodepays$', views.createcodepays, name="createcodepays"),
    url(r'^(?P<id>\d+)/deletecodepays$', views.deletecodepays, name="deletecodepays"),
    url(r'^(?P<id>\d+)/updatecodepays$', views.updatecodepays, name="updatecodepays"),
]