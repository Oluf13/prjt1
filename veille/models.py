from django.db import models
from django.utils import timezone
from django.utils.translation import gettext_lazy as _

from django.contrib.auth.models import User


class Veille(models.Model):
    Nom = models.CharField(max_length=55)
    Prenom = models.CharField(max_length=55,unique=True)
    Date_de_naissance = models.DateField(auto_now=False, auto_now_add=True, blank=True)
    Email = models.CharField(max_length=55)
    Confirmation_email = models.EmailField(max_length=55, unique=True, primary_key=True)
    Mot_de_passe = models.CharField(max_length=55)
def __str__(self):
        return self.Nom

class Article(models.Model):
    Email=models.ForeignKey('Veille',null=False,on_delete=models.CASCADE,default=None)
    titre_article=models.CharField(max_length=150)
    lien_site=models.CharField(max_length=150)
    lien_document=models.CharField(max_length=150)
    abstract = models.CharField(max_length=1000,default="N'est pas disponible")
    date_article=models.DateField(auto_now=True)
    nouveau=models.CharField(max_length=10,default=0)

    def __str__(self):
        return self.titre_article


class information(models.Model) :
    Email = models.ForeignKey('Veille', null=False, on_delete=models.CASCADE, default=None)
    Nom_auteur = models.CharField(max_length=55)
    Domaine = models.CharField(max_length=55)
    Mot_cle1 = models.CharField(max_length=25)
    Mot_cle2 = models.CharField(max_length=25)
    Mot_cle3 = models.CharField(max_length=25)
    date_req = models.DateField(auto_now=True)

class Req(models.Model) :
    Email = models.ForeignKey('Veille', null=False, on_delete=models.CASCADE, default=None)
    requette = models.CharField(max_length=155)
    date_req = models.DateField(auto_now=True)
