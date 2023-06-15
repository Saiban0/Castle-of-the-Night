import pyxel

##Variables globales
max_x,max_y=128,128
class Space:
    def __init__(self):
        """
        Initialisation du jeu
        """
        pyxel.init(max_x,max_y,fps=60, title='Castle of the Night')
        self.player=Joueur(4,64) ##Création du joueur
        self.ennemis=[] ##Liste des ennemis présents
        self.missiles_ennemis=[] ##Liste des missiles ennemis
        self.missiles_joueur=[] ##Liste des missiles du joueur
        self.timer=1 ##Compte à rebours d'apparition des ennemis, *60 car 60 exécutions par seconde
        self.vague=0 ##Compteur de vagues
        self.protections=[Protection(20,10), Protection(20,100)] ##Liste des protections
        ## Liste d'affichage des coeurs, coordonnées désordonnées
        self.coeurs=[Coeur(96,16),Coeur(112,16),Coeur(120,16),Coeur(104,16),Coeur(96,24),Coeur(104,24),Coeur(112,24),Coeur(120,24),Coeur(104,32),Coeur(112,32),Coeur(120,32)]
        self.victoire=False
        pyxel.load("theme.pyxres")
        pyxel.run(self.update,self.draw)


#####################################################################################
#---------------------------------UPDATE--------------------------------------------#
#####################################################################################

    def update(self):
        """
        Mise à jour des positions et des états.
        """
        ##Inputs Joueur
        if pyxel.btn(pyxel.KEY_UP) or pyxel.btn(pyxel.KEY_Z): ##Déplacements haut
            self.player.move(-2)
        if pyxel.btn(pyxel.KEY_DOWN) or pyxel.btn(pyxel.KEY_S): ##Déplacements bas
            self.player.move(2)
        if pyxel.btnr(pyxel.KEY_SPACE) or pyxel.btnr(pyxel.MOUSE_BUTTON_LEFT): ##Tirs du joueur
            self.missiles_joueur.append(self.player.tir())

        ##Apparitions de la nouvelle vague( toutes les 5 secondes)
        self.timer-=1
        if self.timer==0 and self.vague<=5:
            vague=self.nouvelle_vague()
            self.vague+=1
            self.timer = 5 * 60
            for i in vague:
                self.ennemis.append(i)
        elif self.vague>5:
            self.victoire=True

        ## Déplacements et suppression des missiles du joueur
        for tir in self.missiles_joueur:
            if 0<=tir.x<=128 and 0<=tir.y<=128:
                if tir.x>+2:
                    tir.move(4)
                else:
                    self.missiles_joueur.remove(tir)
            else:
                self.missiles_joueur.remove(tir)

        ## Déplacements et suppresions des missiles ennemis
        for tir in self.missiles_ennemis:
            if 0 <= tir.x <= 128 and 0 <= tir.y <= 128:
                if tir.x>0:
                    tir.move(4)
                else:
                    self.missiles_ennemis.remove(tir)
            else:
                self.missiles_ennemis.remove(tir)

        ##Déplacements des ennemis
        for ennemi in self.ennemis:
            ennemi.move(2)

        """Collisions"""

        ##Collisions joueur - Tirs ennemis
        for tir in self.missiles_ennemis:
            if 3<=tir.x<=6 and self.player.y-4<=tir.y<=self.player.y+16:
                self.missiles_ennemis.remove(tir)
                self.player.pv-=1

        ##Collisions Tirs_ennemis - Tirs_Joueurs
        for i in self.missiles_ennemis:
            for j in self.missiles_joueur:
                if i.x==j.x-6 and i.y<=j.y<=i.y+3:
                    self.missiles_ennemis.remove(i)
                    self.missiles_joueur.remove(j)
        ##Collisions Tirs_Joueurs - Ennemis
        for i in self.missiles_joueur:
            for j in self.ennemis:
                if i.x+6==j.x and j.y<=i.y<=j.y+16:
                    i.x,i.y=-100,-100
                    j.x,j.y=-100,-100

        ##Collisions Tirs_Ennemis - Protections
        for i in self.missiles_ennemis:
            for j in self.protections:
                if i.x==j.x+4 and j.y<=i.y<=j.y+24:
                    self.missiles_ennemis.remove(i)
                    j.pv-=1
                    if len(self.coeurs)>0:
                        self.coeurs.pop()

        ##Supression des protections
        for prot in self.protections:
            if prot.pv<=0:
                self.protections.remove(prot)

        ##Tirs ennemis
        rand_tir=pyxel.rndi(0,100)
        for ennemi in self.ennemis:
            if 0<=rand_tir<=2:
                self.missiles_ennemis.append(ennemi.tir())
            rand_tir = pyxel.rndi(0, 100)


