from dataclasses import dataclass
from datetime import datetime, timedelta

@dataclass
class MESSAGES_ACTIVITES:
    DateMessage: datetime = datetime.now()
    NoZone: int= 0
    Message: str = ""


@dataclass
class GICLEURS:
    NoZone: int = 0
    ZoneNom: str = ""
    ZonePhysique: str = ""
    ZoneActive: bool = False
    TempsArrosage: int = 0
    Affichage: bool = False
    AffichageWeb: bool = False
    MessageErreur: str = ""

@dataclass
class ARROSAGE_DATA:
    NoZone: int = 0
    TempsArrosage: int = 0
    ArrosageEnCour: bool = False
    ArrosageTermine: bool = False

@dataclass
class CONFIGURATION_GENERALE:
    HeureDebutArrosage: str = ""   
    SystemArrosageActif: bool = False         
    SondePluieActive: bool = False           
    ArrosageJourPairImpair: str = ""
    NombreJourInterval: int = 0    

@dataclass
class GICLEURS_STATUT:  
    NoZone: int = 0
    Statut: bool = False

@dataclass
class GICLEUR_EN_COUR:  
    NoZone: int = 0  
    HeureDepartArrosage: int = 0  
