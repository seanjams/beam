from phue import Bridge
from sqlalchemy import desc

from db import LightStatus
from config import HUE_BRIDGE_IP, HUE_BRIDGE_USERNAME
from utils import convert_hex, todays_date, yesterdays_date


# Create Bridge
bridge = Bridge(ip=HUE_BRIDGE_IP, username=HUE_BRIDGE_USERNAME)

# color consts
BEAM_LIGHT_NAME = "Porch Beam"
KINGS_PURPLE = "#5A2D81"
WARM_YELLOW = "#efc070"

# Philips Hue helpers
def get_porch_beam():
    return bridge[BEAM_LIGHT_NAME]

def set_color(light, hex_code):
    try:
        if light.on:
            light.xy = convert_hex(hex_code)
            return True
    except Exception:
        pass    
    return False

def save_current_light_status():
    light = get_porch_beam()
    LightStatus(
        name=light.name,
        on=light.on,
        hue=light.hue,
        brightness=light.brightness,
        saturation=light.saturation,
    ).save()

def light_the_beam():
    # turn light Kings purple
    light = get_porch_beam()
    if not light.on:
        light.on = True
    set_color(light, KINGS_PURPLE)

def reset_beam():
    # turn back to whatever it was yesterday, or do nothing
    light = get_porch_beam()
    saved_configuration = LightStatus.get_last_saved()
    if saved_configuration:
        light.on = saved_configuration.on
        light.brightness = saved_configuration.brightness
        light.saturation = saved_configuration.saturation
        light.hue = saved_configuration.hue        
    # else:
    #     set_color(light, WARM_YELLOW)


