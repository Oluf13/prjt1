from django.contrib.admin import models
from django.contrib.auth.models import User
from django.forms import ModelForm, forms

from django.contrib.auth.forms import UserCreationForm
from.models import Veille

class CreateUserForm(UserCreationForm):
	class Meta:
		model = User
		fields = ['username','password1', 'password2']

class Utilform(ModelForm):
	class Meta:
		model=Veille
		fields=['Nom','Email','Confirmation_email']
		labels={'Nom':'Nom,Prenom'}
class logpage(ModelForm):
	class Meta:
		model=Veille
		fields=['Nom','Mot_de_passe']
		labels={'Nom':'Username'}