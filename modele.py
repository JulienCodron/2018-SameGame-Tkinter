#Autor: Codron Julien
#Date: 26/03/18,8/04/18,16/04/18
#file: modeles.py

from random import randint


class Case():
    '''Classe qui modélise une bille du jeu Same.'''
    def __init__(self,couleur,compo=-1):
        ''' Methode, qui construit de la classe Case, elle prend en parametre la couleur est
            définie par un entier positif ou nul, si couleur=-1 la case est vide.
            Argument: -couleur, int
            Return: -None
        '''
        self.__couleur=couleur
        self.__compo=compo


    def couleur(self):
        '''Methode qui retourne la couleur de la bille
           Argument: -self, Case
           Return: -couleur, int
        '''
        return self.__couleur


    def change_couleur(self,couleur):
        '''Methode qui prend en paramètre une valeur entière et change la
           couleur de la bille.
           Argument: -self, Case(modif)
                     -couleur, int
           Return: None
        '''
        self.__couleur=couleur
        self.__compo=-1


    def supprime(self):
        '''Methode qui enlève la bille de la case.
           Argument: -self, Case(modif)
           Return: None
        '''
        self.__couleur=-1
        self.__compo=0


    def est_vide(self):
        '''Methode qui indique si la case est vide ou non.
           Argument: -self, Case
           Return: Bool
        '''
        return (self.__couleur==-1)


    def composante(self):
        '''Methode qui retourn la composante de la case
           Argument: -self, Case
           Return: -compo, int
        '''
        return self.__compo


    def pose_composante(self,num_compo):
        '''Methode qui prend en param`etre un entier et l’affecte comme numero de composante pour le case
           Arguement: -self, Case(modif)
                      -num_compo, int
           Return: None
        '''
        self.__compo=num_compo


    def supprime_compo(self):
        '''Methode qui supprime la composante d'une case (donc qui la fixe à -1)
           ou qui la met a 0 si la case est vide
           Argumlent: -self, Case(modif)
           Return: None
        '''
        if self.__couleur==-1:
            self.__compo=0
        else:
            self.__compo=-1


    def parcourue(self):
        '''Methode parcourue qui teste si la case a ete affectee a un numero de composante
           Argument: -self, Case(modif)
           Return: Bool
        '''
        return self.__compo!=-1

        
        
