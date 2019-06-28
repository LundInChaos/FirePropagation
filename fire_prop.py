
import numpy as np
import random
from tkinter import Tk, Canvas, Button, RIGHT, LEFT

#Map dimensions
NbL = 30
NbC = 30
a = 15
density=0.49


cell = np.zeros((NbL,NbC),dtype=int)
etat = np.zeros((NbL,NbC),dtype=int)


state = {"OFF":0,"FIRE":1, "TREE":2, "ASH":3}

# Calculating next generation
def iterate():
    global flag
    global ash
    rules()
    draw()
    print(ash)
    if flag==1:
        fenetre.after(100, iterate)
    else:
        flag=0

#Initializing the map
def initialize_map():   
    etat[0:NbL,0:NbC] = state["OFF"]

    for x in range(NbL):
        for y in range(NbC):
            num=random.random()
            if num>density:
                etat[x,y] = state["TREE"]
            cell[x,y] = canvas.create_rectangle((x*a, y*a, (x+1)*a, \
                         (y+1)*a), outline="gray", fill="white")
# Defining rules of propagation
def rules():
    global etat
    global ash
    temp = np.zeros((NbL,NbC))
    for x in range(NbL):
        for y in range(NbC):
            nb_voisins = voisinageVonN(x,y)
            #calculating a second order neighborhood
            voisins2=0
            if x>0:
                if y<NbC:
                    voisins2+= voisinageVonN(x-1,y)
                if y>0:
                   voisins2+= voisinageVonN(x-1,y-1)
                if y<NbC-1:
                    voisins2+= voisinageVonN(x-1,y+1)
                
            if x<NbC:
                if y<NbC:
                    voisins2+= voisinageVonN(x,y)
                if y>0:
                   voisins2+= voisinageVonN(x,y-1)
                if y<NbC-1:
                    voisins2+= voisinageVonN(x,y+1)
                    
            if x<(NbC-1):
                if y<NbC:
                    voisins2+= voisinageVonN(x+1,y)
                if y>0:
                   voisins2+= voisinageVonN(x+1,y-1)
                if y<NbC-1:
                    voisins2+= voisinageVonN(x+1,y+1)
            num1=random.random()
            num2=random.random()
            
            if etat[x][y] == state["FIRE"]:
                temp[x][y] = state["ASH"] 
                ash=ash+1
                
            
            if etat[x][y] == state["TREE"] and nb_voisins>=1:
                temp[x][y] = state["FIRE"]
                
#            elif etat[x][y] == state["TREE"] and voisins2>2:
#                temp[x][y] = state["FIRE"]
                
            elif etat[x][y] == state["TREE"]:
                temp[x][y] = state["TREE"]
            elif etat[x][y] == state["ASH"]:
                temp[x][y] = state["ASH"]

    etat = temp.copy()

#Defining a Von Neumann neighborhood
def voisinageVonN(i,j):
    nb_voisins = 0
    if j<(NbC-1) and etat[i][(j+1)] == state["FIRE"]:
            nb_voisins += 1

    if i<(NbL-1) and etat[(i+1)][j] == state["FIRE"]:
            nb_voisins += 1


    if i<NbL and j>0:
        if etat[i][(j-1)] == state["FIRE"]:
            nb_voisins += 1
    if j<NbC and i>0:
        if etat[(i-1)][j] == state["FIRE"]:
            nb_voisins += 1

    return nb_voisins
    
#Defining a Moore neighborhood
    
def voisinageMoore(i,j):
    nb_voisins = 0
    if j<(NbC-1) and etat[i][(j+1)] == state["FIRE"]:
            nb_voisins += 1

    if i<(NbL-1) and etat[(i+1)][j] == state["FIRE"]:
            nb_voisins += 1


    if i<NbL and j>0:
        if etat[i][(j-1)] == state["FIRE"]:
            nb_voisins += 1
    if j<NbC and i>0:
        if etat[(i-1)][j] == state["FIRE"]:
            nb_voisins += 1
            
    if i<(NbL-1) and j<(NbC-1) and etat[(i+1)][j+1] == state["FIRE"]:
            nb_voisins += 1

    if i>0 and j<(NbC-1) and etat[(i-1)][j+1] == state["FIRE"]:
            nb_voisins += 1
            
    if j>0 and i<(NbC-1) and etat[(i+1)][j-1] == state["FIRE"]:
            nb_voisins += 1
            
    if j>0 and i>0 and etat[(i-1)][j-1] == state["FIRE"]:
        nb_voisins += 1

    return nb_voisins

# Drawing the cells
def draw():
    for x in range(NbL):
        for y in range(NbC):
            if etat[x,y]==state["OFF"]:
                coul = "white"
            elif etat[x,y]==state["FIRE"]:
                coul = "red"
            elif etat[x,y]==state["TREE"]:
                coul = "green"
            elif etat[x,y]==state["ASH"]:
                coul = "black"
            canvas.itemconfig(cell[x,y], fill=coul)

# Animation stop
def stop():
    global flag
    flag=0

# Animation start
def start():
    global flag
    if flag==0: 
        flag=1
    iterate()

# Animation step by step
def stepbystep():
    global flag
    flag=2
    iterate()

# Mouse click functions
def  FireCell(event):
    x, y = event.x//a, event.y//a
    etat[x,y]=state["FIRE"]
    color = "red"

    canvas.itemconfig(cell[x][y], fill=color)
    
def  TreeCell(event):
    x, y = event.x//a, event.y//a
    if etat[x,y]==state["OFF"]:
        etat[x,y]=state["TREE"]
        color = "green"
    else:
        etat[x,y]=state["OFF"]
        color = "white"
    canvas.itemconfig(cell[x][y], fill=color)

# Grpahic Interface
fenetre = Tk()
fenetre.title("Fire propagation")
canvas = Canvas(fenetre, width=a*NbC+1, height=a*NbL+1, highlightthickness=0)
fenetre.wm_attributes("-topmost", True) 


canvas.bind("<Button-1>", TreeCell)
canvas.bind("<Button-3>", FireCell)

canvas.pack()
canvas.create_text(100,400,text="ash")

bou1 = Button(fenetre,text='Exit', width=8, command=fenetre.destroy)
bou1.pack(side=RIGHT)
bou2 = Button(fenetre, text='Start', width=8, command=start)
bou2.pack(side=LEFT)
bou3 = Button(fenetre, text='Stop', width=8, command=stop)
bou3.pack(side=LEFT)
bou4 = Button(fenetre, text='Step', width=8, command=stepbystep)
bou4.pack(side=LEFT)
canvas.create_text(100,10,text="ash")

# Launching automata
ash=0
flag = 0
initialize_map()
draw()
iterate()
fenetre.mainloop()

