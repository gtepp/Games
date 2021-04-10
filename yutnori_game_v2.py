# -*- coding: utf-8 -*-
"""
Yutnori Game

Created on Wed Apr  9 11:39:26 2021

@author: Gabe Tepp
"""

import matplotlib.pyplot as plt
import random
import time


# function for moving tokens

def movetoken(onP,minfo):
    
    mvtok = minfo[onP][1]
    newsp = tokeninfo[onP][mvtok][0] + minfo[onP][0] # space that token is moving to

    # handle getting on/off diagonals, center space, & finishing
    if tokeninfo[onP][mvtok][0] == 6 and minfo[onP][2][0]=='y': # if at 1st corner and taking diagonal
        newsp = 21 + minfo[onP][0]
        
        if newsp == 24: # if lands on center, use proper space number
            newsp = 28
        elif newsp>24: # if it goes past center, correct for missing space number
            newsp -= 1
        
    elif tokeninfo[onP][mvtok][0] == 11 and minfo[onP][2][0]=='y': # if at 2nd corner and taking diagonal
        newsp = 25 + minfo[onP][0]
    
    elif tokeninfo[onP][mvtok][0] == 28 and minfo[onP][3][0] == 'u': # if on center space and moving up
        newsp = 23 + minfo[onP][0]
        
        if newsp >= 26: # if it lands on or goes past corner, use proper space number
            newsp -= 10
            
    elif tokeninfo[onP][mvtok][0] in [22,23]: # on lower part of upward diagonal
        if newsp == 24: # if it landed on center, correct space
            newsp = 28
        elif newsp >= 27: # if it goes past corner, fix space
            newsp -= 11
        elif newsp in [25,26]: # if on upper part, subtract 1
            newsp -= 1
            
    elif tokeninfo[onP][mvtok][0] in [24,25]: # on upper part of upward diagonal
        if newsp >= 26: # if it lands on or goes past corner, use proper space number
            newsp -= 10
            
    elif newsp == 31: # if token lands on start from diagonal
        newsp = 21
    
    elif (newsp > 21 and tokeninfo[onP][mvtok][0] <= 21) or newsp > 31: # if token finishes
        print('\nToken has passed the finish!')
        newsp = 50 # assign finish number
    
    # assign newsp to token array
    tokeninfo[onP][mvtok][0] = newsp
                
            
    # Check for other tokens already at token's new position
    for i in range(0,4):
        # if player has token on space (and current token isn't stacked or finished)
        if i != mvtok and not (tokeninfo[onP][mvtok][1] in [0,1,2,3]) and newsp != 50 and \
            tokeninfo[onP][i][0] == newsp:  
            
            # if token on space is not already stacked
            if not (tokeninfo[onP][i][1] in [0,1,2,3]): 
                if onP == 0: # ask user about stacking 
                    print('\nYou already have a token on this space.')   
                    sttok = input('Would you like to stack these tokens? (yes or no):')
                else:
                    sttok = minfo[onP][4]
            elif tokeninfo[onP,i,2] in [0,1,2,3]: # make sure not to stack if already stacked
                sttok = 'n'    
    
            # if tokens are to be stacked, change status
            if sttok == 'y': 
                tokeninfo[onP][mvtok][1] = i
                tokeninfo[onP][i][1] = mvtok
                print('Tokens ',mvtok+1,' and ',i+1,' are now stacked.')
            
            break
        
        # if other player has token on space
        elif newsp != 50 and (tokeninfo[onP-1][i][0] == newsp or \
                              (tokeninfo[onP-1][i][0] == 1 and newsp == 21) or \
                                  (tokeninfo[onP-1][i][0] == 21 and newsp == 1)): 
            print('\nOh no! There\'s already a token here. Clear it off the board.')
            
            # first check to see if it's stacked
            if tokeninfo[onP-1][i][1] in [0,1,2,3]:
                tokeninfo[onP-1][tokeninfo[onP-1][i][1]][:] = [0,-1] # if so, reset all columns for stacked token 
            
            tokeninfo[onP-1][i][:] = [0,-1] # reset all columns for that token 
            

    # Check whether token is stacked
    if tokeninfo[onP][mvtok][1] in [0,1,2,3]: # if so, move the stacked token too
         tokeninfo[onP][tokeninfo[onP][mvtok][1]][0] = newsp
    
    return

    
    
# function for showing game board
    
