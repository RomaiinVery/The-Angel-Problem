import tkinter as tk
import random as rd

## Précisions sur le programme :

####################
#
# - Avec un pouvoir > 1, le programme a quelques problèmes de cohérence (notamment sur les mouvements de l'ange)
#
#
####################

class Ange:

    def __init__(self, n, taille):
        """
        @param n : entier correspondant au pouvoir de l'ange
        @param taille : entier correspondant aux dimensions du quadrillage (taille x taille)
        """

        self.pouvoir = n
        self.jeu = Affiche(taille, n)
        self.taille = taille + n

        self.jeu.button.config(command=self.tour)

        # Placement de l'Ange au milieu du quadrillage
        i = self.taille // 2
        self.jeu.tab[i+1][i+1] = 2
        self.jeu.affichage(i+1, i+1)
        # Lancement du jeu
        self.jeu.mainloop()

    def coordAngeTab(self):
        """
        Renvois les coordonnées i, j de l'Ange sur le tableau
        @return i,j : entiers corrspondants aux coordonnées de l'ange
        """
        for i in range(len(self.jeu.tab)):
            for j in range(len(self.jeu.tab)):

                if self.jeu.tab[i][j] == 2:
                    return i, j

    #### Les 5 prochaines fonctions calculent un chemin optimal pour l'ange,
    #### 4 fonctions de création d'une matrice et une fonction de reconstruction
    #### Les 4 fonctions complètent une à une la matrice en partant de la case de l'Ange pour s'étendre jusqu'aux bords

    def calculCaseHG(self,tab_min,i,j):
        """
        @param tab_min : matrice à compléter
        @param i,j : entiers, coordonnées de l'ange
        @return : matrice complétée en haut à gauche
        """
        #On parcourt la matrice
        for x in range(i):
            for y in range(j):
                #Si la case n'est pas brûlé
                if self.jeu.tab[i-x][j-y] == 0:
                    #On cherche le nombre le plus petit entre la case actuelle et les cases adjacentes +1
                    nb = min(tab_min[i-x][j-y-1]+1 , tab_min[i-x][j-y+1]+1 , tab_min[i-x+1][j-y]+1 , tab_min[i-x-1][j-y]+1 , tab_min[i-x][j-y])
                    tab_min[i-x][j-y] = nb
        return tab_min

    def calculCaseHD(self,tab_min,i,j):
        """
        @param tab_min : matrice à compléter
        @param i,j : entiers, coordonnées de l'ange
        @return : matrice complétée en haut à droite
        """
        #On parcourt la matrice
        for x in range(i):
            for y in range(self.taille - j):
                #Si la case n'est pas brûlé
                if self.jeu.tab[i-x][j+y] == 0:
                    #On cherche le nombre le plus petit entre la case actuelle et les cases adjacentes +1
                    nb = min(tab_min[i-x][j+y+1]+1 , tab_min[i-x][j+y-1]+1 , tab_min[i-x+1][j+y]+1 , tab_min[i-x-1][j+y]+1 , tab_min[i-x][j+y])
                    tab_min[i-x][j+y] = nb
        return tab_min

    def calculCaseBG(self,tab_min,i,j):
        """
        @param tab_min : matrice à compléter
        @param i,j : entiers, coordonnées de l'ange
        @return : matrice complétée en bas à gauche
        """
        #On parcourt la matrice
        for x in range(self.taille - i):
            for y in range(j):
                #Si la case n'est pas brûlé
                if self.jeu.tab[i+x][j-y] == 0:
                    #On cherche le nombre le plus petit entre la case actuelle et les cases adjacentes +1
                    nb = min(tab_min[i+x][j-y-1]+1 , tab_min[i+x][j-y+1]+1 , tab_min[i+x-1][j-y]+1 , tab_min[i+x+1][j-y]+1 , tab_min[i+x][j-y])
                    tab_min[i+x][j-y] = nb
        return tab_min

    def calculCaseBD(self,tab_min,i,j):
        """
        @param tab_min : matrice à compléter
        @param i,j : entiers, coordonnées de l'ange
        @return : matrice complétée en bas à droite
        """
        #On parcourt la matrice
        for x in range(self.taille - i):
            for y in range(self.taille - j):
                #Si la case n'est pas brûlé
                if self.jeu.tab[i+x][j+y] == 0:
                    #On cherche le nombre le plus petit entre la case actuelle et les cases adjacentes +1
                    nb = min(tab_min[i+x][j+y-1]+1 , tab_min[i+x][j+y+1]+1 , tab_min[i+x-1][j+y]+1 , tab_min[i+x+1][j+y]+1 , tab_min[i+x][j+y])
                    tab_min[i+x][j+y] = nb
        return tab_min

    def caseAlea(self,i,j):
        """
        Solution au cas où le programme dynamique et la reconstruction ne fonctionne pas
        Détermine une direction aléatoire possible
        @param i,j : entiers, coordonnées de l'ange
        @return : chaine de caractères définissant une direction
        """
        if self.jeu.tab[i+1][j] == 0:
            return 'bas'
        elif self.jeu.tab[i-1][j] == 0:
            return 'haut'
        elif self.jeu.tab[i][j-1] == 0:
            return 'gauche'
        elif self.jeu.tab[i][j+1] == 0:
            return 'droite'

    def reconstruction(self,tab):
        """
        Reconstruit le chemin pour renvoyer la direction où l'ange doit aller
        @param tab : matrice
        @return : chaîne de caractère indiquant la direction où l'ange doit aller
        """
        nb = 99
        ### On cherche le minimum dans les bordures du tableau
        for a in range(1,self.taille):
            if tab[1][a] < nb:
                nb = tab[1][a]
            if tab[self.taille-1][a] < nb:
                nb = tab[self.taille-1][a]
            if tab[a][1] < nb:
                nb = tab[a][1]
            if tab[a][self.taille-1] < nb:
                nb = tab[a][self.taille-1]

        ### On a le minimum, on cherche d'où il vient
        for a in range(1,self.taille):
            if nb == tab[1][a]:
                i = 1
                j = a
            elif nb == tab[self.taille-1][a]:
                i = self.taille-1
                j = a
            elif nb == tab[a][1]:
                i = a
                j = 1
            elif nb == tab[a][self.taille-1]:
                i = a
                j = self.taille-1

        ### On a la case de départ, et on démarre la reconstruction jusqu'au 0 (jusqu'à l'ange)
        while tab[i][j] > 1:
            if tab[i+1][j] == tab[i][j]-1:
                i = i + 1
            elif tab[i-1][j] == tab[i][j]-1:
                i = i - 1
            elif tab[i][j+1] == tab[i][j]-1:
                j = j + 1
            elif tab[i][j-1] == tab[i][j]-1:
                j = j - 1

        ### On cherche où se trouve l'ange par rapport à la dernière case qui vaut 1
        if tab[i-1][j] == 0:
            return 'bas'
        elif tab[i+1][j] == 0:
            return 'haut'
        elif tab[i][j-1] == 0:
            return 'droite'
        elif tab[i][j+1] == 0:
            return 'gauche'
        else:
            return self.caseAlea(i,j)

    def angeDirection(self, i, j):
        """
        Renvoie la direction où l'ange doit aller selon les précédentes fonctions
        @param i,j : coordonnées de l'ange
        @return direction : chaîne de caractère indiquant la direction où l'ange doit aller
        """
        tab_min = [[99 for x in range(self.taille + 1)] for y in range(self.taille + 1)]
        tab_min[i][j] = 0
        #On crée la matrice des chemins
        tab = self.calculCaseHG(tab_min,i,j)
        tab = self.calculCaseHD(tab,i,j)
        tab = self.calculCaseBG(tab,i,j)
        tab = self.calculCaseBD(tab,i,j)
        # for l in tab:
        #     print(l)
        #On utilise cette matrice pour reconstruire le chemin optimal et en déduire une direction
        direction = self.reconstruction(tab)
        return direction

    def demonAttaque(self,i,j):
        """
        Renvoie la direction où l'ange doit aller selon les précédentes fonctions
        @param i,j : coordonnées de l'ange
        @return direction : chaine de caractère qui détermine la direction de la case à brûler
        """
        d = []
        direction = []
        distance_haut = i
        distance_bas = len(self.jeu.tab) - i - 1
        distance_gauche = j
        distance_droite = len(self.jeu.tab) - j - 1
        d.append(distance_haut)
        d.append(distance_bas)
        d.append(distance_gauche)
        d.append(distance_droite)
        tab_d = ['haut','bas','gauche','droite']

        #tri par insertion de 'd' lié à 'tab_d'
        for i in range(1, len(d)):
            k = d[i]
            l = tab_d[i]
            j = i-1
            while j >= 0 and k < d[j]:
                d[j+1] = d[j]
                tab_d[j+1] = tab_d[j]
                j = j -1
            d[j+1] = k
            tab_d[j+1] = l
        # Variante de l'IA : on regarde si l'ange est à équidistance de deux bordures
        if d[0] == d[1]:
            if tab_d[0] == 'haut' and tab_d[1] == 'gauche' or tab_d[0] == 'gauche' and tab_d[1] == 'haut':
                direction.append('haut-gauche')
            elif tab_d[0] == 'haut' and tab_d[1] == 'droite' or tab_d[0] == 'droite' and tab_d[1] == 'haut':
                direction.append('haut-droite')
            elif tab_d[0] == 'bas' and tab_d[1] == 'gauche' or tab_d[0] == 'gauche' and tab_d[1] == 'bas':
                direction.append('bas-gauche')
            elif tab_d[0] == 'bas' and tab_d[1] == 'droite' or tab_d[0] == 'droite' and tab_d[1] == 'bas':
                direction.append('bas-droite')
        # Puis on ajoute dans l'ordre les directions dans l'ordre du tri par insertion
        for dire in tab_d:
            direction.append(dire)
        return direction

    def angeBloque(self,i,j):
        """
        Vérifie si l'ange est bloqué ou non
        @param i,j : coordonnées de l'ange
        @return : bool True si l'ange est bloqué
        """
        x = self.pouvoir
        #On regarde si les cases entourant l'ange sont des cases brûlées
        if self.jeu.tab[i-x][j] == 1 and self.jeu.tab[i+x][j] == 1 and self.jeu.tab[i][j-x] == 1 and self.jeu.tab[i][j+x] == 1:
            return True
        else:
            return False

    def angeGagne(self,i,j):
         """
         Vérifie si l'ange a gagné
         @param i,j : coordonnées de l'ange
         @return : bool True si l'ange a gagné
         """
         i, j = self.coordAngeTab()
         #On regarde si l'ange est sur une bordure du quadrillage
         if i == 0 or j == 0 or i == len(self.jeu.tab) - 1 or j == len(self.jeu.tab) - 1:
             return True
         else:
             return False

    def tour(self):
        """
        Active le déplacement de l'ange, puis l'action du démon
        """

        i, j = self.coordAngeTab()
        x = self.pouvoir

        # L'Ange se déplace
        d = self.angeDirection(i, j)
        if d == 'haut':
            while x > 0:
                if self.jeu.tab[i - x][j] == 0:
                    self.jeu.tab[i][j] = 0
                    self.jeu.affichage(i, j)
                    self.jeu.tab[i - x][j] = 2
                    self.jeu.affichage(i - x, j)
                    break
                else:
                        x = x - 1

        elif d == 'bas':
            while x > 0:
                if self.jeu.tab[i + x][j] == 0:
                    self.jeu.tab[i][j] = 0
                    self.jeu.affichage(i, j)
                    self.jeu.tab[i + x][j] = 2
                    self.jeu.affichage(i + x, j)
                    break
                else:
                    x = x - 1

        elif d == 'gauche':
            while x > 0:
                if self.jeu.tab[i][j - x] == 0:
                    self.jeu.tab[i][j] = 0
                    self.jeu.affichage(i, j)
                    self.jeu.tab[i][j - x] = 2
                    self.jeu.affichage(i, j - x)
                    break
                else:
                    x = x - 1

        elif d == 'droite':
            while x > 0:
                if self.jeu.tab[i][j + x] == 0:
                    self.jeu.tab[i][j] = 0
                    self.jeu.affichage(i, j)
                    self.jeu.tab[i][j + x] = 2
                    self.jeu.affichage(i, j + x)
                    break
                else:
                    x = x - 1

        ### Jeu du démon
        i,j = self.coordAngeTab()
        direction = self.demonAttaque(i,j)
        for d in direction:
            if d == 'haut':
                if self.jeu.tab[i - x][j] == 0:
                    self.jeu.tab[i - x][j] = 1
                    self.jeu.affichage(i - x, j)
                    break
            elif d == 'bas':
                if self.jeu.tab[i + x][j] == 0:
                    self.jeu.tab[i + x][j] = 1
                    self.jeu.affichage(i + x, j)
                    break

            elif d == 'gauche':
                if self.jeu.tab[i][j - x] == 0:
                    self.jeu.tab[i][j - x] = 1
                    self.jeu.affichage(i, j - x)
                    break

            elif d == 'droite':
                if self.jeu.tab[i][j + x] == 0:
                    self.jeu.tab[i][j + x] = 1
                    self.jeu.affichage(i, j + x)
                    break

            elif d == 'haut-gauche':
                if self.jeu.tab[i - x][j - x] == 0:
                    self.jeu.tab[i - x][j - x] = 1
                    self.jeu.affichage(i - x, j - x)
                    break

            elif d == 'haut-droite':
                if self.jeu.tab[i - x][j + x] == 0:
                    self.jeu.tab[i - x][j + x] = 1
                    self.jeu.affichage(i - x, j + x)
                    break

            elif d == 'bas-gauche':
                if self.jeu.tab[i + x][j - x] == 0:
                    self.jeu.tab[i + x][j - x] = 1
                    self.jeu.affichage(i + x, j - x)
                    break

            elif d == 'bas-droite':
                if self.jeu.tab[i + x][j + x] == 0:
                    self.jeu.tab[i + x][j + x] = 1
                    self.jeu.affichage(i + x, j + x)
                    break

        # On met à jour l'affichage
        self.jeu.affichage(i, j)

        # On verifie si l'Ange est bloqué
        bloque = self.angeBloque(i,j)
        if bloque:
            self.jeu.button.config(text="Fin", command=self.fin)
            return

        # On vérifie si l'Ange a gagné
        ange_gagne = self.angeGagne(i,j)
        if ange_gagne:
            self.jeu.button.config(text="Fin", command=self.fin)


    def fin(self):
        """
        Fin du jeu
        """
        self.jeu.quit()


