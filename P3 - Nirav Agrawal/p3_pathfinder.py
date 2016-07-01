from math import sqrt
from heapq import heappop, heappush

def find_path(source_point, destination_point, mesh):

    path = []
    visited_nodes = []
    source_box = find_box(source_point,mesh)
    destination_box = find_box(destination_point,mesh)
    detail_points = {source_box: source_point}
    backward_detail_points = {destination_box: destination_point}
    box_edges = {}
    previous_box = {}
    backward_previous_box = {}
    dist = {source_box: 0}
    backward_dist = {destination_box: 0}
    queue = []

    if source_box == None or destination_box == None:
        queue = None
    else:
        heappush(queue,(dist[source_box],source_box,'destination'))
        heappush(queue,(backward_dist[destination_box],destination_box,'source'))
    
    while queue:
        current_distance, current_box, current_goal = heappop(queue)
        
        if (current_box in previous_box and current_goal == "source") or (current_box in backward_previous_box and current_goal == "destination") or source_box == destination_box:

            path.extend(createPath(current_box,source_box,detail_points,previous_box))
            path.extend(createPath(current_box,destination_box,backward_detail_points,backward_previous_box))
            forwardLastPoint = detail_points[current_box] 
            backwardLastPoint = backward_detail_points[current_box]

            if path == []:
                path.append((source_point,destination_point))
                visited_nodes.append(source_box)
            else:
                path.append((forwardLastPoint,backwardLastPoint))
            
            break
 
        for adjacent in mesh['adj'][current_box]:
            if current_goal == "destination":
                current_y = detail_points[current_box][0]
                current_x = detail_points[current_box][1]
            if current_goal == "source":
                current_y = backward_detail_points[current_box][0]
                current_x = backward_detail_points[current_box][1]                

            new_y, new_x = findPoint((current_y,current_x),current_box,adjacent)
            
            if current_goal == "destination":
                distance = dist[current_box] + euclidean_distance(current_y,current_x,new_y,new_x)
                if adjacent not in dist or distance < dist[adjacent]:
                    priority = distance + euclidean_distance(destination_point[0],destination_point[1],new_y,new_x)
                    visited_nodes.append(adjacent)
                    dist[adjacent] = distance
                    heappush(queue,(priority,adjacent,current_goal))
                    previous_box[adjacent] = current_box
                    detail_points[adjacent] = (new_y,new_x)
                    
            elif current_goal == "source":
                distance = backward_dist[current_box] + euclidean_distance(current_y,current_x,new_y,new_x)
                if adjacent not in backward_dist or distance < backward_dist[adjacent]:
                    priority = distance + euclidean_distance(source_point[0],source_point[1],new_y,new_x)
                    visited_nodes.append(adjacent)
                    backward_dist[adjacent] = distance
                    heappush(queue,(priority,adjacent,current_goal))
                    backward_previous_box[adjacent] = current_box
                    backward_detail_points[adjacent] = (new_y,new_x)
        
    if path == []:
        print("No path!")

    return path, visited_nodes


def createPath(currentIteration,last_box,detail_points,previous_box):
    
    path = []
    while currentIteration != last_box:
        path.append((detail_points[currentIteration],detail_points[previous_box[currentIteration]]))
        currentIteration = previous_box[currentIteration]

    return path

def findPoint(current_point,selected_box,adjacent_box):
    
    new_point = [0,0]
    count = 0
    for index,coordinate in enumerate(current_point):
        max_coordinate = max(selected_box[count],adjacent_box[count])
        count += 1
        min_coordinate = min(selected_box[count],adjacent_box[count])
        count += 1
        if coordinate <= max_coordinate and coordinate >= min_coordinate:
            new_point[index] = coordinate
        elif coordinate < max_coordinate and coordinate < min_coordinate:
            new_point[index] = max_coordinate
        elif coordinate > max_coordinate and coordinate > min_coordinate:
            new_point[index] = min_coordinate
        else:
            new_point[index] = coordinate

    return new_point[0], new_point[1]

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
