import pygame
import sys
import time
import random
import math


# PRELIMINARY SETUP
pygame.init()
screen_width = 650
screen_height = 700
screen = pygame.display.set_mode((screen_width, screen_height))
pygame.display.set_caption("Paper Crusher")

scissor_width = 150
scissor_height = 125



#PAPER
# Create the paper area rectangle
paper_area_width = 75
paper_area_height = 125
paper_area = pygame.Rect((screen_width - paper_area_width) // 2, (screen_height - paper_area_height) // 2, paper_area_width, paper_area_height)
paper_image1 = pygame.image.load("paper1.png")
paper_image2 = pygame.image.load("paper2.png")

# Function to calculate movement components based on angle and speed
def calculate_movement(angle, speed):
    # Convert angle from degrees to radians
    angle_rad = math.radians(angle)
    # Calculate horizontal and vertical components of movement
    dx = speed * math.cos(angle_rad)
    dy = speed * math.sin(angle_rad)
    return dx, dy

# Function to spawn a new paper ball ALL IMPORTANT FOR DIFFICULTY
def spawn_paper_ball():
    # Randomly select size for paper ball images
    paper_size = random.randint(50, 60)
    
    # Randomly select paper image and speed
    selected_image = random.choice([paper_image1, paper_image2])
    speed = random.randint(1, 3)

    # Resize paper image to match the selected size
    paper_image = pygame.transform.scale(selected_image, (paper_size, paper_size))

    # Randomly choose direction (angle) for paper ball to move
    direction = random.uniform(0, 360)  # Random angle between 0 and 360 degrees

    # Randomly choose starting position within paper area
    start_x = random.randint(paper_area.left, paper_area.right - paper_size)
    start_y = random.randint(paper_area.top, paper_area.bottom - paper_size)

    return {'image': paper_image, 'rect': pygame.Rect(start_x, start_y, paper_size, paper_size), 'direction': direction, 'speed': speed}

# List to store paper balls
paper_balls = []



#RECTANGLES/SCISSOR
# Load scissor image frames
scissor_frames = []
for i in range(1, 5):  # Assuming you have 4 frames of the animation
    frame = pygame.image.load(f"s{i}.png")  # Replace with your image file naming convention
    frame = pygame.transform.scale(frame, (scissor_width, scissor_height)) #IMPORTANT FOR DIFFICULTY
    scissor_frames.append(frame)

# Define rectangles
rectangles = [
    pygame.Rect(0, 85, 99, 530),   # Left rectangle
    pygame.Rect(551, 85, 99, 530), # Right rectangle
    pygame.Rect(100, 0, 450, 100),  # Top rectangle
    pygame.Rect(100, 600, 450, 100) # Bottom rectangle
]

# Hover images
hover_image_left = pygame.image.load("bluehitbox.png")   # Controls, fix image so that a key is on it
hover_image_right = pygame.image.load("greenhitbox.png") # Controls, "" d key
hover_image_top = pygame.image.load("redhitbox.png")     # Controls, "" w key
hover_image_bottom = pygame.image.load("yellowhitbox.png")  # Controls, "" s key

hover_images = {
    0: hover_image_left,
    1: hover_image_right,
    2: hover_image_top,
    3: hover_image_bottom
}

# Define key mappings for shooting
key_mappings = {
    0: pygame.K_a,  # Left rectangle, press 'A'
    1: pygame.K_d,  # Right rectangle, press 'D'
    2: pygame.K_w,  # Top rectangle, press 'W'
    3: pygame.K_s   # Bottom rectangle, press 'S'
}




#SCORE
# Initialize score
score = 0




#  VARIABLES
active_rectangle = None
scissors = []
transparent = (100, 100, 100, 0)
# Initialize the last press time
last_press_time = 0



# GAME LOOP
running = True
while running:
    # Draw rectangles
    for r in rectangles:
        pygame.draw.rect(screen, transparent, r)

    # Background
    screen.blit(pygame.transform.scale(pygame.image.load("BACKGROUND.png.png"), (screen_width, screen_height)), (0,0))
    
    mouse_pos = pygame.mouse.get_pos()

    # Reset active_rectangle
    active_rectangle = None

    # Check if the mouse is hovering over a rectangle
    for idx, rect in enumerate(rectangles):
        if rect.collidepoint(mouse_pos):
            active_rectangle = idx
            screen.blit(hover_images[active_rectangle], (rect.x, rect.y))

    # Cooldown for shooting
    cooldown_time = 0.5  # Delay in seconds IMPORTANT FOR DIFFICULTY
    current_time = time.time()

    # Event handling
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
        elif event.type == pygame.KEYDOWN:
            # Check if enough time has passed since the last shot
            if current_time - last_press_time >= cooldown_time:
                # Check if a key is pressed and if it matches the key for the active rectangle
                if active_rectangle is not None and event.key == key_mappings.get(active_rectangle):
                    # Shoot scissors
                    if active_rectangle == 0:  # Left rectangle
                        scissors.append({'pos': (rectangles[0].x+130, mouse_pos[1]), 'direction': (1, 0), 'frame': 0, 'angle': -90})
                        score -= 1#IMPORTANT FOR DIFFICULTY
                    elif active_rectangle == 1:  # Right rectangle
                        scissors.append({'pos': (rectangles[1].x-25, mouse_pos[1]), 'direction': (-1, 0), 'frame': 0, 'angle': 90})
                        score -= 1
                    elif active_rectangle == 2:  # Top rectangle
                        scissors.append({'pos': (mouse_pos[0], rectangles[2].y+140), 'direction': (0, 1), 'frame': 0, 'angle': 180})
                        score -= 1
                    elif active_rectangle == 3:  # Bottom rectangle
                        scissors.append({'pos': (mouse_pos[0], rectangles[3].y-30), 'direction': (0, -1), 'frame': 0, 'angle': 0})
                        score -= 1
                    # Update the last pressed time
                    last_press_time = current_time

# Move and draw scissors
    for scissor in scissors:
        # Rotate the scissor image
        rotated_scissor = pygame.transform.rotate(scissor_frames[scissor['frame']], scissor['angle'])
        # Get the rect of the rotated image to adjust the position
        rotated_rect = rotated_scissor.get_rect(center=scissor['pos'])
        # Blit the rotated image
        screen.blit(rotated_scissor, rotated_rect.topleft)
        # Update the frame of the scissor
        scissor['frame'] = (scissor['frame'] + 1) % len(scissor_frames)
        # Move the scissor
        scissor['pos'] = (scissor['pos'][0] + scissor['direction'][0] * 5, scissor['pos'][1] + scissor['direction'][1] * 5)


        # Check collision with opposite side of the screen
        if scissor['direction'][0] == 1 and scissor['pos'][0] > screen_width:
            scissors.remove(scissor)
        elif scissor['direction'][0] == -1 and scissor['pos'][0] < 0:
            scissors.remove(scissor)
        elif scissor['direction'][1] == 1 and scissor['pos'][1] > screen_height:
            scissors.remove(scissor)
        elif scissor['direction'][1] == -1 and scissor['pos'][1] < 0:
            scissors.remove(scissor)
        for paper_ball in paper_balls:# Check collision with paper balls
            if paper_ball['rect'].colliderect(pygame.Rect(scissor['pos'], (50, 50))):
                score += 2
                paper_balls.remove(paper_ball)
                break  # Exit inner loop after one collision

        # Spawn a new paper ball with a certain probability
    if random.random() < 0.1:  # IMPORTANT FOR DIFFICULTY FREQUENCY
        paper_balls.append(spawn_paper_ball())

    # Move and draw paper balls
    for paper_ball in paper_balls:
        # Calculate movement components based on direction and speed
        dx, dy = calculate_movement(paper_ball['direction'], paper_ball['speed'])
        # Update position of paper ball based on movement components
        paper_ball['rect'].x += dx
        paper_ball['rect'].y += dy

        # Check if paper ball collides with any of the original four rectangles
        for rect in rectangles:
            if paper_ball['rect'].colliderect(rect):
                # Remove paper ball if it collides with a rectangle
                score -= 2#IMPORTANT FOR DIFFICULTY
                paper_balls.remove(paper_ball)
                break

        # Draw paper ball on the screen
        screen.blit(paper_ball['image'], paper_ball['rect'])

    # Draw paper area (for visualization)
    pygame.draw.rect(screen, (222, 222, 222), paper_area, 2)
    
    # Update and display score
    font = pygame.font.Font(None, 40)
    score_text = font.render(f"Score: {score}", True, (90, 90, 90))
    screen.blit(score_text, (15, 15))
    screen.blit(score_text, (512, 15))
    screen.blit(score_text, (15, 650))
    screen.blit(score_text, (512, 650))
    if score<=-500:
        running=False

    pygame.display.flip()

pygame.quit()
sys.exit()