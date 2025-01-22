import db_init
import random
from time import sleep

## Affichage du menu avec récupération du nom du joueur grâce à la fonction insert_new_player() ##
def show_menu():

    print(f"##")
    print(f"#####")
    print(f"Bienvenu(e) dans le Menu du jeu ! \n")

    player_name = insert_new_player()
    print(f"##\n")
    print(f"#####\n")
    print(f" {player_name}, Que voulez-vous faire ? \n")

    print(f"##")
    print(f"#####")
    print(f"1. Démarrer le jeu")
    print(f"##")
    print(f"#####")
    print(f"2. Voir le Highscore du jeu")
    print(f"##")
    print(f"#####")
    print(f"3. Voir le top 3 des scores")
    print(f"##")
    print(f"#####")
    print(f"4. Quitter le jeu")

    return player_name

## Fonction pour insérer un nouveau joueur dans la collection players avec un score par défaut de 0 ##
def insert_new_player():
    try: 

        enter_name = False

        ## Boucle qui se répète pour l'input du nom du joueur tant qu'un nom non existant dans la collection n'est pas encore entré ##

        while not enter_name:   
            #Saisie du nom du joueur
            input_player_name = input("Entrez le nom du joueur : ")

            # Vérfier si la collection player possède déjà un joueur avec le même nom
            is_player_existing = db_init.db_players.find_one({"player_name": {"$eq": input_player_name}})

            ## Si on trouve un personnage existe déjà, on ne le rajoute pas à la bdd et il passera direct au menu principal ##
            if is_player_existing:
               print(f"Joueur déjà existant dans la collection players \n Bienvenue {input_player_name} !")
               break
            else: 
                db_init.db_players.insert_one({"player_name" : input_player_name, "passed_round": 0})
                enter_name = True
                print(f"Joueur {input_player_name} ajouté à la collection players !")
                

        return input_player_name
    
    except Exception as e:
        print("Erreur lors de l'insertion du nouveau joueur dans la collection : ", e)

## Choisir un monstre aléatoire dans la collection monsters ##
def choose_random_monster():
    try: 
    #Accès la liste entière de monstres 
        all_monsters = list(db_init.db_monsters.find({}, {"_id": 0}))
        #Choisir un monstre aléatoire dans la liste
        random_monster = random.choice(all_monsters)
        #Afficher le monstre choisi avec ses stats
        print(f"Le monstre désigné est : {random_monster['name']}, ATK : {random_monster['ATK']}, DEF : {random_monster['DEF']}, PV : {random_monster['PV']}")
        return random_monster
    except Exception as e:
        print("Erreur lors du choix du monstre : ", e)

## Sélectionner les personnages pour l'équipe du joueur et afficher ses stats ##
def show_and_select_characters():
    try:
        ## Accès à la collection characters ##
        all_characters = list(db_init.db_characters.find({}, {"_id": 0}))

        ## afficher les personnages disponibles en commençant l'index à 1 ##
        for index, character in enumerate(all_characters, start= 1):

            print(f"{index}. Type : {character['type']} - ATK : {character['ATK']} - DEF : {character['DEF']} - PV : {character['PV']}")

        ## Sélection des personnages par le joueur ##
        # Equipe vide à l'état initial
        team = []
        # Ajout de 3 personnages dans l'équipe dans une boucle qui ne se repète que 3 fois
        for i in range(3):
            choice = int(input(f"Choisissez le personnage {i+1} : "))
            #Ajouter le personnage ayant l'index +1 dans la team[]
            team.append(all_characters[choice-1]) # -1 car les index commencent à 0
        #Afficher l'équipe constituée : 
        print(f"Voici la compositiond de votre équipe : ")
        for member in team:
            print(f"Type : {member['type']} - ATK : {member['ATK']} - DEF : {member['DEF']} - PV : {member['PV']}")
        return team
    except Exception as e:
        print("Erreur lors de l'affichage des personnages : ", e)

## Mécanique d'attaque des membres de l'équipe ##
def team_attack(team, monster):
        
        for member in team:
            if member["PV"] > 0:

                print(f"Le personnage {member['type']} attaque {monster['name']} !")

                # Calcul des dégâts infligés au monstre (en évitant les valeurs négatives avec max())
                damages_monstre = max((member["ATK"] - monster["DEF"]), 0)

                print(f"{member["type"]} inflige {damages_monstre} dégâts à {monster["name"]} !")

                # Réduire les PV du monstre
                monster["PV"] -= damages_monstre
                print(f"##")
                print(f"#####")
                print(f"#########")
                print(f"#####")
                print(f"###")
                sleep(1.5)

            else:
                #Si le perso n'a plus de PV, il est mort et est enlevé de l'équipe
                print(f"Le personnage {member['type']} n'a plus de PV et est KO !")
                team.remove(member)
                break

