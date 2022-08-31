""" Blackjack, by Al Sweigart al@inventwithpython.com
The classic card game also known as 21. (This version doesn't have splitting 
or insurance.)
More info at: https://en.wikipedia.org/wiki/Blackjack """

import random, sys

#Set up the constants:
HEARTS = chr(9829) # Character 9829 is '♥'
DIAMONDS = chr(9830) # Character 9830 is '♦'
SPADES = chr(9824) # Character 9824 is '♠'
CLUBS = chr(9827) # Character 9827 is '♣'
# (A list of chr codes is at https://inventwithpython.com/charactermap)
BACKSIDE = 'backside'


def main():
    print('''Blackjack, by Al Sweigart al@inventwithpython.com
          
    Rules:
        Try to get as close to 21 without going over.
        Kings, Queens, and Jacks are worth 10 points.
        Aces are worth 1 or 11 points.
        Cards 2 through 10 are worth their face value.
        (H)it to take another card
        (S)tand to stop taking cards.
        On your first play, you can (D)ouble down to increase your bet but 
        must hit exactly one more time before standing.
        In case of tie, the bet is returned to the player.
        The dealer stops hitting at 17.''')
    
    money = 5000
    while True: #Main game loop.
        # Check if the player has run out of money.
        if money <= 0:
            print("You're broke!")
            print("Good thing you weren't playing with real money")
            print('Thanks for playing')
            sys.exit()
        
        # Let the player enter their bet for this round:
        print(f'Money: {money}')
        bet = getBet(money)
        
        # Give dealer and player two cards from deck each:
        deck = getDeck()
        dealerHand = [deck.pop(), deck.pop()]
        playerHand = [deck.pop(), deck.pop()]
        
        # Handle player actions
        print(f'Bet: {bet}')
        while True: # Keep looping until player stands of busts
            displayHands(playerHand, dealerHand, False)
            print()
        
            # check if player has bust:
            if getHandsValue(playerHand) > 21:
                break
            
            # Get the player's move, either H, S, or D:
            move = getMove(playerHand, money - bet)
            
            # Handle the player actions:
            if move == "D":
                # Player is doubling down, they can increase their bet:
                additionalBet = getBet(min(bet, (money - bet)))
                bet += additionalBet
                print(f'Bet increased to {bet}.')
                print(f'Bet: {bet}')
                
            if move in ('H', 'D'):
                # Hit/doubling down takes another card.
                newCard = deck.pop()
                rank, suit = newCard
                print(f'You drew a {rank} of {suit}.')
                playerHand.append(newCard)
                
                if getHandsValue(playerHand) > 21:
                    #The player hand has busted:
                    continue
                
            if move in ('S', 'D'):
                # stand/doubling down stops players turn.
                break

        # Handle the dealer's action:
        if getHandsValue(playerHand) <= 21:
            while getHandsValue(dealerHand) < 17:
                #The Dealer Hits:
                print('Dealer hits...')
                dealerHand.append(deck.pop())
                displayHands(playerHand, dealerHand, False)
                    
                if getHandsValue(dealerHand) > 21:
                    break #The Dealer has busted.
            input('Press Enter to continue...')
            print('\n\n')
            
            # Show the final hands:
        displayHands(playerHand, dealerHand, True)
        playerValue = getHandsValue(playerHand)
        dealerValue = getHandsValue(dealerHand)
           
        # Handle whether the player won, lost, or tied:
        if dealerValue > 21:
            print(f'Dealer busts! You win ${bet}')
            money += bet
        elif (playerValue > 21) or (playerValue < dealerValue):
            print('You lost!')
            money -= bet
        elif playerValue > dealerValue:
            print(f'You won ${bet}')
            money += bet
        elif playerValue == dealerValue:
            print("It's a tie, the bet is returned to you.")
                
        input('Press Enter to continue...')
        print('\n\n')
                
        
def getBet(maxBet):
    """Ask the player how much thye want to bet for this round"""
    while True: #Keep asking until they enter a valid amount>
        print(f'How much do you bet? (1-{maxBet}, or QUIT)')    
        bet = input('> ').upper().strip()
        if bet == 'QUIT':
            print('Thanks for playing!')
            sys.exit()
            
        if not bet.isdecimal():
            continue #If the player didn't enter a number, ask again.
        
        bet = int(bet)
        if 1 <= bet <= maxBet:
            return bet
        
def getDeck():
    """Return a list of (rank suit) tuples for all 52 cards."""
    deck = []
    for suit in (HEARTS, DIAMONDS, SPADES, CLUBS):
        for rank in range(2,11):
            deck.append((str(rank), suit)) #Add the numbered cards
        for rank in ('J', 'Q', 'K', 'A'):
            deck.append((rank, suit)) #Add the face and ace cards.
    random.shuffle(deck)
    return deck


def displayHands(playerHand, dealerHand, showDealerHand):
    """Show the player's and dealer cards. Hide the dealers first
    card if showDealersHand is False"""
    print()
    if showDealerHand:
        print(f'DEALER: {getHandsValue(dealerHand)}')
        displayCards(dealerHand)
    else:
        print('DEALER: ???')
        #Hide the dealers first card:
        displayCards([BACKSIDE] + dealerHand[1:])
        
    #show the players cards:
        print(f'PLAYER: {getHandsValue(playerHand)}')
        displayCards(playerHand)
        
        
def getHandsValue(cards):
    """"Returns the value of the cards.  Face cards are worth 10, Aces are 
    worth 11 or 1 (This function calculates the most suitable ace value)"""
    value = 0
    numberOfAces = 0
    
    #Add the value of non-ace cards:
    for card in cards:
        rank = card[0] #card is a tuple like (rank, suit)
        if rank == 'A':
            numberOfAces += 1
        elif rank in ('K', 'Q','J'):
            value += 10
        else:
            value += int(rank) #Numbered cares are worth their face value
            
    #add the value for the aces:
    value += numberOfAces #adds one per ace
    for i in range(numberOfAces):
        #IF another 10 can be added without busting, do so:
        if value + 10 <= 21:
            value +=10
    
    return value

def displayCards(cards):
    """Display all the cards in the cards list"""
    rows = ['','','',''] #the text to display on each row
    
    for i,  card in enumerate(cards):
        rows[0] += "____  "   #Print the top line of card
        if card == BACKSIDE:
            #Print the cards back:
            rows[1]  += '|## |'
            rows[2] += '|###|'
            rows[3] += '|_##|'
            
        else: 
            #Print card front:
                rank, suit = card # The cared is a tuple data structure
                rows[1] += '|{} |'.format(rank.ljust(2))
                rows[2] += '| {} |'.format(suit)
                rows[3] += '|_{}|'.format(rank.rjust(2,'_'))
        
    for row in rows:
        print(row)
        
def getMove(playerHand, money):
    """ Ask the plaeyr for their move and returns 'H' for hit, 'S' for stand,
    and 'D' for double down. """
    while True: #Keep looping until the player enteras a correct move.
        # Determin what moves the player can make:
        moves = ['(H)it', '(S)tand']
        
        #The player can double down on their first movew, whcih we can tell
        #because they'll have exaclty two cards
        if len(playerHand) == 2 and money > 0:
            moves.append('(D)ouble down')
            
        #Get the player's move:
        movePrompt = ', '.join(moves)  + '> '
        move = input(movePrompt).upper()
        if move in ('H', 'S'):
            return move  #Player has entered valid move
        if move == 'D' and '(D)ouble down' in moves:
            return move  #Player has entered valid move
        
        
        
#if the program is run (instead of imported), run the game:
if __name__== '__main__':
    main()
        
            
            
    
    

            