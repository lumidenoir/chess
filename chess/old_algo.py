import numpy as np
a=[[0,0,0,0,0,0,0,0,8],[0,0,0,0,0,0,0,0,7],[0,0,0,0,0,0,0,0,6],[0,0,0,0,0,0,0,0,5],[0,0,0,0,0,0,0,0,4],[0,0,0,0,0,0,0,0,3],[0,0,0,0,0,0,0,0,2],[0,0,0,0,0,0,0,0,1],['A','B','C','D','E','F','G','H','#']]
#NOTE - piece declaration=[[color,status],[position],[piece type,piece type status]]
#SECTION - variable declaration
#TODO - dictionary method application and gameplay
bpawn1,bpawn2,bpawn3,bpawn4,bpawn5,bpawn6,bpawn7,bpawn8=np.array([[0,0],[1,0],[112,0]]),np.array([[0,0],[1,1],[112,0]]),np.array([[0,0],[1,2],[112,0]]),np.array([[0,0],[1,3],[112,0]]),np.array([[0,0],[1,4],[112,0]]),np.array([[0,0],[1,5],[112,0]]),np.array([[0,0],[1,6],[112,0]]),np.array([[0,0],[1,7],[112,0]])
wpawn1,wpawn2,wpawn3,wpawn4,wpawn5,wpawn6,wpawn7,wpawn8=np.array([[1,0],[6,0],[80,0]]),np.array([[1,0],[6,1],[80,0]]),np.array([[1,0],[6,2],[80,0]]),np.array([[1,0],[6,3],[80,0]]),np.array([[1,0],[6,4],[80,0]]),np.array([[1,0],[6,5],[80,0]]),np.array([[1,0],[6,6],[80,0]]),np.array([[1,0],[6,7],[80,0]])
wrook1,wrook2,brook1,brook2=np.array([[1,0],[7,0],[82,0]]),np.array([[1,0],[7,7],[82,0]]),np.array([[0,0],[0,0],[114,0]]),np.array([[0,0],[0,7],[114,0]])
wcamel1,wcamel2,bcamel1,bcamel2=np.array([[1,0],[7,2],[66,0]]),np.array([[1,0],[7,5],[66,0]]),np.array([[0,0],[0,2],[98,0]]),np.array([[0,0],[0,5],[98,0]])
wknight1,wknight2,bknight1,bknight2=np.array([[1,0],[7,1],[78,0]]),np.array([[1,0],[7,6],[78,0]]),np.array([[0,0],[0,1],[110,0]]),np.array([[0,0],[0,6],[110,0]])
wqueen,bqueen=np.array([[1,0],[7,3],[81,0]]),np.array([[0,0],[0,3],[113,0]])
wking,bking=np.array([[1,0],[7,4],[75,0]]),np.array([[0,0],[0,4],[107,0]])
alive_pieces_black=[bpawn1,bpawn2,bpawn3,bpawn4,bpawn5,bpawn6,bpawn7,bpawn8,brook1,brook2,bcamel1,bcamel2,bknight1,bknight2,bqueen,bking]
alive_pieces_white=[wpawn1,wpawn2,wpawn3,wpawn4,wpawn5,wpawn6,wpawn7,wpawn8,wrook1,wrook2,wcamel1,wcamel2,wknight1,wknight2,wqueen,wking]
alive_pieces=alive_pieces_black+alive_pieces_white#!SECTION
killed_pieces=[]

def piesel(piece):#REVIEW - changes while implementing playing loop
    my_pieces=alive_pieces_white if piece[0,0]==1 else alive_pieces_black
    opp_pieces=alive_pieces_black if piece[0,0]==1 else alive_pieces_white
    return my_pieces,opp_pieces

def presence(mov,pieces_):
    flag=0
    for k in pieces_:
        if (k[1][0]==mov[0] and k[1][1]==mov[1]):
            flag=1
            break
    present=1 if flag==1 else 0
    return present

def futpresence(k,opp_pieces):#NOTE - a function for checking the validity of king's moves in a scenario of a possible check
    flag=0
    for mov in allkillmoves(opp_pieces):
        if (k[0]==mov[0] and k[1]==mov[1]):
            flag=1
    return flag

def npmd(move):#NOTE - not possible moves deleter
    movem=[]
    for k in move:
        if ((k[0]<=7)and(k[0]>=0)) and ((k[1]<=7)and(k[1]>=0)):
            movem.append(k)
    return movem

def kill(mov,piece_):#NOTE - a function for killing pieces by sending them to another layer
    for k in piece_:
        if k[0,1]==0 and(k[1,0]==mov[0] and k[1,1]==mov[1]):
            k[0,1]=1
            killed_pieces.append(k)
            piece_.remove(k)
    return

def pawnmov(piece):#ANCHOR - pawn movement
    movement=[]
    m = -1 if piece[0,0]==1 else 1
    my_pieces, opp_pieces=piesel(piece)
    mov1,mov2,mov3,mov4=piece[1]+[m,0],piece[1]+[m,1],piece[1]+[m,-1],piece[1]+[2*m,0]
    if ((piece[1,0]<7)and(piece[1,0]>0)) or ((piece[1,1]<7)and(piece[1,1]>0)):
        if piece[2,1]==0 and not(presence(mov4,my_pieces) or presence(mov4,opp_pieces) or presence(mov1,my_pieces) or presence(mov1,opp_pieces)):
            movement.append(mov4)
        if not(presence(mov1,my_pieces) or presence(mov1,opp_pieces)):
            movement.append(mov1)
        if presence(mov2,opp_pieces):
            movement.append(mov2)
        if presence(mov3,opp_pieces):
            movement.append(mov3)
    #print(npmd(movement))
    return npmd(movement)

