import rospy
from geometry_msgs.msg import Pose, PoseStamped
from nav_msgs.msg import Odometry, Path
from socket_server.srv import *
from websocket_server import WebsocketServer
from threading import Thread
import threading
from random import random
from std_msgs.msg import Bool
import time

host_ip_address = '10.110.6.115'
port = 1234
x_offset = 458
y_offset = 368
x_scale = 21.557
y_scale = 21.05
marco_pose_x = 0;
marco_pose_y = 0;

def init_ros():
    rospy.init_node('websocket_transmit_odom')
    rospy.Subscriber('/integrated_to_map',Odometry, odom_callback)
    rospy.Subscriber('/global_path',Path, path_callback)

def odom_callback(odom):
    global marco_pose_x; global marco_pose_y;
    x = odom.pose.pose.position.x
    y = odom.pose.pose.position.y 
    marco_pose_x = x_scale*x - x_offset;
    marco_pose_y = y_scale*y - y_offset;


def path_callback(path):
    path_string = ""
    sendit = True;
    if (len(path.poses) <=2):
        sendit = False

    for pose in path.poses:
        x = pose.pose.position.x
        y = pose.pose.position.y 
        x = x_scale*x - x_offset
        y = y_scale*y - y_offset
        path_string += str(-y)
        path_string += ' '
        path_string += str(-x)
        path_string += ','
    path_string = path_string[:-1]
    m = "path:"+path_string
    # print('sending path....',m)
    global server 
    for client in server.clients:
        try:
            if sendit:
                server.send_message(client,m)
        except:
            pass




def transmit_goal_pose(pixel_coordinates):
    px = pixel_coordinates.split(' ',1)[0].encode("utf-8").strip()
    py = pixel_coordinates.split(' ',1)[1].encode("utf-8").strip()
    px = int(px); py = int(py)
    x = (px+x_offset)/x_scale
    y = (py+y_offset)/y_scale
    # print('Computed coordinates %f %f '%(x,y))
    pose = Pose()
    pose.position.x = x 
    pose.position.y = y 

    m = "busy:1"
    global server 
    for client in server.clients:
        try:
            server.send_message(client,str(m))
        except:
            pass

    rospy.wait_for_service('/goal_channel')

    try:
        channel = rospy.ServiceProxy('/goal_channel', Goal)
        response = channel(pose)
        print('Goal coordinates %f %f sent'%(x,y))

        if response.status:
            x = "success";
            for client in server.clients:
                try:
                    server.send_message(client,x)
                except:
                    pass

            rospy.loginfo("Goal has been reached!")

        else:
            x = "fail";
            for client in server.clients:
                try:
                    server.send_message(client,x)
                except:
                    pass
                    
            rospy.loginfo("Goal has been reached!")
            rospy.loginfo("Something went wrong with service or with planning")

    except rospy.ServiceException as e:
        x = "fail";
        for client in server.clients:
            try:
                server.send_message(client,x)
            except:
                pass
        rospy.loginfo("Service call failed. Performing recovery strategy")
        rec_pub = rospy.Publisher("/recovery_from_stagnation", Pose, queue_size=1)
        rec_pub.publish(pose)

    m = "free:1"
    global server 
    for client in server.clients:
        try:
            server.send_message(client,str(m))
        except:
            pass


def transmit_stop_signal():
    stop_pub = rospy.Publisher("/terminate_planning", Bool, queue_size=1)
    stop_moving = Bool()
    stop_moving.data = True
    stop_pub.publish(stop_moving)
    print('stop signal')
    

def transmit_goal(client,server, message):
    pixel_coordinates = message
    if not '-409' in message:
        print(message)
        if pixel_coordinates == 'stop':
            transmit_stop_signal()

        else:
            if not 'NaN' in pixel_coordinates:
                transmit_stop_signal()
                transmit_goal_pose(pixel_coordinates)

# Called for every client connecting (after handshake)
def new_client(client, server):
    pass
    # print("New client connected and was given id %d" % client['id'])
    # server.send_message(client,"Hey all, a new client has joined us")
    # print "clients are"
    # print server.clients


# Called for every client disconnecting
def client_left(client, server):
    # print("Client(%d) disconnected" % client['id'])
    pass




# Called when a client sends a message
def message_received(client, server, message):
    if len(message) > 200:
        message = message[:200]+'..'
    print("Client(%d) said: %s" % (client['id'], message))


def transmit_odom():

    threading.Timer(0.25, transmit_odom).start()
    m = "odom:"+str(marco_pose_x)+","+str(marco_pose_y)
    global server 
    for client in server.clients:
        # print(client)
        try:
            server.send_message(client,str(m))

        except:
            # print("can't send to ",client['id'])
            pass

def send_odom():
    
    while True:
        # m  = random()
        m = "odom:"+str(marco_pose_x)+","+str(marco_pose_y)
        try:
            for client in server.clients:
                server.send_message(client,str(m))
        except:
            pass
            # print("web page disconnected")
            # server = WebsocketServer(host='10.110.6.102', port=PORT)

        time.sleep(0.25)


init_ros()
PORT=1234
server = WebsocketServer(host='10.110.6.115', port=PORT)
transmit_odom()
server.set_fn_new_client(new_client)
server.set_fn_client_left(client_left)
server.set_fn_message_received(transmit_goal)
server.run_forever()
