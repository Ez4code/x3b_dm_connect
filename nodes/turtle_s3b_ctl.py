#!/usr/bin/env python3


import rospy
import codecs
import numpy
from geometry_msgs.msg import Twist
from digi.xbee.devices import XBeeDevice
from digi.xbee.models.message import XBeeMessage



if __name__== '__main__':



# Receiver the data from x3b

    msg = None
    device = XBeeDevice("/dev/ttyUSB0",9600)
    device.open()
    device.send_data_broadcast("hello life")
        

    rospy.init_node('turtle_s3b_ctl')
    topicName =  "/turtle1/cmd_vel"

    #def talker():
    pub = rospy.Publisher(topicName, Twist, queue_size=1000)

    while 1:

        twist = Twist()
        twist.linear.x = 0.0
        twist.angular.z = 0.0
        # endless loop if not receive data
        msg = device.read_data()
        if msg:
            rx_bytearray = msg.data
            rx_message = codecs.decode(rx_bytearray)
            print (rx_message)
            print(type(rx_message))

# Convert keyboard input to speed  //not done
    

            if rx_message == '1':
                twist.linear.x = 1.0
            if rx_message == '2':
                twist.linear.x = -1.0
            if rx_message == '3':
                twist.angular.z = 1.0
            if rx_message == '4':
                twist.angular.z = -1.0

            pub.publish(twist)
        
