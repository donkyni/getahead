from django.conf.urls import url

from affiliation import views

urlpatterns = [
    # url concernant le tableau de bord
    url(r'^tableaudebord$', views.tableaudebord, name="tableaudebord"),

    # url concernant les postes
    url(r'^poste$', views.poste, name="poste"),
    url(r'^createposte$', views.createposte, name="createposte"),
    url(r'^(?P<id>\d+)/deleteposte$', views.deleteposte, name="deleteposte"),
    url(r'^(?P<id>\d+)/updateposte$', views.updateposte, name="updateposte"),

    # url concernant l'ajout d'un adhérent
    url(r'^ajouter$', views.ajouter, name="ajouter"),
    url(r'^liste$', views.liste, name="liste"),
    url(r'^parcours$', views.parcours, name="parcours"),

    # url concernant les code des pays
    url(r'^codepays$', views.codepays, name="codepays"),
    url(r'^createcodepays$', views.createcodepays, name="createcodepays"),
    url(r'^(?P<id>\d+)/deletecodepays$', views.deletecodepays, name="deletecodepays"),
    url(r'^(?P<id>\d+)/updatecodepays$', views.updatecodepays, name="updatecodepays"),

    # url concernant les niveaux
    url(r'^niveau', views.niveau, name="niveau"),
    url(r'^createniveau$', views.createniveau, name="createniveau"),
    url(r'^(?P<id>\d+)/deleteniveau$', views.deleteniveau, name="deleteniveau"),
    url(r'^(?P<id>\d+)/updateniveau$', views.updateniveau, name="updateniveau"),

    # url concernant les paliers
    url(r'^palier', views.palier, name="palier"),
    url(r'^createpalier$', views.createpalier, name="createpalier"),
    url(r'^(?P<id>\d+)/deletepalier$', views.deletepalier, name="deletepalier"),
    url(r'^(?P<id>\d+)/updatepalier$', views.updatepalier, name="updatepalier"),

    # url concernant les groupes
    url(r'^groupe', views.groupe, name="groupe"),
    url(r'^creatgrouper$', views.creategroupe, name="creategroupe"),
    url(r'^(?P<id>\d+)/deletegroupe$', views.deletegroupe, name="deletegroupe"),
    url(r'^(?P<id>\d+)/updategroupe$', views.updategroupe, name="updategroupe"),

    # url concernant les parents
    url(r'^parent', views.parent, name="parent"),
    url(r'^creatgparent$', views.createparent, name="createparent"),
    url(r'^(?P<id>\d+)/deleteparent$', views.deleteparent, name="deleteparent"),
    url(r'^(?P<id>\d+)/updateparent$', views.updateparent, name="updateparent"),

    # url concernant le niveau 1 > Bamileke
    url(r'^bamileke$', views.bamileke, name="bamileke"),

    # url concernant le niveau 1 > Bamileke > Groupe<id>
    url(r'^(?P<id>\d+)/pyramide$', views.pyramide, name="pyramide"),
]
