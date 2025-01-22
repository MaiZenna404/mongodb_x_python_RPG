### Import du fichier db_init.py pour initialiser la base de données ###
from db_init import *
from game import *

### Début du jeu 

player_name = show_menu()

choice = int(input())

match choice:
    case 1:
        print(f"Vous avez choisi de démarrer le jeu")
        team = show_and_select_characters()
        monster = choose_random_monster()
        fight(team, monster, player_name)
    case 2:
        print(f"Vous avez choisi de voir le Highscore du jeu")
        show_highscore()
    case 3: 
        print(f"Vous avez choisi de voir le top 3 des meilleurs joueurs")
        show_three_highest_score()
    case 4:
        print(f"Vous avez choisi de quitter le jeu")
    case _:
        print(f"Veuillez entrer un nombre entier de 1 à 3 dans votre input")

