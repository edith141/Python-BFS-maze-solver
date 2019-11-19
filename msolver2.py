import cv2
import numpy as np
import threading
import colorsys


class Point(object):

    def __init__(self, x=0, y=0):
        self.x = x
        self.y = y

    def __add__(self, other):
        return Point(self.x + other.x, self.y + other.y)

    def __eq__(self, other):
        return self.x == other.x and self.y == other.y

#rw - width of the start & end points (rect) 
rw = 2
# p - to keep count of points. 0/1/2
p = 0
start = Point()
end = Point()

#4 directions to traverse each cell/point. Up,down,left,rt
dir4 = [Point(0, -1), Point(0, 1), Point(1, 0), Point(-1, 0)]

# BFS 
def BFS(s, e):

    global img, h, w
    const = 8500
    found = False
# q - queue
    q = []
# v - visited nodes list
    v = [[0 for j in range(w)] for i in range(h)]
# parent - parents of each point/node
    parent = [[Point() for j in range(w)] for i in range(h)]

    q.append(s)
    v[s.y][s.x] = 1
    while len(q) > 0:
        p = q.pop(0)
        for d in dir4:
            cell = p + d
            if (cell.x >= 0 and cell.x < w and cell.y >= 0 and cell.y < h and v[cell.y][cell.x] == 0 and
                    (img[cell.y][cell.x][0] != 0 or img[cell.y][cell.x][1] != 0 or img[cell.y][cell.x][2] != 0)):
                q.append(cell)
                v[cell.y][cell.x] = v[p.y][p.x] + 1  # Later

                img[cell.y][cell.x] = list(reversed(
                    [i * 255 for i in colorsys.hsv_to_rgb(v[cell.y][cell.x] / const, 1, 1)])
                )
                parent[cell.y][cell.x] = p
                if cell == e:
                    found = True
                    del q[:]
                    break

    path = []
    if found:
        p = e
        while p != s:
            path.append(p)
            p = parent[p.y][p.x]
# the nodes seq to get to the target node
        path.append(p)
# reverse it to get it in correct order from start to end
        path.reverse()
# draw a line (continuous rects) to highlight the path
        for p in path:
            cv2.rectangle(img, (p.x - 1, p.y - 1),
                          (p.x + 1, p.y + 1), (255, 255, 255), -1)
        print("Path Found")
    else:
        print("Path Not Found")


def mouse_event(event, pX, pY, flags, param):
#mark the start and end points 
    global img, start, end, p

    if event == cv2.EVENT_LBUTTONUP:
        if p == 0:
            cv2.rectangle(img, (pX - rw, pY - rw),
                          (pX + rw, pY + rw), (0, 0, 255), -1)
            start = Point(pX, pY)
            print("start = ", start.x, start.y)
            p += 1
        elif p == 1:
            cv2.rectangle(img, (pX - rw, pY - rw),
                          (pX + rw, pY + rw), (0, 200, 50), -1)
            end = Point(pX, pY)
            print("end = ", end.x, end.y)
            p += 1


def disp():
#disp img in diff thread 
    global img
    cv2.imshow("Image", img)
    cv2.setMouseCallback('Image', mouse_event)
    while True:
        cv2.imshow("Image", img)
        cv2.waitKey(2)


img = cv2.imread("maze.jpg", cv2.IMREAD_GRAYSCALE)
_, img = cv2.threshold(img, 120, 255, cv2.THRESH_BINARY)
img = cv2.cvtColor(img, cv2.COLOR_GRAY2BGR)
h, w = img.shape[:2]

print("Select start and end points : ")


t = threading.Thread(target=disp, args=())
t.daemon = True
t.start()

while p < 2:
    pass

BFS(start, end)

cv2.waitKey(0)
