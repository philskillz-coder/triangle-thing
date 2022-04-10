import math
from PIL import Image, ImageDraw
from random import choice
from typing import Tuple

COORDS = Tuple[Tuple[int, int], Tuple[int, int]]
POINT = Tuple[int, int]

def calc_edge(point: POINT, scale: int=1) -> COORDS:
    x, y = point
    return (
        (x - 15*scale,      y - 15*scale),
        (x + 15*scale,      y + 15*scale)
    )

SCALE = 5 # the factor to multiply with - should meet the following condition: (HEIGHT/SCALE)<850
TRIANGLE_SIZE = 400

# HEIGHT and WIDTH should be the same!
HEIGHT = 4096 # use powers of 2. should be a maximum of 16384
WIDTH = 4096 # use powers of 2. should be a maximum of 16384

# color format: 
# first 3 ints: the color in rgb
# last int: opacity
BACKGROUND_COLOR = (0, 0, 0, 255) # black
TRIANGLE_COLOR = (255, 255, 255, 255) # white

img = Image.new("RGB", (WIDTH, HEIGHT), BACKGROUND_COLOR)
draw = ImageDraw.Draw(img)

centerx = WIDTH / 2
centery = HEIGHT / 2

hypotenuse = abs(math.cos(60) * TRIANGLE_SIZE) # calculate triangle height (Side BC)
adjacent = (TRIANGLE_SIZE**2 - hypotenuse**2)**0.5 # calculate triangle base (Side AB)

hypotenuse *= SCALE # scale the side up
adjacent *= SCALE # scale the side up

p1 = (centerx - hypotenuse,     centery + adjacent) # Point A of the triangle
p2 = (centerx + hypotenuse,     centery + adjacent) # Point B of the triangle
p3 = (centerx,                  centery - TRIANGLE_SIZE * SCALE) # Point C of the triangle
points = [p1, p2, p3] # all points (needed later)


draw.line(
    (p1, p2),
    fill=(255, 255, 255, 255),
    width=4
) # draw triangle side AB

draw.line(
    (p2, p3),
    fill=(255, 255, 255, 255),
    width=4
) # draw triangle side BC

draw.line(
    (p3, p1),
    fill=(255, 255, 255, 255),
    width=4
) # draw triangle side CA


point: POINT = (
    centerx, centery
) # the point to start with


POINT_COUNT = 15000 # how many points to draw. should meet the following condition: (SCALE*TRIANGLE_SIZE)/1500>0.1
POINT_SCALE = 0.2 # you just have to get a feeling for this.
POINT_COLOR = (255, 0, 0, 255) # red, same color schema as above

for i in range(POINT_COUNT):
    x1, y1 = choice(points) # x and y coords of a random triangle side point
    x2, y2 = point # x and y coords of the last drewn point

    midx = (x1+x2)/2 # calculate x center between x1 and x2
    midy = (y1+y2)/2 # calculate y center between y1 and y2

    point = (midx, midy) # the midpoint (this is where we make the new point)

    draw.ellipse(
        calc_edge(point, POINT_SCALE), # make the point coords to a pair of coords
        fill=(255, 0, 0, 255)
    ) # draw the point



img.show() # show the image
img.save("triangle.png") # save it