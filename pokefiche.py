import markdown
import requests 

def download_poke(id:int) :

    link = f"https://pokeapi.co/api/v2/pokemon/{id}"
    response = requests.get(link)
    json_data = response.json()
    return json_data

def generer_html_contenu(titre, contenu):
    return f"""<!DOCTYPE html>
<html lang="fr">
<head>
    <meta charset="UTF-8" />

    <meta name="viewport" content="width=device-width, initial-scale=1.0" />

    <title>Location BMW</title>

    <link rel="stylesheet" type="text/css" href="styles.css" />

    <script src="https://kit.fontawesome.com/5f54a5c31c.js" crossorigin="anonymous"></script>
    
    <link rel="preconnect" href="https://fonts.googleapis.com" />
    <link rel="preconnect" href="https://fonts.gstatic.com" crossorigin />
    <link
        href="https://fonts.googleapis.com/css2?family=Kode+Mono:wght@400..700&family=Orbitron:wght@400..900&display=swap"
        rel="stylesheet">

    <link
        href="https://fonts.googleapis.com/css2?family=Audiowide&family=Titillium+Web:ital,wght@0,200;0,300;0,400;0,600;0,700;0,900;1,200;1,300;1,400;1,600;1,700&display=swap"
        rel="stylesheet">

    <link
        href="https://fonts.googleapis.com/css2?family=Audiowide&family=Rajdhani:wght@300;400;500;600;700&family=Titillium+Web:ital,wght@0,200;0,300;0,400;0,600;0,700;0,900;1,200;1,300;1,400;1,600;1,700&display=swap"
        rel="stylesheet">
</head>
<body>
    {contenu}
</body>
</html>
"""

def pokefiche(id: int):
    data = download_poke(id)
    if data is None:
        return

    # Construire le contenu HTML
    sprite = data["sprites"]["front_default"]
    name = data["name"]
    height = data["height"]
    weight = data["weight"]
    types = data["types"]
    str_type = ""
    if len(types) > 1:
        for i in range(len(types)):
            str_type += types[i]["type"]["name"] + " "
    else:
        str_type += types[0]["type"]["name"] + " "

    # Section corrigée pour les statistiques
    stats = data["stats"]
    stats_html = ""
    for stat in stats:
        stat_name = stat["stat"]["name"]
        base_stat = stat["base_stat"]
        stats_html += f"<p>{stat_name} : {base_stat}</p>"

    contenu = f"""
    <h1>Résultats</h1>
    <img src="{sprite}" alt="{name}">
    <p>Nom : {name}</p>
    <p>Taille : {height}</p>
    <p>Poids : {weight}</p>
    <p>Type : {str_type}</p>
    {stats_html}
    """

    # Sauvegarder dans un fichier HTML
    with open("resultats.html", "w", encoding="UTF-8") as f:
        f.write(generer_html_contenu("Pokémon Fiche", contenu))

def md_to_html(fichier_markdown :str, fichier_html: str) -> None:

    with open (fichier_markdown, "r", encoding="UTF-8") as f :
        txt = f.read()

    html = markdown.markdown(txt)

    with open(fichier_html, "w", encoding="UTF-8") as g:
        g.write(html)

