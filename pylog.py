import time

import math

class display_print:
    def __init__(self,width,height,blanks=" ",border=" "):
        self.width=width
        self.height=height
        self.blanks=blanks
        self.border=border
        self.window=[[self.border if w == 0 or w == self.width-1 or h == 0 or h == self.height-1 else self.blanks for w in range(self.width)] for h in range(self.height)]
        

    # draw a shape
    def draw_poly(self,x,y,width,height,symbol="."):
        # Loop of the height and width as indexs h and w
        for h in range(height):
            for w in range(width):
                # position added by the w and h
                yy=y+h
                xx=x+w
                # Check if the x or y is out of the screen
                out=(yy<0 or yy >= self.height or xx < 0 or xx >= self.width)
                # map onto display window if the coordinates are inside the window
                if not out:
                    self.window[int(yy)][int(xx)]=symbol
    def draw_line(self,P1,P2,symbol="."):
        # distance of the two points
        d=math.hypot(P2[0]-P1[0],P2[1]-P1[1])
        # starting point
        sx,sy=P1
        coords=[]
        # loop by the distance of the two points
        for n in range(int(d)):
            # map onto the display
            x,y=int(sx),int(sy)
            if x >= 0 and x < self.width-1 and y >= 0 and y < self.height-1:
                self.window[int(y)][int(x)]=symbol
                coords.append([int(x),int(y)])
            # angle of the points
            a=math.atan2(P2[0]-P1[0],P2[1]-P1[1])
            # line's length increases by the index of n
            sx=n*math.sin(a)+P1[0]
            sy=n*math.cos(a)+P1[1]
        # This is to avoid gaps
        for i, c in enumerate(coords):
            if i > 0 and i < len(coords):
                c1=1 if [c[0]+1,c[1]] in coords else 0
                c2=1 if [c[0]-1,c[1]] in coords else 0
                c3=1 if [c[0],c[1]+1] in coords else 0
                c4=1 if [c[0],c[1]-1] in coords else 0
                if c1+c2+c3+c4 < 2:
                    c1=1 if [c[0]+1,c[1]-1] in coords else 0
                    c2=1 if [c[0]+1,c[1]+1] in coords else 0
                    c3=1 if [c[0]-1,c[1]+1] in coords else 0
                    c4=1 if [c[0]-1,c[1]-1] in coords else 0
                    dx=P2[0]-P1[0]+1e-3
                    m=(P2[1]-P1[1])/dx
                    m=1 if m < 0 else -1

                    if c1 == 1:
                        self.window[c[1]-m][c[0]]=symbol
                    if c2 == 1:
                        self.window[c[1]-m][c[0]]=symbol
                    if c3 == 1:
                        self.window[c[1]+m][c[0]]=symbol
                    if c4==1:
                        self.window[c[1]+m][c[0]]=symbol
                    
    # Displays the window in the console
    def display(self, join_text=""):
        n=""
        for p in self.window:
            n+="".join(p)+"\n"

        print(n + join_text,end="\r")
    # refreshes screen
    def refresh(self):
        # loop through each point in the window to set as blanks
        for y in range(len(self.window)):
            for x in range(len(self.window[y])):
                self.window[y][x]=self.blanks
                self.window[0][x]=self.border
                self.window[self.height-1][x]=self.border
            self.window[y][0]=self.border
            self.window[y][self.width-1]=self.border
    # add a delay tick to avoid a jittery screen
    def tick(self,fps):
        time.sleep(1/fps)
