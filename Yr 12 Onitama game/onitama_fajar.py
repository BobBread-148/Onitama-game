import pygame
import os
import random

pygame.init()


#STATES------------------------------------------------------
HOME = "home"
RULES = "rules"
PLAYING = "playing"
GAME_OVER = "game over"
game_state = HOME

#VARIABLES ANDF STUFF---------------------------------------------------
THIS_FOLDER = os.path.dirname(os.path.abspath(__file__))
IMAGE_FOLDER = os.path.join(THIS_FOLDER, "images")
rules_slide = 0
current_player = "blue"
selected_card = None
selected_piece = None
highlighted_squares = []
student_positions = [0, 1, 3, 4]
width, height = 1266, 668
x_positions = [70, 188, 420, 536]
card_positions = [(718,85), (955,85), (718,454), (955,454), (1040,270)]
red_hand = []
blue_hand = []
side_pile = []
winner = None
FONT = pygame.font.SysFont(None, 32)
BLACK = (0, 0, 0)


board = [
    [None, None, None, None, None],
    [None, None, None, None, None],
    [None, None, None, None, None],
    [None, None, None, None, None],
    [None, None, None, None, None]
]



CARDS = {
    "Tiger": [(2, 0), (-1, 0)],
    "Dragon": [(1, -2), (1, 2), (-1, -1), (-1, 1)],
    "Frog": [(0, -2), (1, -1), (-1, 1)],
    "Rabbit": [(0, 2), (1, 1), (-1, -1)],
    "Crab": [(2, 0), (0, -2), (0, 2)],
    "Elephant": [(0, -1), (0, 1), (1, 1), (1, -1)],
    "Rooster": [(0, -1), (1, -1), (0, 1), (-1, 1)],
    "Goose": [(0, 1), (1, 1), (0, -1), (-1, -1)],
    "Monkey": [(-1, -1), (1, -1), (-1, 1), (1, 1)],
    "Mantis": [(1, -1), (-1, 0), (1, 1)],
    "Horse" : [(1, 0), (0, -1), (-1, 0)],
    "OX" : [(0, 1), (1, 0), (-1, 0)],
    "Crane" : [(1, 0), (-1, -1), (-1, 1)],
    "Boar" : [(0, -1), (0, 1), (1, 0)],
    "Cobra" : [(0, 1), (1, -1), (-1, -1)],
    "Eel" : [(0, -1), (1, 1), (-1, 1)]
}

#FUNCTIONS------------------------------------------------------------------------------
def load_image(img_name, folder=IMAGE_FOLDER, **kwargs):
    image_path = os.path.join(folder, img_name)
    image = pygame.image.load(image_path).convert_alpha()
    rect = image.get_rect(**kwargs)
    return image, rect

def pixel_to_grid(mouse_pos):
    mouse_x, mouse_y = mouse_pos
    row = (mouse_y - 51) // 116
    col = (mouse_x - 70) // 116
    if 0 <= row < 5 and 0 <= col < 5: 
        return row, col
    else:
        return None
    
def grid_to_pixel(row, col):
    x = 70 + col * 116
    y = 51 + row * 116
    return x, y

def start_new_game():
    
    global board, blue_hand, red_hand, side_pile, current_player, game_state, selected_piece, selected_card, highlighted_squares
    board = [[None for _ in range(5)] for _ in range(5)]
    # Blue Top (Row 0), Red Bottom (Row 4)
    for col in student_positions:
        board[0][col] = Piece("blue", 0, col, blue_piece)
        board[4][col] = Piece("red", 4, col, red_piece)
    board[0][2] = Piece("blue", 0, 2, blue_master, True)
    board[4][2] = Piece("red", 4, 2, red_master, True)
    
    
    names = random.sample(list(CARDS.keys()), 5)
    card_objects = []
    for i in names:
        card_objects.append(Card(i, CARDS[i]))
    
    for i, card in enumerate(card_objects):
        card.surface, _ = load_image(f"{card.name}_card.png")
        card.rect = card.surface.get_rect(topleft=card_positions[i])    

    blue_hand = card_objects[0:2] 
    red_hand = card_objects[2:4]
    side_pile = card_objects[4]
    
    game_state = PLAYING
    current_player = "blue"
    selected_piece = selected_card = None
    highlighted_squares = []