#####################################################################################
# ---------------------------------UPDATE-FIN---------------------------------------#
#####################################################################################

    def nouvelle_vague(self):
        """
        crée une nouvelle vague de 6 ennemis
        """
        return [Ennemi(48,5,'Haut'),Ennemi(48,25,'Haut'),Ennemi(48,45,'Haut'),Ennemi(80,65,'Bas'),Ennemi(80,85,'Bas'),Ennemi(80,105,'Bas')]

    def draw(self):
        """
        Affichage
        """
        pyxel.cls(0)  ## réinitialisation de l'image

        if self.player.pv>=0: ##Affichage standard
            if self.victoire:  ##Message de victoire
                self.ennemis = []
                self.missiles_ennemis = []
                self.missiles_joueur = []
                self.protections = []
                self.player.x, y = 1000, 1000
                pyxel.text(56, 56, "Victory", 7)
                pyxel.blt(64, 64, 1, 24, 16, 8, 8, 0)
                pyxel.blt(64, 64 + 8, 1, 24, 24, 8, 8, 0)

            pyxel.rect(16,0,1,128,13) ##Ligne de limite des ennemis
            pyxel.rect(96, 0, 1, 128, 13)  ##Ligne de limite de l'HUD
            pyxel.text(104,8,"Vie",7)
            for c in self.coeurs: ##Affichage des coeurs
                c.draw()
            pyxel.text(100,56, "Vague "+str(self.vague), 7) ##Affichage de la vague
            self.player.draw()  ##Affichage du joueur
            for ennemi in self.ennemis:  ##Affichage des ennemis
                ennemi.draw()
            for tir in self.missiles_joueur:  ##Affichage des tirs alliés
                tir.draw()
            for tir in self.missiles_ennemis:  ##Affichage des tirs ennemis
                tir.draw()
            for prot in self.protections:  ##Affichage des protections
                prot.draw()

        else: ##Message de défaite
            self.ennemis=[]
            self.missiles_ennemis=[]
            self.missiles_joueur=[]
            self.protections=[]
            pyxel.blt(64, 64, 0, 128, 32, 8, 8, 0)
            pyxel.blt(64 + 8, 64, 0, 128 + 8, 32, 8, 8, 0)
            pyxel.blt(64, 64 + 8, 0, 128, 32 + 8, 8, 8, 0)
            pyxel.blt(64 + 8, 64 + 8, 0, 128 + 8, 32 + 8, 8, 8, 0)
            self.player.x,y=1000,1000
            pyxel.text(56,56,"GAME OVER",8)







class Joueur:
    def __init__(self,x,y):
        """
        :param x: coordonnées x initiales
        :param y: coordonnées y initiales
        """
        self.pv=12 #Points de vie du joueur
        self.x=x
        self.y=y
        self.arc=False #Booléen de changement de sprite

    def move(self,dy):
        """
        :param dx: valeur du déplacement (négatif si en haut)
        """
        if 0<=self.y+dy<=max_y-16:
            self.y+=dy

    def tir(self):
        """
        création d'un missile du joueur
        """
        self.arc=True
        return Missile(self.x+2 ,self.y+8,'Joueur')

    def draw(self):
        """
        Affichage du joueur
        """
        if self.arc==False:
            pyxel.blt(self.x,self.y,0,128,0,8,8)
            pyxel.blt(self.x, self.y+8, 0, 128, 8, 8, 8)
        else:
            pyxel.blt(self.x, self.y, 0, 136, 0, 8, 8)
            pyxel.blt(self.x, self.y + 8, 0, 136, 8, 8, 8)
