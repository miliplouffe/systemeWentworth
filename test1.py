# SPDX-FileCopyrightText: 2017 Tony DiCola for Adafruit Industries
#
# SPDX-License-Identifier: MIT

# Simple demo of reading and writing the digital I/O of the MCP2300xx as if
# they were native CircuitPython digital inputs/outputs.
# Author: Tony DiCola
import time

from dataclasses import dataclass
from datetime import datetime, timedelta
from time import sleep
import RedisInOut as redisInOut

import rpiMethodes

@dataclass
class EQUIPEMENT:
    heureLecture: datetime = datetime.now()
    nomEquipement: str = ""
    valeur: int = 0

equipementsAlarmes = dict ()
equipementsGicleurs = dict()

def initialiseGicleurs(equipementsGicleurs):
    temp = EQUIPEMENT()
    temp.heureLecture = datetime.now()
    temp.nomEquipement = "pinGicleur1"
    temp.valeur=0 
    equipementsGicleurs[temp.nomEquipement]=temp

    temp = EQUIPEMENT()
    temp.heureLecture = datetime.now()
    temp.nomEquipement = "pinGicleur2"
    temp.valeur=0 
    equipementsGicleurs[temp.nomEquipement]=temp

    temp = EQUIPEMENT()
    temp.heureLecture = datetime.now()
    temp.nomEquipement = "pinGicleur3"
    temp.valeur=0 
    equipementsGicleurs[temp.nomEquipement]=temp

    temp = EQUIPEMENT()
    temp.heureLecture = datetime.now()
    temp.nomEquipement = "pinGicleur4"
    temp.valeur=0 
    equipementsGicleurs[temp.nomEquipement]=temp
    
    return equipementsGicleurs


def initialiseAlarmes(equipementsAlarmes):
    temp = EQUIPEMENT()
    temp.heureLecture = datetime.now()
    temp.nomEquipement = "pinChambrePrincipale"
    temp.valeur=0 
    equipementsAlarmes[temp.nomEquipement]=temp

    temp = EQUIPEMENT()
    temp.heureLecture = datetime.now()
    temp.nomEquipement = "pinChambreSecondaire"
    temp.valeur=0 
    equipementsAlarmes[temp.nomEquipement]=temp

    temp = EQUIPEMENT()
    temp.heureLecture = datetime.now()
    temp.nomEquipement = "pinSalon"
    temp.valeur=0 
    equipementsAlarmes[temp.nomEquipement]=temp

    temp = EQUIPEMENT()
    temp.heureLecture = datetime.now()
    temp.nomEquipement = "pinBureau"
    temp.valeur=0 
    equipementsAlarmes[temp.nomEquipement]=temp

    temp = EQUIPEMENT()
    temp.heureLecture = datetime.now()
    temp.nomEquipement = "pinSousSol"
    temp.valeur=0 
    equipementsAlarmes[temp.nomEquipement]=temp

    temp = EQUIPEMENT()
    temp.heureLecture = datetime.now()
    temp.nomEquipement = "pinSalleVernis"
    temp.valeur=0 
    equipementsAlarmes[temp.nomEquipement]=temp

    temp = EQUIPEMENT()
    temp.heureLecture = datetime.now()
    temp.nomEquipement = "pinPorteAvant"
    temp.valeur=0 
    equipementsAlarmes[temp.nomEquipement]=temp

    temp = EQUIPEMENT()
    temp.heureLecture = datetime.now()
    temp.nomEquipement = "pinPorteArriere"
    temp.valeur=0 
    equipementsAlarmes[temp.nomEquipement]=temp

    temp = EQUIPEMENT()
    temp.heureLecture = datetime.now()
    temp.nomEquipement = "pinPorteSousSol"
    temp.valeur=0 
    equipementsAlarmes[temp.nomEquipement]=temp

    temp = EQUIPEMENT()
    temp.heureLecture = datetime.now()
    temp.nomEquipement = "pinSensorFumeeSalleBillard"
    temp.valeur=0 
    equipementsAlarmes[temp.nomEquipement]=temp

    temp = EQUIPEMENT()
    temp.heureLecture = datetime.now()
    temp.nomEquipement = "pinEauAtelier"
    temp.valeur=0 
    equipementsAlarmes[temp.nomEquipement]=temp

    temp = EQUIPEMENT()
    temp.heureLecture = datetime.now()
    temp.nomEquipement = "pinSensorFumeeAtelier"
    temp.valeur=0 
    equipementsAlarmes[temp.nomEquipement]=temp

    temp = EQUIPEMENT()
    temp.heureLecture = datetime.now()
    temp.nomEquipement = "pinSensorPluie"
    temp.valeur=0 
    equipementsAlarmes[temp.nomEquipement]=temp

    return equipementsAlarmes


def executeRequete(requete):
    print ("requete arrosage 1 ", requete)
    if requete == "Gicleur_1_ON":
        print ("--------------------- ON")
        rpiMethodes.set_relais("relais1", True)
        redisInOut.setRequeteArrosageNil()

    if requete == "Gicleur_1_OFF":
        print ("-------------------- OFF")
        rpiMethodes.set_relais("relais1", False)    
        redisInOut.setRequeteArrosageNil()

    print ("requete arrosage 1 ", requete)
    if requete == "Gicleur_2_ON":
        print ("--------------------- ON")
        rpiMethodes.set_relais("relais2", True)
        redisInOut.setRequeteArrosageNil()

    if requete == "Gicleur_2_OFF":
        print ("-------------------- OFF")
        rpiMethodes.set_relais("relais2", False)    
        redisInOut.setRequeteArrosageNil()

    print ("requete arrosage 3 ", requete)
    if requete == "Gicleur_3_ON":
        print ("--------------------- ON")
        rpiMethodes.set_relais("relais3", True)
        redisInOut.setRequeteArrosageNil()

    if requete == "Gicleur_3_OFF":
        print ("-------------------- OFF")
        rpiMethodes.set_relais("relais3", False)    
        redisInOut.setRequeteArrosageNil()

    print ("requete arrosage 1 ", requete)
    if requete == "Gicleur_4_ON":
        print ("--------------------- ON")
        rpiMethodes.set_relais("relais4", True)
        redisInOut.setRequeteArrosageNil()

    if requete == "Gicleur_4_OFF":
        print ("-------------------- OFF")
        rpiMethodes.set_relais("relais4", False)    
        redisInOut.setRequeteArrosageNil()




redisInOut.StartSystemeArrosageRequete()


if __name__ == '__main__':

    # Now loop blinking the pin 0 output and reading the state of pin 1 input.
    sleep(2)

    equipementsAlarmes = initialiseAlarmes(equipementsAlarmes)
    equipementsGicleurs = initialiseGicleurs(equipementsGicleurs)
    
    redisInOut.publishInterfaceAlarmeDetecteur(equipementsAlarmes)
    redisInOut.publishInterfaceDetecteurArrosage(equipementsGicleurs)

    while True:
        # Blink pin 0 on and then off.
        # pin0.value = True
        requete=redisInOut.getRequeteArrosage()
        redisInOut.setRequeteArrosageNil()
        time.sleep(.3)
        print ("Requete : ", requete)
        equipementsAlarmes=rpiMethodes.getValeursAlarme(equipementsAlarmes)
        print(equipementsAlarmes)
        print ("passe 2")
        equipementsGicleurs=rpiMethodes.getValeursGicleurs(equipementsGicleurs)
        print ("passe 3")
