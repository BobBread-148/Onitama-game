import pygame
import sys
import random

# ======================
# Improved Onitama (2D)
# ======================
# - Centered board
# - Blue cards top, Red cards bottom
# - Side card on the right
# - Visual move diagram for selected card

pygame.init()

# ----------------------
# Constants
# ----------------------
WIDTH, HEIGHT = 800, 700
BOARD_SIZE = 5
CELL_SIZE = 90
FPS = 60

BOARD_PIXEL_SIZE = BOARD_SIZE * CELL_SIZE
BOARD_X = (WIDTH - BOARD_PIXEL_SIZE) // 2
BOARD_Y = (HEIGHT - BOARD_PIXEL_SIZE) // 2

WHITE = (245, 245, 245)
BLACK = (0, 0, 0)
RED = (200, 60, 60)
BLUE = (60, 100, 200)
GRAY = (200, 200, 200)
YELLOW = (240, 220, 120)
GREEN = (0, 180, 0)

FONT = pygame.font.SysFont(None, 32)
SMALL_FONT = pygame.font.SysFont(None, 22)

screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Onitama")
clock = pygame.time.Clock()

# ----------------------
# Movement Cards
# ----------------------
CARDS = {
    "Tiger": [(0, -2), (0, 1)],
    "Dragon": [(-2, -1), (2, -1), (-1, 1), (1, 1)],
    "Frog": [(-2, 0), (-1, -1), (1, 1)],
    "Rabbit": [(2, 0), (1, -1), (-1, 1)],
    "Crab": [(-2, 0), (0, -1), (2, 0)],
    "Elephant": [(-1, 0), (-1, -1), (1, 0), (1, -1)],
    "Goose": [(-1, 0), (-1, -1), (1, 0), (1, 1)],
    "Rooster": [(1, 0), (1, -1), (-1, 0), (-1, 1)],
    "Monkey": [(-1, -1), (-1, 1), (1, -1), (1, 1)],
    "Mantis": [(-1, -1), (0, 1), (1, -1)]
}

# ----------------------
# Piece Class
# ----------------------
class Piece:
    def __init__(self, x, y, color, master=False):
        self.x = x
        self.y = y
        self.color = color
        self.master = master

    def draw(self):
        cx = BOARD_X + self.x * CELL_SIZE + CELL_SIZE // 2
        cy = BOARD_Y + self.y * CELL_SIZE + CELL_SIZE // 2
        radius = 26 if self.master else 22
        pygame.draw.circle(screen, self.color, (cx, cy), radius)
        if self.master:
            pygame.draw.circle(screen, YELLOW, (cx, cy), radius, 3)

# ----------------------
# Board Setup
# ----------------------
board = [[None for _ in range(BOARD_SIZE)] for _ in range(BOARD_SIZE)]

for i in range(5):
    board[i][0] = Piece(i, 0, BLUE, master=(i == 2))
    board[i][4] = Piece(i, 4, RED, master=(i == 2))

cards = random.sample(list(CARDS.keys()), 5)
blue_cards = [cards[0], cards[1]]
red_cards = [cards[2], cards[3]]
side_card = cards[4]

current_player = BLUE
selected_piece = None
selected_card = None
valid_moves = []
winner = None

# ----------------------
# Helper Functions
# ----------------------
def draw_board():
    for x in range(BOARD_SIZE):
        for y in range(BOARD_SIZE):
            rect = pygame.Rect(
                BOARD_X + x * CELL_SIZE,
                BOARD_Y + y * CELL_SIZE,
                CELL_SIZE,
                CELL_SIZE,
            )
            pygame.draw.rect(screen, GRAY, rect, 1)


def draw_card_box(card, x, y, selected=False):
    rect = pygame.Rect(x, y, 120, 50)
    pygame.draw.rect(screen, YELLOW if selected else WHITE, rect)
    pygame.draw.rect(screen, BLACK, rect, 2)
    text = SMALL_FONT.render(card, True, BLACK)
    screen.blit(text, (x + 10, y + 16))


