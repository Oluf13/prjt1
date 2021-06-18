from django.contrib.auth.views import LoginView
from django.urls import path

from prjt import settings
from .import views
from django.contrib.auth.views import LogoutView

urlpatterns=[
    path("",views.Accueil,name="Acceuil"),
    path("inscription/",views.Inscription,name="Inscription"),
    path('connexion/',views.loginPage,name="connexion"),
    path('compte/',views.Compte,name="Compte"),
    path('contact/',views.contact,name="contact"),
    path('article/',views.afich_article,name="article"),
    path('logout/', views.logout, name='logout')


]