class Affiche(tk.Tk):

    def __init__(self, taille, pouvoir):

        tk.Tk.__init__(self)
        self.pouvoir = pouvoir

        # Paramètres de la fenètre
        # self.geometry('700x500')
        self.title("Ange et Démon")

        # Texte
        self.titre = tk.Label(text="Ange et Démon")
        self.titre.grid(row=0, column=3)

        # Bouton
        self.button = tk.Button(text="Next")
        self.button.grid(row=2, column=4)

        # Tableau et création du grillage
        self.taille = taille + pouvoir
        self.tab = self.tableau(self.taille)

    def tableau(self, taille):

        # créer une liste de liste
        tab = [[0 for i in range(taille + 2)] for i in range(taille + 2)]

        # créer le grillage

        self.can = tk.Canvas(self, width=taille * 10 + 20, height=taille * 10 + 20, bg="yellow")
        self.can.grid(row=1, column=0, columnspan=7)

        for i in range(taille):
            for j in range(taille):
                tk.Canvas.create_rectangle(self.can, i * 10 + 10, j * 10 + 10, i * 10 + 20, j * 10 + 20,
                                           outline="black", fill="white")
        return tab

    def affichage(self, i, j):

        # Réinitialiser une case
        if self.tab[i][j] == 0:
            tk.Canvas.create_rectangle(self.can, j * 10, i * 10, j * 10 + 10, i * 10 + 10,
                                       outline="black", fill="white")

        # Si c'est une case brûlée
        if self.tab[i][j] == 1:
            tk.Canvas.create_rectangle(self.can, j * 10, i * 10, j * 10 + 10, i * 10 + 10,
                                       outline="red", fill="red")

        # Si c'est l'Ange
        if self.tab[i][j] == 2:
            tk.Canvas.create_rectangle(self.can, j * 10, i * 10, j * 10 + 10, i * 10 + 10,
                                       outline="gray", fill="green")


taille = 20
pouvoir = 1
Ange(pouvoir, taille)
