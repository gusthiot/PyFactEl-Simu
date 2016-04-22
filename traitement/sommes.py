from outils import Outils
from .rabais import Rabais


class Sommes(object):
    """
    Classe contenant les méthodes pour le calcul des sommes par projet, compte, catégorie et client
    """

    cles_somme_projet = ['intitule', 'somme_p_pu', 'somme_p_pv', 'somme_p_pm', 'somme_p_qu', 'somme_p_qv', 'somme_p_qm',
                         'somme_p_om', 'somme_p_nm']

    cles_somme_compte = ['somme_j_pu', 'somme_j_pv', 'somme_j_pm', 'prj', 'pj', 'somme_j_qu', 'somme_j_qv',
                         'somme_j_qm', 'qrj', 'qj', 'somme_j_om', 'orj', 'oj', 'somme_j_nm', 'nrj', 'nj', 'si_facture']

    cles_somme_categorie = ['somme_k_pu', 'somme_k_pv', 'somme_k_pm', 'somme_k_prj', 'pk', 'somme_k_qu',
                            'somme_k_qv', 'somme_k_qm', 'somme_k_qrj', 'qk', 'somme_k_om', 'somme_k_orj', 'ok',
                            'somme_k_nm', 'somme_k_nrj', 'nk']

    cles_somme_client = ['somme_t_pu', 'somme_t_pv', 'somme_t_pm', 'somme_t_prj', 'pt', 'somme_t_qu',
                         'somme_t_qv', 'somme_t_qm', 'somme_t_qrj', 'qt', 'somme_t_om', 'somme_t_orj', 'ot',
                         'somme_t_nm', 'somme_t_nrj', 'nt', 'somme_eq', 'somme_sb', 'somme_t', 'em', 'er0', 'er', 'e']

    def __init__(self, verification, generaux):
        """
        initialisation des sommes, et vérification si données utilisées correctes
        :param verification: pour vérifier si les dates et les cohérences sont correctes
        :param generaux: paramètres généraux
        """

        self.verification = verification
        self.sommes_projets = {}
        self.sp = 0
        self.sommes_comptes = {}
        self.sco = 0
        self.sommes_categories = {}
        self.sca = 0
        self.sommes_clients = {}
        self.calculees = 0
        self.categories = generaux.codes_d3()

    def calculer_toutes(self, livraisons, reservations, acces, prestations, comptes, clients):
        """
        calculer toutes les sommes, par projet, par compte, par catégorie et par client
        :param livraisons: livraisons importées et vérifiées
        :param reservations: réservations importées et vérifiées
        :param acces: accès machines importés et vérifiés
        :param prestations: prestations importées et vérifiées
        :param comptes: comptes importés et vérifiés
        :param clients: clients importés et vérifiés
        """
        self.sommes_par_projet(livraisons, reservations, acces, prestations, comptes)
        self.somme_par_compte(comptes)
        self.somme_par_categorie(comptes)
        self.somme_par_client(clients)

    def nouveau_somme(self, cles):
        """
        créé un nouveau dictionnaire avec les clés entrées
        :param cles: clés pour le dictionnaire
        :return: dictionnaire indexé par les clés données, avec valeurs à zéro
        """
        somme = {}
        for cle in cles:
            somme[cle] = 0
        somme['sommes_cat_m'] = {}
        somme['sommes_cat_r'] = {}
        somme['tot_cat'] = {}
        for categorie in self.categories:
            somme['sommes_cat_m'][categorie] = 0
            somme['sommes_cat_r'][categorie] = 0
            somme['tot_cat'][categorie] = 0
        return somme

    def sommes_par_projet(self, livraisons, reservations, acces, prestations, comptes):
        """
        calcule les sommes par projets sous forme de dictionnaire : client->compte->projet->clés_sommes
        :param livraisons: livraisons importées et vérifiées
        :param reservations: réservations importées et vérifiées
        :param acces: accès machines importés et vérifiés
        :param prestations: prestations importées et vérifiées
        :param comptes: comptes importés et vérifiés
        """

        if self.verification.a_verifier != 0:
            info = "Sommes :  vous devez faire les vérifications avant de calculer les sommes"
            print(info)
            Outils.affiche_message(info)
            return

        spp = {}
        for acce in acces.donnees:
            id_compte = acce['id_compte']
            co = comptes.donnees[id_compte]
            code_client = co['code_client']
            if code_client not in spp:
                spp[code_client] = {}
            client = spp[code_client]
            if id_compte not in client:
                client[id_compte] = {}
            num_projet = acce['num_projet']
            compte = client[id_compte]
            if num_projet not in compte:
                compte[num_projet] = self.nouveau_somme(Sommes.cles_somme_projet)
                projet = compte[num_projet]
                projet['intitule'] = acce['intitule_projet']
            else:
                projet = compte[num_projet]
            projet['somme_p_pu'] += acce['pu']
            projet['somme_p_pm'] += acce['pu']
            projet['somme_p_qu'] += acce['qu']
            projet['somme_p_qm'] += acce['qu']
            projet['somme_p_om'] += acce['om']
            projet['somme_p_nm'] += acce['om']
            projet['somme_p_nm'] += acce['qu']

        for reservation in reservations.donnees:
            id_compte = reservation['id_compte']
            co = comptes.donnees[id_compte]
            code_client = co['code_client']
            if code_client not in spp:
                spp[code_client] = {}
            client = spp[code_client]
            if id_compte not in client:
                client[id_compte] = {}
            num_projet = reservation['num_projet']
            compte = client[id_compte]
            if num_projet not in compte:
                compte[num_projet] = self.nouveau_somme(Sommes.cles_somme_projet)
                projet = compte[num_projet]
                projet['intitule'] = reservation['intitule_projet']
            else:
                projet = compte[num_projet]
            projet['somme_p_pv'] += reservation['pv']
            projet['somme_p_pm'] += reservation['pv']
            projet['somme_p_qv'] += reservation['qv']
            projet['somme_p_qm'] += reservation['qv']
            projet['somme_p_nm'] += reservation['qv']

        for livraison in livraisons.donnees:
            id_compte = livraison['id_compte']
            co = comptes.donnees[id_compte]
            code_client = co['code_client']
            if code_client not in spp:
                spp[code_client] = {}
            client = spp[code_client]
            if id_compte not in client:
                client[id_compte] = {}
            num_projet = livraison['num_projet']
            compte = client[id_compte]
            if num_projet not in compte:
                compte[num_projet] = self.nouveau_somme(Sommes.cles_somme_projet)
                projet = compte[num_projet]
                projet['intitule'] = livraison['intitule_projet']
            else:
                projet = compte[num_projet]

            id_prestation = livraison['id_prestation']
            prestation = prestations.donnees[id_prestation]

            projet['sommes_cat_m'][prestation['categorie']] += livraison['montant']
            projet['sommes_cat_r'][prestation['categorie']] += livraison['rabais_r']
            projet['tot_cat'][prestation['categorie']] += livraison['montant'] - livraison['rabais_r']

        self.sp = 1
        self.sommes_projets = spp

    def somme_par_compte(self, comptes):
        """
        calcule les sommes par comptes sous forme de dictionnaire : client->compte->clés_sommes
        :param comptes: comptes importés et vérifiés
        """

        if self.sp != 0:
            spc = {}
            for code_client, client in self.sommes_projets.items():
                if code_client not in spc:
                    spc[code_client] = {}
                cl = spc[code_client]
                for id_compte, compte in client.items():
                    cc = comptes.donnees[id_compte]
                    cl[id_compte] = self.nouveau_somme(Sommes.cles_somme_compte)
                    somme = cl[id_compte]
                    for num_projet, projet in compte.items():
                        somme['somme_j_pu'] += projet['somme_p_pu']
                        somme['somme_j_pv'] += projet['somme_p_pv']
                        somme['somme_j_pm'] += projet['somme_p_pm']
                        somme['somme_j_qu'] += projet['somme_p_qu']
                        somme['somme_j_qv'] += projet['somme_p_qv']
                        somme['somme_j_qm'] += projet['somme_p_qm']
                        somme['somme_j_om'] += projet['somme_p_om']
                        somme['somme_j_nm'] += projet['somme_p_nm']

                        for categorie in self.categories:
                            somme['sommes_cat_m'][categorie] += projet['sommes_cat_m'][categorie]
                            somme['sommes_cat_r'][categorie] += projet['sommes_cat_r'][categorie]
                            somme['tot_cat'][categorie] += projet['tot_cat'][categorie]

                    somme['prj'], somme['qrj'], somme['orj'] = Rabais.rabais_plafonnement(somme['somme_j_pm'],
                                                                                          cc['seuil'], cc['pourcent'])

                    somme['pj'] = somme['somme_j_pm'] - somme['prj']
                    somme['qj'] = somme['somme_j_qm'] - somme['qrj']
                    somme['oj'] = somme['somme_j_om'] - somme['orj']

                    somme['nrj'] = somme['qrj'] + somme['orj']
                    somme['nj'] = somme['somme_j_nm'] - somme['nrj']

                    tot = somme['somme_j_pm'] + somme['somme_j_qm'] + somme['somme_j_om']
                    for categorie in self.categories:
                        tot += somme['sommes_cat_m'][categorie]
                    if tot > 0:
                        somme['si_facture'] = 1

                    self.sco = 1
                    self.sommes_comptes = spc

        else:
            info = "Vous devez d'abord faire la somme par projet, avant la somme par compte"
            print(info)
            Outils.affiche_message(info)

    def somme_par_categorie(self, comptes):
        """
        calcule les sommes par catégories sous forme de dictionnaire : client->catégorie->clés_sommes
        :param comptes: comptes importés et vérifiés
        """

        if self.verification.a_verifier != 0:
            info = "Sommes :  vous devez faire les vérifications avant de calculer les sommes"
            print(info)
            Outils.affiche_message(info)
            return

        if self.sco != 0:
            spc = {}
            for code_client, client in self.sommes_comptes.items():
                if code_client not in spc:
                    spc[code_client] = {}
                cl = spc[code_client]
                for id_compte, compte in client.items():
                    co = comptes.donnees[id_compte]
                    cat = co['categorie']
                    if cat not in cl:
                        cl[cat] = self.nouveau_somme(Sommes.cles_somme_categorie)
                    somme = cl[cat]

                    somme['somme_k_pu'] += compte['somme_j_pu']
                    somme['somme_k_pv'] += compte['somme_j_pv']
                    somme['somme_k_pm'] += compte['somme_j_pm']
                    somme['somme_k_prj'] += compte['prj']
                    somme['pk'] += compte['pj']
                    somme['somme_k_qu'] += compte['somme_j_qu']
                    somme['somme_k_qv'] += compte['somme_j_qv']
                    somme['somme_k_qm'] += compte['somme_j_qm']
                    somme['somme_k_qrj'] += compte['qrj']
                    somme['qk'] += compte['qj']
                    somme['somme_k_om'] += compte['somme_j_om']
                    somme['somme_k_orj'] += compte['orj']
                    somme['ok'] += compte['oj']
                    somme['somme_k_nm'] += compte['somme_j_nm']
                    somme['somme_k_nrj'] += compte['nrj']
                    somme['nk'] += compte['nj']

                    for categorie in self.categories:
                        somme['sommes_cat_m'][categorie] += compte['sommes_cat_m'][categorie]
                        somme['sommes_cat_r'][categorie] += compte['sommes_cat_r'][categorie]
                        somme['tot_cat'][categorie] += compte['tot_cat'][categorie]

                    self.sca = 1
                    self.sommes_categories = spc

        else:
            info = "Vous devez d'abord faire la somme par compte, avant la somme par catégorie"
            print(info)
            Outils.affiche_message(info)

    def somme_par_client(self, clients):
        """
        calcule les sommes par clients sous forme de dictionnaire : client->clés_sommes
        :param clients: clients importés et vérifiés
        """

        if self.verification.a_verifier != 0:
            info = "Sommes :  vous devez faire les vérifications avant de calculer les sommes"
            print(info)
            Outils.affiche_message(info)
            return

        if self.sca != 0:
            spc = {}
            for code_client, client in self.sommes_categories.items():
                spc[code_client] = self.nouveau_somme(Sommes.cles_somme_client)
                somme = spc[code_client]
                for cat, som_cat in client.items():
                    somme['somme_t_pu'] += som_cat['somme_k_pu']
                    somme['somme_t_pv'] += som_cat['somme_k_pv']
                    somme['somme_t_pm'] += som_cat['somme_k_pm']
                    somme['somme_t_prj'] += som_cat['somme_k_prj']
                    somme['pt'] += som_cat['pk']
                    somme['somme_t_qu'] += som_cat['somme_k_qu']
                    somme['somme_t_qv'] += som_cat['somme_k_qv']
                    somme['somme_t_qm'] += som_cat['somme_k_qm']
                    somme['somme_t_qrj'] += som_cat['somme_k_qrj']
                    somme['qt'] += som_cat['qk']
                    somme['somme_t_om'] += som_cat['somme_k_om']
                    somme['somme_t_orj'] += som_cat['somme_k_orj']
                    somme['ot'] += som_cat['ok']
                    somme['somme_t_nm'] += som_cat['somme_k_nm']
                    somme['somme_t_nrj'] += som_cat['somme_k_nrj']
                    somme['nt'] += som_cat['nk']

                    for categorie in self.categories:
                        somme['sommes_cat_m'][categorie] += som_cat['sommes_cat_m'][categorie]
                        somme['sommes_cat_r'][categorie] += som_cat['sommes_cat_r'][categorie]
                        somme['tot_cat'][categorie] += som_cat['tot_cat'][categorie]

                cl = clients.donnees[code_client]

                somme['somme_eq'], somme['somme_sb'], somme['somme_t'], somme['em'], somme['er0'], somme['er'] = \
                    Rabais.rabais_emolument(somme['pt'], somme['qt'], somme['ot'], somme['tot_cat'],
                                            cl['emol_base_mens'], cl['emol_fixe'], cl['coef'], cl['emol_sans_activite'])
                somme['e'] = somme['em'] - somme['er']
                self.calculees = 1
                self.sommes_clients = spc

        else:
            info = "Vous devez d'abord faire la somme par catégorie, avant la somme par client"
            print(info)
            Outils.affiche_message(info)
