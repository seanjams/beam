import math
from phue import Bridge

from config import HUE_BRIDGE_IP, HUE_BRIDGE_USERNAME

# Create Bridge
bridge = Bridge(ip=HUE_BRIDGE_IP, username=HUE_BRIDGE_USERNAME)

# def random_hex():
#     r = random.randint(0,255)
#     g = random.randint(0,255)
#     b = random.randint(0,255)
#     hex = "#%02X%02X%02X" % (r, g, b)
#     return hex

# https://gist.github.com/error454/6b94c46d1f7512ffe5ee
def enhance_color(normalized):
    if normalized > 0.04045:
        return math.pow( (normalized + 0.055) / (1.0 + 0.055), 2.4)
    else:
        return normalized / 12.92

def convert_hex(hex_code):
    if hex_code.startswith("#"):
        hex_code = hex_code[1:]
    r = int(hex_code[:2],16)
    g = int(hex_code[2:4],16)
    b = int(hex_code[4:6],16)

    r_norm = r / 255.0
    g_norm = g / 255.0
    b_norm = b / 255.0

    r_final = enhance_color(r_norm)
    g_final = enhance_color(g_norm)
    b_final = enhance_color(b_norm)
    
    x = r_final * 0.649926 + g_final * 0.103455 + b_final * 0.197109
    y = r_final * 0.234327 + g_final * 0.743075 + b_final * 0.022598
    z = r_final * 0.000000 + g_final * 0.053077 + b_final * 1.035763

    if x + y + z == 0:
        return (0,0)
    else:
        x_final = x / (x + y + z)
        y_final = y / (x + y + z)
    
        return (x_final, y_final)

def set_color(bridge, light_id, hex_code):
    color_coords = convert_hex(hex_code)
    bridge.set_light(light_id, 'bri', 200)
    bridge.set_light(light_id, 'xy', color_coords)

def light_the_beam(light_id=None):
    hue = "#660066"  # purple
    # for light_id in (1, 2, 3):
    for light_id in (1, 2):
        set_color(bridge, light_id, hue)

def reset_beam(light_id=None):
    hue = "#efc070"  # warm yellow
    # for light_id in (1, 2, 3):
    for light_id in (1, 2):
        set_color(bridge, light_id, hue)
