from importes import Fichier
from outils import Outils
from traitement import Rabais


class Reservation(Fichier):
    """
    Classe pour l'importation des données de Réservations
    """

    cles = ['annee', 'mois', 'id_compte', 'intitule_compte', 'code_client', 'abrev_labo', 'id_user', 'nom_user',
            'prenom_user', 'num_projet', 'intitule_projet', 'id_machine', 'nom_machine', 'date_debut', 'duree_hp',
            'duree_hc', 'si_supprime', 'duree_ouvree', 'date_reservation', 'date_suppression']
    nom_fichier = "res.csv"
    libelle = "Réservation Equipement"

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.comptes = {}

    def obtenir_comptes(self):
        """
        retourne la liste de tous les comptes clients
        :return: liste des comptes clients présents dans les données réservations importées
        """
        if self.verifie_coherence == 0:
            info = self.libelle + ". vous devez vérifier la cohérence avant de pouvoir obtenir les comptes"
            print(info)
            Outils.affiche_message(info)
            return []
        return self.comptes

    def est_coherent(self, comptes, machines):
        """
        vérifie que les données du fichier importé sont cohérentes (id compte parmi comptes,
        id machine parmi machines), et efface les colonnes mois et année
        :param comptes: comptes importés
        :param machines: machines importées
        :return: 1 s'il y a une erreur, 0 sinon
        """
        if self.verifie_date == 0:
            info = self.libelle + ". vous devez vérifier la date avant de vérifier la cohérence"
            print(info)
            Outils.affiche_message(info)
            return 1

        if self.verifie_coherence == 1:
            print(self.libelle + ": cohérence déjà vérifiée")
            return 0

        msg = ""
        ligne = 1
        donnees_list = []

        for donnee in self.donnees:
            if donnee['id_compte'] == "":
                msg += "le compte id de la ligne " + str(ligne) + " ne peut être vide\n"
            elif comptes.contient_id(donnee['id_compte']) == 0:
                msg += "le compte id '" + donnee['id_compte'] + "' de la ligne " + str(ligne) + " n'est pas référencé\n"
            elif donnee['code_client'] not in self.comptes:
                self.comptes[donnee['code_client']] = [donnee['id_compte']]
            elif donnee['id_compte'] not in self.comptes[donnee['code_client']]:
                self.comptes[donnee['code_client']].append(donnee['id_compte'])

            if donnee['id_machine'] == "":
                msg += "le machine id de la ligne " + str(ligne) + " ne peut être vide\n"
            elif machines.contient_id(donnee['id_machine']) == 0:
                msg += "le machine id '" + donnee['id_machine'] + "' de la ligne " + str(ligne) \
                       + " n'est pas référencé\n"

            donnee['duree_hp'], info = Outils.est_un_nombre(donnee['duree_hp'], "la durée réservée HP", ligne)
            msg += info
            donnee['duree_hc'], info = Outils.est_un_nombre(donnee['duree_hc'], "la durée réservée HC", ligne)
            msg += info
            donnee['duree_ouvree'], info = Outils.est_un_nombre(donnee['duree_ouvree'], "la durée ouvrée", ligne)
            msg += info

            del donnee['annee']
            del donnee['mois']
            donnees_list.append(donnee)

            ligne += 1

        self.donnees = donnees_list
        self.verifie_coherence = 1

        if msg != "":
            msg = self.libelle + "\n" + msg
            print("msg : " + msg)
            Outils.affiche_message(msg)
            return 1
        return 0

    def calcul_montants(self, machines, coefmachines, comptes, clients, verification):
        """
        calcule les montants 'pv' et 'qv' et les ajoute aux données
        :param machines: machines importées et vérifiées
        :param coefmachines: coefficients machines importés et vérifiés
        :param comptes: comptes importés et vérifiés
        :param clients: clients importés et vérifiés
        :param verification: pour vérifier si les dates et les cohérences sont correctes
        """
        if verification.a_verifier != 0:
            info = self.libelle + ". vous devez faire les vérifications avant de calculer les montants"
            print(info)
            Outils.affiche_message(info)
            return

        donnees_list = []
        for donnee in self.donnees:
            compte = comptes.donnees[donnee['id_compte']]
            machine = machines.donnees[donnee['id_machine']]
            client = clients.donnees[compte['code_client']]
            coefmachine = coefmachines.donnees[client['id_classe_tarif'] + machine['categorie']]
            duree_fact_hp, duree_fact_hc = Rabais.rabais_reservation(machine['delai_sans_frais'],
                                                                     donnee['duree_ouvree'],
                                                                     donnee['duree_hp'],
                                                                     donnee['duree_hc'])

            donnee['pv'] = round(duree_fact_hp / 60 * round(machine['t_h_reservation_hp_p'] *
                                                            coefmachine['coef_p'], 2) + duree_fact_hc / 60 *
                                 round(machine['t_h_reservation_hc_p'] * coefmachine['coef_p']), 2)

            donnee['qv'] = round(duree_fact_hp / 60 * round(machine['t_h_reservation_hp_np'] *
                                                            coefmachine['coef_np'], 2) + duree_fact_hc / 60 *
                                 round(machine['t_h_reservation_hc_np'] * coefmachine['coef_np']), 2)

            donnee['duree_fact_hp'] = duree_fact_hp
            donnee['duree_fact_hc'] = duree_fact_hc
            donnees_list.append(donnee)
        self.donnees = donnees_list

    def reservations_pour_projet(self, num_projet, id_compte, code_client):
        """
        retourne toutes les données réservations pour un projet donné
        :param num_projet: le numéro du projet
        :param id_compte: l'id du compte
        :param code_client: le code du client
        :return: toutes les données réservations le un projet donné
        """
        donnees_list = []
        for donnee in self.donnees:
            if (donnee['id_compte'] == id_compte) and (donnee['code_client'] == code_client) \
                    and (donnee['num_projet'] == num_projet):
                donnees_list.append(donnee)
        return donnees_list
