from datetime import timedelta
import dateutil.parser
from PIL import Image, ImageDraw

#https://stackoverflow.com/a/20792531
def rgb(minimum, maximum, value):
    minimum, maximum = float(minimum), float(maximum)
    ratio = 2 * (value-minimum) / (maximum - minimum)
    b = int(max(0, 255*(1 - ratio)))
    r = int(max(0, 255*(ratio - 1)))
    g = 255 - b - r
    return r, g, b

for file in ["sleep"]:
    data = open("../../data/processed/analysis/" + file + "_heatmap_minute.txt").read().strip().splitlines()
    data = [[float(j) for j in i.split(", ")] for i in data]

    x_scale, y_scale = 1, 1
    line_height = 1024
    w, h = 60*24*7, 1
    im_long = Image.new('RGB', (w, h), (255,255,255))
    px_long = im_long.load()

    for x in range(w):
        px_long[x, 0] = (rgb(0, 1, sum(data, [])[x]))

    im_long = im_long.resize((w*x_scale, h*line_height*y_scale), Image.NEAREST).crop((0,0, w*x_scale, h*line_height*y_scale))
    #im_long.show()
    im_long.save(file + "_heatmap_minute_long.png", "PNG")

    ################################################################

    x_scale, y_scale = 1, 60
    w, h = 60*24, 7
    im_cal = Image.new('RGB', (w, h), (255,255,255))
    px_cal = im_cal.load()

    for y in range(h):
        for x in range(w):
            px_cal[x, y] = (rgb(0, 1,data[y][x]))

    im_cal = im_cal.resize((w*x_scale, h*y_scale), Image.NEAREST).crop((0,0, w*x_scale, h*y_scale))
    #im_cal.show()
    im_cal.save(file + "_heatmap_minute_cal.png", "PNG")
