import matplotlib.pyplot as plt
import numpy as np
import time
import matplotlib.animation as animation
from bfs import bfs
from dfs import dfs
from gbfs import gbfs
from aStar import aStar
from utils import *
from grid import *

def enclosed_points(points):
    edges = [(points[i], points[(i + 1) % len(points)]) for i in range(len(points))]
    min_x = min(x for x, y in points)
    max_x = max(x for x, y in points)
    min_y = min(y for x, y in points)
    max_y = max(y for x, y in points)
    enclosed = []
    for x in range(min_x, max_x + 1):
        for y in range(min_y, max_y + 1):
            inside = False
            on_edge = False
            for (x1, y1), (x2, y2) in edges:
                if y1 == y2:
                    continue
                if y1 < y2:
                    if y1 <= y <= y2 and x <= x1 + (x2 - x1) * (y - y1) / (y2 - y1):
                        if x == x1 + (x2 - x1) * (y - y1) / (y2 - y1):
                            on_edge = True
                        else:
                            inside = not inside
                else:
                    if y2 <= y <= y1 and x <= x2 + (x1 - x2) * (y - y2) / (y1 - y2):
                        if x == x2 + (x1 - x2) * (y - y2) / (y1 - y2):
                            on_edge = True
                        else:
                            inside = not inside
            if inside or on_edge:
                enclosed.append((x, y))
    return enclosed


def gen_polygons(worldfilepath):
    polygons = []
    edges=[]
    with open(worldfilepath, "r") as f:
        lines = f.readlines()
        lines = [line[:-1] for line in lines]
        for line in lines:
            points=[]
            polygon = []
            pts = line.split(';')
            for pt in pts:
                xy = pt.split(',')
                points.append((int(xy[0]),int(xy[1])))
                polygon.append(Point(int(xy[0]), int(xy[1])))
            polygons.append(polygon)
            
            enclosed = enclosed_points(points)
            print(points,len(enclosed))
            enclosed+=points
            
            edges.append(enclosed)
    return polygons,edges

def saveImage(source,dest,res_path,name,epolygons,tpolygons):
    fig, ax = draw_board()
    draw_grids(ax)
    draw_source(ax, source.x, source.y)  # source point
    draw_dest(ax, dest.x, dest.y)  # destination point
    # Draw enclosure polygons
    for polygon in epolygons:
        for p in polygon:
            draw_point(ax, p.x, p.y)
    for polygon in epolygons:
        for i in range(0, len(polygon)):
            draw_line(ax, [polygon[i].x, polygon[(i+1)%len(polygon)].x], [polygon[i].y, polygon[(i+1)%len(polygon)].y])
    
    # Draw turf polygons
    for polygon in tpolygons:
        for p in polygon:
            draw_green_point(ax, p.x, p.y)
    for polygon in tpolygons:
        for i in range(0, len(polygon)):
            draw_green_line(ax, [polygon[i].x, polygon[(i+1)%len(polygon)].x], [polygon[i].y, polygon[(i+1)%len(polygon)].y])
            
    for i in range(len(res_path)-1):
        draw_result_line(ax, [res_path[i].x, res_path[i+1].x], [res_path[i].y, res_path[i+1].y])
        # plt.pause(0.1)
    
    plt.savefig(name)

def findPathCost(res_path,tEdgets):
    cost=0
    tEdgetsAll = [item for sublist in tEdgets for item in sublist]
    for point in res_path:
        if(point.to_tuple() in tEdgetsAll):
            cost+=1.5
        else:
            cost+=1
    
    return cost
    pass
if __name__ == "__main__":
    text=""
    epolygons,eEdgets = gen_polygons('TestingGrid/world1_enclosures.txt')
    tpolygons,tEdgets = gen_polygons('TestingGrid/world1_turfs.txt')

    source = Point(8,10)
    dest = Point(43,45)
    

    
    # call all the algorithms and get the points
    # dfs call
    res_path,nodes_expanded=dfs((8,10),(43,45),eEdgets)
    cost=findPathCost(res_path,tEdgets)
    text+="dfs1\nPath cost: "+str(cost)+"\nNodes expanded: "+str(nodes_expanded)+"\n\n"
    saveImage(source,dest,res_path,"images/dfs1.png",epolygons,tpolygons)
    # BFS call
    res_path,nodes_expanded=bfs((8,10),(43,45),eEdgets)
    cost=findPathCost(res_path,tEdgets)
    text+="bfs1\nPath cost: "+str(cost)+"\nNodes expanded: "+str(nodes_expanded)+"\n\n"
    saveImage(source,dest,res_path,"images/bfs1.png",epolygons,tpolygons)
    
    # GBFS call (with SLD heuristic)
    res_path,nodes_expanded=gbfs((8,10),(43,45),eEdgets)
    cost=findPathCost(res_path,tEdgets)
    text+="gbfs1\nPath cost: "+str(cost)+"\nNodes expanded: "+str(nodes_expanded)+"\n\n"
    saveImage(source,dest,res_path,"images/gbfs1.png",epolygons,tpolygons)
    # A* call (with SLD heuristic)
    res_path,nodes_expanded=aStar((8,10),(43,45),eEdgets)
    cost=findPathCost(res_path,tEdgets)
    text+="astar1\nPath cost: "+str(cost)+"\nNodes expanded: "+str(nodes_expanded)+"\n\n"
    saveImage(source,dest,res_path,"images/aStar.png",epolygons,tpolygons)

    filename = "summary.txt"
    with open(filename, "w") as file:
        file.write(text)

    
