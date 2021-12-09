from PIL import Image, ImageColor,ImageDraw
from random import randint
from math import cos, sin, pi
import math
import heapq


class Matrix():
    def __init__(self):
        self.height = 700
        self.width = 1000
        self.image = Image.new('RGBA', (self.width, self.height), 'white')
        self.draw = ImageDraw.Draw(self.image)
        self.im = Image.open("download.png").convert("RGB")
        self.weight = 1
    
    def get_user_input(self):

        self.matrix = [list(map(int, input().split()))]
        for x in range(len(self.matrix[0])-1):
            self.matrix.append(list(map(int, input().split())))
        self.cost = list(map(int, input().split())) 
        return self.matrix

    def twod_oned(self,x,y):
        return self.im.width*y +x

    
    def transform(self):
        self.graph = []
        for x in range(len(self.matrix)):
            node = []
            for y in range(len(self.matrix[x])):
                if self.matrix[x][y]:
                    node.append(y)
            self.graph.append(node)
        return self.graph
        
    def new_transform(self):  
        self.graph = []
        for x in range(self.im.width):
            for y in range(self.im.height):
                node = {"cost":0,"neighbors":[]}
                for b in self.im.getpixel((x,y)):
                    node["cost"]+=b
                self.graph.append(node)
                node["neighbors"].append(self.twod_oned(x+1,y))
                node["neighbors"].append(self.twod_oned(x-1,y))
                node["neighbors"].append(self.twod_oned(x,y+1))
                node["neighbors"].append(self.twod_oned(x,y-1))
        return self.graph


    def find_way(self, start, stop):
        is_route_exist = False
        def _find_way_(way = [start]):
            nonlocal start, stop, is_route_exist

            for edge in self.graph[way[-1]]:
                if edge in way:
                    continue
                if edge == stop:
                    is_route_exist = True
                    
                _find_way_(way + [edge])
        _find_way_()
        return is_route_exist

    def find_way_best(self, start, stop):
        shortest_route = None
        def _find_way_(way = [start]):
            nonlocal start, stop, shortest_route
            if way[-1] == stop:
                if not shortest_route: shortest_route = way
                if len(shortest_route) > len(way): shortest_route = way
            for edge in self.graph[way[-1]]:
                if edge in way:
                    continue  
                _find_way_(way + [edge])
        _find_way_()
        return shortest_route


    def create_points(self):
        len_graph = len(self.graph)
        dot_angle = 2*pi / len_graph
        self.cord = []
        for x in range(len(self.graph)):
            self.cord.append((cos(dot_angle*x) * self.width // 4 + self.width / 2,sin(dot_angle*x) * self.height // 4 + self.height / 2))
        return self.cord


    def create_random_points(self):
        while len(self.cord) < len(self.graph):
            x,y = randint(0,1000),randint(0,1000)
            self.cord.add((x,y))
        self.cord = list(self.cord) 
        return self.cord


    
    def draw_graph(self):
        for point  in self.cord: 
            self.draw.ellipse((point[0] - 5,point[1] - 5,point[0] + 5,point[1] + 5), fill = "red")
        return self.cord

    
    def draw_line(self):
        for node in range(len(self.graph)):
            for target in self.graph[node]:
                self.arrowedLine(self.cord[node],self.cord[target],color = ImageColor.getrgb("pink"), width=3)   


    def arrowedLine(self, ptA, ptB, width=1, color=(0,255,0),len_arrow=0.90,width_arrow=5):
        self.draw.line((ptA,ptB), width=width, fill=color)

        
        x0, y0 = ptA
        x1, y1 = ptB
        xb = len_arrow*(x1-x0)+x0
        yb = len_arrow*(y1-y0)+y0

        if x0==x1:
           vtx0 = (xb-width_arrow, yb)
           vtx1 = (xb+width_arrow, yb)

        elif y0==y1:
           vtx0 = (xb, yb+width_arrow)
           vtx1 = (xb, yb-width_arrow)
        else:
           alpha = math.atan2(y1-y0,x1-x0)-math.pi/2
           a = width_arrow* 2 *math.cos(alpha)
           b = width_arrow* 2 *math.sin(alpha)
           vtx0 = (xb+a, yb+b)
           vtx1 = (xb-a, yb-b)

        self.draw.polygon([vtx0, vtx1, ptB], fill=color)


    
    def draw_route(self,route):    
        for i in range(len(route)-1): 
            self.arrowedLine(self.cord[route[i]],self.cord[route[i+1]],color = ImageColor.getrgb("blue"), width=3)

    def oned_twod(self,x):
        return x % self.im.width, x // self.im.width
    
    def new_draw_route(self,route):
        for dot in route:
            self.im.putpixel(self.oned_twod(dot), ImageColor.getrgb("red"))
        print(route)
        
    
    def dejikstra(self,start,stop):
        heap = []
        heapq.heappush(heap, (0,start))
        dist = [float("inf") for x in self.graph]
        dist[start] = 0
        dirrection = [0 for x in self.graph]
        while heap:
            distance, edge  = heapq.heappop(heap)

            for vertix in self.graph[edge]:
                if dist[vertix] > distance + self.cost[vertix]:
                    dist[vertix] = distance + self.cost[vertix]
                    dirrection[vertix] = edge
                    heapq.heappush(heap,(distance + self.cost[vertix],vertix))
            if edge == stop:
                break
            
        current_vertix = stop
        way = [current_vertix]
        
        while current_vertix != start:
            current_vertix = dirrection[current_vertix]
            way.append(current_vertix)
        return way[::-1] 



    def new_dejikstra(self,start,stop):
        heap = []
        heapq.heappush(heap, (0,start))
        dist = [float("inf") for x in self.graph]
        dist[start] = 0
        dirrection = [0 for x in self.graph]
        while heap:
            distance, edge  = heapq.heappop(heap)

            for vertix in self.graph[edge]["neighbors"]:
                try:
                    new_distance = distance + self.graph[vertix]["cost"]
                except: 
                    continue
                if dist[vertix] > new_distance:
                    dist[vertix] = new_distance
                    dirrection[vertix] = edge
                    heapq.heappush(heap,(new_distance,vertix))
            if edge == stop:
                break
            
        current_vertix = stop
        way = [current_vertix]
        
        while current_vertix != start:
            current_vertix = dirrection[current_vertix]
            way.append(current_vertix)
        return way[::-1] 


if __name__ == '__main__':
    matrix = Matrix()
    matrix.new_transform()
    route = matrix.new_dejikstra(randint(0, matrix.im.width*matrix.im.height),randint(0, matrix.im.width*matrix.im.height))
    matrix.new_draw_route(route)
    matrix.im.show()
    
    #Напиши функцию которая сможет отрисовать произвольный маршрут в графе, принимет маршрут и точки
    # Нарисуй на графе первый попавшийся маршрут и кратчайший