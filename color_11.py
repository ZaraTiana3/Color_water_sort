import heapq
 #Using 6 tubes but with negative heapq 
TUBE = 11
NIVEAU = 4
from itertools import takewhile
is_correct= [0]*TUBE #-1 Mixed, #0 Empty, #1 Correct
t = [[]*NIVEAU]*TUBE
#tube=[['b','b','y','y'],['r','g','y','y'],['r','r','b','y'],['r','y','g','g'], ['']*NIVEAU,['']*NIVEAU]

t = [['o','y','p','w'],['k','k','k','r'],['y','p','y','b'],['w','o','b','s'],['s','p','b','w'],['k','g','b','s'],
      ['y','p','r','o'],['g','w','g','r'],['g','o','s','r'],[' ']*NIVEAU,[' ']*NIVEAU]

class Tube:
    def __init__(self, tube):
        self.t = tube
        self.count=0 #variable pour suivre trace les tubes
        self.state=[-2,-2,-2,-2,-2,-2,-2,-2,-2, 0,0] #-2Mixed, #-1 Spaced, #0 Empty, #1 Correct
        #self.space  = [[4,4,''], [5,4,'']]#(, position, quantite, couleur)

    def print_tube(self):
        #Pour afficher l'état des tubes
        print("Les tubes sont:")
        for i in range(NIVEAU):
            print(f'|{self.t[0][i]}| |{self.t[1][i]}| |{self.t[2][i]}| |{self.t[3][i]}| |{self.t[4][i]}| |{self.t[5][i]}| |{self.t[6][i]}| |{self.t[7][i]}| |{self.t[8][i]}| |{self.t[9][i]}| |{self.t[10][i]}|')
            #print(f'|{self.t[0][i]}| |{self.t[1][i]}| |{self.t[2][i]}| |{self.t[3][i]}| |{self.t[4][i]}| |{self.t[5][i]}|')
            #print(self.t[0])

def determine_filler(tube, all_positions:list, pos_filled:list, qtt_filled:int, clr_filled:list):
    #Cette section sert a determiner le tube  filler  pour un espace blanc
#all_positions contient les tubes a ne pas considérer car ce sont des tubes vides ou le candidat lui-meme ou tube correct
    qtt_filler=-1
    pos_filler=-1
    niveau_filler=-1
    all_positions=all_positions+[pos_filled] 
    clr=-1
    print('Les positions à eviter sont: ', all_positions)
    if clr_filled[0]==' ': #'Si la couleur est nulle(cad que la tube est entierement vide), on peut prendre ttes les clrs possible'
        clr_filled = ['r','g','y','b', 'o', 'p', 'k','s','w']
    print('Tube: ', tube)
    for i,t in enumerate(tube):#parcourir les tubes
        #print('Tube: ', i)
        if i in all_positions: #ignorer les tubes incluses dans all_position
            continue
        for j, couleur in enumerate(t): #parcourir les couleurs
            #print('Couleur et clr_filled: ',couleur, clr_filled)
            if couleur==' ': #Tant que la place est encore vide, procéder aux autres niveaux
                continue
            if couleur in clr_filled:        
                count= sum(1 for x in takewhile(lambda x: x == couleur, t[j:]))  
                if j+count==NIVEAU and qtt_filled==NIVEAU:
                    #print('Is here the problem')
                    break
    #if count>qtt_filler: ceci veut dire que si la nvelle vlr count est > à qtt_filler , qtt_filler est mis à jour
                if (count > qtt_filler) and (qtt_filled>=count):
    #Si qtt_filled(tube a remplir)>=count(celui qui remplit),cad le filler rentre bien dans filled, qtt_filler est mis a jour 
                    clr=couleur #clr désigne la couleur à retourner
                    qtt_filler=count  #qtt_filler désigne la quantité du filler
                    pos_filler=i    #position du filler
                    niveau_filler=j
                    #print("Quantite: ", qtt_filler,'et position: ', pos_filler, 'et couleur:', clr_filled)
            break #quand on a recupéré la couleur au debut d'un nieme tube, on passe immédiatement au prochain(n+1) tube
        else:
            continue
    return pos_filler, qtt_filler, niveau_filler, clr

tube = Tube(t)

