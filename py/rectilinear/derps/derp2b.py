
from PIL import Image
import math

# https://stackoverflow.com/a/20926435
def rect(r, theta):
    """theta in degrees

    returns tuple; (float, float); (x,y)
    """
    x = r * math.cos(math.radians(theta))
    y = r * math.sin(math.radians(theta))
    return x,y

def polar(x, y):
    """returns r, theta(degrees)
    """
    r = (x ** 2 + y ** 2) ** .5
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

im0 = Image.open("campus.png")
S = max(im0.size)
im = Image.new('RGB', (S, S), (255,255,255))
# isolated to left half?
im.paste(im0.rotate(90, expand=1).resize((im0.width//2, im0.height*2), Image.NEAREST), (S//8,0))
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
        r = rect(x0,y0)
        #print(x0, y0, p)
        #print(r)
        px[r[0]+S//2 if r[0]+S//2 < 1440 else 0,r[1]+S//2 if r[1]+S//2 < 1440 else 0] = px0[p]

#im.show()
im.save("derp2b.png", "PNG")