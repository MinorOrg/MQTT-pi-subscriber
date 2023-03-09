import sys, math
import threading

# Import and initialize pygame
import pygame

# Values
screenSize = width, height = 800, 800
boundaryDimensions= {"left": 50,
                     "right": width - 50,
                     "top": 50,
                     "bottom": height - 50,
                     }
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



def isDeviceOutOfBound(deviceCenter, deviceRadius):
    left = deviceCenter[0] - deviceRadius
    right = deviceCenter[0] + deviceRadius
    top = deviceCenter[1] - deviceRadius
    bottom = deviceCenter[1] + deviceRadius

    if(
        left < boundaryDimensions["left"] or
        right > boundaryDimensions["right"] or
        top < boundaryDimensions["top"] or
        bottom > boundaryDimensions["bottom"]
    ):
        return True
    else:
        return False

# Calculate distance between two points
def calculateDistance(x1, y1, x2, y2):
    return math.sqrt((x2-x1)**2 + (y2-y1)**2);

def updatePixelPerDistance():
    global pixelPerDistance
    pixelPerDistance = calculateDistance(center[0], center[1], esp1pos[0], esp1pos[1]) / 2
    pixelPerDistance *= scaleFactor

def scale():
    print("Scaled!!")
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

def display():
    pygame.init()
    # Create the screen
    screen = pygame.display.set_mode(screenSize)   
    
    global scaleFactor, pixelPerDistance, distanceFromESP1
    screen.fill(black)

    # Surface to draw the circles
    # sizeOfRectForRadiation = (distancePerPixel * 4, distancePerPixel * 4)
    radiationSurface1 = pygame.Surface(screenSize, pygame.SRCALPHA)
    radiationSurface2 = pygame.Surface(screenSize, pygame.SRCALPHA)
    radiationSurface3 = pygame.Surface(screenSize, pygame.SRCALPHA)

    scale()
    updatePixelPerDistance()


    # Draw a circle around the esp devices
    pygame.draw.circle(radiationSurface1, esp1Radiation, esp1pos_scaled, pixelPerDistance * distanceFromESP1 * scaleFactor)
    pygame.draw.circle(radiationSurface2, esp2Radiation, esp2pos_scaled, pixelPerDistance * distanceFromESP2 * scaleFactor)
    pygame.draw.circle(radiationSurface3, esp3Radiation, esp3pos_scaled, pixelPerDistance * distanceFromESP3 * scaleFactor)

    screen.blit(radiationSurface1, (0,0))
    screen.blit(radiationSurface2, (0,0))
    screen.blit(radiationSurface3, (0,0))

    # Draw the three ESPs
    pygame.draw.circle(screen, esp1Color, esp1pos_scaled, 5)
    pygame.draw.circle(screen, esp2Color, esp2pos_scaled, 5)
    pygame.draw.circle(screen, esp3Color, esp3pos_scaled, 5)


    # Display the screen
    pygame.display.flip()
    # Main loop
    running = True
    while running:

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
    
    pygame.quit()
    sys.exit()

def show(dis1, dis2, dis3):
    global distanceFromESP1, distanceFromESP2, distanceFromESP3, scaleFactor
    distanceFromESP1 = dis1
    distanceFromESP2 = dis2
    distanceFromESP3 = dis3

    maxDist = max(dis1, dis2, dis3)
    scaleFactor = 2 / maxDist
    # print(scaleFactor)

    display()

