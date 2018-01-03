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

im0 = Image.open("../../rectilinear/campus.png")
S = max(im0.size)
im = Image.new('RGB', (S, S), (255,255,255))
# isolated to left half?
im.paste(im0.rotate(90, expand=1).resize((im0.width, im0.height*2), Image.NEAREST), (0,0))
scale = 1
im0 = im.resize((S*scale, S*scale), Image.NEAREST)
#im0.show()
im = Image.new('RGB', (S*scale, S*scale), (255,255,255))

px0 = im0.load()
px = im.load()

step = 1
for x in range(0,S,step):
    for y in range(0,S,step):
        x0, y0 = x-S//2, -y+S//2
        #print(x, y, "|", polar(x, y), sep="\t")
        p = polar(x0, y0)
        #print(x0, y0, p)
        try:
            # theta values 360 and 630 instead of 180 and 270 respectively
            if x0 == 0 and y0 < 0:
                px[p[0],(p[1]-360)*(S/360)] = px0[x,y]
            elif y0 == 0 and x0 < 0:
                px[p[0],(p[1]-180)*(S/360)] = px0[x,y]
            else:
                px[p[0],p[1]*(S/360)] = px0[x,y]
        except:
            print(x, y, x0, y0, p, p[1]*(S/360), sep="\t")
            pass


#im.show()
im.save("derp3.png", "PNG")

