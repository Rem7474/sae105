"""
Programme SAE 105: Traitement de données:
Fichier: ville_france.csv contenant des informations sur les 36700 Villes de France
BUT1 : Année 2022-2023
@author: CUVELIER Rémy B1
"""
# pour afficher la carte avec les villes

import folium,branca
import matplotlib.pyplot as plt
import math
#pour le test de fichier
import os

#-----------------------------------------------------------
# Fonction qui extrait les 12 informations sur chaque ville
#-----------------------------------------------------------

def lire_fichier_csv(nomFich):
    """
    Cette fonction permet de LIRE les données du fichier villes_france.csv
    le fait d'utiliser readlines permet de récupérer une liste dont chaque élément correspond à une ville
    ainsi que toutes les données associées
    :param nomFich: fichier "villes_france.csv"
    :return: une liste "liste_villes" dont chaque élément est une str qui comporte toutes les données d'une ville
    (27 données par ville au total)
    """
    fich = open(nomFich,'r')
    liste_villes = fich.readlines()

    print("Fin de l'Extraction des infos du fichier",nomFich)
    fich.close()
    return liste_villes

def extract_info_villes(uneListe):
    """
    Fonction qui extrait les 12 informations de la liste[str] extraite du fichier Excel
    :param : uneListe:
    :return: L: une liste dont chaque élément contient les 12 infos de la ville
    la taille de la liste L[] retournée est de 36700 villes
    """
    L= []
    temp = []
    for i in uneListe:
        temp.append(i.split(','))
    print("taille = ",len(temp))

    """
    Il faut faire attention aux Départements de Corse : 2A et 2B
    et également aux département d'Outre-Mer : 971, 972, ...,977
    """
    for i in temp:
        # eval(..) transforme "Annecy" en Annecy, et "18.59" en 18.59 donc une chaîne de caractères sans les "..."
        # ensuite il faut transformer le type str() en int() ou float()
        # Pour tous les départements sauf la Corse 2A et 2B
        # et les territoires d'Outre-Mer : les derniers champs sont à 'NULL'
        if ((eval(i[1]) != '2A') and (eval(i[1]) != '2B')) and i[25] != 'NULL':
            L.append([int(eval(i[1])),      # numéro du Département
                    eval(i[3]),             # Nom de la ville en MAJUSCULE
                    eval(i[8]),             # Code postal
                    int(eval(i[14])),       # population en 2010
                    int(eval(i[15])),       # population en 1999
                    int(eval(i[16])),       # population en 2012
                    float(eval(i[17])),     # densité
                    float(eval(i[18])),     # surface
                    float(eval(i[19])),     # longitude
                    float(eval(i[20])),     # latitude
                    int(eval(i[25])),       # altitude min
                    int(eval(i[26]))])      # altitude max
        elif i[13] == 'NULL': # pour gérer les départements et territoires d'Outre-Mer : 971, 972, 974, ...
            L.append([int(eval(i[1])),
                      eval(i[3]),
                      eval(i[8]),
                      int(eval(i[14])),
                      int(eval(i[15])),
                      int(eval(i[16])),
                      float(eval(i[17])),
                      float(eval(i[18])),
                      float(eval(i[19])),
                      float(eval(i[20])),
                      "NULL",
                      "NULL"])
        else:
            L.append([eval(i[1]),
                      eval(i[3]),
                      eval(i[8]),
                      int(eval(i[14])),
                      int(eval(i[15])),
                      int(eval(i[16])),
                      float(eval(i[17])),
                      float(eval(i[18])),
                      float(eval(i[19])),
                      float(eval(i[20])),
                      i[25],
                      i[26]])


    return L

#====================================================================
# Compte le Nombre de villes en fonction de l'indicatif téléphonique
#====================================================================
def appelNombre_Villes_Indicatif(indTel, unelisteInfo):
    """
    Procédure qui compte le nombre de villes en fonction de l'indicatif téléphonique
    :param indTel: indicatif téléphonique en int
    :param unelisteInfo: liste des villes
    """
    #définition de la variable "listeDept" en fonction de l'indicatif téléphonique
    if indTel == 1: 
        #liste des département avec l'indicatif 01
        listeDept = [75, 77, 78, 91, 92, 93, 94, 95] 
    elif indTel == 2:
        #liste des département avec l'indicatif 02
        listeDept = [14,18,22,27,28,29,35,36,37,41,45,49,50,53,56,72,85,974,976] 
    elif indTel == 3:
        #liste des département avec l'indicatif 03
        listeDept = [2,8,10,21,25,39,51,52,54,55,57,58,59,60,62,67,68,70,71,80,88,89,90]
    elif indTel == 4:
        #liste des département avec l'indicatif 04
        listeDept=[1,3,4,5,6,7,11,13,15,"2A","2B",26,30,34,38,42,43,48,63,66,69,73,74,83,84]
    elif indTel == 5:
        #liste des département avec l'indicatif 05
        listeDept = [9,12,16,17,19,23,24,31,32,33,40,46,47,64,65,79,81,82,86,87,971,972,973,975,977,978]
    else:
        #affiche qu'il y a une erreur si l'indicatif téléphonique n'existe pas
        print("Erreur de saisie")
    #appelle la fonction qui compte le nombre de ville en fonction de l'indicatif téléphonique
    nbVilles = extract_villes_depart_indicatif(listeDept, unelisteInfo)
    #affiche le nombre de ville en fonction de l'indicatif téléphonique
    print(f"nombre de villes dans les départements ayant l'indicatif {indTel} = {nbVilles} villes")
