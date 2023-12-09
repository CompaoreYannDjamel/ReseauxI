from Outils.GestionnaireFichier import lire
from Outils.Utilitaires import diviser_binaire

class Lecteur:
    def __init__(self, fichier):
        self.fichier = fichier

    def trouverTypePaquet(self, paquet):
        if (paquet[1][3:] == '01011'):  # Paquet d'appel
            print("Paquet d'appel")
            return ['0']
        elif (paquet[1][3:] == '01111'):  # Paquet communication établie
            print("Paquet communication établie")
            return ['1']
        elif (paquet[1][3:] == '10011'):  # Paquet libération
            if (paquet == '00000001'):  # Distant
                print("Paquet libération (distant)")
                return ['2']
            elif (paquet == '00000010'):  # Fournisseur
                print("Paquet libération (fournisseur)")
                return ['3']
            else:  # Demande libération
                print("Paquet demande libération")
                return ['4']
        elif (paquet[1][3:] == '00001'):  # Acquittement positif
            print("Paquet acquittement positif")
            return ['5']
        elif (paquet[1][3:] == '01001'):  # Acquittement négatif
            print("Paquet acquittement négatif")
            return ['6']
        else:  # Données
            pr = paquet[1][0:3]
            m = paquet[1][3:4]
            ps = paquet[1][4:7]
            print(f"Paquet données: p(r)={pr} m={m} p(s)={ps}")
            return ['7', paquet[2:]]

    def lirePaquet(self):
        contenu = lire(self.fichier)
        contenu = diviser_binaire(contenu)
        return contenu