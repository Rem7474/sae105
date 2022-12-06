"""
Programme SAE 105: Traitement de données:
Fichier: ville_france.csv contenant des informations sur les 36700 Villes de France
BUT1 : Année 2022-2023
@author: CUVELIER Rémy B1
"""
# pour afficher la carte avec les villes

import folium,branca
#import matplotlib.pyplot as plt
#import math


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
    :param indTel: indicatif téléphonique
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
    print(f"nombre de villes dans les départements ayant l'indicatif {indTel} = {nbVilles}")
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


"""
    A compléter
"""

# --------------------------------------------------------
# Fonction extract_villes_depart_indicatif(listeInfo)
# --------------------------------------------------------
def extract_villes_NumDepart(listeInfo):
    """
    Fonction qui extrait l'ensemble des villes pour chaque département,
    en fonction du numéro du Département

    :param numDept: numéro du département
    :param listeVilles: liste des noms de villes
    :return: nbVilles = nombre de villes du département
    """
    #initioalisation de la variable numDept à 12, donc ce n'est pas un parametre d'entrée
    numDept=12
    # initialisation de la variable nbVilles à 0
    nbVilles = 0
    #création de la liste des villes du département
    listeVilles = []
    # boucle qui parcours la liste "listeInfo"
    for i in listeInfo:
        # test si la ville appartient au département
        if i[0] == numDept:
            # incrémentation de la variable nbVilles
            nbVilles += 1
            # ajout de la ville dans la liste des villes du département
            listeVilles.append(i)
    # écriture dans le fichier
    with open(f"villes_{numDept}.txt", "w", encoding="utf-8") as fichier:
        for i in listeVilles:
            fichier.write(str(i) + "\n")
    return nbVilles, listeVilles

# ================================================
# Fonctions Utiles pour le Tri Bulle lié à la POPULATION
# ================================================

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

def MinMax5_villes_Habitants():
    """
    :param numDept:
    :param lstVillesDepart:

        recherche de 5 villes ayant le MOINS d'habitants dans un tableau
        recherche de 5 villes ayant le PLUS d'habitants dans un tableau
        on peut trier la liste par ordre croissant
        *** On IMPOSE le TRI BULLE vu au TP7 ****
        puis extraire les 5 premières valeurs
    """
    #initialisation de la variable numDept à 12
    numDept=12
    #appelle de la fonction qui extrait les villes du département 12
    lstVillesDepart=extract_villes_NumDepart(listeInfo)[1]
    #appelle de la fonction qui trie les villes du département 12 en fonction de la population de 2010
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
def mapTenVilles():#maxPopul, minPopul
    """

    :param maxPop: fichier contenant les 5 villes de forte densité
    :param minPop: fichier contenant les 5 villes de faible densité
    :return:
    """
    numDept=12
    #récupérer le contenue du fichier "Top5Villes_12.txt"
    with open(f"Top5Villes_{numDept}.txt", "r", encoding="utf-8") as fichier:
        maxPopultemp=fichier.readlines()
    with open(f"Min5Villes_{numDept}.txt", "r", encoding="utf-8") as fichier:
        minPopultemp=fichier.readlines()
    maxPopul=[]
    minPopul=[]
    for i in maxPopultemp:
        maxPopul.append(i.split(','))
    for i in minPopultemp:
        minPopul.append(i.split(','))
    #création de la carte
    stations=[]
    lon=[]
    lat=[]
    dens=[]
    for i in maxPopul:
        stations.append(i[1])
        dens.append(float(i[6]))
        lon.append(float(i[8]))
        lat.append(float(i[9]))
    for i in minPopul:
        stations.append(i[1])
        dens.append(float(i[6]))
        lon.append(float(i[8]))
        lat.append(float(i[9]))
    coords = (46.539758, 2.430331)
    map1 = folium.Map(location=coords, tiles='OpenStreetMap', zoom_start=6)
    cm = branca.colormap.LinearColormap(['blue', 'red'], vmin=min(dens), vmax=max(dens))
    map1.add_child(cm) # add this colormap on the display

    for lati, lng, size, color in zip(lat, lon, dens, dens):
        folium.CircleMarker(
            location=[lati, lng],
            radius=size/100,
            color=cm(color),
            fill=True,
            fill_color=cm(color),
            fill_opacity=0.6
        ).add_to(map1)
    map1.save(outfile='map1.html')
    print("Traitement terminé")