def check_result(t):
    somme = sum(i for i in t.state)
    return somme==TUBE


def determine_candidates(t, space:list):
    res =[]
    qtt=0 #space contient les listes des tubes avec des espaces
    for i, t  in enumerate(t.t):
        if i not in space: 
            continue
        qtt = t[0:NIVEAU].count(' ')
        clr = clr_filled = ['r','g','y','b', 'o', 'p', 'k','s','w'] if qtt == 4 else [t[qtt]]
        res.append([-qtt, i, clr]) #i: position, qtt: quantite libre
    #print('Les candidats espaces sont: ', res)
    return res

def fill_modify(t, niveau_filler, clr_filled:str, pos_filler:int,pos_filled:int, qtt_filler:int, qtt_filled:int):
    #remplir la case vide à la pos_filled avec la couleur clr_filled a la position pos_filler
    #On commence a remplir a partir de first_to_fill jusqu'a last_to_fill
    first_to_fill = qtt_filled-qtt_filler 
    last_to_fill = qtt_filled #niveau last_to_fill non inclus
    print('First to fill: ',first_to_fill,  'and last to fill: ', last_to_fill)
    #Remplir les cases vides() du to_fill
    for i in range(first_to_fill, last_to_fill):
        t.t[pos_filled][i]=clr_filled

    #Enlever les couleurs du filler, qtt_filler
    for i in range(niveau_filler, niveau_filler+qtt_filler): #niveau qtt_filler non inclus
        t.t[pos_filler][i]=' '

    print('Evaluer pos_filler')
    #Evaluate the state of the tube 
    if t.t[pos_filler][0]==' ':#si le début est vide 
        if  t.t[pos_filler][NIVEAU-1]!=' ' :#vide au debut mais rempli au fond 
            t.state[pos_filler] = -1
        elif t.t[pos_filler][NIVEAU-1]==' ': #totalement vide
            t.state[pos_filler] = 0
    elif t.t[pos_filler][0]!=' ':#si le tube est rempli
        if sum(1 for j in range(NIVEAU) if t.t[pos_filler][j]==clr_filled)==NIVEAU: #toutes les couleurs sont les meme 
            t.state[pos_filler]=1
        else:#les couleurs sont différentes 
            t.state[pos_filler]=-2
    #print()
    print('Evaluer pos_filled')
     #Evaluate the state of the tube 
    if t.t[pos_filled][0]==' ':#si le début est vide 
        if  t.t[pos_filled][NIVEAU-1]!=' ' :#vide au debut mais rempli au fond 
            t.state[pos_filled] = -1
        elif t.t[pos_filled][NIVEAU-1]==' ': #totalement vide
            t.state[pos_filled] = 0
    elif t.t[pos_filled][0]!=' ':#si le tube est rempli
        if sum(1 for j in range(NIVEAU) if t.t[pos_filled][j]==clr_filled)==NIVEAU: #toutes les couleurs sont les meme 
            t.state[pos_filled]=1
        else:#les couleurs sont différentes 
            t.state[pos_filled]=-2

    print(t.state)

    
