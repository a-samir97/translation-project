
from django.urls import path
from . import views

urlpatterns = [
    path('',views.home,name='home'),
    path('translate', views.translation,name='translate-text'),
]
