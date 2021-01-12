from django.conf.urls import url

from affiliation import views

urlpatterns = [
    # url concernant le tableau de bord
    url(r'^tableaudebord$', views.tableaudebord, name="tableaudebord"),
    url(r'^list_total_pers_pymt', views.list_total_pers_pymt, name="list_total_pers_pymt"),
    url(r'^compte$', views.compte, name="compte"),
    url(r'^mongroupe$', views.mongroupe, name="mongroupe"),
    url(r'^voirmongroupe$', views.voirmongroupe, name="voirmongroupe"),
    url(r'^(?P<id>\d+)/validerpayement$', views.validerpayement, name="validerpayement"),
    url(r'^(?P<id>\d+)/voir_membre_palier_id$', views.voir_membre_palier_id, name="voir_membre_palier_id"),

    # url concernant les postes
    url(r'^poste$', views.poste, name="poste"),
    url(r'^createposte$', views.createposte, name="createposte"),
    url(r'^(?P<id>\d+)/deleteposte$', views.deleteposte, name="deleteposte"),
    url(r'^(?P<id>\d+)/updateposte$', views.updateposte, name="updateposte"),

    # url concernant l'ajout d'un adhérent
    url(r'^ajouter$', views.ajouter, name="ajouter"),
    url(r'^liste$', views.liste, name="liste"),
    url(r'^(?P<id>\d+)/listeupdateuser', views.listeupdateuser, name="listeupdateuser"),
    url(r'^(?P<id>\d+)/listesuppruser', views.listesuppruser, name="listesuppruser"),

    url(r'^(?P<id>\d+)/password/$', views.change_password, name='change_password'),

    url(r'^(?P<id>\d+)/voirplus', views.voirplus, name="voirplus"),
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

    # url concernant le niveau 1 > Bamileke
    url(r'^bamileke$', views.bamileke, name="bamileke"),

    # url concernant le niveau 1 > Bamileke
    url(r'^zoulou', views.zoulou, name="zoulou"),

    # url concernant le niveau 1 > Bamileke
    url(r'^maya', views.maya, name="maya"),

    # url concernant le niveau 1 > Bamileke
    url(r'^mandingue', views.mandingue, name="mandingue"),

    #
    url(r'^payement$', views.payement, name="payement"),
    url(r'^createpayement$', views.createpayement, name="createpayement"),
    url(r'^createpayementzou$', views.createpayementzou, name="createpayementzou"),
    url(r'^createpayementmaya$', views.createpayementmaya, name="createpayementmaya"),
    url(r'^(?P<id>\d+)/updatepayement$', views.updatepayement, name="updatepayement"),
    url(r'^(?P<id>\d+)/deletepayement$', views.deletepayement, name="deletepayement"),

    # url concernant le niveau 1 > Bamileke > Groupe<id>
    url(r'^(?P<id>\d+)/pyramide$', views.pyramide, name="pyramide"),

    # url concernant le programme WARA
    url(r'^wara$', views.wara, name="wara"),
]
