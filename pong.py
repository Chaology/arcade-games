# Pong

import simplegui
import random

# initialize globals - pos and vel encode vertical info for paddles
WIDTH = 600
HEIGHT = 400       
BALL_RADIUS = 10
PAD_WIDTH = 8
PAD_HEIGHT = 80
HALF_PAD_WIDTH = PAD_WIDTH / 2
HALF_PAD_HEIGHT = PAD_HEIGHT / 2
ball_pos = [WIDTH/2,HEIGHT/2]
ball_vel = [3,1]
PAD_move_speed = 5
PAD_move_growth1 = 0
PAD_move_growth2 = 0
paddle1_pos = 120
paddle2_pos = 120
score1 = 0
score2 = 0
LEFT = False
RIGHT = True

# initialize ball_pos and ball_vel for new bal in middle of table
def spawn_ball(direction):
    global ball_pos, ball_vel
    ball_pos = [WIDTH/2,HEIGHT/2]
    if direction == RIGHT:
        ball_vel[0] = random.randrange(2,5)
        ball_vel[1] = random.randrange(1,4)
    else:
        ball_vel[0] = -random.randrange(2,5)
        ball_vel[1] = -random.randrange(1,4)
        

# define event handlers
def new_game():
    global paddle1_pos, paddle2_pos, paddle1_vel, paddle2_vel, score1, score2
    return spawn_ball(RIGHT)

def reset_game():
    global score1,score2
    score1 = 0
    score2 = 0
    return spawn_ball(RIGHT)


def draw(canvas):
    global score1, score2, paddle1_pos, paddle2_pos, ball_pos, ball_vel
    
    if 0 <= paddle1_pos + PAD_move_growth1 <= HEIGHT - PAD_HEIGHT:
        paddle1_pos += PAD_move_growth1
    if 0 <= paddle2_pos + PAD_move_growth2 <= HEIGHT - PAD_HEIGHT:
        paddle2_pos += PAD_move_growth2
        
    ball_pos[0] += ball_vel[0]
    ball_pos[1] += ball_vel[1]
    
    if ball_pos[1] <= BALL_RADIUS or ball_pos[1] >= HEIGHT - BALL_RADIUS:
        ball_vel[1] = -ball_vel[1]
        
    elif ball_pos[0] <= PAD_WIDTH + BALL_RADIUS:
        if paddle1_pos <= ball_pos[1] <= paddle1_pos + PAD_HEIGHT:
            ball_vel[0] = -ball_vel[0]*1.1
            ball_vel[1] = ball_vel[1]*1.1
        else:
            score2 += 1
            return spawn_ball(RIGHT)  
        
    elif ball_pos[0] >= WIDTH - PAD_WIDTH - BALL_RADIUS:
        if paddle2_pos <= ball_pos[1] <= paddle2_pos + PAD_HEIGHT:
            ball_vel[0] = -ball_vel[0]*1.1
            ball_vel[1] = ball_vel[1]*1.1
        else:
            score1 += 1
            return spawn_ball(LEFT)

    canvas.draw_line([WIDTH / 2, 0],[WIDTH / 2, HEIGHT], 1, "White")
    canvas.draw_line([PAD_WIDTH, 0],[PAD_WIDTH, HEIGHT], 1, "White")
    canvas.draw_line([WIDTH - PAD_WIDTH, 0],[WIDTH - PAD_WIDTH, HEIGHT], 1, "White")
    canvas.draw_circle(ball_pos,BALL_RADIUS,4,'White','White')
    canvas.draw_polygon([[0,paddle1_pos],[8,paddle1_pos],[8,paddle1_pos + PAD_HEIGHT],[0,paddle1_pos + PAD_HEIGHT]],1,'White','White')
    canvas.draw_polygon([[WIDTH-PAD_WIDTH,paddle2_pos],[WIDTH,paddle2_pos],[WIDTH,paddle2_pos + PAD_HEIGHT],[WIDTH-PAD_WIDTH,paddle2_pos + PAD_HEIGHT]],1,'White','White')      
    canvas.draw_text(str(score1),[150,80],20,'white')
    canvas.draw_text(str(score2),[450,80],20,'white')
    
def keydown(key):
    global PAD_move_growth1,PAD_move_growth2
    
    if key == simplegui.KEY_MAP['w']:
        PAD_move_growth1 -= PAD_move_speed
    elif key == simplegui.KEY_MAP['s']:
        PAD_move_growth1 += PAD_move_speed
        
    if key == simplegui.KEY_MAP['up']:
        PAD_move_growth2 -= PAD_move_speed
    elif key == simplegui.KEY_MAP['down']:
        PAD_move_growth2 += PAD_move_speed
        
def keyup(key):
    global PAD_move_growth1,PAD_move_growth2
    PAD_move_growth1 = 0 
    PAD_move_growth2 = 0

# create frame
frame = simplegui.create_frame("Pong", WIDTH, HEIGHT)
frame.set_draw_handler(draw)
frame.set_keydown_handler(keydown)
frame.set_keyup_handler(keyup)
frame.add_button('Restart',reset_game,50)


# start frame
new_game()
frame.start()