def rookmov(piece):#ANCHOR - rook movement
    movement=[]
    flag1,flag2,flag3,flag4=0,0,0,0
    my_pieces, opp_pieces=piesel(piece)
    for i in [1,2,3,4,5,6,7]:
        mov=piece[1]+[i,0]
        if flag1==0:
            if not(presence(mov,my_pieces)):
                movement.append(mov)
            else:
                flag1=1
            if (presence(mov,opp_pieces)):
                movement.append(mov)
                flag1=1
        mov=piece[1]+[-i,0]
        if flag2==0:
            if not(presence(mov,my_pieces)):
                movement.append(mov)
            else:
                flag2=1
            if (presence(mov,opp_pieces)):
                movement.append(mov)
                flag2=1
        mov=piece[1]+[0,i]
        if flag3==0:
            if not(presence(mov,my_pieces)):
                movement.append(mov)
            else:
                flag3=1
            if (presence(mov,opp_pieces)):
                movement.append(mov)
                flag3=1
        mov=piece[1]+[0,-i]
        if flag4==0:
            if not(presence(mov,my_pieces)):
                movement.append(mov)
            else:
                flag4=1
            if (presence(mov,opp_pieces)):
                movement.append(mov)
                flag4=1
    return (npmd(movement))

def knightmov(piece):#ANCHOR - knight movement
    my_pieces, opp_pieces=piesel(piece)
    movements=[]
    moves=[piece[1]+[2,1],piece[1]+[2,-1],piece[1]+[1,2],piece[1]+[1,-2],piece[1]+[-2,1],piece[1]+[-2,-1],piece[1]+[-1,2],piece[1]+[-1,-2]]
    for j in moves:
        if not(presence(j,my_pieces)):
            movements.append(j)
    return (npmd(movements))

def camelmov(piece):#ANCHOR - bishop movement
    movement=[]
    flag1,flag2,flag3,flag4=0,0,0,0
    my_pieces, opp_pieces=piesel(piece)
    for i in [1,2,3,4,5,6,7]:
        mov=piece[1]+[i,i]
        if flag1==0:
            if not(presence(mov,my_pieces)):
                movement.append(mov)
            else:
                flag1=1
            if (presence(mov,opp_pieces)):
                movement.append(mov)
                flag1=1
        mov=piece[1]+[-i,-i]
        if flag2==0:
            if not(presence(mov,my_pieces)):
                movement.append(mov)
            else:
                flag2=1
            if (presence(mov,opp_pieces)):
                movement.append(mov)
                flag2=1
        mov=piece[1]+[-i,i]
        if flag3==0:
            if not(presence(mov,my_pieces)):
                movement.append(mov)
            else:
                flag3=1
            if (presence(mov,opp_pieces)):
                movement.append(mov)
                flag3=1
            mov=piece[1]+[i,-i]
        if flag4==0:
            if not(presence(mov,my_pieces)):
                movement.append(mov)
            else:
                flag4=1
            if (presence(mov,opp_pieces)):
                movement.append(mov)
                flag4=1
    return npmd(movement)

def queenmov(piece):
    movement=rookmov(piece)+camelmov(piece)
    return movement

def allkillmoves(pieces):
    movement=[]
    for piece in pieces:
        k=piece[2,0]
        if k==112 or k==80:
            m = -1 if piece[0,0]==1 else 1
            mov=[piece[1]+[m,1],piece[1]+[m,-1]]
            movement=movement+mov
        if k==82 or k==114:
            movement=movement+rookmov(piece)
        if k==66 or k==98:
            movement=movement+camelmov(piece)
        if k==75 or k==107:
            movement=movement+knightmov(piece)
        if k==81 or k==113:
            movement=movement+queenmov(piece)
    return movement

def kingmov(piece):#ANCHOR - king movement function
    my_pieces, opp_pieces=piesel(piece)
    movements=[]
    moves=[piece[1]+[1,0],piece[1]+[-1,0],piece[1]+[0,1],piece[1]+[0,-1],piece[1]+[1,1],piece[1]+[1,-1],piece[1]+[-1,1],piece[1]+[-1,-1]]
    for k in moves:
        if not(presence(k,my_pieces) or futpresence(k,opp_pieces)):
            movements.append(k)
    return (npmd(movements))

def board():
    for alive in alive_pieces:
        posn=alive[1]
        if alive[2,0]==112:
            a[posn[0]][posn[1]]='\u2659'
        if alive[2,0]==107:
            a[posn[0]][posn[1]]='\u2654'
        if alive[2,0]==113:
            a[posn[0]][posn[1]]='\u2655'
        if alive[2,0]==114:
            a[posn[0]][posn[1]]='\u2656'
        if alive[2,0]==98:
            a[posn[0]][posn[1]]='\u2657'
        if alive[2,0]==110:
            a[posn[0]][posn[1]]='\u2658'
        if alive[2,0]==75:
            a[posn[0]][posn[1]]='\u265a'
        if alive[2,0]==81:
            a[posn[0]][posn[1]]='\u265b'
        if alive[2,0]==82:
            a[posn[0]][posn[1]]='\u265c'
        if alive[2,0]==66:
            a[posn[0]][posn[1]]='\u265d'
        if alive[2,0]==78:
            a[posn[0]][posn[1]]='\u265e'
        if alive[2,0]==80:
            a[posn[0]][posn[1]]='\u265f'
        #a[posn[0]][posn[1]]=chr(alive[2,0]) #NOTE - use this line for using ascii board
    ay=np.array(a)
    #STUB - print(ay)
    return

def movboard(movement):
    board()
    for mov in movement:
        a[mov[0]][mov[1]]='#'
    ay=np.array(a)
    return print(ay)
movboard(camelmov(wpawn2))
