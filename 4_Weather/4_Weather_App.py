import os
import pygame
import requests
from datetime import datetime, timedelta

# Initialize Pygame
pygame.init()

#------variables, objects, functions
PATH = '4_Weather/imgs/'
FONT_PATH = '4_Weather/font/PixelifySans.ttf'
temp_font = pygame.font.Font(FONT_PATH, 64)
status_font = pygame.font.Font(FONT_PATH, 18)


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

box = {
    "day": "day-box.png",
    "evening": "evening-box.png",
    "night": "night-box.png"
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
    text_box = "night"
elif current_time > "15:00":
    sky = "evening"
    text_box = "evening"
else:
    sky = "day"
    text_box = "day"

# Assets setup based on weather
weather = get_weather_openmeteo(city_data["latitude"], city_data["longitude"])
print(weather)


# check img
# sky = "night"
# text_box = "night"


# weather['weathercode'] = 1
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

# Text setup
temperature = weather["temperature"]
status_map = {
    0: "Clear",
    1: "Mainly Clear",
    2: "Partly Cloudy",
    3: "Overcast",
    45: "Fog",
    48: "Depositing Fog",
    51: "Light Drizzle",
    53: "Moderate Drizzle",
    55: "Dense Drizzle",
    56: "Freezing Drizzle",
    57: "Freezing Drizzle+",
    61: "Light Rain",
    63: "Moderate Rain",
    65: "Heavy Rain",
    80: "Light Showers",
    81: "Moderate Showers",
    82: "Violent Showers"
    # Add more codes as needed
}
weather_status = status_map.get(weather["weathercode"], "Unknown")

# Loading assets
bg_img = load_image("background/", backgrounds[sky][condition])
if cloud:
    cloud_img = load_image("clouds/", clouds[sky])
box_img = load_image("box/", box[text_box])
box_img.set_alpha(180) 
cat_img = load_image("cats/", cats[cat_index])
cloth_img = load_image("clothes/", clothes[cloth])

temp_text = temp_font.render(f"{int(temperature)}°C", True, (255, 255, 255))
status_text = status_font.render(weather_status, True, (255, 255, 255))

# Set up the game window
screen = pygame.display.set_mode((190, 360))
pygame.display.set_caption("Meownie Weather")

# Game loop
running = True
while running:
    screen.blit(bg_img, (0, 0))
    if cloud:
        screen.blit(cloud_img, (0, 30))
    screen.blit(box_img, (10, 10))
    screen.blit(temp_text, (20, 40))
    screen.blit(status_text, (20, 30))

    screen.blit(cat_img, (40, 210))
    screen.blit(cloth_img , offset)
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