class Missile:
    def __init__(self,x,y,camp):
        """
        :param x: coordonnées x initiales
        :param y: coordonnées y initiales
        :param degats: dégats du missile
        :param camp: camp de l'émetteur du missile (modifie le comportement)
        """
        self.x=x
        self.y=y
        self.camp=camp

    def move(self,dx):
        """
        Déplacements des missiles
        :param dy: valeur de déplacement du missile (négatif si à gauche)
        """
        if self.camp=='Joueur':
            self.x+=dx
        if self.camp=='Ennemi':
            self.x-=dx

    def draw(self):
        """
        Affichage des missiles
        """
        if self.camp=='Joueur':
            pyxel.blt(self.x,self.y,0,136,48,8,8,0)
        if self.camp=='Ennemi':
            pyxel.blt(self.x,self.y,0,136,56,8,8,0)



class Ennemi:
    def __init__(self,x,y, dir):
        """
        :param x: coordonnées x initiales
        :param y: coordonnées y initiales
        """
        self.x=x
        self.y=y
        self.dir=dir

    def move(self,dy):
        """Mouvements de l'ennemi"""
        if self.dir=='Haut':
            if self.y>0:
                self.y-=dy
            else:
                self.dir='Bas'
        if self.dir=='Bas':
            if self.y<128-16:
                self.y+=dy
            else:
                self.dir='Haut'

    def tir(self):
        """
        Création de tirs ennemis
        """
        return Missile(self.x-1,self.y+8,'Ennemi')


    def draw(self):
        """
        Affichage de l'ennemi
        """
        #pyxel.rect(self.x,self.y,16,16,14)
        pyxel.blt(self.x,self.y,0,128,32,8,8,0)
        pyxel.blt(self.x+8, self.y, 0, 128+8, 32, 8, 8,0)
        pyxel.blt(self.x, self.y+8, 0, 128 , 32+8, 8, 8,0)
        pyxel.blt(self.x+8, self.y + 8, 0, 128+8, 32 + 8, 8, 8,0)

    def tir(self):
        """Création d'un missile ennemi"""
        return Missile(self.x,self.y,'Ennemi')

class Protection:
    """
    Sert de couverture au joueur
    :param x: coordonnées x initiales
    :param y: coordonnées y initiales
    """
    def __init__(self,x,y):
        """
        :param x: coordonnées x
        :param y: coordonnées y
        """
        self.x=x
        self.y=y
        self.pv=15

    def draw(self):
        """
        Affichage dynamique de la protection
        """
        if self.pv >10:
            pyxel.blt(self.x, self.y,0, 128,72,4,24,0)
            pyxel.blt(self.x, self.y, 0, 128,88, 4,24, 0)
        elif self.pv>5:
            pyxel.blt(self.x, self.y, 0, 136, 72, 4, 24, 0)
            pyxel.blt(self.x, self.y, 0, 136, 88, 4, 24, 0)
        elif self.pv>0:
            pyxel.blt(self.x, self.y, 0, 144, 72, 4, 24, 0)
            pyxel.blt(self.x, self.y, 0, 144, 88, 4, 24, 0)

class Coeur:
    def __init__(self,x,y):
        """
        Permet de définir l'affichage des coeurs
        :param x: coordonnées x initiales
        :param y: coordonnées y initiales
        :
        """
        self.statut=True
        self.x=x
        self.y=y

    def draw(self):
        if self.statut:
            pyxel.blt(self.x, self.y,0,128,104,8,8,0)
        else:
            pyxel.blt(self.x, self.y,0,136,104,8,8,0)

Space()