from importes import Fichier
from outils import Outils


class Machine(Fichier):
    """
    Classe pour l'importation des données de Machines Cmi
    """

    cles = ['annee', 'mois', 'id_machine', 'nom', 'categorie', 't_h_machine_hp_p', 't_h_machine_hp_np',
            't_h_operateur_hp_mo', 't_h_reservation_hp_p', 't_h_reservation_hp_np', 't_h_machine_hc_p',
            't_h_machine_hc_np', 't_h_operateur_hc_mo', 't_h_reservation_hc_p', 't_h_reservation_hc_np',
            'delai_sans_frais']
    nom_fichier = "machine.csv"
    libelle = "Machines"

    def contient_id(self, id_machine):
        """
        vérifie si une machine contient l'id donné
        :param id_machine: id à vérifier
        :return: 1 si id contenu, 0 sinon
        """
        ligne = 1
        if self.verifie_coherence == 1:
            for cle, machine in self.donnees.items():
                if machine['id_machine'] == id_machine:
                    return ligne
                ligne += 1
        else:
            for machine in self.donnees:
                if machine['id_machine'] == id_machine:
                    return ligne
                ligne += 1
        return 0

    def est_coherent(self, coefmachines):
        """
        vérifie que les données du fichier importé sont cohérentes (id machine unique,
        catégorie machine référencé dans les coefficients machines), et efface les colonnes mois et année
        :param coefmachines: coefficients machines importés
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
        ids = []
        donnees_dict = {}

        for donnee in self.donnees:
            if donnee['id_machine'] == "":
                msg += "le machine id de la ligne " + str(ligne) + " ne peut être vide\n"
            elif donnee['id_machine'] not in ids:
                ids.append(donnee['id_machine'])
                del donnee['annee']
                del donnee['mois']
                donnees_dict[donnee['id_machine']] = donnee
            else:
                msg += "l'id machine '" + donnee['id_machine'] + "' de la ligne " + str(ligne) +\
                       " n'est pas unique\n"

            if donnee['categorie'] == "":
                msg += "la catégorie machine de la ligne " + str(ligne) + " ne peut être vide\n"
            elif coefmachines.contient_categorie(donnee['categorie']) == 0:
                msg += "la catégorie machine '" + donnee['categorie'] + "' de la ligne " + str(ligne) +\
                       " n'est pas référencée dans les coefficients\n"

            donnee['t_h_machine_hp_p'], info = Outils.est_un_nombre(donnee['t_h_machine_hp_p'], "le tarif machine HP P",
                                                                    ligne)
            msg += info
            donnee['t_h_machine_hp_np'], info = Outils.est_un_nombre(donnee['t_h_machine_hp_np'],
                                                                     "le tarif machine HP NP", ligne)
            msg += info
            donnee['t_h_operateur_hp_mo'], info = Outils.est_un_nombre(donnee['t_h_operateur_hp_mo'],
                                                                       "le tarif opérateur HP MO", ligne)
            msg += info
            donnee['t_h_reservation_hp_p'], info = Outils.est_un_nombre(donnee['t_h_reservation_hp_p'],
                                                                        "le tarif réservation HP P", ligne)
            msg += info
            donnee['t_h_reservation_hp_np'], info = Outils.est_un_nombre(donnee['t_h_reservation_hp_np'],
                                                                         "le tarif réservation HP NP", ligne)
            msg += info
            donnee['t_h_machine_hc_p'], info = Outils.est_un_nombre(donnee['t_h_machine_hc_p'], "le tarif machine HC P",
                                                                    ligne)
            msg += info
            donnee['t_h_machine_hc_np'], info = Outils.est_un_nombre(donnee['t_h_machine_hc_np'],
                                                                     "le tarif machine HC NP", ligne)
            msg += info
            donnee['t_h_operateur_hc_mo'], info = Outils.est_un_nombre(donnee['t_h_operateur_hc_mo'],
                                                                       "le tarif opérateur HC MO", ligne)
            msg += info
            donnee['t_h_reservation_hc_p'], info = Outils.est_un_nombre(donnee['t_h_reservation_hc_p'],
                                                                        "le tarif réservation HC P", ligne)
            msg += info
            donnee['t_h_reservation_hc_np'], info = Outils.est_un_nombre(donnee['t_h_reservation_hc_np'],
                                                                         "le tarif réservation HC NP", ligne)
            msg += info
            donnee['delai_sans_frais'], info = Outils.est_un_nombre(donnee['delai_sans_frais'], "le délai sans frais",
                                                                    ligne)
            msg += info

            ligne += 1

        self.donnees = donnees_dict
        self.verifie_coherence = 1

        if msg != "":
            msg = self.libelle + "\n" + msg
            print("msg : " + msg)
            Outils.affiche_message(msg)
            return 1
        return 0
