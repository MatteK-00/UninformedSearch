# -*- coding: cp1252 -*-
from copy import copy,deepcopy
from UninformedSearchs import solve_dfs,solve_bfs,solve_ids,solve_ucs


#Oggetto che rappresenta in modo comppleto lo stato attuale del tavolo di gioco, al suo interno sono definiti:
#listaBlocchi: una lista di liste con un formato di input "standard" che rappresentano la posizione dei blocchi e le loro caratteristiche:
#   in listaBlocchi le singole liste che rappresentano il blocco devono necessariamente essere inserite utilizzando le posizioni nel modo seguente:
#   posizioni nella lista "blocco": 0 Nome, 1 Base, 2 Sopra, 3 SpazioSopraOccupato, 4 bloccoSotto
#dx, sx: rappresentano dei valori interni o None, se il valore è None, significa che il braccio è scarico e quindi potranno essere eseguiti i metodi "AfferraDx/Sx"
#   se il valore è un intero, saranno abilitati i metodi "putOnDx/Sx e putDownDx/Sx" e il valore intero rappresenta l'indice di listaBlocchi che rappresenta il blocco nella mano
#goal: campo opzionale in cui inserire il goal (opzionale sono ai fini di test!)
#mossa: campo opzionale per la generazione dell'output
#parent: campo opzionale gestito dai metodi per la stampa della soluzione finale che contiene un puntatore al padre di ogni nodo
#depth e cost utilizzati dal sistema per generare le statistiche su costi (ucs) e profondita raggiunta dai vari nodi (tutte le ricerche).

#Infine all'interno della classe sono presenti:
#metodi privati: "AfferraDx/Sx","putOnDx/Sx e putDownDx/Sx" che rappresentano le possibili mosse da cui generare gli stati successori
#metodi pubblici:
#   successors: che restituisce la lista di tutti i possibili stati successori dello stato corrente
#   get_data: che restituisce una stringa contenente una versione compatta dello stato
#   print_sol: che stampa la soluzione a partire dallo stato goal trovato
#   goal_state: che confronta lo stato corrente con lo stato goal e restituisce True o False



class Tavolo:

    c = (1,1,1)
    #nodeCount = 0
    
    def __init__(self,listaBlocchi,dx,sx,goal=None,mossa="stato iniziale",parent=None,depth=0,cost=0):
        self.listaBlocchi = listaBlocchi
        self.dx = dx
        self.sx = sx
        self.goal = goal
        self.mossa = mossa
        self.parent = parent
        self.cost = cost
        self.depth = depth
        #Tavolo.nodeCount += 1

    def __putDownDx(self,c):
        if self.dx != None:
            temp=deepcopy(self.listaBlocchi)
            temp[self.dx][4] = 'Tavolo'
            mossa = "Metto con il braccio dx il blocco " +  temp[self.dx][0] + " sul tavolo"
            return [Tavolo(temp,None,self.sx,self.goal,mossa,self,self.depth+1,self.cost +c)]
        else:
            return []

    def __putDownSx(self,c):
        if self.sx != None:
            temp=deepcopy(self.listaBlocchi)
            temp[self.sx][4] = 'Tavolo'
            mossa = "Metto con il braccio sx il blocco " +  temp[self.sx][0] + " sul tavolo"
            return [Tavolo(temp,self.dx,None,self.goal,mossa,self,self.depth+1,self.cost +c)]
        else:
            return []

    def __putOnDx(self,c):
        temp = []
        if self.dx != None:
            for i in range(0,len(self.listaBlocchi)):
                if (i != self.dx)  and (i != self.sx) and ((self.listaBlocchi[i][2] - self.listaBlocchi[i][3]) >= self.listaBlocchi[self.dx][1]):
                        tempPila = deepcopy(self.listaBlocchi)
                        tempPila[i][3] = tempPila[i][3] + self.listaBlocchi[self.dx][1]
                        tempPila[self.dx][4] = tempPila[i][0]
                        mossa = "Metto con il braccio dx il blocco " +  tempPila[self.dx][0] + " sul blocco " + tempPila[i][0]
                        temp.append(Tavolo(tempPila,None,self.sx,self.goal,mossa,self,self.depth+1,self.cost+c))
        return temp

    def __putOnSx(self,c):
        temp = []
        if self.sx != None:
            for i in range(0,len(self.listaBlocchi)):
                if (i != self.sx)  and (i != self.dx) and ((self.listaBlocchi[i][2] - self.listaBlocchi[i][3]) >= self.listaBlocchi[self.sx][1]):
                        tempPila = deepcopy(self.listaBlocchi)
                        tempPila[i][3] = tempPila[i][3] + self.listaBlocchi[self.sx][1]
                        tempPila[self.sx][4] = tempPila[i][0]
                        mossa = "Metto con il braccio sx il blocco " +  tempPila[self.sx][0] + " sul blocco " + tempPila[i][0]
                        temp.append(Tavolo(tempPila,self.dx,None,self.goal,mossa,self,self.depth+1,self.cost+c))
        return temp  

    def __afferraDx(self,c):
        temp = []
        if self.dx == None:
            for j in range(0,len(self.listaBlocchi)):
                if self.listaBlocchi[j][3] == 0:
                    tempPila = deepcopy(self.listaBlocchi)
                    for i in tempPila:
                        if i[0] == tempPila[j][4]:
                            i[3] = i[3] - tempPila[j][1]
                    tempPila[j][4] = 'dx'
                    tempPila[j][3] = 0
                    mossa = "Prendo con il braccio dx il blocco " + tempPila[j][0]
                    temp.append(Tavolo(tempPila,j,self.sx,self.goal,mossa,self,self.depth+1,self.cost +c))
        return temp

    def __afferraSx(self,c):
        temp = []
        if self.sx == None:
            for j in range(0,len(self.listaBlocchi)):
                if self.listaBlocchi[j][3] == 0:
                    tempPila = deepcopy(self.listaBlocchi)
                    for i in tempPila:
                        if i[0] == tempPila[j][4]:
                            i[3] = i[3] - tempPila[j][1]
                    tempPila[j][4] = 'sx'
                    tempPila[j][3] = 0
                    mossa = "Prendo con il braccio sx il blocco " + tempPila[j][0]
                    temp.append(Tavolo(tempPila,self.dx,j,self.goal,mossa,self,self.depth+1,self.cost+c))
        return temp

    def successors(self,cost=c):
        temp = []
        temp.extend(self.__putDownDx(cost[0]))
        temp.extend(self.__putDownSx(cost[0]))
        temp.extend(self.__putOnDx(cost[1]))
        temp.extend(self.__putOnSx(cost[1]))
        temp.extend(self.__afferraDx(cost[2]))
        temp.extend(self.__afferraSx(cost[2]))
        return temp

    def goal_state(self):
        if self.listaBlocchi == self.goal:
            return True
        else:
            return False

    def get_data(self):
        temp = ""
        for i in self.listaBlocchi:
            temp += "[ " + i[0] + " - " + i[4] + " ]"
        return temp

    def print_sol(self):
        if self.parent is not None:
            self.parent.print_sol()
        temp = self.get_data() + "    " + self.mossa
        print temp
        print


            