def cancel_move(t, niveau_filler,clr_filled:str, pos_filler:int,pos_filled:int, qtt_filler:int, qtt_filled:int):
    #remplir la case vide à la pos_filled avec la couleur clr_filled a la position pos_filler
    #On commence a remplir a partir de first_to_fill jusqu'a last_to_fill
    first_to_fill = qtt_filled-qtt_filler 
    last_to_fill = qtt_filled #niveau last_to_fill non inclus

    #Remplir les cases vides() du to_fill
    for i in range(first_to_fill, last_to_fill):
        t.t[pos_filled][i]=' '

    #Enlever les couleurs du filler, qtt_filler
    for i in range(niveau_filler, niveau_filler+qtt_filler): #niveau qtt_filler non inclus
        t.t[pos_filler][i]=clr_filled

    print('Evaluer pos_filler')
    #Evaluate the state of the tube 
    if t.t[pos_filler][0]==' ':#si le début est vide 
        if  t.t[pos_filler][NIVEAU-1]!=' ' :#vide au debut mais rempli au fond 
            t.state[pos_filler] = -1
        elif t.t[pos_filler][NIVEAU-1]==' ': #totalement vide
            t.state[pos_filler] = 0
    elif t.t[pos_filler][0]!=' ':#si le tube est rempli
        if sum(1 for j in range(NIVEAU) if t.t[pos_filler][j]==clr_filled)==NIVEAU: #toutes les couleurs sont les meme 
            t.state[pos_filler]=1
        else:#les couleurs sont différentes 
            t.state[pos_filler]=-2
    print(t.state)
    print('\n Evaluer pos_filled')
     #Evaluate the state of the tube 
    if t.t[pos_filled][0]==' ':#si le début est vide 
        if  t.t[pos_filled][NIVEAU-1]!=' ' :#vide au debut mais rempli au fond 
            t.state[pos_filled] = -1
        elif t.t[pos_filled][NIVEAU-1]==' ': #totalement vide
            t.state[pos_filled] = 0
    elif t.t[pos_filled][0]!=' ':#si le tube est rempli
        if sum(1 for j in range(NIVEAU) if t.t[pos_filled][j]==clr_filled)==NIVEAU: #toutes les couleurs sont les meme 
            t.state[pos_filled]=1
        else:#les couleurs sont différentes 
            t.state[pos_filled]=-2
    print(t.state)


def solve(t, k):
    print('\n')
    
    if k>35:
        raise Exception("Stop") 
    k+=1
    print('k= ',k)
    """if check_result(t):
        print('++++++++++++++++++++++++++++++++++++++++FIN++++++++++++++++++++++++++++++++++++++++++++++++++++')
        t.print_tube()
        print('++++++++++++++++++++++++++++++++++++++++FIN++++++++++++++++++++++++++++++++++++++++++++++++++++')
        return True  
    """
    print("Sum(i for i in t.state): ", sum(i for i in t.state))
    if sum(i for i in t.state)==TUBE-2:
        t.print_tube()
        return True
    space =  [i for i, val in enumerate(t.state) if val == 0 or val==-1]#toutes les tubes avec espace blanc
    print('Space: ', space)
    pos_to_avoid= [i for i, val in enumerate(t.state) if val == 0 or val==1] #contenant les tube totalement vides
    candidates = determine_candidates(t, space)
    heapq.heapify(candidates)
    print('Les candidats espaces sont: ', candidates)
    #for pos_filled, qtt_filled,clr_filled  in candidates: 
    #    print(pos_filled, qtt_filled,clr_filled )


    while candidates:
        qtt_filled,pos_filled, clr_filled = heapq.heappop(candidates)
        qtt_filled = -qtt_filled
        print('On va prendre le candidat',qtt_filled, pos_filled,  clr_filled)
        #all_positions est la position_exclue
        pos_filler, qtt_filler, niveau_filler, clr_filled = determine_filler(t.t, pos_to_avoid, pos_filled, qtt_filled,clr_filled)
        print("Les solutions correspondantes sont:")
        print("pos_filler, qtt_filler, niveau_filler, clr_filled: ", pos_filler, qtt_filler, niveau_filler, clr_filled )
        if pos_filler==-1:
            print("***********************************************************************")
            print('Position negative')
            print("***********************************************************************")
            continue
        fill_modify(t, niveau_filler, clr_filled, pos_filler,pos_filled, qtt_filler, qtt_filled)
        #Afficher l'etat actuel du tube
        t.print_tube()
        print('On va passer au prochain round')
        if solve(t, k):
            return True
        print('Cancel move')
        cancel_move(t, niveau_filler, clr_filled, pos_filler,pos_filled, qtt_filler, qtt_filled)
    return False



t = [['o','y','p','w'],['k','k','k','r'],['y','p','y','b'],['w','o','b','s'],['s','p','b','w'],['k','g','b','s'],
      ['y','p','r','o'],['g','w','g','r'],['g','o','s','r'],[' ']*NIVEAU,[' ']*NIVEAU]


t = Tube(t)
t.print_tube()
k=0
print('We begin')

"""for i in range(NIVEAU):
    print(f'|{t[0][i]}| |{t[1][i]}| |{t[2][i]}| |{t[3][i]}| |{t[4][i]}| |{t[5][i]}| |{t[6][i]}| |{t[7][i]}|')"""

solve(t,k)



