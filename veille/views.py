from pyexpat.errors import messages

from django.contrib import auth
from django.contrib.auth import authenticate, login, logout
from pyexpat.errors import messages

from django.core.exceptions import ObjectDoesNotExist

from django.contrib.auth import authenticate, login, logout
from django.shortcuts import redirect
from django.shortcuts import render
from requests import Response

from .fromulaire import CreateUserForm, Utilform, logpage
from .formulaire_requete import req
from .models import information, Veille, Req, Article
from .selenium1 import cree_fich
from django.contrib import messages

name_of_user = ''
user_1 = ''
deja_article=0


def Accueil(request):
    return render(request, "main/home.html", {})


def contact(request):
    if request.method=="POST":
        form=Utilform(request.POST)
        #print(form.Nom)
        if form.is_valid():
             form1=Veille(Nom= form.cleaned_data['Nom'],Prenom=user_1,Confirmation_email= form.cleaned_data['Confirmation_email'],Email = form.cleaned_data['Email'])
             v=Veille.objects.all()
             var=0  #false
             for varr in v :
                if varr.Prenom==form1.Prenom :
                    var=1
             if var==0 :
                form1.save()
                return redirect('Acceuil')
             else:
                    messages.success(request,"les donnees sont incorrectes .")
                    form = Utilform()
                    render(request, "Contact.html", {'form': form})
        else:
             messages.success(request,"les donnees sont incorrectes .")
             form = Utilform()
             render(request, "Contact.html", {'form': form})
    else:
        form=Utilform()
    return render(request,'Contact.html',{'form':form})

def Inscription(request):
    if request.method == "POST":
        #global user_1
        form = CreateUserForm(request.POST)
        if form.is_valid():
            form.save()
            global user_1
            user_1 = form.cleaned_data['username']
            print(user_1)
            return redirect('contact')
        else:
            form = CreateUserForm()
            messages.success(request,"les donnees sont incorrectes .")
            render(request, "main/inscription.html", {'form': form})
    else:
        form = CreateUserForm()
    return render(request, "main/inscription.html", {'form': form})


def Contact(request):
    return render(request, "Contact.html", {})


def Compte(request):
    if request.method == "POST":
        print(name_of_user)
        veille = Veille.objects.get(Prenom=request.user.username)
        form = req(request.POST).save(commit=False)
        form1 = information(Email=veille, Nom_auteur=form.Nom_auteur, Domaine=form.Domaine, Mot_cle1=form.Mot_cle1,
                            Mot_cle2=form.Mot_cle2, Mot_cle3=form.Mot_cle3)
        form1.save()
        msg = cree(form1.id)
        messages.success(request,msg)
        form = req()  # tajriba
        return render(request, "main/compte.html", {'form': form})
    else:
        form = req()
    return render(request, "main/compte.html", {'form': form})


def loginPage(request):
    if request.method == 'POST':
        global name_of_user
        form = logpage(request.POST).save(commit=False)
        
        # name_of_user==request.user.username
        print(name_of_user)
        user = auth.authenticate(request, username=form.Nom, password=form.Mot_de_passe)
        #print(user.username)
        if user is not None:
            login(request, user)
            #cree_fich(name_of_user)
            print(1)
            return redirect('Compte')
        else:
            messages.success(request,"Username ou le mot de passe est incorrecte .")
            form = logpage()
            return render(request, "main/connexion.html", {'form': form})
    else:
        form = logpage()
    return render(request, "main/connexion.html", {'form': form})



def logout(request):
        veille = Veille.objects.get(Prenom=request.user.username)
        deja_vu(veille.Email)
        print(2)
        auth.logout(request)
        return redirect('/')


def cree(id):
    info = information.objects.get(id=id)
    veille = Veille.objects.get(Prenom=request.user.username)
    req = ''
    author = info.Nom_auteur
    if (author != 'None'):
        req = 'AUTHOR :' + author

    field = info.Domaine
    if (field != 'None'):
        if req!='' :
            req = field + ' and ' + req
        else :
            req =field

    key = ''
    k = info.Mot_cle1
    if k != 'None':
        k = sans_mot_vide(k)
        if req!='' :
            key = k + ' and '
        else :
            key =k
    k = info.Mot_cle2
    if k != 'None':
        k = sans_mot_vide(k)
        if key!='' :
            key = k + ' and ' + key
        else :
            key = k
            if req!='' :key+=' and '
    k = info.Mot_cle3
    if k != 'None':
        k = sans_mot_vide(k)
        if key != '':
            key = k + ' and ' + key
        else:
            key = k
            if req != '': key += ' and '
    a = key + req
    if a != '':
        form = Req(Email=veille, requette=a)
        form.save()
        print(form.requette)
        return 'La requette est bien enregistrée'
    else:
        return 'Vous douvez remplir au moins un champs du formulaire'


def afich_article(request):
    veille = Veille.objects.get(Prenom=request.user.username)
    article = Article.objects.filter(Email=veille).order_by('-date_article')

    msg = ''
    form = []
    lg=len(article)
    if  lg> 0:
        msg = 'Vous avez ' + str(len(article)) + ' :'
        for  art in   article:
            if art.lien_document==" n'existe pas " or art.lien_document=="le document n'existe pas .":
                info="le document n'existe pas ."
                form.append((info,art))
            else :
                print(art.lien_document)
                info = "click"
                form.append((info, art))
    else:
        msg = 'Vous avez aucun article !'

    messages.success(request,msg)
    return render(request, 'main/article.html', {'form':form, 'msg': msg})


def deja_vu(email):
    veille = Veille.objects.get(Email=email)
    print(veille.Email)
    article = Article.objects.all()
    print(2)
    for art in article:
        if art.Email == veille:
            print(art.nouveau)
            art.nouveau = 'deja_vu'
            print(art.nouveau)
            print(1)
            art.save()



def sans_mot_vide(mot_cle):
    T = ["le", "la", "l'", "La", "Le", "L'", "les", "Les", "LE", "LA", "LES"]
    mot_tab = mot_cle.split()
    if len(mot_tab) > 1:
        if mot_tab[0] in T:
            mot_tab = mot_tab[1:]
        else:
            mot_tab[0] = mot_tab[0].replace("l'", "")
            mot_tab[0] = mot_tab[0].replace("L'", "")
        if len(mot_tab) > 1:
            a = mot_tab[0]
            for i in mot_tab[1:]:
                a = a + ' ' + i
            mot_cle = "".join(('"', a, '"'))
        else:
            mot_cle = mot_tab[0]

    else:
        mot_cle = mot_cle.replace("l'", "")
        mot_cle = mot_cle.replace("L'", "")
    return mot_cle


def all_users_articles(request):
    users = Veille.objects.all()
    for user in users:
        print(user.Prenom)
    for user in users:
        cree_fich(user.Prenom)
        print(user.Prenom)
    return render(request, 'main/arts.html')
