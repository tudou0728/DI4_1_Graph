# coding: utf8
from tkinter import *
import os

# ############################
# Lecture du fichier
# ############################

fichier_graphe = 'graphe_ff.txt'
#test1.txt graphe_qcq.txt graphe_ff.txt

# Format du fichier :
# Pour chaque arc :
# sommet_origine - tab - sommet_destination
# (derniere ligne sans le ENTER)

LeGraphe = open(fichier_graphe,"r")
touslesarcs = LeGraphe.readlines()

INFINI = 99999

Origine = [] #起点
Destination = [] #终点
Capa_min=[]
Capa_max=[]

for un_arc in touslesarcs:
    # Decoupage du contenu d'une ligne
    cet_arc = un_arc.split("\t")
    orig = int(cet_arc[0]) #起点
    dest=int(cet_arc[1]) #终点
    capmin=int(cet_arc[2]) #最小值
    capmax=int(cet_arc[3]) #最大值
    Origine.append(orig)
    Destination.append(dest)
    Capa_min.append(capmin)
    Capa_max.append(capmax)

# ############################
# Remplissage des vecteurs
# ############################

NbSommets = max(max(Origine),max(Destination))+1
NbArcs=len(Origine)

Couleur=['-' for j in range(0,NbArcs)]
Couleur_succ=[[] for i in range(0,NbSommets)]
Couleur_prec=[[] for i in range(0,NbSommets)]
succ=[[] for i in range (NbSommets)]
prec=[[] for i in range (NbSommets)]



for u in range(0,NbArcs):
    succ[Origine[u]].append(Destination[u])
    prec[Destination[u]].append(Origine[u])
    Couleur_succ[Origine[u]].append('N')
    Couleur_prec[Destination[u]].append('N')

print(Origine)
print(Destination)
print(succ)
print(prec)
Marque = [0 for j in range(0,NbSommets)]
Predecesseur = [-1 for j in range(0,NbSommets)]
Successeur = [-1 for j in range(0,NbSommets)]

Marque2 = [0 for j in range(0,NbSommets)]
Predecesseur2 = [-1 for j in range(0,NbSommets)]
Successeur2 = [-1 for j in range(0,NbSommets)]

Marque3 = [0 for j in range(0,NbSommets)]
Predecesseur3 = [-1 for j in range(0,NbSommets)]
Successeur3 = [-1 for j in range(0,NbSommets)]
Lachaine=[]

# ############################
# recherche le numero d'arc
# ############################
def chercherArc(dep,arr):
    trouve=-1
    print('\t le numero arc de',dep,'a',arr )
    i=0
    while(i<len(Origine)) and (trouve<0):
        if(Origine[i]==dep) and (Destination[i]==arr):
            trouve=i
        i=i+1
    return trouve


# ############################
# recherche chaine
# ############################
def chercherChaine(dep,arr):

    print('\t cherche chaine de',dep,'a',arr )
    Liste=[]
    Liste.append(dep)
    deja_Empile=[0]*NbSommets
    trouve=False
    while (Liste != []) and (not trouve):
        i=Liste[0]
        deja_Empile[i]=1
        Marque[i]=1
        del(Liste[0])
        for k in succ[i]:
            if k== arr:
                trouve=True
            if Marque[k]==0 and deja_Empile[k]==0:
                Liste.append(k)
                Predecesseur[k]=i
                deja_Empile[k]=1
        for m in prec[i]:
            if m==arr:
                trouve=True
            if Marque[m]==0 and deja_Empile[m]==0:
                Liste.append(m)
                Successeur[m]=i
                deja_Empile[m]=1
    print(Liste)
    print(Predecesseur)
    print(Successeur)
    print(Marque)
    return(trouve)


