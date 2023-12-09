from Paquets.Lecteur import Lecteur
from Paquets.Expediteur import Expediteur
from Outils.Utilitaires import chaine_binaire_vers_entier, binaire_vers_chaine, entier_vers_binaire_3bits
from Outils.GestionnaireFichier import vider
import time, random

lecteur = Lecteur("fichiers/L_ecr")  # Expediteur(addr_source, addr_destination)

while (True):
    donnees = []
    journal = []
    paquet = lecteur.lirePaquet()
    paquet_precedent = []
    if (len(paquet) > 0):  # Si un paquet est lu
        expediteur = Expediteur("fichiers/L_lec", paquet[3], paquet[2])
        addr_emetteur = chaine_binaire_vers_entier(paquet[2])
        addr_recepteur = chaine_binaire_vers_entier(paquet[3])

        # TODO Conditions sur l'adresse de l'appelant
        if (addr_emetteur % 19 == 0):
            info = f"Pas de réponse car adresse source % 19"
            journal.append(info)
            print(info)
            vider("fichiers/S_lec", journal)
        elif (addr_emetteur % 13 == 0):
            info = f"Refus de connexion car adresse distante % 13"
            journal.append(info)
            print(info)
            vider("fichiers/S_lec", journal)
            expediteur.envoyer_paquet_liberation_distant()
            time.sleep(2)
            expediteur.effacer_fichier()
        elif (addr_emetteur % 27 == 0):
            info = f"Refus de connexion car adresse distante % 27"
            journal.append(info)
            print(info)
            vider("fichiers/S_lec", journal)
            expediteur.envoyer_paquet_liberation_fournisseur()
            time.sleep(2)
            expediteur.effacer_fichier()
        elif (paquet[1] == '00001011'):  # Paquet Appel
            expediteur.envoyer_paquet_communication_etablie()
            info = "Paquet d'appel reçu, envoi de communication établie"
            journal.append(info)
            print(info)

            paquet_precedent = paquet
            communication = True

            while (communication):
                time.sleep(1)
                paquet = lecteur.lirePaquet()
                info = f"\nPaquet reçu: {paquet}"
                journal.append(info)
                print(info)

                if (paquet != paquet_precedent):
                    if (paquet[1] == '00010011'):  # Demande Libération
                        communication = False
                    elif (addr_emetteur % 15 == 0):
                        info = f"Pas d'acquittement car adresse source % 15"
                        journal.append(info)
                        print(info)
                        break
                    else:  # Données
                        alea = random.randint(0, 7)
                        alea = entier_vers_binaire_3bits(alea)

                        info = f"\nalea: {alea}\np(s):{paquet[1][4:7]}"
                        journal.append(info)
                        print(info)
                        if (paquet[1][4:7] == alea):
                            info = f"Acquittement négatif"
                            journal.append(info)
                            print(info)
                            expediteur.envoyer_paquet_acquittement(paquet[1][:3], False)
                        else:
                            donnees.append(paquet[2:])
                            paquet_precedent = paquet
                            expediteur.envoyer_paquet_acquittement(paquet[1][:3], True)

                    if (not communication):
                        chaine = ""
                        for x in range(0, len(donnees)):
                            chaine += binaire_vers_chaine(donnees[x])
                        info = f"Données: {chaine}"
                        journal.append(info)
                        print(info)
                        vider("fichiers/S_lec", journal)
                        expediteur.effacer_fichier()

                    time.sleep(3)

