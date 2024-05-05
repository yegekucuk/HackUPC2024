import pygame
from random import randrange
import face
import cv2
from const import *

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
    screen.blit(text_surface, (650,500))
    pygame.display.flip()
    clock.tick(60)

# random position for obstacle
pos = pygame.Vector2(randrange(res_x), randrange(res_y))
goal_rect = pygame.Rect(pos[0], pos[1], character_size*2, character_size*2)
enemy_rects = []
enemy_rects.append({pygame.Rect(randrange(res_x), randrange(res_y)), time.time()})
enemy_rects.append({pygame.Rect(randrange(res_x), randrange(res_y)), time.time()})

while running:
    # poll for events
    # pygame.QUIT event means the user clicked X to close your window
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()

    # fill the screen with a color to wipe away anything from last frame
    screen.fill("green")
    # creating the character
    pygame.draw.circle(screen, "blue", player_pos, character_size)
    
    change, location = face.getDeltaLoc(location[0], location[1])
    player_movement = face.getDirectionChange(change, player_movement)
    print("Change: ", change, player_movement)

    if (player_pos[0] >= 0 and player_pos[0] <= res_x):
        player_pos[0] += acceleration*player_movement[0]
    else:
        if player_pos[0] < 0:
            player_pos[0] = res_x # break
        else:
            player_pos[0] = 0
    
    if (player_pos[1] >= 0 and player_pos[1] <= res_y):
        player_pos[1] += acceleration*player_movement[1]
    else:
        if player_pos[1] < 0:
            player_pos[1] = res_y # break
        else:
            player_pos[1] = 0

    player_rect = pygame.Rect(player_pos[0], player_pos[1], character_size*2, character_size*2)
    pygame.draw.circle(screen, "red", pos, goal_size)
    collision = goal_rect.colliderect(player_rect)
    if collision:
        pos = pygame.Vector2(randrange(1920), randrange(1080))
        goal_rect = pygame.Rect(pos[0], pos[1], goal_size*2, goal_size*2)
    for enemy in enemy_rects:
        if (time.time() - enemy[1] >= enemy_life):
            enemy_rects.remove(enemy)
            enemy_rects.append({pygame.Rect(randrange(res_x), randrange(res_y)), time.time()})
        collision = enemy[0].colliderect(player_rect)
        if (time.time() - enemy[1] >= activation_time and collision):
            running = False

    # flip() the display to put your work on screen
    pygame.display.flip()

    clock.tick(60)  # limits FPS to 60

while True:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
    screen.fill("black")
    
    text_surface = my_font.render("GAME OVER", False, rgb_white)
    screen.blit(text_surface, ((res_x//2)-font_size, (res_y//2)-font_size))
    pygame.display.flip()
    clock.tick(60)
