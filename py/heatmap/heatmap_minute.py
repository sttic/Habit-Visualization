from PIL import Image, ImageDraw
from colour import Color    # use colorsys instead (std lib)?

# TODO draw full base image (with hour/day indicators)
# TODO organize mess

# pure white has no colour bias to start from, leading to 'contamination'
palette = [[243,247,252], [54,139,202], [8,48,107]]
col = [Color(rgb=tuple([j/255 for j in i])) for i in palette]
density, weight = 1000, [0.5,0.5]   # weights must sum up to 1.0
grad = sum([list(col[i].range_to(col[i+1], round(density*weight[i]))) for i in range(len(palette)-1)], [])

def rgb(val):
    col = grad[round(val*(density-1))]
    return tuple([round(i*255) for i in [col.red, col.green, col.blue]])

for file in ["sleep"]:
    im_grad = Image.new('RGB', (density, 1), (255,255,255))
    px_grad = im_grad.load()

    for x in range(im_grad.width):
        px_grad[x, 0] = rgb(x/density)
    xs, ys = 1, 128
    im_grad = im_grad.resize((im_grad.width*xs, im_grad.height*ys)).crop((0,0,im_grad.width*xs, im_grad.height*ys))
    im_grad.save("gradient.png", "PNG")
    
    ################################################################
    
    data = open("../../data/processed/analysis/" + file + "_heatmap_minute.txt").read().strip().splitlines()
    data = [[float(j) for j in i.split(", ")] for i in data]

    x_scale, y_scale = 1, 1
    line_height = 1024
    w, h = 60*24*7, 1
    im_long = Image.new('RGB', (w, h), (255,255,255))
    px_long = im_long.load()

    for x in range(w):
        px_long[x, 0] = rgb(sum(data, [])[x])

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
            px_cal[x, y] = rgb(data[y][x])

    im_cal = im_cal.resize((w*x_scale, h*y_scale), Image.NEAREST).crop((0,0, w*x_scale, h*y_scale))
    #im_cal.show()
    im_cal.save(file + "_heatmap_minute_cal.png", "PNG")
