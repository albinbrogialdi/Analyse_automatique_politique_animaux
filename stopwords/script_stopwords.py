# -*- coding: utf-8 -*-
"""
Script de creation d'une liste de stop-words contenant les
numéros d'amendements, les numéros de loi dans les titres
et dans les descriptions.
"""

import re
with open ('data_website_tab.csv', 'r', encoding='utf-8') as f, open('stopwords_list.txt', 'w', encoding='utf-8') as g :  
    title = []
    descr = []
    for line in f :
        line = line.rstrip()
        column = line.split('\t')
        title.append(column[0])
        descr.append(column[1])
    
    #Exctraction des numeros de lois et amendements dans les titres
    regex_res = []
    for words in title : 
        # Match : tout élément qualifié par n° et prend en compte les énumérations sur colonne titre
        regex_nb1 = r".*n°(\s)?(\w+(-\w+)?(,\s\w+(-\w+)?)*(\set\s\w+(-\w+)?)?)"
        matchObj1 = re.match(regex_nb1, words, flags=0)
        if matchObj1 : 
            group_nb1 = matchObj1.group(2).replace(",", "").replace("et", "")
            regex_res.append(group_nb1)
        # Match : tous les amendements aux noms variés sur colonne titre 
        regex_nb2 = r".*[aA]mendements?\s([^Nn]\w+(-\w+)?(,\s[^Nn]\w+(-\w+)?)*(\set\s[^Nn]\w+(-\w+)?)?)"
        matchObj2 = re.match(regex_nb2, words, flags=0)
        if matchObj2 : 
            group_nb2 = matchObj2.group(1).replace(",", "").replace("et", "")
            if group_nb2[0].isupper() or group_nb2[0].isdigit(): 
                regex_res.append(group_nb2)

    # Exctraction des numeros de lois et amendements dans les descriptions 
    for words in descr :
        # Match : tout élément qualifié par n° + prend en compte les énumérations de type sur colonne description
        regex_nb3 = r".*n°(\s)?(\w+(-\w+)?(,\s]\w+(-\w+)?)*(\set\s\w+(-\w+)?)?)"
        matchObj3 = re.match(regex_nb3, words, flags=0)
        if matchObj3 : 
            group_nb3 = matchObj3.group(2).replace(",", "").replace("et", "")
            regex_res.append(group_nb3)
        # Match : tous les amendements aux noms variés sur colonne description
        regex_nb4 = r".*[aA]mendements?\s([^Nn]\w+(-\w+)?(,\s[^Nn]\w+(-\w+)?)*(\set\s[^Nn]\w+(-\w+)?)?)"
        matchObj4 = re.match(regex_nb4, words, flags=0)
        if matchObj4 : 
            group_nb4 = matchObj4.group(1).replace(",", "").replace("et", "")
            #Ajout des éléments non null à la liste des mots 
            if len(group_nb4) > 0 : 
                if group_nb4[0].isupper() or group_nb4[0].isdigit(): 
                    regex_res.append(group_nb4)

    #Création d'une nouvelle liste avec les éléments retenus 
    lst_stopwords = []
    for mot in regex_res :
        if " " in mot : 
            mot = mot.split()
            for m in mot : 
                # Ne garde que les éléments qui correspondent à des numéros de lois/amendements 
                # ou des noms d'amendements qui commencent par une majuscule
                if m[0].isupper() or m[0].isdigit() : 
                    lst_stopwords.append(m)
        elif mot[0].isupper() or mot[0].isdigit() : 
            lst_stopwords.append(mot)

    #Suppression des doublons et écriture dans le fichier avec ajout manuel de "n°" et "N°"
    lst_stopwords = list(set(lst_stopwords))
    lst_stopwords.append("N°")
    lst_stopwords.append("n°")
    lst_stopwords.sort()
    for mot in lst_stopwords : 
        g.write(mot+"\n")
        
    
