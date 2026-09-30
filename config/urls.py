from django.contrib import admin
from django.urls import path
from portfolio import views
urlpatterns = [path('',views.home),path('api/pulses/',views.pulses),path('admin/',admin.site.urls)]
