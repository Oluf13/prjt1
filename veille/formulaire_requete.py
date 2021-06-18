from django.forms import ModelForm
from .models import information
class req(ModelForm):
    class Meta :
        model = information
        fields =['Nom_auteur' , 'Domaine' , 'Mot_cle1','Mot_cle2','Mot_cle3' ]