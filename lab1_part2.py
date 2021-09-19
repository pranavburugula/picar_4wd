import picar_4wd as fc
import numpy as np
import signal
import sys

ANGLE_RANGE = 180
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


def printA(grid):
    for row in grid:
        print(row)

def sig_handler(signal, frame):
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
    
signal.signal(signal.SIGINT, sig_handler)

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

        

        

