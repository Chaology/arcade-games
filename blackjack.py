# Blackjack

import simplegui
import random

# load card sprite - 936x384 - source: jfitz.com
CARD_SIZE = (72, 96)
CARD_CENTER = (36, 48)
card_images = simplegui.load_image("http://storage.googleapis.com/codeskulptor-assets/cards_jfitz.png")

CARD_BACK_SIZE = (72, 96)
CARD_BACK_CENTER = (36, 48)
card_back = simplegui.load_image("http://storage.googleapis.com/codeskulptor-assets/card_jfitz_back.png")    

BACK_SIZE = (1680,1080)
BACK_CENTER = (1680/2,1080/2)
table_back = simplegui.load_image('https://betclick.hs.llnwd.net/e1/pict/Casino/06_Backgrounds/_EXPEKT_GAME_BKG_TABLEGAME.jpg')

LOGO_SIZE = (694,240)
LOGO_CENTER = (694/2,240/2)
logo = simplegui.load_image('http://hillarkuusk.com/assets/Horizontal%20Banner/Blackjack%20PNG%20694x240%20horizontal%20banner%20transparent.png')


# initialize some useful global variables
in_play = False
outcome = ""
score = 0

# define globals for cards
SUITS = ('C', 'S', 'H', 'D')
RANKS = ('A', '2', '3', '4', '5', '6', '7', '8', '9', 'T', 'J', 'Q', 'K')
VALUES = {'A':1, '2':2, '3':3, '4':4, '5':5, '6':6, '7':7, '8':8, '9':9, 'T':10, 'J':10, 'Q':10, 'K':10}


# define card class
class Card:
    def __init__(self, suit, rank):
        if (suit in SUITS) and (rank in RANKS):
            self.suit = suit
            self.rank = rank
        else:
            self.suit = None
            self.rank = None
            print "Invalid card: ", suit, rank

    def __str__(self):
        return self.suit + self.rank

    def get_suit(self):
        return self.suit

    def get_rank(self):
        return self.rank

    def draw(self, canvas, pos):
        card_loc = (CARD_CENTER[0] + CARD_SIZE[0] * RANKS.index(self.rank), 
                    CARD_CENTER[1] + CARD_SIZE[1] * SUITS.index(self.suit))
        canvas.draw_image(card_images, card_loc, CARD_SIZE, [pos[0] + CARD_CENTER[0], pos[1] + CARD_CENTER[1]], CARD_SIZE)
        
# define hand class
class Hand:
    def __init__(self):
        self.cards = []

    def __str__(self):
        result = ''
        for card in self.cards:
            result += ' ' + str(card)
        return result

    def add_card(self, card):
        self.cards.append(card)

    def get_value(self):
        value = 0
        contained_ace = False
        for card in self.cards:
            rank = card.get_rank()
            value += VALUES[rank]
            if rank == 'A':
                contained_ace = True
        if contained_ace and value <= 11:
            value += 10
            return value
        return value

   
    def draw(self, canvas, pos):
        for card in self.cards:
            card.draw(canvas,pos)
            pos[0] += 80
 
        
# define deck class 
class Deck:
    def __init__(self):
        self.deck = []
        for suit in SUITS:
            for rank in RANKS:
                self.deck.append(Card(suit,rank))
         
    def shuffle(self):
        random.shuffle(self.deck)

    def deal_card(self):
        return self.deck.pop(-1)
    
    def __str__(self):
        result = ''
        for card in self.deck:
            result += ' ' + str(card)
        return result



#define event handlers for buttons
def deal():
    global outcome, in_play, deck, player_hand, dealer_hand, score
    if not in_play:
        deck = Deck()
        deck.shuffle()
        
        player_hand = Hand()
        dealer_hand = Hand()
        
        player_hand.add_card(deck.deal_card())
        dealer_hand.add_card(deck.deal_card())

        player_hand.add_card(deck.deal_card())
        dealer_hand.add_card(deck.deal_card())
        
        outcome = 'Hit or Stand?'
        
        in_play = True
        
    else:
        outcome = 'You gave up, click to start a new deal'
        score -= 1
        in_play = False


def hit():
    global outcome,in_play,deck, player_hand,score
    if in_play:
        player_hand.add_card(deck.deal_card())
        print player_hand
        if player_hand.get_value() > 21:
            outcome = 'You busted! New Deal?'
            score -= 1
            print outcome
            in_play = False

    
def stand():
    global outcome, in_play, deck, dealer_hand, score
    if in_play:
        while dealer_hand.get_value() < 17:
            dealer_hand.add_card(deck.deal_card())
            print dealer_hand
        if dealer_hand.get_value() > 21:
            outcome = 'Dealer busted! New Deal?'
            print outcome
            score += 1
            in_play = False
        elif dealer_hand.get_value() >= player_hand.get_value():
            outcome = 'Dealer wins! New Deal?'
            print outcome
            score -= 1
            in_play = False
        else:
            outcome = 'You wins! New Deal?'
            print outcome
            score += 1
            in_play = False
            

# draw handler    
def draw(canvas):
    #canvas.draw_image(table_back,BACK_CENTER,BACK_SIZE,[300,300],BACK_SIZE)
    canvas.draw_image(logo,LOGO_CENTER,LOGO_SIZE,[300,55],[200,100])
    #canvas.draw_text('Blackjack',[200,50],35,'Black')
    dealer_hand.draw(canvas, [100, 150])    
    player_hand.draw(canvas, [100, 300])
    canvas.draw_text(outcome,[100,450],24,'White')
    canvas.draw_text('Your score: ' + str(score),[400,550],24,'White')
    canvas.draw_text('Dealer',[35,150],20,'White')
    canvas.draw_text('You',[50,300],20,'White')
    if in_play:
        canvas.draw_image(card_back,CARD_BACK_CENTER,CARD_BACK_SIZE,[136,198],CARD_BACK_SIZE)


# initialization frame
frame = simplegui.create_frame("Blackjack", 600, 600)
frame.set_canvas_background("Green")

#create buttons and canvas callback
frame.add_button("Deal", deal, 200)
frame.add_button("Hit",  hit, 200)
frame.add_button("Stand", stand, 200)
frame.set_draw_handler(draw)


# get things rolling
deal()
frame.start()