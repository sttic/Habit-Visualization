from datetime import timedelta
import dateutil.parser
from PIL import Image, ImageDraw

data = open("../data/original/on_campus_tracker.txt").read().strip().splitlines()
for i in range(len(data)):
    if data[i].find("(") > 0:
        data[i] = data[i][:data[i].find("(")] + data[i][data[i].find(")")+1:]
data = [[dateutil.parser.parse(j) for j in i.split(", ")] for i in data]

step = timedelta(minutes=1)
time, end = data[0][0].replace(hour=0, minute=0), data[-1][1].replace(hour=23, minute=59)
duration = (end - time).days

line_height = 8
x_scale, y_scale = 1, 1
width, height = 24*60, (duration+1)*line_height

im = Image.new('RGB', (width, height), (255,255,255))
draw, px = ImageDraw.Draw(im), im.load()

i, instance = 0, data[0]
while time != end:
    if (time - instance[0]).total_seconds() >= 0 and (time - instance[1]).total_seconds() < 0:
        color, shade = [(68,140,193),(58,134,189)], [(36,103,162),(32,95,154)]
    else:
        color, shade = [(229,229,229),(225,225,225)], [(220,220,220),(215,215,215)]
        if (time - instance[1]).total_seconds() >= 0 and i < len(data)-1:
            i += 1
            instance = data[i]

    x, y = time.hour*60 + time.minute, -(end - time).days + duration
    draw.line((x, y*line_height, x, y*line_height + line_height - 1), fill=color[time.hour%2])
    px[x, y*line_height + line_height - 1] = shade[time.hour%2]

    time = time + step

im.resize((width*x_scale, height*y_scale), Image.NEAREST).crop((0,0,width*x_scale,height*y_scale)).save("campus.png", "PNG")
