"""getahead URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/3.1/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.conf import settings
from django.conf.urls.static import static
from django.contrib import admin
from django.contrib.auth import views as auth_views
from django.urls import path, include

from affiliation.views import acceuil, cabinet, presentation, programme

"""from affiliation.views import acceuil, cabinet, presentation, programme, WaraLoginView, formation_wara, version_wara, \
    create_version, version_module, version_module_detail, module_formation, vague_formation, \
    formation_wara_utilisateur, base, voir_modules, voir_modules_detail
"""
urlpatterns = [
    path('admin/', admin.site.urls),
    path('', acceuil, name="acceuil"),
    path('cabinet_jgk-ec/', cabinet, name="cabinet_jgk-ec"),
    path('presentation_get_ahead/', presentation, name="presentation_get_ahead"),
    path('programme_wara/', programme, name="programme_wara"),

    # url concernant la connexion pour le programme GET AHEAD
    path('login/', auth_views.LoginView.as_view(template_name='login.html'), name='login'),
    path('logout/', auth_views.LogoutView.as_view(template_name='logout.html'), name='logout'),

    # url concernant la connexion pour le programme GET AHEAD
    # path('wlogin/', WaraLoginView.as_view(), name='wlogin'),

    # path('base/', base, name='base'),
    # path(r'^(?P<id>\d+)/modules-concernant-la-formation/', voir_modules, name='voir_modules'),
    # path(r'^(?P<id>\d+)/details-modules-concernant-la-formation/', voir_modules_detail, name='voir_modules_detail'),
    # path('formation-wara/', formation_wara, name='formation-wara'),
    # path('formation-wara-utilisateur/', formation_wara_utilisateur, name='formation-wara-utilisateur'),

    # path(r'^(?P<id>\d+)/version-module-programme-wara/', version_module, name='version_module'),
    # path(r'^(?P<id>\d+)/details-module-programme-wara/', version_module_detail, name='version_module_detail'),

    # path('enregistrer-module-de-formation/', module_formation, name='module_formation'),
    # path('enregistrer-vague-de-formation/', vague_formation, name='vague_formation'),

    # path('versions-du-programme-wara/', version_wara, name='version-wara'),
    # path('create-wara-version/', create_version, name="create-version"),
    # path('login/', WaraLogoutView.as_view(template_name='wlogin.html'), name='wlogin'),

    path('affiliation/', include('affiliation.urls')),
]

if settings.DEBUG:
    urlpatterns += static(
        settings.MEDIA_URL,
        document_root=settings.MEDIA_ROOT
    )
