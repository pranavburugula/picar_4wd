import picar_4wd as fc
import numpy as np
import signal
import sys
import time

class Car():
    def __init__(self):
        self.turn_radius = 13.97
        self.wheel_radius = 3.175
        self.orientation = 90
        self.position = (100,99)
        self.ANGLE_RANGE = 144
        self.STEP = 18
        self.us_step = self.STEP
        self.angles = np.array([i for i in range(-int(self.ANGLE_RANGE / 2), int(self.ANGLE_RANGE / 2) + self.STEP, self.STEP)])
        self.scans = []
        
        self.angle_distance = [0,0]
        self.current_angle = 0
        self.max_angle = self.ANGLE_RANGE/2
        self.min_angle = -self.ANGLE_RANGE/2
        self.scan_list = []
        self.num_scans_made = 0

        self.env_grid = np.zeros((100,200))

        fc.left_rear_speed.start()
        fc.right_rear_speed.start()
        signal.signal(signal.SIGINT, self._move_sig_handler)
    
    def __del__(self):
        fc.left_rear_speed.deinit()
        fc.right_rear_speed.deinit()

    def _move_sig_handler(self, signal, frame):
        fc.stop()
        self.__del__()
        sys.exit(0)

    def move_distance(self, dist, power):
        dist *= 2.54

        cur_dist = 0
        time.sleep(0.5)
        fc.forward(power)
        while cur_dist < dist:
            time.sleep(0.002)
            cur_dist += fc.speed_val() * 0.002
        fc.stop()

        new_x = self.position[0] + dist * np.cos(self.orientation)
        new_y = self.position[1] + dist * np.sin(self.orientation)
        self.position = (new_x, new_y)

    def turn_angle(self, angle, power):
        angle_rad = np.radians(np.abs(angle))
        arc_length = angle_rad * self.turn_radius

        left_dist = 0
        right_dist = 0
        time.sleep(0.5)
        fc.turn_right(power if angle >= 0 else -power)
        while np.abs(left_dist) < arc_length and np.abs(right_dist) < arc_length:
            time.sleep(0.002)
            left_dist += fc.left_rear_speed() * 0.002
            right_dist += fc.right_rear_speed() * 0.002
        fc.stop()

        self.orientation = (self.orientation - angle) % 360

    def set_orientation(self, angle, power):
        if self.orientation == angle:
            return
        
        turn_degrees = self.orientation - angle
        if np.abs(turn_degrees) > 180:
            turn_degrees = 360 + turn_degrees if turn_degrees < 0 else -1 * (360 - turn_degrees)
        
        self.turn_angle(turn_degrees, power)
        self.orientation = angle

    def scan_step(self):
        angle_steps = self.angles.copy()
        scan_reversed = False
        if self.current_angle == self.max_angle:
            angle_steps = np.flip(angle_steps)
            scan_reversed = True

        scan_list = []
        for angle in angle_steps:
            dist = fc.get_distance_at(angle)
            self.current_angle = angle
            scan_list.append(dist)
        

        if scan_reversed:
            # print("reverse")
            scan_list.reverse()
        # print(self.scan_list)
        return scan_list

    def update_map(self):
        cosines = np.cos(np.radians(self.angles + self.orientation))
        sines = np.sin(np.radians(self.angles + self.orientation))
        num_scans = 0
        while num_scans < 2:
            scan = np.array(self.scan_step())
            last = 0
            last_row = -1
            last_col = -1
            for i in range(len(scan)):
                if scan[i] < 0:
                    continue
                row = int((self.position[1] - (scan[i] * sines[i]) / 5))
                col = int(self.position[0] + (scan[i] * cosines[i] / 5))

                if row < 0 or col < 0 or col >= 200 or row >= 100:
                    continue
                
                if scan[i] > 0 and scan[i] <= 100:
                    self.env_grid[row][col] = 1
                    
                    # fill in line between this and last point as ones
                    if last == 1:
                        if col == last_col:
                            for i in range(last_row, row):
                                self.env_grid[i][col] = 1
                        else:
                            slope = (row - last_row) / (col - last_col)
                            for i in range(last_col if col > last_col else col, col if col > last_col else last_col):
                                self.env_grid[int(last_row + slope * (i - last_col))][i] = 1

                    
                    last = 1
                    last_row = row
                    last_col = col
                else:
                    last = 0

            num_scans += 1
        self.num_scans_made += 1
        np.savetxt("map_{num_scans}.csv".format(num_scans = self.num_scans_made), self.env_grid, delimiter=" ", fmt='%i')

    def get_env_grid(self):
        return self.env_grid
    def get_x(self):
        return self.position[0]
    def get_y(self):
        return self.position[1]