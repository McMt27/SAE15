import os
import json
import requests
import matplotlib.pyplot as plt
import webbrowser

# ================================================
# 1. GESTION DU CACHE
# ================================================

def telecharger_avec_cache(url: str, chemin_cache: str) -> dict:
    """
    Télécharge les données JSON depuis une URL ou utilise un fichier cache.
    Si le fichier cache existe, il est utilisé. Sinon, une requête est effectuée.
    """
    if os.path.exists(chemin_cache):
        with open(chemin_cache, "r") as fichier:
            return json.load(fichier)
    
    response = requests.get(url)
    donnees = response.json()
    with open(chemin_cache, "w") as fichier:
        json.dump(donnees, fichier)
    return donnees

# ================================================
# 2. RÉCUPÉRATION DES DONNÉES D'UN POKÉMON
# ================================================

def recuperer_donnees_pokemon(id_ou_nom: str) -> dict:
    """
    Récupère les données d'un Pokémon avec gestion du cache.
    """
    if not os.path.exists("cache"):
        os.mkdir("cache")
    chemin_cache = f"cache/{id_ou_nom}.json"
    url = f"https://pokeapi.co/api/v2/pokemon/{id_ou_nom}/"
    return telecharger_avec_cache(url, chemin_cache)

# ================================================
# 3. RÉCUPÉRATION DU NOM EN FRANÇAIS D'UN POKÉMON
# ================================================

def nom_pokemon_en_francais(url_espece: str) -> str:
    """
    Récupère le nom en français d'un Pokémon à partir de l'URL de son espèce.
    """
    chemin_cache = f"cache/espece_{url_espece.split('/')[-2]}.json"
    donnees_espece = telecharger_avec_cache(url_espece, chemin_cache)

    if donnees_espece:
        for name_entry in donnees_espece["names"]:
            if name_entry["language"]["name"] == "fr":
                return name_entry["name"]
    return "Nom non disponible"

# ================================================
# 4. CLASSEMENT DES TYPES DE POKÉMON
# ================================================

def classer_types(pokemons: list) -> dict:
    """
    Classe les types de Pokémon par fréquence.
    """

    types_count = {}
    for pokemon in pokemons:
        for t in pokemon["types"]:
            type_name = t["type"]["name"]
            if type_name in types_count:
                types_count[type_name] += 1
            else:
                types_count[type_name] = 1


    types_list = []
    for type_name, count in types_count.items():
        types_list.append((type_name, count))


    for i in range(len(types_list)):

        max_index = i
        for j in range(i + 1, len(types_list)):
            if types_list[j][1] > types_list[max_index][1]: 
                max_index = j

        if max_index != i:
            types_list[i], types_list[max_index] = types_list[max_index], types_list[i]

    types_dict = {}
    for type_name, count in types_list:
        types_dict[type_name] = count


    return types_dict


# ================================================
# 5. GÉNÉRATION DE LA CARTE HTML D'UN POKÉMON
# ================================================

