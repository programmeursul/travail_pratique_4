# -*- coding: utf-8 -*-
"""
Module contenant la description de la classe Tableau. Un tableau est utilisé pour jouer une partie du jeu Démineur.

Auteurs: à compléter
"""

from case import Case
from random import randint


class Tableau():
    """
    Tableau du jeu de démineur, implémenté avec un dictionnaire de cases.

    Warning:
        Si vous ajoutez des attributs à la classe Tableau, n'oubliez pas de les documenter ici.

    Attributes:
        dimension_rangee (int): Nombre de rangées du tableau
        dimension_colonne (int): Nombre de colonnes du tableau
        nombre_mines (int): Nombre de mines cachées dans le tableau

        nombre_cases_sans_mine_a_devoiler (int) : Nombre de cases sans mine qui n'ont pas encore été dévoilées
            Initialement, ce nombre est égal à dimension_rangee * dimension_colonne - nombre_mines

        dictionnaire_cases (dict): Un dictionnaire de case en suivant le format suivant:
            Les clés sont les positions du tableau sous la forme d'un tuple (x, y),
                x étant le numéro de la rangée, y étant le numéro de la colonne.
            Les éléments sont des objets de la classe Case.
    """

    def __init__(self, dimension_rangee=5, dimension_colonne=5, nombre_mines=5):
        """ Initialisation d'un objet tableau.

        Attributes:
            dimension_rangee (int): Nombre de rangées du tableau (valeur par défaut: 5)
            dimension_colonne (int): Nombre de colonnes du tableau (valeur par défaut: 5)
            nombre_mines (int): Nombre de mines cachées dans le tableau (valeur par défaut: 5)
        """

        self.dimension_rangee = dimension_rangee
        self.dimension_colonne = dimension_colonne
        self.nombre_mines = nombre_mines

        # Le dictionnaire de case, vide au départ, qui est rempli par la fonction initialiser_tableau().
        self.dictionnaire_cases = {}

        self.initialiser_tableau()

        self.nombre_cases_sans_mine_a_devoiler = self.dimension_rangee * self.dimension_colonne - self.nombre_mines

    def valider_coordonnees(self, rangee_x, colonne_y):
        """
        Valide les coordonnées reçues en argument. Les coordonnées sont considérées valides si elles se trouvent bien
        dans les dimensions du tableau.

        Args:
            rangee_x (int) : Numéro de la rangée de la case dont on veut valider les coordonnées
            colonne_y (int): Numéro de la colonne de la case dont on veut valider les coordonnées

        Returns:
            bool: True si les coordonnées (x, y) sont valides, False autrement
        """
        rangee_valide = rangee_x >= 1 and rangee_x <= self.dimension_rangee
        colonne_valide = colonne_y >= 1 and colonne_y <= self.dimension_colonne
        return rangee_valide and colonne_valide

    def obtenir_case(self, rangee_x, colonne_y):
        """
        Récupère une case à partir de ses numéros de ligne et de colonne

        Args:
            rangee_x (int) : Numéro de la rangée de la cas
            colonne_y (int): Numéro de la colonne de la case
        Returns:
            Case: Une référence vers la case obtenue
            (ou None si les coordonnées ne sont pas valides)
        """
        if not self.valider_coordonnees(rangee_x, colonne_y):
            return None

        coordonnees = (rangee_x, colonne_y)
        return self.dictionnaire_cases[coordonnees]

    def obtenir_voisins(self, rangee_x, colonne_y):
        """
        Retourne une liste de coordonnées correspondant aux cases voisines d'une case. Toutes les coordonnées retournées
        doivent être valides (c'est-à-dire se trouver à l'intérieur des dimensions du tableau).

        Args:
            rangee_x (int) : Numéro de la rangée de la case dont on veut connaître les cases voisines
            colonne_y (int): Numéro de la colonne de la case dont on veut connaître les cases voisines

        Returns:
            list : Liste des coordonnées (tuple x, y) valides des cases voisines de la case dont les coordonnées
            sont reçues en argument
        """
        voisinage = ((-1, -1), (-1, 0), (-1, 1),
                     (0, -1), (0, 1),
                     (1, -1), (1, 0), (1, 1))

        liste_coordonnees_cases_voisines = []

        for voisin in voisinage:
            rangee_voisin_x = rangee_x + voisin[0]
            colonne_voisin_y = colonne_y + voisin[1]
            if rangee_voisin_x > 0 and colonne_voisin_y > 0:
                if rangee_voisin_x <= self.dimension_rangee and colonne_voisin_y <= self.dimension_colonne:
                    liste_coordonnees_cases_voisines.append((rangee_voisin_x, colonne_voisin_y))
        return liste_coordonnees_cases_voisines

    def initialiser_tableau(self):
        """
        Initialise le tableau à son contenu initial en suivant les étapes suivantes:
            1) On crée chacune des cases du tableau (cette étape est programmée pour vous).
            2) On y ajoute ensuite les mines dans certaines cases qui sont choisies au hasard
                (attention de ne pas choisir deux fois la même case!).
                - À chaque fois qu'on ajoute une mine dans une case, on obtient la liste de
                  ses voisins (pour se faire, utilisez la méthode obtenir_voisins)
                - Pour chaque voisin, on appelle la méthode ajouter_une_mine_voisine de la case correspondante.
        """
        for rangee_x in range(1, self.dimension_rangee + 1):
            for colonne_y in range(1, self.dimension_colonne + 1):
                coordonnees = (rangee_x, colonne_y)
                self.dictionnaire_cases[coordonnees] = Case()

        compte_mines = 0
        coordonnees_liste = ()
        while compte_mines < self.nombre_mines:
            rangee_aleatoire_x = randint(1, self.dimension_rangee)
            colonne_aleatoire_y = randint(1, self.dimension_colonne)
            coordonnees = (rangee_aleatoire_x, colonne_aleatoire_y)
            if coordonnees not in coordonnees_liste:
                coordonnees_liste = coordonnees_liste + (coordonnees,)
                self.dictionnaire_cases[coordonnees].ajouter_mine()
                voisins = self.obtenir_voisins(rangee_aleatoire_x, colonne_aleatoire_y)
                compte_mines += 1
                for voisin in voisins:
                    self.dictionnaire_cases[voisin].ajouter_une_mine_voisine()

    def valider_coordonnees_a_devoiler(self, rangee_x, colonne_y):
        """
        Valide que les coordonnées reçues en argument sont celles d'une case que l'on peut dévoiler
        (donc que les coordonnées sont valides et que la case correspondante n'a pas encore été dévoilée).

        Args:
            rangee_x (int) : Numéro de la rangée de la case dont on veut valider les coordonnées
            colonne_y (int): Numéro de la colonne de la case dont on veut valider les coordonnées

        Returns
            bool: True si la case à ces coordonnées (x, y) peut être dévoilée, False autrement (donc si la
                  case a déjà été dévoilée ou que les coordonnées ne dont pas valides).
        """
        if self.valider_coordonnees(rangee_x, colonne_y):
            case_xy = self.obtenir_case(rangee_x, colonne_y)
            if not case_xy.est_devoilee:
                return True
            else:
                return False
        else:
            return False

    def afficher_solution(self):
        """
        Méthode qui affiche le tableau de la solution à l'écran. La solution montre les
        mines pour les cases qui en contiennent et la valeur du nombre de mines voisines
        pour les autres cases.

        Important: Vous n'avez pas à modifier cette méthode, mais vous pouvez vous
        en inspirer pour écrire la méthode afficher_tableau().
        """
        print()  # Retour de ligne

        for rangee_x in range(0, self.dimension_rangee + 1):

            # Affichage d'une ligne, caractère par caractère
            for colonne_y in range(0, self.dimension_colonne + 1):
                if rangee_x == 0 and colonne_y == 0:
                    # Premiers caractères de l'en-tête (coin supérieur gauche)
                    car = '  |'
                elif rangee_x == 0:
                    # En-tête: numéro de la colonne
                    # (si y > 10, on affiche seulement l'unité pour éviter les décalages)
                    car = f'{colonne_y % 10}'
                elif colonne_y == 0:
                    # Début de ligne: numéro de la ligne sur deux caractères,
                    # suivi d'une ligne verticale.
                    car = f'{rangee_x:<2}|'
                else:
                    # Contenu d'une case
                    case_xy = self.obtenir_case(rangee_x, colonne_y)
                    if case_xy.est_minee:
                        car = 'M'
                    else:
                        car = str(case_xy.nombre_mines_voisines)

                # Afficher le caractère suivit d'un espace (sans retour de ligne)
                print(car, end=" ")

            # À la fin de chaque ligne
            print()  # Retour de ligne
            if rangee_x == 0:  # Ligne horizontale de l'en-tête
                print('--+-' + '--' * self.dimension_colonne)

    def afficher_tableau(self):
        """
        Méthode qui affiche le tableau à l'écran. Le tableau montre le contenu des cases dévoilées
        (mine ou nombre de mines voisines) ou un point pour les cases non dévoilées.
        """
        print()  # Retour de ligne

        for rangee_x in range(0, self.dimension_rangee + 1):

            # Affichage d'une ligne, caractère par caractère
            for colonne_y in range(0, self.dimension_colonne + 1):
                if rangee_x == 0 and colonne_y == 0:
                    # Premiers caractères de l'en-tête (coin supérieur gauche)
                    car = '  |'
                elif rangee_x == 0:
                    # En-tête: numéro de la colonne
                    # (si y > 10, on affiche seulement l'unité pour éviter les décalages)
                    car = f'{colonne_y % 10}'
                elif colonne_y == 0:
                    # Début de ligne: numéro de la ligne sur deux caractères,
                    # suivi d'une ligne verticale.
                    car = f'{rangee_x:<2}|'
                else:
                    # Contenu d'une case
                    case_xy = self.obtenir_case(rangee_x, colonne_y)
                    if case_xy.est_devoilee:
                        if case_xy.est_minee:
                            car = 'M'
                        else:
                            car = str(case_xy.nombre_mines_voisines)
                    else:
                        car = '.'

                # Afficher le caractère suivit d'un espace (sans retour de ligne)
                print(car, end=" ")

            # À la fin de chaque ligne
            print()  # Retour de ligne
            if rangee_x == 0:  # Ligne horizontale de l'en-tête
                print('--+-' + '--' * self.dimension_colonne)

    def contient_cases_a_devoiler(self):
        """
        Méthode qui indique si le tableau contient des cases à dévoiler.

        Returns:
            bool: True s'il reste des cases à dévoiler, False autrement.

        """
        for rangee in range(1, self.dimension_rangee + 1):
            for colonne in range(1, self.dimension_colonne + 1):
                case_xy = self.obtenir_case(rangee, colonne)
                if not case_xy.est_devoilee:
                    return True
        return False

    def devoiler_case(self, rangee_x, colonne_y):
        """
        Méthode qui dévoile le contenu de la case dont les coordonnées sont reçues en argument. Si la case ne
        contient pas de mine, on décrémente l'attribut qui représente le nombre de cases sans mine à dévoiler.
        Aussi, si cette case n'est voisine d'aucune mine, on dévoile ses voisins.

        Args:
            rangee_x (int) : Numéro de la rangée de la case à dévoiler
            colonne_y (int): Numéro de la colonne de la case à dévoiler
        """
        case_xy = self.obtenir_case(rangee_x, colonne_y)
        case_xy.devoiler()

        if not self.contient_mine(rangee_x, colonne_y):
            self.nombre_cases_sans_mine_a_devoiler -= 1
        if case_xy.nombre_mines_voisines == 0:
            voisins = self.obtenir_voisins(rangee_x, colonne_y)
            for case_voisin in voisins:
                case_xy = self.obtenir_case(case_voisin[0], case_voisin[1])
                if not case_xy.est_devoilee:
                    self.nombre_cases_sans_mine_a_devoiler -= 1
                    case_xy.devoiler()

    def contient_mine(self, rangee_x, colonne_y):
        """
        Méthode qui vérifie si la case dont les coordonnées sont reçues en argument contient une mine.

        Args:
            rangee_x (int) : Numéro de la rangée de la case dont on veut vérifier si elle contient une mine
            colonne_y (int): Numéro de la colonne de la case dont on veut vérifier si elle contient une mine

        Returns:
            bool: True si la case à ces coordonnées (x, y) contient une mine, False autrement.
        """
        case_xy = self.obtenir_case(rangee_x, colonne_y)
        return case_xy.est_minee


