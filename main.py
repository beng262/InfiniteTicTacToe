import pygame
import sys
import random

# Init
pygame.init()

# Constants
SCREEN_SIZE = 600
GRID_SIZE = 3
CELL_SIZE = SCREEN_SIZE // GRID_SIZE
LINE_WIDTH = 15
CROSS_WIDTH = 25
SPACE = 55
NEW_GAME_BUTTON_HEIGHT = 50
ANIMATION_DURATION = 120  # 2 seconds at 60 FPS

# Colors
BG_COLOR = (28, 170, 156)
LINE_COLOR = (23, 145, 135)
CROSS_COLOR = (162, 207, 254)  # Light blue color #A2CFFE
BUTTON_COLOR = (173, 216, 230)  # Baby blue color
BUTTON_TEXT_COLOR = (255, 255, 255)
GREEN = (140, 255, 158)  # Light green color #8CFF9E

# Function to create an empty green circle surface
def create_circle_surface(radius, color, width):
    # Create a surface with transparent background
    surface = pygame.Surface((radius * 2, radius * 2), pygame.SRCALPHA)
    # Draw an empty circle (outline) on the surface
    pygame.draw.circle(surface, color, (radius, radius), radius, width)
    return surface

# Create the empty green circle surface
circle_img = create_circle_surface(CELL_SIZE // 2 - 14 - SPACE // 4, GREEN, 15)

# Screen setup
screen = pygame.display.set_mode((SCREEN_SIZE, SCREEN_SIZE + NEW_GAME_BUTTON_HEIGHT))
pygame.display.set_caption('Infinite Tic Tac Toe')
screen.fill(BG_COLOR)

# Board
board = [['' for _ in range(GRID_SIZE)] for _ in range(GRID_SIZE)]

# Players
player = 'X'
player_positions = {'X': [], 'O': []}

# Draw grid lines
def draw_grid():
    for x in range(1, GRID_SIZE):
        pygame.draw.line(screen, LINE_COLOR, (0, x * CELL_SIZE), (SCREEN_SIZE, x * CELL_SIZE), LINE_WIDTH)
        pygame.draw.line(screen, LINE_COLOR, (x * CELL_SIZE, 0), (x * CELL_SIZE, SCREEN_SIZE), LINE_WIDTH)

# Draw X
def draw_x(row, col):
    start_desc = (col * CELL_SIZE + SPACE, row * CELL_SIZE + SPACE)
    end_desc = (col * CELL_SIZE + CELL_SIZE - SPACE, row * CELL_SIZE + CELL_SIZE - SPACE)
    pygame.draw.line(screen, CROSS_COLOR, start_desc, end_desc, CROSS_WIDTH)
    start_asc = (col * CELL_SIZE + SPACE, row * CELL_SIZE + CELL_SIZE - SPACE)
    end_asc = (col * CELL_SIZE + CELL_SIZE - SPACE, row * CELL_SIZE + SPACE)
    pygame.draw.line(screen, CROSS_COLOR, start_asc, end_asc, CROSS_WIDTH)

# Draw O 
def draw_o(row, col):
    screen.blit(circle_img, (col * CELL_SIZE + (CELL_SIZE - circle_img.get_width()) // 2, row * CELL_SIZE + (CELL_SIZE - circle_img.get_height()) // 2))

# Check if cell is empty
def is_cell_empty(row, col):
    return board[row][col] == ''

# Make move
def make_move(row, col, player):
    if is_cell_empty(row, col):
        board[row][col] = player
        player_positions[player].append((row, col))
        if player == 'X':
            draw_x(row, col)
        else:
            draw_o(row, col)
        return True
    return False

# Check for winner
def check_winner(player):
    # Check rows
    for row in board:
        if row.count(player) == GRID_SIZE:
            return True
    # Check columns
    for col in range(GRID_SIZE):
        if all(board[row][col] == player for row in range(GRID_SIZE)):
            return True
    # Check diagonals
    if all(board[i][i] == player for i in range(GRID_SIZE)) or all(board[i][GRID_SIZE - 1 - i] == player for i in range(GRID_SIZE)):
        return True
    return False

# Draw new game button
def draw_new_game_button():
    button_rect = pygame.Rect(0, SCREEN_SIZE, SCREEN_SIZE, NEW_GAME_BUTTON_HEIGHT)
    pygame.draw.rect(screen, BUTTON_COLOR, button_rect)
    font = pygame.font.Font(pygame.font.match_font('arial', bold=True), 36)
    text = font.render('New Game', True, BUTTON_TEXT_COLOR)
    text_rect = text.get_rect(center=button_rect.center)
    screen.blit(text, text_rect)

# Reset game
def reset_game():
    global board, player, player_positions
    board = [['' for _ in range(GRID_SIZE)] for _ in range(GRID_SIZE)]
    player_positions = {'X': [], 'O': []}
    player = 'X'
    screen.fill(BG_COLOR)
    draw_grid()
    draw_new_game_button()

# Animate winner with falling Xs or Os like rain
def animate_winner(player):
    for frame in range(ANIMATION_DURATION):  # 2 seconds at 60 FPS
        screen.fill(BG_COLOR)
        draw_grid()
        draw_new_game_button()

        for _ in range(15):  # Drop 15 Xs or Os per frame
            x = random.randint(0, SCREEN_SIZE)
            y = random.randint(-CELL_SIZE, SCREEN_SIZE)
            if player == 'X':
                draw_x(y // CELL_SIZE, x // CELL_SIZE)
            else:
                screen.blit(circle_img, (x - CELL_SIZE // 2, y))  # Draw O at falling position

        pygame.display.update()
        pygame.time.delay(16)  # Delay for ~60 FPS

# Main loop
def main():
    global player
    draw_grid()
    draw_new_game_button()
    running = True
    winner = None

    while running:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
                pygame.quit()
                sys.exit()

            if event.type == pygame.MOUSEBUTTONDOWN:
                mouseX = event.pos[0]
                mouseY = event.pos[1]

                if mouseY >= SCREEN_SIZE:
                    reset_game()
                else:
                    clicked_row = mouseY // CELL_SIZE
                    clicked_col = mouseX // CELL_SIZE

                    if make_move(clicked_row, clicked_col, player):
                        if check_winner(player):
                            winner = player
                            animate_winner(player)
                            reset_game()
                        else:
                            if len(player_positions[player]) > 3:
                                oldest_move = player_positions[player].pop(0)
                                board[oldest_move[0]][oldest_move[1]] = ''
                                screen.fill(BG_COLOR)
                                draw_grid()
                                draw_new_game_button()
                                for pos in player_positions['X']:
                                    draw_x(pos[0], pos[1])
                                for pos in player_positions['O']:
                                    draw_o(pos[0], pos[1])
                            player = 'O' if player == 'X' else 'X'

        pygame.display.update()

if __name__ == '__main__':
    main()
