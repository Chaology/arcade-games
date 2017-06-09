# implementation of card game - Memory

import simplegui
import random

# helper function to initialize globals
deck1 = range(8)
deck2 = range(8)
deck = deck1 + deck2

def new_game():
    global deck, state, turns, exposed
  
    random.shuffle(deck)
    state = 0
    turns = 0
    exposed = [False for card_index in range(len(deck))]
    
    label.set_text('Turns = ' + str(turns))

     
# define event handlers
def mouseclick(pos):
    global hit, card_index, exposed, state, turns, card_index1, card_index2
    
    hit = int(pos[0]/50)
    
    if state == 0 and exposed[hit] == False:
        card_index1 = hit
        exposed[card_index1] = True
        state = 1
    elif state == 1 and exposed[hit] == False:
        card_index2 = hit
        exposed[card_index2] = True
        state = 2
        turns += 1
    elif state == 2 and exposed[hit] == False:
        if deck[card_index1] == deck[card_index2]:
            pass
        else:
            exposed[card_index1] = False
            exposed[card_index2] = False
        card_index1 = hit
        exposed[card_index1] = True
        state = 1
    label.set_text('Turns = ' + str(turns))
                        
# cards are logically 50x100 pixels in size    
def draw(canvas):
    for card_index in range(len(deck)):
        card_pos = 50 * card_index
        if exposed[card_index]:
            canvas.draw_text(str(deck[card_index]),[card_pos + 10,60],40,'White')
        else:
            canvas.draw_polygon([[card_pos,0],[50 + card_pos,0],[50 + card_pos,100],[card_pos,100]],4,'Green','Black')
               

# create frame and add a button and labels
frame = simplegui.create_frame("Memory", 800, 100)
frame.add_button("Reset", new_game)
label = frame.add_label("Turns = 0")

# register event handlers
frame.set_mouseclick_handler(mouseclick)
frame.set_draw_handler(draw)

# get things rolling
new_game()
frame.start()


# Always remember to review the grading rubric