## Mécanique d'attaque du monstre ##
def monster_attack(team, monster):
        if monster['PV'] > 0:
            print(f"{monster['name']} attaque l'équipe !")
            # choix aléatoire d'un perso à attaquer si équipe non vide
            if team:
                attacked_character = random.choice(team)
            # Vérifie si le perso visé n'est pas déjà mort
                if attacked_character["PV"] <= 0:
                    print(f"{attacked_character['type']} est déjà mort, il ne peut pas être attaqué !")
                    return
            # Calcul des dégâts infligés au perso en évitant les valeurs négatives avec max()
                damages_character = max((monster['ATK'] - attacked_character['DEF']), 0)
                print(f"{monster["name"]} inflige {damages_character} dégâts à {attacked_character["type"]} !")
            # Réduire les PV du perso attaqué
                attacked_character["PV"] -= damages_character

                print(f"##")
                print(f"#####")
                print(f"#########")
                print(f"#####")
                print(f"###")
                sleep(1.5)

        else: 
            # Si PV du monstre = 0, le monstre est mort
            print(f"Victoire ! {monster['name']} est mort !")

        """ 3. **Système de combat**
    - Une fois l'équipe créée, le joueur affronte des monstres aléatoires tirés de la base de données.
    - Le combat se poursuit à l'infini, avec un compteur de vagues qui s'incrémente à chaque victoire.
    - Chaque personnage possède des points de vie (PV), s'ils atteignent zéro, l'équipe est vaincue. """

## Mécanique de combat ##
def fight(team, monster, player_name):
    ## Vérification pour voir si une équipe et un monstre existent ##
    if not team:
        print("L'équipe est vide, le jeu ne peut pas commencer !")
        return
    if not monster:
        print("Il n'y a pas de monstre à combattre, le combat ne peut pas commencer !")
        return
    
    ## Initialisation du jeu ##

    # Round = 0 au début, avec un +1 si victoire ou rien si défaite
    round = 1
    # Tant que l'équipe a encore un membre, le combat continue
    while team:

        ## Pour chaque membre de la Team, si PV > 0 alors attaque le monstre ##
        print(f"#####")
        print(f"#########")
        print(f"Round {round} :")
        print(f"#########")
        print(f"#####")
        ## Attaque par les membres de l'équipe ##
        team_attack(team, monster)

        ## Après chaque attaque des persos, le monstre attaque à son tour 1 membre au hasard s'il est encore en vie
        monster_attack(team, monster)
        
        ## Affichage des stats du monstre et des membres de l'équipe après chaque tour ##
        print(f"Stats du monstre {monster['name']} : ATK : {monster['ATK']} - DEF : {monster['DEF']} - PV : {monster['PV']}")
        print(f"#########")
        print(f"Stats de l'équipe : \n")
        for member in team:
            print(f"Type : {member['type']} - ATK : {member['ATK']} - DEF : {member['DEF']} - PV : {member['PV']}")
            print(f"######")
        ## Si tous les persos sont morts (= tableau team[]ayant 0 éléements), le combat est fini
        if not team:
            print(f"Défaite ! L'équipe a été vaincue par {monster['name']} !")
        ## Affichage du nombre de round passés ##
            print(f"Vous avez survécu à {round} rounds.")
        ## Mise à jour du score du joueur via une fonction ##
            add_passed_round_to_highscore(player_name, round)
            break
    ## Si équipe n'est pas vide et que le monstre est mort, on incrémente le round + 1 ##
        else:
            
            print(f"Victoire ! {monster['name']} a été vaincu !")
            round += 1
            print(f"Vous avez effectué {round} rounds.")

            print(f"##")
            print(f"#####")
            print(f"#########")
            print(f"#####")
            print(f"###")
            sleep(3)

        ## Choix d'un nouveau monstre aléatoire pour le prochain round ##
            monster = choose_random_monster()
            if not monster:
                print("Il n'y a pas de monstres à combattre !")
                break

    print(f"Nombre de rounds passés : {round}")
    return round

## Mettre à jour le nombre de rounds passés par le joueur actif une fois sa partie terminée ##
def add_passed_round_to_highscore(player_name, round):
    try:
        ## Ciblage le nom du joueur ayant fait la partie et mise à jour de son nombre de rounds passés ##
        db_init.db_players.update_one({"player_name": player_name}, {"$set": {"passed_round": round}})
        print(f"Score du joueur {player_name} mis à jour !")
    except Exception as e:
        print("Erreur lors de l'ajout du nombre de rounds passés à la collection : ", e)

## Voir le highscore entier du jeu ##
def show_highscore():

    try:
        ## Accès à la collection players ##
        all_players = list(db_init.db_players.find({}))
        ## afficher le highscore du jeu ##
        for player in all_players:
            print(f"Joueur : {player['player_name']} - Round passé : {player['passed_round']}")
    except Exception as e:
        print("Erreur lors de l'affichage du highscore : ", e)

## Voir uniquement les 3 meilleurs scores du jeu ##
def show_three_highest_score():
    try: 
        ## Connexion à la Bdd et on récupère tous les scores et les noms des joueurs respectifs ##
        all_scores = list(db_init.db_players.find({}, {"_id": 0}))

        ## On trie (= sorted()) les scores par ordre décroissant (=reverse =True) et on affiche les 3 meilleurs scores (on slice = [:3]) ##
        sort_scores = sorted(all_scores, reverse=True, key=lambda x: x["passed_round"])[:3]

        print(f"Les 3 meilleurs scores du jeu sont :\n")
        ranking = 1
        for one_score in sort_scores:
            print(f"{ranking}) {one_score['player_name']} - Score : {one_score['passed_round']}")
            ranking += 1

    except Exception as e:
        print("Erreur lors de l'affichage des 3 meilleurs scores : ", e)