"""GhostBusterNetwork URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/4.1/topics/http/urls/
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
from django.contrib import admin
from django.urls import path, include
from django.conf import settings
from django.conf.urls.static import static
from rest_framework import permissions
from drf_yasg.views import get_schema_view
from drf_yasg import openapi
from rest_framework import routers
from ghosts_and_equipments import views as GEViews
from missions import views as MViews


#swagger docs
schema_view = get_schema_view(
    openapi.Info(
        title="Ghost Buster Network API",
        default_version='v1',
        description="Backend database build on Django Rest API",
        terms_of_service="https://www.google.com/policies/terms/",
        contact=openapi.Contact(email="meetpatelmrp1005@gmail.com"),
        license=openapi.License(name="BSD License"),
    ),
    public=True,
    permission_classes=[permissions.AllowAny],
)


#ghost and equipments routers
GhostRouter = routers.DefaultRouter()
GhostRouter.register('', GEViews.GhostApi, basename='Ghosts')
EquipmentrRouter = routers.DefaultRouter()
EquipmentrRouter.register('', GEViews.EquipmentApi, basename='Equipments')

#missions router
MissionsRouter = routers.DefaultRouter()
MissionsRouter.register('', MViews.MissionsApi, basename='Missionss')


urlpatterns = [
    #swagger docs
    path('swagger/', schema_view.with_ui('swagger', cache_timeout=0), name='schema-swagger-ui'),
    path('redoc/', schema_view.with_ui('redoc', cache_timeout=0), name='schema-redoc'),

    #router urls
    path('ghost/', include(GhostRouter.urls), name='Ghosts'),
    path('equipment/', include(EquipmentrRouter.urls), name='Ghosts'),
    path('mission/', include(MissionsRouter.urls), name='Missions'),

    path('admin/', admin.site.urls),
    path('accounts/', include('accounts.urls')),
   
] + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
