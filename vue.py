#Autor: Codron Julien
#Date: 26/03/18,8/04/18,16/04/18
#file: vue.py

from tkinter import *
from modele import *

class Vue_same():
    '''Classe qui  construit la fenêtre principale de l’application et
       tous les co
       mposants de la vue.
    '''
    def __init__(self,same):
        '''Methode qui construit la classe Vue_same, permetant d'afficher a
           partir d'un Modele_same l'interface graphique de celui-ci.
           Argument, -self, Vue_same
                     -same, Model_le_same
           Return: None
        '''
        self.__same=same
        self.__nextscore=0

        self.__fen=Tk()
        self.__fen.title("Same Game")

        frame_bille=Frame(self.__fen)
        frame_menu=Frame(self.__fen)

        self.__images=[]
        for nbcoul in range(1,same.nbcouleurs()+1):
            img = PhotoImage(file="img/medium_sphere"+str(nbcoul)+".png")
            self.__images.append(img)
        img = PhotoImage(file="img/medium_spherevide.gif")
        self.__images.append(img)

        self.__images_noires=[]
        for nbimg in range(1,same.nbcouleurs()+1):
            img = PhotoImage(file="img/medium_sphere"+str(nbimg)+"black.png")
            self.__images_noires.append(img)
            
        self.__les_btns=[]
        for i in range(same.nblig()):
            ligne = []
            for j in range (same.nbcol()):
                mon_img = None
                btn =Button(frame_bille,image=self.__images[same.couleur(i,j)],command=self.creer_controleur_btn(i,j))
                btn.bind("<Motion>",self.creer_motion_btn(i,j),"+")
                btn.bind("<Leave>",self.creer_leave_btn(i,j),"+")
                ligne.append(btn)
                btn.grid(row=i,column=j)
            self.__les_btns.append(ligne)        

        frame_bille.pack(side='left')

        ligne1=Label(frame_menu,text='----------------------------------')
        ligne1.pack()
        start=Button(frame_menu,text='      Indice      ',command=self.indice)
        start.pack() 
        ligne2=Label(frame_menu,text='----------------------------------')
        ligne2.pack()
        self.__score=Label(frame_menu,text='Score: '+ str(self.__same.score()))
        self.__score.pack()
        self.__scorenext=Label(frame_menu,text='Point du prochain coup: +'+ str(self.__nextscore))
        self.__scorenext.pack()
        ligne3=Label(frame_menu,text='----------------------------------')
        ligne3.pack()
        start=Button(frame_menu,text='      Reset      ',command=self.nouvelle_partie)
        start.pack()
        ligne5=Label(frame_menu,text='----------------------------------')
        ligne5.pack()
        quitte=Button(frame_menu,text='     Quitter     ',command=self.__fen.destroy)
        quitte.pack()
        frame_menu.pack(side='right')
        ligne4=Label(frame_menu,text='----------------------------------')
        ligne4.pack()

        self.__fen.mainloop()
        

    def redessine(self):
        '''Methode qui parcourt tous les boutons de self.__les_btns et change l’image
           qu’ils afﬁchent en fonction de same;
           Attribut: -self, Vue_same 
           Return: None
        '''
        for i in range(len(self.__les_btns)):
            for j in range (len(self.__les_btns[1])):
                if self.__images[self.__same.couleur(i,j)]==-1:
                    self.__les_btns[i][j]['image']=self.__images[self.__same.nbcouleurs()]
                else:
                    self.__les_btns[i][j]['image']=self.__images[self.__same.couleur(i,j)]
        self.__score.config(text = "Score : " + str(self.__same.score()))
                
                
        

    def nouvelle_partie(self):
        '''Methode qui est associée au  bouton Reset, elle demande au modèle de
           reinitialiser une nouvelle partie et met a jour l'affichage
           Argument: -self, Vue_same(Modele_same modif)
           Return: None
        '''
        self.__same.nouvelle_partie()
        self.redessine()

    def creer_controleur_btn(self,i,j):
        '''Methode qui creer un fonction unique pour chaque bouton et qui le control lors d'un clic.
           Attribut: -self, Vue_same
                     -i, int
                     -j, int
           Return: Fonction
        '''
        def controleur_btn():
            '''Fonction unique qui est le controleur du bouton , elle permet de suprimer la
               la bille du bouton puis la redessine.
               Attribut: None
               Return: None
            '''
            if self.__same.supprime_composante(self.__same.composante(i,j)):
                self.redessine()
        return controleur_btn
        

    def creer_motion_btn(self,i,j):
        '''Fonction qui creer une fonction unique pour chaque bouton qui control l'action lors ce qu'on survole celui-ci.
           Elle permet de mettre en valeur la composante de ce button.
           Attribut: -Self, Vue_Same
                     -i, int
                     -j, int
           Return: Fonction
        '''
        def motion_btn(event):
            '''Fonction qui change l'image des buttons qui sont de la même composante qui celui que l'on survole.
               Attribut: -event
               Return: None
            '''
            for y in range(self.__same.nblig()):
                for z in range(self.__same.nbcol()):
                    if (self.__same.composante(y,z)==self.__same.composante(i,j)) and self.__same.couleur(y,z)!=-1:
                        self.__les_btns[y][z]['image']=self.__images_noires[self.__same.couleur(y,z)]
                        self.__nextscore= (self.__same.nb_elts_compo()[self.__same.composante(i,j)] -2 )**2
                        self.__scorenext.config(text='Point du prochain coup: +'+ str(self.__nextscore))
        return motion_btn
    
    def creer_leave_btn(self,i,j):
        '''Fonction qui creer une fonction unique pour chaque bouton qui control l'action lors ce qu'on ne survole plus celui-ci.
           Elle permet remetre les images normal de la composante de ce button.
           Attribut: -Self, Vue_Same
                     -i, int
                     -j, int
           Return: Fonction
        '''
        def leave_btn(event):
            '''Fonction  qui remet l'autre image lorcequ'on ne la survole plus.
               Attribut: -event, event
               Return: None
            '''
            for y in range(self.__same.nblig()):
                for z in range(self.__same.nbcol()):
                    if self.__same.composante(y,z)==self.__same.composante(i,j):
                        self.__les_btns[y][z]['image']=self.__images[self.__same.couleur(y,z)]
                        self.__nextscore=0
                        self.__scorenext.config(text='Point du prochain coup: +'+ str(self.__nextscore))
        return leave_btn

    def indice(self):
        '''Méthode associé au bouton indince, qui permet de mettre en valuer la plus grande composante.
           Argument: self, Vue_Same
           Return: None
        '''
        for i in range(self.__same.nblig()):
                for j in range(self.__same.nbcol()):
                    if self.__same.plus_grande_compo()==self.__same.composante(i,j):
                         self.__les_btns[i][j]['image']=self.__images_noires[self.__same.couleur(i,j)]
        

        
if __name__=="__main__":
    same=Modele_same()
    vue= Vue_same(same)




