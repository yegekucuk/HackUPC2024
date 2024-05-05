from random import randint

# resolution of the game
res = (1280, 720)
res_x = res[0]
res_y = res[1]

# pygame text font
font_size = 30
point_font_size = 30

# properties
goal_size = 100
character_size = 120
    #collision = 0
acceleration = 10
time_given = 180

# color
rgb_white = (255,255,255)
rgb_black = (0,0,0)

#images
pieces = 7
bee_img_loc = f"img/Bee{randint(1,7)}.png"
flower_img_loc = f"img/Flower1.png"

#face-cam
fc_width = 300
fc_height = 300