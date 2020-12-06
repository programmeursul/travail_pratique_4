"""
TODO: Ce fichier présente une ébauche d'interface pour le TP4. Vous pouvez le modifier à souhait.
N'oubliez pas de commenter le code!
"""
from tkinter import Tk, Frame, Button
from tableau import Tableau
from bouton_case import BoutonCase
from tkinter import ttk

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

        self.cadre = Frame(self)
        self.cadre.grid(padx=10, pady=10)

        self.dictionnaire_boutons = {}

        for i in range(self.tableau_mines.dimension_rangee):
            for j in range(self.tableau_mines.dimension_colonne):
                bouton = BoutonCase(self.cadre, i+1, j+1)
                bouton.grid(row=i, column=j)
                bouton.bind('<Button-1>', self.devoiler_case)
                self.dictionnaire_boutons[(i+1, j+1)] = bouton

    def devoiler_case(self, event):
        bouton = event.widget
        case = self.tableau_mines.obtenir_case(bouton.rangee_x, bouton.colonne_y)
        if case.est_minee:
            bouton['text'] = "M"
        else:
            bouton['text'] = case.nombre_mines_voisines

    def nouvelle_partie(self):
        self.tableau_mines = Tableau()

        for bouton in self.dictionnaire_boutons.values():
            bouton['text'] = " "

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
        #popup.mainloop()

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


