"""
Script de Webscraping
Auteur : Albin Brogialdi
​
Permet d'obtenir depuis le site politique animaux le texte de chacun des articles
avec le titre, le corps du texte, le theme ainsi que la prise de position.
"""

import bs4
from pip._vendor import requests

site = "https://www.politique-animaux.fr/?page="

# Génère les URLs de chaque page du site en indiquant le nombre de pages souhaité
def get_pages(site, nb_pages):
    liste_pages = ["https://www.politique-animaux.fr/"]
    for i in range (1 , nb_pages):
        current_page_link = site + str(i)
        liste_pages.append(current_page_link)
    return liste_pages


# Permet de récupérer les URLs de chaque article pour chaque page
pages = get_pages(site, 1126) # 1126 pages  # liste des URLs de toutes les pages du site
link_list = []
print("Start - Récupération URLs Articles")
for page in pages:
    response = requests.get(page) # code HTML de la page site
    soup = bs4.BeautifulSoup(response.text, 'html.parser')
    HTML_link_list = soup.find_all("div", {"class":"links"})
    for i in HTML_link_list:
        a_tag = i.a
        link = a_tag['href']
        link_tosave = site[:-7]+link
        link_list.append(link_tosave)
print("End - Récupération URLs Articles")
        
# Boucle sur tous les URLs d'articles afin d'obtenir les données des pages
resume_site = [] # liste de liste avec tous les resume_article
counter = 0
erreursNb = 0
print("Start - Récupération Données pour chaque Article")
for article in link_list :
    counter += 1
    resume_article = [] # liste avec titre, body, position, liste de theme(s)
     
    # Récupère le code HTML de l'article courant
    response_article = requests.get(article)
    soup_article = bs4.BeautifulSoup(response_article.text, 'html.parser')
    
    # Récupère le titre de l'article
    link_article_title = soup_article.find("h1", {"class":"title"})
    if not link_article_title:
        print("Titre pas lu - Retry")
        #print(response_article.text)
        response_article = requests.get(article)
        soup_article = bs4.BeautifulSoup(response_article.text, 'html.parser')
        link_article_title = soup_article.find("h1", {"class":"title"})

    if link_article_title :

        title_article = link_article_title.text
        resume_article.append(title_article)


        # Récupère le corps du texte de l'article
        link_article_body = soup_article.find("div", {"class":"body"})
        body_article = link_article_body.text
        body_article = body_article.replace("\n"," ")
        resume_article.append(body_article)

        # Récupère la note d'évaluation qui permet de définir la position et de gérer les cas a/ont
        link_position_article = soup_article.find("div", {"class":"evaluation"})
        position_lettre = str(link_position_article)[28:29]
        position_complete = ""
        if position_lettre == "a":
            position_complete = "Agit pour les animaux"
        elif position_lettre == "b":
            position_complete = "Penche pour les animaux"
        elif position_lettre == "c":
            position_complete = "Penche contre les animaux"
        elif position_lettre == "d":
            position_complete = "Agit contre les animaux"
        resume_article.append(position_complete)



        # Récupère les thèmes de l'article s'il y en a plusieurs puis stocke dans une liste
        link_theme_article = soup_article.find_all("p", {"class":"theme"})
        liste_theme = []
        for theme in link_theme_article:
            a_tag_article = theme.a
            theme_article = a_tag_article['href']
            theme_article_final = theme_article[1:]
            liste_theme.append(theme_article_final)
        resume_article.append(liste_theme)
        resume_site.append(resume_article)

        #print("Page : "+ str(int(1+counter/6)))
        #print(title_article)
#    print(liste_theme)
#    print()

    else:
        print("Titre non lu - Failed")
        erreursNb += 1
        print("Page : "+ str(int(1+counter/6)))

print("End - Récupération Données pour chaque Article")
print("Nb pbm : ")
print(erreursNb)

# Ecrit sur une ligne dans un fichier csv le contenu d'un article
# Si l'article a plusieurs thèmes, écrit une ligne par thème avec titre, corps, orientation, thème
# La condition else permet d'ignorer les articles n'ayant pas de thèmes pour éviter les erreurs
print("Start - Ecriture dans le csv")
with open('data_website.csv', 'w', encoding='utf8') as f1:
    for resume in resume_site :
        nb_theme = len(resume[3])
        if nb_theme > 1 :
            for i in range (nb_theme):
                f1.write('!DELIM!'.join(resume[:3])+'!DELIM!'+resume[3][i-1]+'\n')
        elif nb_theme == 1 :
            f1.write('!DELIM!'.join(resume[:3])+'!DELIM!'+resume[3][0]+'\n')
        else :
            pass
print("End - Ecriture dans le csv")
