#!/usr/bin/python
# -*- coding: iso-8859-15 -*-

# import des modules necessaires
import os,sys,glob,datetime,random,urllib,time

from firebase import firebase
import RPi.GPIO as GPIO # Pour piloter le RPI

from TableauSoleil import TableauSoleil # Import du tableau avec les horaires de leves et couches de soleil
from ModuleGestionConnexion import InternetOk # Import des fonctions permettant de tester la connexion internet
from VariablesConfig import CompteFirebase # Import du fichier de config (pour les variables)
from GestionBuffer import TableauBuffer, AjouterItemBuffer, SupprimerVieilleValeurBuffer, LirePlusVieilleValeurBuffer, ViderBuffer # Import du module de gestion du buffer (en cas de perte du reseau)
import ModuleLampe, ModuleJourAnnee

# On initialise quelques variables pour rendre le programme paramétrable
Interval=60*10  # Temps en seconde entre chaque vérification
EtatLampe=False # On part du principe qu'au lancement la lumière est éteinte
NumPortGPIO=40 # Numero du port qui est utilisé

# On bascule le GPIO et notamment le port utilisé en mode OUT
GPIO.setmode(GPIO.BOARD)
GPIO.setup(NumPortGPIO, GPIO.OUT)

DateDuJour = datetime.datetime.now()
HoraireDuMoment="{:%H:%M}".format(DateDuJour)

# Avant de commencer, on commence par eteindre la lampe (au cas où)
EteindreLampe(NumPortGPIO)
# On entre dans la boucle infinie
i=0
firebase = firebase.FirebaseApplication(CompteFirebase,None)
    # On commence par récupérer la position du jour en cours dans l'année
while 1==1 :
    DateDuJour = datetime.datetime.now()
    HoraireDuMoment="{:%H:%M}".format(DateDuJour)
    NumeroDuJour=numjouran([DateDuJour.day, DateDuJour.month, DateDuJour.year])
    #NumeroDuJour=1     # Pour l'essai, on positionne le numero à 1
    # On récupère les valeurs du levé et couché pour le jour correspondand dans le tableau
    HoraireLeveSoleil=TableauSoleil[NumeroDuJour][0]
    HeureLeve=int(HoraireLeveSoleil[0:2])
    MinuteLeve=int(HoraireLeveSoleil[3:5])
    HoraireCoucheSoleil=TableauSoleil[NumeroDuJour][1]
    HeureCouche=int(HoraireCoucheSoleil[0:2])
    MinuteCouche=int(HoraireCoucheSoleil[3:5])
    HeureDuMoment=int(HoraireDuMoment[0:2])
    MinuteDuMoment=int(HoraireDuMoment[3:5])
    NbMinutesLeve=int(HeureLeve*60+MinuteLeve)
    NbMinutesCouche=int(HeureCouche*60+MinuteCouche)
    NbMinutesDuMoment=int(HeureDuMoment*60+MinuteDuMoment)
    Moment=""
    #On peut à présent regarder si on est dans une période de nuit ou de jour
    Nuit=False
    if NbMinutesDuMoment < NbMinutesLeve:
        Nuit=True
        Moment="Matin"
    else:
        if NbMinutesDuMoment < NbMinutesCouche:
            Nuit=False
            Moment="Journee"
        else:
            Nuit=True
            Moment="Soir"
    # On peut à présent regarde l'état de la lampe et activer l'interrupteur qu'en cas de changement
    if EtatLampe==Nuit:
        #print("On ne change pas l'état de la lampe")
        i=i
    else:
        #print("On change l'etat de la lampe")
        EtatLampe=not EtatLampe
	# On appelle la fonction de gestion de la lampe en fonction de l'etat de la variable
	if EtatLampe==True:
        AllumerLampe(NumPortGPIO)
        #VariableFirebase="/Lampe/1" + Chaine
        Horodatage=datetime.datetime.now()
        firebase.put('/Lampe/1','Etat',1)
        firebase.put('/Lampe/1','Date',Horodatage)
    else:
        EteindreLampe(NumPortGPIO)
        #VariableFirebase="/Lampe/1" + Chaine
        Horodatage=datetime.datetime.now()
        firebase.put('/Lampe/1','Etat',0)
        firebase.put('/Lampe/1','Date',Horodatage)
    print(DateDuJour.day,DateDuJour.month, DateDuJour.year,"(",NumeroDuJour,")",HoraireDuMoment,"(",HoraireLeveSoleil,"/",HoraireCoucheSoleil,")",Moment,EtatLampe)

    i=i+1
    time.sleep(Interval)
