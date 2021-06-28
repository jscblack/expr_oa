"""expr URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/3.2/topics/http/urls/
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
from django.urls import path
from django.urls import include, path
from django.conf.urls import url
from rest_framework import routers
from oa.views import *
from drf_yasg2.views import get_schema_view
from drf_yasg2 import openapi

schema_view = get_schema_view(
   openapi.Info(
      title="OA API",
      default_version='v1',
      description="OA description",
      #terms_of_service="https://www.google.com/policies/terms/",
      #contact=openapi.Contact(email="contact@snippets.local"),
      #license=openapi.License(name="BSD License"),
   ),
   public=True,
   permission_classes=[permissions.AllowAny],
)
router = routers.DefaultRouter()

#router.register(r"users", CustomUserAllViewSet)

urlpatterns = [
    path('', include(router.urls)),
    path('api-auth/', include('rest_framework.urls', namespace='rest_framework')),
    path("listUsers/", CustomUserAll.as_view()),
    path("filterUsers/", CustomUserFilter.as_view()),
    path("addUser/", CustomUserAdd.as_view()),
    path("userDetail/<int:pk>/", CustomUserDetail.as_view()),
    path("createProcess/",CreateProcess.as_view()),
    path("listProcesses/",ListProcess.as_view()),
    path("processDetail/<int:pk>/",ProcessDetail.as_view()),
    path("listUnhandledProcess/",ListUnhandledProcess.as_view()),
    path("handleProcess/<int:ProcessOriginalEvent>/",HandleProcess.as_view()),
    path("modifyProcessRaiseEvent/<int:pk>/",modifyProcessRaiseEvent.as_view()),
    url(r'^swagger(?P<format>\.json|\.yaml)$', schema_view.without_ui(cache_timeout=0), name='schema-json'),
    # url(r'^swagger/$', schema_view.with_ui('swagger', cache_timeout=0), name='schema-swagger-ui'),
    url(r'^redoc/$', schema_view.with_ui('redoc', cache_timeout=0), name='schema-redoc'),

]
