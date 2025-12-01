# win.py
# Gestion de la condition de victoire du jeu

def game_won(game):
    player = game.player

    print("\n" + "=" * 50)
    print("🎉 VICTOIRE ! 🎉")
    print("=" * 50 + "\n")

    print(
        f"{player.name}, grâce à toi, la Corruption qui rongeait Brumeval "
        "a été purifiée.\n"
        "La graine sacrée a rendu vie à l'Arbre-Source, la brume se dissipe, "
        "et la forêt retrouve peu à peu ses couleurs.\n"
    )

    print(
        "Les habitants pourront revenir au village, les chemins seront à nouveau sûrs, "
        "et les histoires de ton courage seront racontées pendant des générations.\n"
    )

    print("Merci d'avoir joué à cette aventure.\n")

    game.finished = True