def showboard(tokcol):
    
    # coordinates of spaces
    coords = [[-1,0,1,2,3,4,5,5,5,5,5,5,4,3,2,1,0,0,0,0,0,0,25/6,10/3,5/3,5/6,25/6,10/3,2.5,5/3,5/6],\
              [-1,0,0,0,0,0,0,1,2,3,4,5,5,5,5,5,5,4,3,2,1,0,5/6,5/3,10/3,25/6,25/6,10/3,2.5,5/3,5/6]]
              
    plt.figure(figsize=(12,12))
    
    # plot spaces
    plt.scatter([0,5,5,0,2.5],[0,0,5,5,2.5],s=5000,color=[0.25,0.25,0.25],marker='o',edgecolors='k') # plot corners and center
    plt.scatter([1,2,3,4,5,5,5,5,1,2,3,4,0,0,0,0],[0,0,0,0,1,2,3,4,5,5,5,5,1,2,3,4], \
                s=3000,color='w',marker='o',edgecolors='k') # plot outside spaces
    plt.scatter([x*5/6 for x in [1,2,4,5,1,2,4,5]],[5/6*x for x in [1,2,4,5,5,4,2,1]],
                s=3000,color='w',marker='o',edgecolors='k') # plot diagonal spaces
    
    # plot arrows
    plt.arrow(0,-0.75,2,0,width=0.05) # below
    plt.arrow(5.75,0,0,2,width=0.05) # right
    plt.arrow(3.75,0.5,-0.4,0.4,width=0.03) # lower diagonal
    plt.arrow(3.75,4.5,-0.4,-0.4,width=0.03) # upper diagonal
    
    # plot tokens
    for onP in range(0,2):
    
        for i in range(0,4):
            
            # user's tokens
            if tokeninfo[onP][i][0] == 0: # not started
                plt.scatter(onP-2,i+1,s=1500,color=tokcol[onP],marker='o',edgecolors='k') # plot tokens
                plt.text(onP-2,i+1,i+1,fontsize=20) # label tokens
            elif tokeninfo[onP][i][0] == 50: # if finished
                plt.scatter(onP-2,i+1,s=1500,color=tokcol[onP],marker='o',edgecolors='k') # plot tokens
                plt.text(onP-2,i+1,i+1) # label tokens
                plt.scatter(onP-2,i+1,s=2000,marker='x',color='k',linewidths=3) # plot crosses
            else: # on the board
                plt.scatter(coords[0][tokeninfo[onP][i][0]],coords[1][tokeninfo[onP][i][0]], \
                            s=2000,color=tokcol[onP],marker='o',edgecolors='k') # plot tokens
                plt.text(coords[0][tokeninfo[onP][i][0]],coords[1][tokeninfo[onP][i][0]],i+1,fontsize=20) # label player's tokens
                
            
    plt.axis([-3,6,-1,6])
    plt.xticks([]) # get rid of x tick labels
    plt.yticks([]) # get rid of y tick labels
    plt.show()
    
    return

def computermove(complvl,moves):
    # make decisions about which token to move
    mvtok = -1         

    if complvl == 3: # for hard level only
        for i in range(0,4):
            if tokeninfo[1][i][0] != 50: # if token isn't finished
                # try to knock off user's tokens
                for j in range(0,4):
                    if tokeninfo[1][i][0]+moves == tokeninfo[0][j][0]:
                        mvtok = i
                        break
                
                break
        
    # finish if possible 
    for i in range(0,4):  
        if mvtok == -1 and tokeninfo[1][i][0] != 50: # if token isn't finished
            if tokeninfo[1][i][0]+moves > 21 or tokeninfo[1][i][0]+moves > 31:
                mvtok = i
                break
    
    # go to corner/center/end
    for i in range(0,4):
        if mvtok == -1 and tokeninfo[1][i][0] != 50: # if token isn't finished
            if complvl == 3 and tokeninfo[1][i][0]+moves in [6,11,21,28,31]:
                mvtok = i
                break

    # move stacked tokens
    for i in range(0,4):
        if complvl == 2 and mvtok == -1 and tokeninfo[1][i][0] != 50: # if token isn't finished
            if tokeninfo[1][i][1] in [0,1,2,3]:
                mvtok = i
                break
    
    # move token if on a corner or center
    for i in range(0,4):
        if mvtok == -1 and tokeninfo[1][i][0] != 50: # if token isn't finished
            if tokeninfo[1][i][0] in [6,11,28]:
                mvtok = i
                break
    
    # randomly choose which token to move if no good choices
    while mvtok == -1:
        mvtok = random.randint(0,3)
        # check if random token is finished
        if tokeninfo[1][mvtok][0] == 50:
            mvtok = -1
    
    return mvtok
    
# function to check for winner

