from math import *
from keyboard import is_pressed
import pylog
# TileSize
TS=20
# MAP of 0s and 1s
# 1 = wall
# 0 = Nothing
MAP=[
    [1,1,1,1,1,1,1,1,1],
    [1,0,0,1,0,1,0,0,1],
    [1,0,1,1,0,1,1,0,1],
    [1,0,0,1,0,0,1,0,1],
    [1,0,0,0,0,0,0,0,1],
    [1,0,1,0,0,0,1,1,1],
    [1,0,1,1,1,0,1,0,1],
    [1,0,0,0,1,0,0,0,1],
    [1,1,1,1,1,1,1,1,1]
]
px,py=[len(MAP[0])/2*TS+TS/2,len(MAP)/2*TS+TS/2]
# player angle
t=0
# Field of View
FOV=60
# player's velocity
v=0
# Display window width and height
w,h=100,40
# Render distance
R=w
# Scaling
s=w/FOV

fps=60
win=pylog.display_print(w,h,border=".")
run=True
while run:
    # Player movements and rotations
    if is_pressed("left"):
        t-=.1
    elif is_pressed("right"):
        t+=.1
    if is_pressed("up"):
        v=1
    elif is_pressed("down"):
        v=-1
    else:
        v=0
    # Avoid player colliding with walls
    if v!=0:
        vx=px+sin(t)*v
        vy=py+cos(t)*v
        nx,ny=[int(vx/TS),int(vy/TS)]
        if nx >= 0 and nx < len(MAP[0]) and ny >= 0 and ny < len(MAP):
            if MAP[ny][nx]==0:
                px=vx
                py=vy
    for ray in range(FOV):
        for depth in range(R):
            # angle of ray
            angle=t+radians(ray)-radians(FOV/2)
            # ray's coordinates
            tx=depth*sin(angle)+px
            ty=depth*cos(angle)+py
            nx,ny=int(tx/TS),int(ty/TS)
            # validation for if the ray is inside the MAP
            if nx >= 0 and nx < len(MAP[0]) and ny >= 0 and ny < len(MAP):
                # Detect if ray collides with wall
                if MAP[ny][nx] == 1:
                    a=atan2(tx-px,ty-py)
                    # distance calculation for fisheye effect avoidance
                    d=depth*cos(t-a)
                    # wall's height
                    wh=h*16/(d+.001)
                    x1=int(s*ray)
                    x2=int(s)+1
                    y1=int(h/2-wh/2)
                    y2=int(wh)
                    # symbols used for the wall based on the distance
                    characters=list("@$Kɴnl!ⁿ',.|")
                    # calculation for what symbol to use (Bigger the symbol the closer the player is)
                    c=characters[0 if int(len(characters)/R*depth)-1 < 0 else int(len(characters)/R*depth)-1]
                    # Draw wall
                    win.draw_poly(x1,y1,x2,y2,c)
                    break
    # display's window in console and refreshes it by the tick speed
    win.display()
    win.refresh()
    win.tick(fps)
