from importes import Fichier
from outils import Outils


class CoefPrest(Fichier):
    """
    Classe pour l'importation des données de Coefficients Prestations
    """

    cles = ['annee', 'mois', 'id_classe_tarif', 'intitule', 'categorie', 'nom_categorie', 'coefficient']
    nom_fichier = "coeffprestation.csv"
    libelle = "Coefficients Prestations"

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.classes = []
        self.noms_cat = {}

    def obtenir_classes(self):
        """
        retourne toutes les classes de tarif présentes
        :return: toutes les classes de tarif présentes
        """
        if self.verifie_coherence == 0:
            info = self.libelle + ". vous devez vérifier la cohérence avant de pouvoir obtenir les classes"
            print(info)
            Outils.affiche_message(info)
            return []
        return self.classes

    def obtenir_noms_categories(self, categorie):
        """
        retourne le nom lié à une catégorie
        :return: nom lié à une catégorie
        """
        if self.verifie_coherence == 0:
            info = self.libelle + ". vous devez vérifier la cohérence avant de pouvoir obtenir les catégories"
            print(info)
            Outils.affiche_message(info)
            return []
        if categorie not in self.noms_cat:
            return categorie
        else:
            return self.noms_cat[categorie]

    def contient_categorie(self, categorie):
        """
        vérifie si la catégorie est présente
        :param categorie: la catégorie à vérifier
        :return: 1 si présente, 0 sinon
        """
        if self.verifie_coherence == 1:
            for cle, coefprest in self.donnees.items():
                if coefprest['categorie'] == categorie:
                    return 1
        else:
            for coefprest in self.donnees:
                if coefprest['categorie'] == categorie:
                    return 1
        return 0

    def est_coherent(self, generaux):
        """
        vérifie que les données du fichier importé sont cohérentes (si couple catégorie - classe de tarif est unique),
        et efface les colonnes mois et année
        :param generaux: paramètres généraux
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
        categories = []
        couples = []
        donnees_dict = {}

        for donnee in self.donnees:
            if donnee['categorie'] == "":
                msg += "la catégorie de la ligne " + str(ligne) + " ne peut être vide\n"
            elif donnee['categorie'] not in generaux.codes_d3():
                msg += "la catégorie '" + donnee['categorie'] + "' de la ligne " + str(ligne) +\
                       " n'existe pas dans les paramètres D3\n"
            elif donnee['categorie'] not in categories:
                categories.append(donnee['categorie'])

            if donnee['id_classe_tarif'] == "":
                msg += "la classe de tarif de la ligne " + str(ligne) + " ne peut être vide\n"
            elif donnee['id_classe_tarif'] not in self.classes:
                self.classes.append(donnee['id_classe_tarif'])

            if (donnee['categorie'] != "") and (donnee['id_classe_tarif'] != ""):
                couple = [donnee['categorie'], donnee['id_classe_tarif']]
                if couple not in couples:
                    couples.append(couple)
                    del donnee['annee']
                    del donnee['mois']
                    donnees_dict[donnee['id_classe_tarif']+donnee['categorie']] = donnee
                else:
                    msg += "Couple categorie '" + donnee['categorie'] + "' et classe de tarif '" + \
                           donnee['id_classe_tarif'] + "' de la ligne " + str(ligne) + " pas unique\n"

            if donnee['categorie'] not in self.noms_cat:
                self.noms_cat[donnee['categorie']] = donnee['nom_categorie']

            donnee['coefficient'], info = Outils.est_un_nombre(donnee['coefficient'], "le coefficient", ligne)
            msg += info

        for categorie in generaux.codes_d3():
            if categorie not in categories:
                msg += "La categorie D3 '" + categorie + "' dans les paramètres généraux n'est pas présente dans " \
                                                         "les coefficients de prestations\n"

        for categorie in categories:
            for classe in self.classes:
                couple = [categorie, classe]
                if couple not in couples:
                    msg += "Couple categorie '" + categorie + "' et classe de tarif '" + \
                           classe + "' n'existe pas\n"

            ligne += 1

        self.donnees = donnees_dict
        self.verifie_coherence = 1

        if msg != "":
            msg = self.libelle + "\n" + msg
            print("msg : " + msg)
            Outils.affiche_message(msg)
            return 1


        return 0
