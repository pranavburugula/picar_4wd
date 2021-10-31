import socket
import picar_4wd as fc
from picar_4wd import Speed
import time
import datetime
import os

HOST = "192.168.0.108" # IP address of your Raspberry PI
PORT = 1030          # Port to listen on (non-privileged ports are > 1023)
fc.stop()
with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
    s.bind((HOST, PORT))
    s.listen()

    try:
        distance = 0
        cur_time = 0
        direction = "stop"
        fc.left_rear_speed.start()
        fc.right_rear_speed.start()
        last_time = time.time_ns()
        while 1:
            client, clientInfo = s.accept()
            print("server recv from: ", clientInfo)
            data = client.recv(1024)      # receive 1024 Bytes of message in binary format
            if data == b"87\r\n":
                fc.forward(10)
                direction = "forward"
            elif data == b"83\r\n":
                fc.backward(10)
                direction = "backward"
            elif data == b"65\r\n":
                fc.turn_left(10)
                direction = "left"
            elif data == b"68\r\n":
                fc.turn_right(10)
                direction = "right"
            elif data == b"81\r\n":
                fc.stop()
                direction = "stop"

            cur_time = time.time_ns()
            if direction == "forward" or direction == "backward":
                distance += fc.speed_val() * (cur_time - last_time) / 10**9
            last_time = cur_time
            cpu_temp = os.popen("vcgencmd measure_temp").readline().replace("temp=", "")
            print(data)     
            return_data = "{dir},{speed},{dist},{temp}\r\n".format(dir = direction, speed = fc.speed_val(), dist = distance, temp = cpu_temp)

            client.sendall(bytes(return_data, 'utf-8'))
    except Exception as e: 
        print(e)
        print("Closing socket")
        client.close()
        s.close()    