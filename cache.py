import json
import os
import requests

def download(url: str, cache: str) -> dict: 
    """Télécharge les données JSON depuis une URL et les sauvegarde dans un fichier spécifique."""


    response = requests.get(url)
    json_data = response.json()

    # Écrit les données dans le fichier cache
    with open(cache, "w") as f:
        json.dump(json_data, f)

    return json_data  

def download_poke_cached(id: int) -> dict:
    """Télécharge les données d'un Pokémon ou utilise le cache si disponible."""
    if not os.path.isdir("cache"):
        os.mkdir("cache")

    cache_file = f"cache/{id}.json"

    # Vérifie si le fichier existe déjà dans le cache
    if os.path.isfile(cache_file) == True:
        with open(cache_file, "r") as f:
            return json.load(f)

    url = f"https://pokeapi.co/api/v2/pokemon/{id}/"
    return download(url, cache_file) 

def download_pokemons(debut: int, fin:int):
    """Télécharge les données des n premiers Pokémon et les sauvegarde en fichiers JSON."""
    """Ne pas mettre 0 pour la valeur du début car il n'y aucun pokemon avec cette id"""

    os.mkdir("cache")
    for i in range(debut, fin+1):
        cache_file = f"cache/{i}.json"

        # Si le fichier n'existe pas déjà, on le crée.
        if os.path.isfile(cache_file) == False:

            response = requests.get(f"https://pokeapi.co/api/v2/pokemon/{i}/")
            with open(cache_file, "w") as f:
                json.dump(response.json(), f)