#--------------------------------------------------------
# Fonction extract_villes_depart_indicatif(listeInfo)
#--------------------------------------------------------
def extract_villes_depart_indicatif(listeDept, listeInfo):
    """
    Fonction qui extrait l'ensemble des villes pour chaque département,
    en fonction de l'indicatif téléphonique (01 = Île-de-France, 02 = Nord-Ouest, ...

    :param listeDept: qui est la liste des départements ayant cet indicatif
    :param listeInfo: liste des noms de villes
    :return: nbVilles = nombre de villes
    """
    #initialisation de la variable contenant la liste des département de la zone 05
    dep05=[9,12,16,17,19,23,24,31,32,33,40,46,47,64,65,79,81,82,86,87,971,972,973,975,977,978]
    #initialisation de la variable nbVilles à 0
    nbVilles = 0
    #initialise la string "ligne" à vide
    ligne = ""
    #compte le nombre de ville en fonction de l'indicatif téléphonique qui nous ai donné
    indice_ville=1
    #boucle qui parcours la liste "listeInfo" 
    for i in listeInfo:
        #test si le département de la ville est dans la liste des départements
        if i[0] in listeDept:
            #incrémentation de la variable nbVilles
            nbVilles += 1
        #test si le département de la ville est dans la liste des départements de la zone 05
        if i[0] in dep05:
            #ajout dans la string des villes à écrire dans le fichier
            ligne+=str(indice_ville)+" "+str(i[1])+" "+"("+str(i[0])+")"+"\n"
            indice_ville+=1
    #écriture dans le fichier des villes de la zone 05
    with open("SO05.txt", "w", encoding="utf-8") as fichier:
	    fichier.write(ligne)
    #retourne le nombre de ville en fonction de l'indicatif téléphonique
    return nbVilles


#--------------------------------------------------------
# Procédure qui permet d'appeler la fonction
# qui extrait les informations sur les villes
#---------------------------------------------------------
def appelExtractionVilles():
    print("Extraction des informations des Villes de France")
    listeVillesFr = lire_fichier_csv("villes_france.csv")
    print("une ligne = ",listeVillesFr[0])

    # la liste info contient les 12 Informations retenues pour la suite du programme
    info = extract_info_villes(listeVillesFr)

    return info

#==========================================================
# Recherche les infos d'une Ville dans la liste
#==========================================================
def rechercheVille(name,listeVilles):
    """

    :param name: nom de la ville recherchée doit être en MAJUSCULE
    :param listeVilles: liste de toutes les villes
    :return: listeVilles[i] : la ville recherchée
    """
    #boucle qui parcours la liste "listeVilles"
    for i in range(len(listeVilles)):
        #test si la ville recherchée est dans la liste
        if listeVilles[i][1] == name:
            #retourne la ville recherchée
            return listeVilles[i]
    #retourne "ville non trouvée" si la ville n'est pas dans la liste
    print("ville non trouvée")

# --------------------------------------------------------
# Fonction extract_villes_depart_indicatif(listeInfo)
# --------------------------------------------------------
def extract_villes_NumDepart(numDept,listeInfo):
    """
    Fonction qui extrait l'ensemble des villes pour chaque département,
    en fonction du numéro du Département

    :param numDept: numéro du département
    :param listeInfo: liste des noms de villes
    :return: nbVilles = nombre de villes du département
    """
    # initialisation de la variable nbVilles à 0
    nbVilles = 0
    #création de la liste des villes du département
    listeVilles = []
    # boucle qui parcours la liste "listeInfo"
    for i in listeInfo:
        # test si la ville appartient au département
        if i[0] == numDept:
            # incrémentation de la variable nbVilles si la ville appartient au département
            nbVilles += 1
            # ajout de la ville dans la liste des villes du département
            listeVilles.append(i)
    # écriture dans le fichier
    with open(f"villes_{numDept}.txt", "w", encoding="utf-8") as fichier:
        #écriture d'une ville par ligne dans le fichier ville_numDept.txt
        for i in listeVilles:
            fichier.write(str(i) + "\n")
    # retourne le nombre de ville en fonction du numéro du département, ainsi que la liste des villes du département
    return nbVilles, listeVilles

