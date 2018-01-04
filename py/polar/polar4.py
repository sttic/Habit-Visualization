from PIL import Image
import math

def polar(x, y):
    r = (x**2 + y**2)**0.5
    theta = 0
    if y == 0:
        theta = 180 if x < 0 else 0
    elif x == 0:
        theta = 90 if y > 0 else 270
    else:
        theta = math.degrees(math.atan(y/x))

    if x < 0:
        theta += 180
    elif y < 0:
        theta += 360
        
    return r, theta

im0 = Image.open("../heatmap/sleep_heatmap_minute_cal.png")
# https://stackoverflow.com/a/14178717
#im0 = im0.transform((im0.width, im0.height + round(im0.height/7)), Image.AFFINE, (1, 0, 0, -0.042, 1, 0), Image.BICUBIC)

extra  = im0.height/7
im1 = Image.new('RGBA', (im0.width, im0.height + round(extra)))
px0, px1 = im0.load(), im1.load()
for x in range(im0.width):
    for y in range(im0.height):
        px1[x, y + extra - (extra/im0.width)*(im0.width-x)] = px0[x, y]
im0 = im1
#im0.show()

S = max(im1.size)
im = Image.new('RGB', (S, S), (255,)*3)
# isolated to left half?
im0 = im0.rotate(-90, expand=1).resize((round(S/3), S), Image.NEAREST)
im.paste(im0, (round(im1.width/6), 0), mask=im0)
#im.show()

im0 = im
im = Image.new('RGB', (S, S))

px, px0 = im.load(), im0.load()

step = 1
for x in range(0,S,step):
    for y in range(0,S,step):
        x0, y0 = x-S//2, -y+S//2
        #print(x, y, "|", polar(x, y), sep="\t")
        p = polar(x0, y0)
        #print(x0, y0, p)
        try:
            px[x,y] = px0[p[0],p[1]*(S/360)]
        except:
            #print(x, y, x0, y0, p, p[1]*(S/360), sep="\t")
            # theta values 360 and 630 instead of 180 and 270 respectively
            if y0 == 0:
                px[x,y] = px0[p[0],(p[1]-180)*(S/360)]
            elif x0 == 0:
                px[x,y] = px0[p[0],(p[1]-360)*(S/360)]

im = im.transpose(Image.FLIP_LEFT_RIGHT).rotate(-90)
#im.show()
im.save("WIP4_spiral.png", "PNG")

