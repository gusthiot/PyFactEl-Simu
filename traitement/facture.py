import csv
from latex import Latex
from outils import Outils


class Facture(object):
    """
    Classe contenant les méthodes nécessaires à la génération des factures
    """

    def __init__(self, prod2qual=None):
        """
        Constructeur

        :param prod2qual: Une instance de la classe Prod2Qual
        """

        self.prod2qual = prod2qual

    def factures(self, sommes, destination, edition, generaux, clients, comptes,
                 lien_annexes, lien_annexes_techniques, annexes, annexes_techniques):
        """
        génère la facture sous forme de csv
        :param sommes: sommes calculées
        :param nom_dossier: nom du dossier dans lequel enregistrer le csv
        :param delimiteur: code délimiteur de champ dans le fichier csv
        :param encodage: encodage du texte
        :param edition: paramètres d'édition
        :param generaux: paramètres généraux
        :param clients: clients importés
        :param comptes: comptes importés
        :param lien_annexes: lien au dossier contenant les annexes
        :param lien_annexes_techniques: lien au dossier contenant les annexes techniques
        :param dossier_annexes: dossier contenant les annexes
        :param dossier_annexes_techniques: dossier contenant les annexes techniques
        """

        if sommes.calculees == 0:
            info = "Vous devez d'abord faire toutes les sommes avant de pouvoir créer la facture"
            print(info)
            Outils.affiche_message(info)
            return

        if self.prod2qual:
            suffixe = "_qualite.csv"
        else:
            suffixe = ".csv"
        nom = "facture_" + str(edition.annee) + "_" + Outils.mois_string(edition.mois) + "_" + \
              str(edition.version) + suffixe
        with destination.writer(nom) as fichier_writer:
            fichier_writer.writerow(["Poste", "Système d'origine", "Type de document de vente", "Organisation commerciale",
                                     "Canal de distribution", "Secteur d'activité", "Agence commerciale",
                                     "Groupe de vendeurs", "Donneur d'ordre", "Nom 2 du donneur d'ordre",
                                     "Nom 3 du donneur d'ordre", "Adresse e-mail", "Client facturé", "Payeur", "Client livré", "Devise",
                                     "Mode d'envoi", "Numéro de la commande d'achat du client",
                                     "Date de livraison E/Tsouhaitée", "Nom émetteur", "Textes", "Lien réseau 01",
                                     "Doc interne", "Lien réseau 02", "Doc interne", "Lien réseau 03", "Doc interne",
                                     "Lien réseau 04", "Doc interne", "Lien réseau 05", "Doc interne", "Article",
                                     "Désignation du poste d'une commande client", "Quantité cible en unité de vente",
                                     "Unité de quantité cible", "Type de prix net", "Prix net du poste",
                                     "Type de rabais poste", "Valeur rabais poste", "Date de livraison poste souhaitée",
                                     "Centre financier émetteur", "Compte budgétaire émetteur", "Fonds émetteur",
                                     "OTP émetteur", "Numéro d'ordre interne émetteur", "Code OP émetteur",
                                     "Affaire émetteur", "Demande de voyage émetteur", "Matricule émetteur", "Textes",
                                     "Nom consommateur interne de la prestation", "Fonds récepteur 01",
                                     "Proportion fonds récepteur 01", "OTP récepteur fonds 01",
                                     "Numéro d'ordre interne récepteur fonds 01", "Code OP récepteur fonds 01",
                                     "Affaire récepteur 01", "Demande de voyage récepteur fonds 01",
                                     "Matricule récepteur fonds 01", "Fonds récepteur 02", "Proportion fonds récepteur 02",
                                     "OTP récepteur fonds 02", "Numéro d'ordre interne récepteur fonds 02",
                                     "Code OP récepteur fonds 02", "Affaire récepteur 02",
                                     "Demande de voyage récepteur fonds 02", "Matricule récepteur fonds 02",
                                     "Fonds récepteur 03", "Proportion fonds récepteur 03", "OTP récepteur fonds 03",
                                     "Numéro d'ordre interne récepteur fonds 03", "Code OP récepteur fonds 03",
                                     "Affaire récepteur 03", "Demande de voyage récepteur fonds 03",
                                     "Matricule récepteur fonds 03", "Fonds récepteur 04", "Proportion fonds récepteur 04",
                                     "OTP récepteur fonds 04", "Numéro d'ordre interne récepteur fonds 04",
                                     "Code OP récepteur fonds 04", "Affaire récepteur 04",
                                     "Demande de voyage récepteur fonds 04", "Matricule récepteur fonds 04",
                                     "Fonds récepteur 05", "Proportion fonds récepteur 05", "OTP récepteur fonds 05",
                                     "Numéro d'ordre interne récepteur fonds 05", "Code OP récepteur fonds 05",
                                     "Affaire récepteur 05", "Demande de voyage récepteur fonds 05",
                                     "Matricule récepteur fonds 05"])

            contenu = ""

            for code_client in sorted(sommes.sommes_clients.keys()):
                poste = 0
                client = sommes.sommes_clients[code_client]
                cl = clients.donnees[code_client]

                tot = client['somme_t_pu'] + client['somme_t_nm']
                for categorie in generaux.codes_d3():
                    tot += client['sommes_cat_m'][categorie]
                if tot == 0 and client['e'] == 0:
                    continue
    
                code_sap = cl['code_sap']
                if self.prod2qual and not (self.prod2qual.code_client_existe(code_sap)):
                    continue
    
                if cl['type_labo'] == "I":
                    genre = generaux.code_int
                else:
                    genre = generaux.code_ext
                nature = generaux.nature_client_par_code_n(cl['type_labo'])
                reference = nature + str(edition.annee)[2:] + Outils.mois_string(edition.mois) + "." + code_client
                if edition.version != "0":
                    reference += "-" + edition.version
    
                nom_annexe = "annexe_" + str(edition.annee) + "_" + Outils.mois_string(edition.mois) + \
                              "_" + str(edition.version) + "_" + code_client + ".pdf"
                lien_annexe = lien_annexes + nom_annexe
                dossier_annexe = "../" + annexes + "/" + nom_annexe
    
                nom_annexe_technique = "annexeT_" + str(edition.annee) + "_" + \
                                        Outils.mois_string(edition.mois) + "_" + str(edition.version) + "_" + \
                                        code_client + ".pdf"
                lien_annexe_technique = lien_annexes_techniques + nom_annexe_technique
                dossier_annexe_technique = "../" + annexes_techniques + "/" + nom_annexe_technique
    
                if self.prod2qual:
                    code_sap_traduit = self.prod2qual.traduire_code_client(code_sap)
                else:
                    code_sap_traduit = code_sap
    
                dico_contenu = {'code': code_client, 'abrev': cl['abrev_labo'],
                                'nom': cl['nom_labo'], 'dest': cl['dest'], 'ref': cl['ref'],
                                'ref_fact': reference, 'texte': generaux.entete}
                contenu_client = r'''<section><div id="entete"> %(code)s <br />
                    %(abrev)s <br />
                    %(nom)s <br />
                    %(dest)s <br />
                    %(ref)s <br />
                    </div><br />
                    %(ref_fact)s <br /><br />
                    %(texte)s <br />
                    ''' % dico_contenu
    
                contenu_client += r'''<table id="tableau">
                    <tr>
                    <td>Item </td><td> Date </td><td> Name </td><td> Description </td><td> Unit </td><td> Quantity </td>
                    <td> Unit Price <br /> [CHF] </td><td> Discount </td><td> Net amount <br /> [CHF] </td>
                    </tr>
                    '''
    
                fichier_writer.writerow([poste, generaux.origine, genre, generaux.commerciale,
                                         generaux.canal, generaux.secteur, "", "",
                                         code_sap_traduit, cl['dest'], cl['ref'], cl['email'], code_sap_traduit, code_sap_traduit,
                                         code_sap_traduit, generaux.devise, cl['mode'], reference, "", "",
                                         generaux.entete, lien_annexe, "", lien_annexe_technique, "X"])
    
                op_centre = cl['type_labo'] + str(edition.annee)[2:] + Outils.mois_string(edition.mois)
                if int(cl['emol_base_mens']) > 0:
                    poste = generaux.poste_emolument
                    fichier_writer.writerow(self.ligne_facture(generaux, generaux.articles[0], poste, client['em'], client['er'],
                                                                  op_centre, "", edition))
                    contenu_client += self.ligne_tableau(generaux.articles[0], poste, client['em'], client['er'], "", edition)

                if client['r'] > 0:
                    poste = generaux.poste_reservation
                    fichier_writer.writerow(self.ligne_facture(generaux, generaux.articles[1], poste, client['rm'], client['rr'],
                                                               op_centre, "", edition))
                    contenu_client += self.ligne_tableau(generaux._articles[1], poste, client['rm'], client['rr'], "", edition)
    
                inc = 1
                client_comptes = sommes.sommes_comptes[code_client]
                for id_compte in sorted(client_comptes.keys()):
                    compte = client_comptes[id_compte]
                    co = comptes.donnees[id_compte]
                    if compte['si_facture'] > 0:
                        poste = inc*10
                        if compte['somme_j_pu'] > 0:
                            fichier_writer.writerow(self.ligne_facture(generaux, generaux.articles[2],
                                                                       poste, compte['somme_j_pu'],
                                                                       compte['prj'], op_centre, co['intitule'], edition))
                            contenu_client += self.ligne_tableau(generaux.articles[2], poste, compte['somme_j_pu'],
                                                                     compte['prj'], co['intitule'], edition)
                            poste += 1
    
                        if compte['somme_j_nm'] > 0:
                            fichier_writer.writerow(self.ligne_facture(generaux, generaux.articles[3],
                                                                       poste, compte['somme_j_nm'],
                                                                        compte['nrj'], op_centre, co['intitule'], edition))
                            contenu_client += self.ligne_tableau(generaux.articles[3], poste, compte['somme_j_nm'],
                                                                     compte['nrj'], co['intitule'], edition)
                            poste += 1
    
                        for article in generaux.articles_d3:
                            categorie = article.code_d
                            if compte['sommes_cat_m'][categorie] > 0:
                                fichier_writer.writerow(self.ligne_facture(generaux, article,
                                    poste,
                                    compte['sommes_cat_m'][categorie], compte['sommes_cat_r'][categorie], op_centre,
                                                                              co['intitule'], edition))
                                contenu_client += self.ligne_tableau(article, poste,
                                                                         compte['sommes_cat_m'][categorie],
                                                                         compte['sommes_cat_r'][categorie], co['intitule'],
                                                                         edition)
                                poste += 1
                        inc += 1
    
                contenu_client += r'''
                    <tr><td colspan="8" id="toright">Net amount [CHF] : </td><td id="toright">
                    ''' + "%.2f" % (client['somme_t'] + client['em'] - client['er']) + r'''</td></tr>
                    </table>
                    '''
                contenu_client += r'''<a href="''' + dossier_annexe + r'''" target="new">''' + nom_annexe + r'''
                    </a>&nbsp;&nbsp;&nbsp;'''
                contenu_client += r'''<a href="''' + dossier_annexe_technique + r'''" target="new">
                    ''' + nom_annexe_technique + r'''</a>'''
                contenu_client += "</section>"
                contenu += contenu_client
        self.creer_html(contenu, destination)

    def ligne_tableau(self, article, poste, net, rabais, consommateur, edition):
        montant = net - rabais
        date_livraison = str(edition.dernier_jour) + "." + Outils.mois_string(edition.mois) + "." + str(edition.annee)
        description = article.code_d + " : " + article.code_sap
        dico_tab = {'poste': poste, 'date': date_livraison, 'descr': description,
                    'texte': article.texte_sap, 'nom': Latex.echappe_caracteres(consommateur),
                    'unit': article.unite, 'quantity': article.quantite,
                    'unit_p': "%.2f" % net, 'discount': "%.2f" % rabais, 'net': "%.2f" % montant}
        ligne = r'''<tr>
            <td> %(poste)s </td><td> %(date)s </td><td> %(nom)s </td><td> %(descr)s <br /> %(texte)s </td>
            <td> %(unit)s </td><td id="toright"> %(quantity)s </td><td id="toright"> %(unit_p)s </td>
            <td id="toright"> %(discount)s </td><td id="toright"> %(net)s </td>
            </tr>
            ''' % dico_tab
        return ligne

    def ligne_facture(self, generaux, article, poste, net, rabais, op_centre, consommateur, edition):
        """
        retourne une ligne de facturation  formatée

        :param generaux: paramètres généraux
        :param article: Une instance de la classe generaux.Article
        :param poste: indice de poste
        :param net: montant net
        :param rabais: rabais sur le montant
        :param op_centre: centre d'opération
        :param consommateur: consommateur
        :param edition: paramètres d'édition
        :return: ligne de facturation formatée
        """
        if rabais == 0:
            rabais = ""
        code_op =  generaux.code_t + op_centre + article.code_d
        date_livraison = str(edition.annee) + Outils.mois_string(edition.mois) + str(edition.dernier_jour)

        return [poste, "", "", "", "", "", "", "", "", "", "", "", "", "", "", "", "", "", "", "", "", "", "", "", "",
                "", "", "", "", "", "", article.code_sap, "", article.quantite,
                article.unite, article.type_prix, net,
                article.type_rabais, rabais, date_livraison, generaux.centre_financier, "",
                generaux.fonds, "", "", code_op, "", "", "", article.texte_sap,
                consommateur]

    def creer_html(self, contenu, destination):
        if self.prod2qual:
            suffixe = "_qualite.html"
        else:
            suffixe = ".html"

        Outils.copier_dossier("./reveal.js/", "js", destination.chemin)
        Outils.copier_dossier("./reveal.js/", "css", destination.chemin)
        with destination.open("ticket" + suffixe) as fichier:

            html = r'''<!DOCTYPE html PUBLIC "-//W3C//DTD XHTML 1.0 Strict//EN"
                "http://www.w3.org/TR/xhtml1/DTD/xhtml1-strict.dtd">
                <html xmlns="http://www.w3.org/1999/xhtml">
                <head>
                <meta content="text/html; charset=cp1252" http-equiv="content-type" />
                <meta content="CMi" name="author" />
                <style>
                #entete {
                    margin-left: 600px;
                    text-align:left;
                }
                #tableau {
                    border-collapse: collapse;
                    margin: 20px;
                }
                #tableau tr, #tableau td {
                    border: 1px solid black;
                    vertical-align:middle;
                }
                #tableau td {
                    padding: 3px;
                }
                #toright {
                    text-align:right;
                }
                </style>
                <link rel="stylesheet" href="css/reveal.css">
                <link rel="stylesheet" href="css/white.css">
                </head>
                <body>
                <div class="reveal">
                <div class="slides">
                '''
            html += contenu
            html += r'''</div>
                    <script src="js/reveal.js"></script>
                    <script>
                        Reveal.initialize();
                    </script>
                    </body>
                </html>'''
            fichier.write(html)
