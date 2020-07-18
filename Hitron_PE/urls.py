"""Hitron_PE URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/3.0/topics/http/urls/
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
from django.conf.urls.static import static
from django.conf import settings
from PE.views import (input_data, Submit_master, Submit_form, Trace_Data, Query, GetCode, TrackingCode, code_render, Update_Confirm, DetailForm, NoneImageUpdate)

urlpatterns = [
    path('admin/', admin.site.urls),
    path('', Submit_form),
    path('PE/Submit_master', Submit_master, name="Submit_master"),
    path('submit_form', Submit_form, name="Submit_form"),
    path('trace', Trace_Data, name="Trace"),
    path('query', Query, name="Query"),
    path('getCode', GetCode, name="getCode"),
    path('TrackingCode', TrackingCode, name="TrackingCode"),
    path('coderender', code_render, name='coderender'),
    path('updateconfirm/<code>', Update_Confirm, name='Update_Confirm'),
    path('noneimageupdate/<code>', NoneImageUpdate, name='NoneImageUpdate'),
    path('detail/<code>', DetailForm, name='Detail')
]

if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL,
                          document_root=settings.MEDIA_ROOT)
