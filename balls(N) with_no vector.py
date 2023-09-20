import pygame
import sys
import math
import random

# Initialize the game
pygame.init()

# Set up display
width, height = 800, 600
window = pygame.display.set_mode((width, height))

# Set up initial parameters
ball_radius = 15
N = 7 # You can change this value to any number of balls
balls = []

for _ in range(N):
    balls.append({
        #"pos": [random.randint(ball_radius, width - ball_radius), random.randint(ball_radius, height - ball_radius)],
        "pos": [random.randint(20,width-20), random.randint(20, height - 20)],
        "vel": [random.uniform(-6, 6), random.uniform(-6, 6)],
        'color':(random.randint(0,255),random.randint(0,255),random.randint(0,255),)
    })

def check_collision(pos1, pos2, radius):
    distance = math.sqrt((pos1[0] - pos2[0])**2 + (pos1[1] - pos2[1])**2)
    return distance < 2 * radius

def resolve_collision(pos1, vel1, pos2, vel2):
    # Calculate the angle of collision
    collision_angle = math.atan2(pos2[1] - pos1[1], pos2[0] - pos1[0])

    # Calculate the new velocities in the collision axis
    vel1_mag = math.sqrt(vel1[0]**2 + vel1[1]**2)
    vel2_mag = math.sqrt(vel2[0]**2 + vel2[1]**2)
    vel1_angle = math.atan2(vel1[1], vel1[0])
    vel2_angle = math.atan2(vel2[1], vel2[0])

    vel1_mag_new = vel2_mag * math.cos(vel2_angle - collision_angle)
    vel2_mag_new = vel1_mag * math.cos(vel1_angle - collision_angle)
    
    # Calculate the new velocities in the perpendicular axis (which remain unchanged)
    vel1_perpendicular = vel1_mag * math.sin(vel1_angle - collision_angle)
    vel2_perpendicular = vel2_mag * math.sin(vel2_angle - collision_angle)

    # Calculate the final velocities in x and y components
    vel1x_new = vel1_mag_new * math.cos(collision_angle) + vel1_perpendicular * math.cos(collision_angle + math.pi/2)
    vel1y_new = vel1_mag_new * math.sin(collision_angle) + vel1_perpendicular * math.sin(collision_angle + math.pi/2)

    vel2x_new = vel2_mag_new * math.cos(collision_angle) + vel2_perpendicular * math.cos(collision_angle + math.pi/2)
    vel2y_new = vel2_mag_new * math.sin(collision_angle) + vel2_perpendicular * math.sin(collision_angle + math.pi/2)
    
    return [vel1x_new, vel1y_new], [vel2x_new, vel2y_new]

# Main game loop
while True:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
            sys.exit()

    # Update ball positions and check for collisions with walls
    for ball in balls:
        ball['pos'][0] += ball['vel'][0]
        ball['pos'][1] += ball['vel'][1]
        if ball['pos'][0] - ball_radius < 0 or ball['pos'][0] + ball_radius > width:
            ball['vel'][0] = -ball['vel'][0]
        if ball['pos'][1] - ball_radius < 0 or ball['pos'][1] + ball_radius > height:
            ball['vel'][1] = -ball['vel'][1]

    # Check for collisions between balls and resolve collisions
    for i in range(len(balls)):
        for j in range(i+1, len(balls)):
            if check_collision(balls[i]['pos'], balls[j]['pos'], ball_radius):
                balls[i]['vel'], balls[j]['vel'] = resolve_collision(balls[i]['pos'], balls[i]['vel'], balls[j]['pos'], balls[j]['vel'])

    # Clear the screen
    window.fill((150, 50, 130))

    # Draw the balls and velocity vectors
    for ball in balls:
        pygame.draw.circle(window, ball['color'], ball['pos'], ball_radius)
        

    # Update the display
    pygame.display.flip()

    # Cap the frame rate
    pygame.time.Clock().tick(60)
