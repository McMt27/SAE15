import markdown

def md_to_html(fichier_markdown :str, fichier_html: str) -> None:

    with open (fichier_markdown, "r", encoding="UTF-8") as f :
        txt = f.read()

    html = markdown.markdown(txt)

    with open(fichier_html, "w", encoding="UTF-8") as g:
        g.write(html)