def draw_cards():
    screen.blit(FONT.render("Blue's Turn" if current_player == BLUE else "Red's Turn", True, BLACK), (20, 20))

    # Blue cards (top)
    for i, card in enumerate(blue_cards):
        draw_card_box(card, WIDTH // 2 - 140 + i * 140, 20, card == selected_card)

    # Red cards (bottom)
    for i, card in enumerate(red_cards):
        draw_card_box(card, WIDTH // 2 - 140 + i * 140, HEIGHT - 80, card == selected_card)

    # Side card (right)
    draw_card_box(side_card, WIDTH - 150, HEIGHT // 2 - 25)


def draw_card_moves(card):
    if not card:
        return

    # Position move display next to current player's cards
    if current_player == BLUE:
        cx = WIDTH // 2 + 160
        cy = 45
    else:
        cx = WIDTH // 2 + 160
        cy = HEIGHT - 55

    pygame.draw.circle(screen, BLACK, (cx, cy), 6)

    for dx, dy in CARDS[card]:
        dy = dy if current_player == BLUE else -dy
        px = cx + dx * 18
        py = cy + dy * 18
        pygame.draw.circle(screen, GREEN, (px, py), 6)
        pygame.draw.line(screen, GREEN, (cx, cy), (px, py), 2)


def get_valid_moves(piece, card_name):
    if card_name is None:
        return []

    moves = []
    for dx, dy in CARDS[card_name]:
        if piece.color == RED:
            dy = -dy
        nx, ny = piece.x + dx, piece.y + dy
        if 0 <= nx < BOARD_SIZE and 0 <= ny < BOARD_SIZE:
            target = board[nx][ny]
            if target is None or target.color != piece.color:
                moves.append((nx, ny))
    return moves



def switch_turn(used_card):
    global current_player, side_card
    if current_player == BLUE:
        blue_cards.remove(used_card)
        blue_cards.append(side_card)
    else:
        red_cards.remove(used_card)
        red_cards.append(side_card)
    side_card = used_card
    current_player = RED if current_player == BLUE else BLUE

# ----------------------
# Main Loop
# ----------------------
while True:
    clock.tick(FPS)
    screen.fill(WHITE)

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
            sys.exit()

        if event.type == pygame.MOUSEBUTTONDOWN and not winner:
            mx, my = pygame.mouse.get_pos()

            # Card selection
            for i, card in enumerate(blue_cards if current_player == BLUE else red_cards):
                y = 20 if current_player == BLUE else HEIGHT - 80
                rect = pygame.Rect(WIDTH // 2 - 140 + i * 140, y, 120, 50)
                if rect.collidepoint(mx, my):
                    selected_card = card
                    selected_piece = None
                    valid_moves = []

            # Board interaction
            if BOARD_X <= mx <= BOARD_X + BOARD_PIXEL_SIZE and BOARD_Y <= my <= BOARD_Y + BOARD_PIXEL_SIZE:
                x = (mx - BOARD_X) // CELL_SIZE
                y = (my - BOARD_Y) // CELL_SIZE
                if selected_card:
                    piece = board[x][y]

                # Click on one of your own pieces → select / reselect
                if piece and piece.color == current_player:
                    selected_piece = piece
                    valid_moves = get_valid_moves(piece, selected_card)

                # Click on a valid move square → move piece
                elif selected_piece and (x, y) in valid_moves:
                    target = board[x][y]
                    if target and target.master:
                        winner = current_player

                    board[selected_piece.x][selected_piece.y] = None
                    selected_piece.x, selected_piece.y = x, y
                    board[x][y] = selected_piece

                    # Temple win
                    if selected_piece.master:
                        if selected_piece.color == BLUE and (x, y) == (2, 4):
                            winner = BLUE
                        if selected_piece.color == RED and (x, y) == (2, 0):
                            winner = RED

                    switch_turn(selected_card)
                    selected_piece = None
                    selected_card = None
                    valid_moves = []


    draw_board()

    for row in board:
        for piece in row:
            if piece:
                piece.draw()

    for mx, my in valid_moves:
        cx = BOARD_X + mx * CELL_SIZE + CELL_SIZE // 2
        cy = BOARD_Y + my * CELL_SIZE + CELL_SIZE // 2
        pygame.draw.circle(screen, GREEN, (cx, cy), 7)

    draw_cards()
    draw_card_moves(selected_card)

    if winner:
        text = FONT.render("Blue Wins!" if winner == BLUE else "Red Wins!", True, BLACK)
        screen.blit(text, (WIDTH // 2 - 80, HEIGHT // 2))

    pygame.display.flip()





#CARDS = {
    "Tiger": [(0, 2), (0, -1)],
    "Dragon": [(-2, 1), (2, 1), (-1, -1), (1, -1)],
    "Frog": [(-2, 0), (-1, 1), (1, -1)],
    "Rabbit": [(2, 0), (1, 1), (-1, -1)],
    "Crab": [(0, 2), (-2, 0), (2, 0)],
    "Elephant": [(-1, 0), (1, 0), (1, 1), (-1, 1)],
    "Goose": [(-1, 0), (-1, 1), (1, 0), (1, -1)],
    "Rooster": [(1, 0), (1, 1), (-1, 0), (-1, -1)],
    "Monkey": [(-1, -1), (-1, 1), (1, -1), (1, 1)],
    "Mantis": [(-1, 1), (0, -1), (1, 1)],
    "Horse" : [(0, 1), (-1, 0), (0, -1)],
    "OX" : [(0, 1), (1, 0), (0, -1)],
    "Crane" : [(0, 1), (-1, -1), (1, -1)],
    "Boar" : [(-1, 0), (0, 1), (1, 0)],
    "Eel" : [(1, 0), (-1, 1), (-1, -1)],
    "Cobra" : [(-1, 0), (1, 1), (1, -1)]
#}