# ================================================
# Fonctions Utiles pour le Tri Bulle lié à la POPULATION
# ================================================


def MinMax5_villes_Habitants(numDept,lstVillesDepart):
    """
    :param numDept:
    :param lstVillesDepart:
        recherche de 5 villes ayant le MOINS d'habitants dans un tableau
        recherche de 5 villes ayant le PLUS d'habitants dans un tableau
        on peut trier la liste par ordre croissant
        *** On IMPOSE le TRI BULLE vu au TP7 ****
        puis extraire les 5 premières valeurs
    """
    def unPassage(tab, dernier):
        mouvement=0
        for i in range(0,dernier-1):
            if tab[i][3]>tab[i+1][3]:
                temp1=tab[i] 
                temp2=tab[i+1]
                tab[i]=temp2
                tab[i+1]=temp1
                mouvement+=1
        return tab,mouvement
    def triBulle(liste):
        dernier=len(liste)
        move=1
        while dernier!=0 and move>0:
            liste=unPassage(liste, dernier)[0]
            move=unPassage(liste, dernier)[1]
            dernier-=1
        return liste
    #appelle de la fonction qui trie les villes du département en fonction de la population de 2010
    villes=triBulle(lstVillesDepart)
    #affiche les 5 première valeur de la liste "villes"
    print("5 villes ayant le moins d'habitants :")
    # écriture dans le fichier
    with open(f"Min5Villes_{numDept}.txt", "w", encoding="utf-8") as fichier:
        for i in range(0,5):
            fichier.write(str(villes[i]) + "\n")
            print(villes[i])
    print("5 villes ayant le plus d'habitants :")
    with open(f"Top5Villes_{numDept}.txt", "w", encoding="utf-8") as fichier:
        for i in range(len(villes)-1,len(villes)-6,-1):
            fichier.write(str(villes[i]) + "\n")
            print(villes[i])

#-------------------------------------------------------------------------
# Procédure qui permet d'afficher sur une carte OpenStreetMap
# les 10 villes (5 ayant la population MAX, et 5 ayant la population MIN)
#-------------------------------------------------------------------------
def mapTenVilles(maxPop,minPop):
    """
    :param maxPop: fichier contenant les 5 villes ayant la population MAX
    :param minPop: fichier contenant les 5 villes ayant la population MIN
    """
    numDept=12
    #récupérer le contenue des fichiers avec les 5 villes ayant la population MAX et MIN
    with open(maxPop, "r", encoding="utf-8") as fichier:
        maxPopultemp=fichier.readlines()
    with open(minPop, "r", encoding="utf-8") as fichier:
        minPopultemp=fichier.readlines()
    #création de la liste des villes ayant la population MAX
    maxPopul=[]
    #création de la liste des villes ayant la population MIN
    minPopul=[]
    #boucle qui parcours la liste des villes ayant la population MAX
    for i in maxPopultemp:
        #découpage de la chaine de caractère pour en faire une liste
        maxPopul.append(i.split(','))
    #boucle qui parcours la liste des villes ayant la population MIN
    for i in minPopultemp:
        #découpage de la chaine de caractère pour en faire une liste
        minPopul.append(i.split(','))
    
    #création de la carte

    #initialisation de la liste des coordonnées des villes
    lon=[]
    lat=[]
    #initialisation de la liste de la densité de population des villes
    dens=[]
    #boucle qui parcours la liste des villes ayant la population MAX pour ajouter les coordonnées et la densité de population des villes dans les listes
    for i in maxPopul:
        #ajout de la densité de population des villes dans la liste "dens", en convertissant la chaine de caractère en nombre
        dens.append(float(i[6]))
        #ajout des coordonnées des villes dans les listes "lon" et "lat", en convertissant la chaine de caractère en nombre
        lon.append(float(i[8]))
        lat.append(float(i[9]))
    #boucle qui parcours la liste des villes ayant la population MIN pour ajouter les coordonnées et la densité de population des villes dans les listes
    for i in minPopul:
        #ajout de la densité de population des villes dans la liste "dens", en convertissant la chaine de caractère en nombre
        dens.append(float(i[6]))
        #ajout des coordonnées des villes dans les listes "lon" et "lat", en convertissant la chaine de caractère en nombre
        lon.append(float(i[8]))
        lat.append(float(i[9]))
    #coordonnées du centre de la carte
    coords = (46.539758, 2.430331)
    map1 = folium.Map(location=coords, tiles='OpenStreetMap', zoom_start=6)
    cm = branca.colormap.LinearColormap(['blue', 'red'], vmin=min(dens), vmax=max(dens))
    #ajout de la couleur en fonction de la densité de population
    map1.add_child(cm)
    #boucle qui parcours la liste des latitudes, longitudes et densité de population des villes
    for lati, lng, size, color in zip(lat, lon, dens, dens):
        folium.CircleMarker(
            location=[lati, lng],
            radius=size/100,
            color=cm(color),
            fill=True,
            fill_color=cm(color),
            fill_opacity=0.6
        ).add_to(map1)
    #enregistrement de la carte
    map1.save(outfile='map1.html')
    print("Carte enregistrée")