# ############################
# recherche chemin
# ############################
def chercherchemin(dep,arr):
    global Marque2
    print('\t cherche chemin de',dep,'a',arr )
    Liste1=[]
    Liste1.append(dep)
    deja_Empile=[0]*NbSommets
    trouve=False
    while (not trouve) and (Liste1!=[]):
        i=Liste1[0]
        deja_Empile[i]=1
        Marque2[i]=1
        del(Liste1[0])
        for k in succ[i]:
            if k== arr:
                trouve=True
            if Marque2[k]==0 and deja_Empile[k]==0:
                Liste1.append(k)
                Predecesseur2[k]=i
                deja_Empile[k]=1
    j=arr
    Liste2=[]
    Liste2.append(j)
    while(Predecesseur2[j] != dep):
        Liste2.append(Predecesseur2[j])
        j=Predecesseur2[j]
    Liste2.append(dep)
    print(Liste1)
    print(Marque2)
    print(Predecesseur2)
    return(Liste2)

# ############################
# mis a jour couleur
# ############################
def maj_couleur(flot):
    for u in range(0,NbArcs):
        if(flot[u]>=Capa_max[u]):
            Couleur[u]='V'
        else:
            if(flot[u]<=Capa_min[u]):
                Couleur[u]='N'
            else:
                Couleur[u]='R'
        i=Origine[u]
        j=Destination[u]
        k=succ[i].index(j)
        Couleur_succ[i][k]=Couleur[u]
        l=prec[j].index(i)
        Couleur_prec[j][l]=Couleur[u]
    print('\t Couleur: ',Couleur)
    print('\t Couleur_succ: ',Couleur_succ)
    print('\t Couleur_prec: ',Couleur_prec)


# ############################
# recherche cycle
# ############################
def ChercheCycle_NRV(u0):
    global Marque, Predesseur,Successeur,Lachaine
    s=Origine[u0]
    t=Destination[u0]
    if(Couleur[u0]=='N'):
        sens_u0=1
        dep=t
        arr=s
    if(Couleur[u0]=='V'):
        sens_u0=-1
        dep=s
        arr=t
    Liste=[]
    deja_Empile=[0]*NbSommets

    #找起点的所有前继结点和后继节点 而且前继结点和后继结点不能等于自己
    k=0
    for k in range(0,len(succ[dep])):
        if succ[dep][k]!=dep and Couleur_succ[dep][k]!='V':
            Liste.append(succ[dep][k])
            deja_Empile[succ[dep][k]]=1
            Predecesseur[succ[dep][k]]=dep
    k=0
    for k in range(0,len(prec[dep])):
        if prec[dep][k]!=dep and Couleur_prec[dep][k]!='N':
            Liste.append(prec[dep][k])
            deja_Empile[prec[dep][k]]=1
            Successeur[prec[dep][k]]=dep

    trouve=False
    while(Liste!=[]) and (not trouve):
        d=Liste[0]
        Marque[d]=1
        deja_Empile[d]=1
        del(Liste[0])
        for k in succ[d]:
            nume_arc=chercherArc(d,k)
            if(Couleur[nume_arc]=='N' or Couleur[nume_arc]=='R') and (k==arr) :
                trouve =True
            if(deja_Empile[k]==0) and (Marque[k]==0) and ((Couleur[nume_arc]=='N') or (Couleur[nume_arc]=='R')):
                Liste.append(k)
                deja_Empile[k]=1
                Predecesseur[k]=d
        for p in prec[d]:
            nume_arc=chercherArc(p,d)
            if Couleur[nume_arc]!='N' and (p==arr):
                trouve=True
            if(deja_Empile[p]==0) and (Marque[p]==0) and (Couleur[nume_arc] != 'N'):
                Liste.append(p)
                deja_Empile[p]==1
                Successeur[p]=d
    if(trouve):
        i=arr
        while(i!=dep):
            if(Successeur[i] != -1):
                m=Successeur[i]
                num=chercherArc(i,m)
                Lachaine.append([num,-1])
                i=m
            else:
                if(Predecesseur[i] !=-1):
                    m=Predecesseur[i]
                    num=chercherArc(m,i)
                    Lachaine.append([num,1])
                    i=m
    print('\t Marque: ',Marque)
    print('\t deja_Empile: ',deja_Empile)
    print('\t Successeur: ',Successeur)
    print('\t Predecesseur: ',Predecesseur)
    print ('\t La Chaine:',Lachaine)
    return trouve