def switch_turn():
    global current_player, blue_hand, red_hand, side_pile, selected_card

    # swap selected card with side pile
    if current_player == "blue":
        blue_hand.remove(selected_card)
        blue_hand.append(side_pile)
        side_pile = selected_card
        current_player = "red"
    else:
        red_hand.remove(selected_card)
        red_hand.append(side_pile)
        side_pile = selected_card
        current_player = "blue"

    selected_card = None

    for i, card in enumerate(blue_hand):
        card.rect.topleft = card_positions[i]

    for i, card in enumerate(red_hand):
        card.rect.topleft = card_positions[i + 2]

    side_pile.rect.topleft = card_positions[4]


#CLASSES------------------------------------------------------------------------------
class Player:
    def __init__(self, colour):
        self.colour = colour
        self.cards = []

class Piece():
    def __init__(self, colour, row, column, img, master=False):
        self.colour = colour
        self.master = master
        self.row = row
        self.col = column
        self.surface = img
        
    def new_row (self, new_row):
        self.row = new_row
        
    def new_col (self, new_col):
        self.col = new_col
        

class Card():
    def __init__(self, name, moves):
        self.name = name
        self.moves = moves
        self.rect = pygame.Rect(0,0,0,0)
        self.surface = None

    def move_options(self, piece, player_colour, current_board):
        possible_positions = []   
        flip = 1 if player_colour == "blue" else -1
        for row, col in self.moves:
            new_row, new_col = piece.row + row*flip, piece.col + col*flip
            if 0<= new_row < 5 and 0 <= new_col < 5:
                check = current_board[new_row][new_col]
                if check is None or check.colour != player_colour:
                    possible_positions.append((new_row, new_col))
        return possible_positions
            
class Game():
    def __init__(self, turn):
        self.turn = turn



#SETTING UP THE SCREEN--------------------------------------------------------------------
screen = pygame.display.set_mode((width, height))
pygame.display.set_caption("Onitama")
THIS_FOLDER = os.path.dirname(__file__)


#Loading home screen images---------------------------------------------------------
home_screen, home_rect = load_image("home_bg.png")
play_button, play_btn_homerect = load_image("play_button.png", topleft=(750,400))
_, play_btn_rulesrect = load_image("play_button.png", topleft=(493,334))
rules_button, rules_btn_rect = load_image("rules_button.png", topleft=(250,400))

#loading rules screen images--------------------------------------------------------
rules_slides = []
for i in range(1,4):
    rules_slides.append(load_image(f"rules_slide{i}.png")[0])
next_arrow, next_arrow_rect = load_image("next_arrow.png", topleft=(1061,297))
back_arrow, back_arrow_rect = load_image("back_arrow.png", topleft=(140,297))