def MinMax10Accroissement(numDept,lstVillesDepart):
    """
    :param lstVillesDepart:

        recherche de 10 villes ayant la plus FORTE BAISSE de sa population entre 1999 et 2012
        recherche de 10 villes ayant le plus FORT ACCROISSEMENT de sa population entre 1999 et 2012
        on peut trier la liste par ordre croissant
        *** On IMPOSE le TRI BULLE vu au TP7 ****
        puis extraire les 10 premières valeurs et 10 dernières valeurs
    """
    def unPassage(tab, dernier):
        mouvement=0
        for i in range(0,dernier-1):
            if tab[i][5]-tab[i][4]>tab[i+1][5]-tab[i+1][4]:
                temp1=tab[i] 
                temp2=tab[i+1]
                tab[i]=temp2
                tab[i+1]=temp1
                mouvement+=1
        return tab,mouvement
    def triBulle(liste):
        dernier=len(liste)
        move=1
        while dernier!=0 and move>0:
            liste=unPassage(liste, dernier)[0]
            move=unPassage(liste, dernier)[1]
            dernier-=1
        return liste
    #tri de la liste des villes par accroissement entre 1999 et 2012, de population en ordre croissant
    liste = triBulle(lstVillesDepart)

    print("10 villes ayant la plus forte baisse de population entre 1999 et 2012 :")
    #ouverture du fichier contenant les 10 villes ayant la plus forte baisse de population entre 1999 et 2012
    with open(f"TopBaisse10Villes_{numDept}.txt", "w", encoding="utf-8") as fichier:
        #boucle qui parcours la liste des 10 villes ayant la plus forte baisse de population entre 1999 et 2012
        for i in range(0,10):
                #affichage des 10 villes ayant la plus forte baisse de population entre 1999 et 2012
                print(liste[i][1])
                #écriture des 10 villes ayant la plus forte baisse de population entre 1999 et 2012 dans le fichier
                fichier.write(str(liste[i][0]) + "," + str(liste[i][1]) + "," + str(liste[i][5]-liste[i][4]) + "\n")
    print("10 villes ayant la plus forte accroissement de population entre 1999 et 2012 :")
    #ouverture du fichier contenant les 10 villes ayant la plus forte accroissement de population entre 1999 et 2012
    with open(f"TopAcc10Villes_{numDept}.txt", "w", encoding="utf-8") as fichier:
        #boucle qui parcours la liste des 10 villes ayant la plus forte accroissement de population entre 1999 et 2012
        for i in range(len(liste)-1,len(liste)-11,-1):
                #affichage des 10 villes ayant la plus forte accroissement de population entre 1999 et 2012
                print(liste[i][1])
                #écriture des 10 villes ayant la plus forte accroissement de population entre 1999 et 2012 dans le fichier
                fichier.write(str(liste[i][0]) + "," + str(liste[i][1]) + "," + str(liste[i][5]-liste[i][4]) + "\n")