def generer_carte_pokemon(pokemon: dict, nom_francais: str):
    """Génère une carte HTML pour un Pokémon avec des reflets et un design moderne."""

    sprite = pokemon["sprites"]["front_default"]
    types = [] 
    for t in pokemon["types"]: 
        type_name = t["type"]["name"]
        types.append(type_name)
    stats = {}
    for stat in pokemon["stats"]:
        stat_name = stat["stat"]["name"] 
        base_stat = stat["base_stat"] 
        stats[stat_name] = base_stat


    # Couleurs des types
    type_colors = {
        "normal": "#A8A878", "fire": "#F08030", "water": "#6890F0",
        "electric": "#F8D030", "grass": "#78C850", "ice": "#98D8D8",
        "fighting": "#C03028", "poison": "#A040A0", "ground": "#E0C068",
        "flying": "#A890F0", "psychic": "#F85888", "bug": "#A8B820",
        "rock": "#B8A038", "ghost": "#705898", "dragon": "#7038F8",
        "dark": "#705848", "steel": "#B8B8D0", "fairy": "#EE99AC",
    }

    # Choisir la couleur du fond en fonction du type principal (ou premier type)
    type_couleur = type_colors.get(types[0], "#A8A878")  # Défaut : couleur normale si type non défini

    # Génération HTML
    html_content = f"""
    <html>
    <head>
        <style>
            body {{
                font-family: 'Arial', sans-serif;
                background-color: #2d2d44;
                color: white;
                margin: 0;
                padding: 0;
                display: flex;
                justify-content: center;
                align-items: center;
                height: 100vh;
            }}

            .card {{
                max-width: 400px;
                width: 100%;
                padding: 20px;
                background: {type_couleur};
                border-radius: 20px;
                box-shadow: 0 10px 20px rgba(0, 0, 0, 0.5);
                overflow: hidden;
                position: relative;
                transform: translateY(-10px);
                transition: transform 0.3s ease-in-out;
            }}

            .card:hover {{
                transform: translateY(-20px);
            }}

            .header {{
                text-align: center;
                position: relative;
            }}

            .header img {{
                width: 150px;
                height: 150px;
                border-radius: 50%;
                border: 4px solid #fff;
                box-shadow: 0 5px 10px rgba(0, 0, 0, 0.5);
                margin-bottom: 15px;
            }}

            .header h1 {{
                font-size: 2rem;
                color: #fff;
                text-shadow: 2px 2px 4px rgba(0, 0, 0, 0.6);
                margin: 0;
            }}

            .types {{
                margin: 10px 0;
                display: flex;
                justify-content: center;
                flex-wrap: wrap;
            }}

            .type {{
                display: inline-block;
                margin: 5px;
                padding: 8px 15px;
                border-radius: 15px;
                font-weight: bold;
                text-transform: capitalize;
                color: #fff;
                box-shadow: 0 3px 6px rgba(0, 0, 0, 0.3);
            }}

            .types span {{
                animation: pulse 1.5s infinite ease-in-out;
            }}

            .stats {{
                margin-top: 20px;
                font-size: 1.1rem;
            }}

            .stats h3 {{
                text-align: center;
                font-size: 1.5rem;
                margin-bottom: 10px;
                text-transform: uppercase;
                letter-spacing: 1px;
                font-weight: 600;
            }}

            table {{
                width: 100%;
                border-collapse: collapse;
            }}

            th, td {{
                padding: 8px;
                text-align: center;
                border: 1px solid #ccc;
                background-color: rgba(255, 255, 255, 0.1);
            }}

            th {{
                background-color: rgba(0, 0, 0, 0.4);
                font-size: 1.2rem;
            }}

            tr:nth-child(even) {{
                background-color: rgba(0, 0, 0, 0.2);
            }}

            tr:hover {{
                background-color: #555;
            }}

            @keyframes pulse {{
                0% {{
                    transform: scale(1);
                    opacity: 1;
                }}
                50% {{
                    transform: scale(1.1);
                    opacity: 0.8;
                }}
                100% {{
                    transform: scale(1);
                    opacity: 1;
                }}
            }}

        </style>
    </head>
    <body>
        <div class="card">
            <div class="header">
                <img src="{sprite}" alt="{nom_francais}">
                <h1>{nom_francais}</h1>
                <div class="types">
    """

    for type_pokemon in types:
        html_content += f'<span class="type type-{type_pokemon}">{type_pokemon}</span>'

    html_content += "</div></div><div class='stats'><h3>Statistiques</h3><table><tr><th>Statistique</th><th>Valeur</th></tr>"

    for stat, value in stats.items():
        html_content += f"<tr><td>{stat}</td><td>{value}</td></tr>"

    # Sauvegarde et ouverture
    chemin_fichier = "carte_pokemon_reflet.html"
    with open(chemin_fichier, "w", encoding="utf-8") as fichier:
        fichier.write(html_content)
    print(f"Carte générée : {chemin_fichier}")
    webbrowser.open(chemin_fichier)


def generer_dataset_to_md(pokemons: list):
    """Génère un fichier dataset_to_md avec les informations de chaque Pokémon."""
    with open("dataset_to_md.md", "w", encoding="utf-8") as fichier:
        fichier.write("# Dataset des Pokémon\n\n")
        for pokemon in pokemons:
            nom_francais = nom_pokemon_en_francais(pokemon["species"]["url"])
            types = ""
            for t in pokemon["types"]:
                types += t["type"]["name"] + ", "
            types = types(", ")
            stats = ""
            for stat in pokemon["stats"]:
                stats += f"{stat['stat']['name']}: {stat['base_stat']}, "
            stats = stats(", ")
            fichier.write(f"## {nom_francais}\n")
            fichier.write(f"Type(s): {types}\n")
            fichier.write(f"Stats: {stats}\n\n")
    print("Fichier dataset_to_md.md généré.")

def generer_infos_locales(pokemons: list):
    """Génère un fichier infos_locales.txt avec les informations sur les Pokémon."""
    with open("infos_locales.txt", "w", encoding="utf-8") as fichier:
        for pokemon in pokemons:
            nom_francais = nom_pokemon_en_francais(pokemon["species"]["url"])
            types = ""
            for t in pokemon["types"]:
                types += t["type"]["name"] + ", "
            types = types(", ") 
            fichier.write(f"{nom_francais} - Types: {types}\n")
    print("Fichier infos_locales.txt généré.")


# ================================================
# 6. RÉCUPÉRATION D'UNE PLAGE D'ID DE POKÉMON
# ================================================

def recuperer_pokemons_plage(debut: int, fin: int) -> list:
    """
    Récupère les données pour une plage d'IDs Pokémon (entre debut et fin).
    """
    pokemons = []
    for id_pokemon in range(debut, fin + 1):
        donnees = recuperer_donnees_pokemon(id_pokemon)
        if donnees:
            pokemons.append(donnees)
    return pokemons