#### Tests unitaires (à compléter) ###

def test_initialisation():
    tableau_test = Tableau()

    assert tableau_test.contient_cases_a_devoiler()
    assert tableau_test.nombre_cases_sans_mine_a_devoiler == tableau_test.dimension_colonne * \
           tableau_test.dimension_rangee - tableau_test.nombre_mines


def test_valider_coordonnees():
    tableau_test = Tableau()
    dimension_x, dimension_y = tableau_test.dimension_rangee, tableau_test.dimension_colonne

    assert tableau_test.valider_coordonnees(dimension_x, dimension_y)
    assert not tableau_test.valider_coordonnees(dimension_x + 1, dimension_y)
    assert not tableau_test.valider_coordonnees(dimension_x, dimension_y + 1)
    assert not tableau_test.valider_coordonnees(-dimension_x, dimension_y)
    assert not tableau_test.valider_coordonnees(0, 0)


def test_obtenir_voisins():
    tableau_test = Tableau()

    assert tableau_test.obtenir_voisins(1, 1) == [(1, 2), (2, 1), (2, 2)]
    assert tableau_test.obtenir_voisins(1, 3) == [(1, 2), (1, 4), (2, 2), (2, 3), (2, 4)]
    assert tableau_test.obtenir_voisins(1, 5) == [(1, 4), (2, 4), (2, 5)]
    assert tableau_test.obtenir_voisins(5, 5) == [(4, 4), (4, 5), (5, 4)]
    assert tableau_test.obtenir_voisins(3, 3) == [(2, 2), (2, 3), (2, 4), (3, 2), (3, 4), (4, 2), (4, 3), (4, 4)]