def MinMax10Accroissement(lstVillesDepart):
    """
    :param lstVillesDepart:

        recherche de 10 villes ayant la plus FORTE BAISSE de sa population entre 1999 et 2012
        recherche de 10 villes ayant le plus FORT ACCROISSEMENT de sa population entre 1999 et 2012
        on peut trier la liste par ordre croissant
        *** On IMPOSE le TRI BULLE vu au TP7 ****
        puis extraire les 10 premières valeurs et 10 dernières valeurs
    """
"""
    A compléter
"""


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


"""
    A compléter
"""


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

    """
        A compléter
    """


#===================================================================
# Construction de l'HISTOGRAMME
#===================================================================
def traceHistoVilles(lstVillesDepart):
    """
        A compléter
    """

#====================================================================
# Distance EUCLIDIENNE entre 2 villes (en km)
#====================================================================
def dist_Euclidienne(ville1, ville2):
# Méthode par le calcul de Pythagore
    """
        A compléter
    """

#====================================================================
# Distance GEODESIQUE (surface de la terre) entre 2 villes (en km)
# Formule de Haversine
#====================================================================
def dist_GEOdesique(ville1, ville2):
# calcul par la méthode HAVERSINE
    """
        A compléter
    """

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


    """
        A compléter
    """

#===================================================================
# ETAPE 5 : Plus court chemin entre les 2 Villes vil1 et vil2
#===================================================================
def parcoursVilles(vil1, vil2, listeRef, rayon):
    """
        A compléter
    """

#----------------------------------------------------------------------------------
# On sauvegarde le trajet dans un fichier html pour l'afficher dans un navigateur
#----------------------------------------------------------------------------------
def map_trajet(villes_traversees):
    """
        A compléter
    """

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
        print("A compléter")
        listeInfo = appelExtractionVilles()
        extract_villes_NumDepart(listeInfo)
        #=====================================
        finiBis = False
        while finiBis == False:
            # ==> Changer le numéro du Département <==
            afficheSOUS_MENU(74)
            choixBis = input("votre choix: ")
            if choixBis == '1':
                print("\nappel de la stat1 : Min/Max Habitants : 5 villes\n")
                MinMax5_villes_Habitants()
                mapTenVilles()
            elif choixBis == '2':
                print("\nappel de la stat2: Afficher les 10 villes (DENSITE) sur la carte\n")
                """
                    A compléter
                """
            elif choixBis == '3':
                print("\nappel de la stat3: ACCROISSEMENT/BAISSE population entre 1999 et 2012\n")
                """
                    A compléter
                """
            elif choixBis == '4':
                print("\nappel de la stat4 : HISTOGRAMME du nombre des Villes par habitants\n")
                """
                    A compléter
                """
            elif choixBis == '5':
                print("\nappel de la stat5 : ALTITUDE Min/Max : 5 villes\n")
                """
                    A compléter
                """
            elif choixBis == '6':
                print("\nappel de la stat6: Afficher les 10 villes (ALTITUDE) sur la carte\n")
                """
                    A compléter
                """
            else:
                finiBis = True
    elif choix == '3':
        print("\nDistance Euclidienne entre 2 villes")
        """
            A compléter
        """

        print("\nDistance Géodésique entre 2 villes")
        """
            A compléter
        """
    elif choix == '4':
        print("\nPLus court chemine entre 2 villes")
        """
            A compléter
        """
        print("*** Traitement terminé, Map réalisée ****")
    elif choix == '5':
        print("\nAppel de la fonction4\n")
    elif choix == 'F':
        fini = True

print("Fin du programme")
