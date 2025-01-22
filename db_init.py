## Insertion des persos et monstres dans MongoDB ##

import pymongo
import os

# Connexion à la base de données :
try: 
    client = pymongo.MongoClient(os.environ.get("MONGO_DB_PATH"))
    """print("Connexion à la base de données ok à l'adresse : ", client)"""
except Exception as e:
    print("Erreur lors de la connexion à MongoDB : ", e)

# Création de la base de données "game" avec ses 3 collections (characters, monsters, players) :
try:
    db = client["game"]
    """print("Base de données ", client , "créée avec succès.")"""

except Exception as e:
    print("Erreur lors de la création de la base de données : ", e)

try: 
    db_characters = db["characters"]
    db_monsters = db["monsters"]
    db_players = db["players"]
    """print("Collections ",  db_characters, db_monsters, db_players, " créées avec succès.")"""
except Exception as e:
    print("Erreur lors de la création des collections : ", e)
## Insertion des autres personnages et monstres dans les collections respectives ##

try:
    ## Insérer les persos dans la collection characters ##
    
    ## data des persos (type, ATK, DEF, PV) ##

    characters = [
       {"type": "Mage", "ATK": 20, "DEF": 5, "PV": 80},
        {"type": "Archer", "ATK": 18, "DEF": 7, "PV": 90},
        {"type": "Voleur", "ATK": 22, "DEF": 8, "PV": 85},
        {"type": "Paladin", "ATK": 14, "DEF": 12, "PV": 110},
        {"type": "Sorcier", "ATK": 25, "DEF": 3, "PV": 70},
        {"type": "Chevalier", "ATK": 17, "DEF": 15, "PV": 120},
        {"type": "Moine", "ATK": 19, "DEF": 9, "PV": 95},
        {"type": "Berserker", "ATK": 23, "DEF": 6, "PV": 105},
        {"type": "Chasseur", "ATK": 16, "DEF": 11, "PV": 100}
    ]
        ## Si on trouve un personnage existe déjà, on ne le rajoute pas à la bdd ##
    for character in characters:
        if not db_characters.find_one({"type": {"$eq": character["type"]}}):
            db_characters.insert_one(character)
    else:
        """print("Personnage déjà existant dans la collection characters")"""   
        
except Exception as e:
        """print("Erreur lors de l'insertion des valeurs dans la collection : ", e)"""


try:
    ## Data monsters (name, ATK, DEF, PV) ##
    monsters = [
        {"name": "Orc", "ATK": 20, "DEF": 8, "PV": 120},
        {"name": "Dragon", "ATK": 35, "DEF": 20, "PV": 300},
        {"name": "Zombie", "ATK": 12, "DEF": 6, "PV": 70},
        {"name": "Troll", "ATK": 25, "DEF": 15, "PV": 200},
        {"name": "Spectre", "ATK": 18, "DEF": 10, "PV": 100},
        {"name": "Golem", "ATK": 30, "DEF": 25, "PV": 250},
        {"name": "Vampire", "ATK": 22, "DEF": 12, "PV": 150},
        {"name": "Loup-garou", "ATK": 28, "DEF": 18, "PV": 180},
        {"name": "Squelette", "ATK": 15, "DEF": 7, "PV": 90}
        ]
    
    ## Si un monstre existe déjà, on ne le rajoute pas à la collection ##
    for monster in monsters:
        if not db_monsters.find_one({"name": {"$eq": monster["name"]}}):
            db_monsters.insert_one(monster)
    else:
        """print("Personnage déjà existant dans la collection monsters")"""   
        
except Exception as e:
        print("Erreur lors de l'insertion des valeurs dans la collection monsters: ", e)