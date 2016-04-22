import csv

from outils import Outils


class BilanMensuel(object):
    """
    Classe pour la création du bilan mensuel
    """

    @staticmethod
    def bilan(dossier_destination, edition, sommes, clients, generaux, acces, reservations, livraisons,
              comptes):
        """
        création du bilan

        :param dossier_source: Une instance de la classe dossier.DossierSource
        :param edition: paramètres d'édition
        :param sommes: sommes calculées
        :param clients: clients importés
        :param generaux: paramètres généraux
        :param acces: accès importés
        :param reservations: réservations importés
        :param livraisons: livraisons importées
        :param comptes: comptes importés
        """

        if sommes.calculees == 0:
            info = "Vous devez d'abord faire toutes les sommes avant de pouvoir créer le bilan mensuel"
            print(info)
            Outils.affiche_message(info)
            return

        nom = "bilan_" + str(edition.annee) + "_" + Outils.mois_string(edition.mois) + "_" + \
              str(edition.version) + ".csv"

        with dossier_destination.writer(nom) as fichier_writer:

            ligne = ["année", "mois", "référence", "code client", "code client sap", "abrév. labo", "nom labo",
                     "type client", "nature client", "nb utilisateurs", "nb tot comptes", "nb comptes cat 1",
                     "nb comptes cat 2", "nb comptes cat 3", "nb comptes cat 4", "somme T", "Em base", "somme EQ",
                     "Rabais Em", "Prj 1", "Prj 2", "Prj 3", "Prj 4", "Pt", "Qt", "Ot", "Nt"]
            for categorie in generaux.codes_d3():
                ligne.append(categorie + "t")
            fichier_writer.writerow(ligne)

            for code_client in sorted(sommes.sommes_clients.keys()):
                scl = sommes.sommes_clients[code_client]
                sca = sommes.sommes_categories[code_client]
                cl = clients.donnees[code_client]
                nature = generaux.nature_client_par_code_n(cl['type_labo'])
                reference = nature + str(edition.annee)[2:] + Outils.mois_string(edition.mois) + "." + code_client
                nb_u = len(BilanMensuel.utilisateurs(acces, livraisons, reservations, code_client))
                cptes = BilanMensuel.comptes(acces, livraisons, reservations, code_client)
                cat = {'1': 0, '2': 0, '3': 0, '4': 0}
                nb_c = 0
                for cpte in cptes:
                    nb_c += 1
                    cat[comptes.donnees[cpte]['categorie']] += 1

                if '1' in sca:
                    kprj1 = sca['1']['somme_k_prj']
                else:
                    kprj1 = 0
                if '2' in sca:
                    kprj2 = sca['2']['somme_k_prj']
                else:
                    kprj2 = 0
                if '3' in sca:
                    kprj3 = sca['3']['somme_k_prj']
                else:
                    kprj3 = 0
                if '4' in sca:
                    kprj4 = sca['4']['somme_k_prj']
                else:
                    kprj4 = 0

                ligne = [edition.annee, edition.mois, reference, code_client, cl['code_sap'], cl['abrev_labo'],
                         cl['nom_labo'], 'U', cl['type_labo'], nb_u, nb_c, cat['1'], cat['2'], cat['3'], cat['4'],
                         scl['somme_t'], scl['em'], scl['somme_eq'], scl['er'], kprj1, kprj2, kprj3, kprj4, scl['pt'],
                         scl['qt'], scl['ot'], scl['nt']]
                for categorie in generaux.codes_d3():
                    ligne.append(scl['tot_cat'][categorie])
                fichier_writer.writerow(ligne)

    @staticmethod
    def utilisateurs(acces, livraisons, reservations, code_client):
        """
        retourne la liste de tous les utilisateurs concernés pour les accès, les réservations et les livraisons
        pour un client donné
        :param acces: accès importés
        :param livraisons: livraisons importées
        :param reservations: réservations importées
        :param code_client: client donné
        :return: liste des utilisateurs
        """
        utilisateurs = []
        for cae in acces.donnees:
            if cae['code_client'] == code_client:
                if cae['id_user'] not in utilisateurs:
                    utilisateurs.append(cae['id_user'])
        for lvr in livraisons.donnees:
            if lvr['code_client'] == code_client:
                if lvr['id_user'] not in utilisateurs:
                    utilisateurs.append(lvr['id_user'])
        for res in reservations.donnees:
            if res['code_client'] == code_client:
                if res['id_user'] not in utilisateurs:
                    utilisateurs.append(res['id_user'])
        return utilisateurs

    @staticmethod
    def comptes(acces, livraisons, reservations, code_client):
        """
        retourne la liste de tous les comptes concernés pour les accès, les réservations et les livraisons
        pour un client donné
        :param acces: accès importés
        :param livraisons: livraisons importées
        :param reservations: réservations importées
        :param code_client: client donné
        :return: liste des comptes
        """
        comptes = []
        for cae in acces.donnees:
            if cae['code_client'] == code_client:
                if cae['id_compte'] not in comptes:
                    comptes.append(cae['id_compte'])
        for lvr in livraisons.donnees:
            if lvr['code_client'] == code_client:
                if lvr['id_compte'] not in comptes:
                    comptes.append(lvr['id_compte'])
        for res in reservations.donnees:
            if res['code_client'] == code_client:
                if res['id_compte'] not in comptes:
                    comptes.append(res['id_compte'])
        return comptes
