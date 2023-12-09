import math

def chaine_vers_binaire(chaine):
    l, m = [], []
    for i in chaine:
        l.append(ord(i))
    for i in l:
        x = f"{int(bin(i)[2:])}"
        for y in range(len(x), 8):
            x = '0' + x
        m.append(x)
    return m

def binaire_vers_chaine(binaire):
    l = []
    m = ""
    for i in binaire:
        i = int(i)
        b = 0
        c = 0
        k = int(math.log10(i)) + 1
        for j in range(k):
            b = ((i % 10) * (2 ** j))
            i = i // 10
            c = c + b
        l.append(c)
    for x in l:
        m = m + chr(x)
    return m

def diviser_binaire(donnees):
    sortie = [donnees[i:i + 8] for i in range(0, len(donnees), 8)]
    return sortie

def entier_vers_binaire_3bits(entier):
    b = f"{bin(entier)[2:]}"
    for x in range(len(b), 3):
        b = '0' + b
    return b

def liste_vers_chaine(donnees):
    chaine = ''
    for x in range(0, len(donnees)):
        chaine += f"{donnees[x]}"
    return chaine

def chaine_binaire_vers_entier(chaine):
    return int(chaine, 2)

def entier_vers_binaire_8bits(entier):
    b = f"{bin(entier)[2:]}"
    for x in range(len(b), 8):
        b = '0' + b
    return b
