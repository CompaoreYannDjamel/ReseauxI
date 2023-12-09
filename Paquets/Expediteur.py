from Outils.GestionnaireFichier import ecrire, tronquer

class Expediteur:
    def __init__(self, fichier, addr_source, addr_destination):
        self.num_connexion = '11111111'
        if(len(self.num_connexion) != 8):
            raise ValueError("Numéro de connexion incorrecte (Pas 8 bits)")

        if(len(addr_source) != 8):
            raise ValueError("Adresse source incorrecte (Pas 8 bits)")
        self.addr_source = addr_source

        if(len(addr_destination) != 8):
            raise ValueError("Adresse destination incorrecte (Pas 8 bits)")
        self.addr_destination = addr_destination

        self.fichier = fichier



    def envoyer_paquet_appel(self):
        type = '00001011'
        paquet = self.num_connexion+type+ self.addr_source+ self.addr_destination
        ecrire(self.fichier, paquet)
        return paquet

    def envoyer_paquet_communication_etablie(self):
        type = '00001111'
        paquet = self.num_connexion+type+self.addr_source+self.addr_destination
        ecrire(self.fichier, paquet)
        return paquet



    def envoyer_paquet_liberation_distant(self):
        type = '00010011'
        raison = '00000001'
        paquet = self.num_connexion+type+self.addr_source+self.addr_destination+raison
        ecrire(self.fichier, paquet)
        return paquet

    def envoyer_paquet_liberation_fournisseur(self):
        type = '00010011'
        raison = '00000010'
        paquet = self.num_connexion+type+self.addr_source+self.addr_destination+raison
        ecrire(self.fichier, paquet)
        return paquet

    def envoyer_paquet_demande_liberation(self):
        type = '00010011'
        paquet = self.num_connexion+type+self.addr_source+self.addr_destination
        ecrire(self.fichier, paquet)
        return paquet

    def envoyer_paquet_donnees(self, pr, m, ps, donnees):
        type = pr+m+ps+'0'
        paquet = self.num_connexion+type+donnees
        ecrire(self.fichier, paquet)
        return paquet

    def effacer_fichier(self):
        tronquer(self.fichier)

    def obtenir_num_connexion(self):
        return self.num_connexion


    def envoyer_paquet_acquittement(self, pr, positif):
        if(len(pr) != 3):
            raise ValueError("p(r) (Pas 3 bits)")

        if(positif is True):
            queue = '00001'
        elif(positif is False):
            queue = '01001'
        else:
            raise ValueError("Acquittement est positif ou négatif non trouvé")

        paquet = self.num_connexion+pr+queue
        ecrire(self.fichier, paquet)
        return paquet