def haswon():
    
    p1sum = 0
    p2sum = 0
    
    for i in range(0,4):
        if tokeninfo[0][i][0] == 50:
            p1sum += 1
            
        if tokeninfo[1][i][0] == 50:
            p2sum += 1
    
    if p1sum == 4:  
        print('\n**** You won!! ****')
        return True
        
    elif p2sum == 4:
        print('\n**** The computer won. Better luck next time. ****')
        return True
    
    else:
        return False


# Initialize variables and arrays

global tokeninfo
tokeninfo = [[[0,-1],[0,-1],[0,-1],[0,-1]],[[0,-1],[0,-1],[0,-1],[0,-1]]] # players (2), tokens (4), and info (space, stacked?)

onP = random.randint(0,1) # which player's turn it is
playerinfo = [[0,0,'y','d','y'],[0,0,'y','d','y']] # num_moves, move_token, takediag, upordown, stack_tokens
tossseqpl = [1,1,1,2,2,2,3,3,3,4,5] # possible toss outcomes for user

# Ask player for computer level

print('\n----------\nWelcome to the game of Yutnori!\n')
complvl = input('Choose the computer\'s difficulty level (1=easy, 2=medium, 3=hard): ') # computer's level (1=easy, 2=medium, 3=hard) - add this in later
playertc = input('Choose your token color (red, blue, green, yellow, magenta): ')
print('----------')

# Set up some settings

# computer level settings (default is 2)
if not complvl: # if not chosen
    complvl = 2
else:
    complvl = int(complvl)

if complvl == 1:
    playerinfo[1][4] = 'n'
    tossseq = [tossseqpl,[1,1,1,1,1,2,2,2,2,2,2,3,3,3,3,3,4,5]]
elif complvl == 3:
    tossseq = [tossseqpl,tossseqpl]
else:
    tossseq = [tossseqpl,[1,1,1,1,2,2,2,2,3,3,3,3,4,5]]

# token colors
if not playertc: # default if player didn't input an answer
    tokcol = ['b','r']
elif playertc[0] == 'r':
    tokcol = ['r','b']
elif playertc[0] in ['b','g','y','m']:
    tokcol = [playertc[0],'r']
else: # go to default if player didn't choose option
    tokcol = ['b','r']
        

# Display empty board
showboard(tokcol)

# Play game

while haswon() == False:
      
    # toss sticks
    playerinfo[onP][0] = random.choice(tossseq[onP][:])
    
    if onP==0: # tell user of moves
        
        print('\nIt\'s your turn!')
        print('You can move a token ',playerinfo[onP][0],' spaces.\n')
        
        # ask for which token to move
        goodT = 0
        while goodT == 0:
            playerinfo[onP][1] = input('Which token would you like to move? (1-4): ')
            
            if playerinfo[onP][1] in ['1','2','3','4']: # if good number entered
                playerinfo[onP][1] = int(playerinfo[onP][1]) - 1 # adjust for indexing
            
                if tokeninfo[0][playerinfo[onP][1]][0] == 50:
                    print('This token has already finished. Please choose another one to move.')
                elif playerinfo[onP][1] in [0,1,2,3]: # if it's an actual token number
                    goodT = 1
            else:
                print('Please enter a number 1-4.')
            
        
        # check for corner or center position
        if tokeninfo[0][playerinfo[onP][1]][0] in [6,11]:
            playerinfo[0][2] = input('Take the diagonal path? (yes or no): ')
        elif tokeninfo[0][playerinfo[onP][1]][0] == 28:
            playerinfo[0][3] = input('Move up or down?: ')
            
    else: 
        
        print('\nIt\'s the computer\'s turn!')
        print('It can move a token ',playerinfo[onP][0],' spaces.\n')
        time.sleep(2) # pause for 3 sec so user can read & think
         
        # set up computer moves
        if complvl == 3:
           playerinfo[onP][1] = computermove(complvl,playerinfo[onP][0])
            
        elif complvl == 1:
            # always move same token until finished, going in sequential order 
            for i in range(0,4):
                if tokeninfo[1][i][0] != 50:
                    playerinfo[onP][1] = i
                    break
                        
        else:         
           playerinfo[onP][1] = computermove(complvl,playerinfo[onP][0]) 
        
    movetoken(onP,playerinfo)
    
    # print out board for player to see    
    showboard(tokcol)
    
    # switch to other player unless current player rolled 4 or 5
    if playerinfo[onP][0] in [4,5]:
        print('\nPlayer gets an extra turn!')
    else:
        onP = abs(onP-1)
    
