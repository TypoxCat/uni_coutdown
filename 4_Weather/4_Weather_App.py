import os
import pygame
import pytz
import requests
from datetime import datetime

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

city_data = {
    "city_name": "Yogyakarta",
    "country": "Indonesia",
    "latitude": "-7.782961",
    "longitude": "110.367086"
}

friend_data = {
    "city_name": "Tokyo",
    "country": "Japan",
    "latitude": "35.6895",
    "longitude": "139.6917"
}

def get_sky(current_time):
    if current_time > "18:00":
        return "night", "night"
    elif current_time > "15:00":
        return "evening", "evening"
    else:
        return "day", "day"

# Background setup
current_time = datetime.now().strftime("%H:%M")
friend_tz = pytz.timezone("Australia/Canberra")
friend_time = datetime.now(friend_tz).strftime("%H:%M")

sky, text_box = get_sky(current_time)
friend_sky, friend_text_box = get_sky(friend_time)

# Assets setup based on weather
weather = get_weather_openmeteo(city_data["latitude"], city_data["longitude"])
temperature = weather["temperature"]
time = weather['time']
print(time)
weather_status = status_map.get(weather["weathercode"], "Unknown")

friend_weather = get_weather_openmeteo(friend_data["latitude"], friend_data["longitude"])
friend_temperature = friend_weather["temperature"]
friend_status = status_map.get(friend_weather["weathercode"], "Unknown")

# weather['weathercode'] = 1
cloud = False

def get_weatherCode(weathercode):
    match weathercode:
        case 0 | 1:
            return "clear", "sunny", (32, 245), False
        case 2 | 3 | 45 | 48:
            return "clear", "windy", (17, 172), True
        case 51 | 53 | 55 | 56 | 57 | 61 | 63 | 65 | 80 | 81 | 82:
            return "rain", "rain", (12, 167), False
        case _:
            return "winter", "winter", (40, 175), False
        
condition, cloth, offset, cloud = get_weatherCode(weather['weathercode'])
friend_condition, friend_cloth, friend_offset, friend_cloud = get_weatherCode(friend_weather['weathercode'])


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

# Loading friend assets
friend_bg_img = load_image("background/", backgrounds[friend_sky][friend_condition])
friend_box_img = load_image("box/", box[friend_text_box])
friend_box_img.set_alpha(180)

if friend_cloud:
    friend_cloud_img = load_image("clouds/", clouds[friend_sky])

friend_cat_img = load_image("cats/", cats[cat_index])
friend_cloth_img = load_image("clothes/", clothes[friend_cloth])

friend_temp_text = temp_font.render(f"{int(friend_temperature)}°C", True, (255, 255, 255))
friend_status_text = status_font.render(friend_status, True, (255, 255, 255))

# Set up the game window
screen = pygame.display.set_mode((190*2, 360))
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

    # Friend's weather panel
    screen.blit(friend_bg_img, (190, 0))
    if friend_cloud:
        screen.blit(friend_cloud_img, (190, 30))
    screen.blit(friend_box_img, (190 + 10, 10))
    screen.blit(friend_temp_text, (190 + 20, 40))
    screen.blit(friend_status_text, (190 + 20, 30))
    screen.blit(friend_cat_img, (190 + 40, 210))
    screen.blit(friend_cloth_img, (190 + friend_offset[0], friend_offset[1]))

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
# button to change cat each panel(self/friend)