import pygame, sys
from pygame.locals import *
import random
pygame.init()
fps=60
fpsClock=pygame.time.Clock()
#SCREEN
screen_width=1000
screen_height=500
screen=pygame.display.set_mode((screen_width,screen_height))
pygame.display.set_caption('Ping pong game')
#BALL, PLAYER, OPPONENT
ball=pygame.Rect(screen_width/2-15,screen_height/2-15,30,30)
player=pygame.Rect(screen_width-20,screen_height/2-70,10,140)
opponent=pygame.Rect(10,screen_height/2-70,10,140)
bg_color=pygame.Color('Grey12')
light_grey=(200,200,200)

#BALL
ball_speed_x=7*random.choice((1,-1))
ball_speed_y=7*random.choice((1,-1))

def ball_animation():
    global ball_speed_x, ball_speed_y,player_score,opponent_score,score_time
    ball.x+=ball_speed_x
    ball.y+=ball_speed_y
    if ball.left<=0:
        player_score+=1               
        score_time=pygame.time.get_ticks()
    if ball.right>=screen_width:
        opponent_score+=1
        score_time=pygame.time.get_ticks()
    if ball.top<=0 or ball.bottom>=screen_height:
        ball_speed_y*=-1
    if ball.colliderect(player) and ball_speed_x>0:
        if abs(ball.right-player.left)<10:
            ball_speed_x*=-1
        elif abs(ball.bottom-player.top)<10 and ball_speed_y>0:
            ball_speed_y*=-1
        elif abs(ball.top-player.bottom)<10 and ball_speed_y<0:
            ball_speed_y*=-1
    if ball.colliderect(opponent) and ball_speed_x<0:
        if abs(ball.left-opponent.right)<10:
            ball_speed_x*=-1
        elif abs(ball.bottom-opponent.top)<10 and ball_speed_y>0:
            ball_speed_y*=-1
        elif abs(ball.top-opponent.bottom)<10 and ball_speed_y<0:
            ball_speed_y*=-1
        
def ball_start():
    global ball_speed_x,ball_speed_y,score_time
    current_time=pygame.time.get_ticks()
    ball.center=(screen_width/2,screen_height/2)
    if current_time-score_time<700:
        number_three=game_font.render("3",False,light_grey)
        screen.blit(number_three,(screen_width/2-7,screen_height/2))
    if 700<current_time-score_time <1400:
        number_two=game_font.render("2",False,light_grey)
        screen.blit(number_two,(screen_width/2-7,screen_height/2))
    if current_time-score_time<1600:
        ball_speed_x,ball_speed_y=0,0
    elif 1600<=current_time-score_time<2100:
        ball_speed_x=9*random.choice((1,-1))
        ball_speed_y=9*random.choice((1,-1))
        score_time=None
    elif current_time-score_time>2100:
        opponent_speed=4
        score_time=None
#PLAYER
player_speed=0
def player_animation():
    if player.top<=0:
        player.top=0
    if player.bottom>=screen_height:
        player.bottom=screen_height
#OPPONENT:
opponent_speed=random.choice((7,4))
def opponent_ai():
    global opponent_speed
    if opponent.top<=ball.y:
        opponent.top+=opponent_speed
    if opponent.top>=ball.y:
        opponent.top-=opponent_speed
    if opponent.top<=0:
        opponent.top=0
    if opponent.bottom>=screen_height:
        opponent.bottom=screen_height
#TEXT VARIABLES
player_score=0
opponent_score=0
game_font=pygame.font.Font('freesansbold.ttf',32)
#SCORE TIMER
score_time=True
#LOOP
while True:
    for event in pygame.event.get():
        #HANDLING INPUT
        if event.type==pygame.QUIT:
            pygame.quit()
            sys.exit()
        if event.type==pygame.KEYDOWN:
            if event.key==pygame.K_DOWN:
                player_speed+=7
            if event.key==pygame.K_UP:
                player_speed-=7
        if event.type==pygame.KEYUP:
            if event.key==pygame.K_DOWN:
                player_speed-=7
            if event.key==pygame.K_UP:
                player_speed+=7
    
    #BALL
    ball_animation()
    #PLAYER
    player_animation()
    player.y+=player_speed
    #OPPONENT
    opponent_ai()
    
        
    #VISUAL
    screen.fill(bg_color)
    pygame.draw.rect(screen,light_grey,player)
    pygame.draw.rect(screen,light_grey,opponent)
    pygame.draw.ellipse(screen,light_grey,ball)
    pygame.draw.aaline(screen, light_grey,(screen_width/2,0),(screen_width/2,screen_height))

    if score_time:
        ball_start()
    #TEXT
    player_text=game_font.render(f"{player_score}",False,light_grey)
    screen.blit(player_text,(screen_width/2+15,screen_height/2))

    if opponent_score<10:
        opponent_text=game_font.render(f"{opponent_score}",False,light_grey)
        screen.blit(opponent_text,(screen_width/2-27,screen_height/2)) 
    if  opponent_score>=10:
        opponent_text=game_font.render(f"{opponent_score}",False,light_grey)
        screen.blit(opponent_text,(screen_width/2-50,screen_height/2))

    #UPDATING THE WINDOW
    pygame.display.update()
    fpsClock.tick(fps)
