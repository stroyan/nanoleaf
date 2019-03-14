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
    unset_color=(-1,-1,-1)
    panel_list.append({"panelId":str(panel["panelId"]),"x":new_x,"y":new_y,"color":unset_color})
effect = {
    "command": "display",
    "animType": "static",
    "loop": False
}
for t in range(20):
    start_time=time.time()
    im = PIL.ImageGrab.grab() 
    im.thumbnail([5,2])
    px = im.load()
    panel_strings = []
    effect["animData"] = ""
    for panel in panel_list:
        color = px[panel["x"],panel["y"]]
        if (color != panel["color"]):
            panel["color"] = color
            r, g, b = color
            panel_strings.append("{} 1 {} {} {} 0 10 ".format(panel["panelId"], r, g, b))

    if(len(panel_strings) > 0):
        effect["animData"] = str(len(panel_strings)) + " " + " ".join(panel_strings)
        print(effect)
        backsplash.effect_set_raw(effect)

    print("sleep after {} seconds".format(time.time() - start_time))
    time.sleep(1)