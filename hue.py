from phue import Bridge

from config import HUE_BRIDGE_IP, HUE_BRIDGE_USERNAME

# def random_hex():
#     r = random.randint(0,255)
#     g = random.randint(0,255)
#     b = random.randint(0,255)
#     hex = "#%02X%02X%02X" % (r, g, b)
#     return hex

# This is only scanning R and G? Need better solution
def convert_hex(hex_code):
    if hex_code.startswith("#"):
        hex_code = hex_code[1:]
    R = int(hex_code[:2],16)
    G = int(hex_code[2:4],16)
    B = int(hex_code[4:6],16)

    total = R + G + B

    if R == 0:
        firstPos = 0
    else:
        firstPos = R / total
    
    if G == 0:
        secondPos = 0
    else:
        secondPos = G / total

    return [firstPos, secondPos]

# cache this
def get_bridge():
    bridge = Bridge(ip=HUE_BRIDGE_IP, username=HUE_BRIDGE_USERNAME)
    bridge.connect()
    return bridge

def set_color(bridge, light_id, hex_code):
    color_coords = convert_hex(hex_code)
    bridge.set_light(light_id, 'xy', color_coords)

def light_the_beam(light_id=None):
    bridge = get_bridge()
    hue = "#990099"
    set_color(bridge, 1, hue)
    set_color(bridge, 2, hue)
    set_color(bridge, 3, hue)

def reset_beam(light_id=None):
    bridge = get_bridge()
    hue = "#eedc9c"
    set_color(bridge, 1, hue)
    set_color(bridge, 2, hue)
    set_color(bridge, 3, hue)
