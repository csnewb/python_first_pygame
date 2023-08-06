from save_mgmt import update_high_scores, print_high_scores, load_high_scores

import sys
import pygame
import random
import time
import math
import os

SCREEN_HEIGHT = 1200
SCREEN_WIDTH = 1800
PLAY_H_BOUNDARY = 150
PLAY_W_BOUNDARY = 50
PLAY_W_MIN = 0 + (PLAY_W_BOUNDARY // 2)
PLAY_W_MAX = SCREEN_WIDTH - (PLAY_W_BOUNDARY // 2)
PLAY_H_MIN = 0 + (PLAY_H_BOUNDARY // 2)
PLAY_H_MAX = SCREEN_HEIGHT - (PLAY_H_BOUNDARY // 2)
play_area_rect = pygame.Rect(PLAY_W_MIN, PLAY_H_MIN, PLAY_W_MAX - PLAY_W_MIN, PLAY_H_MAX - PLAY_H_MIN)



# Define movement speed
movement_speed = 2

DIFFICULTY = 5

OPTION_KEY_CONTROL = True
OPTION_MOUSE_CONTROL = False

collision_detected = False
toggle_menu = False



PLAYER_NAME = ""
SCORE = 0
CLOCK = 0
LEVEL = 1
MAX_SCORE = 0
elapsed_time_seconds = 0
SHIELDS = 0
SHIELDS_ON = False
GAME_OVER = False
DEATH_TIMER_ENABLED = False
GAME_OVER_ENABLED = False
FLASH_SHIELDS = False
FLASH_SHIELDS_TIMER = 0
DIFFICULTY_LEVEL = 1
NUM_BOUNCE_OBSTACLES = 1


def display_difficulty_level(text, font_size=40, color=(255, 255, 255)):
    font = pygame.font.Font(None, font_size)
    text_surface = font.render(text, True, color)
    text_rect = text_surface.get_rect()
    text_rect.center = ((SCREEN_WIDTH // 6) * 1, 20)
    screen.blit(text_surface, text_rect)

def display_level(text, font_size=40, color=(255, 255, 255)):
    font = pygame.font.Font(None, font_size)
    text_surface = font.render(text, True, color)
    text_rect = text_surface.get_rect()
    text_rect.center = ((SCREEN_WIDTH // 6) * 2, 20)
    screen.blit(text_surface, text_rect)

def display_score(text, font_size=40, color=(255, 255, 255)):
    font = pygame.font.Font(None, font_size)
    text_surface = font.render(text, True, color)
    text_rect = text_surface.get_rect()
    text_rect.center = ((SCREEN_WIDTH // 6) * 3, 20)
    screen.blit(text_surface, text_rect)

def display_max_score(text, font_size=40, color=(255, 255, 255)):
    font = pygame.font.Font(None, font_size)
    text_surface = font.render(text, True, color)
    text_rect = text_surface.get_rect()
    text_rect.center = ((SCREEN_WIDTH // 6) * 4, 20)
    screen.blit(text_surface, text_rect)

def display_shields(text, font_size=40, color=(255, 255, 255)):
    font = pygame.font.Font(None, font_size)
    text_surface = font.render(text, True, color)
    text_rect = text_surface.get_rect()
    text_rect.center = ((SCREEN_WIDTH // 6) * 5, 20)
    screen.blit(text_surface, text_rect)

def display_shields_earned(text, font_size=20, color=(200, 50, 50)):
    font = pygame.font.Font(None, font_size)
    text_surface = font.render(text, True, color)
    text_rect = text_surface.get_rect()
    text_rect.center = ((SCREEN_WIDTH // 2) * 5, 40)
    screen.blit(text_surface, text_rect)






def display_game_over(text, font_size=40, color=(200, 50, 50)):
    font = pygame.font.Font(None, font_size)
    text_surface = font.render(text, True, color)
    text_rect = text_surface.get_rect()
    text_rect.center = (SCREEN_WIDTH // 2, SCREEN_HEIGHT - 20)
    screen.blit(text_surface, text_rect)



def display_text(text, font_size=24, color=(255, 255, 255)):
    font = pygame.font.Font(None, font_size)
    text_surface = font.render(text, True, color)
    text_rect = text_surface.get_rect()
    text_rect.center = (SCREEN_WIDTH // 2, SCREEN_HEIGHT - 20)
    screen.blit(text_surface, text_rect)


class BounceObstacle:
    def __init__(self, x, y, width, height, speed=1):
        self.rect = pygame.Rect(x, y, width, height)
        self.speed = speed
        angle = random.uniform(0, 2 * math.pi)  # Random angle in radians
        self.direction = [math.cos(angle), math.sin(angle)]  # Convert angle to x and y components

    def move(self, play_area_rect):
        # Move the obstacle
        self.rect.x += self.speed * self.direction[0]
        self.rect.y += self.speed * self.direction[1]

        # Check for collision with play area and reverse direction if needed
        if self.rect.left < play_area_rect.left or self.rect.right > play_area_rect.right:
            self.direction[0] *= -1
        if self.rect.top < play_area_rect.top or self.rect.bottom > play_area_rect.bottom:
            self.direction[1] *= -1

        # Clamp the obstacle within the play area
        self.rect.clamp_ip(play_area_rect)

    def draw(self, screen):
        pygame.draw.rect(screen, DARK_GREEN, self.rect)


def initialize_game():
    global screen
    global player
    global food
    global menu_bar
    global obstacles
    global bounce_obstacles

    screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
    pygame.display.set_caption("First Pygame")


    ######### SPRITES ###############
    player = pygame.Rect((SCREEN_WIDTH // 2 - 25, SCREEN_HEIGHT // 2 - 25, 50, 50))
    food = pygame.Rect(random.randint(PLAY_W_MIN, PLAY_W_MAX) - 25, random.randint(PLAY_H_MIN, PLAY_H_MAX) - 25, 25, 25)
    menu_bar = pygame.Rect(0, PLAY_H_MAX, SCREEN_WIDTH, SCREEN_HEIGHT - PLAY_H_MAX)


    ######### INSTANTIATE SPRITES ######
    obstacles = []
    for _ in range(DIFFICULTY):
        instantiate_obstacle()

    bounce_obstacles = []
    for _ in range(NUM_BOUNCE_OBSTACLES):
        instantiate_bounce_obstacle(30, 30)

def instantiate_obstacle():
    global obstacles
    obstacle_rect = pygame.Rect(random.randint(PLAY_W_MIN, PLAY_W_MAX) - 25, random.randint(PLAY_H_MIN, PLAY_H_MAX) - 25, 25, 25)
    obstacles.append(obstacle_rect)

def instantiate_bounce_obstacle(height, width):
    global bounce_obstacles
    # Create the bouncing obstacle
    bounce_obstacle = BounceObstacle(random.randint(PLAY_W_MIN, PLAY_W_MAX) - width, random.randint(PLAY_H_MIN, PLAY_H_MAX) - height, height, width)  # You can customize the initial position and size
    bounce_obstacles.append(bounce_obstacle)

############ COLORS ##############
BG = (50, 50, 50)
BLACK = (0, 0, 0)
RED = (255, 0, 0)
GREEN = (0, 255, 0)
DARK_GREEN = (125, 250, 125)
PURPLE = (125, 0, 125)
BLUE = (0, 0, 255)
YELLOW = (200, 200, 0)
ORANGE = (255, 165, 0)
player_color = BLUE
obstacle_color = BLACK
MENU_COLOR = (0, 0, 100)


def draw_elements(start_time):
    global player_color
    global obstacle_color
    global elapsed_time_seconds
    global SCORE
    global DEATH_TIMER_ENABLED
    global MAX_SCORE
    global bounce_obstacles

    # Calculate elapsed time in milliseconds
    elapsed_time_ms = pygame.time.get_ticks() - start_time

    # Update elapsed_time_seconds only if a whole second has passed
    if elapsed_time_ms // 1000 > elapsed_time_seconds:
        elapsed_time_seconds = elapsed_time_ms // 1000
        if DEATH_TIMER_ENABLED:
            SCORE -= (10 * DIFFICULTY_LEVEL)

    screen.fill(BG)
    ########### DRAW SPRITES #################
    border_color = pygame.Color('gray')
    pygame.draw.rect(screen, border_color, play_area_rect, 2)
    pygame.draw.rect(screen, player_color, player)
    pygame.draw.rect(screen, YELLOW, food)
    for obstacle in obstacles:
        pygame.draw.rect(screen, obstacle_color, obstacle)

    for bounce_obstacle in bounce_obstacles:
        bounce_obstacle.draw(screen)

    pygame.draw.rect(screen, MENU_COLOR, menu_bar)

    if not GAME_OVER:
        display_text(f"LEVEL: {LEVEL}  | SCORE: {SCORE}  | MAX SCORE: {MAX_SCORE}  | SHIELDS: {SHIELDS}  | TIME: {elapsed_time_seconds} seconds  | X: {player.x}  Y: {player.y}  | COLLISION: {collision_detected}  ")
    else:
        display_game_over(f"----- GAME OVER ------ LEVEL: {LEVEL}  | SCORE: {SCORE} | MAX SCORE: {MAX_SCORE}  ")

    display_level(f"LEVEL: {LEVEL}")
    display_score(f"SCORE: {SCORE}")
    display_max_score(f"MAX: {MAX_SCORE}")
    display_difficulty_level(f"DIFFICULTY: {DIFFICULTY_LEVEL}")
    display_shields(f"SHIELDS: {SHIELDS}")

    flag_timers()
    if FLASH_SHIELDS:
        display_shields_earned(f"Shields +1,000")
    return


def handle_player_input(events):
    global OPTION_MOUSE_CONTROL

    for event in events:
        # Check for key press and release events
        if event.type == pygame.KEYDOWN:
            down_key = pygame.key.get_pressed()
            key_name = pygame.key.name(event.key)
            print(f"down_key: {key_name}")

            ############ MENU CONTROL ##################
            if down_key[pygame.K_F1]:
                print("Mouse Control Toggled")
                if not OPTION_MOUSE_CONTROL:
                    OPTION_MOUSE_CONTROL = True
                else:
                    OPTION_MOUSE_CONTROL = False
    return


def handle_object_movement():
    global bounce_obstacles
    for bounce_obstacle in bounce_obstacles:
        bounce_obstacle.move(play_area_rect)


def handle_collisions():
    global SCORE
    global player_color
    global collision_detected
    global obstacle_color
    global LEVEL
    global SHIELDS
    global DEATH_TIMER_ENABLED
    global GAME_OVER_ENABLED
    global FLASH_SHIELDS

    ########## COLLISSIONS #################
    collision_detected = False

    if SHIELDS_ON:
        player_color = PURPLE
    else:
        player_color = BLUE
    obstacle_color = BLACK

    for obstacle in obstacles:
        if obstacle.colliderect(player):
            if SHIELDS_ON:
                obstacle_color = ORANGE
            else:
                obstacle_color = RED

        if player.colliderect(obstacle):
            player_color = RED
            collision_detected = True
            if SHIELDS_ON:
                SHIELDS -= 5 * DIFFICULTY_LEVEL
            else:
                SCORE -= 5 * DIFFICULTY_LEVEL
        else:
            collision_detected = False

        if food.colliderect(obstacle):
            food.centerx = random.randint(PLAY_W_MIN, PLAY_W_MAX)
            food.centery = random.randint(PLAY_H_MIN, PLAY_H_MAX)

    for obstacle in bounce_obstacles:
        if obstacle.rect.colliderect(player):
            if SHIELDS_ON:
                obstacle_color = ORANGE
            else:
                obstacle_color = RED

        if player.colliderect(obstacle.rect):
            player_color = RED
            collision_detected = True
            if SHIELDS_ON:
                SHIELDS -= 5 * DIFFICULTY_LEVEL
            else:
                SCORE -= 5 * DIFFICULTY_LEVEL
        else:
            collision_detected = False


    if player.colliderect(food):
        food.centerx = random.randint(PLAY_W_MIN, PLAY_W_MAX)
        food.centery = random.randint(PLAY_H_MIN, PLAY_H_MAX)
        SCORE += 150 * (1 + (DIFFICULTY_LEVEL / 3))
        LEVEL += 1
        DEATH_TIMER_ENABLED = True
        GAME_OVER_ENABLED = True
        if LEVEL % 5 == 0:
            SHIELDS += 1000 * (1 + (DIFFICULTY_LEVEL / 2))
            FLASH_SHIELDS = True


        instantiate_obstacle()
        update_game_state()




    return SCORE


def handle_exit(events):
    for event in events:
        if event.type == pygame.QUIT:
            pygame.quit()
            sys.exit()

def flag_timers():
    global FLASH_SHIELDS
    global FLASH_SHIELDS_TIMER

    # Check if FLASH_SHIELDS was just set to True
    if FLASH_SHIELDS and FLASH_SHIELDS_TIMER == 0:
        FLASH_SHIELDS_TIMER = pygame.time.get_ticks()

    # Check if 2 seconds have passed since FLASH_SHIELDS was set to True
    if FLASH_SHIELDS and pygame.time.get_ticks() - FLASH_SHIELDS_TIMER >= 2000:
        FLASH_SHIELDS = False
        FLASH_SHIELDS_TIMER = 0  # Reset the timer for future use




def player_control():
    ############ MOVEMENT ####################
    key = pygame.key.get_pressed()

    if OPTION_KEY_CONTROL:
        if key[pygame.K_LEFT] or key[pygame.K_a]:
            player.move_ip(-movement_speed, 0)
        elif key[pygame.K_RIGHT] or key[pygame.K_d]:
            player.move_ip(movement_speed, 0)
        elif key[pygame.K_UP] or key[pygame.K_w]:
            player.move_ip(0, -movement_speed)
        elif key[pygame.K_DOWN] or key[pygame.K_s]:
            player.move_ip(0, movement_speed)

    if OPTION_MOUSE_CONTROL:
        pos = pygame.mouse.get_pos()
        player.center = pos

    # Keep the player object within the boundaries
    player.clamp_ip(play_area_rect)
    return


def handle_game_logic():
    global SCORE
    global MAX_SCORE
    global SHIELDS
    global SHIELDS_ON
    global GAME_OVER
    global GAME_OVER_ENABLED
    global DEATH_TIMER_ENABLED

    if SCORE > MAX_SCORE:
        MAX_SCORE = SCORE

    if SHIELDS > 0:
        SHIELDS_ON = True
    if SHIELDS <= 0:
        SHIELDS = 0
        SHIELDS_ON = False


    if SCORE <= 0:
        if GAME_OVER_ENABLED:
            GAME_OVER = True

    if GAME_OVER:
        DEATH_TIMER_ENABLED = False

    return


def update_game_state():
    global DIFFICULTY_LEVEL
    height = 30
    width = 30

    if LEVEL % 25 == 0:
        DIFFICULTY_LEVEL += 1
        height += int(DIFFICULTY_LEVEL // 2) * 10
        width += int(DIFFICULTY_LEVEL // 2) * 10
        instantiate_bounce_obstacle(height, width)

def reset_game():
    global PLAYER_NAME, SCORE, CLOCK, LEVEL, MAX_SCORE, elapsed_time_seconds
    global SHIELDS, SHIELDS_ON, GAME_OVER, DEATH_TIMER_ENABLED, GAME_OVER_ENABLED
    global FLASH_SHIELDS, FLASH_SHIELDS_TIMER, DIFFICULTY_LEVEL
    global obstacles

    # PLAYER_NAME = ""            # Assuming the player will enter their name again
    SCORE = 0                   # Reset the score
    CLOCK = pygame.time.Clock() # Reinitialize the game clock
    LEVEL = 1                   # Reset the level
    MAX_SCORE = 0               # Reset the maximum score
    elapsed_time_seconds = 0    # Reset the elapsed time
    SHIELDS = 0                 # Reset the shields
    SHIELDS_ON = False          # Turn off the shields
    GAME_OVER = False           # Reset the game over flag
    DEATH_TIMER_ENABLED = False # Reset the death timer flag
    GAME_OVER_ENABLED = False   # Reset the game over enabled flag
    FLASH_SHIELDS = False       # Reset the flash shields flag
    FLASH_SHIELDS_TIMER = 0     # Reset the flash shields timer
    DIFFICULTY_LEVEL = 1        # Reset the difficulty level
    obstacles = []

def get_player_name():
    global PLAYER_NAME

    font = pygame.font.Font(None, 36)
    center_x = SCREEN_WIDTH // 2
    input_box = pygame.Rect(center_x - 90, 150, 140, 32)
    button_rect = pygame.Rect(center_x - 58, 200, 120, 32)
    color_inactive = pygame.Color('lightskyblue3')
    color_active = pygame.Color('dodgerblue2')
    color = color_active  # Start with the active color
    active = True        # Start with the input box active
    text = ''
    clock = pygame.time.Clock()

    text_color = (255, 255, 255)
    name_input_label = font.render("What is your name?", True, text_color)
    button_text = font.render("Submit", True, text_color)
    while True:
        events = pygame.event.get()
        for event in events:
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            if event.type == pygame.MOUSEBUTTONDOWN:
                if input_box.collidepoint(event.pos):
                    active = not active
                elif button_rect.collidepoint(event.pos):
                    PLAYER_NAME = text
                    return
                else:
                    active = False
                color = color_active if active else color_inactive

            if event.type == pygame.KEYDOWN:
                if active:
                    if event.key == pygame.K_RETURN:
                        PLAYER_NAME = text
                        return
                    elif event.key == pygame.K_BACKSPACE:
                        text = text[:-1]
                    else:
                        text += event.unicode

        txt_surface = font.render(text, True, color)
        width = max(200, txt_surface.get_width()+10)
        input_box.w = width
        screen.blit(name_input_label, (center_x - name_input_label.get_width() // 2, 100))
        screen.blit(txt_surface, (input_box.x+5, input_box.y+5))
        pygame.draw.rect(screen, color, input_box, 2)

        button_color = (0, 150, 255)
        border_color = (0, 0, 0)
        pygame.draw.rect(screen, button_color, button_rect)
        # screen.blit(button_text, (button_rect.x + 40 - button_text.get_width() // 2, button_rect.y + 5))
        screen.blit(button_text, (button_rect.x + 15, button_rect.y + 5))
        pygame.draw.rect(screen, border_color, button_rect, 2)

        pygame.display.flip()
        screen.fill((30, 30, 30))
        clock.tick(30)



def display_high_scores():
    scores_data = load_high_scores()
    scores_list = scores_data.get("scores", [])[:25]

    font = pygame.font.Font(None, 30)
    text_color = (255, 255, 255)

    button_rect = pygame.Rect(SCREEN_WIDTH // 2 - 150, SCREEN_HEIGHT - 130, 300, 50)
    button_color = (0, 150, 255)
    border_color = (0, 0, 0)

    high_scores_table_width = 560  # Adjust this value based on the actual width of your table
    table_start_x = (SCREEN_WIDTH - high_scores_table_width) // 2
    # table_start_y = (SCREEN_HEIGHT - 30 * len(scores_list)) // 2
    table_start_y = 60

    while True:
        screen.fill((30, 30, 30))
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            elif event.type == pygame.MOUSEBUTTONDOWN:
                if button_rect.collidepoint(event.pos):
                    return

        # Display high scores
        if not scores_list:
            no_scores_label = font.render("No high scores available.", True, text_color)
            screen.blit(no_scores_label, (table_start_x, table_start_y))
        else:
            title_label = font.render("High Scores:", True, text_color)
            screen.blit(title_label, (table_start_x, table_start_y - 30))
            # header_label = font.render("Rank     | Score       | Name                         | Level    | Difficulty  ", True, text_color)
            header_label = font.render("Rank      |  Level   |  Difficulty  |  Score             |  Name                         ", True, text_color)
            screen.blit(header_label, (table_start_x, table_start_y))

            for rank, score in enumerate(scores_list, 1):
                int_score = int(score['MAX_SCORE'])
                formatted_score = "{:,}".format(int_score)
                # score_text = f"{rank:<8} | {score['MAX_SCORE']:<12} | {score['PLAYER_NAME'][:20]:<30} | {score['LEVEL']:<8} | {score['DIFFICULTY_LEVEL']}"
                score_text = f"{rank:<12}    {score['LEVEL']:<8}       {score['DIFFICULTY_LEVEL']:<15}  {formatted_score:<15}     {score['PLAYER_NAME'][:20]:<30}"
                score_label = font.render(score_text, True, text_color)
                screen.blit(score_label, (table_start_x, table_start_y + rank * 38))

        # Draw Return to Main Menu button with border
        pygame.draw.rect(screen, button_color, button_rect)
        pygame.draw.rect(screen, border_color, button_rect, 2)
        button_text = font.render("Return to Main Menu", True, text_color)
        text_center_x = button_rect.x + button_rect.width // 2 - button_text.get_width() // 2
        screen.blit(button_text, (text_center_x, button_rect.y + 10))

        pygame.display.flip()



def game_over_buttons():
    font = pygame.font.Font(None, 36)
    play_again_button = pygame.Rect(SCREEN_WIDTH // 2 - 70, SCREEN_HEIGHT // 2 - 40, 200, 40)
    main_menu_button = pygame.Rect(SCREEN_WIDTH // 2 - 70, SCREEN_HEIGHT // 2 + 10, 200, 40)
    color = pygame.Color('dodgerblue2') # A good shade of blue
    border_color = pygame.Color('black') # Black color for the border

    while True:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            if event.type == pygame.MOUSEBUTTONDOWN:
                if play_again_button.collidepoint(event.pos):
                    reset_game()
                    return
                if main_menu_button.collidepoint(event.pos):
                    game_menu()
                    return

        # Draw the borders (black)
        pygame.draw.rect(screen, border_color, play_again_button.inflate(4, 4))
        pygame.draw.rect(screen, border_color, main_menu_button.inflate(4, 4))

        # Draw the buttons (blue)
        pygame.draw.rect(screen, color, play_again_button)
        pygame.draw.rect(screen, color, main_menu_button)

        play_again_text = font.render("Play Again", True, (255, 255, 255)) # White text
        main_menu_text = font.render("Main Menu", True, (255, 255, 255)) # White text

        screen.blit(play_again_text, (play_again_button.x + 20, play_again_button.y + 10))
        screen.blit(main_menu_text, (main_menu_button.x + 20, main_menu_button.y + 10))

        pygame.display.flip()




def main_loop():
    reset_game()
    initialize_game()
    start_time = pygame.time.get_ticks()

    while True:
        events = pygame.event.get()
        handle_exit(events)

        handle_player_input(events)
        if not GAME_OVER:
            player_control()
            handle_object_movement()
            handle_collisions()
        handle_game_logic()
        draw_elements(start_time)

        # Update the display
        pygame.display.flip()

        if GAME_OVER:
            # Update high scores
            update_high_scores(MAX_SCORE, PLAYER_NAME, LEVEL, DIFFICULTY_LEVEL)

            # Print high scores
            print_high_scores()

            # Options to Return to the menu
            game_over_buttons()

def game_menu():
    # Collect the player's name using the Pygame UI
    get_player_name()

    # Fonts and colors
    title_font = pygame.font.Font(None, 72)  # Larger font for the game title
    credits_font = pygame.font.Font(None, 24)  # Smaller font for the credits
    font = pygame.font.Font(None, 36)
    color = pygame.Color('dodgerblue2') # A good shade of blue for the buttons
    border_color = pygame.Color('black') # Black color for the border
    text_color = (255, 255, 255) # White text color

    start_game_button = pygame.Rect(SCREEN_WIDTH // 2 - 120, SCREEN_HEIGHT // 2 - 60, 240, 40)
    view_high_scores_button = pygame.Rect(SCREEN_WIDTH // 2 - 120, SCREEN_HEIGHT // 2, 240, 40)

    while True:
        screen.fill((0, 0, 0))  # Clear the screen

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            if event.type == pygame.MOUSEBUTTONDOWN:
                if start_game_button.collidepoint(event.pos):
                    main_loop()
                if view_high_scores_button.collidepoint(event.pos):
                    display_high_scores()

        # Game title
        game_title = title_font.render("First Pygame", True, text_color)
        title_position = (
        SCREEN_WIDTH // 2 - game_title.get_width() // 2, SCREEN_HEIGHT // 4 - game_title.get_height() // 2)
        screen.blit(game_title, title_position)

        # Credits
        credits = credits_font.render("by CSNEWB, Michael Barnes", True, text_color)
        credits_position = (
        SCREEN_WIDTH // 2 - credits.get_width() // 2, SCREEN_HEIGHT // 4 + game_title.get_height() // 2)
        screen.blit(credits, credits_position)

        # Draw the button borders (black)
        pygame.draw.rect(screen, border_color, start_game_button.inflate(4, 4))
        pygame.draw.rect(screen, border_color, view_high_scores_button.inflate(4, 4))

        # Draw the buttons (blue)
        pygame.draw.rect(screen, color, start_game_button)
        pygame.draw.rect(screen, color, view_high_scores_button)

        start_game_text = font.render("Start Game", True, text_color)
        view_high_scores_text = font.render("View High Scores", True, text_color)

        start_game_text_center_x = start_game_button.x + start_game_button.width // 2 - start_game_text.get_width() // 2
        view_high_scores_text_center_x = view_high_scores_button.x + view_high_scores_button.width // 2 - view_high_scores_text.get_width() // 2

        screen.blit(start_game_text, (start_game_text_center_x, start_game_button.y + 10))
        screen.blit(view_high_scores_text, (view_high_scores_text_center_x, view_high_scores_button.y + 10))

        pygame.display.flip()




# Entry point
if __name__ == "__main__":
    # Set the x and y position of the window
    x = 100
    y = 100
    os.environ['SDL_VIDEO_WINDOW_POS'] = "%d,%d" % (x, y)
    pygame.init()
    screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))  # Set the screen size
    game_menu()

