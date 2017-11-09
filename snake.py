from collections import deque
import time
import random
import copy
class snake:
    queue = deque()
    food = [0, 0]
    hashset = {}
    direct_map = {"left" : [-1, 0], "right" : [1, 0], "up" : [0, 1], "down" : [0, -1]}
    def __init__(self):
        self.reset()
        self.update_food()
    def reset(self):
        self.queue.clear()
        self.hashset.clear()
        self.queue.append([0, 0])
        self.hashset["0&0"] = True
    def run(self, direction):
            new_point = copy.deepcopy(self.queue[0])
            new_point[0] += self.direct_map[direction][0]
            new_point[1] += self.direct_map[direction][1]
            if new_point[0] >= 10 or new_point[0] < 0 or new_point[1] >= 10 or new_point[1] < 0:
                return False
            if self.hashset.has_key(str(new_point[0])+"&"+str(new_point[1])):
                return False
            self.queue.appendleft(new_point)
            self.hashset[str(new_point[0])+"&"+str(new_point[1])] = True
            Got_food = False
            if new_point[0] != self.food[0] or new_point[1] != self.food[1]:
                tail = self.queue.pop()
                self.hashset.pop(str(tail[0])+"&"+str(tail[1]))
            else:
                self.update_food()
                Got_food = True
            return (self.queue,Got_food)
    def get_state(self):
        x, y = self.queue[0][0], self.queue[0][1]
        dir = [[0,0] for _ in range(0,4)]
        dir[0] = None if x == 0 else [x - 1, y]
        dir[1] = None if y == 0 else [x, y - 1]
        dir[2] = None if y == 9 else [x, y + 1]
        dir[3] = None if x == 9 else [x + 1, y]
        food = self.get_food()

        for i in range(0, 4):
            item = dir[i]
            if item == None:
                dir[i] = 0
            elif item[0] == food[0] and item[1] == food[1]:
                dir[i] = 2
            elif str(item[0]) + "&" + str(item[1]) in self.hashset:
                dir[i] = 1
            else:
                dir[i] = 3
        waypoint = None
        x_dist, y_dist = food[0] - x, food[1] - y
        x_dist_abs, y_dist_abs = abs(x_dist), abs(y_dist)
        if x_dist_abs > y_dist_abs:
            if x_dist < 0:
                waypoint = "up"
            else:
                waypoint = "down"
        else:
            if y_dist < 0:
                waypoint = "left"
            else:
                waypoint = "right" 
        return (dir[0], dir[3], dir[1], dir[2], waypoint)
    def get_food(self):
        return self.food
    def update_food(self):
        self.food[0] = random.randrange(10)
        self.food[1] = random.randrange(10)