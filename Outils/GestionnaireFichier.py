def ecrire(fichier, contenu):
    fichier = open(fichier, "wb")
    fichier.write(bytes(contenu, encoding='utf8'))
    fichier.close()

def lire(fichier):
    fichier = open(fichier, "r")
    contenu = fichier.read()
    fichier.close()
    return contenu

def tronquer(fichier):
    fichier = open(fichier, "w+")
    fichier.truncate(0)
    fichier.close()

def vider(fichier, liste):
    fichier = open(fichier, "a+", encoding="utf-8")
    fichier.write("\n")
    for x in (0, len(liste)-1):
        fichier.write(f"{liste[x]}\n")
    fichier.close()
