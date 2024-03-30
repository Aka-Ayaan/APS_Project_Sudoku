import pygame
import sys
import random

# Initialize Pygame
pygame.init()

# Initializing constants for the game
WIDTH, HEIGHT = 600, 650
GRID_SIZE = 9
CELL_SIZE = WIDTH // GRID_SIZE
WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
RED = (255, 0, 0)
LIGHT_RED = (255, 150, 150)
GREEN = (0, 255, 0)
DARK_GREEN = (0, 100, 0)
LIGHT_GREEN = (150, 255, 150)
BLUE = (0 ,0, 255)
LIGHT_BLUE = (150, 150, 255)
FONT_SIZE = 40
SELECTED_COLOR = (200, 200, 255)
BUTTON_COLOR = (150, 150, 150)
BUTTON_TEXT_COLOR = BLACK


# Setting up dimensions, title, and variable
screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Sudoku")
font = pygame.font.Font(None, FONT_SIZE)
selected_cell = None
input_numbers = [[0] * GRID_SIZE for _ in range(GRID_SIZE)]     # Stores only the correct values entered
tempStore = {}   # Stores all values with tuple(coordinates) keys
puzzle = None

# Function to select puzzle based on difficulty
def select_puzzle(difficulty):
    global puzzle
    
    # Sudoku puzzle (0 represents empty cell) in a 2D list
    if difficulty == 1:
        puzzle = [
            [5, 3, 0, 0, 7, 0, 0, 0, 0],
            [6, 0, 0, 1, 9, 5, 0, 0, 0],
            [0, 9, 8, 0, 0, 0, 0, 6, 0],
            [8, 0, 0, 0, 6, 0, 0, 0, 3],
            [4, 0, 0, 8, 0, 3, 0, 0, 1],
            [7, 0, 0, 0, 2, 0, 0, 0, 6],
            [0, 6, 0, 0, 0, 0, 2, 8, 0],
            [0, 0, 0, 4, 1, 9, 0, 0, 5],
            [0, 0, 0, 0, 8, 0, 0, 7, 9]
        ]
    elif difficulty == 2:
        puzzle = [
            [7, 0, 0, 0, 0, 8, 0 ,0 ,1],
            [9, 0, 0, 0, 3, 0, 7, 0, 5],
            [5, 0, 0, 0, 0, 2, 0, 0, 0],
            [1, 0, 0, 9, 0, 0, 0, 0, 4],
            [0, 0, 0, 0, 0, 0, 0, 0, 0],
            [0, 8, 4, 0, 0, 3, 0, 0, 7],
            [0, 6, 0, 0, 0, 4, 0, 0, 3],
            [0, 1, 0, 0, 2, 0, 0, 4, 0],
            [4, 0, 0, 0, 0, 0, 2, 5, 0]
        ]
    else:
        puzzle = [
            [0, 2, 9, 0, 0, 0, 4, 0, 0],
            [0, 0, 0, 5, 0, 0, 1, 0, 0],
            [0, 4, 0, 0, 0, 0, 0, 0, 0],
            [0, 0, 0, 0, 4, 2, 0, 0, 0],
            [6, 0, 0, 0, 0, 0, 0, 7, 0],
            [5, 0, 0, 0, 0, 0, 0, 0, 0],
            [7, 0, 0, 3, 0, 0, 0, 0, 5],
            [0, 1, 0, 0, 9, 0, 0, 0, 0],
            [0, 0, 0, 0, 0, 0, 0, 6, 0]
        ]

# Function to randomize the puzzle
def randomize_puzzle():
    for _ in range(20):
        # Swap rows within each 3x3 block
        row_block = random.randint(0, 2) * 3
        row1, row2 = random.sample(range(row_block, row_block + 3), 2)
        puzzle[row1], puzzle[row2] = puzzle[row2], puzzle[row1]

        # Swap columns within each 3x3 block
        col_block = random.randint(0, 2) * 3
        col1, col2 = random.sample(range(col_block, col_block + 3), 2)
        for row in puzzle:
            row[col1], row[col2] = row[col2], row[col1]

