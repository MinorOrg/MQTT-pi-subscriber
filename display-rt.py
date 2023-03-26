import paho.mqtt.client as mqtt
import sys
import pygame

MQTT_ADDRESS = '0.0.0.0'
MQTT_USER = 'mosquitong'
MQTT_PASSWORD = 'elong-mosquitong'
MQTT_TOPIC_ESP = 'esp/+'
MQTT_TOPIC_ESP1 = 'esp/ble1'
MQTT_TOPIC_ESP2 = 'esp/ble2'
MQTT_TOPIC_ESP3 = 'esp/ble3'

testssid = "wifi"




pygame.init()


size = (1400, 700)
radiationSurfaceSize = (700, 700)

# Positions of the ESPs
esp1_1 = (100, 600)
esp2_1 = (300, 200)
esp3_1 = (500, 600)
esp1_2 = (800, 600)
esp2_2 = (1000, 200)
esp3_2 = (1200, 600)

# Colors
esp1Color = 255, 255, 255
white = esp1Color
esp2Color = 255, 0, 0
esp3Color = 0, 0, 255
deviceColor = 0, 255, 0
black = 0, 0, 0
esp1Radiation = pygame.Color(192, 57, 43, 128)
esp2Radiation = pygame.Color(41, 128, 185,128)
esp3Radiation = pygame.Color(142, 68, 173,128)

font = pygame.font.Font(None, 24)

device1Text = font.render("Device 1", True, white)
device2Text = font.render("Device 2", True, white)


screen = pygame.display.set_mode(size)
pygame.display.set_caption("Trilateration Visualizer")

A = [-92.6483870967742, -87.7368191721133, -90.50672043010752]

n = 2

running = True

def on_connect(client, userdata, flags, rc):
    print('Connected with result code ' + str(rc))
    client.subscribe(MQTT_TOPIC_ESP)

esp1rssi_nothing = 0
esp2rssi_nothing = 0
esp3rssi_nothing = 0

esp1rssi_mobhaile = 0
esp2rssi_mobhaile = 0
esp3rssi_mobhaile = 0