def MinMax5Alt_Dept(lstVillesDepart):
    """
    :param lstVillesDepart:

        recherche de 5 villes ayant la plus FAIBLE différence d'altitude dans un tableau
        recherche de 5 villes ayant la plus FORTE différence d'altitude dans un tableau
        on peut trier la liste par ordre croissant
        *** On IMPOSE le TRI BULLE vu au TP7 ****
        puis extraire les 5 premières valeurs
        Numéro du département = lstVillesDepart[0][0]
    """
    def unPassage(tab, dernier):
        mouvement=0
        for i in range(0,dernier-1):
            if tab[i][11]-tab[i][10]>tab[i+1][11]-tab[i+1][10]:
                temp1=tab[i] 
                temp2=tab[i+1]
                tab[i]=temp2
                tab[i+1]=temp1
                mouvement+=1
        return tab,mouvement
    def triBulle(liste):
        dernier=len(liste)
        move=1
        while dernier!=0 and move>0:
            liste=unPassage(liste, dernier)[0]
            move=unPassage(liste, dernier)[1]
            dernier-=1
        return liste
    #tri de la liste des villes par différence d'altitude en ordre croissant
    VillesDept=triBulle(lstVillesDepart)
    #numéro du département
    numDept=str(VillesDept[0][0])
    print("5 villes ayant la plus faible différence d'altitude dans le département :")
    #ouverture du fichier contenant les 5 villes ayant la plus faible différence d'altitude dans le département
    with open(f"Top5Alt_{numDept}.txt", "w", encoding="utf-8") as fichier:
        #boucle qui parcours la liste des 5 villes ayant la plus faible différence d'altitude dans le département
        for i in range(0,5):
            #affichage des 5 villes ayant la plus faible différence d'altitude dans le département
            print(VillesDept[i])
            #écriture des 5 villes ayant la plus faible différence d'altitude dans le département dans le fichier, avec département, le nom de la ville, la latitude, la longitude, et la différence d’altitude
            fichier.write(numDept + "," + str(VillesDept[i][1]) + "," + str(VillesDept[i][9]) + "," + str(VillesDept[i][8]) + "," + str(VillesDept[i][11]-VillesDept[i][10])+"\n")
    print("5 villes ayant la plus forte différence d'altitude dans le département :")
    #ouverture du fichier contenant les 5 villes ayant la plus forte différence d'altitude dans le département
    with open(f"Min5Alt_{numDept}.txt", "w", encoding="utf-8") as fichier:
        #boucle qui parcours la liste des 5 villes ayant la plus forte différence d'altitude dans le département
        for i in range(len(VillesDept)-1,len(VillesDept)-6,-1):
            #affichage des 5 villes ayant la plus forte différence d'altitude dans le département
            print(VillesDept[i])
            #écriture des 5 villes ayant la plus forte différence d'altitude dans le département dans le fichier, avec département, le nom de la ville, la latitude, la longitude, et la différence d’altitude
            fichier.write(numDept + "," + str(VillesDept[i][1]) + "," + str(VillesDept[i][9]) + "," + str(VillesDept[i][8]) + "," + str(VillesDept[i][11]-VillesDept[i][10])+"\n")
#-------------------------------------------------------------------------
# Procédure qui permet d'afficher sur une carte OpenStreetMap
# les 10 villes (5 ayant la différence d'ALTITUDE MAX
# et 5 ayant la différence d'ALTITUDE MIN)
#-------------------------------------------------------------------------
def mapTenAlt(maxAlt, minAlt):
    """

    :param maxAlt: fichier contenant les 5 villes de forte différence d'altitude
    :param minAlt: fichier contenant les 5 villes de faible différence d'altitude
    :return:
    """
    with open(maxAlt, "r", encoding="utf-8") as fichier:
        #lecture du fichier contenant les 5 villes de forte différence d'altitude
        lignesMaxAlt = fichier.readlines()
    
    with open(minAlt, "r", encoding="utf-8") as fichier:
        #lecture du fichier contenant les 5 villes de faible différence d'altitude
        lignesMinAlt = fichier.readlines()

    #création de la liste des villes ayant la plus forte différence d'altitude
    listeMaxAlt=[]
    #création de la liste des villes ayant la plus faible différence d'altitude
    listeMinAlt=[]
    #creation de la liste des coordonnées des villes
    lon=[]
    lat=[]
    #création de la liste des différences d'altitude
    alt=[]
    #boucle qui parcours la liste des villes ayant la plus forte différence d'altitude
    for i in lignesMaxAlt:
        #découpage de la chaine de caractère pour en faire une liste
        listeMaxAlt.append(i.split(','))
    #boucle qui parcours la liste des villes ayant la plus faible différence d'altitude
    for i in lignesMinAlt:
        #découpage de la chaine de caractère pour en faire une liste
        listeMinAlt.append(i.split(','))
    
    for i in listeMaxAlt:
        #ajout de la densité de population des villes dans la liste "dens", en convertissant la chaine de caractère en nombre
        alt.append(float(i[4]))
        #ajout des coordonnées des villes dans les listes "lon" et "lat", en convertissant la chaine de caractère en nombre
        lon.append(float(i[3]))
        lat.append(float(i[2]))
    #boucle qui parcours la liste des villes ayant la population MIN pour ajouter les coordonnées et la densité de population des villes dans les listes
    for i in listeMinAlt:
        #ajout de la densité de population des villes dans la liste "dens", en convertissant la chaine de caractère en nombre
        alt.append(float(i[4]))
        #ajout des coordonnées des villes dans les listes "lon" et "lat", en convertissant la chaine de caractère en nombre
        lon.append(float(i[3]))
        lat.append(float(i[2]))
    coords = (46.539758, 2.430331)
    map1 = folium.Map(location=coords, tiles='OpenStreetMap', zoom_start=6)
    cm = branca.colormap.LinearColormap(['blue', 'red'], vmin=min(alt), vmax=max(alt))
    #ajout de la couleur en fonction de la densité de population
    map1.add_child(cm)
    #boucle qui parcours la liste des latitudes, longitudes et densité de population des villes
    for lati, lng, size, color in zip(lat, lon, alt, alt):
        folium.CircleMarker(
            location=[lati, lng],
            radius=size/100,
            color=cm(color),
            fill=True,
            fill_color=cm(color),
            fill_opacity=0.6
        ).add_to(map1)
    #enregistrement de la carte
    map1.save(outfile='map2.html')
    print("Carte enregistrée")

