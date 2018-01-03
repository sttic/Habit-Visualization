from PIL import Image, ImageDraw
from colour import Color    # use colorsys instead (std lib)?

# TODO draw full base image (with hour/day indicators)

def rgb(val):
    col = grad[round(val*(density-1))]
    return tuple([round(i*255) for i in [col.red, col.green, col.blue]])

def gradient(x_scale, y_scale):
    im = Image.new('RGB', (density, 1), (255,255,255))
    px = im.load()

    for x in range(im.width):
        px[x, 0] = rgb(x/density)

    return im.resize((im.width*x_scale, im.height*y_scale), Image.NEAREST)

def spectrum(data, x_scale, y_scale):
    im = Image.new('RGB', (60*24*7, 1), (255,255,255))
    px = im.load()

    for x in range(im.width):
        px[x, 0] = rgb(sum(data, [])[x])

    return im.resize((im.width*x_scale, im.height*y_scale), Image.NEAREST)

def cal(data, x_scale, y_scale):
    im = Image.new('RGB', (60*24, 7), (255,255,255))
    px = im.load()

    for y in range(im.height):
        for x in range(im.width):
            px[x, y] = rgb(data[y][x])

    return im.resize((im.width*x_scale, im.height*y_scale), Image.NEAREST)

# pure white has no colour bias to start from, leading to 'contamination'
palette = [[243,247,252], [54,139,202], [8,48,107]]
col = [Color(rgb=tuple([j/255 for j in i])) for i in palette]
density, weight = 1000, [0.5,0.5]   # weights must sum up to 1.0
grad = sum([list(col[i].range_to(col[i+1], round(density*weight[i]))) for i in range(len(palette)-1)], [])

for file in ["sleep", "campus", "transit"]:
    data = open("../../data/processed/analysis/" + file + "_heatmap_minute.txt").read().strip().splitlines()
    data = [[float(j) for j in i.split(", ")] for i in data]

    spectrum(data, 1, 1024).save(file + "_heatmap_minute_spectrum.png", "PNG")
    cal(data, 1, 60).save(file + "_heatmap_minute_cal.png", "PNG")

gradient(1, 128).save("gradient.png", "PNG")
