

class Rabais(object):
    """
    Classe contenant les règles de rabais
    """

    @staticmethod
    def rabais_reservation(drsf, supp, shp, shc):
        """
        calcule le rabais de réservation
        :param drsf: délai sans frais pour une machine donnée
        :param supp: durée ouvrée
        :param shp: durée du slot réservée en heures pleines
        :param shc: durée du slot réservée en heures creuses
        :return: durée facturée en heures pleines, durée facturée en heures creuses
        """
        if drsf == 0:
            return 0, 0
        else:
            k = max(0, min(1, (1-supp / drsf)))
            fhp = round(k * shp, 0)
            fhc = round(k * shc, 0)
            return fhp, fhc

    @staticmethod
    def rabais_emolument(pt, qt, ot, cat_t, emb, fix, coef_a, regle, res):
        """
        calcule le rabais sur émolument
        :param pt: pt
        :param qt: qt
        :param ot: ot
        :param cat_t: dico des totaux des catégories de prestations
        :param emb: émolument de base mensuel
        :param fix: émolument fixe
        :param coef_a: coefficient a
        :param regle: émolument sans activité
        :param res: frais de réservation
        :return: somme EQ, somme SB, somme T, em, er0, er
        """
        somme_eq = pt + qt + res
        somme_sb = pt + qt + ot
        somme_t = pt + qt + ot
        for cat, tt in cat_t.items():
            somme_t += tt

        em = emb
        er0 = round(min(emb, max(0, emb - fix - (coef_a - 1) * somme_eq))/10, 0)*10
        if ((regle == "ZERO") and (somme_t == 0)) or ((regle == "NON") and (somme_sb == 0)):
            er = em
        else:
            er = er0
        return somme_eq, somme_t, em, er0, er

    @staticmethod
    def rabais_plafonnement(somme_j_pu, s, k):
        """
        calcule le rabais sur plafonnement
        :param somme_j_pu: somme par compte des machines plafonnées
        :param s: seuil
        :param k: pourcentage appliqué après le seuil
        :return: rabais sur montant plafonné, sur montant non-plafonné, sur main d'oeuvre opérateur
        """
        prj = -min(0, min(somme_j_pu, s) + k * max(0, somme_j_pu - s) - somme_j_pu)
        qrj = 0
        orj = 0
        return prj, qrj, orj

    @staticmethod
    def rabais_reservation_petit_montant(rm, rmin):
        """
        si le montant ne dépasse pas un seuil minimum, un rabais égal à ce montant est appliqué
        :param rm: montant
        :param rmin: seuil
        :return: rabais
        """
        if rm < int(rmin):
            return rm
        else:
            return 0