class Modele_same():
    '''Classe qui modélise le jeu Same.'''
    def __init__(self,nblig=10,nbcol=15,nbcouleurs=4):
        '''Methode qui initialise construit la classe Modele_same,
           elle prend en paramètre le nombre de ligne li, le nombre de
           colonnes col et le nombre de couleur utilise couleur.
           Argument: -self, Model_le_same
                     -li, int
                     -col, int
                     -couleur, int
           Return: None
        '''
        self.__nblig=nblig
        self.__nbcol=nbcol
        self.__nbcouleurs=nbcouleurs
        self.__mat=[]
        for i in range(nblig):
            ligne=[]
            for j in range(nbcol):
                case=Case(randint(0,nbcouleurs-1))
                ligne.append(case)
            self.__mat.append(ligne)
    
        self.__score=0
        self.__nb_elts_compo=[]
        self.calcule_composantes()


    def nblig(self):
        '''Methode qui retourne le nombre de ligne.
           Argument: -self, Model_le_same
           Return: int
        '''
        return (self.__nblig)


    def nbcol(self):
        '''Methode qui retourne le nombre de colonnes.
           Argument: -self, Model_le_same
           Return: int
        '''
        return (self.__nbcol)


    def nbcouleurs(self):
        '''Methode qui retourne le nombre de couleurs.
           Argument: -self, Model_le_same
           Return: int
        '''
        return (self.__nbcouleurs)


    def score(self):
        '''Methode qui retourne le score.
           Argument: -self, Model_le_same
           Return: int
        '''
        return (self.__score)


    def coords_valides(self,i,j):
        '''Metode qui indique si la case de coord (i,j)
           s’agit de coordonnees valides pour le jeu
           Argument: -self, Model_le_same
                     -i, int
                     -j, int
           Return: bool
        '''
        return(i<=self.__nblig and j<=self.__nbcol and i>=0 and j>=0)


    def couleur(self,i,j):
        '''Methode qui retourne un entier représentant la couleur de la
           case en coord i,j.
           Argument: -self, Model_le_same
                     -i, int
                     -j, int
           Return: int
        '''
        assert self.coords_valides(i,j),'coordonnees non valides'
        return(self.__mat[i][j].couleur())


    def supprime_bille(self,i,j):
        '''Methode qui supprime une bille en coordonnees i,j en
           remplacent sa couleur par -1
           Argument: -self, Model_le_same(modif)
                     -i, int
                     -j, int
           Return: None
        '''
        self.__mat[i][j].supprime()


    def nouvelle_partie(self):
        '''Methode qui reinitialise le jeu en redonnant une couleur
           disponnible a chaque case.
           Argument: -self, Model_le_same(modif)
           Return: None
        '''
        for i in range(self.__nblig):
            for j in range(self.__nbcol):
                self.__mat[i][j].change_couleur(randint(0,self.__nbcouleurs-1))
        self.__score = 0
        self.recalc_composantes()



    def composante(self,i,j):
        '''Methode qui prend deux parametres i et j et qui renvoie la composante de la bille en (i,j).
           Argument: -self, Model_le_same
                     -i, int
                     -j, int
           Return: composante, int
        '''
        assert self.coords_valides(i,j),'coordonnees non valides'
        return (self.__mat[i][j].composante())


    def calcule_composantes(self):
        '''Methode qui calcule les composante de toute les case de la matrice
           Argument: -self, Model_le_Same(modif)
           Return: None
        '''
        self.__nb_elts_compo.append(0)
        num_compo=1
        for i in range(self.__nblig):
            for j in range(self.__nbcol):
                if not(self.__mat[i][j].parcourue()):
                    couleur=self.couleur(i,j)
                    nb=self.calcule_composante_numero(i,j,num_compo,couleur)
                    self.__nb_elts_compo.append(nb)
                    num_compo+=1

    def calcule_composante_numero(self,i,j,num_compo,couleur):
        '''Methode qui calcule la composante numero num_compo ap artir d'une case de la matrice de
           coordonnée i,j et de sa couleur, couleur. Et qui retourne le nombre de bille de cette composante.
           Argument: -self, Model_le_Same(modif)
                     -i, int
                     -j, int
                     -num_compo, int
                     -couleur, int
           Return: -int
        '''
        if self.couleur(i,j) != couleur or self.__mat[i][j].parcourue():
            res=0
        else:
            self.__mat[i][j].pose_composante(num_compo)
            res=1 
            if i > 0:
                res +=self.calcule_composante_numero(i-1,j,num_compo,couleur)
            if i < self.__nblig-1:
                res +=self.calcule_composante_numero(i+1,j,num_compo,couleur)
            if j > 0:
                res +=self.calcule_composante_numero(i,j-1,num_compo,couleur)
            if j < self.__nbcol-1:
                res +=self.calcule_composante_numero(i,j+1,num_compo,couleur)    
        return (res)


    def recalc_composantes(self):
        ''' Methode qui supprime la composante attribuee a chaque case
            Arguments: -self, ModelSame(modif)
	    Retour: -None
	'''
        self.__nb_elts_compo=[]
        for i in range(self.__nblig):
            for j in range(self.__nbcol):
                self.__mat[i][j].supprime_compo()
        self.calcule_composantes()

            
    def supprime_composante(self,num_compo):
        '''Methode qui supprime une composante donnee
           Attribut: -self, Model_le_Same(modif)
           Return: Bool
        '''
        if self.__nb_elts_compo[num_compo] >=2 :
            for j in range(self.__nbcol):
                self.supprime_composante_colonne(j,num_compo) 
            self.supprime_colonnes_vides()
            self.__score += (self.__nb_elts_compo[num_compo] -2 )**2
            self.recalc_composantes()
            return True
        return False


    def est_vide(self,i,j):
        '''Methode qui retourne si une case est vide
           Argument: -self, Modele_same
                     -i, int
                     -j, int
           Return: Bool
        '''
        return (self.__mat[i][j].est_vide())

    def supprime_composante_colonne(self,j,num_compo):
        '''Methode qui supprime les billes d'une compo dans une colonne, et
           qui fait tomber les billes
           Argument: -self,Modele_same(modif)
                     -j, int
                     -num_compo, int
           Return: None
        '''
        
        compt=self.__nblig
        verif=False
        for i in range(self.__nblig-1,-1,-1):
            if  self.composante(i,j)==num_compo :
                    self.supprime_bille(i,j)
                    verif=True
            elif verif:
                compt-=1
                self.__mat[compt][j].change_couleur(self.__mat[i][j].couleur())
                self.supprime_bille(i,j)
            else:
                compt=i

    def supprime_colonnes_vides(self):
        '''Methode qui decale les collone vide a droite.
           Arugment: -self, Modele_same(modif)
           Return: None
        '''

        for u in range(self.__nbcol):
            compt=0
            a=0
            verif=False
            for j in range (self.__nbcol):
                a=0
                for i in range(self.__nblig):
                   if (self.est_vide(i,j)):
                        a+=1
                compt+=1    
                if a==self.__nblig:
                    for y in range (compt,self.__nbcol):
                        for x in range (self.__nblig):
                            self.__mat[x][y-1].change_couleur(self.__mat[x][y].couleur())
                            self.__mat[x][y].change_couleur(-1) 
                    


    def plus_grande_compo(self):
        '''Méthode qui retourne l'orde de la plus grande composante
           Argument: self, Modele_same
           Return: int.
        '''
        pgc=0
        for i in range(len(self.__nb_elts_compo)):
            if self.__nb_elts_compo[pgc]<self.__nb_elts_compo[i]:
                pgc=i
        return (pgc)

    def nb_elts_compo(self):
        '''Methode qui retourne la liste des élement de compo
           Argument: -self, Model_same
           Return: liste de int
        '''
        return (self.__nb_elts_compo)

  
            
