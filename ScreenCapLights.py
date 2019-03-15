import PIL.ImageGrab
import math
import time
import colorsys
from nanoleaf import Aurora

backsplash = Aurora("nanoleaf", "gsFyJGvYGQzs818SsmBgn9eVyYe51WFg")
backsplash.on = True
info = backsplash.info
panel_list = []
for panel in info["panelLayout"]["layout"]["positionData"]:
    #print(str(panel["panelId"])+"\t"+str(panel["x"])+"\t"+str(panel["y"]))
    x = panel["x"]
    y = panel["y"]
    angle = math.radians(60)
    new_x = math.floor((x * math.cos(angle) + y * math.sin(angle)) / 75 + 2.5)
    new_y = 1-math.floor((-x * math.sin(angle) + y * math.cos(angle)) / 172 + 0.75)
    unset_color=(-1,-1,-1)
    panel_list.append({"panelId":str(panel["panelId"]),"x":new_x,"y":new_y,"color":unset_color})
effect = {
    "command": "display",
    "animType": "static",
    "loop": False
}
while True:
    im = PIL.ImageGrab.grab() 
    im.thumbnail([5,2])
    px = im.load()
    panel_strings = []
    for panel in panel_list:
        color = px[panel["x"],panel["y"]]
        if (color != panel["color"]):
            panel["color"] = color
            r, g, b = color            
            hsv = colorsys.rgb_to_hsv(r/255, g/255, b/255)
            h, s, v = hsv
            s = min(1, 1.5*s)
            rgb = colorsys.hsv_to_rgb(h, s, v)
            r, g, b = rgb
            r = math.floor(r*255)
            g = math.floor(g*255)
            b = math.floor(b*255)
            panel_strings.append("{} 1 {} {} {} 0 10 ".format(panel["panelId"], r, g, b))

    if(len(panel_strings) > 0):
        effect["animData"] = str(len(panel_strings)) + " " + " ".join(panel_strings)
        #print(effect)
        backsplash.effect_set_raw(effect)
    #time.sleep(1)