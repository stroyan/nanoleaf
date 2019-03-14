import PIL.ImageGrab
import math
import time
from nanoleaf import Aurora

backsplash = Aurora("nanoleaf", "gsFyJGvYGQzs818SsmBgn9eVyYe51WFg")
backsplash.on = True
info = backsplash.info
panel_list = []
for panel in info["panelLayout"]["layout"]["positionData"]:
    print(str(panel["panelId"])+"\t"+str(panel["x"])+"\t"+str(panel["y"]))
    x = panel["x"]
    y = panel["y"]
    angle = math.radians(60)
    new_x = math.floor((x * math.cos(angle - y * math.sin(angle))) / 65 + 2.5)
    new_y = math.floor((x * math.sin(angle + y * math.cos(angle))) / 172 + 0.75)
    panel_list.append({"panelId":str(panel["panelId"]),"x":new_x,"y":new_y})
effect = {
    "command": "display",
    "animType": "static",
    "loop": False
}
for t in range(20):
    im = PIL.ImageGrab.grab() 
    im.thumbnail([5,2])
    px = im.load()
    effect["animData"] = str(len(panel_list)) + " "
    for panel in panel_list:
        r, g, b = px[panel["x"],panel["y"]]
        effect["animData"] = effect["animData"] + "{} 1 {} {} {} 0 10 ".format(panel["panelId"], r, g, b)

    print(effect)
    backsplash.effect_set_raw(effect)
    time.sleep(1)