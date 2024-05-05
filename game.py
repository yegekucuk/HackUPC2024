import pygame
from random import randrange
import face
import cv2
from const import *
import time

# game point
point = 0

# start the camera
face_cascade = cv2.CascadeClassifier(cv2.data.haarcascades + 'haarcascade_frontalface_default.xml')
cap = cv2.VideoCapture(0)
if not cap.isOpened():
    print("Cannot open camera")
    exit(1)
change, location = face.getDeltaLoc()

# pygame setup
pygame.init()
screen = pygame.display.set_mode(res)
clock = pygame.time.Clock()
running = True
start_game = False
my_font = pygame.font.SysFont('Comic Sans MS', font_size)

# player pos and movement
player_pos = pygame.Vector2(screen.get_width() / 2, screen.get_height() / 2)
player_movement = [0,0]

while True:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
        if event.type == pygame.MOUSEBUTTONUP:
            start_game = True
            break
    if start_game:
        break

    screen.fill("black")
    text_surface = my_font.render("Click to start game", False, rgb_white)
    size_of_text = text_surface.get_size()
    screen.blit(text_surface, ((res_x//2) - size_of_text[0]//2, (res_y//2) - size_of_text[1]//2))
    pygame.display.flip()
    clock.tick(60)

# random position for obstacle
pos = pygame.Vector2(randrange(res_x), randrange(res_y))
goal_rect = pygame.Rect(pos[0], pos[1], goal_size, goal_size)
# adding enemy
    #enemy_rects = []
    #enemy_rects.append((pygame.Rect(randrange(res_x), randrange(res_y), goal_size*2, goal_size*2), time.time()))
# bee image load
image = pygame.image.load(bee_img_loc)
image2 = pygame.image.load(flower_img_loc)
image = pygame.transform.scale(image, (character_size, character_size))
image2 = pygame.transform.scale(image2, (goal_size, goal_size))

start_time = time.time()
while running:
    # poll for events
    # pygame.QUIT event means the user clicked X to close your window
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()

    # fill the screen with a color to wipe away anything from last frame
    screen.fill("green")
    # creating the character
        #pygame.draw.circle(screen, "blue", player_pos, character_size)
    screen.blit(image, player_pos - pygame.Vector2(character_size/2, character_size/2))

    time_left = time_given-(time.time()-start_time)
    if time_left < 0:
        running = False

    # display point
    point_font = pygame.font.SysFont('Comic Sans MS', point_font_size)
    text_surface = point_font.render("Point: %d  Time: %d" % (point,time_left), False, rgb_black)
    screen.blit(text_surface, (0,0))
    
    change, location = face.getDeltaLoc(location[0], location[1])
    player_movement = face.getDirectionChange(change, player_movement)
    print("Change: ", change, player_movement)

    if (player_pos[0] >= 0 and player_pos[0] <= res_x):
        player_pos[0] += acceleration*player_movement[0]
    else:
        if player_pos[0] < 0:
            player_pos[0] = res_x
        else:
            player_pos[0] = 0
    
    if (player_pos[1] >= 0 and player_pos[1] <= res_y):
        player_pos[1] += acceleration*player_movement[1]
    else:
        if player_pos[1] < 0:
            player_pos[1] = res_y
        else:
            player_pos[1] = 0

    player_rect = pygame.Rect(player_pos[0], player_pos[1], character_size, character_size)
        #pygame.draw.circle(screen, "red", pos, goal_size)
    screen.blit(image2, pos - pygame.Vector2(goal_size/2, goal_size/2))
    collision = goal_rect.colliderect(player_rect)
    if collision:
        pos = pygame.Vector2(randrange(res_x), randrange(res_y))
        goal_rect = pygame.Rect(pos[0], pos[1], goal_size, goal_size)
        point += 1
        #for enemy in enemy_rects:
        #    if (time.time() - enemy[1] >= enemy_life):
        #        enemy_rects.remove(enemy)
        #        enemy_rects.append((pygame.Rect(randrange(res_x), randrange(res_y), goal_size*2, goal_size*2), time.time()))
        #    collision = enemy[0].colliderect(player_rect)
        #    if (time.time() - enemy[1] >= activation_time and collision):
        #        running = False

    # flip() the display to put your work on screen
    pygame.display.flip()

    clock.tick(60)  # limits FPS to 60

while True:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
    screen.fill("black")
    
    text_surface = my_font.render("Your score: %d" %(point), False, rgb_white)
    size_of_text = text_surface.get_size()
    text_loc = ((res_x//2) - size_of_text[0]//2, (res_y//2) - size_of_text[1]//2)
    screen.blit(text_surface, (text_loc))

    pygame.display.flip()
    clock.tick(60)
