#!/usr/bin/env python
import rospy
from geometry_msgs.msg import PoseStamped
import socket
import json
from clover.srv import SetVelocity, SetVelocityRequest
from mavros_msgs.srv import CommandBool, CommandTOL, SetMode

# Initialize the ROS node
rospy.init_node('drone_velocity_controller', anonymous=True)

# Service proxy for setting velocity
set_velocity_service = rospy.ServiceProxy('/set_velocity', SetVelocity)



def start_server():
    """
    Starts a TCP server to listen for velocity commands and send back the current position.
    """
    host = ''
    port = 65000

    with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
        s.bind((host, port))
        s.listen()
        print("Waiting for a connection...")
        conn, addr = s.accept()
        while True:
            print('Connected by', addr)
            with conn:
                data = conn.recv(1024) # receive velocity setpoint
                if not data:
                    continue
                command = json.loads(data.decode('utf-8'))
                # Set velocity
                request = SetVelocityRequest(vx=command['vx'], vy=command['vy'], vz=command['vz'], frame_id='map', auto_arm=1)
                try:
                    response = set_velocity_service(request)
                    print(response)
                except rospy.ServiceException as e:
                    print("Service call failed: %s" % e)
                
                rospy.sleep(0.04)# need to be verify: control frequency 250Hz?

                

    def land(land=True):
        rospy.wait_for_service('/mavros/cmd/land')
        try:
            land_service = rospy.ServiceProxy('/mavros/cmd/land', CommandTOL)
            land_service(0.0, 0.0, 0.0, 0.0, 0.0)
            print("Landing starts.")
            rospy.sleep(10)
            print("Landing command completed.")
        except rospy.ServiceException as e:
            print("Service landing call failed: %s" % e)

if __name__ == '__main__':
    start_server()
