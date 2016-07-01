from math import sqrt
from heapq import heappop, heappush

def find_path(source_point, destination_point, mesh):

    path = []
    visited_nodes = []

    source_box = find_box(source_point,mesh)
    destination_box = find_box(destination_point,mesh)
    detail_points = {}
    box_edges = {}
    previous_box = {}
    dist = {}
    queue = []

    detail_points["destination"] = destination_point
    dist[source_box] = 0
    heappush(queue,(dist[source_box],source_box))

    while queue:
        current_distance, current_box = heappop(queue)
        detail_points[source_box] = source_point
        if current_box == destination_box:
            currentIteration = destination_box
            path.append((detail_points["destination"],detail_points[currentIteration]))
            while currentIteration != source_box:
                path.append((detail_points[currentIteration],detail_points[previous_box[currentIteration]]))
                currentIteration = previous_box[currentIteration]            
            visited_nodes.append(source_box)
            break

        for adjacent in mesh['adj'][current_box]:
            max_y = max(current_box[0],adjacent[0])
            min_y = min(current_box[1],adjacent[1])              
            max_x = max(current_box[2],adjacent[2])
            min_x = min(current_box[3],adjacent[3])
            current_y = detail_points[current_box][0]
            current_x = detail_points[current_box][1]
            
            new_x = 0 
            new_y = 0

            if current_x <= max_x and current_x >= min_x:
                new_x = current_x
            elif current_x < max_x and current_x < min_x:
                new_x = max_x
            elif current_x > max_x and current_x > min_x:
                new_x = min_x
            else:
                new_x = current_x
                
            if current_y <= max_y and current_y >= min_y:
                new_y = current_y
            elif current_y < max_y and current_y < min_y:
                new_y = max_y
            elif current_y > max_y and current_y > min_y:
                new_y = min_y
            else:
                new_y = current_y

            distance = dist[current_box] + euclidean_distance(current_y,current_x,new_y,new_x)
            if adjacent not in dist or distance < dist[adjacent]:
                priority = distance + euclidean_distance(destination_point[0],destination_point[1],new_y,new_x)
                visited_nodes.append(adjacent)
                dist[adjacent] = distance
                heappush(queue,(priority,adjacent))
                previous_box[adjacent] = current_box
                detail_points[adjacent] = (new_y,new_x)
        
    if path == []:
        print("No path!")

    return path, visited_nodes


def find_box(point,mesh):

    box = None
    
    for current_box in mesh['boxes']:
        y_point = point[0]
        x_point = point[1]

        y_box_initial = current_box[0]
        x_box_initial = current_box[2]
        y_box_final = current_box[1]
        x_box_final = current_box[3]
    
        if x_point >= x_box_initial and x_point <= x_box_final:
            if y_point >= y_box_initial and y_point <= y_box_final:
                box = current_box

    return box
    
def euclidean_distance(p1y,p1x,p2y,p2x):
    distance = sqrt((p1y-p2y)**2+(p1x-p2x)**2)
    return distance
