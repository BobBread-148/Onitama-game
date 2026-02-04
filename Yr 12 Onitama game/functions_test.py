import pygame
import os
pygame.init()

width, height = 600, 600
white = (255,255,255)

screen = pygame.display.set_mode((width, height))
pygame.display.set_caption("Step 1 - blank window")
this_folder = os.path.dirname(__file__)

def load_image(this_folder, img_name, w, h):
    image_path = os.path.join(this_folder, img_name)
    image = pygame.image.load(image_path)
    
    img_w, img_h = image.get_size()
    scale = min(w/img_w, h/img_h)
    new_size = (int(img_w * scale), int(img_h * scale))
    
    image = pygame.transform.scale(image, new_size)
    return image



running = True

while running:
    screen.fill(white)
    screen.blit(load_image(this_folder, "kai.jpg", 300, 300) , (0,0))
    
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
    pygame.display.flip()
    

    
pygame.quit()