def test_valider_coordonnees_a_devoiler():
    tableau_test = Tableau()

    tableau_test.initialiser_tableau()
    case_1 = tableau_test.obtenir_case(1, 1)
    case_1.devoiler()
    case_2 = tableau_test.obtenir_case(3, 2)
    case_2.devoiler()

    assert not tableau_test.valider_coordonnees_a_devoiler(1, 1)
    assert not tableau_test.valider_coordonnees_a_devoiler(3, 2)
    assert tableau_test.valider_coordonnees_a_devoiler(3, 3)
    assert not tableau_test.valider_coordonnees_a_devoiler(3, 6)


def test_devoiler_case():
    print('\ntest_devoiler_case:')
    tableau_test = Tableau()

    tableau_test.initialiser_tableau()
    case_1 = tableau_test.obtenir_case(1, 1)
    case_1.est_minee = False

    tableau_test.devoiler_case(1, 1)
    print('\nAfficher tableau -> test_devoiler_case:')
    tableau_test.afficher_tableau()


def test_case_contient_mine():
    tableau_test = Tableau()

    tableau_test.initialiser_tableau()
    case_1 = tableau_test.obtenir_case(1, 1)
    case_1.est_minee = True
    case_2 = tableau_test.obtenir_case(3, 2)
    case_2.est_minee = False

    assert tableau_test.contient_mine(1, 1)
    assert not tableau_test.contient_mine(3, 2)


if __name__ == '__main__':
    # Cles cinq prochaines lignes de code sont là pour vous aider à tester votre
    # première tentative d'implémentation des méthodes initialiser_tableau et afficher_tableau.

    tableau_test = Tableau()
    print('\nTABLEAU:')
    tableau_test.afficher_tableau()
    print('\nSOLUTION:')
    tableau_test.afficher_solution()

    print('Tests unitaires...')
    test_initialisation()
    test_valider_coordonnees()
    test_obtenir_voisins()
    test_valider_coordonnees_a_devoiler()
    test_devoiler_case()
    test_case_contient_mine()
    print('Tests réussis!')