def on_message(client, userdata, msg):

    global esp1rssi_nothing, esp1rssi_mobhaile, esp2rssi_nothing, esp2rssi_mobhaile, esp3rssi_nothing, esp3rssi_mobhaile


    payload = str(msg.payload)[2::][::-1][1::][::-1].strip()
    print(payload)
    for ble in payload.split(':'):
        if ble == ' ' or ble == '':
            continue
        namerssi = str(ble).split(',')
        name = namerssi[0].strip()
        rssi = int(namerssi[1].strip())
        if msg.topic ==  MQTT_TOPIC_ESP1:
            if name == "nothing":
                esp1rssi_nothing= 10**((A[0]-rssi)/(10*n))
            elif name == "mobhaile":
                esp1rssi_mobhaile = 10**((A[0]-rssi)/(10*n))

        elif msg.topic ==  MQTT_TOPIC_ESP2:
            if name == "nothing":
                esp2rssi_nothing = 10**((A[1]-rssi)/(10*n))
            elif name == "mobhaile":
                esp2rssi_mobhaile = 10**((A[1]-rssi)/(10*n))
                # mobhaile_file.write(f"esp2: {rssi} \n")

        
        elif msg.topic ==  MQTT_TOPIC_ESP3:
            if name == "nothing":
                esp3rssi_nothing = 10**((A[2]-rssi)/(10*n))
                # nothing_file.write(f"esp3: {rssi} \n")
            elif name == "mobhaile":
                esp3rssi_mobhaile = 10**((A[2]-rssi)/(10*n))
                # mobhaile_file.write(f"esp3: {rssi} \n")
    
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
        
    esp1Text_1 = font.render("ESP1: " + str(round(esp1rssi_nothing, 2)) + "m", True, (255, 255, 255))
    esp2Text_1 = font.render("ESP2: " + str(round(esp2rssi_nothing, 2)) + "m", True, (255, 255, 255))
    esp3Text_1 = font.render("ESP3: " + str(round(esp3rssi_nothing, 2)) + "m", True, (255, 255, 255))

    esp1Text_2 = font.render("ESP1: " + str(round(esp1rssi_mobhaile, 2)) + "m", True, (255, 255, 255))
    esp2Text_2 = font.render("ESP2: " + str(round(esp2rssi_mobhaile, 2)) + "m", True, (255, 255, 255))
    esp3Text_2 = font.render("ESP3: " + str(round(esp3rssi_mobhaile, 2)) + "m", True, (255, 255, 255))

    device1Rect = device1Text.get_rect()
    device2Rect = device2Text.get_rect()

    esp1Rect_1 = esp1Text_1.get_rect()
    esp2Rect_1 = esp2Text_1.get_rect()
    esp3Rect_1 = esp3Text_1.get_rect()

    esp1Rect_2 = esp1Text_2.get_rect()
    esp2Rect_2 = esp2Text_2.get_rect()
    esp3Rect_2 = esp3Text_2.get_rect()

    device1Rect.centerx = 350
    device1Rect.centery = 30
    device2Rect.centerx = 1050
    device2Rect.centery = 30

    esp1Rect_1.topleft = (20, 30)
    esp2Rect_1.topleft = (20, esp1Rect_1.bottomleft[1] + 5)
    esp3Rect_1.topleft = (20, esp2Rect_1.bottomleft[1] + 5)

    esp1Rect_2.topleft = (720, 30)
    esp2Rect_2.topleft = (720, esp1Rect_2.bottomleft[1] + 5)
    esp3Rect_2.topleft = (720, esp2Rect_2.bottomleft[1] + 5)

    # if running:    
    clearScreen(screen)
    # Surface to draw the circles
    radiationSurface1_1 = pygame.Surface(radiationSurfaceSize, pygame.SRCALPHA)
    radiationSurface2_1 = pygame.Surface(radiationSurfaceSize, pygame.SRCALPHA)
    radiationSurface3_1 = pygame.Surface(radiationSurfaceSize, pygame.SRCALPHA)
    radiationSurface1_2 = pygame.Surface(radiationSurfaceSize, pygame.SRCALPHA)
    radiationSurface2_2 = pygame.Surface(radiationSurfaceSize, pygame.SRCALPHA)
    radiationSurface3_2 = pygame.Surface(radiationSurfaceSize, pygame.SRCALPHA)
    # Draw a circle around the esp devices with a breathing pattern
    radius1_1 = esp1rssi_nothing * 200
    radius2_1 = esp2rssi_nothing * 200
    radius3_1 = esp3rssi_nothing * 200
    radius1_2 = esp1rssi_mobhaile * 200
    radius2_2 = esp2rssi_mobhaile * 200
    radius3_2 = esp3rssi_mobhaile * 200
    # Draw a circle around the esp devices
    pygame.draw.circle(radiationSurface1_1, esp1Radiation, esp1_1, radius1_1)
    pygame.draw.circle(radiationSurface2_1, esp2Radiation, esp2_1, radius2_1)
    pygame.draw.circle(radiationSurface3_1, esp3Radiation, esp3_1, radius3_1)
    pygame.draw.circle(radiationSurface1_2, esp1Radiation, esp1_1, radius1_2)
    pygame.draw.circle(radiationSurface2_2, esp2Radiation, esp2_1, radius2_2)
    pygame.draw.circle(radiationSurface3_2, esp3Radiation, esp3_1, radius3_2)
    # Draw the surfaces to the screen
    screen.blit(radiationSurface1_1, (0,0))
    screen.blit(radiationSurface2_1, (0,0))
    screen.blit(radiationSurface3_1, (0,0))
    screen.blit(radiationSurface1_2, (700,0))
    screen.blit(radiationSurface2_2, (700,0))
    screen.blit(radiationSurface3_2, (700,0))
    # Display esps for first phone
    pygame.draw.circle(screen, esp1Color, esp1_1, 5)
    pygame.draw.circle(screen, esp2Color, esp2_1, 5)
    pygame.draw.circle(screen, esp3Color, esp3_1, 5)
    pygame.draw.circle(screen, esp1Color, ( esp1Rect_1.left - 10, esp1Rect_1.centery), 5)
    pygame.draw.circle(screen, esp2Color, ( esp2Rect_1.left - 10, esp2Rect_1.centery), 5)
    pygame.draw.circle(screen, esp3Color, ( esp3Rect_1.left - 10, esp3Rect_1.centery), 5)
    
    # Draw line between the screens
    pygame.draw.line(screen, white, (700, 0), (700, 700))
    # Display esps for second phone
    pygame.draw.circle(screen, esp1Color, esp1_2, 5)
    pygame.draw.circle(screen, esp2Color, esp2_2, 5)
    pygame.draw.circle(screen, esp3Color, esp3_2, 5)
    pygame.draw.circle(screen, esp1Color, (esp1Rect_2.left - 10, esp1Rect_2.centery), 5)
    pygame.draw.circle(screen, esp2Color, ( esp2Rect_2.left - 10, esp2Rect_2.centery), 5)
    pygame.draw.circle(screen, esp3Color, ( esp3Rect_2.left - 10, esp3Rect_2.centery,), 5)
    # Display the text
    screen.blit(device1Text, device1Rect)
    screen.blit(device2Text, device2Rect)
    screen.blit(esp1Text_1, esp1Rect_1)
    screen.blit(esp2Text_1, esp2Rect_1)
    screen.blit(esp3Text_1, esp3Rect_1)
    screen.blit(esp1Text_2, esp1Rect_2)
    screen.blit(esp2Text_2, esp2Rect_2)
    screen.blit(esp3Text_2, esp3Rect_2)
    pygame.display.flip()

def clearScreen(screen):
    screen.fill("black")

def main():
   

    mqtt_client = mqtt.Client()
    mqtt_client.on_connect = on_connect
    mqtt_client.on_message = on_message
    mqtt_client.username_pw_set(MQTT_USER, MQTT_PASSWORD)
    mqtt_client.connect(MQTT_ADDRESS, 1883, 60)
    mqtt_client.loop_forever()

    

    # Font for
       
if __name__ == '__main__':
    main()
