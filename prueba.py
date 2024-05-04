import pygame

# pygame setup
pygame.init()
screen = pygame.display.set_mode((1920, 1080))
clock = pygame.time.Clock()
running = True
start_game = False
my_font = pygame.font.SysFont('Comic Sans MS', 100)
player_pos = pygame.Vector2(screen.get_width() / 2, screen.get_height() / 2)
player_movement = [0,0]

while True:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
        if event.type == pygame.MOUSEBUTTONUP:
            start_game = True
            break
    if start_game:
        break

    screen.fill("#000000")
    text_surface = my_font.render("Click to start game", False, (255, 255, 255))
    screen.blit(text_surface, (650,500))
    pygame.display.flip()
    clock.tick(60)

while running:
    # poll for events
    # pygame.QUIT event means the user clicked X to close your window
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False

    # fill the screen with a color to wipe away anything from last frame
    screen.fill("#EB89FF")

    pygame.draw.circle(screen, "blue", player_pos, 40)

    keys = pygame.key.get_pressed()
    if keys [pygame.K_w]:
        player_movement = [0,-1]
    if keys[pygame.K_s]:
        player_movement = [0,1]
    if keys[pygame.K_a]:
        player_movement = [-1,0]
    if keys[pygame.K_d]:
        player_movement = [1,0]

    if (player_pos[0] >= 0 and player_pos[0] <= 1920):
        player_pos[0] += 10*player_movement[0]
    elif (player_pos[0] <= 0 and player_movement[0] > 0):
        player_pos[0] += 10*player_movement[0]
    elif (player_pos[0] >= 1920 and player_movement[0] < 0):
        player_pos[0] += 10*player_movement[0]
    if (player_pos[1] >= 0 and player_pos[1] <= 1080):
        player_pos[1] += 10*player_movement[1]
    elif (player_pos[1] <= 0 and player_movement[1] > 0):
        player_pos[1] += 10*player_movement[1]
    elif (player_pos[1] >= 1080 and player_movement[1] < 0):
        player_pos[1] += 10*player_movement[1]

    # flip() the display to put your work on screen
    pygame.display.flip()

    clock.tick(60)  # limits FPS to 60

pygame.quit()

