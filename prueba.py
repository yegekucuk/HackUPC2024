import pygame
from random import randrange
import face
import cv2

# Head Controller Branch

# start the camera
face_cascade = cv2.CascadeClassifier(cv2.data.haarcascades + 'haarcascade_frontalface_default.xml')
cap = cv2.VideoCapture(0)
if not cap.isOpened():
    print("Cannot open camera")
    exit(1)
change, location = face.getDeltaLoc()

# resolution
# res = (800,600)
res = (1920,1080)
res_x = res[0]
res_y = res[1]

# pygame setup
pygame.init()
screen = pygame.display.set_mode(res)
clock = pygame.time.Clock()
running = True
start_game = False
# text font
font_size = 100
my_font = pygame.font.SysFont('Comic Sans MS', font_size)
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

    screen.fill("#000000")
    rgb_white = (255,255,255)
    text_surface = my_font.render("Click to start game", False, rgb_white)
    screen.blit(text_surface, (650,500))
    pygame.display.flip()
    clock.tick(60)

obstacle_size = 30
character_size = 40
pos = pygame.Vector2(randrange(1920), randrange(1080))
collision_rect = pygame.Rect(pos[0], pos[1], character_size*2, character_size*2)
collision = 0
acceleration = 10

while running:
    # poll for events
    # pygame.QUIT event means the user clicked X to close your window
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()

    # fill the screen with a color to wipe away anything from last frame
    screen.fill("#EB89FF")

    pygame.draw.circle(screen, "blue", player_pos, character_size)

    #keys = pygame.key.get_pressed()
    #if keys [pygame.K_w]:
    #    player_movement = [0,-1]
    #if keys[pygame.K_s]:
    #    player_movement = [0,1]
    #if keys[pygame.K_a]:
    #    player_movement = [-1,0]
    #if keys[pygame.K_d]:
    #    player_movement = [1,0]

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
    pygame.draw.circle(screen, "green", pos, obstacle_size)
    collision = collision_rect.colliderect(player_rect)
    if collision:
        pos = pygame.Vector2(randrange(1920), randrange(1080))
        collision_rect = pygame.Rect(pos[0], pos[1], obstacle_size*2, obstacle_size*2)

    # flip() the display to put your work on screen
    pygame.display.flip()

    clock.tick(60)  # limits FPS to 60

while True:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
    screen.fill("#000000")
    
    text_surface = my_font.render("GAME OVER", False, rgb_white)
    screen.blit(text_surface, ((res_x//2)-font_size, (res_y//2)-font_size))
    pygame.display.flip()
    clock.tick(60)