#===================================================================
# Construction de l'HISTOGRAMME
#===================================================================
def traceHistoVilles(numDept,lstVillesDepart):
    popVilles = []
    for i in lstVillesDepart:
        popVilles.append(i[3])
    plt.hist(popVilles,bins=100, color='blue', edgecolor='red')
    plt.title(f"Dépt {numDept} nombre de villes en fonction de leur population")
    plt.xlabel("Population")
    plt.ylabel("Nombre de villes")
    plt.show()
    moyenne=0
    somme=0
    total=0
    #================================================
    #calcul de la moyenne de la population des villes
    #================================================
    #somme des populations des villes
    for i in popVilles:
        total+=i
    #calcul de la moyenne
    moyenne=total/len(popVilles)
    #affichage de la moyenne
    print(f"La moyenne de la population des villes du département {numDept} est de {moyenne} habitants")
    #==================================================
    #calcul de l'écart type de la population des villes
    #==================================================
    #somme des carrés des écarts à la moyenne
    for i in popVilles:
        somme+=(i-moyenne)**2
    #calcul de l'écart type
    ecartType=math.sqrt(somme/len(popVilles))
    #affichage de l'écart type
    print(f"L'écart type de la population des villes du département {numDept} est de {ecartType} habitants")

#====================================================================
# Distance EUCLIDIENNE entre 2 villes (en km)
#====================================================================
def dist_Euclidienne(ville1, ville2):
    #Méthode par le calcul de Pythagore
    #Multiplication par 111.32 pour convertir les degrés en km
    distance = math.sqrt((ville1[8]-ville2[8])**2 + (ville1[9]-ville2[9])**2)*111.32
    return distance

#====================================================================
# Distance GEODESIQUE (surface de la terre) entre 2 villes (en km)
# Formule de Haversine
#====================================================================
def dist_GEOdesique(ville1, ville2):
# calcul par la méthode HAVERSINE
    lat1 = math.radians(ville1[9])
    lon1 = math.radians(ville1[8])
    lat2 = math.radians(ville2[9])
    lon2 = math.radians(ville2[8])
    R = 6371 # rayon de la terre en km
    if math.sin(lat1)*math.sin(lat2)+math.cos(lat1)*math.cos(lat2)*math.cos(lon2-lon1) >1:
        S=0
    else:
        S=math.acos(math.sin(lat1)*math.sin(lat2)+math.cos(lat1)*math.cos(lat2)*math.cos(lon2-lon1))*R
    return S
#===============================================================
# ETAPE 5 : Parcours Ville1 ==> Ville2
#===============================================================

#=================================================================
# Recherche un ensemble de villes distante de R km dans une liste
#=================================================================
def ensembleVilles(name, rayon, listeVilles):
    """

    :param name: centre = ville avec les 12 infos
    :param rayon: distance de la ville retenue
    :param listeVilles: liste de toutes les villes
    :return: listeVilles[i] : la ville recherchée
    """
    listeVillesRetenues = []
    for i in listeVilles:
        if dist_GEOdesique(name, i) <= rayon:
            listeVillesRetenues.append(i)
    return listeVillesRetenues

