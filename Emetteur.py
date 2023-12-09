from Outils.Utilitaires import chaine_vers_binaire, entier_vers_binaire_3bits, liste_vers_chaine, entier_vers_binaire_8bits
from Outils.GestionnaireFichier import vider
from Paquets.Expediteur import Expediteur
from Paquets.Lecteur import Lecteur
import time, random

#S_lec : Ce fichier est utilisé pour stocker les journaux (logs) des événements qui se produisent
# lors de la réception des paquets. Les journaux sont enregistrés ici pour les analyser ultérieurement.

#L_ecr : Ce fichier est utilisé par l'expéditeur pour écrire les paquets de données qui doivent être envoyés
#L'expéditeur y écrit les paquets, et le lecteur les lit depuis ce fichier.

#L_lec : Ce fichier est utilisé par le lecteur pour lire les paquets de données envoyés par l'expéditeur.
# Le lecteur lit les paquets depuis ce fichier, et l'expéditeur y écrit les paquets.

#S_ecr : Ce fichier est utilisé pour stocker les journaux (logs) des événements qui se produisent lors de l'émission des paquets.
#Les journaux sont enregistrés ici pour les analyser ultérieurement.
def segmenterDonnees(donnees):
    binaire = chaine_vers_binaire(donnees)

    segmentation = True
    contenu = []
    pr = []
    ps = []
    m = []

    compteur = 0
    while (segmentation):
        contenu.append(liste_vers_chaine(binaire[0:16]))  # Découpe 128 octets
        del binaire[0:16]  # Supprime 128 octets
        a = entier_vers_binaire_3bits(compteur % 8)
        if (len(binaire) == 0):  # Si dernier segment
            segmentation = False
            pr.append(entier_vers_binaire_3bits(0 % 8))
            m.append('0')  # Dernière partie
        else:  # A d'autres parties
            pr.append(entier_vers_binaire_3bits(compteur + 1 % 8))
            m.append('1')  # a d'autres parties
            compteur += 1
        ps.append(a)
    return ps, m, pr, contenu

temps_attente = 5
journal = []

addresse_emetteur = entier_vers_binaire_8bits(random.randint(0, 254))#Compris entre 0 et 254

addresse_recepteur = entier_vers_binaire_8bits(random.randint(0, 254))#Compris entre 0 et 254

#addresse_emetteur = entier_vers_binaire_8bits(19)#Compris entre 0 et 254

#addresse_recepteur = entier_vers_binaire_8bits(19)#Compris entre 0 et 254


info = f"addresse_emetteur: {addresse_emetteur}\naddresse_recepteur: {addresse_recepteur}"
journal.append(info)
print(info)

message = "Bon mois de Ramadan a tous"

expediteur = Expediteur("fichiers/L_ecr", addresse_emetteur, addresse_recepteur)
lecteur = Lecteur("fichiers/L_lec")

emission = False

expediteur.envoyer_paquet_appel()
time.sleep(1)

x = 0
while (x < temps_attente):
    time.sleep(1)
    paquet = lecteur.lirePaquet()
    if (len(paquet) > 0):  # Quelque chose à lire
        if (paquet[1] == '00001111'):  # Si paquet == communication établie
            if (paquet[0] != expediteur.obtenir_num_connexion()):
                info = f"numéro de connexion incorrect, abandon"
                journal.append(info)
                print(info)
                break
            elif (paquet[2] != addresse_recepteur):
                info = f"adresse source incorrecte, abandon"
                journal.append(info)
                print(info)
                break
            elif (paquet[3] != addresse_emetteur):
                info = f"adresse destination incorrecte, abandon"
                journal.append(info)
                print(info)
                break
            else:
                info = f"Communication établie, début d'émission"
                journal.append(info)
                print(info)
                emission = True
                x = temps_attente
        elif (paquet[1] == '00010011'):
            if (paquet[4] == '00000001'):
                info = f"Connexion refusée par le distant"
                journal.append(info)
                print(info)
                break
            elif (paquet[4] == '00010011'):
                info = f"Connexion refusée par le fournisseur"
                journal.append(info)
                print(info)
                break
        else:
            x += 1

        if (not emission):
            info = f"La connexion n'a pas pu être établie"
            journal.append(info)
            print(info)
        else:
            info = f"Émission de données"
            journal.append(info)
            print(info)
            segments = segmenterDonnees(message)
            ps = segments[0]
            m = segments[1]
            pr = segments[2]
            contenu = segments[3]

            for i in range(0, len(contenu)):
                if (emission):
                    acquittement = False
                    tentatives = 0
                    while (tentatives < 2):
                        expediteur.envoyer_paquet_donnees(ps[i], m[i], pr[i], contenu[i])
                        info = f"Envoi du paquet {i + 1} sur {len(contenu)}"
                        journal.append(info)
                        print(info)
                        paquet_precedent = paquet

                        x = 0
                        while (x < temps_attente):
                            paquet = lecteur.lirePaquet()
                            if (paquet != paquet_precedent):
                                if (paquet[0] != expediteur.obtenir_num_connexion()):
                                    info = f"Mauvais numéro de connexion, abandon"
                                    journal.append(info)
                                    print(info)
                                    emission = False
                                elif (paquet[1][:3] != ps[i]):
                                    info = f"p(s) '{paquet[1][:3]}' reçu, attendu: {ps[i]}, abandon"
                                    journal.append(info)
                                    print(info)
                                    emission = False
                                elif (paquet[1][3:] == '01001'):  # Acquittement négatif
                                    info = f"{tentatives + 1} Paquet acquittement négatif reçu"
                                    journal.append(info)
                                    print(info)
                                    x = temps_attente
                                elif (paquet[1][3:] == '00001'):  # Acquittement positif
                                    acquittement = True
                                    x = temps_attente
                            x += 1
                            time.sleep(1)
                        if (x == temps_attente):
                            info = f"Demande d'ACK en attente."
                            journal.append(info)
                            print(info)

                        if (acquittement == False):  # Pas de réponse
                            tentatives += 1
                        else:  # Réponse reçue
                            tentatives = 2

                    if (acquittement == False):  # Problème de communication
                        info = f"Échec de la communication"
                        journal.append(info)
                        print(info)
                        emission = False

            if (emission):
                expediteur.envoyer_paquet_demande_liberation()
                time.sleep(3)

        vider("fichiers/S_ecr", journal)
        expediteur.effacer_fichier()
