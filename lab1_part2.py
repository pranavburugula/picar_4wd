import picar_4wd as fc
import numpy as np
import signal
import sys
import time
from car import Car

ANGLE_RANGE = 180
TURN_RADIUS = 13.97
WHEEL_RADIUS = 3.175
STEP = 18
us_step = STEP
angle_distance = [0,0]
current_angle = 0
max_angle = ANGLE_RANGE/2
min_angle = -ANGLE_RANGE/2
scan_list = []
angles = []
scans = []

def scan_step():
    global scan_list, current_angle, us_step
    current_angle += us_step
    if current_angle >= max_angle:
        current_angle = max_angle
        us_step = -STEP
    elif current_angle <= min_angle:
        current_angle = min_angle
        us_step = STEP
    dist = fc.get_distance_at(current_angle) - current_angle * 0.2

    scan_list.append(dist)
    if current_angle == min_angle or current_angle == max_angle:
        if us_step < 0:
            # print("reverse")
            scan_list.reverse()
        # print(scan_list)
        tmp = scan_list.copy()
        scan_list = []
        return tmp
    else:
        return []

def move_distance(dist, power):
    dist *= 2.54

    cur_dist = 0
    time.sleep(0.5)
    fc.forward(power)
    while cur_dist < dist:
        time.sleep(0.002)
        cur_dist += fc.speed_val() * 0.002
    fc.stop()

def turn_angle(angle, power):
    angle_rad = np.radians(np.abs(angle))
    arc_length = angle_rad * TURN_RADIUS

    left_dist = 0
    right_dist = 0
    time.sleep(0.5)
    fc.turn_right(power if angle >= 0 else -power)
    while np.abs(left_dist) < arc_length and np.abs(right_dist) < arc_length:
        time.sleep(0.002)
        left_dist += fc.left_rear_speed() * 0.002
        right_dist += fc.right_rear_speed() * 0.002
    fc.stop()

def printA(grid):
    for row in grid:
        print(row)

def scan_sig_handler(signal, frame):
    global scans
    # scan_arr = np.array(scans)
    # np.save(scan_arr, "maps")
    map_to_save = scans[-2].astype(int)
    print(map_to_save)
    np.savetxt("map.csv", map_to_save, delimiter=" ", fmt='%i')
    # with open("map.txt", 'rw') as file:
    #     for row in map_to_save:
    #         file.write(str(row))

    sys.exit(0)

def move_sig_handler(signal, frame):
    fc.stop()
    sys.exit(0)

def scan_relative_map():
    signal.signal(signal.SIGINT, scan_sig_handler)

    angles = np.array([i for i in range(-int(ANGLE_RANGE / 2), int(ANGLE_RANGE / 2), STEP)])
    angles = np.radians(angles)
    cosines = np.cos(angles)
    sines = np.sin(angles)
    while 1:
        scan = np.array(scan_step())
        grid = np.zeros((100, 200))
        # print(cosines)
        if len(scan) > 0: 
            # scan[scan > 100] = -1
            # scan[scan < 0] = -1

            # angles = output[1]
            # print(scan)
            # print(angles)
            last = 0
            last_row = -1
            last_col = -1
            for i in range(len(scan)):
                # print(len(scan), len(cosines))
                row = int(100 - scan[i] * cosines[i])
                col = int(100 + scan[i] * sines[i])

                if row < 0 or col < 0 or col > 200:
                    continue
                
                # print(row, col, scan[i])
                if scan[i] > 0 and scan[i] <= 100:
                    grid[row - 1][col - 1] = 1
                    
                    # fill in line between this and last point as ones
                    if last == 1:
                        if col == last_col:
                            for i in range(last_row, row):
                                grid[i][col - 1] = 1
                        else:
                            slope = (row - last_row) / (col - last_col)
                            for i in range(last_col, col):
                                grid[int(last_row + slope * (i - last_col)) - 1][i] = 1

                    
                    last = 1
                    last_row = row
                    last_col = col
                else:
                    last = 0
                # else:
                #     grid[row - 1][col - 1] = 0


            # print(np.where(grid == 1))
            # printA(grid)
            scans.append(grid)

if __name__=="__main__":
    car = Car()
    # car.move_distance(20, 2)
    # car.turn_angle(-90, 2)
    # car.move_distance(5, 2)
    # car.set_orientation(90, 2)
    # car.set_orientation(180, 2)
    # car.set_orientation(270, 2)
    # car.set_orientation(0, 2)
    # car.set_orientation(200, 2)
    car.update_map()

    del car