#===================================================================
# ETAPE 5 : Plus court chemin entre les 2 Villes vil1 et vil2
#===================================================================
def parcoursVilles(vil1, vil2, listeRef, rayon, methode):
    #distance ville 1 à ville 2
    distMin=dist_GEOdesique(vil1, vil2)
    #initialisation de la ville la plus proche de la ville 2
    vilMin = vil1
    #liste des villes du trajet
    trajetVilles = [vil1]
    #initialisation de la population max
    popMax = 0
    #rayon de recherche des villes
    rayonDepart = rayon
    #liste des rayons de recherche
    listerayon = [rayon]
    if methode == "population":
            methode = 0
    else:
            methode = 1
    #recherche tant que la ville la plus proche de la ville 2 n'est pas la ville 2
    while vilMin != vil2:
        #liste des populations des villes à parcourir
        listepopMax = []
        #augmente le rayon de recherche des villes jusqu'a avoir une ville de plus de 1000 habitants
        while popMax < 1000:
            #liste des villes à parcourir
            listeVilles = ensembleVilles(vilMin, rayon, listeRef)
            #parcours toute les villes proche de la dernière ville
            for i in listeVilles:
                #recherche de la ville avec la plus proche de la ville 2
                if dist_GEOdesique(i, vil2) < distMin:
                    #ajoute la population de la ville dans la liste des populations
                    listepopMax.append(i[5])
                else:
                    #ajoute la population de la ville dans la liste des populations
                    listepopMax.append(0)
            #défini la population max
            popMax = max(listepopMax)
            #augmente le rayon de recherche des villes
            rayon += 1
        #parcours toute les villes proche de la dernière ville
        for i in listeVilles:
            #recherche de la ville avec la plus proche de la ville 2 ou celle avec la plus grande population
            if methode == 1:
                if dist_GEOdesique(vil2, i) < distMin and i not in trajetVilles and i[1] != vil2[1]:
                    #définit la ville la plus proche de la ville 2
                    vilMin = i
                    #définit la distance de la ville la plus proche de la ville 2
                    distMin = dist_GEOdesique(i, vil2)
                #si la ville la plus proche de la ville 2 est la ville 2
                elif i[1] == vil2[1]:
                    #condition d'arrêt de la boucle while
                    vilMin = i
            else:
                if (dist_GEOdesique(vil2, i) < distMin or i[5] == popMax) and i not in trajetVilles and i[1] != vil2[1]:
                    #définit la ville la plus proche de la ville 2
                    vilMin = i
                    #définit la distance de la ville la plus proche de la ville 2
                    distMin = dist_GEOdesique(i, vil2)
                #si la ville la plus proche de la ville 2 est la ville 2
                elif i[1] == vil2[1]:
                    #condition d'arrêt de la boucle while
                    vilMin = i
        #si la ville la plus proche de la ville 2 est pas la liste des villes du trajet
        if vilMin in trajetVilles:
            #augmente le rayon de recherche des villes
            rayon += 1
            print("ville déjà parcourue")
        else:
            listerayon.append(rayon)
            rayon = rayonDepart
            trajetVilles.append(vilMin)
            print(vilMin[1])
        popMax = 0
        listeVilles = ensembleVilles(vilMin, rayon, listeRef)
    return trajetVilles, listerayon
#----------------------------------------------------------------------------------
# On sauvegarde le trajet dans un fichier html pour l'afficher dans un navigateur
#----------------------------------------------------------------------------------
def map_trajet(villes_traversees,listerayon):
    lat = []
    lon = []
    ray = []
    for i in range(len(villes_traversees)):
        lat.append(villes_traversees[i][9])
        lon.append(villes_traversees[i][8])
        ray.append(listerayon[i])
    coords = (44.304147, 2.747558)
    map2 = folium.Map(location=coords, tiles='OpenStreetMap', zoom_start=6)
    cm = branca.colormap.LinearColormap(['blue', 'red'], vmin=min(rayon), vmax=max(rayon))
    #ajout de la couleur en fonction de la densité de population
    map2.add_child(cm)
    #boucle qui parcours la liste des latitudes, longitudes et densité de population des villes
    for lati, lng, size, color in zip(lat, lon, ray, ray):
        folium.CircleMarker(
            location=[lati, lng],
            radius=size,
            color=cm(color),
            fill=True,
            fill_color=cm(color),
            fill_opacity=0.6
        ).add_to(map2)
    #enregistrement de la carte
    map2.save(outfile=f"trajet_{villes_traversees[0][1]}_{villes_traversees[len(villes_traversees)-1][1]}_{listerayon[0]}.html")
    print("Carte enregistrée")

#===============================================================
# AFFICHE MENU
#===============================================================

def afficheMENU():
    print("\n================ MENU ==================")
    print("taper 1: Nombre de villes en fonction de l'indicatif téléphonique")
    print("taper 2: Extraire des Statistiques des Villes d’un département")
    print("taper 3: Distance Euclidienne et Géodésique entre 2 villes")
    print("taper 4: Plus court chemin entre 2 villes")
    print("F: pour finir")


def afficheSOUS_MENU(unDepartement):
    print("\n================ SOUS MENU : STATISTIQUES du Département ", unDepartement, "==================")
    print("taper 1: Lister les 5 Villes ayant le plus/le moins d'habitants")
    print("taper 2: Afficher les 10 Villes en fonction de la DENSITE sur une carte")
    print("taper 3: Lister les 10 Villes ayant le plus fort/faible taux d'accroissement")
    print("taper 4: HISTOGRAMME des villes par habitants")
    print("taper 5: Lister les 5 Villes ayant la différence d'altitude max/min")
    print("taper 6: Afficher les 10 Villes en fonction de l'ALTITUDE sur une carte")
    print("Q: pour Quitter le sous-menu")


