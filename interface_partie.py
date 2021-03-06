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
        self.couleur_tableau = "#737373"
        self.couleur_mine = "#ff0000"
        bouton_frame = Frame(self)
        bouton_frame.grid()

        bouton_nouvelle_partie = Button(bouton_frame, text='Nouvelle partie', command=self.nouvelle_partie)
        bouton_nouvelle_partie.grid(row=0, column=0)

        bouton_quitter = Button(bouton_frame, text="Quitter", command=self.quitter)
        bouton_quitter.grid(row=0, column=1)

        bouton_info = Button(bouton_frame, text="Instructions", command=self.instructions)
        bouton_info.grid(row=0, column=2)

        bouton_save = Button(bouton_frame, text="Sauvegarder",command=self.sauvegarder_popup)
        bouton_save.grid(row=1, column=0)

        bouton_charger = Button(bouton_frame, text="Charger", command=self.charger_popup)
        bouton_charger.grid(row=1, column=1)

        bouton_configurer = Button(bouton_frame, text="Configurer", command=self.configurer_popup)
        bouton_configurer.grid(row=1, column=2)

        self.tour = 0
        self.compteur_tour()

        self.base_string_clock = "Temp écoulé ="
        self.start = time.time()
        self.horloge = ttk.Label(text=self.base_string_clock)
        self.horloge.grid(row=0, column=4)

        self.temps_total = 1000
        self.base_string_countdown = "Temp restant ="
        self.countdown = ttk.Label(text=self.base_string_countdown)
        self.countdown.grid(row=1, column=4)

        self.update_clock()
        self.contre_la_montre()

        self.cadre = Frame(self)
        self.cadre.grid(padx=10, pady=10)

        self.dictionnaire_boutons = {}

        for i in range(self.tableau_mines.dimension_rangee):
            for j in range(self.tableau_mines.dimension_colonne):
                bouton = BoutonCase(self.cadre, i+1, j+1)
                bouton.grid(row=i, column=j)
                bouton.bind('<Button-1>', self.devoiler_case)
                bouton['bg'] = self.couleur_tableau
                self.dictionnaire_boutons[(i+1, j+1)] = bouton

    def update_clock(self):
        now = time.time()
        start = self.start
        elapsed = str(int(now - start))
        self.horloge.configure(text=self.base_string_clock + elapsed + "s")
        if int(now - start) < self.temps_total:
            self.after(1000, self.update_clock)

    def contre_la_montre(self):
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
        self.after(1000, self.contre_la_montre)

    def devoiler_case(self, event):
        bouton = event.widget
        self.compteur_tour()
        case = self.tableau_mines.obtenir_case(bouton.rangee_x, bouton.colonne_y)
        if case.est_minee:
            bouton['text'] = "M"
            bouton['bg'] = self.couleur_mine
            self.defaite()
        else:
            if not self.tableau_mines.contient_mine(bouton.rangee_x, bouton.colonne_y):
                case = self.tableau_mines.obtenir_case(bouton.rangee_x, bouton.colonne_y)
                case.devoiler()
                self.tableau_mines.nombre_cases_sans_mine_a_devoiler -= 1
                bouton['text'] = case.nombre_mines_voisines
                bouton['fg'] = self.color_choser(case.nombre_mines_voisines)
            if case.nombre_mines_voisines == 0:
                voisins = self.tableau_mines.obtenir_voisins(bouton.rangee_x, bouton.colonne_y)
                for case_voisin in voisins:
                    case = self.tableau_mines.obtenir_case(case_voisin[0], case_voisin[1])
                    if not case.est_devoilee:
                        case.devoiler()
                        bouton = self.dictionnaire_boutons[case_voisin[0],case_voisin[1]]
                        self.tableau_mines.nombre_cases_sans_mine_a_devoiler -= 1
                        bouton['text'] = case.nombre_mines_voisines
                        bouton['fg'] = self.color_choser(case.nombre_mines_voisines)

            if self.tableau_mines.nombre_cases_sans_mine_a_devoiler == 0:
                self.victoire()

    def color_choser(self,nb_voisins):
        color = "#33cc33"
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
                        bouton['bg'] = self.couleur_mine
                    else:
                        bouton['text'] = case.nombre_mines_voisines
                        bouton['fg'] = self.color_choser(case.nombre_mines_voisines)

        popup = Tk()
        popup.wm_title("Défaite")
        msg = "Vous avez perdu!"
        NORM_FONT = ("Verdana", 10)
        label = ttk.Label(popup, text=msg, font=NORM_FONT)
        label.pack(side="top", fill="x", pady=10)
        B1 = ttk.Button(popup, text="Ok :(", command=lambda:self.ferme_fenetre_dialogue(popup))
        B1.pack()

    def close_window(self, window):
        self.window.destroy()
        
    def victoire(self):
        popup = Tk()
        popup.wm_title("Victoire!")
        msg = "Vous avez gagné!"
        NORM_FONT = ("Verdana", 10)
        label = ttk.Label(popup, text=msg, font=NORM_FONT)
        label.pack(side="top", fill="x", pady=10)
        B1 = ttk.Button(popup, text="Ok :)", command=lambda:self.ferme_fenetre_dialogue(popup))
        B1.pack()

    def nouvelle_partie(self):
        self.fenetre_dialogue = Tk()
        self.fenetre_dialogue.resizable(width=False, height=False)
        self.fenetre_dialogue.wm_title("Nouvelle partie")
        
        # Les widgets de la fenetre dialogue 
        ttk.Label(self.fenetre_dialogue, text='Entrez le numéro de colonne').grid(row=0, column=0, pady=10)
        self.entree_colonne = ttk.Entry(self.fenetre_dialogue)
        self.entree_colonne.grid(row=0, column=1, padx=10)
        ttk.Label(self.fenetre_dialogue, text='Entrez le numéro de ligne').grid(row=1, column=0, pady=10)
        self.entree_ligne = ttk.Entry(self.fenetre_dialogue)
        self.entree_ligne.grid(row=1, column=1, padx=10)
        ttk.Label(self.fenetre_dialogue, text='Entrez le nombre de mines').grid(row=2, column=0, pady=10)
        self.entree_nombre_mines = ttk.Entry(self.fenetre_dialogue)
        self.entree_nombre_mines.grid(row=2, column=1, padx=10)        
        ttk.Button(self.fenetre_dialogue, text="Commencer!", command=self.commencer).grid(row=3, column=0, pady=10)
        
        self.wait_window(self.fenetre_dialogue)

    def commencer(self):
        # On sauvegarde le contenu des Entry dans les attributs
        self.entree_colonne = int(self.entree_colonne.get())
        self.entree_ligne = int(self.entree_ligne.get())
        self.entree_nombre_mines = int(self.entree_nombre_mines.get())
                
        self.fenetre_dialogue.destroy()
        
        self.tableau_mines = Tableau(self.entree_ligne,self.entree_colonne,self.entree_nombre_mines)
        
        self.cadre.destroy()
        self.cadre = Frame(self)
        self.cadre.grid(padx=10, pady=10)
        
        self.tour = 0
        self.compteur_tour()
        self.start = time.time()
        self.dictionnaire_boutons = {}

        for i in range(self.tableau_mines.dimension_rangee):
            for j in range(self.tableau_mines.dimension_colonne):
                bouton = BoutonCase(self.cadre, i+1, j+1)
                bouton.grid(row=i, column=j)
                bouton.bind('<Button-1>', self.devoiler_case)
                bouton['bg'] = self.couleur_tableau
                self.dictionnaire_boutons[(i+1, j+1)] = bouton
                
        for bouton in self.dictionnaire_boutons.values():
            bouton['text'] = " "
    
    def compteur_tour(self):
        compte = "Nombre de tours joués = % 2d" % self.tour
        compteur = Label(self, text=compte)
        compteur['text'] = compte
        compteur.grid(row=2, column=4)
        self.tour += 1
         
    def sauvegarder_popup(self):
        popup = Tk()
        popup.wm_title("Sauvegarder")
        NORM_FONT = ("Verdana", 10)
        label = ttk.Label(popup, text="Nom du fichier :", font=NORM_FONT)
        label.pack(side="top", pady=10)
        entree = StringVar(popup)
        B1 = ttk.Entry(popup,textvariable = entree)
        B1.pack()
        B2 = ttk.Button(popup, text="Sauvegarder", command=lambda :[self.sauvegarder(entree),popup.destroy()])
        B2.pack()
        label = ttk.Label(popup, text="Le fichier sera sauvegardé dans le même répertoire que principal.py", font= ("Verdana", 8))
        label.pack(side="bottom", pady=10)

    def sauvegarder(self,nom):
        file_name = nom.get()
        file_name = file_name +".txt"
        f = open(file_name, "w+")
        f.write(str(self.tableau_mines.dimension_rangee) +"\n")
        f.write(str(self.tableau_mines.dimension_colonne) +"\n")
        f.write(str(self.tableau_mines.nombre_mines) +"\n\n")
        
        for i in range(self.tableau_mines.dimension_rangee):
            for j in range(self.tableau_mines.dimension_colonne):
                case = self.tableau_mines.obtenir_case(i+1, j+1)
                f.write(str(case.est_minee) + "\n")
                f.write(str(case.est_devoilee) + "\n")
                if case.est_minee:
                    f.write("M" + "\n")
                else:
                    f.write(str(case.nombre_mines_voisines) + "\n")              
        f.close

    def charger_popup(self):
        popup = Tk()
        popup.wm_title("Charger")
        NORM_FONT = ("Verdana", 10)
        label = ttk.Label(popup, text="Nom du fichier :", font=NORM_FONT)
        label.pack(side="top", pady=10)
        entree = StringVar(popup)
        B1 = ttk.Entry(popup,textvariable = entree)
        B1.pack()
        B2 = ttk.Button(popup, text="Charger", command=lambda :[self.charger(entree),popup.destroy()])
        B2.pack()


    def charger(self,nom):
        file_name = nom.get()
        file_name = file_name +".txt"
        f = open(file_name, "r")
        content = f.read().splitlines()
        rangee = int(content[0])
        colonne = int(content[1])

        self.tableau_mines = Tableau(rangee,colonne,0)
        line = 4

        for i in range(self.tableau_mines.dimension_rangee):
            for j in range(self.tableau_mines.dimension_colonne):
                case = self.tableau_mines.obtenir_case(i+1, j+1)

                bouton = BoutonCase(self.cadre, i+1 , j+1 )
                bouton.grid(row=i, column=j)
                bouton.bind('<Button-1>', self.devoiler_case)
                bouton['bg'] = "#737373"
                self.dictionnaire_boutons[(i+1 , j+1 )] = bouton

                mine = content[line]

                etat = content[line+1]

                charactere = content[line+2]
                if charactere != "M":
                    case.nombre_mines_voisines=str(charactere)
                    
                case.est_minee = mine == "True"

                if etat == "True":

                    bouton['text'] = charactere
                    bouton['fg'] = self.color_choser(case.nombre_mines_voisines)
                line += 3

        f.close

    def quitter(self):
        popup = Tk()
        popup.wm_title("Quitter?")
        msg = "Etes vous certain de vouloir quitter?"
        NORM_FONT = ("Verdana", 10)
        label = ttk.Label(popup, text=msg, font=NORM_FONT)
        label.pack(side="top", fill="x", pady=10)
        B1 = ttk.Button(popup, text="Oui", command=lambda:[self.ferme_fenetre_dialogue(popup),self.ferme_fenetre_principale()])
        B1.pack(side="left")
        B2 = ttk.Button(popup, text="Non", command=lambda:self.ferme_fenetre_dialogue(popup))
        B2.pack(side="right")

    def ferme_fenetre_dialogue(self, window):
        window.destroy()

    def ferme_fenetre_principale(self):
        self.destroy()
        
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

    def configurer_popup(self):
        self.parametres_fenetre = Tk()
        self.parametres_fenetre.resizable(width=False, height=False)
        self.parametres_fenetre.wm_title("Paramètres")
        # Les widgets de la fenetre paramètres
        # Tableau
        ttk.Label(self.parametres_fenetre, text='Couleur tableau').grid(row=0, column=0, pady=10)
        self.frameRadioButton = Frame(self.parametres_fenetre)       
        self.frameRadioButton.grid(row=0, column=1)        
        self.varTableau = StringVar(self.frameRadioButton,self.couleur_tableau)
        self.radioButtonGris = ttk.Radiobutton(self.frameRadioButton, text="Grise", variable=self.varTableau, value='#737373', command=self.selectionner_couleur_tableau)
        self.radioButtonGris.grid(row=0, column=0)
        self.radioButtonBlanc = ttk.Radiobutton(self.frameRadioButton, text="Blanc", variable=self.varTableau, value='#FFFFFF', command=self.selectionner_couleur_tableau)
        self.radioButtonBlanc.grid(row=0, column=1)
        # Mines
        ttk.Label(self.parametres_fenetre, text='Couleur mines').grid(row=1, column=0, pady=10)
        self.frameRadioButtonMine = Frame(self.parametres_fenetre)       
        self.frameRadioButtonMine.grid(row=1, column=1)        
        self.varMine = StringVar(self.frameRadioButtonMine,self.couleur_mine)
        self.radioButtonRouge = ttk.Radiobutton(self.frameRadioButtonMine, text="Rouge", variable=self.varMine, value='#ff0000', command=self.selectionner_couleur_mine)
        self.radioButtonRouge.grid(row=1, column=0)
        self.radioButtonRose = ttk.Radiobutton(self.frameRadioButtonMine, text="Rose", variable=self.varMine, value='#ffc0cb', command=self.selectionner_couleur_mine)
        self.radioButtonRose.grid(row=1, column=1)
        ttk.Button(self.parametres_fenetre, text="OK", command=lambda:self.ferme_fenetre_dialogue(self.parametres_fenetre)).grid(row=3, column=0, pady=10)
                        
    def selectionner_couleur_tableau(self):
        if self.varTableau.get() == "#737373":
            self.couleur_tableau = "#737373"
        elif self.varTableau.get() == "#FFFFFF":
            self.couleur_tableau = "#FFFFFF"

    def selectionner_couleur_mine(self):
        if self.varMine.get() == "#ff0000":
            self.couleur_mine = "#ff0000"
        elif self.varMine.get() == "#ffc0cb":
           self.couleur_mine = "#ffc0cb"