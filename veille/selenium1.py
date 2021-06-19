from selenium import webdriver
import pandas as pd
from bs4 import BeautifulSoup
import requests
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.common.by import By
from selenium.webdriver.support import expected_conditions as EC
import time
from .models import Req,Veille,Article
from django.core.mail import send_mail
import os 

def cree_fich(name) :
    nombre_article=0
    Reqs=Req.objects.all()
    Req_imp=[]
    date = ''
    user=Veille.objects.get(Prenom=name)
    print(1)
    for r in Reqs :
        if r.Email==user :
            Req_imp.append(r.requette)
            print(r.requette)

    for requets in Req_imp :
        #driver = webdriver.Chrome("C:/Users/HP/Desktop/pfa/prjt1/veille/chromedriver.exe")
        chrome_options =webdriver.ChromeOptions()
        chrome_options.binary_location=os.environ.get("GOOGLE_CHROME_BIN")
        chrome_options.add_argument("--headless")
        chrome_options.add_argument("--disable-dev-shm-usage")
        chrome_options.add_argument("--no-sandbox")
        driver = webdriver.Chrome(executable_path=os.environ.get("CHROMEDRIVER_PATH"),chrome_options=chrome_options)
        driver.get("https://scholar.google.com/")
        search = driver.find_element_by_id('gs_hdr_tsi') #q
        search.send_keys(requets)
        search.send_keys(Keys.RETURN)
        url = driver.current_url
        headers = {'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_11_5)\
            AppleWebKit/537.36 (KHTML, like Gecko) Cafari/537.36'}
        link = []
        response = requests.get(url, headers=headers)
        soup = BeautifulSoup(response.text, features="html.parser")
        i = 0
        A=''
        for abc in soup.find_all(id='gs_bdy_sb_in'):
            for abc1 in abc.find_all('li', class_='gs_ind'):
                for abc2 in abc1.find_all('a'):
                    i += 1
                    if (i == 7):
                        A = 'https://scholar.google.com' + abc2['href']

        B = list(A)
        fois = 0
        for ch in range(len(B)):
            if (B[ch] == '1' and fois == 0):
                B[ch] = '2'
                fois = 1
        A = "".join(B)
        print(A)
        link.append(A)
        response = requests.get(link[0], headers=headers)
        print(1)
        soup = BeautifulSoup(response.text, features="html.parser")
        print(1)
        print(len(soup.select('div#gs_nml>a')))
        for i in range(len(soup.select('div#gs_nml>a'))):
            link.append('https://scholar.google.com' + soup.select('div#gs_nml>a')[i]['href'])
            print('https://scholar.google.com' + soup.select('div#gs_nml>a')[i]['href'])
        k = 0
        print(k)
        for lin in link:
            response = requests.get(lin, headers=headers)
            soup = BeautifulSoup(response.text, features="html.parser")
            for item in soup.find_all('div', class_='gs_r gs_or gs_scl'):
                print(0)
                nv_article = Article(Email = user)
                j = 0
                tour = 0
                for i in item.find_all('a'):

                    if (j == 0):
                        if ('[PDF]' in i.get_text()):
                            nv_article.lien_document=i['href']
                            j += 1
                        elif ('[HTML]' in i.get_text()):
                            j += 1
                        elif ('[DOC]' in i.get_text()):
                            nv_article.lien_document = i['href']
                            j += 1
                        else:
                            if ("https://" in i['href'] or "http://" in i['href']):
                                nv_article.lien_site = i['href']
                                nv_article.titre_article = i.get_text()
                                nv_article.lien_document = "le document n'existe pas ."
                                date_non_text = item.find('span', class_='gs_age')
                                if date_non_text is None:
                                    date= 'a b c 11'
                                else:
                                    date = date_non_text.get_text()
                                abstract=item.find('div', class_='gs_rs')
                                if abstract is None:
                                    nv_article.abstract= "l'abstract n'existe pas"
                                else:
                                    nv_article.abstract = abstract.get_text()
                                j += 2
                    elif (j == 1 and tour == 1):
                        if ('/scholar?output' in i['href']):
                            j += 1
                        else:
                            if ("https://" in i['href'] or "http://" in i['href']):
                                nv_article.lien_site = i['href']
                                nv_article.titre_article = i.get_text()
                                date_non_text = item.find('span', class_='gs_age')
                                if date_non_text is None:
                                    date = 'a b c 11'
                                else:
                                    date = date_non_text.get_text()
                                abstract = item.find('div', class_='gs_rs')
                                if abstract is None:
                                    nv_article.abstract = "l'abstract n'existe pas"
                                else:
                                    nv_article.abstract = abstract.get_text()
                                j += 2
                    tour += 1
                x=(int) (date.split()[3])
                print(x)

                if(x<5) :
                    nv=0
                    T_article=Article.objects.all()
                    T_article_email=[]
                    for art in T_article :
                        if(art.Email==user) :
                            T_article_email.append(art)
                    if(len(T_article_email)>0) :
                        for arts in T_article_email :
                            if(arts.titre_article==nv_article.titre_article) :
                                print(arts.titre_article)
                                nv=1
                    if(nv==0) :
                        nv_article.nouveau='nv'
                        nv_article.save()
                        nombre_article+=1
                        print(nv_article.titre_article)
    send_email(user.Prenom, user.Email, nombre_article)
    driver.close()



def send_email(username,email, x):
    if(x>0) :
        x=str(x)
        send_mail('Vamo Notifications',
              'Bonjour ' + username + ' Vous avez la quentite de ' + x + ' articles non vues veuillez acceder a votre compte.',
              'vamoveille@gmail.com', ['aminelyazrhi90@gmail.com'], fail_silently=False)

def all_users_articles() :
    users=Veille.objects.all()
    for user in users :
        cree_fich(user.Prenom)