#=============================================================================================
# Programme principal
# Appel de la procédure afficheMENU()
#=============================================================================================
fini = False
while fini == False:
    afficheMENU()
    choix = input("votre choix: ")
    if choix == '1':
        # Pour débuter il faut extraire des informations du fichier CSV
        listeInfo = appelExtractionVilles()
        #on demande à l'utilisateur de saisir un indicatif téléphonique
        indicatif = int(input("Entrer votre indicatif téléphonique : "))
        #on appelle la procédure qui affiche le nombre de villes en fonction de l'indicatif téléphonique
        appelNombre_Villes_Indicatif(indicatif,listeInfo)

    elif choix == '2':
        print("\n**** Nombre de Villes par Département *****")
        dept=int(input("Entrer le numéro du département : "))
        listeInfo = appelExtractionVilles()
        nbville, listeVilles = extract_villes_NumDepart(dept,listeInfo)
        print("Le département ", dept, "comporte ", nbville, "villes")
        #=====================================
        finiBis = False
        while finiBis == False:
            afficheSOUS_MENU(dept)
            choixBis = input("votre choix: ")
            if choixBis == '1':
                print("\nappel de la stat1 : Min/Max Habitants : 5 villes\n")
                #appel de la procédure qui affiche les 5 villes ayant le plus/le moins d'habitants
                MinMax5_villes_Habitants(dept,listeVilles)
            elif choixBis == '2':
                print("\nappel de la stat2: Afficher les 10 villes (DENSITE) sur la carte\n")
                #test si le fichier existe
                if not os.path.isfile(f"Top5Villes_{dept}") or not os.path.isfile(f"Min5Villes_{dept}"):
                    #appelle de la procédure qui met dans un fichier les 5 villes ayant la densité max/min si le fichier n'existe pas
                    MinMax5_villes_Habitants(dept,listeVilles)
                #appelle de la fonction qui affiche les 10 villes sur la carte
                mapTenVilles(f"Top5Villes_{dept}.txt", f"Min5Villes_{dept}.txt")
            elif choixBis == '3':
                print("\nappel de la stat3: ACCROISSEMENT/BAISSE population entre 1999 et 2012\n")
                #appel de la procédure qui affiche les 10 villes ayant le plus fort/faible taux d'accroissement
                MinMax10Accroissement(dept,listeVilles)
            elif choixBis == '4':
                print("\nappel de la stat4 : HISTOGRAMME du nombre des Villes par habitants\n")
                #appel de la procédure qui affiche l'histogramme du nombre des villes par habitants
                traceHistoVilles(dept,listeVilles)
            elif choixBis == '5':
                print("\nappel de la stat5 : ALTITUDE Min/Max : 5 villes\n")
                #appel de la procédure qui affiche les 5 villes ayant la différence d'altitude max/min
                MinMax5Alt_Dept(listeVilles)
            elif choixBis == '6':
                print("\nappel de la stat6: Afficher les 10 villes (ALTITUDE) sur la carte\n")
                if not os.path.isfile(f"Top5Alt_{dept}") or not os.path.isfile(f"Min5Alt_{dept}"):
                    #appelle de la procédure qui met dans un fichier les 5 villes ayant la plus grande/plus petite différence d'altitude si le fichier n'existe pas
                    MinMax5Alt_Dept(listeVilles)
                #appelle de la fonction qui affiche les 10 villes ayant la plus grande/plus petite différence d'altitude sur la carte
                mapTenAlt(f"Top5Alt_{dept}.txt", f"Min5Alt_{dept}.txt")
            else:
                finiBis = True
    elif choix == '3':
        listeInfo = appelExtractionVilles()
        ville1=input("Entrer le nom de la première ville en MAJUSCULE : ")
        infoVille1=rechercheVille(ville1,listeInfo)
        ville2=input("Entrer le nom de la deuxième ville en MAJUSCULE : ")
        infoVille2=rechercheVille(ville2,listeInfo)
        print("\nDistance Euclidienne entre 2 villes")
        distanceEucl=dist_Euclidienne(infoVille1, infoVille2)
        print("La distance Euclidienne entre ", ville1, "et", ville2, "est de", distanceEucl, "km")
        print("\nDistance Géodésique entre 2 villes")
        distanceGeo=dist_GEOdesique(infoVille1, infoVille2)
        print("La distance Géodésique entre ", ville1, "et", ville2, "est de", distanceGeo, "km")
    elif choix == '4':
        listeInfo = appelExtractionVilles()
        ville1=input("Entrer le nom de la première ville en MAJUSCULE : ")
        infoVille1=rechercheVille(ville1,listeInfo)
        ville2=input("Entrer le nom de la deuxième ville en MAJUSCULE : ")
        infoVille2=rechercheVille(ville2,listeInfo)
        zone_recherche=input("Entrer le rayon de recherche en km (défaut : 15km) : ")
        if zone_recherche == "":
            zone_recherche = 15
        else:
            zone_recherche = int(zone_recherche)
        typeitineraire=input("Entrer le type d'itinéraire (défaut : direct, ou population) : ")
        print("\nPLus court chemine entre 2 villes")
        villes, rayon = parcoursVilles(infoVille1, infoVille2, listeInfo,zone_recherche, typeitineraire)
        map_trajet(villes, rayon)
        print("*** Traitement terminé, Map réalisée ****")
    elif choix == '5':
        print("\nAppel de la fonction4\n")
    elif choix == 'F':
        fini = True

print("Fin du programme")