# Checks if the number is valid in the sudoku or not. 
def is_valid(row,col,num):
    global puzzle, input_numbers
    
    # The use of col != i, row != j is to make sure that the valid function doesn't check on the same coordinates
    # Checks if the number repeats in the row of puzzle or input_numbers
    for i in range(9):
        if num == puzzle[row][i] or num == input_numbers[row][i] and col != i:
            return False
    
    #Cheks if the number repeats in the column of puzzle or input_numbers
    for j in range(9):
        if num == puzzle[j][col] or num == input_numbers[j][col] and row != j:
            return False
    
    #Checks if the number repeats in that specific box in either puzzle or input_numbers
    for l in range(row // 3 * 3, row // 3 * 3 + 3):
        for m in range(col // 3 * 3, col // 3 * 3 + 3):
            if num == puzzle[l][m] or num == input_numbers[l][m] and (row != l or col!= m):
                return False
    return True

# Function to draw the Sudoku grid
def draw_grid():
    for i in range(GRID_SIZE + 1):
        if i % 3 == 0:
            pygame.draw.line(screen, BLACK, (0, i * CELL_SIZE), (WIDTH, i * CELL_SIZE), 4)
            pygame.draw.line(screen, BLACK, (i * CELL_SIZE, 0), (i * CELL_SIZE, HEIGHT - 50), 4)
        else:
            pygame.draw.line(screen, BLACK, (0, i * CELL_SIZE), (WIDTH, i * CELL_SIZE), 2)
            pygame.draw.line(screen, BLACK, (i * CELL_SIZE, 0), (i * CELL_SIZE, HEIGHT - 50), 2)

# Function to draw the Sudoku numbers
def draw_numbers():
    global tempStore
    for i in range(GRID_SIZE):
        for j in range(GRID_SIZE):
            x = j * CELL_SIZE + CELL_SIZE // 2 - FONT_SIZE // 4
            y = i * CELL_SIZE + CELL_SIZE // 2 - FONT_SIZE // 2

            # Highlight selected cell
            if selected_cell == (i, j):
                pygame.draw.rect(screen, WHITE, (j * CELL_SIZE, i * CELL_SIZE, CELL_SIZE, CELL_SIZE))

            # Draw puzzle number
            if puzzle[i][j] != 0:
                number = font.render(str(puzzle[i][j]), True, BLACK)
                screen.blit(number, (x, y))

            # Draw input number
            elif (i,j) in tempStore:
                
                # If the number is valid then output it with green color
                if is_valid(i,j,tempStore[(i,j)]):
                    input_number = font.render(str(tempStore[(i,j)]), True, DARK_GREEN)
                    screen.blit(input_number, (x, y))
               
                # If the number isn't valid then output it with red color
                elif not is_valid(i,j,tempStore[(i,j)]):
                    input_number = font.render(str(tempStore[(i,j)]), True, RED)
                    screen.blit(input_number, (x, y))
                

# Function to update the input numbers based on user interaction
def update_input_numbers(event):
    global selected_cell
    
    # If the user uses mouse/touchpad to interact with the game
    if event.type == pygame.MOUSEBUTTONDOWN:
        x, y = event.pos
        row = y // CELL_SIZE
        col = x // CELL_SIZE
        selected_cell = (row, col)

        # Check if the "Quit" button is clicked
        if WIDTH - 300 <= x <= WIDTH - 200 and HEIGHT - 50 <= y <= HEIGHT:
            pygame.quit()
            sys.exit()

        # Check if the "Play Again" button is clicked
        elif WIDTH - 200 <= x <= WIDTH and HEIGHT - 50 <= y <= HEIGHT:
            reset_game()
   
    # If the user presses a key
    elif event.type == pygame.KEYDOWN:
       
        # Checks if number is between 1 and 9 numbers and saves the value to number
        if pygame.K_1 <= event.key <= pygame.K_9:
            number = event.key - pygame.K_0

            # Check if the move is valid before updating the input_numbers
            if selected_cell is not None and is_valid(selected_cell[0],selected_cell[1],number):
                tempStore[selected_cell] = number
                input_numbers[selected_cell[0]][selected_cell[1]] = number
            elif selected_cell is not None and is_valid(selected_cell[0],selected_cell[1],number) == False:
                tempStore[selected_cell] = number

        elif event.key == pygame.K_BACKSPACE or event.key == pygame.K_DELETE:
            # Delete the input number in the selected cell (if not in the original puzzle)
            if selected_cell is not None and puzzle[selected_cell[0]][selected_cell[1]] == 0:
                input_numbers[selected_cell[0]][selected_cell[1]] = 0
                del tempStore[selected_cell]

        elif event.key == pygame.K_LEFT:
            # Move the selection to the left
            if selected_cell is not None and selected_cell[1] > 0:
                selected_cell = (selected_cell[0], selected_cell[1] - 1)

        elif event.key == pygame.K_RIGHT:
            # Move the selection to the right
            if selected_cell is not None and selected_cell[1] < GRID_SIZE - 1:
                selected_cell = (selected_cell[0], selected_cell[1] + 1)

        elif event.key == pygame.K_UP:
            # Move the selection upward
            if selected_cell is not None and selected_cell[0] > 0:
                selected_cell = (selected_cell[0] - 1, selected_cell[1])

        elif event.key == pygame.K_DOWN:
            # Move the selection downward
            if selected_cell is not None and selected_cell[0] < GRID_SIZE - 1:
                selected_cell = (selected_cell[0] + 1, selected_cell[1])

# Function to check if the puzzle is completed
def is_puzzle_completed():
    for i in range(GRID_SIZE):
        for j in range(GRID_SIZE):
            
            # If the given number is already in puzzle then no need to check it
            if puzzle[i][j] != 0:
                continue
            
            # If the given number is not in input_numbers while the specific index is 0 in puzzle then return False
            elif puzzle[i][j] == 0 and input_numbers[i][j] == 0:
                return False
    
    # If no case return false then return true
    return True

# Function to reset the game
def reset_game():
    global puzzle, selected_cell, input_numbers, difficulty, tempStore, fill_color
    difficulty = start_screen()
    select_puzzle(difficulty)
    randomize_puzzle()

    # Set background color based on the difficulty
    if difficulty == 1:
        fill_color = LIGHT_GREEN
    elif difficulty == 2:
        fill_color = LIGHT_BLUE
    else:
        fill_color = LIGHT_RED

    selected_cell = None
    input_numbers = [[0] * GRID_SIZE for _ in range(GRID_SIZE)]
    tempStore = {}

def start_screen():
    global GREEN, BLUE, RED, WHITE, BLACK, WIDTH, HEIGHT, FONT_SIZE, screen, font, difficulty, Title_font
    
    # Font declaration
    font_path = "Beyonders.otf"   # Path to the font file (if already in the same directory, just the name of the font file)
    font_size = 60
    Title_font = pygame.font.Font(font_path, font_size)
    background = pygame.image.load("Background1.jpg")   # Path to the background image (if already in the same directory, just the name of the image file)
    running = True

    # Define the positions and sizes of the difficulty buttons
    easy_button = pygame.Rect(WIDTH // 4 - 150 // 2, 210, 150, 50)
    medium_button = pygame.Rect(WIDTH // 2 - 150 // 2, 210, 150, 50)
    hard_button = pygame.Rect(3 * WIDTH // 4 - 150 // 2, 210, 150, 50)

    while running:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            elif event.type == pygame.MOUSEBUTTONDOWN:
                
                # Get the mouse position
                mouse_pos = pygame.mouse.get_pos()

                # Check if the mouse position is within the bounds of any of the difficulty buttons
                if easy_button.collidepoint(mouse_pos):
                    difficulty = 1
                elif medium_button.collidepoint(mouse_pos):
                    difficulty = 2
                elif hard_button.collidepoint(mouse_pos):
                    difficulty = 3
                
                # Start the game with the selected difficulty
                return difficulty

        # Set the background image
        screen.blit(background, (-120, 0))

        # Display title
        title_text = Title_font.render("Sudoku", True, WHITE)
        screen.blit(title_text, (WIDTH // 2 - title_text.get_width() // 2, 50))

        # Display instructions
        instruction_text = font.render("Select difficulty:", True, WHITE)
        screen.blit(instruction_text, (WIDTH // 2 - instruction_text.get_width() // 2, 175))

        # Display difficulty buttons
        pygame.draw.rect(screen, GREEN, easy_button)
        pygame.draw.rect(screen, BLUE, medium_button)
        pygame.draw.rect(screen, RED, hard_button)

        easy_text = font.render("Easy", True, BUTTON_TEXT_COLOR)
        medium_text = font.render("Medium", True, BUTTON_TEXT_COLOR)
        hard_text = font.render("Hard", True, BUTTON_TEXT_COLOR)

        screen.blit(easy_text, (WIDTH // 4 - easy_text.get_width() // 2, 225))
        screen.blit(medium_text, (WIDTH // 2 - medium_text.get_width() // 2, 225))
        screen.blit(hard_text, (3 * WIDTH // 4 - hard_text.get_width() // 2, 225))

        pygame.display.flip()

def main():
    
    # Creating the start screen and getting difficulty
    difficulty = start_screen()

    # Select the puzzle based on the difficulty
    select_puzzle(difficulty)

    # Load font
    font = pygame.font.Font(None, FONT_SIZE)

    # Initialize the game
    randomize_puzzle()

    # Set background color based on the difficulty
    global fill_color
    if difficulty == 1:
        fill_color = LIGHT_GREEN
    elif difficulty == 2:
        fill_color = LIGHT_BLUE
    else:
        fill_color = LIGHT_RED

    # Main game loop
    running = True

    while running:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
            update_input_numbers(event)      

        # Fill the background with white
        screen.fill(fill_color)

        # Draw Sudoku grid and numbers
        draw_grid()
        draw_numbers()

        # Draw Quit and Play Again buttons
        pygame.draw.rect(screen, BUTTON_COLOR, (WIDTH - 300, HEIGHT - 50, 100, 50))
        pygame.draw.rect(screen, BUTTON_COLOR, (WIDTH - 200, HEIGHT - 50, 200, 50))
        quit_button_text = font.render("Quit    |", True, BUTTON_TEXT_COLOR)
        play_again_button_text = font.render("Play Again", True, BUTTON_TEXT_COLOR)
        screen.blit(quit_button_text, (WIDTH - 275, HEIGHT - 40))
        screen.blit(play_again_button_text, (WIDTH - 150, HEIGHT - 40))    

         # Check if the puzzle is completed
        if is_puzzle_completed():
            screen.fill(WHITE)
            win_message = font.render("You Win!.", True, "red")
            textRect = win_message.get_rect()
            textRect.center = (WIDTH // 2, HEIGHT // 2 - 35)
            screen.blit(win_message, textRect)
            
            # Drawing the buttons again on the win screen
            pygame.draw.rect(screen, BUTTON_COLOR, (WIDTH - 300, HEIGHT - 50, 100, 50))
            pygame.draw.rect(screen, BUTTON_COLOR, (WIDTH - 200, HEIGHT - 50, 200, 50))
            quit_button_text = font.render("Quit    |", True, BUTTON_TEXT_COLOR)
            play_again_button_text = font.render("Play Again", True, BUTTON_TEXT_COLOR)
            screen.blit(quit_button_text, (WIDTH - 275, HEIGHT - 40))
            screen.blit(play_again_button_text, (WIDTH - 150, HEIGHT - 40))

        # Update the display
        pygame.display.flip()

    # Quit Pygame
    pygame.quit()
    sys.exit()

# Calling the main function by running the script directly
if __name__ == "__main__":
    main()