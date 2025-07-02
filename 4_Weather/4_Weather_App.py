import os
import pygame
import requests
from datetime import datetime, timedelta

# Initialize Pygame
pygame.init()

#------variables, objects, functions
PATH = '4_Weather/imgs/'

def load_image(folder, file):
    return pygame.image.load(os.path.join(PATH, folder, file))

def get_weather_openmeteo(lat, lon):
    url = f"https://api.open-meteo.com/v1/forecast?latitude={lat}&longitude={lon}&current_weather=true&timezone=auto"
    res = requests.get(url)
    data = res.json()

    current = data['current_weather']
    return current

backgrounds = {
    "day": {
        "clear": "day.png",
        "rain": "day_rain.png",
        "winter": "day_winter.png"
    },
    "evening": {
        "clear": "evening.png",
        "rain": "evening_rain.png",
        "winter": "evening_winter.png"
    },
    "night": {
        "clear": "night.png",
        "rain": "night_rain.png",
        "winter": "night_winter.png"
    }
}

clouds = {
    "day": "cloud_day.png",
    "evening": "cloud_evening.png",
    "night": "cloud_night.png"
}

cats = [
    "cat_grey.png",
    "cat_void.png",
    "cat_orange.png",
    "cat_white.png"
]
cat_index = 0

clothes = {
    "sunny": "cloth_sunny.png",
    "rain": "cloth_rain.png",
    "windy": "cloth_windy.png",
    "winter": "cloth_winter.png"
}

city_data = {
    "city_name": "Yogyakarta",
    "country": "Indonesia",
    "latitude": "-7.782961",
    "longitude": "110.367086"
}

# Background setup
current_time = datetime.now().strftime("%H:%M")
if current_time > "18:00":
    sky = "night"
elif current_time > "15:00":
    sky = "evening"
else:
    sky = "day"

# Assets setup based on weather
weather = get_weather_openmeteo(city_data["latitude"], city_data["longitude"])
print(weather)
sky = "night"
weather['weathercode'] = 1
cloud = False
match weather['weathercode']:
    case 0:
        condition = "clear"
        cloth = "sunny"
        offset = (32, 245)
    case 1 | 2 | 3 | 45 | 48:
        condition = "clear"
        cloth = "windy"
        offset = (17, 172)
        cloud = True
    case 51 | 53 | 55 | 56 | 57 | 61 | 63 | 65 | 80 | 81 | 82:
        condition = "rain"
        cloth = "rain"
        offset = (12, 167)
    case _:
        condition = "winter"
        cloth = "winter"
        offset = (40, 175)

# Loading assets
bg_img = load_image("background/", backgrounds[sky][condition])
print(clouds["day"])
if cloud:
    cloud_img = load_image("clouds/", clouds[sky])

# Set up the game window
screen = pygame.display.set_mode((190, 360))
pygame.display.set_caption("Meownie Weather")

# Game loop
running = True
while running:
    screen.blit(bg_img, (0, 0))
    if cloud:
        screen.blit(cloud_img, (0, 30))
    screen.blit(load_image("cats/", cats[cat_index]), (40, 210))
    screen.blit(load_image("clothes/", clothes[cloth]), offset)
    pygame.display.update()
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
        elif event.type == pygame.KEYDOWN:
            if event.key == pygame.K_RIGHT:
                cat_index = (cat_index + 1) % len(cats)
            elif event.key == pygame.K_LEFT:
                cat_index = (cat_index - 1) % len(cats)

# Quit Pygame
pygame.quit()

# TO DO:
# add temperature, time, status, friend