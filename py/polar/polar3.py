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
        
    return theta, r

im0 = Image.open("../rectilinear/campus.png")
S = max(im0.size)
im = Image.new('RGB', (S, S), (255,255,255))
im.paste(im0) # .resize((S, int(S/1.42)))
im0 = im
im0.show()
im = Image.new('RGB', (S, S), (0,0,0))

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
            if x0 == 0 and y0 < 0:
                px[x, y] = px0[(p[0]-360)*((S-1)/360),p[1]*((S-1)/(2*(S//2)**2)**0.5)]
            elif y0 == 0 and x0 < 0:
                px[x, y] = px0[(p[0]-180)*((S-1)/360),p[1]*((S-1)/(2*(S//2)**2)**0.5)]
            else:
                px[x, y] = px0[p[0]*((S-1)/360),p[1]*((S-1)/(2*(S//2)**2)**0.5)]
        except:
            print(x0, y0, "|", p, (p[0]*((S-1)/360),p[1]*((S-1)/(2*(S//2)**2)**0.5)), sep="\t")
im.show()
#im.save("WIP_polar3.png", "PNG")

