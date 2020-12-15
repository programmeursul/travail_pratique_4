"""
TODO: Ce fichier présente une ébauche d'interface pour le TP4. Vous pouvez le modifier à souhait.
N'oubliez pas de commenter le code!
"""
from tkinter import Tk, Frame, Button, Label, StringVar
from tableau import Tableau
from bouton_case import BoutonCase
from tkinter import ttk
import time


class InterfacePartie(Tk):
    def __init__(self):
        super().__init__()

        # Nom de la fenêtre.
        self.title("Démineur")
        self.resizable(0,0)

        self.tableau_mines = Tableau()

        bouton_frame = Frame(self)
        bouton_frame.grid()

        bouton_nouvelle_partie = Button(bouton_frame, text='Nouvelle partie', command=self.nouvelle_partie)
        bouton_nouvelle_partie.grid(row=0, column=0)

        bouton_quitter = Button(bouton_frame, text="Quitter", command=self.quitter)
        bouton_quitter.grid(row=0, column=1)

        bouton_info = Button(bouton_frame, text="Instructions", command=self.instructions)
        bouton_info.grid(row=0, column=2)

        bouton_save = Button(bouton_frame, text="Sauvegarder",command=self.sauvegarder)
        bouton_save.grid(row=1, column=0)

        self.tour = 0
        #labelVar = StringVar()
        #compte = "Nombre de tours joués = 0"
        #labelVar.set(compte)
        #ompteur = Label(bouton_frame, textvariable = labelVar)
        #compteur.grid(row=0, column=3)

        self.base_string_clock = "Temp écoulé ="
        self.start = time.time()
        self.horloge = ttk.Label(text=self.base_string_clock)
        self.horloge.grid(row=0, column=4)


        self.temps_total = 1000
        self.base_string_countdown = "Temp restant ="
        self.countdown = ttk.Label(text=self.base_string_countdown)
        self.countdown.grid(row=1, column=4)



        self.update_clock()
        self.contre_la_monte()  # Enlever d'ici et placer dans une condition if pour choisir le type de jeux

        self.cadre = Frame(self)
        self.cadre.grid(padx=10, pady=10)

        self.dictionnaire_boutons = {}

        for i in range(self.tableau_mines.dimension_rangee):
            for j in range(self.tableau_mines.dimension_colonne):
                bouton = BoutonCase(self.cadre, i+1, j+1)
                bouton.grid(row=i, column=j)
                bouton.bind('<Button-1>', self.devoiler_case)
                bouton['bg'] = "#737373"
                self.dictionnaire_boutons[(i+1, j+1)] = bouton

    def update_clock(self):
        now = time.time()
        start = self.start
        elapsed = str(int(now - start))
        self.horloge.configure(text=self.base_string_clock + elapsed + "s")
        if int(now - start) < self.temps_total:
            self.after(1000, self.update_clock)

    def contre_la_monte(self):
        now = time.time()
        elapsed_2 = int(now - self.start)
        restant = self.temps_total-elapsed_2
        if restant > 0:
            restant = str(restant)
        else:
            restant = "0"
        if self.temps_total-elapsed_2 == 0:
            popup = Tk()
            popup.wm_title("Temps écoulé!")
            msg = "Temp écoulé! Vous avez perdu!"
            NORM_FONT = ("Verdana", 10)
            label = ttk.Label(popup, text=msg, font=NORM_FONT)
            label.pack(side="top", fill="x", pady=10)
            B1 = ttk.Button(popup, text="Ok :(", command=self.quit)
            B1.pack()
            self.countdown.configure(text=self.base_string_countdown + restant + "s", foreground="red")
        self.countdown.configure(text=self.base_string_countdown + restant + "s")
        self.after(1000, self.contre_la_monte)




    def devoiler_case(self, event):
        bouton = event.widget
        self.compteur_tour()
        case = self.tableau_mines.obtenir_case(bouton.rangee_x, bouton.colonne_y)
        if case.est_minee:
            bouton['text'] = "M"
            bouton['bg'] = "red"
            self.defaite()

        if not self.tableau_mines.contient_mine(bouton.rangee_x, bouton.colonne_y):
            self.tableau_mines.nombre_cases_sans_mine_a_devoiler -= 1
            bouton['text'] = case.nombre_mines_voisines
            bouton['fg'] = self.color_choser(case.nombre_mines_voisines)
        if case.nombre_mines_voisines == 0:
            voisins = self.tableau_mines.obtenir_voisins(bouton.rangee_x, bouton.colonne_y)
            for case_voisin in voisins:
                case = self.tableau_mines.obtenir_case(case_voisin[0], case_voisin[1])
                if not case.est_devoilee:
                    bouton = self.dictionnaire_boutons[case_voisin[0],case_voisin[1]]
                    self.tableau_mines.nombre_cases_sans_mine_a_devoiler -= 1
                    bouton['text'] = case.nombre_mines_voisines
                    bouton['fg'] = self.color_choser(case.nombre_mines_voisines)

        if self.tableau_mines.nombre_cases_sans_mine_a_devoiler == 0:
            self.victoire()


    def color_choser(self,nb_voisins):
        if nb_voisins == 0:
            color = "#33cc33"

        if nb_voisins == 1:
            color = "#66ff33"

        if nb_voisins == 2:
            color = "#99ff33"

        if nb_voisins == 3:
            color = "#ff9900"

        if nb_voisins == 4:
            color = "#ff6600"

        if nb_voisins == 5:
            color = "#ff0000"

        if nb_voisins == 6:
            color = "black"


        return color



    def defaite(self):

        for i in range(self.tableau_mines.dimension_rangee):
            for j in range(self.tableau_mines.dimension_colonne):
                case = self.tableau_mines.obtenir_case(i+1, j+1)
                if not case.est_devoilee:
                    bouton = self.dictionnaire_boutons[i+1, j+1]
                    if case.est_minee:
                        bouton['text'] = "M"
                        bouton['bg'] = "red"
                    else:
                        bouton['text'] = case.nombre_mines_voisines
                        bouton['fg'] = self.color_choser(case.nombre_mines_voisines)

        popup = Tk()
        popup.wm_title("Défaite")
        msg = "Vous avez perdu!"
        NORM_FONT = ("Verdana", 10)
        label = ttk.Label(popup, text=msg, font=NORM_FONT)
        label.pack(side="top", fill="x", pady=10)
        B1 = ttk.Button(popup, text="Ok :(", command=self.quit)
        B1.pack()

    def victoire(self):
        popup = Tk()
        popup.wm_title("Victoire!")
        msg = "Vous avez gagné!"
        NORM_FONT = ("Verdana", 10)
        label = ttk.Label(popup, text=msg, font=NORM_FONT)
        label.pack(side="top", fill="x", pady=10)
        B1 = ttk.Button(popup, text="Ok :)", command=self.quit)
        B1.pack()


    def nouvelle_partie(self):
        self.tableau_mines = Tableau()

        for bouton in self.dictionnaire_boutons.values():
            bouton['text'] = " "

    def compteur_tour(self):
        self.tour += 1
        compte = "Nombre de tours joués = % 2d" % self.tour
        compteur = Label(self, text=compte)
        compteur['text'] = compte
        compteur.grid(row=2, column=4)

    def sauvegarder(self):
        popup = Tk()
        popup.wm_title("Sauvegarder")
        NORM_FONT = ("Verdana", 10)
        label = ttk.Label(popup, text="Nom du fichier :", font=NORM_FONT)
        label.pack(side="top", pady=10)
        entree = StringVar()
        B1 = ttk.Entry(popup,textvariable = entree)
        B1.pack()
        B2 = ttk.Button(popup, text="Sauvegarder", command=popup.destroy)
        B2.pack()
        label = ttk.Label(popup, text="Le fichier sera sauvegardé dans le même répertoire que principal.py", font= ("Verdana", 8))
        label.pack(side="bottom", pady=10)





    def quitter(self):
        popup = Tk()
        popup.wm_title("Quitter?")
        msg = "Etes vous certain de vouloir quitter?"
        NORM_FONT = ("Verdana", 10)
        label = ttk.Label(popup, text=msg, font=NORM_FONT)
        label.pack(side="top", fill="x", pady=10)
        B1 = ttk.Button(popup, text="Oui", command=self.quit)
        B1.pack(side="left")
        B2 = ttk.Button(popup, text="Non", command=popup.destroy)
        B2.pack(side="right")


    def instructions(self):
        popup = Tk()
        popup.wm_title("Règles")
        msg = """                                                         -_-_-_-_- Règles du jeu -_-_-_-_- \n
        Le but du jeux est de découvrir toutes les cases ne contenant pas de mines en cliquant dessus.
        
        Lorsque vous cliquez sur une case qui n'est pas une mine, le nombre affiché dans la case correspond au
        nombre de mines voisines. Notez que le voisinage d'une mine comprend aussi les diagonales. Si vous 
        sélectionnez une case avec une mine, vous perdez. 
                                                                                                                                                              
        """
        NORM_FONT = ("Verdana", 10)
        label = ttk.Label(popup, text=msg, font=NORM_FONT)
        label.pack(side="top", fill="x", pady=10)
        B1 = ttk.Button(popup, text="Retour au jeu", command=popup.destroy)
        B1.pack(side="bottom")


