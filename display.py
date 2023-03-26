import sys, math
import threading

# Import and initialize pygame
import pygame

# Values
screenSize = width, height = 800, 800
scaleFactor = 1
pixelPerDistance = 10

# Colors
esp1Color = 255, 255, 255
esp2Color = 255, 0, 0
esp3Color = 0, 0, 255
deviceColor = 0, 255, 0
black = 0, 0, 0
esp1Radiation = pygame.Color(192, 57, 43, 128)
esp2Radiation = pygame.Color(41, 128, 185,128)
esp3Radiation = pygame.Color(142, 68, 173,128)

# Positions
center = width/2, height/2 - 50
esp3pos = center[0], height - 50
esp2pos = center[0] + math.sqrt(3) * height / 4, height/4 - 50
esp1pos = center[0] - math.sqrt(3) * height / 4, height/4 - 50
devicePos = center[0], center[1]
esp1pos_scaled = esp1pos
esp2pos_scaled = esp2pos
esp3pos_scaled = esp3pos

# Distances
distanceFromESP1 = 2
distanceFromESP2 = 2
distanceFromESP3 = 2



# Radii of the radiations
radii = []

# Calculate distance between two points
def calculateDistance(x1, y1, x2, y2):
    return math.sqrt((x2-x1)**2 + (y2-y1)**2);

def updatePixelPerDistance():
    global pixelPerDistance
    pixelPerDistance = calculateDistance(center[0], center[1], esp1pos[0], esp1pos[1]) / 2
    # pixelPerDistance *= scaleFactor

def scale():
    # print("Scaled!!")
    global esp3pos, esp1pos, esp2pos
    global radiationSurface1, radiationSurface2, radiationSurface3
    global scaleFactor
    global esp1pos_scaled, esp2pos_scaled, esp3pos_scaled

    # Translate the fixed point to origin
    esp1pos_scaled = esp1pos[0] - center[0], esp1pos[1] - center[1]
    esp2pos_scaled = esp2pos[0] - center[0], esp2pos[1] - center[1]
    esp3pos_scaled = esp3pos[0] - center[0], esp3pos[1] - center[1]

    # Scale the ESP circles
    esp1pos_scaled = esp1pos_scaled[0] * scaleFactor, esp1pos_scaled[1] * scaleFactor
    esp2pos_scaled = esp2pos_scaled[0] * scaleFactor, esp2pos_scaled[1] * scaleFactor
    esp3pos_scaled = esp3pos_scaled[0] * scaleFactor, esp3pos_scaled[1] * scaleFactor

    # Translate back
    esp1pos_scaled = esp1pos_scaled[0] + center[0], esp1pos_scaled[1] + center[1]
    esp2pos_scaled = esp2pos_scaled[0] + center[0], esp2pos_scaled[1] + center[1]
    esp3pos_scaled = esp3pos_scaled[0] + center[0], esp3pos_scaled[1] + center[1]

def render():
    print("rendering")

def clearScreen(screen):
    screen.fill("black")


def display():
    pygame.init()

    # Create the screen
    screen = pygame.display.set_mode(screenSize)   
    pygame.display.set_caption("WiFi Trilateration")


    
    global scaleFactor, pixelPerDistance, distanceFromESP1, distanceFromESP2, distanceFromESP3

    # Font for the text
    font = pygame.font.Font(None, 36)
    esp1Text = font.render("ESP1: " + str(round(distanceFromESP1, 2)) + "m", True, (255, 255, 255))
    esp2Text = font.render("ESP2: " + str(round(distanceFromESP2, 2)) + "m", True, (255, 255, 255))
    esp3Text = font.render("ESP3: " + str(round(distanceFromESP3, 2)) + "m", True, (255, 255, 255))

    esp1Rect = esp1Text.get_rect()
    esp2Rect = esp2Text.get_rect()
    esp3Rect = esp3Text.get_rect()

    esp1Rect.topleft = (10, 10)
    esp2Rect.topleft = (10, esp1Rect.bottomleft[1] + 5)
    esp3Rect.topleft = (10, esp2Rect.bottomleft[1] + 5)

    # Duration of animation
    duration = 5

    # Define frequency of the sine wave
    frequency = 2 * math.pi / duration

    radiationRadiusChange = 1
    clock = pygame.time.Clock()

    # Main loop
    running = True
    while running:

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
        
        clearScreen(screen)
        scale()
        updatePixelPerDistance()

        time = pygame.time.get_ticks() / 1000


        # Surface to draw the circles
        radiationSurface1 = pygame.Surface(screenSize, pygame.SRCALPHA)
        radiationSurface2 = pygame.Surface(screenSize, pygame.SRCALPHA)
        radiationSurface3 = pygame.Surface(screenSize, pygame.SRCALPHA)

        # Draw a circle around the esp devices with a breathing pattern
        radius1 = pixelPerDistance * distanceFromESP1 * scaleFactor
        radius2 = pixelPerDistance * distanceFromESP2 * scaleFactor
        radius3 = pixelPerDistance * distanceFromESP3 * scaleFactor  

        radiationRange = (
                        [radius1 * 0.97, radius1 * 1.03],
                        [radius2 * 0.97, radius2 * 1.03],
                        [radius3 * 0.97, radius3 * 1.03]
                        )

        radius1 = (radiationRange[0][1] - radiationRange[0][0]) / 2 * math.sin(frequency * time) + (radiationRange[0][1] + radiationRange[0][0]) / 2

        radii = []

        for i in range(3):
            maxRadius = radiationRange[i][1]
            minRadius = radiationRange[i][0]

            radii.append((maxRadius - minRadius) / 2 * math.sin(frequency * time) + (radiationRange[i][1] + radiationRange[i][0]) / 2)

        # Draw a circle around the esp devices
        pygame.draw.circle(radiationSurface1, esp1Radiation, esp1pos_scaled, radii[0])
        pygame.draw.circle(radiationSurface2, esp2Radiation, esp2pos_scaled, radii[1])
        pygame.draw.circle(radiationSurface3, esp3Radiation, esp3pos_scaled, radii[2])

        screen.blit(radiationSurface1, (0,0))
        screen.blit(radiationSurface2, (0,0))
        screen.blit(radiationSurface3, (0,0))

        # Draw the three ESPs
        pygame.draw.circle(screen, esp1Color, esp1pos_scaled, 5)
        pygame.draw.circle(screen, esp2Color, esp2pos_scaled, 5)
        pygame.draw.circle(screen, esp3Color, esp3pos_scaled, 5) 

        # Display the text
        screen.blit(esp1Text, esp1Rect)
        screen.blit(esp2Text, esp2Rect)
        screen.blit(esp3Text, esp3Rect)

        # Display the screen
        pygame.display.flip()

        clock.tick(60)
    
    pygame.quit()
    sys.exit()

def show(dis1, dis2, dis3):
    global distanceFromESP1, distanceFromESP2, distanceFromESP3, scaleFactor
    distanceFromESP1 = dis1
    distanceFromESP2 = dis2
    distanceFromESP3 = dis3

    maxDist = max(distanceFromESP1, distanceFromESP2, distanceFromESP3)
    scaleFactor = 2 / maxDist
    print(scaleFactor)

    display()