# ================================================
# 7. CHOIX DE LA STATISTIQUE À TRIER
# ================================================

def choisir_statistique():
    """Permet à l'utilisateur de choisir la statistique à trier."""
    print("\nChoisissez la statistique à trier par :")
    print("1 - HP")
    print("2 - Attaque")
    print("3 - Défense")
    print("4 - Vitesse")
    print("5 - Sp. Atk")
    print("6 - Sp. Def")
    
    choix = input("Entrez le numéro correspondant à la statistique : ").strip()

    for char in choix:
        if char < '0' or char > '9':
            print("Erreur : veuillez entrer un nombre valide.")
            return None

    return int(choix)



# ================================================
# 8. TRIER PAR LA STATISTIQUE CHOISIE
# ================================================
def obtenir_base_stat(pokemon, statistique_choisie):
    """
    Récupère la valeur de la statistique choisie pour un Pokémon.
    """
    for stat in pokemon["stats"]:
        if stat["stat"]["name"] == statistique_choisie:
            return stat["base_stat"]
    return 0 


def trier_par_statistique(pokemons: list, choix: int) -> dict:
    """
    Trie les Pokémon par la statistique choisie.
    """

    statistiques = ["hp", "attack", "defense", "speed", "special-attack", "special-defense"]
    
    if choix < 1 or choix > 6:
        print("Choix invalide.")
        return None

    statistique_choisie = statistiques[choix - 1]

    pokemon_max_stat = None
    max_stat_value = -1  

    for pokemon in pokemons:
        # Obtenir la valeur de la statistique choisie
        base_stat = obtenir_base_stat(pokemon, statistique_choisie)
        
        # Comparer et mettre à jour si la statistique est la plus haute
        if base_stat > max_stat_value:
            max_stat_value = base_stat
            pokemon_max_stat = pokemon

    return pokemon_max_stat

# ================================================
# 9. Graphique
# ================================================

def generer_graphique_statistiques(noms_pokemons: list):
    """Génère un graphique comparatif des statistiques des Pokémon."""
    stats_pokemons = {}

    for nom in noms_pokemons:
        nom = nom
        donnees = recuperer_donnees_pokemon(nom) 

        if donnees:
            stats = {}
            for stat in donnees["stats"]:
                stats[stat["stat"]["name"]] = stat["base_stat"]
            

            nom_francais = nom_pokemon_en_francais(donnees["species"]["url"])
            

            stats_pokemons[nom_francais] = stats

    if stats_pokemons:
        noms_stats = list(next(iter(stats_pokemons.values())).keys())

    x = range(len(noms_stats)) 
    largeur = 0.8 / len(stats_pokemons)

    # Création du graphique
    fig, ax = plt.subplots(figsize=(10, 6))
    for i, (nom, stats) in enumerate(stats_pokemons.items()):

        valeurs = []
        for stat in noms_stats:
            valeurs.append(stats.get(stat, 0))  

        positions = [p + i * largeur for p in x]

        ax.bar(positions, valeurs, largeur, label=nom)

    positions_x = [p + largeur * (len(stats_pokemons) - 1) / 2 for p in x]
    ax.set_xticks(positions_x)
    ax.set_xticklabels(noms_stats, rotation=45, ha="right")

    ax.set_xlabel("Statistiques")
    ax.set_ylabel("Valeurs")
    ax.legend()

    plt.tight_layout()

    plt.show()


# ================================================
# 10. MAIN
# ================================================

if __name__ == "__main__":
    entree = input("Entrez les noms/IDs des Pokémon (séparés par des virgules ',') ou une plage avec un tiret '-' : ")

    if "," in entree:
        noms_separes = entree.split(",")
    
        noms = []
        for nom in noms_separes:
            nom = nom 
            if nom:  
                noms.append(nom)

        if noms:
            generer_graphique_statistiques(noms)


    elif "-" in entree:
        # Mode plage d'IDs
        try:
            debut, fin = map(int, entree.split("-"))
            pokemons = recuperer_pokemons_plage(debut, fin)
        except ValueError:
            print("Erreur : veuillez entrer une plage valide au format 'début-fin' (ex : 1-10).")
            pokemons = []

        if pokemons:
            choix = choisir_statistique()
            pokemon_max_stat = trier_par_statistique(pokemons, choix)
            if pokemon_max_stat:
                nom_francais = nom_pokemon_en_francais(pokemon_max_stat["species"]["url"])
                print(f"\nLe Pokémon avec le plus de {choix} est : {nom_francais}")
                generer_carte_pokemon(pokemon_max_stat, nom_francais)


    else:
        print("Entrée invalide. Veuillez entrer des noms/IDs séparés par des virgules ',' ou une plage d'IDs avec un tiret '-'.")