#posizioni nella lista: 0 Nome, 1 Base, 2 Sopra, 3 SpazioSopraOccupato, 4 bloccoSotto
A = ['A',2,2,2,'Tavolo']
B = ['B',2,2,2,'A']
C = ['C',2,2,0,'B']
D = ['D',2,2,0,'Tavolo']
E = ['E',2,2,0,'dx']


############    Tavolo Facile Con Soluzione (medio con DFS)

goal1 = [['A',2,2,2,'Tavolo'],['B',2,2,2,'A'],['C',2,2,0,'B'],['D',2,2,0,'sx'],['E',2,2,0,'Tavolo']]

tavolo1 = Tavolo([A,B,C,D,E],4,None,goal1)

############     Tavolo Facilissimo Senza Soluzione 

goal2 = [['A',2,2,0,'B'],['B',2,1,2,'Tavolo']]

tavolo2 = Tavolo([['A',2,2,0,'Tavolo'],['B',2,1,0,'Tavolo']],None,None,goal2)

############     Tavolo Facilissimo Con Soluzione 

goal3 = [['A',2,4,0,'dx'],['B',2,2,0,'sx']]

tavolo3 = Tavolo([['A',2,4,0,'B'],['B',2,2,2,'Tavolo']],None,None,goal3)

############    Tavolo Difficile Senza Soluzione (medio con DFS, irrisolvibile con UCS per "RuntimeError: maximum recursion depth exceeded" all'interno di quicksort)

goal4 = [['A',2,4,2,'Tavolo'],['B',2,1,2,'A'],['C',2,2,0,'B'],['D',2,2,0,'sx'],['E',2,2,0,'Tavolo']]

tavolo4 = Tavolo([['A',2,4,2,'Tavolo'],['B',2,1,0,'A'],['C',2,2,0,'A'],
                  ['D',2,2,0,'Tavolo'],['E',2,2,0,'Tavolo']],None,None,goal1)

############    Tavolo Difficile Senza Soluzione (medio con DFS, irrisolvibile con UCS per "RuntimeError: maximum recursion depth exceeded" all'interno di quicksort)

goal5 = [['A',2,4,3,'Tavolo'],['B',1,1,0,'A'],['C',2,2,0,'A'],['D',2,2,0,'sx'],['E',2,2,0,'Tavolo']]

tavolo5 = Tavolo([['A',2,4,1,'Tavolo'],['B',1,1,0,'A'],['C',2,2,0,'Tavolo'],
                  ['D',2,2,0,'Tavolo'],['E',2,2,0,'Tavolo']],None,None,goal1)

############     Tavolo Facile Con Soluzione (Esempio con due blocchi sopra un blocco)

goal6 = [['A',4,4,4,'Tavolo'],['B',2,1,0,'A'],['C',2,1,0,'A']]

tavolo6 = Tavolo([['A',4,4,0,'Tavolo'],['B',2,1,0,'Tavolo'],['C',2,1,0,'Tavolo']],None,None,goal6)

############     Esempio facile fatto durante la presentazione

goal7 = [['A',2,2,2,'Tavolo'],['B',2,2,2,'A'],['C',2,2,0,'B']]

tavolo7 = Tavolo([['A',2,2,0,'B'],['B',2,2,2,'C'],['C',2,2,2,'Tavolo']],None,None,goal7)





solve_dfs(tavolo1)
print
solve_bfs(tavolo1)
print
solve_ids(tavolo1)
print
solve_ucs(tavolo1,(1,1,1))

print
#solve_ucs(tavolo2,(1,1,1))
print
#solve_bfs(tavolo2)
print
#solve_ids(tavolo2)
print
#solve_dfs(tavolo2)

#solve_ucs(tavolo3,(1,1,1))
print
#solve_bfs(tavolo3)
print
#solve_ids(tavolo3)
print
#solve_dfs(tavolo3)

print
#solve_dfs(tavolo4)
print
#solve_bfs(tavolo4)
print
#solve_ids(tavolo4)
print
#solve_ucs(tavolo4,(1,1,1))

print
#solve_dfs(tavolo6)
print
#solve_bfs(tavolo6)
print
#solve_ids(tavolo6)
print
#solve_ucs(tavolo6,(1,1,1))



            
