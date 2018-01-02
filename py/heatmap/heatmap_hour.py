from PIL import Image, ImageDraw
from colour import Color    # use colorsys instead (std lib)?

# TODO organize mess

# pure white has no colour bias to start from, leading to 'contamination'
palette = [[243,247,252], [54,139,202], [8,48,107]]
col = [Color(rgb=tuple([j/255 for j in i])) for i in palette]
density, weight = 1000, [0.5,0.5]   # weights must sum up to 1.0
grad = sum([list(col[i].range_to(col[i+1], round(density*weight[i]))) for i in range(len(palette)-1)], [])

def rgb(val):
    col = grad[round(val*(density-1))]
    return tuple([round(i*255) for i in [col.red, col.green, col.blue]])

for file in ["sleep", "campus", "transit"]:
    data = open("../../data/processed/analysis/" + file + "_heatmap_hour.txt").read().strip().splitlines()
    data = [[float(j) for j in i.split(", ")] for i in data]
    
    x_scale, y_scale = 64, 64
    w, h = 24, 7
    im_cal = Image.new('RGB', (w, h), (255,255,255))
    px_cal = im_cal.load()

    for y in range(h):
        for x in range(w):
            px_cal[x, y] = rgb(data[y][x])

    new_size = (w*x_scale, h*y_scale)
    im_cal = im_cal.resize(new_size, Image.NEAREST).crop(((0,0)+new_size))
    #im_cal.show()
    im_cal.save(file + "_heatmap_hour_cal.png", "PNG")