#loading game play images-----------------------------------------------------------
game_screen, playing_rect = load_image("game_board.png")
red_piece, _ = load_image("red_piece.png")
blue_piece, _ = load_image("blue_piece.png")
red_master, _ = load_image("red_masterpiece.png")
blue_master, _ = load_image("blue_masterpiece.png")
red_wins, winner_rect = load_image("red_wins.png", center=(width//2, height//2))
blue_wins, winner_rect = load_image("blue_wins.png", center=(width//2, height//2))

        
#GAME LOOP--------------------------------------------------------------------------------
running = True
while running:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
            
        if event.type == pygame.MOUSEBUTTONDOWN:
            mouse_pos = event.pos
            
            if game_state == HOME:
                if play_btn_homerect.collidepoint(mouse_pos):
                    start_new_game()
                       
                elif rules_btn_rect.collidepoint(mouse_pos):
                    game_state = RULES
            
            elif game_state == RULES:
                if next_arrow_rect.collidepoint(mouse_pos) and rules_slide < 2:
                    rules_slide += 1
                if back_arrow_rect.collidepoint(mouse_pos):
                    if rules_slide == 0:
                        game_state = HOME
                    else:
                        rules_slide -= 1
                if play_btn_rulesrect.collidepoint(mouse_pos):
                    start_new_game()  
                    
            elif game_state == PLAYING:
                hand = blue_hand if current_player == "blue" else red_hand
                for card in hand:
                    if card.rect.collidepoint(mouse_pos):
                        selected_card = card 
                        highlighted_squares = []
                
                grid_pos = pixel_to_grid(mouse_pos)
                if grid_pos:
                    piece = board[grid_pos[0]][grid_pos[1]]
                    if piece and piece.colour == current_player:
                        selected_piece = piece
                        highlighted_squares = []
                
                if selected_card and selected_piece:
                    highlighted_squares = selected_card.move_options(selected_piece, current_player, board)
                
                if grid_pos:
                    grid_row, grid_col = grid_pos   
                    if (grid_row, grid_col) in highlighted_squares and selected_piece:
                        
                        #capture win
                        target = board[grid_row][grid_col]
                        if target and target.master:
                            winner = current_player 
                            
                        board[selected_piece.row][selected_piece.col] = None
                        selected_piece.new_row(grid_row)
                        selected_piece.new_col(grid_col)
                        board[selected_piece.row][selected_piece.col] = selected_piece
                        
                        #temple win
                        if selected_piece.master:
                            if selected_piece.colour == "blue" and (grid_row, grid_col) == (4, 2):
                                winner = "blue"
                            if selected_piece.colour == "red" and (grid_row, grid_col) == (0, 2):
                                winner = "red"
                        
                        selected_piece = None
                        highlighted_squares = []
                        valid_moves = []
                        switch_turn()
        
    if game_state == HOME:
        screen.blit(home_screen, home_rect)
        screen.blit(play_button, play_btn_homerect)
        screen.blit(rules_button, rules_btn_rect)

    elif game_state == RULES:
        screen.blit(rules_slides[rules_slide], (0,0))
        if rules_slide < 2:
            screen.blit(next_arrow, next_arrow_rect)
        if rules_slide <= 2:
            screen.blit(back_arrow, back_arrow_rect) 
        if rules_slide == 2:
            screen.blit(play_button, play_btn_rulesrect)

    elif game_state == PLAYING:
        screen.blit(game_screen, playing_rect)
        for row, col in highlighted_squares:
            x, y = grid_to_pixel(row, col)
            pygame.draw.rect(screen, (255,255,0), (x, y, 116, 116), 4)
        
        for row in range(5): 
            for col in range(5):
                piece = board[row][col]   
                if piece:
                    piece_x, piece_y = grid_to_pixel(row, col)
                    piece_rect = piece.surface.get_rect(center=(piece_x + 58, piece_y + 58))
                    screen.blit(piece.surface, piece_rect)
                    if piece == selected_piece:
                        pygame.draw.rect(screen, (255, 255, 255), (piece_x, piece_y, 116, 116), 2)
    
        for card in blue_hand:
            screen.blit(card.surface, card.rect)
            if card == selected_card:
                pygame.draw.rect(screen, (0, 255, 0), card.rect, 3)
        
        for card in red_hand:
            screen.blit(card.surface, card.rect)
            if card == selected_card:
                pygame.draw.rect(screen, (0, 255, 0), card.rect, 3)

        if side_pile:
            screen.blit(side_pile.surface, side_pile.rect)
    
    elif game_state == GAME_OVER:
        if winner == "red":
            screen.blit(red_wins, winner_rect)
        elif winner == "blue":
            screen.blit(blue_wins, winner_rect)
                                        
    if winner:                  
        game_state = GAME_OVER                 

                 

    pygame.display.flip()
pygame.quit()