# ############################
# compatible ou non
# ############################
def Compatible_Non(flot):
    Compatible=[0 for j in range(0,NbArcs)]
    i=0
    while(i<NbArcs):
        if(flot[i]>Capa_max[i]) or (flot[i]<Capa_min[i]):
            Compatible[i]=0
        else:
            Compatible[i]=1
        i=i+1
    return Compatible

# ############################
# compatible un arc
# ############################
def Compatible_Arc(flot):
    global Lachaine
    maj_couleur(flot)
    Compatible_liste=Compatible_Non(flot)
    compatible=sum(Compatible_liste)
    flot_compatible=True
    while(compatible != NbArcs) and (flot_compatible==True) :
        Lachaine=[]
        u0=Compatible_liste.index(0)
        trouve=ChercheCycle_NRV(u0)
        if(trouve==True):
           k=0
           epsilon=[]
           while(k<len(Lachaine)):
                if(Lachaine[k][1]==1):
                    epsilon.append(Capa_max[Lachaine[k][0]]-flot[Lachaine[k][0]])
                else:
                    epsilon.append(flot[Lachaine[k][0]]-Capa_min[Lachaine[k][0]])
                k=k+1
           eps=min(epsilon) #计算epsilon
           print(eps)
           k=0
           while(k<len(Lachaine)):
                if(Lachaine[k][1]==1):
                     flot[Lachaine[k][0]]=flot[Lachaine[k][0]]+eps
                else:
                    flot[Lachaine[k][0]]=flot[Lachaine[k][0]]-eps #重新设置流
                k=k+1
           print(flot)
           maj_couleur(flot)
           Compatible_liste=Compatible_Non(flot)
           compatible=sum(Compatible_liste)
        else:
            flot_compatible=False
    print('\t flot: ',flot)

# ############################
# Cherche cocycle
# ############################
def Cherche_Cocycle(u):
    setA=[]
    marque=[0 for j in range(0,NbSommets)]
    liste=[]
    deja_empile=[0 for j in range(0,NbSommets)]
    dep=Origine[u]
    arr=Destination[u]
    if(Couleur[u]=='N'):
        liste.append(arr)
        marque[dep]=1
        while(liste !=[]):
            i=liste[0]
            marque[i]=1
            del(liste[0])
            for k in succ[i]:
                nb=chercherArc(i,k)
                if(Couleur[nb] != 'V') and (deja_empile[k]==0)and (marque[k]==0):
                    liste.append(k)
                    deja_empile[k]=1
            for m in prec[i]:
                nb=chercherArc(m,i)
                if(Couleur[nb] != 'N') and (deja_empile[k]==0)and (marque[k]==0):
                    liste.append(m)
                    deja_empile[m]=1
        index_dep=marque.index(dep)
        marque[index_dep]=0
        for p in marque:
            if(p==1):
                setA.append(p)
    if(Couleur[u]=='V'):
        liste.append(arr)
        marque[dep]=1
        while(liste !=[]):
            i=liste[0]
            marque[i]=1
            del(liste[0])
            for k in succ[i]:
                nb=chercherArc(i,k)
                if(Couleur[nb] != 'N') and (deja_empile[k]==0)and (marque[k]==0):
                    liste.append(k)
                    deja_empile[k]=1
            for m in prec[i]:
                nb=chercherArc(m,i)
                if(Couleur[nb] != 'V') and (deja_empile[k]==0)and (marque[k]==0):
                    liste.append(m)
                    deja_empile[m]=1
        index_dep=marque.index(dep)
        marque[index_dep]=0
        for p in marque:
            if(p==0):
                setA.append(p)
    return setA

# ############################
# recherche
# ############################
print(chercherArc(1,2))
flot=[0 for j in range(0,NbArcs)]
#print(maj_couleur(flot))
#print(ChercheCycle_NRV(0))
#print(chercherChaine(4,11))
#print(chercherchemin(4,11))

# ############################
# recherche du flot compatible
# ############################
Compatible_liste=Compatible_Non(flot)
print('\t Compatible: ',Compatible_liste)
compatible=sum(Compatible_liste)
print('\t Compatible: ',compatible)
Compatible_Arc(flot)
print(Compatible_Arc(flot))

